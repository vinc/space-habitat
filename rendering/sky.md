# Reproduce the sky texture

`generate_sky.py` combines ESA's original **4000 × 2000 Gaia EDR3 PNG** with
Spacekit's processed Yale Bright Star Catalogue, also used by ESA's NEO viewer.
It writes one 8192 × 4096 linear OpenEXR image and a JSON recipe manifest.
The current recipe draws 8,404 catalogue entries through visual magnitude 6.5.
There are no random stars.

## Generate it

From the repository root, using ordinary Python 3.11 or newer:

```sh
python -m venv rendering/.venv
source rendering/.venv/bin/activate
python -m pip install -r rendering/requirements.txt
python rendering/generate_sky.py
```

This creates `rendering/output/habitat-sky.exr` and `habitat-sky.json`.
Blender and `bpy` are not required to generate the texture.
The first run downloads about 19 MB into `rendering/assets/`; subsequent runs
reuse those files. Both source files are checked against SHA-256 hashes pinned
in the script. Preserve the cache for offline regeneration. A changed upstream
file causes an error rather than silently changing the result.

An alternative configuration, cache or destination can be selected explicitly:

```sh
python rendering/generate_sky.py --config my-sky.json --assets-dir my-cache --output my-sky.exr
```

## Tweak the recipe

Edit `rendering/sky.json` and run the generator again.

| Parameter | Default | Effect |
| --- | --- | --- |
| `zero_magnitude_flux` | 80 | Brightness of the catalogue stars; doubling it doubles their flux. |
| `milky_way_gain` | 0.4 | Brightness of the diffuse panorama; zero removes that layer. |
| `magnitude_limit` | 6.5 | Faintest catalogue entries included; a smaller number gives fewer stars. |
| `star_fwhm_arcmin` | 3.5 | Apparent image-profile width, in arcminutes; a display choice rather than a stellar diameter. |
| `star_colour_strength` | 0.35 | Zero gives white stars; one uses the full approximate temperature colours. |
| `milky_way_blur_deg` | 0.15 | FWHM of smoothing applied to the source panorama, in degrees. |
| `yaw_deg` | 0 | Rotates both layers together around world Z. |
| `width` | 8192 | Image width; height is half this value. Higher resolutions need more memory. |

The original PNG has a much wider brightness range than the viewer texture.
Its default gain of 0.4 keeps the Milky Way visible at the supplied exterior
exposure of −5.5 stops and sky Strength 5. A gain around 0.2 is fainter; 0.6 is
more pronounced. Change this parameter independently of the catalogue-star flux.
The 0.15° smoothing retains more of the source's detail while softening its
point sources beneath the sharp catalogue layer.

The PNG's gAMA value (0.45455) is decoded to linear light before smoothing and
reprojection. An explicit sRGB chunk takes precedence when present. The output
EXR uses linear Rec.709 primaries and half-float channels.
Gaia maps integrated stellar brightness and obscuring dust; it does not include
all the emission and reflection nebulosity seen in deep photographs of Orion.

The generator preserves flux ratios of `10 ** (-0.4 * magnitude)` before display
colour management. Gaussian star profiles account for pixel solid angle, so
moving a star toward a texture pole does not make it dimmer. The profile uses a
fixed angular width, not a fixed number of pixels. At low resolutions, increase
`star_fwhm_arcmin` enough to resolve that profile; 8192 is the intended default.

## Use it in Blender

The supplied split scene loads `output/habitat-sky.exr` through the relative
path `//output/habitat-sky.exr`. Keep the EXR inside `rendering/output/`,
relative to `rendering/space-habitat-900m.blend`. No script is required to
render when this file is present. If it is missing, run the generator above;
its default output matches the scene path.

For a regenerated image, open the World Shader Editor and select the Environment
Texture node labelled **Gaia and catalogue stars - packed equirectangular sky**.
Open the new EXR in that node, keep **Equirectangular** projection and **Linear
Rec.709** colour space, save the Blender file with the image path relative to the scene. Keep
**Automatically Pack Resources** disabled. If reusing the same image path,
reload the image before rendering.

The Background node labelled **Visible sky - camera background only** controls
overall visibility. The supplied value is 5, paired with the existing exterior
exposure of −5.5 stops. The external sky contributes no scene illumination or
reflections. The independent Sun disk and the light reflected from Eros remain
separate from this texture.

## Coordinates and limits

Catalogue right ascensions and declinations use J2000. They are converted to
J2000 mean ecliptic coordinates. The Gaia panorama is sampled in Galactic
coordinates using the corresponding fixed equatorial/Galactic rotation.
Both layers therefore share one sky orientation.

With zero yaw, world +X points to the equinox and +Z to ecliptic north.
The EXR follows Blender's environment convention: +X at image centre, +Y at
one-quarter width and +Z at the top. It is not mirrored as an ordinary
longitude-increasing panorama would be.

The texture defines the stellar coordinate frame; it does not determine the
Sun direction. The Blender scene uses the dated geometric Sun direction at
Eros perihelion on 22 November 2027, recorded in
[solar-reference.json](solar-reference.json) and explained in the
[rendering guide](README.md#sun-and-exposure). Do not rotate the sky to align
the Sun: the light and visible Sun disk use that same fixed stellar frame.
Proper motions, parallax, variable-star changes, planets and zodiacal light
are omitted from the texture. Temperature colours, image-profile sizes and
the absolute brightness of both layers are visual approximations, not a
calibrated prediction of human vision.

The source Gaia image already contains integrated starlight. Smoothing and a
low gain make it a diffuse backdrop to the sharp catalogue layer; this blend
is not intended for photometric measurements. The adjacent manifest records
parameters, input hashes, generator hash and output hash.

Run the coordinate, magnitude-flux and source-integrity checks with:

```sh
python -m unittest discover -s rendering -p 'test_*.py' -v
```

## Sources and credit

- [ESA NEO orbit viewer](https://neotools.neo.s2p.esa.int/ovt?object=433%20Eros).
- [Original Gaia EDR3 PNG, 4000 × 2000](https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2020/12/the_colour_of_the_sky_from_gaia_s_early_data_release_32/22358132-1-eng-GB/The_colour_of_the_sky_from_Gaia_s_Early_Data_Release_3.png),
  with [ESA's image description](https://www.esa.int/ESA_Multimedia/Images/2020/12/The_colour_of_the_sky_from_Gaia_s_Early_Data_Release_32).
  This original PNG is the generator's diffuse-background input.
  Credit **ESA/Gaia/DPAC**, [CC BY-SA 3.0 IGO](https://creativecommons.org/licenses/by-sa/3.0/igo/).
  The generated texture retains this credit and licence. Changes include
  smoothing, brightness scaling, reprojection and the added catalogue stars.
- [Processed star catalogue](https://neotools.neo.s2p.esa.int/static/spacekit/data/processed/bsc.json),
  from [Spacekit](https://github.com/typpo/spacekit/blob/master/src/data/process_bsc.py),
  which processes [Bretton Wade's Yale Bright Star Catalogue JSON](https://github.com/brettonw/YaleBrightStarCatalog).
  Fields are RA in hours, declination in degrees, approximate temperature in K
  and visual magnitude. Missing temperatures are rendered white.
- [Blender equirectangular projection convention](https://github.com/blender/blender/blob/main/intern/cycles/kernel/camera/projection.h).

The Spacekit-derived temperature classes and catalogue conversion carry these
MIT notices:

```text
MIT License

Copyright (c) 2019 Ian Webster
Copyright (c) 2016 Bretton Wade

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
