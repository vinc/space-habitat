"""Checks for the sky's handedness, flux conservation and source integrity."""

import json
import math
from pathlib import Path
import tempfile
import unittest
import struct

import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import generate_sky as sky


class SkyTests(unittest.TestCase):
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
