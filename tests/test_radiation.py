import math
import unittest

import numpy as np

from habitat_model import load, params
from radiation_model import environment as env, neutrons, physics, reference, shield, tube
from radiation_model.transport import Transport

P = params(load())
ROCK = physics.material("Tailings (L/LL chondrite, metal removed)")
WATER = physics.material("Water")


class TestPhysics(unittest.TestCase):
    def test_proton_ranges_match_pstar(self):
        rt = physics.RangeTable(WATER)
        self.assertAlmostEqual(float(rt.range(100.0)), 7.718, delta=0.08)
        self.assertAlmostEqual(float(rt.range(10.0)), 0.1230, delta=0.003)
        # Ions of the same speed: range scales as A / Z².
        self.assertAlmostEqual(float(rt.range(100.0, 2, 4)), float(rt.range(100.0)), places=9)
        self.assertAlmostEqual(float(rt.energy(rt.range(250.0))), 250.0, delta=0.5)

    def test_ranges_hold_below_the_bethe_formula(self):
        # Heavy materials: the range must keep falling towards zero energy, not blow up.
        rt = physics.RangeTable(ROCK)
        r = rt.range(np.array([0.1, 1.0, 10.0]))
        self.assertTrue(np.all(np.diff(r) > 0))
        self.assertLess(r[0], 0.01)

    def test_cross_sections(self):
        self.assertAlmostEqual(physics.sigma_inelastic(1, 16), 300, delta=30)
        self.assertAlmostEqual(physics.sigma_inelastic(12, 12), 870, delta=50)
        self.assertEqual(physics.sigma_inelastic(56, 1), physics.sigma_inelastic(1, 56))
        self.assertAlmostEqual(physics.interaction_length(WATER, 1), 83, delta=5)

    def test_quality_factor(self):
        q = physics.quality_factor([5.0, 50.0, 200.0])
        self.assertAlmostEqual(q[0], 1.0)
        self.assertAlmostEqual(q[1], 0.32 * 50 - 2.2)
        self.assertAlmostEqual(q[2], 300 / math.sqrt(200))

    def test_modulation_lowers_the_flux(self):
        t = np.array([100.0, 1000.0])
        self.assertTrue(np.allclose(env.gcr(t, 0.0, "p"), env.lis_proton(t)))
        self.assertTrue(np.all(env.gcr(t, 1000.0, "p") < env.gcr(t, 300.0, "p")))


class TestNeutrons(unittest.TestCase):
    def test_deep_in_a_thick_slab_the_flux_balances_the_source(self):
        # Uniform source s, far from the vacuum face: φ = s / Σ_removal at the reflecting face.
        layers = [(ROCK, 3000.0)]
        fast, _, prof = neutrons.fluence(layers, lambda x: np.ones_like(x), cells=600)
        removal = physics.neutron_groups(ROCK)[0][1]
        self.assertAlmostEqual(fast * removal, 1.0, delta=0.01)
        self.assertGreater(prof["fast"][-1], prof["fast"][0])

    def test_slab_source_sums_the_directions(self):
        s = neutrons.slab_source(lambda path, mu: np.full_like(path, 3.0))
        self.assertAlmostEqual(float(s(np.array([10.0]))[0]), 2 * math.pi * 3.0, places=9)

    def test_water_absorbs_the_rock_s_neutrons(self):
        src = lambda x: np.where(x < 100, 1.0, 0.0)
        rock_only, _, _ = neutrons.fluence([(ROCK, 200.0)], src)
        with_water, _, _ = neutrons.fluence([(ROCK, 100.0), (WATER, 100.0)], src)
        self.assertLess(with_water, 0.2 * rock_only)


class TestCollisions(unittest.TestCase):
    def setUp(self):
        self.t = Transport()
        self.d = self.t.data(ROCK)
        self.c = self.t.grid.centres

    def test_no_pions_below_threshold(self):
        from radiation_model.transport import PION_THRESHOLD_MEV
        low = self.c < PION_THRESHOLD_MEV
        self.assertEqual(float(self.d.pions[low].sum()), 0.0)
        self.assertGreater(float(self.d.pions[~low].sum()), 0.0)

    def test_collision_energy_budget(self):
        # Every represented channel, for each material and at the ends of every collision input's range.
        from radiation_model.environment import PION_A
        from radiation_model.transport import EVAPORATION_MEV, M_PION, Knobs, MaterialData
        assumptions = load()
        names = ("leading_nucleon_z", "cascade_nucleons_coeff", "cascade_nucleon_mev", "evaporation_neutrons_coeff",
                 "knockout_alphas_coeff")
        cases = [{}] + [{n: getattr(assumptions[n], end)} for n in names for end in ("low", "high")]
        cases.append({n: assumptions[n].high for n in names})
        g = self.t.grid
        c = g.centres
        for name in ("Tailings (L/LL chondrite, metal removed)", "Steel", "Water"):
            for over in cases:
                knobs = Knobs.from_params(params(assumptions, **over))
                d = MaterialData(physics.material(name), g, knobs)
                a = (knobs.leading_z * 2.7 - 1) / (1 - knobs.leading_z)
                lead = np.maximum((a + 1) / (a + 2) * c, d.lead @ c)
                spent = (lead + d.casc @ c + 0.5 * d.casc_below + d.alphas @ (4 * c)
                         + d.evap * EVAPORATION_MEV
                         + 1.5 * d.pions @ (c * PION_A + M_PION))       # charged pions and their neutral half
                self.assertTrue(np.all(spent <= c * (1 + 1e-3) + 1e-6), (name, over, float(np.max(spent / c))))
        # Within the pion grid (kinetic energies up to ~15 GeV) the pions' budget is spent in full.
        mid = (c > 1000) & (c < 5000)
        spent = self.d.pions @ (c * PION_A + M_PION)
        self.assertTrue(np.allclose(spent[mid], self.d.pion_budget[mid], rtol=0.01))

    def test_reviewer_case_stays_within_energy(self):
        # Tailings with the most light ions: the 301 MeV bin was 11.7% over its input.
        from radiation_model.environment import PION_A
        from radiation_model.transport import M_PION, Knobs, MaterialData
        d = MaterialData(ROCK, self.t.grid, Knobs.from_params(params(load(), knockout_alphas_coeff=0.2)))
        c = self.t.grid.centres
        j = int(np.argmin(np.abs(c - 301.4)))
        total = (d.lead[j] @ c + d.casc[j] @ c + d.pions[j] @ (c * PION_A + M_PION) + d.alphas[j] @ (4 * c))
        self.assertLessEqual(total, c[j])


class TestTransport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = shield.Model(P)
        cls.depths = [5.0, 100.0, 300.0, 500.0, 700.0, 900.0]
        cls.rock = cls.m.profile(ROCK, cls.depths)
        cls.water = cls.m.profile(WATER, cls.depths)

    def test_free_space_dose(self):
        d = self.rock[0]
        self.assertGreater(d.gray, 200)          # mGy/yr behind 5 g/cm²
        self.assertLess(d.gray, 500)
        self.assertGreater(d.total, 800)
        self.assertLess(d.total, 2500)

    def test_dose_falls_with_depth_and_water_beats_rock(self):
        rock = [d.total for d in self.rock[1:]]
        self.assertTrue(all(b < a for a, b in zip(rock, rock[1:])))
        for r, w in zip(self.rock[2:], self.water[2:]):
            self.assertLess(w.total, r.total)
        # Neutrons dominate deep in rock.
        self.assertGreater(self.rock[-1].neutron_share, 0.5)

    def test_nucleon_attenuation_in_air(self):
        air = physics.Material("Air", {"N": 0.755, "O": 0.232, "C": 0.0003}, 0.0012)
        t = Transport()
        g = t.grid
        inc = {s: np.zeros(g.n) for s in env.SPECIES}
        inc["p"] = (g.edges[:-1] ** -1.7 - g.edges[1:] ** -1.7) * (g.centres > 10)
        vals = []
        for d in (400.0, 800.0):
            st = t.march([(air, d)], inc)["state"]
            mask = g.centres > 1000
            vals.append(float(st["p"][mask].sum() + st["n"][mask].sum()))
        lam = 400 / math.log(vals[0] / vals[1])
        self.assertGreater(lam, 100)
        self.assertLess(lam, 135)

    def test_fine_steps_at_the_end_settle_the_short_ranged_particles(self):
        inc = self.m.incident()
        a = self.m.t.march([(ROCK, 300.0)], inc, tail=6.0)
        b = self.m.t.march([(ROCK, 300.0)], inc, step=1.0, tail=10.0, fine=0.1)
        da, db = sum(self.m.t.dose(a["state"])[0].values()), sum(self.m.t.dose(b["state"])[0].values())
        self.assertAlmostEqual(da / db, 1.0, delta=0.05)


class TestTube(unittest.TestCase):
    def test_axis_of_a_long_tube_against_quadrature(self):
        lay = {"a": 28.0, "jacket": 5.0, "jacket_under_fill": 5.0, "fill": 0.0, "fill_density": 1.7,
               "rock_density": 2.0}
        lam = 170.0
        ray = lambda length: np.exp(-length / lam)
        dose, _ = tube.dose_at(lay, (0.0, 0.0), ray, 0.0, n_dirs=20000)
        t = 5.0 * 2.0 * 100
        mu, w = np.polynomial.legendre.leggauss(400)
        expected = 2 * math.pi * np.sum(w * np.exp(-t / (lam * np.sqrt(1 - mu ** 2))))
        self.assertAlmostEqual(dose / expected, 1.0, delta=0.02)

    def test_tube_shields_better_than_a_sphere(self):
        lay = {"a": 28.0, "jacket": 5.0, "jacket_under_fill": 5.0, "fill": 0.0, "fill_density": 1.7,
               "rock_density": 2.0}
        ray = lambda length: np.exp(-length / 170.0)
        axis, _ = tube.dose_at(lay, (0.0, 0.0), ray, 0.0)
        floor, _ = tube.dose_at(lay, (0.0, -26.0), ray, 0.0)
        sphere = 4 * math.pi * math.exp(-1000 / 170.0)
        self.assertLess(axis, 0.6 * sphere)
        self.assertLess(floor, axis)


class TestReference(unittest.TestCase):
    def test_oltaris_table(self):
        self.assertAlmostEqual(float(reference.table2("Water", 7)), 16.1)
        self.assertAlmostEqual(reference.needed("Water", 20), 6.6, delta=0.1)
        self.assertAlmostEqual(reference.needed("Lunar regolith (OLTARIS's)", 20), 10.3, delta=0.1)
        # Past the table, the last slope carries on.
        r = reference.TABLE2["Lunar regolith (OLTARIS's)"]
        self.assertAlmostEqual(float(reference.table2("Lunar regolith (OLTARIS's)", 12)), r[-1] ** 2 / r[-2], places=6)
        self.assertAlmostEqual(reference.WALL_FACTOR, 0.4985, places=4)

    def test_needed_reports_limits_out_of_reach(self):
        reg = "Lunar regolith (OLTARIS's)"
        # 1 mSv/yr lies beyond the table: found on its extension, not at the bottom of the range.
        x = reference.needed(reg, 1.0)
        self.assertGreater(x, 11)
        self.assertAlmostEqual(float(reference.table2(reg, x)), 1.0, delta=0.01)
        self.assertIsNone(reference.needed(reg, 1.0, high=14.0))
        self.assertAlmostEqual(reference.needed(reg, 1000.0), 1.0)
        # Halving the dose (near a wall) needs less.
        self.assertLess(reference.needed(reg, 20, 0.5), reference.needed(reg, 20))

    def test_jacket_section_out_of_range(self):
        from radiation_model.__main__ import jacket_section
        text = "\n".join(jacket_section(params(load(), dose_limit_msv_yr=1e-6), 1.0))
        self.assertIn("beyond the curve", text)
        self.assertNotIn("with ~6", text)

    def test_model_matches_oltaris_for_water(self):
        m = shield.Model(P)
        depths = [100.0 * t for t in range(5, 9)]
        tot = [d.total for d in m.profile(WATER, depths)]
        need = float(np.interp(-math.log(20), -np.log(tot), depths)) / 100
        self.assertAlmostEqual(need, reference.needed("Water", 20), delta=0.5)


if __name__ == "__main__":
    unittest.main()
