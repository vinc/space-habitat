# Closed atmosphere: balance, failures, startup and Biosphere 2

Plan §7 (`ecology_model/`): a compartment model of one torus's air (O2, CO2, N2), its farm ring's crops, its people, the soil's organic carbon and the valley's vegetation; the farm's air quasi-steady, exchanged with the valleys' through the hub ducts. Most inputs are estimates or guesses (`reports/assumptions.md`).

## A torus in balance

Per torus of a six-stack, three farm tiers lit (`ecology_model/closed.py`). The farm fixes its share of its people's food and the valley's gardens the rest, half of it edible (`harvest_index`); people eat it and breathe it out; the inedible half is composted into the soil and respired; the valley's grown woodland sheds as much as it grows. The farm's air is held at ~1,000 ppm-equivalent of CO2 (100 Pa), exchanged with the valleys' through the hub ducts at 400 m³/s, so the valleys sit a little above it. The O2 store is the air's own: years of breathing.

| Torus | People | O2 in the air | O2 breathed a day | Air's O2 / breathing | Valley CO2 | Farm CO2 | Soil carbon, at equilibrium |
|---|---|---|---|---|---|---|---|
| 900 m | 3,050 | 3.95 kt | 2.2 t | 4.8 yr | 108 Pa | 100 Pa | 13 kg/m² |
| 1.6 km | 9,650 | 21.5 kt | 7.1 t | 8.3 yr | 125 Pa | 100.0 Pa | 13 kg/m² |

## Failures

From a torus in balance, uncontrolled for a year: days until the valleys' CO2 passes 500 Pa (~5,000 ppm at sea level) and the O2 falls below 17 kPa, the worst of each; then the oxygen a physico-chemical plant must recover from CO2 (a Bosch or Sabatier reactor with electrolysis, undoing respiration as photosynthesis does) to hold both, at 25 MJ per kg of O2. The farm's crops take up more CO2 as it rises (x / (x + 35 Pa)), which buffers small upsets on its own.

| Torus | Scenario | CO2 limit after | O2 limit after | Peak CO2 | Lowest O2 | Food store (90 days) runs out after | Recovery needed at peak |
|---|---|---|---|---|---|---|---|
| 900 m | One farm tier dark | 113 days | never (1 yr) | 1,020 Pa | 19.3 kPa | never (36 days left) | 0.57 t/day (0.17 MW) |
| 900 m | Two tiers dark (the pumps' passive fallback) | 36 days | 330 days | 3,370 Pa | 16.7 kPa | 169 days | 2.1 t/day (0.60 MW) |
| 900 m | The whole farm dark | 22 days | 176 days | 5,910 Pa | 13.9 kPa | 97 days | 3.6 t/day (1.0 MW) |
| 900 m | Soil burst, +1 µmol/m²/s fading over 1 yr | never (1 yr) | never (1 yr) | 256 Pa | 20.1 kPa | never (179 days left) | 0 t/day (0 MW) |
| 1.6 km | One farm tier dark | 193 days | never (1 yr) | 710 Pa | 19.6 kPa | never (30 days left) | 1.7 t/day (0.50 MW) |
| 1.6 km | Two tiers dark (the pumps' passive fallback) | 60 days | never (1 yr) | 2,040 Pa | 18.2 kPa | 167 days | 6.4 t/day (1.9 MW) |
| 1.6 km | The whole farm dark | 36 days | 320 days | 3,490 Pa | 16.6 kPa | 97 days | 11 t/day (3.2 MW) |
| 1.6 km | Soil burst, +1 µmol/m²/s fading over 1 yr | never (1 yr) | never (1 yr) | 251 Pa | 20.1 kPa | never (176 days left) | 0 t/day (0 MW) |

A dark tier costs food before it costs air: the crops fertilised by the extra CO2 make up only part of it, and the store runs down. Once it is empty the model has people breathe out their body reserves (tracked, so the carbon still closes); later crossings assume no resupply, so read them as bounds. Relighting the tiers or bringing food in ends it.

## A new torus

A 900 m torus filled with its soil (imported organics at 0.1 t/m², ~50 kg C/m²) and young woodland (1 kg C/m², growing towards 8), its farm lit for its people. The soil's organic carbon respires towards the much smaller stock the residues and litter keep up: as Biosphere 2's compost-rich soil did, it draws down the O2 and loads the air with CO2, far faster than people do. Ten years, uncontrolled and with recovery:

| Soil | CO2 limit after | O2 limit after | Recovery at peak | O2 recovered, t/day at 0.5 / 2 / 5 yr | O2 recovered over 10 yr |
|---|---|---|---|---|---|
| As planned: imported organics, 30% fast-decaying | 3 days | 25 days | 7.8 MW | 17 / 4.7 / 0.88 | 12 kt |
| Organics composted before they go in (5% fast-decaying) | 16 days | 161 days | 1.4 MW | 3.7 / 2.3 / 1.4 | 5.9 kt |
| Half the organics, the rest grown from residues | 7 days | 61 days | 3.4 MW | 7.1 / 1.4 / 0 | 3.9 kt |

## Leaks

A hole in a 900 m torus's pressure hull, air escaping at the speed of sound (choked flow, discharge coefficient 0.6) from 70 kPa: time to lose a tenth of the air, and so of the pressure. A background leak of 0.1% of the air a year (seals, docking, airlocks) is in every run above.

| Hole | Air lost | 10% of the air gone after |
|---|---|---|
| 1 cm | 0.0079 kg/s | 1,930 days |
| 10 cm | 0.79 kg/s | 19 days |
| 100 cm | 79 kg/s | 4.6 hours |

The rock jacket and the crawl space keep meteoroids off the pressure hull (notes §13); holes would come from failures, so a 10 cm one leaves weeks and a 1 m one hours.

## Biosphere 2, replayed

Biosphere 2 (1991–1993): O2 fell from ~20.9% to ~14.2% in ~16 months, as the compost-rich soil respired and the CO2 went largely into the concrete. Its figures here are approximate, recalled, not sourced (~1.27 ha, ~1.8 × 10⁵ m³ of air at ~1 atm, eight people on ~2,000 kcal a day). The replay runs its oxygen bookkeeping through the same model, with the CO2 held near 1,500 ppm by the concrete, and fits the net soil respiration that photosynthesis didn't return. It checks the model's accounting, not its soil: Biosphere 2's soil data aren't in the notes.

|  | Biosphere 2 | 900 m torus |
|---|---|---|
| Air per m² of floor | 16.8 kg | 39.1 kg |
| Net soil respiration beyond photosynthesis, fitted | 1.2 µmol/m²/s | — |
| CO2 into the concrete over the 16 months | 25.1 t | no concrete |
| The same excess per m²: CO2 limit after | (held by the concrete) | 231 days |
| … O2 limit after | ~a year to 14% | never (1 yr) |

~1 µmol/m²/s is a fraction of ordinary soil respiration (several µmol/m²/s), so a small imbalance is enough. In a torus the same imbalance shows first as CO2, within months, because nothing like the concrete absorbs it, and the farm's crops, fertilised by it, return most of the oxygen.

Not modelled: water and humidity (condensed and recycled, notes §13), trace gases (methane, ethylene, volatiles from materials), nitrogen fixation and denitrification, the valley's daily CO2 swing, people's movement between tori, the seasons of a seasonal sky, and the controls' own failures.
