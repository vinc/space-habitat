import math
import unittest

import numpy as np

from habitat_model import Design, evaluate, load, params
from logistics_model import flows, propulsion, transfers, water

P = params(load())


class TestTransfers(unittest.TestCase):
    def setUp(self):
        transfers.ELEMENTS["Inner"] = (1.0, 0.0, 0.0, 0.0, 0.0)
        transfers.ELEMENTS["Outer"] = (1.524, 0.0, 0.0, 0.0, 0.0)

    def tearDown(self):
        del transfers.ELEMENTS["Inner"], transfers.ELEMENTS["Outer"]

    def test_lambert_follows_a_circular_orbit(self):
        r1, v1 = transfers.state(transfers.ELEMENTS["Inner"], np.array([0.0]))
        r2, v2 = transfers.state(transfers.ELEMENTS["Inner"], np.array([math.pi / 2]))
        t1, t2 = transfers.lambert(r1, r2, np.array([transfers.period(1.0) / 4]))
        np.testing.assert_allclose(t1, v1, rtol=1e-6, atol=1e-3)
        np.testing.assert_allclose(t2, v2, rtol=1e-6, atol=1e-3)

    def test_best_phase_between_circular_orbits_is_hohmann(self):
        a1, a2 = transfers.AU, 1.524 * transfers.AU
        mu = transfers.MU_SUN
        at = (a1 + a2) / 2
        hohmann = (math.sqrt(mu * (2 / a1 - 1 / at)) - math.sqrt(mu / a1)
                   + math.sqrt(mu / a2) - math.sqrt(mu * (2 / a2 - 1 / at)))
        dv, _, _, days = transfers.best_phase("Inner", "Outer")
        self.assertAlmostEqual(dv / hohmann, 1.0, delta=0.002)
        self.assertAlmostEqual(days, math.pi * math.sqrt(at ** 3 / mu) / transfers.DAY, delta=3)

    def test_synodic_period(self):
        # Earth and Eros (1.76-year orbit): ~2.3 years between windows.
        self.assertAlmostEqual(transfers.synodic_period("Earth", "Eros"), 2.31, delta=0.03)

    def test_reproduces_the_notes_ryugu_to_eros(self):
        dv, *_ = transfers.best_phase("Ryugu", "Eros")
        self.assertAlmostEqual(dv / 1e3, 4.5, delta=0.15)


class TestPropulsion(unittest.TestCase):
    def test_rocket_equation(self):
        ratio, energy = propulsion.per_kg(3000.0, 3000.0, 0.5)
        self.assertAlmostEqual(ratio, math.e - 1)
        self.assertAlmostEqual(energy, (math.e - 1) * 3000.0 ** 2)

    def test_energy_optimal_exhaust(self):
        dv = 4700.0
        ve = propulsion.energy_optimal_ve(dv)
        best = propulsion.per_kg(dv, ve, 1.0)[1]
        for f in (0.8, 0.95, 1.05, 1.25):
            self.assertGreater(propulsion.per_kg(dv, ve * f, 1.0)[1], best)

    def test_propellant_cap(self):
        dv = 4700.0
        ve = propulsion.energy_optimal_ve(dv, max_propellant_ratio=1.0)
        self.assertAlmostEqual(propulsion.per_kg(dv, ve, 1.0)[0], 1.0)

    def test_mass_driver_beats_fast_exhaust_on_energy(self):
        opts = propulsion.options(P, 4700.0, 1e8, 4e9, 1e8)
        self.assertLess(opts[2]["energy"], opts[0]["energy"])
        self.assertGreater(opts[2]["propellant"], opts[0]["propellant"])
        self.assertTrue(opts[2]["fits"])


class TestWater(unittest.TestCase):
    def setUp(self):
        self.d = Design(radius_m=900, n_tori=2, host_class="LL", site="Eros")
        self.r = evaluate(P, self.d)

    def test_budget_adds_up(self):
        b = water.budget(self.r)
        self.assertAlmostEqual(b["total"], self.r["mass"]["water_needed"], delta=1.0)

    def test_lakes_and_ballast(self):
        m, floor = self.r["mass"], self.r["geometry"]["floor_area"]
        self.assertAlmostEqual(m["water_lakes"], P.lake_floor_frac * P.lake_depth_m * 1e3 * floor)
        self.assertAlmostEqual(m["water_ballast"], 2 * P.ballast_frac * (m["rim"] - m["water_ballast"]), delta=1.0)

    def test_ballast_cancels_the_imbalance(self):
        # Water spread as A (1 - cos) around the rim, of the model's total, must cancel the first moment of an
        # unbalanced mass e M at the rim radius.
        m = self.r["mass"]
        r = 900.0
        theta = np.linspace(0, 2 * math.pi, 20001)[:-1]
        dtheta = theta[1] - theta[0]
        shape = 1 - np.cos(theta)
        density = m["water_ballast"] * shape / (np.sum(shape) * dtheta * r)     # kg per m of rim
        moment = np.sum(density * r * np.cos(theta) * r) * dtheta                  # x first moment, kg m
        imbalance = P.ballast_frac * (m["rim"] - m["water_ballast"]) * r
        self.assertAlmostEqual(-moment / imbalance, 1.0, places=6)

    def test_routes_charge_the_oxygen(self):
        w = water.routes(P, self.d, self.r)
        routes = list(w["routes"].values())
        self.assertLess(routes[1]["shipped"], routes[0]["shipped"])
        self.assertAlmostEqual(routes[1]["shipped"], routes[2]["shipped"], delta=1.0)   # methane's carbon offsets organics
        water_kg = self.r["materials"]["water_to_source"]
        self.assertAlmostEqual(w["hydrogen"] / water_kg, 0.1119, places=3)
        self.assertAlmostEqual(w["iron_for_oxygen"] / ((water_kg - w["hydrogen"]) / water.O_PER_FE), 1.0, places=3)
        o = w["local_oxygen"]
        iron = w["iron_for_oxygen"]
        self.assertAlmostEqual(o["moe_electric"], iron * P.moe_mj_kg_fe * 1e6)
        self.assertAlmostEqual(o["moe_heat"], iron * P.moe_heat_mj_kg_fe * 1e6)
        self.assertAlmostEqual(o["split"], water_kg * P.electrolysis_mj_kg_water * 1e6)
        # The iron replaces free metal, so less rock is mined (an LL host is sized by its metal).
        self.assertAlmostEqual(w["rock_saved"], iron / P.metal_wt_LL)
        self.assertAlmostEqual(routes[1]["other_energy"],
                               o["split"] + o["moe_electric"] + o["moe_heat"] - o["crushing_saved"])

    def test_supply_combinations(self):
        combos = water.supply(P, self.d, self.r)
        self.assertEqual(len(combos), 6)
        for (route, engine), v in combos.items():
            self.assertAlmostEqual(v["total"], v["shipping"] + v["other_energy"])
            if engine == "Mass driver":
                self.assertLess(v["shipping"], combos[(route, "Electric thrusters")]["shipping"])


class TestFlows(unittest.TestCase):
    def test_composition_and_rates(self):
        r = evaluate(P, Design(radius_m=900, n_tori=2, host_class="LL", site="Eros"))
        c = flows.composition(P, r)
        self.assertAlmostEqual(c["host"] + c["shipped"] + c["vitamins"], c["built"])
        self.assertGreater(c["local_share"], 0.95)
        a, b = flows.rates(r, 10, 5), flows.rates(r, 20, 5)
        self.assertAlmostEqual(a["s_type_day"] / b["s_type_day"], 2.0)

    def test_growth(self):
        d = Design(radius_m=900, n_tori=2, c_partner="Ryugu")
        g = flows.growth(P, d, evaluate(P, d), 10)
        self.assertAlmostEqual(g["after"][50], 2 * 2 ** 5)
        self.assertAlmostEqual(2 * 2 ** (g["years_to_c_limit"] / 10), g["c_type_supports"])


if __name__ == "__main__":
    unittest.main()
