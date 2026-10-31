# 2 × 900 m tori, 1 farm tier lit, L host, site 1 AU, C-type Ryugu

## Geometry

|  | Per torus | Stack of 2 |
|---|---|---|
| Period / rpm / rim speed | 60.0 s / 1.0 / 94.2 m/s |  |
| Spin gravity | 1.0 g at the floor, 0.068 g at the hub rim |  |
| Tube width / hub radius | 56.2 m / 60.8 m |  |
| Floor area | 31.8 ha | 63.6 ha |
| Air volume | 13.6 million m³ | 27.2 million m³ |
| Rock jacket / envelope radius (jacket + crawl space) | 5.5 m / 35.1 m |  |
| Pitch / clear gap / stack length | 80.2 m / 10.0 m | 332 m |
| Farm section: farm ring radius / crops per tier | 360 m / 9.16 ha |  |
| Farm section: ring pitch / section length / gap to the main section | 60.6 m | 121 m / 50.0 m |
| Main section length / whole stack |  | 160 m / 332 m |

## Mass

|  | Per torus | Stack of 2 |
|---|---|---|
| Rock shield (after fill credit) | 11.0 Mt | 22.0 Mt |
| Fill (soil + regolith) | 0.541 Mt | 1.08 Mt |
| Hull and frames | 0.300 Mt | 0.600 Mt |
| Cable spokes | 0.864 Mt | 1.73 Mt |
| Water needed / N₂ / O₂ | 0.0656 Mt / 7.92 kt / 3.68 kt |  |
| **Total** (excl. hub and factory) | **12.7 Mt** | **25.5 Mt** |
| Per m² of floor | 40.1 t |  |
| Farm ring: shell and growing systems / its spokes / its N₂ (at the farm's pressure) | 48.6 / 0.56 / 0.57 kt |  |
| Despun array / radiator panels (ideal) | 0.371 / 0.251 kt |  |
| Spin-up propellant (water, if used) | 0.400 Mt |  |

## Materials and mining

|  | Per torus | Stack of 2 |
|---|---|---|
| Metal needed (with hub, dock, factory) | 1.48 Mt | 2.95 Mt |
| S-type (L host), sized by metal | 16.4 Mt (~250 m) | 32.8 Mt |
| Spare tailings | 3.64 Mt |  |
| C-type, sized by nitrogen | 5.05 Mt (~200 m) | 10.1 Mt |
| Water / carbon in the C-type | 0.323 / 0.227 Mt |  |
| **Mined** | **21.5 Mt** | **42.9 Mt** |
| Copper contained (S + C) | 1.49 + 0.636 kt |  |

Trace elements (demands mostly guesses from the notes; `--trace` for the table): short: K; unbudgeted: Cr, Zn, Mo, Sn.

## Power and light

|  | Per torus | Stack of 2 |
|---|---|---|
| Valley sky + other loads | 21.7 + 4.77 MW | 52.9 MW |
| Farm lighting per tier lit | 11.2 MW | 22.3 MW |
| **Total electricity** | **37.6 MW** | **75.2 MW** |
| Despun array at 1 AU, constant sky | 0.174 km² | 0.347 km² |
| Despun array at 1 AU (1.0× sunlight at aphelion, seasonal sky) | 0.124 km² | 0.247 km² |

## Food

|  | Per torus | Stack of 2 |
|---|---|---|
| Light on the crops per person | 3,240 mol/day |  |
| Crop area / electricity per person | 90.1 m² / 11.0 kW |  |
| People per tier lit | 1,020 | 2,030 |
| **People fed** | **1,020** | **2,030** |
| Floor per person | 313 m² |  |

## Heat

|  | Per torus | Stack of 2 |
|---|---|---|
| Main section (valleys and other loads) | 26.4 MW | 52.9 MW |
| Farm section (tiers lit) | 11.2 MW | 22.3 MW |
| Main section: ideal limit of its two open ends, black bodies at ~285 K |  | 1.64 GW |
| Main section: ideal margin / break-even (upper bounds) |  | 31× / 62 tori |
| Ideal radiating surface, black body, lower bound (two-sided panels: half) | 10.0 ha | 20.1 ha |

Preliminary radiative exchange (ray tracing, emissivity 0.9), each section on its own:
- main section (drum, ends only): rejects at most 1.23 GW (75% of its ideal limit), a margin of 23×; needs 7.95 ha of panels (2% of its radiator annuli), against 7.85 ha ideally.
- farm section (open, radiators to 900 m): rejects at most 1.53 GW, a margin of 69×; needs 3.35 ha of panels (1% of its radiator annuli), against 3.31 ha ideally.
- the whole stack, traced together: margins of 18× (main) and 25× (farm) at 100% / 35% panel coverage, so both sections can be cooled.

## Stability (rigid stack)

|  | Per torus | Stack of 2 |
|---|---|---|
| I_axis / I_transverse, tori alone / whole stack |  | 1.99 / 1.99 (stable with a 20% margin) |
| Max tori at this gap: tori alone, no margin / 10% / 20%; whole stack, 20% |  | 27 / 24 / 22; 22 |

## Processing and replication

|  | Per torus | Stack of 2 |
|---|---|---|
| Crushing S-type / baking C-type | 1.39 / 7.57 PJ |  |
| Shipping 0.106 Mt of volatiles (Ryugu → 1 AU, no Δv known: pass --dv) | unknown |  |
| Energy, processing + shipping | unknown | unknown |
| Generation time at 1 GW (energy only) |  | unknown (≥ 0.57 years for processing alone) |
