# Heat rejection: radiator layout, sunlight, coolant loops and the valley's swing

Plan §6 (`thermal_model/`), building on the assembled radiative exchange of `habitat_model/cavity.py` (`reports/thermal.md`): radiators at ~285 K, emissivity ~0.9.

## The farm radiators: where, and how far out

Heat flows from the farm rings at 0.4 r to their radiators. **Outboard** (the baseline, from the rings out to ~1 r), the warm coolant must sink against spin gravity: pumped loops. **Inboard** (from the hub to the rings), it rises: passive thermosiphons, as in the main section, but the radiators then sit in the space the farm rings enclose. The whole stack traced as one scene (`habitat_model/cavity.py`), both sections' panel coverages swept on a finer grid; best margins main / farm, and the least panel area (one face, main / farm section) that keeps both at 1.5× (coverage in steps of 5%, so areas move in steps of ~25%).

| Stack, tiers lit | Farm radiators | Best margins, main / farm | At coverage, main / farm | Least panels for 1.5× (ha), main / farm | Tiers the passive set alone carries |
|---|---|---|---|---|---|
| 900 m pair, 3 tiers | outboard | 14 / 15 | 100% / 100% | 17.9 / 21.2 | — |
| 900 m pair, 3 tiers | inboard | 4.2 / 4.0 | 10% / 100% | 17.9 / 19.8 | 12 |
| 900 m six, 2 tiers | outboard | 6.5 / 6.9 | 100% / 25% | 53.8 / 63.5 | — |
| 900 m six, 2 tiers | inboard | 3.4 / 2.0 | 10% / 100% | 53.8 / 59.3 | 4.0 |
| 900 m six, 3 tiers | outboard | 5.7 / 6.1 | 100% / 50% | 53.8 / 63.5 | — |
| 900 m six, 3 tiers | inboard | 1.9 / 1.4 | 5% / 75% | **not reached** | 4.3 |
| 1.6 km six, 3 tiers | outboard | 5.8 / 6.0 | 100% / 50% | 171 / 202 | — |
| 1.6 km six, 3 tiers | inboard | 1.9 / 1.4 | 5% / 100% | **not reached** | 4.1 |

**Inboard radiators cool a six-stack's farm passively, but below 1.5× in some cases** (~1.4× at worst, ~4.0 tiers' heat): no pumps needed with all tiers lit, outboard pumped radiators for a full margin, the inboard set as their passive fallback.

**How far out the outboard radiators must reach** (× floor radius) for each margin, both sections:

| Stack, tiers lit | Reach for 1× | Reach for 1.5× |
|---|---|---|
| 900 m six, 3 tiers | 0.45 | 0.48 |
| 1.6 km six, 3 tiers | 0.45 | 0.48 |
| 900 m six, 2 tiers | 0.45 | 0.45 |

## How many tori the radiators can cool

Most tori (with their farm rings) the assembled stack can cool, farm radiators outboard to 1 r, by farm tiers lit (any margin above 1×; the search stops at 40, beyond passive stability's ~22–25):

| Torus | 0 tiers lit | 1 tier | 2 tiers | 3 tiers |
|---|---|---|---|---|
| 900 m | 40 | 40 | 40 | 40 |
| 1.6 km | 40 | 40 | 40 | 40 |

Panels per torus at 1.5× (one face, outboard farm radiators). Finite panels that see each other, and the farm radiators shading the drum's farm end, need ~2–3× the black-body area (`reports/thermal.md`). Areas at the grid's smallest coverage step (5%) are an upper bound: fewer panels may do.

| Stack, tiers lit | Main section (valley) | Farm section |
|---|---|---|
| 900 m pair, 3 tiers | 9.0 ha | 11 ha |
| 900 m six, 2 tiers | 9.0 ha | 11 ha |
| 900 m six, 3 tiers | 9.0 ha | 11 ha |
| 1.6 km six, 3 tiers | 29 ha | 34 ha |

## Sunlight on the radiators

The axis points at the orbit's pole (notes §11), so sunlight arrives edge-on to the panels. A tilt lets it fall on one face of each, unless the tori (as true tori), the hub or the farm rings shade them. Sun rays marched through a 900 m six-stack (`thermal_model/sunlight.py`), panels at 5% / 5% coverage (main / farm, the least panels for 1.5×), solar absorptivity 0.15 (white paint), at 1 AU; as a share of each section's heat (three tiers lit). 0.27° is the Sun's own radius, the least tilt any panel sees.

| Axis tilt from the pole | Main section (drum) | Farm section (open) |
|---|---|---|
| 0.27° | 0 MW (0.0%) | 0.49 MW (0.2%) |
| 0.5° | 0 MW (0.0%) | 0.91 MW (0.5%) |
| 1° | 0 MW (0.0%) | 1.8 MW (0.9%) |
| 1.5° | 0.36 MW (0.2%) | 2.7 MW (1.4%) |
| 2° | 0.64 MW (0.4%) | 3.6 MW (1.8%) |
| 3° | 0.84 MW (0.5%) | 5.4 MW (2.7%) |
| 5° | 2.3 MW (1.5%) | 8.7 MW (4.3%) |

The drum's panels see no direct sunlight below ~1.5° of tilt: the tori shade them, through the ends and through the gaps alike. The open farm section takes ~0.9% of its heat per degree of tilt at 1 AU, up to ×1.5–1.8 at the nearest candidates' perihelia and ×2 as the paint ages towards ~0.3: **a few degrees cost a few percent**, so the axis needs holding only roughly (within ~1–2°), trimmed as the orbit plane drifts over centuries.

## Coolant loops

Single-phase water, 10 K warmer leaving the heat source, 12 loops per torus or farm ring (`thermal_model/coolant.py`). Main section: natural circulation from the rim to the radiators' centroid, pipes sized so that friction uses up the buoyancy head (out and back, radiators' own tubes not counted). Farm section, radiators outboard: pumped at 2 m/s, the pump also working against the buoyancy that resists the warm coolant sinking. Per torus or farm ring, six-stacks with three tiers lit.

| Torus | Valley's heat | Pipe (each loop) | Speed | Buoyancy head | Water in the loops | Farm ring's heat | Pipe (each loop) | Pumping |
|---|---|---|---|---|---|---|---|---|
| 900 m | 26.4 MW | 0.34 m | 0.60 m/s | 4.2 kPa | 0.51 kt | 33.5 MW | 0.21 m | 100 kW (0.30%) |
| 1.6 km | 83.5 MW | 0.52 m | 0.79 m/s | 7.4 kPa | 2.1 kt | 106 MW | 0.37 m | 295 kW (0.28%) |

**Main section: passive, as intended.** A few tenths of a kPa per kelvin of buoyancy, over hundreds of metres of spin gravity, drive ~0.3 m pipes at under 1 m/s; the loops hold ~0.5 kt of water per 900 m torus (~0.8% of its water budget, local). **Farm section: pumps** of ~0.3% of its heat.

**Two-phase loops need throttling.** An evaporating loop (ammonia, as on the ISS) would carry the heat in far smaller pipes, but the liquid returning outward from the radiators builds a column of hundreds of metres of near-1 g head: at the rim it is far above its saturation pressure and can't boil at the valley's temperature unless throttled (or run through a turbine) just before the evaporator.

| Torus | Fluid | Saturation pressure at 285 K | Liquid pressure at the rim | Boils at |
|---|---|---|---|---|
| 900 m | ammonia | 620 kPa | 1.9 MPa | 47.6 °C |
| 900 m | water | 1.40 kPa | 2.0 MPa | 195 °C |
| 1.6 km | ammonia | 620 kPa | 2.8 MPa | 63.5 °C |
| 1.6 km | water | 1.40 kPa | 3.5 MPa | 220 °C |

## The valley's day and night

Steady-periodic swing of a 900 m valley under a 12 h day (`thermal_model/valley.py`): the sky's 15.0 mol/m² of light, ~76.4 W/m² while lit, all ending as heat in the valley; the air (~42.8 m of it per m² of floor, 856 J/m³K at 70.0 kPa), the vegetation's water and the ponds as heat capacity; the soil as a semi-infinite conductor (its daily swing reaches ~10–13 cm); the cooling taking heat out at U towards a coolant at a fixed temperature (the cold ceiling's radiation and the air handling). Peak-to-peak, at three couplings:

| Valley | Capacity (air, plants, ponds) | Soil effusivity (W s½/m²K) | U = 3 W/m²K | U = 7 (baseline) | U = 15 |
|---|---|---|---|---|---|
| Arid canyon | 49.2 kJ/m²K | 624 | 11 K | 7.5 K | 4.4 K |
| Baseline | 162 kJ/m²K | 1,940 | 4.2 K | 3.7 K | 2.9 K |
| Fern gully | 476 kJ/m²K | 1,940 | 2.5 K | 2.4 K | 2.1 K |

Left to itself the valley swings a few kelvin: the soil's admittance (~5–17 W/m²K at a daily period) and the ponds hold it, so a wet valley stays within ~2–4 K and a dry canyon ~4–11 K. Wider swings (the notes' ~15 °C canyon) need the cooling scheduled: more at night through the cold ceiling, less by day.

Not modelled: the spokes and cables in the ray tracing, the envelopes' rounded inner faces, the radiators' own tubes and their pressure, freezing in cold panels when the load drops, sunlight reflected between panels, the despun array's shadow, and the valley's air movement.
