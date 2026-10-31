"""Regression tests for the findings of the section 1 review (GitHub issue #1)."""

import json
import math
import unittest
from contextlib import redirect_stdout
from io import StringIO

from habitat_model import Design, evaluate, load, metrics, params
from habitat_model import cavity, report, sensitivity, validation
from habitat_model.__main__ import main


class TestGeometryEnvelope(unittest.TestCase):
    def setUp(self):
        self.p = params(load())

    def test_envelopes_do_not_overlap(self):
        for r in (400, 900, 1600, 2500):
            g = evaluate(self.p, Design(radius_m=r, n_tori=2, gap_m=10))["geometry"]
            self.assertAlmostEqual(g["jacket"], self.p.shield_areal_t_m2 / self.p.rock_density)
            self.assertAlmostEqual(g["pitch"] - 2 * g["envelope_radius"], 10)
            self.assertGreater(g["envelope_radius"], g["tube_radius"] + g["jacket"])
            self.assertGreater(g["drum_radius"], g["hub_radius"])
        with self.assertRaises(ValueError):
            Design(radius_m=900, gap_m=-1) and evaluate(self.p, Design(radius_m=900, gap_m=-1))

    def test_pitch_at_900_m(self):
        # 56.25 m tube + 2 x 5.5 m jacket + 2 x 1.5 m crawl space + 10 m gap.
        g = evaluate(self.p, Design(radius_m=900))["geometry"]
        self.assertAlmostEqual(g["pitch"], 56.25 + 11 + 3 + 10)

    def test_finite_thickness_jacket(self):
        r = evaluate(params(load(), fill_depth_m=0), Design(radius_m=900, n_tori=1))
        g, m = r["geometry"], r["mass"]
        a, t = g["tube_radius"], g["jacket"]
        thin = 4 * math.pi ** 2 * (900 - a) * a * t * self.p.rock_density * 1e3
        self.assertAlmostEqual(m["shield"] / thin, 1 + t / (2 * a))


class TestFillCredit(unittest.TestCase):
    def test_zero_fill_gives_zero_credit(self):
        m = evaluate(params(load(), fill_depth_m=0), Design())["mass"]
        self.assertEqual(m["fill"], 0)
        self.assertEqual(m["fill_credit"], 0)

    def test_credit_grows_with_depth_and_never_exceeds_the_jacket(self):
        credits = [evaluate(params(load(), fill_depth_m=x), Design())["mass"]["fill_credit"] for x in (0.5, 1, 2)]
        self.assertLess(credits[0], credits[1])
        self.assertLess(credits[1], credits[2])
        deep = evaluate(params(load(), fill_depth_m=20), Design())["mass"]
        self.assertGreater(deep["shield"], 0)


class TestUnknownTransfer(unittest.TestCase):
    def test_unknown_delta_v_stays_unknown(self):
        rep = evaluate(params(load()), Design(site="1 AU"))["replication"]
        self.assertIsNone(rep["delta_v_km_s"])
        self.assertIsNone(rep["shipping"])
        self.assertIsNone(rep["energy_per_torus"])
        self.assertIsNone(rep["generation_time_yr"])
        self.assertGreater(rep["generation_time_lower_bound_yr"], 0)

    def test_zero_delta_v_is_zero(self):
        rep = evaluate(params(load()), Design(site="1 AU", delta_v_km_s=0.0))["replication"]
        self.assertEqual(rep["shipping"], 0.0)
        self.assertAlmostEqual(rep["energy_per_torus"], rep["processing"])

    def test_json_and_summary(self):
        out = StringIO()
        with redirect_stdout(out):
            main(["--json", "-"])
        stats = json.loads(out.getvalue())
        self.assertIsNone(stats["stack"]["generation_time_yr"])
        self.assertIsNone(stats["stack"]["energy_pj"])
        self.assertGreater(stats["stack"]["generation_time_lower_bound_yr"], 0)
        out = StringIO()
        with redirect_stdout(out):
            main([])
        self.assertIn("unknown", out.getvalue())


class TestSensitivityOutputs(unittest.TestCase):
    def test_shipping_inputs_are_ranked(self):
        a = load()
        _, rows = sensitivity.tornado(a, Design(radius_m=900, n_tori=6, tiers_lit=2, site="Eros"))
        names = {r.name for r in rows}
        self.assertIn("ep_exhaust_km_s", names)
        self.assertIn("organics_shipped_t_m2", names)

    def test_unknown_metrics_are_left_out(self):
        base, rows = sensitivity.tornado(load(), Design(site="1 AU"))
        self.assertIsNone(base["shipping_energy"])
        for r in rows:
            self.assertNotIn("shipping_energy", r.effects)
        self.assertIn("unknown", report.tornado(base, rows, load(), Design(site="1 AU")))

    def test_combined_ranking_covers_the_designs(self):
        ranking = sensitivity.combined_ranking(load())
        designs = {r["design"] for _, r in ranking}
        self.assertGreater(len(designs), 1)


class TestCavity(unittest.TestCase):
    def setUp(self):
        self.p = params(load())
        self.d = Design(radius_m=900, n_tori=6, tiers_lit=3)
        self.r = evaluate(self.p, self.d)
        self.g, self.h = self.r["geometry"], self.r["heat"]

    def test_sparse_panels_nearly_all_escape(self):
        for scene in (cavity.main_scene(self.g, 6), cavity.farm_scene(self.g, 6)):
            e = cavity.escape_probability(scene, 1e-4, 0.9, n_rays=4000)
            self.assertGreater(e["escape"], 0.99)
            self.assertEqual(e["unresolved"], 0)

    def test_never_beats_the_ideal_limit(self):
        # A black body at the panels' temperature can't push more through the openings than they pass.
        c = cavity.check_main(params(load(), radiator_emissivity=1.0), self.d, self.g, self.h, n_rays=6000)
        for point in c["curve"]:
            self.assertLessEqual(point["output"], 1.03 * c["ideal_limit"])

    def test_six_stack_three_tiers(self):
        main = cavity.check_main(self.p, self.d, self.g, self.h)
        farm = cavity.check_farm(self.p, self.d, self.g, self.h)
        self.assertGreater(main["margin"], 1)
        self.assertLess(main["margin"], self.h["margin"])            # below the ideal margin
        self.assertGreater(main["needed"]["panel_area"], main["ideal_panel_area"])
        self.assertGreater(farm["margin"], 1)
        self.assertGreater(farm["needed"]["panel_area"], farm["ideal_panel_area"])


class TestFarmSection(unittest.TestCase):
    """The farm rings form their own section on the shared hub (farm-section layout)."""

    def setUp(self):
        self.p = params(load())

    def test_sections_add_up(self):
        r = evaluate(self.p, Design(radius_m=900, n_tori=6, tiers_lit=3))
        g, h, pw = r["geometry"], r["heat"], r["power"]
        self.assertAlmostEqual(g["stack_length"], g["main_length"] + g["farm_section_gap"] + g["farm_length"])
        self.assertAlmostEqual(h["main_stack"] / (6 * pw["valley"]), 1)
        self.assertAlmostEqual(h["farm_stack"] / (6 * 3 * pw["farm_per_tier"]), 1)
        self.assertAlmostEqual(h["stack"] / (h["main_stack"] + h["farm_stack"]), 1)

    def test_farm_heat_leaves_the_main_drum(self):
        for tiers in (0, 3):
            h = evaluate(self.p, Design(radius_m=900, n_tori=6, tiers_lit=tiers))["heat"]
            self.assertAlmostEqual(h["break_even_tori"], h["capacity"] / h["main_per_torus"])
        one = evaluate(self.p, Design(radius_m=900, n_tori=6, tiers_lit=1))["heat"]["margin"]
        three = evaluate(self.p, Design(radius_m=900, n_tori=6, tiers_lit=3))["heat"]["margin"]
        self.assertAlmostEqual(one, three)

    def test_light_farm_section_keeps_stability(self):
        st = evaluate(self.p, Design(radius_m=900, n_tori=6))["stability"]
        self.assertAlmostEqual(st["whole_inertia_ratio"], st["inertia_ratio"], delta=0.02)
        self.assertEqual(st["whole_max_tori"], st["max_tori"])

    def test_farm_spokes_air_and_nitrogen(self):
        base = evaluate(self.p, Design(radius_m=900, n_tori=1))
        m, mat = base["mass"], base["materials"]
        self.assertLess(m["farm_spokes"], 0.02 * m["farm_ring"])        # light spokes at ~38 m/s
        self.assertGreater(m["farm_n2"], 0)
        low = evaluate(params(load(), farm_pressure_kpa=30), Design(radius_m=900, n_tori=1))
        self.assertLess(low["mass"]["farm_n2"], m["farm_n2"])
        self.assertLess(low["materials"]["c_type"], mat["c_type"])
        self.assertGreater(mat["metal_needed"], m["steel"] * (1 + self.p.hub_factory_metal_frac))

    def test_farm_radiators_shade_the_drum(self):
        # The farm radiators span most of the drum's farm end: with them, far fewer main rays escape.
        g = evaluate(self.p, Design(radius_m=900, n_tori=6))["geometry"]
        scene = cavity.assembled_scene(g, 6)
        alone = cavity.escape_probability(cavity.main_scene(g, 6), 1.0, 0.9, n_rays=8000)["escape"]
        bare = cavity.escape_probability(scene, (1.0, 0.0), 0.9, n_rays=8000, source=0)["escape"]
        shaded = cavity.escape_probability(scene, (1.0, 1.0), 0.9, n_rays=8000, source=0)["escape"]
        self.assertAlmostEqual(bare, alone, delta=0.02)            # the bare farm section barely matters
        self.assertLess(shaded, 0.75 * alone)

    def test_open_radius_only_ends_rays(self):
        # The physical surfaces stay put: moving the ray-termination radius changes nothing, even with
        # the farm radiators reaching beyond the tori.
        for frac in (1.0, 1.4):
            g = evaluate(params(load(), farm_radiator_outer_frac=frac), Design(radius_m=900, n_tori=6))["geometry"]
            near, far = cavity.assembled_scene(g, 6), cavity.assembled_scene(g, 6, open_margin=2000.0)
            self.assertEqual(near.face, far.face)
            self.assertAlmostEqual(near.face[2], g["envelope_outer"])
            for source in (0, 1):
                e = [cavity.escape_probability(s, (0.75, 0.2), 0.9, n_rays=8000, source=source)["escape"]
                     for s in (near, far)]
                self.assertAlmostEqual(e[0], e[1], delta=0.01)

    def test_assembled_is_below_each_section_alone(self):
        d = Design(radius_m=900, n_tori=6, tiers_lit=3)
        r = evaluate(self.p, d)
        g, h = r["geometry"], r["heat"]
        a = cavity.check_assembled(self.p, d, g, h, n_rays=4000)
        self.assertTrue(a["feasible"])
        self.assertLess(a["main_margin"], cavity.check_main(self.p, d, g, h, n_rays=4000)["margin"])
        self.assertLess(a["farm_margin"], cavity.check_farm(self.p, d, g, h, n_rays=4000)["margin"])

    def test_short_farm_radiators_leave_no_margin(self):
        # Within the declared range, the farm radiators' reach decides whether the stack can be cooled:
        # at 0.6 r the six-stack with three tiers was at the edge with sulfur lamps; with LEDs it keeps 1.5×.
        d = Design(radius_m=900, n_tori=6, tiers_lit=3)
        out = {}
        for lamps, (lamp, farm) in {"sulfur": (1.4, 0), "led": (None, None)}.items():
            for frac in (0.6, 1.4):
                over = {"farm_radiator_outer_frac": frac}
                if lamp:
                    over.update(lamp_efficacy_umol_j=lamp, farm_lamp_efficacy_umol_j=farm, ceiling_delivery=0.75,
                                farm_delivery=0.85)
                p = params(load(), **over)
                r = evaluate(p, d)
                out[lamps, frac] = cavity.check_assembled(p, d, r["geometry"], r["heat"], n_rays=4000)
        self.assertLess(out["sulfur", 0.6]["margin"], 1.2)
        self.assertGreater(out["sulfur", 1.4]["margin"], 2 * out["sulfur", 0.6]["margin"])
        self.assertGreater(out["led", 0.6]["margin"], 1.5)


class TestStatsJson(unittest.TestCase):
    def test_stack_stability_is_the_whole_stack(self):
        # A light farm shell: the tori alone pass the 20% margin at 22 tori, the whole stack doesn't.
        p, d = params(load(), farm_shell_m=0.02), Design(radius_m=900, n_tori=22)
        r = evaluate(p, d)
        st = r["stability"]
        self.assertNotEqual(st["max_tori"], st["whole_max_tori"])
        stack = report.stats_json(p, d, r)["stack"]
        self.assertEqual(stack["inertia_ratio"], st["whole_inertia_ratio"])
        self.assertEqual(stack["max_tori"], st["whole_max_tori"])
        self.assertFalse(stack["inertia_stable"])
        self.assertEqual(stack["main_max_tori"], st["max_tori"])


class TestTraceBudget(unittest.TestCase):
    def test_budget(self):
        budget = evaluate(params(load()), Design())["materials"]["trace_budget"]
        self.assertEqual(budget["Cu"]["status"], "ok")
        self.assertLess(budget["Cu"]["recoverable"], budget["Cu"]["contained"])
        self.assertEqual(budget["Sn"]["status"], "unbudgeted")
        self.assertIsNone(budget["Sn"]["demand"])


class TestValidationHeadline(unittest.TestCase):
    def test_headline_separates_literal_and_configured(self):
        outcomes = validation.run(params(load()))
        text = report.validation(outcomes)
        within5 = sum(abs(o.diff) <= 0.05 for o in outcomes)
        self.assertIn(f"**{within5} within 5%**", text)
        self.assertIn("does not validate the physical design", text)


if __name__ == "__main__":
    unittest.main()


class TestRankingOverrides(unittest.TestCase):
    def test_overrides_reach_the_combined_ranking(self):
        a = load()
        plain = dict(sensitivity.combined_ranking(a))
        fixed = dict(sensitivity.combined_ranking(a, overrides={"ep_exhaust_km_s": 20.0}))
        self.assertIn("ep_exhaust_km_s", plain)
        self.assertNotIn("ep_exhaust_km_s", fixed)   # held at the override, not swept
