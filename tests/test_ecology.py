import math
import unittest
from dataclasses import replace

from habitat_model import Design, evaluate, load, params
from ecology_model import closed, scenarios

P = params(load())
R = evaluate(P, Design(radius_m=900, n_tori=6, tiers_lit=3))


class TestClosed(unittest.TestCase):
    def setUp(self):
        self.c = replace(closed.config(P, R), leak=0.0)

    def test_carbon_is_conserved(self):
        for s in (closed.initial(self.c), closed.mature(self.c)):
            f = closed.fluxes(self.c, s, self.c.lit)
            total = f["d_co2"] + f["d_food"] + f["d_labile"] + f["d_stable"] + f["d_veg"]
            scale = f["uptake"] + f["soil"] + f["breathe_co2"]
            self.assertLess(abs(total), 1e-12 * scale)

    def test_a_mature_torus_holds_steady(self):
        s = closed.mature(self.c)
        f = closed.fluxes(self.c, s, self.c.lit)
        self.assertLess(abs(f["d_o2"]), 1e-9 * f["breathe_o2"])
        self.assertLess(abs(f["d_co2"]), 1e-9 * f["breathe_co2"])
        out = closed.run(self.c, 1.0, state=closed.mature(self.c))
        self.assertAlmostEqual(out["o2"][-1] / out["o2"][0], 1.0, places=6)
        self.assertAlmostEqual(out["co2"][-1] / out["co2"][0], 1.0, places=4)

    def test_people_breathe_their_food(self):
        # ~2,500 kcal a day costs ~0.7 kg of O2.
        o2 = self.c.food_c / self.c.rq * closed.M_O2 * closed.DAY
        self.assertAlmostEqual(o2, 0.74, delta=0.05)

    def test_farm_quasi_steady_balance(self):
        p_valley = 150.0
        uptake, x = closed.farm_uptake(self.c, p_valley, self.c.lit)
        supplied = self.c.exchange / (closed.R_GAS * self.c.temperature) * (p_valley - x)
        self.assertAlmostEqual(uptake / supplied, 1.0, places=9)
        # Saturating: more CO2, more uptake, but less than in proportion.
        more, _ = closed.farm_uptake(self.c, 2 * p_valley, self.c.lit)
        self.assertGreater(more, uptake)
        self.assertLess(more, 2 * uptake)

    def test_darker_farm_fails_sooner(self):
        _, rows = scenarios.failures(P, R, years=0.5)
        days = [r["co2_days"] for r in rows]
        self.assertTrue(all(d is not None for d in days[1:]))
        self.assertGreater(days[1], days[2])


class TestScenarios(unittest.TestCase):
    def test_choked_leak(self):
        # Air through an ideal orifice (discharge 1): ~0.0404 p A / sqrt(T) kg/s.
        row = scenarios.leak(P, R, diameters=(1.0,), discharge=1.0)[0]
        area = math.pi / 4
        coefficient = row["flow"] / (area * P.pressure_kpa * 1e3 / math.sqrt(P.air_temperature_k))
        self.assertAlmostEqual(coefficient, 0.0404, delta=0.0005)

    def test_biosphere2_replay(self):
        b = scenarios.biosphere2(P)
        self.assertAlmostEqual(b["series"]["o2_frac"][-1], scenarios.B2["o2_end"], places=3)
        self.assertGreater(b["excess_umol_m2_s"], 0.5)
        self.assertLess(b["excess_umol_m2_s"], 3.0)

    def test_composted_organics_ease_the_startup(self):
        _, _, _, raw = scenarios.startup(P, R, years=2.0)
        _, _, _, composted = scenarios.startup(P, R, years=2.0, soil_labile=closed.config(P, R).soil_labile / 6)
        self.assertLess(composted["regen_peak"], raw["regen_peak"])


if __name__ == "__main__":
    unittest.main()
