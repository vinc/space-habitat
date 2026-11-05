"""Checks for the sky's handedness, flux conservation and source integrity."""

import json
import math
from pathlib import Path
import tempfile
import unittest
import struct
import contextlib
import io
import subprocess
import sys
from unittest.mock import patch

import numpy as np
import OpenEXR
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import generate_sky as sky


class SkyTests(unittest.TestCase):
    def test_missing_dependency_explains_installation(self):
        result = subprocess.run(
            [sys.executable, "-S", str(Path(sky.__file__))],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing sky generator dependency", result.stderr)
        self.assertIn("-m pip install -r", result.stderr)
        self.assertIn("requirements.txt", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_output_must_not_overwrite_recipe(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory)/"sky.manifest.json"
            config.write_text("recipe must survive")
            for output in [config, config.with_name("sky.exr")]:
                with self.subTest(output=output), contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        sky.main(["--config", str(config), "--output", str(output)])
                self.assertEqual(config.read_text(), "recipe must survive")

    def test_offline_generation_writes_exr_and_preserves_recipe(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            panorama = root/"gaia-edr3-original.png"
            catalogue = root/"bsc.json"
            Image.new("RGB", (32, 16), (128, 64, 32)).save(panorama)
            catalogue.write_text(json.dumps([[0, 0, 6000, 1], [6, 20, 6000, 7]]))
            sources = {p.name: {"url": "https://invalid.example/unused", "sha256": sky.sha256(p)}
                       for p in [panorama, catalogue]}
            config = json.loads(Path(sky.__file__).with_name("sky.json").read_text())
            config.update(width=1024, star_fwhm_arcmin=30)
            recipe = root/"sky.json"
            recipe.write_text(json.dumps(config))
            original = recipe.read_bytes()
            output = root/"sky.exr"
            with patch.dict(sky.SOURCES, sources, clear=True), patch.object(sky, "urlopen") as fetch:
                with contextlib.redirect_stdout(io.StringIO()):
                    sky.main(["--config", str(recipe), "--assets-dir", str(root), "--output", str(output)])
                fetch.assert_not_called()
            self.assertEqual(recipe.read_bytes(), original)
            manifest = json.loads((root/"sky.manifest.json").read_text())
            self.assertEqual(manifest["catalogue_rows"], 2)
            self.assertEqual(manifest["stars_drawn"], 1)
            self.assertEqual(manifest["parameters"], config)
            self.assertEqual(manifest["output_sha256"], sky.sha256(output))
            self.assertEqual(manifest["sources"], sources)
            with OpenEXR.File(str(output)) as exr:
                pixels = exr.channels()["RGB"].pixels
                self.assertEqual(pixels.shape, (512, 1024, 3))
                self.assertEqual(pixels.dtype, np.float16)
                self.assertTrue(np.isfinite(pixels).all())
                expected = sky.srgb_to_linear(np.array([128, 64, 32])/255) * config["milky_way_gain"]
                np.testing.assert_allclose(pixels[0, 0], expected, rtol=.001)
                self.assertGreater(float(pixels.max()), float(expected.max()))

    def test_png_gamma_is_decoded_before_filtering(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"gamma.png"
            info = PngInfo()
            info.add(b'gAMA', struct.pack('>I', 45455))
            Image.new('RGB', (1, 1), (128, 128, 128)).save(path, pnginfo=info)
            expected = (128/255) ** (1/.45455)
            np.testing.assert_allclose(sky.load_linear_png(path), expected, rtol=1e-6)

    def test_srgb_chunk_takes_precedence_over_gamma(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"srgb.png"
            info = PngInfo()
            info.add(b'gAMA', struct.pack('>I', 45455))
            info.add(b'sRGB', b'\x00')
            Image.new('RGB', (1, 1), (128, 128, 128)).save(path, pnginfo=info)
            expected = ((128/255+.055)/1.055) ** 2.4
            np.testing.assert_allclose(sky.load_linear_png(path), expected, rtol=1e-6)

    def test_blender_axes_are_not_mirrored(self):
        directions = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
        x, y = sky.direction_to_pixel(directions, 2048)
        np.testing.assert_allclose(x[:2] + .5, [1024, 512])
        np.testing.assert_allclose(y + .5, [512, 512, 0])

    def test_equatorial_ecliptic_reference_directions(self):
        # Equinox, summer-solstice ecliptic point, north ecliptic pole.
        result = sky.equatorial_to_world([0, 6, 18], [0, 23.439291111, 66.560708889])
        np.testing.assert_allclose(result, np.eye(3), atol=1e-12)

    def test_galactic_centre_and_pole(self):
        # Independent standard J2000 reference coordinates, in degrees.
        ra, dec = np.radians(266.404994801), np.radians(-28.936173960)
        direction = np.array([math.cos(dec)*math.cos(ra), math.cos(dec)*math.sin(ra), math.sin(dec)])
        np.testing.assert_allclose(sky.EQ_TO_GAL @ direction, [1, 0, 0], atol=1e-6)
        ra, dec = np.radians(192.85948), np.radians(27.12825)
        pole = np.array([math.cos(dec)*math.cos(ra), math.cos(dec)*math.sin(ra), math.sin(dec)])
        np.testing.assert_allclose(sky.EQ_TO_GAL @ pole, [0, 0, 1], atol=1e-6)

    def flux(self, ra, dec, magnitude, width):
        config = {"magnitude_limit": 8, "yaw_deg": 0, "star_fwhm_arcmin": 30,
                  "zero_magnitude_flux": 80, "star_colour_strength": 0}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"stars.json"
            path.write_text(json.dumps([[ra, dec, 6000, magnitude]]))
            image = np.zeros((width//2, width, 3), dtype=np.float32)
            sky.add_stars(image, path, config)
        latitude = (.5 - (np.arange(width//2)+.5)/(width//2))*np.pi
        # Integrate against each row's sky solid angle, rather than pixel area.
        return np.sum(image[..., 0]*np.cos(latitude)[:, None]) / width**2

    def test_visual_magnitude_flux_ratio(self):
        self.assertAlmostEqual(self.flux(6, 20, 1, 1024) / self.flux(6, 20, 2, 1024), 10**.4, places=6)

    def test_flux_does_not_depend_on_latitude_or_resolution(self):
        reference = self.flux(0, 0, 1, 1024)
        for ra, dec, width in [(0, 0, 2048), (18, 66.0, 1024), (12, -30, 2048)]:
            self.assertAlmostEqual(self.flux(ra, dec, 1, width)/reference, 1, places=6)

    def test_changed_cached_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"bsc.json"
            path.write_text("[]")
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                sky.source_file(Path(directory), "bsc.json")


if __name__ == "__main__":
    unittest.main()
