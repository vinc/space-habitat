# Blender rendering choices

This note records the visual additions in `space-habitat-900m.blend`, separately from the numerical habitat model. It describes the six-torus scene prepared on 3 November 2026, with Vincent's bottom camera added on 4 November. The [browser explorer](explorer/README.md) is a separate visualization.

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

The current Sun uses a **1 AU reference**: approximately 550 W/m² as a visible-band rendering approximation to the 1,361 W/m² all-spectrum solar constant, and an angular diameter of about 1,919 arcseconds. This differs from the **Eros-aphelion sunlight used to size the array**. The image is not calibrated to that operating point.

Camera exposure, AgX colour management and material roughness substantially affect the result. The supplied exterior camera uses −5.5 stops and the interior camera uses 0. These settings serve the image rather than predicting human visibility.

Artificial light sources are shared for common colour and power controls. The red beacon lens is emissive, with its strength driven by twice the source's Power value and direct lighting disabled. That value controls render visibility; it is not an electrical fixture rating.

### Stars

The star field is synthetic, with brightness boosted for the camera. It contributes no illumination to the habitat and does not represent a catalogue or a particular date and location. Uniform background fill is currently zero.

### Eros

Eros uses the [NEAR/Gaskell shape model](https://doi.org/10.26033/d0gq-9427), so its overall shape comes from spacecraft data. Its placement at X = −90 km, Y = 0, Z = −60 km and its orientation are composition choices, without a dated ephemeris or a selected habitat orbit.

The material uses an approximate, Sun-dependent Hapke-style reflectance treatment. It has not been validated as a spectral or photometric reconstruction. Blender calculates its reflected light separately from the numerical habitat power and thermal models.

### Cameras

Cameras are viewing aids. Vincent added a bottom camera at location **(0, 0, −3000) m**, with XYZ Euler rotation **(−180°, 0°, 0°)**. Its placement is recorded here from his description; it does not change the habitat geometry or the numerical model.

## What the scene leaves out

The scene has no farm rings, factory, radiators or docking facilities. It also omits detailed inter-torus structural connections, pressure tunnels and engineered cable fittings. Repeated hub sleeves alone do not establish a structurally complete six-torus assembly.

Omitting something from the picture does not remove it from the wider design study. Use the [model reports](reports/) for numerical results.
