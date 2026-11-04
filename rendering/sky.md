# Reproduce the sky texture

`generate_sky.py` combines the two sky inputs used by ESA's NEO orbit viewer:
a Gaia Milky Way panorama and Spacekit's processed Yale Bright Star Catalogue.
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
The first run downloads about 3 MB into `rendering/assets/`; subsequent runs
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
| `milky_way_gain` | 8.0 | Brightness of the diffuse panorama; zero removes that layer. |
| `magnitude_limit` | 6.5 | Faintest catalogue entries included; a smaller number gives fewer stars. |
| `star_fwhm_arcmin` | 3.5 | Apparent image-profile width, in arcminutes; a display choice rather than a stellar diameter. |
| `star_colour_strength` | 0.35 | Zero gives white stars; one uses the full approximate temperature colours. |
| `milky_way_blur_deg` | 0.4 | FWHM of smoothing applied to the source panorama, in degrees. |
| `yaw_deg` | 0 | Rotates both layers together around world Z. |
| `width` | 8192 | Image width; height is half this value. Higher resolutions need more memory. |

The source panorama is already dimmed for ESA's viewer. The default Milky Way
gain of 8.0 makes the band and its dust lanes visible at the supplied exterior
exposure of −5.5 stops and sky Strength 10. A gain around 4 is fainter; 12 is
more pronounced. Change this parameter independently of the catalogue-star flux.
Gaia maps integrated stellar brightness and obscuring dust; it does not include
all the emission and reflection nebulosity seen in deep photographs of Orion.

The generator preserves flux ratios of `10 ** (-0.4 * magnitude)` before display
colour management. Gaussian star profiles account for pixel solid angle, so
moving a star toward a texture pole does not make it dimmer. The profile uses a
fixed angular width, not a fixed number of pixels. At low resolutions, increase
`star_fwhm_arcmin` enough to resolve that profile; 8192 is the intended default.

## Use it in Blender

The supplied `.blend` already contains the packed image. No script is required
to open or render it.

For a regenerated image, open the World Shader Editor and select the Environment
Texture node labelled **Gaia and catalogue stars - packed equirectangular sky**.
Open the new EXR in that node, keep **Equirectangular** projection and **Linear
Rec.709** colour space, then use **File > External Data > Pack Resources** and
save the Blender file. If reusing the same image path, reload it before packing.

The Background node labelled **Visible sky - camera background only** controls
overall visibility. The supplied value is 10, paired with the existing exterior
exposure of −5.5 stops. The packed sky contributes no scene illumination or
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

This is a scene orientation convention. The Sun's fixed +X direction has not
been matched to Eros perihelion at a particular epoch. Proper motions, parallax,
variable-star changes, planets and zodiacal light are omitted. Temperature
colours, image-profile sizes and the absolute brightness of both layers are
visual approximations, not a calibrated prediction of human vision.

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
- [Viewer's Milky Way texture](https://neotools.neo.s2p.esa.int/static/textures/MilkyWay.png),
  credited by the viewer to [Gaia EDR3](https://www.esa.int/ESA_Multimedia/Images/2020/12/The_colour_of_the_sky_from_Gaia_s_Early_Data_Release_32).
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
