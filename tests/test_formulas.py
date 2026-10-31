"""Unit tests on the model's formulas (plan §1.3)."""

import math
import unittest

from habitat_model import Design, evaluate, load, params
from habitat_model import food, heat, mass, replication, stability
from habitat_model.geometry import ONE_G, radius_for_period


class TestFormulas(unittest.TestCase):
    def setUp(self):
        self.p = params(load())

    def test_one_g_family(self):
        # r = (T/2)^2 gives a = pi^2 for every even period (§1).
        for period in (20, 40, 60, 80, 100):
            d = Design(radius_m=radius_for_period(period), n_tori=1)
            geo = evaluate(self.p, d)["geometry"]
            self.assertAlmostEqual(geo["period"], period, places=6)
            self.assertAlmostEqual(geo["accel"], math.pi ** 2, places=9)
            self.assertAlmostEqual(geo["rim_speed"], math.pi * period / 2, places=6)
            self.assertAlmostEqual(geo["rim_speed"] ** 2, ONE_G * geo["radius"], places=6)

    def test_reduced_gravity_period(self):
        # T(g) = T(1 g) / sqrt(g) at fixed radius (§9).
        geo = evaluate(self.p, Design(radius_m=900, n_tori=1, g=0.3))["geometry"]
        self.assertAlmostEqual(geo["period"], 60 / math.sqrt(0.3), places=6)

    def test_torus_geometry_ratios(self):
        geo = evaluate(self.p, Design(radius_m=1600, n_tori=1))["geometry"]
        r = geo["radius"]
        self.assertAlmostEqual(geo["floor_area"], math.pi * r ** 2 / 8)
        self.assertAlmostEqual(geo["volume"] / r ** 3, 0.01867, places=5)
        self.assertAlmostEqual(geo["hull_area"] / r ** 2, 1.195, places=3)
        self.assertAlmostEqual(geo["hull_area"] / geo["floor_area"], 3.04, places=2)

    def test_spoke_taper(self):
        # M_spokes / M_rim = rho v^2 / (sigma - rho v^2 / 2): ~7% at 900 m, ~13% at 1.6 km, ~22% at 2.5 km (§5c).
        for period, expected in ((60, 0.07), (80, 0.13), (100, 0.22)):
            v = math.pi * period / 2
            self.assertAlmostEqual(mass.spoke_factor(self.p, v), expected, delta=0.006)
        # It diverges where rho v^2 / 2 reaches the working stress, near 26 km at 1 GPa (§5c, §9).
        v_limit = math.sqrt(2 * self.p.wire_stress_mpa * 1e6 / self.p.steel_density)
        self.assertAlmostEqual(v_limit ** 2 / ONE_G / 1000, 25.6, delta=0.5)
        with self.assertRaises(ValueError):
            mass.spoke_factor(self.p, v_limit * 1.01)

    def test_n2_scaling(self):
        # N2 ~ 1.086e-5 r^3 t at 70 kPa / 29% O2 (§3c).
        r = 900
        n2 = evaluate(self.p, Design(radius_m=r, n_tori=1))["mass"]["n2"]
        self.assertAlmostEqual(n2 / 1e3 / r ** 3, 1.086e-5, delta=0.01e-5)

    def test_radiator_law(self):
        # ~375 W/m^2 at 285 K (§13).
        self.assertAlmostEqual(heat.radiator_flux(285), 374, delta=1)
        self.assertAlmostEqual(heat.radiator_flux(570) / heat.radiator_flux(285), 16)

    def test_food_chain(self):
        # ~3,200 mol per person per day, ~89 m^2 of crops, ~12 kW with blue + red LEDs over their life (§13).
        per_crop, mol = food.light_per_person(self.p)
        self.assertAlmostEqual(mol, 3200, delta=0.05 * 3200)
        expected = {"potato": 600, "wheat": 1080, "soybean": 560, "lentils": 320,
                    "berries": 150, "flax": 190, "greens": 40}
        for crop, ref in expected.items():
            self.assertAlmostEqual(per_crop[crop], ref, delta=0.05 * ref, msg=crop)
        f = evaluate(self.p, Design(radius_m=900, n_tori=1))["food"]
        self.assertAlmostEqual(f["power_per_person"] / 1e3, 12, delta=0.6)
        # The lamps' ageing: power scales with 1 / the fleet's maintained output.
        new = evaluate(params(load(), lamp_maintained_output=1.0), Design(radius_m=900, n_tori=1))["food"]
        self.assertAlmostEqual(f["power_per_person"] / new["power_per_person"], 1 / self.p.lamp_maintained_output)
        # Power per person doesn't depend on the light level on the crops, only the area does.
        brighter = evaluate(params(load(), crop_light_mol=45), Design(radius_m=900, n_tori=1))["food"]
        self.assertAlmostEqual(brighter["power_per_person"], f["power_per_person"])
        self.assertLess(brighter["crop_area_per_person"], f["crop_area_per_person"])

    def test_people_scale_with_tiers(self):
        one = evaluate(self.p, Design(radius_m=900, n_tori=1, tiers_lit=1))
        three = evaluate(self.p, Design(radius_m=900, n_tori=1, tiers_lit=3))
        self.assertAlmostEqual(three["food"]["people"], 3 * one["food"]["people"])
        self.assertAlmostEqual(three["power"]["total"] - one["power"]["total"], 2 * one["power"]["farm_per_tier"])

    def test_stability_closed_form_matches_inertia(self):
        # The closed form of §11 is the inertia sum of thin rings.
        for radius, pitch, margin in ((900, 66.25, 0.2), (1600, 110, 0.1), (900, 96.25, 0.2), (400, 35, 0.0)):
            n = stability.max_tori(radius, pitch, margin)
            self.assertGreater(stability.inertia_ratio(n, radius, pitch), 1 + margin)
            self.assertLessEqual(stability.inertia_ratio(n + 1, radius, pitch), 1 + margin)
        self.assertAlmostEqual(stability.inertia_ratio(1, 900, 66), 2.0)

    def test_shipping_energy(self):
        # ~1.2e8 J/kg at 4.5 km/s with 30 km/s exhaust at 60% (§15).
        self.assertAlmostEqual(replication.shipping_energy_per_kg(self.p, 4.5) / 1e8, 1.21, delta=0.01)
        self.assertEqual(replication.shipping_energy_per_kg(self.p, 0), 0)

    def test_mass_balance(self):
        m = evaluate(self.p, Design(radius_m=1600, n_tori=1))["mass"]
        self.assertAlmostEqual(m["total"], m["rim"] + m["spokes"])
        self.assertAlmostEqual(m["steel"], m["hull_frames"] + m["spokes"])
        self.assertAlmostEqual(m["shield"], m["shield_gross"] - m["fill_credit"])

    def test_s_type_sizing(self):
        # An H host is sized by the shield at 900 m, an LL host by the metal (§10).
        h = evaluate(self.p, Design(radius_m=900, n_tori=1, host_class="H"))["materials"]
        ll = evaluate(self.p, Design(radius_m=900, n_tori=1, host_class="LL"))["materials"]
        self.assertEqual(h["s_sized_by"], "shield")
        self.assertEqual(ll["s_sized_by"], "metal")
        self.assertGreater(ll["s_type"], 2 * h["s_type"])
        self.assertGreaterEqual(ll["spare_tailings"], 0)


if __name__ == "__main__":
    unittest.main()
