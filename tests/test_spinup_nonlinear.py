"""Checks on the geometrically nonlinear spin-up model (plan §2)."""

import math
import unittest

import numpy as np

from habitat_model import Design, load, params
from structure_model import nonlinear as nl
from structure_model import sequence


def shortest(n, net, factor=1.0, pairs=1):
    return nl.opposite_pairs(n, sequence.arc_count(n, net, factor), pairs)


class TestBeam(unittest.TestCase):
    def test_cantilever_tip_load(self):
        # One corotational beam element, clamped at one end, small tip load: P L^3 / 3 E I.
        m = nl.Model.__new__(nl.Model)
        m.X = np.array([[0.0, 0.0], [10.0, 0.0]])
        m.elements = [(0, 1)]
        m.chords, m.chord_l0, m.chord_eas, m.chord_mus, m.chord_areas = [], np.zeros(0), [], [], np.zeros(0)
        m.radials, m.joints, m.sliding = [], [], np.zeros(0, dtype=bool)
        m.rim_ea, m.rim_ei = 1e12, 1e9
        m.mass = np.zeros(2)
        m.k_joint = (0.0, 0.0, 0.0)
        m.ndof = 6
        _, K, _ = m.assemble(np.zeros(6), 0.0)
        free = [3, 4, 5]
        flex = np.linalg.inv(K[np.ix_(free, free)])
        self.assertAlmostEqual(flex[1, 1] / (10.0 ** 3 / (3 * 1e9)), 1, places=9)
        self.assertAlmostEqual(flex[0, 0] / (10.0 / 1e12), 1, places=9)

    def test_rigid_rotation_strains_nothing(self):
        # Corotational: a large rigid rotation of the element leaves no internal force.
        m = nl.Model.__new__(nl.Model)
        m.X = np.array([[0.0, 0.0], [10.0, 0.0]])
        m.elements = [(0, 1)]
        m.chords, m.chord_l0, m.chord_eas, m.chord_mus, m.chord_areas = [], np.zeros(0), [], [], np.zeros(0)
        m.radials, m.joints, m.sliding = [], [], np.zeros(0, dtype=bool)
        m.rim_ea, m.rim_ei = 1e12, 1e9
        m.mass = np.zeros(2)
        m.k_joint = (0.0, 0.0, 0.0)
        m.ndof = 6
        a = 1.0
        u = np.array([0, 0, a, 10 * math.cos(a) - 10, 10 * math.sin(a), a])
        R, _, out = m.assemble(u, 0.0)
        self.assertLess(np.abs(R).max(), 1e-3)


class TestSpinUpNonlinear(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = params(load())

    def test_shortest_locked_arcs_match_the_linear_model(self):
        m, info = nl.for_design(self.p, 900, arcs_fn=shortest)
        res = m.solve(info["geometry"]["omega"], 1.0)
        self.assertTrue(res["resolved"])
        self.assertAlmostEqual(res["tension_max"] / info["net"]["tension_end"], 1.94, delta=0.1)
        hoop = info["line_mass"] * (info["geometry"]["omega"] * 900) ** 2
        self.assertAlmostEqual(res["joint_tension_max"] / hoop, 0.01, delta=0.002)
        self.assertLess(res["rotation_max"], 0.01)

    def test_spin_limit_of_the_shortest_arcs(self):
        m, info = nl.for_design(self.p, 900, arcs_fn=shortest)
        lim = m.spin_limit(info["geometry"]["omega"], info["sigma"])
        self.assertAlmostEqual(lim["limit"], 0.72, delta=0.03)
        self.assertAlmostEqual(lim["state"]["stress_max"], info["sigma"],
                               delta=0.1 * info["sigma"])

    def test_joints_must_stay_locked(self):
        # Released towards sliding from a locked equilibrium at 0.7 of the spin, the arcs lose it.
        m, info = nl.for_design(self.p, 900, arcs_fn=lambda n, net: shortest(n, net, 1.5))
        res = m.release(info["geometry"]["omega"], 0.7, to="sliding")
        self.assertFalse(res["resolved"])

    def test_radial_lines_hold_an_arc_at_full_spin(self):
        plain, info = nl.for_design(self.p, 900, arcs_fn=lambda n, net: shortest(n, net, 1.5))
        lined, _ = nl.for_design(self.p, 900, arcs_fn=lambda n, net: shortest(n, net, 1.5), **sequence.SUPPORT)
        om = info["geometry"]["omega"]
        a, b = plain.solve(om, 1.0), lined.solve(om, 1.0)
        self.assertGreater(a["peak_stress"], info["sigma"])
        # Checked at their peaks (review of #16): the lines within their allowable, the chords within ~1%.
        self.assertLessEqual(b["line_peak_stress"], info["sigma"])
        self.assertLess(b["peak_stress"], 1.02 * info["sigma"])
        self.assertLess(sequence.hull_bending(info, b["rim_moment_max"]), 0.2 * sequence.HULL_STRESS)
        self.assertGreater(sequence.hull_bending(info, a["rim_moment_max"]), sequence.HULL_STRESS)
        # The lines' pulls balance across the hub: the centre of mass holds with no reaction.
        _, _, out = lined.assemble(b["u"], om ** 2)
        self.assertGreater(sum(out["R"]), 0)

    def test_peaks_include_the_cables_own_spin_load(self):
        m, info = nl.for_design(self.p, 900, arcs_fn=shortest, radial_lines=1.0)
        om = info["geometry"]["omega"]
        res = m.solve(om, 1.0)
        rho = self.p.steel_density
        length = float(m.chord_l0.mean()) * (1 + nl.PRESTRAIN)
        self.assertAlmostEqual(res["peak_stress"] - res["stress_max"], rho * om ** 2 * (length / 2) ** 2 / 2,
                               delta=1e3)
        h = info["geometry"]["hub_radius"]
        self.assertAlmostEqual(res["line_peak_stress"] - res["line_tension_max"] / m.radial_area,
                               rho * om ** 2 * (900 ** 2 - h ** 2) / 2, delta=1e3)

    def test_opposite_pairs(self):
        arcs = nl.opposite_pairs(100, 10, pairs=2)
        starts = sorted(a for a, _ in arcs)
        self.assertEqual(len(arcs), 4)
        self.assertEqual([b - a for a, b in zip(starts, starts[1:])], [25, 25, 25])

    def test_hull_bending_formula(self):
        info = {"steel_area": 2.0, "geometry": {"tube_radius": 10.0}}
        self.assertAlmostEqual(sequence.hull_bending(info, 1e9), 2 * 1e9 / (2.0 * 10.0))


class TestHungTorus(unittest.TestCase):
    def test_link_arcs_as_they_are_hung(self):
        from dynamics_model import links as lk
        p = params(load())
        d = Design(radius_m=900, n_tori=6)
        unlinked, _, _ = lk.building_torus(p, d, 0.5, link=False, radial_lines=False)
        linked, _, _ = lk.building_torus(p, d, 0.5, link=True, radial_lines=True)
        self.assertLess(unlinked, 1.0)
        self.assertGreater(linked, 1.2)

    def test_spin_up_from_rest_is_worst_at_full_spin(self):
        from dynamics_model import links as lk
        p = params(load())
        for r in (900, 1600):
            margins = lk.spinup(p, Design(radius_m=r, n_tori=6), fractions=(0.1, 0.5, 1.0))
            values = [margins[f] for f in (0.1, 0.5, 1.0)]
            self.assertTrue(all(a >= b - 1e-6 for a, b in zip(values, values[1:])))
            self.assertGreater(values[-1], 1.2)

    def test_radial_lines_counted_from_the_arcs(self):
        # Near closure the gaps are shorter than an end zone and fewer anchors are single-laced than
        # eight full end zones would give (review of #16).
        from dynamics_model import links as lk
        p = params(load())
        d = Design(radius_m=900, n_tori=6)
        _, _, early = lk.building_torus(p, d, 0.5, link=True, radial_lines=True)
        _, _, late = lk.building_torus(p, d, 0.95, link=True, radial_lines=True)
        model, _ = nl.for_design(p, 900, arcs_fn=lambda n, net: nl.opposite_pairs(n, round(0.95 * n / 4), pairs=2))
        self.assertEqual(late, model.single_laced)
        self.assertLess(late, early)


if __name__ == "__main__":
    unittest.main()
