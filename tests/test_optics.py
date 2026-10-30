import math
import unittest

import numpy as np

from habitat_model import load, params
from optics_model import pipe, scenes
from optics_model.trace import Scene, lambertian, trace

P = params(load())


class TestPipe(unittest.TestCase):
    def test_light_is_accounted_for(self):
        r = pipe.design(40, 0.25, 27.6, 0.01, 0.85, 0.5, 0.3)
        self.assertAlmostEqual(r["efficiency"] + r["film"] + r["extractor"] + r["ends"], 1.0, places=9)
        self.assertGreater(r["uniformity"], 0.98)

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
        close = scenes.light_box(P, gap=0.1, n=100_000)["glow_ratio"]
        far = scenes.light_box(P, gap=0.75, n=100_000)["glow_ratio"]
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


if __name__ == "__main__":
    unittest.main()
