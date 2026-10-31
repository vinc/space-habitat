"""Checks on the baseline: a torus built at rest and spun up finished (plan §2)."""

import unittest

from habitat_model import load, params
from structure_model import rest


class TestAtRest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = params(load())

    def test_pretension_squeezes_the_closed_ring(self):
        s, m, info = rest.at_rest(self.p, 900)
        self.assertIsNotNone(s)
        self.assertEqual(s["open"], 0)                       # every joint bears on its stops
        self.assertEqual(s["slack"], 0)
        self.assertLess(-s["hull_min"], rest.HULL_COMPRESSION)
        # The joints carry the chords' pull around the ring: the hull's compression times its area.
        self.assertAlmostEqual(s["joint_compression"] / (-s["hull_min"] * info["steel_area"]), 1, delta=0.05)

    def test_taut_and_within_compression_through_the_thermal_swing(self):
        for state in rest.thermal(self.p, 900).values():
            self.assertEqual(state["slack"], 0)
            self.assertLess(-state["hull_min"], rest.HULL_COMPRESSION)

    def test_no_buckling_in_the_plane(self):
        b = rest.buckling(self.p, 900)
        self.assertGreater(b["factor"], 10)



class TestLines(unittest.TestCase):
    """The hub's stabilising lines from rest to full spin, fixed-length and tension-only (review of #18)."""

    @classmethod
    def setUpClass(cls):
        cls.p = params(load())
        cls.lines = {r: rest.lines(cls.p, r) for r in (900, 1600)}

    def test_fixed_lines_at_the_finished_sizing_are_overloaded_by_the_bow(self):
        for ln in self.lines.values():
            self.assertGreater(ln["as_sized_ratio"], 1.3)

    def test_lines_sized_for_the_bow_hold_the_hub_throughout(self):
        sigma = self.p.wire_stress_mpa * 1e6
        for ln in self.lines.values():
            self.assertTrue(ln["taut"])
            self.assertLessEqual(max(ln["pull"]), ln["area"] * sigma)
            self.assertGreaterEqual(ln["margin_min"], 0.99 * ln["margin_finished"])
            self.assertLess(ln["dock_offset"], 0.1 * ln["gap_rest"])
            self.assertGreater(ln["gap_full"], 0.5 * ln["gap_rest"])

    def test_the_pull_grows_with_the_bow(self):
        ln = self.lines[900]
        # A fixed line takes up the whole bow: k_s (bow + d0) at full spin, the line and chord in series.
        self.assertGreater(ln["pull_full"], 10 * ln["service_preload"])
        self.assertAlmostEqual(ln["pull_in_full"], ln["bow"] + ln["d0"], delta=0.1 * ln["bow"])
        self.assertTrue(all(b >= a - 1e-6 for a, b in zip(ln["pull"], ln["pull"][1:])))

    def test_tension_share_is_continuous(self):
        ln = self.lines[900]
        lam = ln["lam_open"]
        self.assertAlmostEqual(rest.tension_share(lam - 1e-9, ln["s0"], lam), lam, places=6)
        self.assertAlmostEqual(rest.tension_share(0.0, ln["s0"], lam), ln["s0"])


class TestSpinUp(unittest.TestCase):
    def test_spin_up_from_rest_stays_within_the_finished_state(self):
        p = params(load())
        res = rest.spin_up(p, 900, scatter=False, record=(0.0, 0.1, 1.0))
        self.assertTrue(res["resolved"])
        self.assertLessEqual(res["chord_path_ratio"], 1.0 + 1e-6)
        self.assertEqual(res["final"]["open"], res["final"]["joints"])
        self.assertAlmostEqual(res["final"]["tension_max"] / res["tension_end"], 1.0, delta=0.01)
        self.assertLess(res["hull_final"], 0.05 * rest.HULL_COMPRESSION)
        self.assertGreater(res["spin_open"], 0.2)
        self.assertLess(res["spin_open"], 0.5)


class TestTorqueAndFill(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = params(load())

    def test_angular_acceleration_is_negligible(self):
        t = rest.torque(self.p, 900)
        self.assertLess(t["rim_ratio"], 1e-5)
        self.assertLess(t["laced_force"], 0.1 * t["line_capacity"])
        self.assertLess(rest.farm_twist(t, 0.02)["rest"], 0.01)
        self.assertLess(t["options"]["rock mass driver"]["energy"], t["options"]["water thrusters"]["energy"])

    def test_loose_fill_opens_the_side_walls(self):
        f = rest.fill(self.p, 900)
        self.assertGreater(min(d["slot_dose"] for d in f["loose"].values()), 10)
        self.assertLess(max(d["slot_dose"] for d in f["compacted"].values()), 3)
        self.assertLess(f["first_moment"], f["ballast"])

    def test_loose_cells_hold_less_shield(self):
        # A fixed volume filled loose holds rho_loose / rho_final of the design's rock (review of #18).
        f = rest.fill(self.p, 900)
        for d in f["loose"].values():
            self.assertAlmostEqual(d["areal"], self.p.shield_areal_t_m2 * d["density"] / self.p.rock_density)
            self.assertGreater(d["jacket_dose"], f["design_dose"])
            self.assertAlmostEqual(d["top_up"], d["strain"] * f["shield_mass"])
        for d in f["compacted"].values():
            self.assertEqual(d["areal"], self.p.shield_areal_t_m2)
            self.assertEqual(d["top_up"], 0.0)


if __name__ == "__main__":
    unittest.main()
