import math
import unittest

import numpy as np

from habitat_model import load, params
from optics_model import pipe, scenes
from optics_model.trace import Scene, lambertian, trace

P = params(load())
# The sulfur light-pipe design first proposed, which the pipe and light-box traces describe.
from optics_model.__main__ import FIRST_SIZING  # noqa: E402
PS = params(load(), lamp_efficacy_umol_j=P.sulfur_efficacy_umol_j, **FIRST_SIZING)


class TestPipe(unittest.TestCase):
    def test_light_is_accounted_for(self):
        r = pipe.design(40, 0.25, 27.6, 0.01, 0.85, 0.5, 0.3)
        self.assertAlmostEqual(r["efficiency"] + r["film"] + r["extractor"] + r["ends"], 1.0, places=9)

    def test_the_graded_glow_holds_on_independent_rays(self):
        # Graded on the quadrature, checked on a large sample it never saw.
        r = pipe.design(40, 0.25, 27.6, 0.01, 0.85, 0.5, 0.3)
        self.assertGreater(r["design_uniformity"], 0.98)
        self.assertGreater(r["uniformity"], 0.97)
        self.assertLess(r["peak"], 1.03)
        check = pipe.evaluate(r["coverage"], 40, 0.25, 27.6, 0.01, 0.85, 0.5, pipe.classes(27.6, 50_000, seed=3))
        self.assertAlmostEqual(check["efficiency"], r["efficiency"], delta=0.003)

    def test_quadrature_matches_the_distributions(self):
        tan_t, b = pipe.quadrature(27.6, 32, 64)
        # Mean impact parameter of (4/π) √(1 − b²) on [0, 1]: 4 / (3π).
        self.assertAlmostEqual(b.mean(), 4 / (3 * math.pi), places=3)
        cos_t = 1 / np.sqrt(1 + tan_t ** 2)
        self.assertAlmostEqual(cos_t.mean(), (1 + math.cos(math.radians(27.6))) / 2, places=9)

    def test_a_lossless_pipe_loses_only_at_its_ends(self):
        r = pipe.design(40, 0.25, 27.6, 0.0, 1.0, 0.0, 0.3)
        self.assertAlmostEqual(r["film"] + r["extractor"], 0.0, places=12)
        self.assertAlmostEqual(r["efficiency"], 1 - r["ends"], places=9)
        self.assertGreater(r["efficiency"], 0.95)

    def test_longer_and_lossier_pipes_lose_more(self):
        short = pipe.design(20, 0.25, 27.6, 0.01, 0.85, 0.5, 0.3)["efficiency"]
        long = pipe.design(80, 0.25, 27.6, 0.01, 0.85, 0.5, 0.3)["efficiency"]
        lossy = pipe.design(20, 0.25, 27.6, 0.02, 0.85, 0.5, 0.3)["efficiency"]
        self.assertGreater(short, long)
        self.assertGreater(short, lossy)

    def test_classes_stay_inside_the_cone(self):
        tan_t, b = pipe.classes(27.6)
        self.assertLessEqual(tan_t.max(), math.tan(math.radians(27.6)) + 1e-12)
        self.assertTrue(np.all((b >= 0) & (b < 1)))


class TestTrace(unittest.TestCase):
    def test_parallel_strips_crossed_strings(self):
        # A diffuse strip of width w facing an equal strip h away, black walls between: the view factor of
        # infinitely long strips is sqrt(1 + (h/w)^2) - h/w (Hottel's crossed strings).
        w, h, n = 1.0, 0.7, 200_000
        rng = np.random.default_rng(5)
        s = Scene(10.0)
        s.add("top", "segment", (w + 1, h), (1.0, h))
        s.add("left", "segment", (1.0, 0.0), (1.0, h), front=(0, 0), back=(0, 0))
        s.add("right", "segment", (w + 1, h), (w + 1, 0.0), front=(0, 0), back=(0, 0))
        s.add("bottom", "segment", (1.0, 0.0), (w + 1, 0.0))
        o = np.stack([1 + w * rng.random(n), np.full(n, 1e-9)], axis=1)
        d = lambertian(np.tile([0.0, 1.0], (n, 1)), rng)
        out = trace(s, o, d, rng)
        f = out["absorbed"]["top"].size / n
        self.assertAlmostEqual(f, math.sqrt(1 + (h / w) ** 2) - h / w, delta=0.005)

    def test_an_ideal_light_box_delivers_everything(self):
        r = scenes.light_box(P, n=20_000, mgo_reflectance=1.0, pipe_albedo=1.0, diffuser_absorptance=0.0,
                             floor_albedo=0.0)
        self.assertAlmostEqual(r["delivered"], 1.0, places=9)
        self.assertEqual(r["lost"], 0.0)

    def test_light_box_conserves_light(self):
        r = scenes.light_box(P, n=50_000)
        self.assertAlmostEqual(sum(r["absorbed"].values()), 1.0, places=9)

    def test_diffuser_blends_the_stripes(self):
        close = scenes.light_box(PS, gap=0.1, n=100_000)["glow_ratio"]
        far = scenes.light_box(PS, gap=0.75, n=100_000)["glow_ratio"]
        self.assertGreater(close, 1.5)
        self.assertLess(far, 1.2)

    def test_farm_tier(self):
        r = scenes.farm_tier(P, n=50_000)
        self.assertAlmostEqual(sum(r["absorbed"].values()), 1.0, places=9)
        self.assertGreater(r["delivered"], 0.9)
        near = scenes.farm_tier(P, pipe_gap=0.1, n=100_000)["uniformity"]
        far = scenes.farm_tier(P, pipe_gap=1.0, n=100_000)["uniformity"]
        self.assertLess(near, far)


class TestDelivery(unittest.TestCase):
    def test_chain_multiplies(self):
        pr = {"efficiency": 0.7}
        d = scenes.delivery(P, pipe_result=pr, box={"delivered": 0.9}, tier={"delivered": 0.95})
        self.assertAlmostEqual(d["valley"], P.pipe_coupling * 0.7 * 0.9)
        self.assertAlmostEqual(d["farm"], P.pipe_coupling * 0.7 * 0.95)

    def test_pitch_follows_the_loading(self):
        self.assertAlmostEqual(scenes.valley_pitch(P) * scenes.valley_peak_w_m2(P), P.pipe_w_per_m)

    def test_farm_pipes_cover_the_bed_s_power(self):
        for delivery in (0.5, 0.6, 0.85, 0.9):
            q = scenes.with_delivery(P, {"valley": 0.75, "farm": delivery})
            pipes = scenes.farm_pipes_per_bed(q)
            need = P.bed_width_m * scenes.farm_peak_w_m2(q)
            self.assertGreaterEqual(pipes * P.pipe_w_per_m, need)
            self.assertLess((pipes - 1) * P.pipe_w_per_m, need)

    def test_converged_layout_carries_its_own_power(self):
        pr = {"efficiency": 0.72}
        d = scenes.converged(P, n=50_000, pipe_result=pr)
        q = d["params"]
        installed_valley = P.pipe_w_per_m / d["box"]["pitch"]
        self.assertAlmostEqual(installed_valley / scenes.valley_peak_w_m2(q), 1.0, delta=0.01)
        self.assertGreaterEqual(d["tier"]["pipes"] * P.pipe_w_per_m, P.bed_width_m * scenes.farm_peak_w_m2(q))
        # Denser than the layout sized for the assumed deliveries, and so less delivered.
        first = scenes.delivery(P, n=50_000, pipe_result=pr)
        self.assertLess(d["box"]["pitch"], first["box"]["pitch"])
        self.assertLess(d["valley"], first["valley"])


class TestArchitectures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from optics_model import architectures
        cls.a = architectures
        cls.opts = {o[0]: o for o in architectures.options(P)}
        cls.names = list(cls.opts)

    def run_option(self, name, n=30_000):
        _, over, eff, _ = self.opts[name]
        return self.a.evaluate_option(P, over, eff, n=n)

    def test_lamps_in_the_box_beat_the_pipes(self):
        pipes, _ = self.run_option(self.names[0])
        lamps, _ = self.run_option(self.names[5])
        self.assertGreater(lamps["valley"], pipes["valley"] + 0.2)
        self.assertGreater(lamps["farm"], pipes["farm"] + 0.2)
        # No pipe in the chain: the luminaire's efficiency is the whole coupling.
        self.assertAlmostEqual(lamps["lamp_to_pipe_out"], P.luminaire_efficiency)

    def test_shorter_and_heavier_pipes_help(self):
        base, _ = self.run_option(self.names[0])
        short, _ = self.run_option(self.names[1])
        heavy, _ = self.run_option(self.names[2])
        self.assertGreater(short["valley"], base["valley"])
        self.assertGreater(heavy["valley"], base["valley"])
        self.assertGreater(heavy["box"]["pitch"], base["box"]["pitch"])

    def test_sector_plants_raise_the_efficacy_only(self):
        _, q_small = self.run_option(self.names[5])
        _, q_sector = self.run_option(self.names[6])
        self.assertAlmostEqual(q_sector.lamp_efficacy_umol_j, P.sector_efficacy_umol_j * P.waveguide_efficiency)
        self.assertAlmostEqual(q_small.lamp_efficacy_umol_j, P.sulfur_efficacy_umol_j)
        _, r_small = self.a.system(q_small)
        _, r_sector = self.a.system(q_sector)
        self.assertLess(r_sector["power"]["total"], r_small["power"]["total"])

    def test_bulb_count(self):
        name = self.names[5]
        d, q = self.run_option(name)
        _, r = self.a.system(q)
        installed, count = self.a.bulbs(P, q, r, self.opts[name][1])
        self.assertAlmostEqual(count, installed / P.lamp_power_w)
        pw = r["power"]
        self.assertAlmostEqual(installed, pw["valley_sky"] * 24 / P.valley_day_h
                               + 3 * pw["farm_per_tier"] * 24 / P.farm_photoperiod_h)
        led = self.names[7]
        _, ql = self.run_option(led)
        self.assertIsNone(self.a.bulbs(P, ql, self.a.system(ql)[1], self.opts[led][1])[1])

    def test_blue_red_farm_lowers_only_the_farm(self):
        _, qw = self.run_option(self.names[7])
        _, qm = self.run_option(self.names[8])
        rw, rm = self.a.system(qw)[1]["power"], self.a.system(qm)[1]["power"]
        self.assertAlmostEqual(rm["valley_sky"], rw["valley_sky"])
        self.assertAlmostEqual(rm["farm_per_tier"] / rw["farm_per_tier"], P.lamp_efficacy_umol_j / P.farm_lamp_efficacy_umol_j)


class TestLeds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from optics_model import architectures, leds
        cls.leds = leds
        opts = architectures.options(P)
        cls.qw = architectures.evaluate_option(P, opts[7][1], 1.0, n=20_000)[1]
        cls.white = architectures.system(cls.qw)
        cls.mixed = architectures.system(architectures.evaluate_option(P, opts[8][1], 1.0, n=20_000)[1])
        cls.qm = architectures.evaluate_option(P, opts[8][1], 1.0, n=20_000)[1]

    def test_die_area_follows_the_power(self):
        r = self.white[1]
        b = self.leds.budget(self.qw, r)
        self.assertEqual(b["die_m2"]["red"], 0.0)
        self.assertAlmostEqual(b["die_m2"]["blue"] * 1e6 * P.led_die_w_mm2, b["valley_w"] + b["farm_w"])
        self.assertAlmostEqual(b["phosphor"], (b["valley_w"] + b["farm_w"]) * P.led_phosphor_g_w / 1e3)

    def test_red_dies_bring_indium_and_arsenic(self):
        bw = self.leds.budget(self.qw, self.white[1])
        bm = self.leds.budget(self.qm, self.mixed[1])
        self.assertAlmostEqual(bm["red_w"], P.led_farm_red_share * bm["farm_w"])
        self.assertGreater(bm["use"]["In"], 10 * bw["use"]["In"])
        self.assertGreater(bm["use"]["As"], 0.0)
        self.assertLess(bm["phosphor"], bw["phosphor"])
        # Gallium in the film over the reactor's utilization; indium enters below its own fed amount.
        self.assertAlmostEqual(bw["fed"]["Ga"], bw["film"]["Ga"] / P.mocvd_utilization)
        # The adopted lamps are the blue + red option.
        self.assertEqual(self.qm.farm_lamp_efficacy_umol_j, P.farm_lamp_efficacy_umol_j)
        self.assertLess(bm["use"]["In"], 0.05 * self.leds.contained(self.mixed[1], "In"))


if __name__ == "__main__":
    unittest.main()
