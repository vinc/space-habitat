# 6 × 900 m tori, 2 farm tiers lit, L host, site Eros, C-type Ryugu

## Geometry

|  | Per torus | Stack of 6 |
|---|---|---|
| Period / rpm / rim speed | 60.0 s / 1.0 / 94.2 m/s |  |
| Spin gravity | 1.0 g at the floor, 0.068 g at the hub rim |  |
| Tube width / hub radius | 56.2 m / 60.8 m |  |
| Floor area | 31.8 ha | 191 ha |
| Air volume | 13.6 million m³ | 81.7 million m³ |
| Rock jacket / envelope radius (jacket + crawl space) | 5.5 m / 35.1 m |  |
| Pitch / clear gap / stack length | 80.2 m / 10.0 m | 895 m |
| Farm section: farm ring radius / crops per tier | 360 m / 9.16 ha |  |
| Farm section: ring pitch / section length / gap to the main section | 60.6 m | 364 m / 50.0 m |
| Main section length / whole stack |  | 482 m / 895 m |

## Mass

|  | Per torus | Stack of 6 |
|---|---|---|
| Rock shield (after fill credit) | 11.0 Mt | 66.1 Mt |
| Fill (soil + regolith) | 0.541 Mt | 3.24 Mt |
| Hull and frames | 0.300 Mt | 1.80 Mt |
| Cable spokes | 0.868 Mt | 5.21 Mt |
| Water needed / N₂ / O₂ | 0.124 Mt / 7.92 kt / 3.68 kt |  |
| **Total** (excl. hub and factory) | **12.8 Mt** | **76.9 Mt** |
| Per m² of floor | 40.3 t |  |
| Farm ring: shell and growing systems / its spokes / its N₂ (at the farm's pressure) | 48.6 / 0.56 / 0.57 kt |  |
| Despun array / radiator panels (ideal) | 4.18 / 0.812 kt |  |
| Spin-up propellant (water, if used) | 0.402 Mt |  |

## Materials and mining

|  | Per torus | Stack of 6 |
|---|---|---|
| Metal needed (with hub, dock, factory) | 1.48 Mt | 8.89 Mt |
| S-type (L host), sized by metal | 16.5 Mt (~251 m) | 98.8 Mt |
| Spare tailings | 3.69 Mt |  |
| C-type, sized by nitrogen | 5.05 Mt (~200 m) | 30.3 Mt |
| Water / carbon in the C-type | 0.323 / 0.227 Mt |  |
| **Mined** | **21.5 Mt** | **129 Mt** |
| Copper contained (S + C) | 1.50 + 0.636 kt |  |

Trace elements (demands mostly guesses from the notes; `--trace` for the table): short: K; unbudgeted: Cr, Zn, Mo, Sn.

Eros (LL-like, ~6,700,000 Mt) supplies ~200,000 tori of this size by free metal; Ryugu (~450 Mt) ~89 by nitrogen.

## Power and light

|  | Per torus | Stack of 6 |
|---|---|---|
| Valley sky + other loads | 52.6 + 4.77 MW | 344 MW |
| Farm lighting per tier lit | 32.1 MW | 192 MW |
| **Total electricity** | **122 MW** | **729 MW** |
| Despun array at 1 AU, constant sky | 0.561 km² | 3.37 km² |
| Despun array at Eros (0.32× sunlight at aphelion, seasonal sky) | 1.39 km² | 8.37 km² |

## Food

|  | Per torus | Stack of 6 |
|---|---|---|
| Light on the crops per person | 3,240 mol/day |  |
| Crop area / electricity per person | 90.1 m² / 31.5 kW |  |
| People per tier lit | 1,020 | 6,100 |
| **People fed** | **2,030** | **12,200** |
| Floor per person | 156 m² |  |

## Heat

|  | Per torus | Stack of 6 |
|---|---|---|
| Main section (valleys and other loads) | 57.4 MW | 344 MW |
| Farm section (tiers lit) | 64.2 MW | 385 MW |
| Main section: ideal limit of its two open ends, black bodies at ~285 K |  | 1.64 GW |
| Main section: ideal margin / break-even (upper bounds) |  | 4.8× / 29 tori |
| Ideal radiating surface, black body, lower bound (two-sided panels: half) | 32.5 ha | 195 ha |

Preliminary radiative exchange (ray tracing, emissivity 0.9), each section on its own:
- main section (drum, ends only): rejects at most 1.36 GW (83% of its ideal limit), a margin of 4.0×; needs 58.4 ha of panels (5% of its radiator annuli), against 51.1 ha ideally.
- farm section (open, radiators to 900 m): rejects at most 1.99 GW, a margin of 5.2×; needs 62.8 ha of panels (5% of its radiator annuli), against 57.2 ha ideally.
- the whole stack, traced together: margins of 2.6× (main) and 2.9× (farm) at 100% / 35% panel coverage, so both sections can be cooled.

## Stability (rigid stack)

|  | Per torus | Stack of 6 |
|---|---|---|
| I_axis / I_transverse, tori alone / whole stack |  | 1.91 / 1.91 (stable with a 20% margin) |
| Max tori at this gap: tori alone, no margin / 10% / 20%; whole stack, 20% |  | 27 / 24 / 22; 22 |

## Processing and replication

|  | Per torus | Stack of 6 |
|---|---|---|
| Crushing S-type / baking C-type | 1.40 / 7.57 PJ |  |
| Shipping 0.164 Mt of volatiles (Ryugu → Eros, 4.7 km/s) | 20.9 PJ |  |
| Energy, processing + shipping | 29.8 PJ | 179 PJ |
| Generation time at 1 GW (energy only) |  | 5.7 years |
