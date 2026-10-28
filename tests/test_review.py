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

    def test_sparse_panels_nearly_all_escape(self):
        e = cavity.escape_probability(self.r["geometry"], 6, 1e-4, 0.9, side_gaps=False, n_rays=4000)
        self.assertGreater(e["escape"], 0.99)
        self.assertEqual(e["unresolved"], 0)

    def test_never_beats_the_ideal_limit(self):
        # A black body at the panels' temperature can't push more through the openings than they pass.
        c = cavity.check(params(load(), radiator_emissivity=1.0), self.d, self.r["geometry"], self.r["heat"]["stack"],
                         side_gaps=False, n_rays=6000)
        for point in c["curve"]:
            self.assertLessEqual(point["output"], 1.03 * c["ideal_limit"])

    def test_six_stack_three_tiers(self):
        c = cavity.check(self.p, self.d, self.r["geometry"], self.r["heat"]["stack"], side_gaps=False)
        self.assertGreater(c["margin"], 1)                 # still feasible
        self.assertLess(c["margin"], self.r["heat"]["margin"])  # but less than the ideal margin
        self.assertGreater(c["needed"]["panel_area"], c["ideal_panel_area"])


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
