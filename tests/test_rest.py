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

    def test_hub_held_at_rest(self):
        h = rest.hub_at_rest(self.p, 900, 0.02)
        self.assertLess(h["dock_offset"], 0.1 * h["gap"])


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
        self.assertGreater(min(d["dose"] for d in f["loose"].values()), 10)
        self.assertLess(max(d["dose"] for d in f["compacted"].values()), 3)
        self.assertLess(f["first_moment"], f["ballast"])


if __name__ == "__main__":
    unittest.main()
