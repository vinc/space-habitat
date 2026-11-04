# Blender rendering choices

This note records the visual additions in `space-habitat-900m.blend`, separately from the numerical habitat model. It describes the six-torus scene prepared on 3 November 2026, with perihelion lighting updated on 4 November. The [browser explorer](explorer/README.md) is a separate visualization.

The Blender file is maintained manually. Editing it does not update the calculations, and changes to the calculations do not automatically update the scene.

## What comes from the model

The scene uses a 900 m habitat floor radius, a 56.25 m torus tube diameter, a 5.5 m rock jacket and a 60.75 m hub radius. The pressure shell, shielding and cable nets follow the model's geometry and structural concept. Individual meshes may lag subsequent structural revisions.

Six tori and no farm rings are the selected configuration. The torus array leaves about 10 m between outer skins. Its 80.274 m pitch includes rendered skin thicknesses; the idealized model pitch is 80.25 m.

The solar collecting area comes from [power.py](habitat_model/power.py) and the [model assumptions](habitat_model/assumptions.toml), evaluated at commit [feb36fd](https://github.com/vinc/space-habitat/commit/feb36fd0d105c47ebc1a326653dcc655a2c60f1f):

| Sizing input | Scene configuration |
| --- | --- |
| Habitat | Six tori, 900 m floor radius |
| Site | Eros, using sunlight at aphelion, about 1.7812 AU |
| Valley lighting | Default seasonal sky setting |
| Farms | No farm tiers or farm load |
| Active collecting aperture | 1,476,633 m², about 1.477 km² |

This covers the modeled valley lighting and other habitat loads. Factory demand and the exterior lights added for the render are excluded. The area counts the aperture once, even though the rendered array has active surfaces on both faces.

Changing the number of tori in Blender does not recalculate the solar array.

## Additions made for the image

| Addition | Visual choices and their scope |
| --- | --- |
| Steel surface | Small sheets, seams, brushing, waviness and roughness make the exterior read as stainless steel. Their layout and optical properties are appearance choices, without a manufacturing design or measured material data. |
| Solar surface | Blue colour variation distinguishes modules approximately 1 × 2.01 m, aligned with their support sections. The colours do not encode efficiency, temperature or damage. |
| Soil and grass | Soil texture, grass colour and blades illustrate a planted valley. Detailed blades are concentrated near the interior camera. Grass fades out on slopes around 35–40°. |
| Trees | Instanced tree variants form two forest bands, with open space in the middle and no trees on slopes over roughly 30°. Placement, density and individual appearance are scenery choices. These meshes do not calculate biomass, water demand or maintenance. |
| Interior light fittings | The ceiling diffuser, reflector, frames and light pipes illustrate a possible arrangement. Their shader brightness has not been calibrated to the model's plant-light target or to a demonstrated uniform light distribution. |
| Exterior light fittings | Four red rim beacons per torus mark its position; white hub lamps remain. The rim surface wash is disabled. The fittings and their render power have no corresponding mass, electrical or heat budget added to the numerical model. |
| Cable connections | Cable paths illustrate the structural concept. Contacts with the rim and hub are idealized; engineered anchors, terminations and crossings remain to be designed. |

The numerical study may contain general allowances for vegetation and equipment. Detailed scenery does not refine those allowances.

### Solar bands and supports

The calculated aperture is divided into 60 bands, each 20 m wide, with 1 m gaps. Each band contains 12 sections, approximately 20 × 102.54 m, separated by another 1 m gap. The footprint is approximately 1,259 × 1,241.53 m. Gaps are real openings and do not count as collecting area.

The band arrangement, rails, perimeter frame, hollow mast and open hub mount are schematic additions. Their dimensions have not been derived from deployment, strength, vibration or attitude-control calculations. Their detailed mass has not been checked against the model's generic solar-array mass allowance.

## Lighting and surroundings

### Sun and exposure

The native Sun illuminates the scene from +X, with the habitat spin axis along +Z. A visible disk follows the Sun light's direction and angular size without adding illumination a second time.

The Sun now uses **Eros perihelion, 1.133324 AU**, from the [ESA NEOCC orbital solution](https://neo.ssa.esa.int/search-for-asteroids?des=433+Eros&tab=obs) dated 9 October 2026. Total sunlight scales from 1,361 W/m² at 1 AU to approximately **1,059.62 W/m²**. The RGB render retains the existing 40.39% visible-band approximation, giving a native Sun Strength of **427.98 W/m²**, with an angular diameter of **0.470347°** (about 1,693 arcseconds). This is an RGB lighting approximation rather than a spectral or thermal simulation.

Select **Sun > Light Data > Custom Properties > Distance (AU)** to change the reference distance. Native drivers keep irradiance proportional to the inverse square of distance and update the apparent diameter. The visible disk follows both values. The **solar array remains sized for aphelion**, when less sunlight is available; changing the lighting distance does not resize it. The numerical model uses rounded Eros orbital elements for that sizing, while this scene's perihelion distance uses the cited ESA value.

Camera exposure, AgX colour management and material roughness substantially affect the result. The supplied exterior camera uses −5.5 stops and the interior camera uses 0. These settings serve the image rather than predicting human visibility.

Artificial light sources are shared for common colour and power controls. The red beacon lens is emissive, with its strength driven by twice the source's Power value and direct lighting disabled. That value controls render visibility; it is not an electrical fixture rating.

### Stars

The sky is one packed **8192 × 4096 linear EXR**, combining the original **4000 × 2000** [Gaia EDR3 PNG](https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2020/12/the_colour_of_the_sky_from_gaia_s_early_data_release_32/22358132-1-eng-GB/The_colour_of_the_sky_from_Gaia_s_Early_Data_Release_3.png) with **8,404 Yale Bright Star Catalogue entries through visual magnitude 6.5**. The stars use catalogue positions and magnitude-based flux ratios; there are no random stars. The panorama and stars share a J2000 ecliptic orientation, with +X toward the equinox and +Z toward ecliptic north. This is a scene convention, without a dated alignment of the Sun or updates for proper motion and parallax.

The Milky Way remains subdued but visible, using `milky_way_gain = 0.4` at the supplied exterior exposure and 0.15° smoothing. The gain is tuned to the original PNG's brightness and adjusted independently of the catalogue stars. The PNG's gamma metadata is decoded before filtering; the 8192 × 4096 output preserves the original map's finer detail without adding detail beyond that source. Gaia shows integrated stellar brightness and dark dust lanes; it does not provide all the nebulosity seen in deep Orion photographs. Absolute visibility, approximate temperature colours and finite star-image profiles are display choices. **Visible sky - camera background only > Strength** controls overall brightness; the supplied value is 5. The sky provides no illumination or reflections. Uniform background fill is zero, and the independent Sun disk and Eros lighting remain separate.

The [generator](rendering/generate_sky.py) and editable [recipe](rendering/sky.json) reproduce the texture without Blender or `bpy`. See [sky.md](rendering/sky.md) for dependencies, controls, packing instructions, source hashes and attribution.

### Manual sky brightness and optional Sun halo

Change **Shading > Shader Editor > World > Visible sky - camera background
only > Strength** directly before rendering. The saved value is **5**.
A value of 2.5 gives half this radiance; 10 gives twice this radiance.
The Milky Way and catalogue stars share this control. Their brightness is a
display choice, without an absolute photometric calibration.

There is no foreground metering or automatic background adjustment. Film
transparency stays off. Saved viewport settings use Scene World, full background
opacity and no environment blur. Use Material Preview or Rendered shading.

The compositor contains only three nodes: **Scene render**, **Sun halo - mute
to disable**, and **Final image**. The Glare node adds a restrained soft halo
around very bright highlights, with a high threshold chosen to isolate the
visible Sun in this scene. Its source is capped to keep the halo bounded.
It is an artistic approximation of lens scatter, without a calibrated lens
model. Select the Glare node and press **M** to disable the effect. It does not
meter or rescale the background.

The compositor requires no Environment or Mist pass. No script or add-on is
needed. Ordinary World Strength editing works independently of the halo.

### Eros

Eros uses the [NEAR/Gaskell shape model](https://doi.org/10.26033/d0gq-9427), so its overall shape comes from spacecraft data. Its centre is **200 km from the habitat**, at approximately **X = −141.421 km, Y = 0, Z = −141.421 km**. With the Sun toward +X and below defined as −Z, Eros is halfway between directly behind and directly below an observer facing the Sun: 45° below the direction opposite the Sun. Direct sunlight and light reflected from Eros therefore arrive from opposite sides, with the reflected light also arriving from below. The position and orientation are composition choices, without a dated ephemeris or a propagated habitat orbit.

The material uses an approximate, Sun-dependent Hapke-style reflectance treatment. It has not been validated as a spectral or photometric reconstruction. Blender calculates its reflected light separately from the numerical habitat power and thermal models.

## What the scene leaves out

The scene has no farm rings, factory, radiators or docking facilities. It also omits detailed inter-torus structural connections, pressure tunnels and engineered cable fittings. Repeated hub sleeves alone do not establish a structurally complete six-torus assembly.

Omitting something from the picture does not remove it from the wider design study. Use the [model reports](reports/) for numerical results.
