import math
import unittest

from habitat_model import Design, cavity, evaluate, load, params
from thermal_model import coolant, layout, sunlight, valley

P = params(load())


class TestCoolant(unittest.TestCase):
    def test_potential_and_centroid(self):
        self.assertAlmostEqual(coolant.potential(0.1, 900, 600), 0.01 * (900 ** 2 - 600 ** 2) / 2)
        self.assertAlmostEqual(coolant.annulus_centroid(499.999, 500.001), 500.0, places=3)

    def test_natural_circulation_balances_its_head(self):
        x = coolant.size_natural(57e6, 0.1047, 872, 630, 10, 12)
        friction, _ = coolant.pipe_drop(x["m_dot"], x["diameter"], x["length"])
        self.assertAlmostEqual(friction / x["head"], 1.0, places=3)
        self.assertAlmostEqual(x["m_dot"] * 12 * coolant.WATER["cp"] * 10, 57e6)

    def test_pumped_loop_works_against_buoyancy(self):
        x = coolant.size_pumped(96e6, 0.1047, 364, 680, 10, 12)
        self.assertGreater(x["opposing"], 0)
        flow = 12 * x["m_dot"] / coolant.WATER["rho"]
        self.assertAlmostEqual(x["pump_power"], flow * (x["friction"] + x["opposing"]) / 0.7)

    def test_liquid_column_suppresses_boiling(self):
        rim = coolant.two_phase_rim(0.1047, 872, 630, coolant.AMMONIA["rho_l"], coolant.AMMONIA)
        self.assertGreater(rim["t_sat"], 310)
        # Clausius-Clapeyron round trip at the reference point.
        self.assertAlmostEqual(coolant.saturation_temperature(coolant.AMMONIA["p_sat"], coolant.AMMONIA), 285.0)


class TestValley(unittest.TestCase):
    def test_capacity_alone_gives_a_triangle(self):
        # No soil, no cooling coupling: the temperature ramps up by (q - mean) t_on / C and back down.
        valley.SOILS["none"] = (1e-12, 1e-12)
        try:
            case = {"soil": "none", "pond_frac": 0.0, "pond_depth": 0.0, "biomass_water": 0.0}
            c = 1200.0 * 50
            s = valley.swing(case, 100.0, 12, 0.0, 50, 1200.0, harmonics=400)
            self.assertAlmostEqual(s["swing"], 100.0 * 0.5 * 0.5 * valley.DAY / c, delta=0.02 * s["swing"])
        finally:
            del valley.SOILS["none"]

    def test_wet_valley_swings_less(self):
        light = valley.light_on_floor(P, 12)
        air_c = valley.air_heat_capacity(P)
        dry = valley.swing(valley.CASES["Arid canyon"], light, 12, 7, 43, air_c)["swing"]
        wet = valley.swing(valley.CASES["Fern gully"], light, 12, 7, 43, air_c)["swing"]
        self.assertLess(wet, dry)

    def test_air_heat_capacity_follows_the_atmosphere(self):
        # 70 kPa at 288 K: ~0.85 kg/m3 of N2 and O2.
        self.assertAlmostEqual(valley.air_heat_capacity(P) / (0.852 * valley.AIR_CP), 1.0, delta=0.01)
        thin = params(load(), pressure_kpa=50)
        self.assertLess(valley.air_heat_capacity(thin), valley.air_heat_capacity(P))


class TestSunlight(unittest.TestCase):
    def test_edge_on_sees_nothing_and_a_tilt_follows_sin(self):
        d = Design(radius_m=900, n_tori=1, tiers_lit=3)
        g = evaluate(P, d)["geometry"]
        self.assertEqual(sunlight.absorbed(g, 1, 0.0, (1.0, 1.0))["farm"], 0.0)
        tilt = 2.0
        # A lone farm plane with its ring shrunk to nothing: only the hub shades it.
        bare = {**g, "farm_width": 1e-3, "farm_height": 1e-3}
        a = sunlight.absorbed(bare, 1, tilt, (0.0, 1.0), absorptivity=1.0, rays=80000)["farm"]
        r_in, r_out = cavity._farm_band(bare)
        expected = sunlight.SOLAR * math.sin(math.radians(tilt)) * math.pi * (r_out ** 2 - r_in ** 2)
        self.assertAlmostEqual(a / expected, 1.0, delta=0.08)
        # With its ring, the ring shades part of its own outboard panels.
        self.assertLess(sunlight.absorbed(g, 1, tilt, (0.0, 1.0), absorptivity=1.0, rays=80000)["farm"], a)

    def test_tori_shade_the_drum_at_small_tilts(self):
        d = Design(radius_m=900, n_tori=6, tiers_lit=3)
        g = evaluate(P, d)["geometry"]
        self.assertEqual(sunlight.absorbed(g, 6, 0.5, (1.0, 1.0))["main"], 0.0)
        self.assertGreater(sunlight.absorbed(g, 6, 5.0, (1.0, 1.0))["main"], 0.0)


class TestLayout(unittest.TestCase):
    def test_layouts(self):
        g = evaluate(P, Design(radius_m=900))["geometry"]
        self.assertEqual(cavity._farm_band(g, "inboard"), (g["hub_radius"] + 1.0, g["farm_radius"]))
        with self.assertRaises(ValueError):
            cavity._farm_band(g, "sideways")

    def test_smallest(self):
        points = [{"margin": 2.0, "panel_area": (3.0, 3.0)}, {"margin": 1.6, "panel_area": (1.0, 2.0)},
                  {"margin": 1.2, "panel_area": (0.5, 0.5)}]
        self.assertEqual(layout.smallest(points, 1.5)["panel_area"], (1.0, 2.0))
        self.assertIsNone(layout.smallest(points, 3.0))

    def test_sizing_coverage_falls_back_when_the_target_is_out_of_reach(self):
        met = {"least": {"coverage": (0.15, 0.2)}, "coverage": (1.0, 1.0)}
        self.assertEqual(layout.sizing_coverage(met), ((0.15, 0.2), True))
        unmet = {"least": None, "coverage": (1.0, 0.75)}
        self.assertEqual(layout.sizing_coverage(unmet), ((1.0, 0.75), False))

    def test_reach_search_keeps_the_other_overrides(self):
        seen = []

        def fake_check(p, d, lay, n_rays, grid=None):
            seen.append((p.radiator_temp_k, p.farm_radiator_outer_frac))
            return {"margin": 2.0 * p.farm_radiator_outer_frac}

        original = layout._check
        layout._check = fake_check
        try:
            reach = layout.reach_needed(load(), Design(radius_m=900, n_tori=6, tiers_lit=3), 1.5,
                                        overrides={"radiator_temp_k": 275.0}, steps=6)
        finally:
            layout._check = original
        self.assertTrue(all(t == 275.0 for t, _ in seen))
        self.assertAlmostEqual(reach, 0.75, delta=0.02)

    def test_passive_tiers(self):
        self.assertAlmostEqual(layout.passive_tiers({"farm": 0.5, "loads": (0, 300.0)}, 100.0), 1.5)


if __name__ == "__main__":
    unittest.main()
