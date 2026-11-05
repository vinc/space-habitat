#!/usr/bin/env python3
"""Bake ESA/Gaia's original sky PNG and catalogue stars into one Blender sky EXR.

Run with ordinary Python; Blender/bpy is not required. See sky.md for usage,
coordinate conventions, source credits and the distinction from photometry.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
from urllib.request import urlopen

import numpy as np
from PIL import Image
import OpenEXR


SOURCES = {
    "gaia-edr3-original.png": {
        "url": "https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2020/12/the_colour_of_the_sky_from_gaia_s_early_data_release_32/22358132-1-eng-GB/The_colour_of_the_sky_from_Gaia_s_Early_Data_Release_3.png",
        "sha256": "68fef2ee355015f84a43105bbf296f5a8d8b38d2fe8fe1a068ba1402e9ce5550",
        "credit": "ESA/Gaia/DPAC; acknowledgement A. Moitinho; CC BY-SA 3.0 IGO",
        "dimensions": [4000, 2000],
    },
    "bsc.json": {
        "url": "https://neotools.neo.s2p.esa.int/static/spacekit/data/processed/bsc.json",
        "sha256": "32cc0252ec884478049f3a2068d664eb97c3afe8f1b554cf948eaf0983006b8c",
        "credit": "Bright Star Catalogue, processed by Spacekit (Ian Webster); see sky.md",
    },
}

# ICRS/J2000 equatorial -> Galactic. The inverse is its transpose.
# SOFA iauIcrs2g convention, sufficient well below this texture's resolution.
EQ_TO_GAL = np.array([
    [-0.0548755604162154, -0.8734370902348850, -0.4838350155487132],
    [+0.4941094278755837, -0.4448296299600112, +0.7469822444972189],
    [-0.8676661490190047, -0.1980763734312015, +0.4559837761750669],
])
EPSILON = math.radians(23.439291111)  # J2000 mean obliquity
EQ_TO_ECL = np.array([
    [1., 0., 0.],
    [0., math.cos(EPSILON), math.sin(EPSILON)],
    [0., -math.sin(EPSILON), math.cos(EPSILON)],
])


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def source_file(directory, name):
    """Use cached bytes, or fetch once, and reject changed upstream data."""
    path = directory / name
    spec = SOURCES[name]
    if not path.exists():
        directory.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".download")
        try:
            with urlopen(spec["url"], timeout=60) as response, temporary.open("wb") as out:
                while chunk := response.read(1024 * 1024):
                    out.write(chunk)
            if sha256(temporary) != spec["sha256"]:
                raise ValueError(f"Source checksum changed: {name}")
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    if sha256(path) != spec["sha256"]:
        raise ValueError(f"Source checksum mismatch: {path}")
    return path


def srgb_to_linear(value):
    value = np.asarray(value, dtype=np.float32)
    return np.where(value <= .04045, value / 12.92, ((value + .055) / 1.055) ** 2.4)


def load_linear_png(path):
    """Decode PNG colour metadata before any filtering or reprojection.

    The original Gaia PNG has gAMA=0.45455 and Rec.709 chromaticities.
    An explicit sRGB chunk takes precedence over gAMA, as the PNG spec requires.
    """
    with Image.open(path) as image:
        rgb = np.asarray(image.convert("RGB"), dtype=np.float32) / 255.
        gamma = image.info.get("gamma")
        if "srgb" not in image.info and gamma is not None:
            if not math.isfinite(gamma) or gamma <= 0:
                raise ValueError("Invalid PNG gamma")
            return rgb ** (1 / gamma)
        return srgb_to_linear(rgb)


def yaw_matrix(degrees):
    angle = math.radians(degrees)
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, 0.], [s, c, 0.], [0., 0., 1.]])


def equatorial_to_world(ra_hours, dec_degrees, yaw_degrees=0.):
    ra = np.radians(np.asarray(ra_hours) * 15)
    dec = np.radians(dec_degrees)
    vectors = np.stack((np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)), axis=-1)
    return vectors @ (yaw_matrix(yaw_degrees) @ EQ_TO_ECL).T


def direction_to_pixel(vectors, width):
    """File convention: top = +Z; centre = +X; quarter width = +Y.

    This matches Cycles' equirectangular environment lookup, including its
    longitude handedness. No extra mapping rotation is required in Blender.
    """
    longitude = np.arctan2(vectors[..., 1], vectors[..., 0])
    latitude = np.arcsin(np.clip(vectors[..., 2], -1, 1))
    return ((.5 - longitude / (2 * np.pi)) * width - .5) % width, (.5 - latitude / np.pi) * (width // 2) - .5


def milky_way(path, width, gain, blur_deg, yaw_deg):
    # The source is a Galactic panorama: l=0 at centre; l increases leftward.
    # Convert from the PNG's colour encoding BEFORE filtering/resampling.
    source = load_linear_png(path)
    if blur_deg:
        sigma = blur_deg * source.shape[1] / 360 / 2.354820045
        # Wrap longitude, but extend the pole rows rather than mixing poles.
        pad = max(1, math.ceil(4 * sigma))
        channels = []
        for channel in source.transpose(2, 0, 1):
            padded = np.pad(channel, ((0, 0), (pad, pad)), mode="wrap")
            padded = np.pad(padded, ((pad, pad), (0, 0)), mode="edge")
            # Pillow's GaussianBlur does not accept floating-point F images.
            # Use a separable linear convolution, retaining HDR/linear values.
            x = np.arange(-pad, pad + 1)
            kernel = np.exp(-.5 * (x / sigma) ** 2)
            kernel /= kernel.sum()
            horizontal = np.apply_along_axis(lambda row: np.convolve(row, kernel, mode="valid"), 1, padded)
            blurred = np.apply_along_axis(lambda col: np.convolve(col, kernel, mode="valid"), 0, horizontal)
            channels.append(blurred.astype(np.float32))
        source = np.stack(channels, axis=-1)
    height = width // 2
    output = np.zeros((height, width, 3), dtype=np.float32)
    longitude = (.5 - (np.arange(width) + .5) / width) * 2 * np.pi
    coslon, sinlon = np.cos(longitude), np.sin(longitude)
    # World -> ecliptic -> equatorial -> Galactic, applied to row vectors.
    world_to_gal = EQ_TO_GAL @ EQ_TO_ECL.T @ yaw_matrix(yaw_deg).T
    for start in range(0, height, 64):
        rows = np.arange(start, min(start + 64, height))
        lat = (.5 - (rows + .5) / height) * np.pi
        clat, slat = np.cos(lat)[:, None], np.sin(lat)[:, None]
        directions = np.stack(np.broadcast_arrays(clat * coslon, clat * sinlon, slat), axis=-1)
        gal = directions @ world_to_gal.T
        lon = np.arctan2(gal[..., 1], gal[..., 0])
        latitude = np.arcsin(np.clip(gal[..., 2], -1, 1))
        x = ((.5 - lon / (2 * np.pi)) * source.shape[1] - .5) % source.shape[1]
        y = np.clip((.5 - latitude / np.pi) * source.shape[0] - .5, 0, source.shape[0] - 1)
        x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
        x1, y1 = (x0 + 1) % source.shape[1], np.minimum(y0 + 1, source.shape[0] - 1)
        fx, fy = (x - x0)[..., None], (y - y0)[..., None]
        output[start:start + len(rows)] = gain * (
            (1-fy) * ((1-fx)*source[y0, x0] + fx*source[y0, x1])
            + fy * ((1-fx)*source[y1, x0] + fx*source[y1, x1])
        )
    return output


def star_colour(temperature, strength):
    # Same broad temperature classes used by ESA's Spacekit star renderer.
    # This is an appearance approximation, not synthetic spectral photometry.
    classes = [(30000, 9614847), (10000, 10666239), (7500, 14016767),
               (6000, 16381439), (5200, 16772579), (3700, 16767669), (0, 16758124)]
    if temperature <= 0:
        return np.ones(3)
    rgb = next(rgb for threshold, rgb in classes if temperature >= threshold)
    colour = srgb_to_linear(np.array([(rgb >> 16) & 255, (rgb >> 8) & 255, rgb & 255]) / 255.)
    colour /= colour @ np.array([.2126, .7152, .0722])
    return (1-strength) + strength * colour


def add_stars(image, catalogue, config):
    height, width = image.shape[:2]
    stars = np.asarray(json.loads(catalogue.read_text()), dtype=float)
    if stars.ndim != 2 or stars.shape[1] != 4 or not np.isfinite(stars).all():
        raise ValueError("Expected [RA hours, Dec degrees, temperature K, magnitude] rows")
    if np.any((stars[:, 0] < 0) | (stars[:, 0] >= 24) | (np.abs(stars[:, 1]) > 90)):
        raise ValueError("Catalogue coordinates out of range")
    selected = stars[stars[:, 3] <= config["magnitude_limit"]]
    vectors = equatorial_to_world(selected[:, 0], selected[:, 1], config["yaw_deg"])
    px, py = direction_to_pixel(vectors, width)
    sigma = math.radians(config["star_fwhm_arcmin"] / 60) / 2.354820045
    radius_y = max(2, math.ceil(4 * sigma * height / math.pi))
    # Flux units are referenced to an 8192-wide map. Account for pixel solid
    # angle so changing resolution/latitude does not change a star's flux.
    reference_flux = config["zero_magnitude_flux"] * (width / 8192) ** 2
    for row, direction, cx, cy in zip(selected, vectors, px, py):
        latitude = math.asin(direction[2])
        ys = np.arange(max(0, math.floor(cy)-radius_y), min(height, math.floor(cy)+radius_y+2))
        radius_x = min(width//2, math.ceil(radius_y / max(.001, math.cos(latitude))))
        xs = (np.arange(math.floor(cx)-radius_x, math.floor(cx)+radius_x+2) % width)
        xs = np.unique(xs)
        lon = (.5 - (xs + .5) / width) * 2 * math.pi
        lat = (.5 - (ys + .5) / height) * math.pi
        dot = np.cos(lat)[:, None] * (np.cos(lon)*direction[0] + np.sin(lon)*direction[1]) + np.sin(lat)[:, None]*direction[2]
        distance = np.arccos(np.clip(dot, -1, 1))
        kernel = np.exp(-.5 * (distance / sigma) ** 2)
        normalisation = np.sum(kernel * np.cos(lat)[:, None])
        if normalisation <= 0:
            raise ValueError("Star profile undersampled; increase width or star_fwhm_arcmin")
        flux = reference_flux * 10 ** (-.4 * row[3])
        colour = star_colour(row[2], config["star_colour_strength"])
        image[ys[:, None], xs] += (kernel * (flux / normalisation))[..., None] * colour
    return len(stars), len(selected)


def validate(config):
    expected = {"width", "magnitude_limit", "zero_magnitude_flux", "star_fwhm_arcmin",
                "star_colour_strength", "milky_way_gain", "milky_way_blur_deg", "yaw_deg"}
    if set(config) != expected or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in config.values()):
        raise ValueError("Config must contain exactly the documented finite numeric parameters")
    w = config["width"]
    if not isinstance(w, int) or w < 1024 or w > 16384 or w % 2:
        raise ValueError("width must be an even integer between 1024 and 16384")
    if not 0 <= config["star_colour_strength"] <= 1:
        raise ValueError("star_colour_strength must be between 0 and 1")
    if not -2 <= config["magnitude_limit"] <= 8:
        raise ValueError("magnitude_limit must be between -2 and 8")
    if min(config["zero_magnitude_flux"], config["star_fwhm_arcmin"]) <= 0:
        raise ValueError("Star flux and FWHM must be positive")
    if min(config["milky_way_gain"], config["milky_way_blur_deg"]) < 0:
        raise ValueError("Milky Way gain and blur must be non-negative")


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=root / "sky.json")
    parser.add_argument("--assets-dir", type=Path, default=root / "assets")
    parser.add_argument("--output", type=Path, default=root / "assets/sky.exr")
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    validate(config)
    files = {name: source_file(args.assets_dir, name) for name in SOURCES}
    image = milky_way(files["gaia-edr3-original.png"], config["width"], config["milky_way_gain"], config["milky_way_blur_deg"], config["yaw_deg"])
    available, count = add_stars(image, files["bsc.json"], config)
    if not np.isfinite(image).all() or image.max() > np.finfo(np.float16).max:
        raise ValueError("Sky radiance exceeds finite half-float EXR range")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with OpenEXR.File({"compression": OpenEXR.ZIP_COMPRESSION, "type": OpenEXR.scanlineimage,
                      "comments": "ESA/Gaia/DPAC; CC BY-SA 3.0 IGO. Catalogue stars: Spacekit. See adjacent JSON manifest."},
                     {"RGB": image.astype(np.float16)}) as output:
        output.write(str(args.output))
    manifest = {"recipe_version": 2, "parameters": config, "sources": SOURCES,
                "catalogue_rows": available, "stars_drawn": count,
                "coordinates": "J2000 ecliptic; +X equinox, +Z north; optional global yaw",
                "projection": "Blender equirectangular, file top +Z, centre +X, quarter width +Y",
                "colour_space": "linear Rec.709/sRGB primaries, 16-bit float RGB EXR",
                "photometric_calibration": False,
                "generator_sha256": sha256(Path(__file__)), "output_sha256": sha256(args.output)}
    args.output.with_suffix(".json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "size": [config["width"], config["width"]//2], "stars": count, "sha256": manifest["output_sha256"]}))


if __name__ == "__main__":
    main()
