"""Checks on the structural model (plan §2)."""

import math
import unittest

import numpy as np

from habitat_model import Design, evaluate, load, params
from habitat_model.mass import spoke_factor
from structure_model import cable_net, net_statics, spinup, wire
from structure_model.__main__ import main


class TestCableNet(unittest.TestCase):
    def setUp(self):
        self.p = params(load())
        self.sigma = self.p.wire_stress_mpa * 1e6

    def test_radial_limit_is_the_system_model(self):
        for v in (63, 94, 126, 157):
            uniform = cable_net.chord_mass_factor(v, self.sigma, self.p.steel_density, 1.0, tapered=False)
            self.assertAlmostEqual(uniform, spoke_factor(self.p, v))

    def test_taper_is_lighter_and_matches_the_notes(self):
        # Notes §12: taper factor exp(rho v^2 / 2 sigma) ~1.04 at 900 m, ~1.07 at 1.6 km.
        for r, expected in ((900, 1.04), (1600, 1.07)):
            res = evaluate(self.p, Design(radius_m=r, n_tori=1))
            g, m = res["geometry"], res["mass"]
            n = cable_net.compute(r, m["rim"], g["omega"], g["hub_radius"], self.sigma, self.p.steel_density)
            self.assertAlmostEqual(n["taper_ratio"], expected, delta=0.01)
            self.assertLess(n["mass_tapered"], n["mass_uniform"])
            # Chords weigh the same as radial spokes to well under 1%.
            self.assertLess(abs(n["chord_vs_radial"]), 0.01)

    def test_anchor_tension_balances_the_rim(self):
        n_chords, cos_t = 500, math.cos(0.07)
        t = cable_net.anchor_tension(1e10, 0.1, 900, n_chords, cos_t)
        self.assertAlmostEqual(2 * n_chords * t * cos_t, 1e10 * 0.01 * 900)

    def test_bowing_matches_numerical_integration(self):
        # y'' = -rho w^2 c / sigma for a uniform-stress chord, y(+-L) = 0.
        omega, c, L = 0.1047, 67.0, 897.0
        s = np.linspace(-L, L, 4001)
        curvature = self.p.steel_density * omega ** 2 * c / self.sigma
        y = curvature * (L ** 2 - s ** 2) / 2
        np.testing.assert_allclose(np.gradient(np.gradient(y, s), s)[10:-10], -curvature, rtol=1e-6)
        self.assertAlmostEqual(cable_net.bowing(omega, c, L, self.sigma, self.p.steel_density), y.max())


class TestSpinUp(unittest.TestCase):
    """Assembled statics: one tension per chord, rigid segments, joint springs (review on PR #2)."""

    def setUp(self):
        self.p = params(load())
        self.sigma = self.p.wire_stress_mpa * 1e6
        r = 900
        res = evaluate(self.p, Design(radius_m=r, n_tori=1))
        g, m = res["geometry"], res["mass"]
        self.r, self.g = r, g
        self.net = cable_net.compute(r, m["rim"], g["omega"], g["hub_radius"], self.sigma, self.p.steel_density)
        self.lam = m["rim"] / (2 * math.pi * r)

    def solve(self, arc, joints):
        return net_statics.solve(self.r, self.net["tangent_radius"], self.lam, self.g["omega"],
                                 self.net["wire_area_uniform"], self.p.steel_density, arc_length=arc,
                                 segment_length=self.g["width"], joints=joints, stress_pa=self.sigma)

    def test_finished_ring_matches_the_net_formula(self):
        s = self.solve(None, "sliding")
        self.assertTrue(s["equilibrium"])
        self.assertLess(s["residual"], 1e-6)
        self.assertEqual(s["slack_chords"], 0)
        self.assertAlmostEqual(float(np.mean(s["tensions"])) / self.net["tension_end"], 1, delta=0.02)

    def test_locked_joints_in_a_closed_ring_take_hoop_load(self):
        # Strain compatibility (notes §12): stiff joints along the rim make the hull a hoop.
        s = self.solve(None, "locked")
        self.assertGreater(s["joint_axial_max"] / s["hoop_full_ring"], 0.3)
        self.assertLess(s["tension_max"], self.net["tension_end"])

    def test_shortest_arcs_double_the_chord_load(self):
        arc = 4 * self.net["theta"] * self.r
        s = self.solve(arc, "locked")
        self.assertTrue(s["equilibrium"])
        self.assertAlmostEqual(s["tension_max"] / self.net["tension_end"], 2, delta=0.1)
        # Stresses scale with spin^2: the stage stays within the allowable only below ~0.7 of the final spin.
        self.assertAlmostEqual(s["max_spin_fraction"], 0.71, delta=0.03)
        # Joint tension close to the single-arc estimate of spinup.partial_arc (~1.1% of the hoop force).
        estimate = spinup.partial_arc(self.r, self.net["theta"], self.lam, self.g["omega"])
        self.assertAlmostEqual(s["joint_axial_max"] / estimate["joint_tension"], 1, delta=0.25)
        self.assertGreater(s["joint_axial_min"], 0)  # tension, not compression

    def test_sliding_joints_cannot_hold_a_partial_ring(self):
        s = self.solve(4 * self.net["theta"] * self.r, "sliding")
        self.assertFalse(s["equilibrium"])

    def test_imbalance(self):
        self.assertAlmostEqual(spinup.imbalance_offset(1e6, 900, 1e9), 0.9)


class TestWire(unittest.TestCase):
    def test_relaxation(self):
        self.assertEqual(wire.relaxation_1000h(0.3), 0)
        self.assertAlmostEqual(wire.relaxation_1000h(0.5), 0.05)
        # 1 GPa on 2 GPa wire over 900 m: 10% of 0.5% elastic strain, ~0.45 m.
        self.assertAlmostEqual(wire.creep_elongation(1e9, 2e9, 900), 0.45)

    def test_report_runs(self):
        from contextlib import redirect_stdout
        from io import StringIO
        out = StringIO()
        with redirect_stdout(out):
            self.assertEqual(main([]), 0)
        self.assertIn("Tangent-chord net", out.getvalue())


if __name__ == "__main__":
    unittest.main()


class TestUniformChordArea(unittest.TestCase):
    def test_uniform_chord_stays_within_the_allowable(self):
        p = params(load())
        sigma = p.wire_stress_mpa * 1e6
        for r in (900, 2500):
            res = evaluate(p, Design(radius_m=r, n_tori=1))
            g, m = res["geometry"], res["mass"]
            n = cable_net.compute(r, m["rim"], g["omega"], g["hub_radius"], sigma, p.steel_density)
            self.assertGreater(n["wire_area_uniform"], n["wire_area_tapered_end"])
            # Peak stress of the uniform chord, at mid-chord: end tension over its area plus its own spin load.
            peak = n["tension_end"] / n["wire_area_uniform"] + n["self_load_stress"]
            self.assertAlmostEqual(peak / sigma, 1, places=9)
            self.assertAlmostEqual(n["tension_mid_uniform"] / n["wire_area_uniform"], sigma, delta=1)
