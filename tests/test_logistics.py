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


class TestEphemeris(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from logistics_model.ephemeris import Ephemeris
        cls.e = Ephemeris()

    def test_interpolation_hits_the_table(self):
        from logistics_model.ephemeris import KM
        jd = self.e.jd[100]
        r, v = self.e.state("Eros", np.array([jd]))
        self.assertTrue(np.allclose(r[0], self.e.tables["Eros"][100, :3] * KM))
        self.assertTrue(np.allclose(v[0], self.e.tables["Eros"][100, 3:] * KM))

    def test_interpolation_between_samples_follows_kepler(self):
        # Halfway between two samples, against a two-body propagation from the first: Eros meets no planet
        # closely, so the two agree to well under a km/s of Δv precision (positions to ~100 km).
        from logistics_model.ephemeris import DAY, KM
        k = 400
        jd0 = self.e.jd[k]
        r0, v0 = self.e.tables["Eros"][k, :3] * KM, self.e.tables["Eros"][k, 3:] * KM
        r_mid, v_mid = self.e.state("Eros", np.array([jd0 + 5.0]))
        # Two-body step by fine RK4.
        y, h = np.concatenate([r0, v0]), 5 * DAY / 2000
        f = lambda y: np.concatenate([y[3:], -transfers.MU_SUN * y[:3] / np.linalg.norm(y[:3]) ** 3])
        for _ in range(2000):
            k1 = f(y); k2 = f(y + h / 2 * k1); k3 = f(y + h / 2 * k2); k4 = f(y + h * k3)
            y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        self.assertLess(np.linalg.norm(r_mid[0] - y[:3]), 1e5)
        self.assertLess(np.linalg.norm(v_mid[0] - y[3:]), 0.1)

    def test_calendar_round_trip(self):
        from logistics_model.ephemeris import calendar, jd_of
        self.assertEqual(jd_of(2000, 1, 1), 2451544.5)
        for jd in (2451544.5, 2462502.5, 2470000.5):
            self.assertAlmostEqual(jd_of(*calendar(jd)), jd)

    def test_fetched_elements_replace_the_recalled_ones(self):
        from logistics_model.ephemeris import elements
        fetched = elements()
        # Within rounding of the values recalled before the network was open.
        recalled = {"Ryugu": (1.1896, 0.1902, 5.884), "Eros": (1.4580, 0.2227, 10.828), "Itokawa": (1.3241, 0.2801, 1.621)}
        for name, (a, e, i) in recalled.items():
            self.assertAlmostEqual(fetched[name][0], a, delta=0.002)
            self.assertAlmostEqual(fetched[name][1], e, delta=0.001)
            self.assertAlmostEqual(fetched[name][2], i, delta=0.02)
            self.assertEqual(transfers.ELEMENTS[name], fetched[name])


class TestWindows(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from logistics_model.ephemeris import Ephemeris
        cls.e = Ephemeris()

    def test_dated_windows_above_the_phase_free_bound(self):
        from logistics_model import windows
        from logistics_model.ephemeris import jd_of
        s = windows.summary(self.e, "Ryugu", "Eros", jd_of(2028), jd_of(2072))
        bound = transfers.best_phase("Ryugu", "Eros")[0]
        self.assertGreater(s["best"][0], bound - 50)
        self.assertLess(s["best"][0], bound + 300)
        # The notes' dated value, ~4.7 km/s in 2030–2060.
        in_span = [w for w in s["all"] if jd_of(2030) <= w[1] < jd_of(2060)]
        self.assertAlmostEqual(min(in_span)[0] / 1e3, 4.7, delta=0.1)
        # The refined window is a local minimum.
        dv, t1, tof = s["best"]
        for d1, d2 in ((3, 0), (-3, 0), (0, 5), (0, -5)):
            self.assertGreaterEqual(float(windows.delta_v(self.e, "Ryugu", "Eros", t1 + d1, tof + d2)), dv - 1e-6)

    def test_refined_departures_stay_in_the_span(self):
        # The reviewer's case: a two-day span on a descending stretch of the curve.
        from logistics_model import windows
        from logistics_model.ephemeris import jd_of
        lo, hi = jd_of(2031, 5, 1), jd_of(2031, 5, 2)
        s = windows.summary(self.e, "Ryugu", "Eros", lo, hi, within=1000.0)
        for w in s["all"]:
            self.assertGreaterEqual(w[1], lo - 1e-6)
            self.assertLessEqual(w[1], hi + 1e-6)

    def test_one_window_per_basin(self):
        from logistics_model import windows
        # A broad single minimum: one basin, one pick.
        x = np.linspace(-1, 1, 400)
        self.assertEqual(windows.local_minima(1000 * x ** 2, 12), [200])
        # Two refined results a day apart collapse to the better one; others stay, separated.
        found = [(3660.5, 1000.0, 300.0), (3660.4, 1000.6, 301.0), (3189.0, 5000.0, 390.0), (3189.1, 5000.3, 390.0),
                 (4000.0, 1300.0, 200.0)]
        kept = windows.deduplicate(found, 120.0)
        self.assertEqual([round(w[1], 1) for w in kept], [1000.6, 1300.0, 5000.0])

    def test_final_windows_obey_their_separation(self):
        from logistics_model import windows
        from logistics_model.ephemeris import jd_of
        for origin in ("2015 DX198", "Ryugu"):
            found, _ = windows.windows(self.e, origin, "Eros", jd_of(2028), jd_of(2072))
            dates = [w[1] for w in found]
            self.assertTrue(np.all(np.diff(dates) >= 120.0 - 1e-6), origin)

    def test_gaps_are_reported(self):
        from logistics_model import windows
        from logistics_model.ephemeris import jd_of
        s = windows.summary(self.e, "Ryugu", "Eros", jd_of(2028), jd_of(2072), within=1000.0)
        self.assertGreaterEqual(s["max_gap"], s["mean_gap"])
        # No usable Ryugu → Eros window between 2036 and 2056.
        self.assertGreater(s["max_gap"], 15.0)

    def test_rendezvous_with_itself_costs_nothing(self):
        from logistics_model import windows
        jd = float(self.e.jd[300])
        # Ryugu to Ryugu over a quarter of its period: the transfer arc is Ryugu's own orbit.
        self.assertLess(float(windows.delta_v(self.e, "Ryugu", "Ryugu", jd, 120.0)), 50.0)


class TestCatalogue(unittest.TestCase):
    def test_ranked_and_screened(self):
        from logistics_model import catalogue
        data = catalogue.load()
        for host in catalogue.HOSTS:
            rows = catalogue.ranked(data, host, 6)
            self.assertEqual([r[2] for r in rows], sorted(r[2] for r in rows))
            for key, _, best, _ in rows:
                # The coarse screen sits above the refined value.
                self.assertGreaterEqual(data["delta_v"][host][key]["coarse"], best - 1.0)
        self.assertAlmostEqual(catalogue.mass_kg(0.896) / 1e9, 448, delta=5)     # Ryugu, ~4.5e11 kg

    def test_stored_result_reproduces(self):
        from logistics_model import catalogue
        data = catalogue.load()
        key, entry, best, _ = catalogue.ranked(data, "Eros", 1)[0]
        saved = transfers.ELEMENTS.get(key)
        transfers.ELEMENTS[key] = tuple(entry["elements"])
        try:
            self.assertAlmostEqual(transfers.best_phase(key, "Eros")[0], best, delta=1.0)
        finally:
            if saved is None:
                del transfers.ELEMENTS[key]
            else:
                transfers.ELEMENTS[key] = saved


if __name__ == "__main__":
    unittest.main()
