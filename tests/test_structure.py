"""Checks on the structural model (plan §2)."""

import math
import unittest

import numpy as np

from habitat_model import Design, evaluate, load, params
from habitat_model.mass import spoke_factor
from structure_model import cable_net, net_statics, spinup, tube_section, wire
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

    def test_tension_only_law_holds_for_every_chord(self):
        # Review on PR #2: removed chords that stretch again must carry tension (T = k max(stretch, 0)).
        for factor, joints in ((3.9, "pinned"), (3.9, "locked"), (1, "locked"), (None, "sliding")):
            arc = None if factor is None else factor * 4 * self.net["theta"] * self.r
            s = self.solve(arc, joints)
            expected = s["chord_stiffness"] * np.maximum(s["stretch"], 0)
            np.testing.assert_allclose(s["tensions"], expected, rtol=0, atol=1e-6 * self.net["tension_end"])
            if s["equilibrium"]:
                self.assertTrue(s["converged"])
                self.assertLess(s["residual"], 1e-3)

    def test_large_displacement_stages_stay_unresolved(self):
        # Review on PR #2: the 803 m pinned arcs rotate segments by ~107 degrees; no spin limit may be claimed.
        s = self.solve(3 * 4 * self.net["theta"] * self.r, "pinned")
        self.assertFalse(s["equilibrium"])
        self.assertGreater(s["max_rotation"], net_statics.ROTATION_LIMIT)
        self.assertIsNone(s["max_spin_fraction"])
        self.assertEqual(s["status"], "outside the small-displacement range")

    def test_resolved_stages_are_kinematically_small(self):
        s = self.solve(4 * self.net["theta"] * self.r, "locked")
        self.assertTrue(s["equilibrium"])
        f2 = min(1.0, s["max_spin_fraction"]) ** 2
        self.assertLessEqual(s["max_rotation"] * f2, net_statics.ROTATION_LIMIT)
        self.assertLessEqual(s["max_displacement"] * f2, net_statics.DISPLACEMENT_LIMIT * self.r)

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
        self.assertIn("Tube cross-section", out.getvalue())


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


class TestTubeSection(unittest.TestCase):
    """The tube's cross-section by finite elements (plan §2.1)."""

    @classmethod
    def setUpClass(cls):
        cls.p = params(load())
        cls.runs = {a: tube_section.run(cls.p, 900, a, "vaulted") for a in tube_section.ANCHORS}

    def test_quad_patch(self):
        # A uniform strain gives a uniform stress and balanced nodal forces.
        square = np.array([[[0.0, 0.0], [2.0, 0.0], [2.0, 1.0], [0.0, 1.0]]])
        k = tube_section.quad_unit_stiffness(square)[0]
        u = np.zeros(8)
        u[0::2] = 1e-3 * square[0, :, 0]
        np.testing.assert_allclose(k @ u @ np.tile([0.0, 1.0], 4), 0, atol=1e-3)
        np.testing.assert_allclose((k @ u)[0::2].sum(), 0, atol=1e-3)
        b, _ = tube_section._b_matrix(square, 0.0, 0.0)
        stress = tube_section._plane_stress() @ b[0] @ u
        e = tube_section.E / (1 - tube_section.NU ** 2) * 1e-3
        np.testing.assert_allclose(stress, [e, tube_section.NU * e, 0], rtol=1e-9)

    def test_pressure_alone_gives_the_hoop_force(self):
        inp = self.runs["sides"]["inputs"]
        from dataclasses import replace
        bare = replace(inp, rock_density=0.0, floor_mass=0.0, omega=0.0, bumper=0.0)
        model = tube_section.Model(bare, "sides")
        nt, ne = model.mesh.nt, len(model.mesh.quads)
        s = model.solve(np.full(nt, 0.01), np.full(nt, 0.01), np.full(ne, 1e-9))
        np.testing.assert_allclose(s["n_hull"], inp.pressure * inp.a, rtol=0.01)

    def test_equilibrium_and_rim_load(self):
        res = evaluate(self.p, Design(radius_m=900, n_tori=1))
        g, m = res["geometry"], res["mass"]
        for r in self.runs.values():
            self.assertAlmostEqual(r["reaction_sum"] / r["load"], 1, places=6)
        # The load per metre is about the rim's (with the system model's hull) at the centre line.
        centre = g["radius"] - g["tube_radius"]
        rim_load = m["rim"] / (2 * math.pi * centre) * g["omega"] ** 2 * centre
        self.assertAlmostEqual(self.runs["sides"]["load"] / rim_load, 1, delta=0.03)

    def test_anchors_at_the_sides(self):
        crest, sides, fan = (self.runs[a]["per_torus"]["total"] for a in ("crest", "sides", "fan"))
        self.assertGreater(crest, 2 * sides)
        self.assertAlmostEqual(fan / sides, 1, delta=0.05)
        # In the fan, the side anchors take most of the load.
        forces = self.runs["fan"]["anchor_force"]
        self.assertGreater((forces[90] + forces[270]) / self.runs["fan"]["load"], 0.8)

    def test_fully_stressed_at_every_integration_point(self):
        for name in ("sides", "fan"):
            r = self.runs[name]
            inp = r["inputs"]
            self.assertTrue(r["converged"], name)
            self.assertLessEqual(r["utilisation"], 1.02)
            self.assertLessEqual(r["solution"]["utilisation"].max(), 1.02)
            self.assertTrue((r["t_hull"] >= inp.skin_min).all() and (r["t_outer"] >= inp.skin_min).all())
            self.assertTrue((r["tau"] >= inp.wall_min / inp.cell - 1e-12).all())

    def test_sizing_converges_at_every_size(self):
        # Review on PR #4: local stresses, not just the total mass, must settle.
        for r in (400, 1600, 2500):
            out = tube_section.run(self.p, r, "sides", "vaulted")
            self.assertTrue(out["converged"], r)
            self.assertLessEqual(out["utilisation"], 1.02)

    def test_unfinished_sizing_is_flagged(self):
        inp = self.runs["sides"]["inputs"]
        out = tube_section.Model(inp, "sides").size(max_iter=2)
        self.assertFalse(out["converged"])
        self.assertFalse(out["sized"])
        self.assertGreater(out["utilisation"], 1.02)

    def test_allowance_is_continuous(self):
        k = tube_section.COMPRESSION_KNOCKDOWN
        a = tube_section.allowance
        self.assertEqual(float(a(np.array(1.0), np.array(0.5))), 1.0)
        self.assertAlmostEqual(float(a(np.array(-1.0), np.array(-0.2))), k)
        self.assertAlmostEqual(float(a(np.array(1.0), np.array(-1.0))), (1 + k) / 2)
        self.assertAlmostEqual(float(a(np.array(1.0), np.array(-1e-9))), 1.0, places=6)

    def test_rock_rests_on_the_walls(self):
        # Review on PR #4: the rock's weight enters at the hull or the outer wall, never inside the jacket.
        inp = self.runs["sides"]["inputs"]
        for ceiling in tube_section.CEILINGS:
            m = tube_section.Model(inp, "sides", ceiling)
            f = m.f_fixed.reshape(-1, 2)
            interior = m.mesh.columns[:, 1:-1].ravel()
            np.testing.assert_allclose(f[interior], 0, atol=1e-9)
            # The rock goes on the outer wall (floor side; and hub side when hung) or on the hull (hub side,
            # vaulted), in full: rock + bumper on the outer wall, rock + fill + pressure on the hull.
            hub_side = np.cos(m.mesh.phi) < 0
            outer_x = f[m.mesh.outer_nodes, 0]
            hull_x = f[m.mesh.hull_nodes, 0]
            if ceiling == "hung":
                self.assertGreater(outer_x[hub_side].sum(), 0)
            else:
                self.assertLess(abs(outer_x[hub_side].sum()), 0.01 * m.rock_load)
            total = f[:, 0].sum()
            fill = inp.floor_mass * inp.omega ** 2 * inp.centre
            self.assertAlmostEqual((total - m.rock_load) / (fill + m.bumper_mass * inp.omega ** 2 * inp.centre), 1,
                                   delta=0.05)
            self.assertGreater(hull_x.sum() + outer_x.sum(), 0.99 * total)

    def test_fittings_pass_on_no_couple(self):
        # Review on PR #4: a tension-only chord passes on a force at its attachment, not a moment.
        for name, r in self.runs.items():
            s = r["solution"]
            for j in s["anchors"]:
                self.assertLess(abs(s["moment"][j]), 1e-6 * r["load"], name)
        # The fitting does turn about the attachment (the line's x displacements aren't all equal).
        s = self.runs["sides"]["solution"]
        column = tube_section.Mesh(self.runs["sides"]["inputs"]).columns[s["anchors"][0]]
        ux = s["u"][2 * column]
        self.assertGreater(np.ptp(ux), 1e-6)
        self.assertAlmostEqual(float(ux[-1]), 0.0, places=12)

    def test_close_to_the_system_model_at_900_m(self):
        r = self.runs["sides"]
        self.assertAlmostEqual(r["per_torus"]["total"] / r["model_hull_frames"], 1, delta=0.3)

    def test_mesh_converged(self):
        coarse = self.runs["sides"]["per_metre"]["total"]
        fine = tube_section.run(self.p, 900, "sides", "vaulted", n_radial=6, n_around=216)["per_metre"]["total"]
        self.assertAlmostEqual(fine / coarse, 1, delta=0.01)


class TestHub(unittest.TestCase):
    """The hub held in the two chord nets by stabilising lines (plan §2)."""

    @classmethod
    def setUpClass(cls):
        from structure_model import hub
        cls.hub = hub
        cls.p = params(load())
        cls.out = {}
        for r in (400, 900, 1600, 2500):
            res = evaluate(cls.p, Design(radius_m=r, n_tori=1))
            cls.out[r] = hub.compute(cls.p, res["geometry"], res["mass"])

    def test_chord_stiffness_is_a_taut_string(self):
        k = self.hub.chord_stiffness(5e7, 900.0, 400.0, 0.0)
        self.assertAlmostEqual(k, 2 * 5e7 / 900)
        # Its own spin load softens it a little: 2 T beta cot(beta L) < 2 T / L.
        soft = self.hub.chord_stiffness(5e7, 900.0, 400.0, 0.105)
        beta = math.sqrt(400 * 0.105 ** 2 / 5e7)
        self.assertAlmostEqual(soft, 2 * 5e7 * beta / math.tan(beta * 900))
        self.assertLess(soft, k)
        self.assertAlmostEqual(soft / k, 1 - (beta * 900) ** 2 / 3, delta=1e-3)

    def test_two_bodies_balance(self):
        mt, mh, k, w, ft, fh = 1e10, 3e8, 6e7, 0.1, 2e6, -5e5
        res = self.hub.two_bodies(mt, mh, k, w, ft, fh)
        w2 = w * w
        self.assertAlmostEqual((mt * w2 * res["x_torus"] + mh * w2 * res["x_hub"] + ft + fh) / ft, 0, places=9)
        self.assertAlmostEqual(mh * w2 * res["x_hub"] - res["force"] + fh, 0, delta=1e-6 * abs(ft))

    def test_finished_nets_hold_the_hub(self):
        for r, out in self.out.items():
            self.assertGreater(out["margin"], 5, r)
            self.assertGreater(out["natural_vs_spin"], 2, r)
            # Lines much stiffer than chords: the nets give about N k_chord / 2 per plane.
            self.assertAlmostEqual(out["k_plane"] / (out["n_lines"] / 2 * out["k_chord"] / 2), 1, delta=0.1)
            for case in out["cases"].values():
                self.assertLess(abs(case["relative"]), out["gap"] / 10)
            # Light lines: well under 0.1% of the torus.
            self.assertLess(out["line_mass"], 1e-3 * out["torus_mass"])

    def test_one_pair_cannot_hold_the_hub_two_can(self):
        for r, out in self.out.items():
            self.assertFalse(out["build"][1]["stable_unbraced"], r)
            self.assertTrue(out["build"][2]["stable_unbraced"], r)
            self.assertLess(abs(out["build"][2]["offset"]), abs(out["build"][1]["offset"]))
            self.assertLess(abs(out["build"][2]["offset"]), out["gap"])

    def test_axial_hold_needs_inclined_lines(self):
        for r, out in self.out.items():
            self.assertLess(out["axial_natural_vs_spin"], 1, r)
            self.assertGreater(out["k_axial_inclined"], 5 * out["k_axial"], r)


class TestHubReview(unittest.TestCase):
    """Review on PR #5: Coriolis modes, taut lines while building, inclined length, consistent sizing."""

    @classmethod
    def setUpClass(cls):
        from structure_model import hub
        cls.hub = hub
        cls.p = params(load())
        cls.out = {}
        for r in (400, 900, 2500):
            res = evaluate(cls.p, Design(radius_m=r, n_tori=1))
            cls.out[r] = (hub.compute(cls.p, res["geometry"], res["mass"]), res["geometry"])

    def test_isotropic_modes_split_by_the_spin(self):
        mu, k, w = 2e8, 6e7, 0.1
        m = self.hub.modes(mu, k, k, w)
        wn = math.sqrt(k / mu)
        np.testing.assert_allclose(m["frequencies"], [abs(wn - w), wn + w], rtol=1e-9)
        self.assertEqual(m["growth"], 0.0)

    def test_asymmetric_rotor_grows_between_its_frequencies(self):
        mu, w = 1e8, 0.1
        grows = self.hub.modes(mu, 0.5 * mu * w * w, 3 * mu * w * w, w)
        self.assertGreater(grows["growth"], 0)
        stable = self.hub.modes(mu, 1.5 * mu * w * w, 3 * mu * w * w, w)
        self.assertEqual(stable["growth"], 0.0)

    def test_finished_modes_in_the_rotating_frame(self):
        for r, (out, geo) in self.out.items():
            wn = math.sqrt(out["k_torus"] / out["reduced_mass"]) / geo["omega"]
            np.testing.assert_allclose(out["rotating_vs_spin"], [wn - 1, wn + 1], rtol=1e-6)
            self.assertAlmostEqual(out["natural_vs_spin"], wn)
            self.assertEqual(out["growth"], 0.0)

    def test_load_cases_use_the_final_stiffness(self):
        for r, (out, _) in self.out.items():
            for case in out["cases"].values():
                self.assertAlmostEqual(case["force"] / (out["k_torus"] * case["relative"]), 1, places=9)

    def test_lines_stay_taut_and_within_the_wire_stress(self):
        sigma = self.p.wire_stress_mpa * 1e6
        for r, (out, _) in self.out.items():
            self.assertGreater(out["service_preload"], out["service_swing"])
            self.assertLessEqual((out["service_preload"] + out["service_swing"]) / out["line_area"], sigma * (1 + 1e-6))
            first = out["build"][out["build_pairs"]]
            self.assertGreaterEqual(first["preload"], self.hub.TAUT_MARGIN * first["swing"] * (1 - 1e-6))
            self.assertLessEqual(first["line_stress"], sigma * (1 + 1e-6))
            self.assertEqual(first["growth"], 0.0)
            # A single pair without preload is an asymmetric rotor: the hub's motion grows.
            self.assertGreater(out["build"][1]["growth_unbraced"], 0)

    def test_inclined_lines_use_their_length(self):
        hub = self.hub
        for r, (out, _) in self.out.items():
            length = math.hypot(out["gap"], out["plane_offset"])
            self.assertAlmostEqual(out["inclined_length"], length)
            k = hub.series(out["k_chord"], hub.E_WIRE * out["line_area"] / length)
            expected = hub.INCLINED_FRAC * out["n_lines"] * k * math.sin(out["inclination"]) ** 2
            self.assertAlmostEqual(out["k_axial_inclined"] / expected, 1, places=9)
