# Replication logistics

Plan §5 (`logistics_model/`): the water per torus by use, where it comes from, the transfers and propulsion that ship the C-type's products, and the flows of a generation. Designs: 900 m pairs and 1.6 km six-stacks at Eros (LL host), Ryugu as the C-type.

## Water per torus

Built up from its uses instead of fitted to the notes' totals: soil moisture (25% of 0.5 m of soil), ponds and streams on 2% of the floor at 1.00 m mean depth (kept small: water access for the biosphere, not a main feature; within the fill), the water electrolysed for the O₂, ballast to trim an unbalanced mass of 0.05% of the rim's at the rim (water spread as A (1 − cos) around it: its first moment is only half its mass times the radius, so 2 e M of water), and the vegetation's water (~10.0 kg/m² of floor). Not counted: coolant loops (plan §6), people, stores and pipes (hundreds of tonnes), the algae trays (~200 m³).

| Use | 900 m | 1.6 km | 2.5 km |
|---|---|---|---|
| Soil moisture | 39.8 kt | 126 kt | 307 kt |
| Ponds and streams | 6.36 kt | 20.1 kt | 49.1 kt |
| Electrolysed for the O₂ (valley and farm ring) | 4.45 kt | 24.2 kt | 91.2 kt |
| Ballast | 11.9 kt | 36.4 kt | 88.0 kt |
| Vegetation | 3.18 kt | 10.1 kt | 24.5 kt |
| **Total** | **0.066 Mt** | **0.22 Mt** | **0.56 Mt** |
| Notes until now (fitted, no breakdown) | ~0.15 Mt | ~0.4 Mt | ~0.9 Mt |
| Spin-up with water thrusters, if chosen | 0.40 Mt | 1.7 Mt | 5.6 Mt |
| Water in the nitrogen-sized C-type | 0.32 Mt | 1.8 Mt | 6.6 Mt |

Soil moisture is about 60% of it, the ballast about a fifth, the ponds about a tenth. The C-type sized by nitrogen holds ~5–12× the water needed, so water never sizes the C-type unless spin-up uses water thrusters (900 m).

## Where the water comes from

Water is 89% oxygen, which the S-type has in its silicates. The alternative to shipping water: split it at the C-type, ship only the hydrogen and take the oxygen from the silicates by molten-oxide electrolysis (notes §10, proposed; ~0.29 kg of oxygen per kg of iron, so ~3.1 kg of iron per kg of water). Hydrogen is hard to store (20 K); methane (111 K) carries it with carbon, which replaces the organics shipped for the soil (the same mass as bare hydrogen while its carbon stays below the organics needed), and burnt with the same oxygen it is a storable rocket propellant (methalox, ~3.6 km/s) for tugs and docking. The baseline host gets all its metal as free metal and electrolyses nothing, so the oxygen is charged in full: the electrolysis's electricity and the furnace heat to melt the rock, less the crushing of the free-metal rock its iron replaces. Each route with each freighter (next section): electric thrusters at the notes' Ryugu → Eros Δv, or the energy-optimal mass driver.

| Stack (per torus) | Route | Shipped | Local oxygen and splitting | Electric thrusters: shipping | Total | Mass driver: shipping | Total |
|---|---|---|---|---|---|---|---|
| 900 m pair | Water | 106 kt | 0 PJ | 13.5 PJ | **13.5 PJ** | 3.6 PJ | **3.61 PJ** |
| 900 m pair | Hydrogen (H₂), oxygen from the silicates | 47.6 kt | 6.4 PJ | 6.06 PJ | **12.5 PJ** | 1.6 PJ | **8.05 PJ** |
| 900 m pair | Methane, oxygen from the silicates | 47.6 kt | 6.4 PJ | 6.06 PJ | **12.5 PJ** | 1.6 PJ | **8.05 PJ** |
| 1.6 km six-stack | Water | 363 kt | 0 PJ | 46.2 PJ | **46.2 PJ** | 12 PJ | **12.4 PJ** |
| 1.6 km six-stack | Hydrogen (H₂), oxygen from the silicates | 171 kt | 21 PJ | 21.8 PJ | **42.9 PJ** | 5.8 PJ | **27.0 PJ** |
| 1.6 km six-stack | Methane, oxygen from the silicates | 171 kt | 21 PJ | 21.8 PJ | **42.9 PJ** | 5.8 PJ | **27.0 PJ** |

| Stack | Iron electrolysed for the oxygen | Splitting the water | Electrolysis (electricity) | Melting the rock (furnace heat) | Crushing saved | Hydrogen | Carbon in the methane | Organics needed |
|---|---|---|---|---|---|---|---|---|
| 900 m pair | 0.20 Mt | 1.3 PJ | 2.0 PJ | 3.5 PJ | −0.38 PJ | 7.34 kt | 21.9 kt | 31.8 kt |
| 1.6 km six-stack | 0.67 Mt | 4.3 PJ | 6.7 PJ | 11 PJ | −1.3 PJ | 24.2 kt | 72.2 kt | 101 kt |

With electric thrusters, shipping the hydrogen saves a little; with mass drivers, shipping costs less than making the oxygen, so water is the cheaper cargo. Only a host that electrolyses its silicates for its iron anyway (a small LL host, notes §10) gets the oxygen without the electrolysis and the furnace heat: then only the splitting is left.

## Transfers

Two-impulse rendezvous on zero-revolution Lambert arcs (`logistics_model/transfers.py`). **Phase-free** ("best phase"): departure and arrival points and flight time all free, a lower bound whatever the bodies' positions, on the osculating elements of JPL's Small-Body Database (fetched 2026-10-30; within rounding of the ones recalled before). **Dated** (`windows.py`): on JPL Horizons' ephemerides (2027–2077, planets' perturbations and Apophis's 2029 flyby included, `logistics_model/data/`), departures every 5 days and flights of 60–900 days, each dip of the best-flight curve refined. A usable window: within 1 km/s of the pair's best in 2028–2072.

| Transfer | Best phase (model) | Best phase (notes) | Dated, 2030–2060 | Dated (notes) | Best, 2028–2072 | Usable windows |
|---|---|---|---|---|---|---|
| Ryugu → Eros | 4.51 km/s | 4.5 km/s | 4.66 km/s (2031-07) | 4.7 km/s | 4.52 km/s (2061-07, 318 d) | 8, every ~5.7 yr |
| Bennu → Eros | 5.74 km/s | 5.8 km/s | 5.90 km/s (2049-03) | 6.2 km/s | 5.90 km/s (2049-03, 174 d) | 10, every ~4.5 yr |
| Ryugu → Itokawa | 6.26 km/s | 6.3 km/s | 6.30 km/s (2051-06) | 6.3 km/s | 6.28 km/s (2069-09, 351 d) | 10, every ~4.2 yr |
| Bennu → Itokawa | 8.23 km/s | 8.3 km/s | 8.42 km/s (2059-02) | 8.5 km/s | 8.42 km/s (2059-02, 218 d) | 17, every ~2.5 yr |
| Ryugu → Apophis 2029 | 5.45 km/s | 5.5 km/s | 5.77 km/s (2059-06) | — | 5.63 km/s (2069-11, 265 d) | 8, every ~4.7 yr |
| Bennu → Apophis 2029 | 7.43 km/s | 7.4 km/s | 8.65 km/s (2058-12) | — | 8.45 km/s (2067-03, 432 d) | 22, every ~2.0 yr |
| Ryugu → Torifune | 7.58 km/s | 7.6 km/s | 7.67 km/s (2056-09) | 7.6 km/s | 7.64 km/s (2061-11, 300 d) | 10, every ~4.2 yr |
| Itokawa → Torifune | 3.49 km/s | 3.6 km/s | 3.50 km/s (2048-01) | 3.6 km/s | 3.50 km/s (2048-01, 168 d) | 9, every ~4.6 yr |
| Itokawa → Eros | 7.81 km/s | 7.8 km/s | 7.80 km/s (2043-05) | — | 7.80 km/s (2043-05, 470 d) | 8, every ~5.0 yr |
| Earth → Eros | 6.87 km/s | 6.9 km/s | 6.92 km/s (2042-01) | — | 6.92 km/s (2042-01, 297 d) | 6, every ~6.9 yr |
| Earth → Torifune | 4.07 km/s | 4.0 km/s | 4.11 km/s (2047-06) | — | 4.11 km/s (2047-06, 201 d) | 8, every ~3.8 yr |
| Ryugu → Didymos | 7.14 km/s | — | 7.12 km/s (2058-06) | — | 7.12 km/s (2058-06, 582 d) | 14, every ~3.1 yr |

The dated search lands on the notes' quoted values within ~0.1 km/s (Bennu → Eros 0.3 lower), and on the phase-free bound within ~0.1–0.3 km/s at its best window: the bound is reached about once in a few decades. Usable windows come every ~2–7 years, not once per synodic period on the dot; a freighter fleet times its departures to them. Low-thrust transfers need somewhat more than these impulsive values.

## Better C-type partners

A catalogue search (`logistics_model/catalogue.py`, JPL's Small-Body Database, fetched 2026-10-30): 365 near-Earth asteroids that are classified in the C complex (19) or dark in NEOWISE's albedos (< 0.08, at least 0.3 km across), each with its phase-free Δv to the hosts, screened on a coarse grid and refined for the best dozen per host. Mass at Ryugu's bulk density (1.19 t/m³); tori its nitrogen could supply at ~5.0 Mt of C-type per 900 m torus (the system model's).

| Host | Candidate | Type | Albedo | Diameter | Mass | 900 m tori supplied | Best phase |
|---|---|---|---|---|---|---|---|
| Eros | (2015 DX198) | — | 0.023 | 0.35 km | 26.5 Mt | ~5 | **3.2 km/s** |
| Eros | 275611 (1999 XX262) | — | 0.046 | 1.5 km | 2,030 Mt | ~402 | **3.6 km/s** |
| Eros | (2002 BM26) | X | 0.023 | 0.84 km | 369 Mt | ~73 | **3.9 km/s** |
| Eros | 499582 (2010 TH19) | — | 0.044 | 0.46 km | 61.0 Mt | ~12 | **4.4 km/s** |
| Itokawa | 252558 (2001 WT1) | — | 0.062 | 0.53 km | 94.3 Mt | ~19 | **3.9 km/s** |
| Itokawa | (2010 GU21) | — | 0.025 | 0.51 km | 82.7 Mt | ~16 | **4.5 km/s** |
| Itokawa | (2000 AA6) | — | 0.026 | 0.32 km | 19.7 Mt | ~4 | **5.0 km/s** |
| Itokawa | (2015 DE176) | — | 0.048 | 0.68 km | 195 Mt | ~39 | **5.0 km/s** |
| Torifune | 252558 (2001 WT1) | — | 0.062 | 0.53 km | 94.3 Mt | ~19 | **2.8 km/s** |
| Torifune | 410777 (2009 FD) | — | 0.010 | 0.47 km | 65.5 Mt | ~13 | **5.4 km/s** |
| Torifune | 65679 (1989 UQ) | B | 0.033 | 0.92 km | 482 Mt | ~95 | **5.6 km/s** |
| Torifune | 363505 (2003 UC20) | — | 0.029 | 1.9 km | 4,110 Mt | ~815 | **5.7 km/s** |
| Didymos | 162741 (2000 WG6) | — | 0.014 | 3.9 km | 38,300 Mt | ~7,576 | **3.8 km/s** |
| Didymos | 7753 (1988 XB) | B | — | 1.5 km | 2,040 Mt | ~405 | **3.8 km/s** |
| Didymos | 190161 (2005 TJ174) | — | 0.040 | 3.0 km | 17,500 Mt | ~3,470 | **3.9 km/s** |
| Didymos | (2003 SS214) | — | 0.022 | 0.86 km | 391 Mt | ~77 | **4.4 km/s** |

Ryugu (448 Mt, ~89 tori) is at 4.5 km/s from Eros, 6.3 from Itokawa and 7.6 from Torifune. Dated, on Horizons' ephemerides:

| Transfer | Best, 2030–2060 | Best, 2028–2072 | Usable windows |
|---|---|---|---|
| Ryugu → Eros | 4.66 km/s (2031-07) | 4.52 km/s (2061-07) | every ~5.7 yr |
| 1999 XX262 → Eros | 3.95 km/s (2044-11) | 3.91 km/s (2067-11) | every ~1.9 yr |
| 2015 DX198 → Eros | 3.60 km/s (2030-02) | 3.19 km/s (2071-03) | every ~8.2 yr |
| Ryugu → Itokawa | 6.30 km/s (2051-06) | 6.28 km/s (2069-09) | every ~4.2 yr |
| 2001 WT1 → Itokawa | 3.86 km/s (2054-09) | 3.86 km/s (2054-09) | every ~4.5 yr |
| Ryugu → Torifune | 7.67 km/s (2056-09) | 7.64 km/s (2061-11) | every ~4.2 yr |
| 2001 WT1 → Torifune | 2.99 km/s (2053-01) | 2.99 km/s (2053-01) | every ~6.8 yr |

And what the lower Δv saves, per torus of a 1.6 km six-stack at Eros (electric thrusters, the system model's baseline):

| Volatiles from | Δv (best, 2030–2060) | Shipping | Energy per torus | Generation (yr) |
|---|---|---|---|---|
| Ryugu → Eros | 4.66 km/s | 45.8 PJ | 101 PJ | 19.3 |
| 1999 XX262 → Eros | 3.95 km/s | 38.4 PJ | 93.9 PJ | 17.9 |
| 2015 DX198 → Eros | 3.60 km/s | 34.8 PJ | 90.3 PJ | 17.2 |

**Proposed: characterise 1999 XX262 for Eros and 2001 WT1 for Itokawa and Torifune.** 1999 XX262 is ~1.5 km across, ~4.5× Ryugu's mass, ~0.71 km/s closer to Eros at its 2030–2060 windows and with usable windows ~3× as often; 2001 WT1 (~0.5 km) is ~2.4 km/s closer to Itokawa and ~4.7 closer to Torifune than Ryugu. **1999 XX262 is already a B-type**, like Bennu: visible and near-infrared spectra (Popescu et al. 2019; Marsset et al. 2022, MIT–Hawaii survey) and SDSS colours (Sergeyev et al. 2023) all give B, Mahlke et al. (2022) Ch, with the 0.7 µm band of water-bearing clays; NEOWISE puts it at 1.48 ± 0.01 km and albedo 0.044 (SsODNet, consulted 30 October 2026). Its nitrogen is unknown: the 3 µm band of hydrated minerals and ammonium (JWST, or IRTF at its 2033–2038 passes) comes next, then a sample. **2001 WT1** has only near-infrared colours from the VISTA survey (MOVIS, too uncertain to class it) and NEOWISE's albedo (~0.04–0.06, ~0.54 km): a spectrum first, at its October 2027 or October 2035 passes. Ryugu stays the baseline until then.

## Propulsion

Per torus's cargo (the water route), Ryugu → Eros at the notes' 4.7 km/s. Electricity per kg delivered is ½ (e^(Δv/vₑ) − 1) vₑ² / η, lowest at vₑ ≈ Δv / 1.59 (~3 km/s here): a fast exhaust saves propellant, not energy. A mass driver (a linear motor throwing pellets, O'Neill's reaction engine) can run there, using the C-type's baked residue, waste otherwise, as reaction mass; it also gives ~8× the thrust per watt, so shorter transfers for the same power.

| Stack (per torus) | Option | Exhaust | Efficiency | Propellant | Available at the C-type | Electricity | Thrust |
|---|---|---|---|---|---|---|---|
| 900 m pair | Electric thrusters (baseline) | 30 km/s | 60% | 0.018 Mt | — | 13.5 PJ | 40.0 N/MW |
| 900 m pair | Electrothermal, water | 6.0 km/s | 35% | 0.13 Mt | 0.26 Mt | 6.47 PJ | 117 N/MW |
| 900 m pair | Mass driver, energy-optimal | 2.9 km/s | 50% | 0.42 Mt | 4.5 Mt | 3.61 PJ | 339 N/MW |
| 1.6 km six-stack | Electric thrusters (baseline) | 30 km/s | 60% | 0.062 Mt | — | 46.2 PJ | 40.0 N/MW |
| 1.6 km six-stack | Electrothermal, water | 6.0 km/s | 35% | 0.43 Mt | 1.5 Mt | 22.2 PJ | 117 N/MW |
| 1.6 km six-stack | Mass driver, energy-optimal | 2.9 km/s | 50% | 1.4 Mt | 25 Mt | 12.4 PJ | 339 N/MW |

Efficiencies are estimates or guesses (mass driver 50%, range 30–80%); the mass driver uses less electricity than the baseline down to ~13% efficiency.

## A generation

A parent stack builds a child stack torus by torus, so a cluster doubles once per generation. **What a child is made of**, per torus (the torus, its share of the hub and factory metal, its farm ring and its array), by source: the host's rock and metal, the C-type's shipped products, and imported vitamins (the array's silicon at 0.400 kg/m², and ~50.0 t of electronics, dopants, catalysts and the like per 900 m torus, a guess).

| Stack (per torus) | Built | From the host | Shipped from the C-type | Vitamins |
|---|---|---|---|---|
| 900 m pair | 13.1 Mt | 99.19% | 106 kt (0.81%) | 420 t (0.003%) |
| 1.6 km six-stack | 43.0 Mt | 99.15% | 363 kt (0.85%) | 1,330 t (0.003%) |

**Energy floor on the generation**, with the factory at 1.00 GW per stack: processing and shipping as in the system model (water route, electric thrusters), then the cheapest combination of route and freighter above (900 m pair: water by mass driver; 1.6 km six-stack: water by mass driver).

| Stack (per torus) | Processing | Shipping | Generation (yr) | Best combination | Generation (yr) |
|---|---|---|---|---|---|
| 900 m pair | 10.4 PJ | 13.5 PJ | 1.5 | 14.0 PJ | 0.89 |
| 1.6 km six-stack | 55.6 PJ | 46.2 PJ | 19 | 67.9 PJ | 13 |

**Rates for a given generation**, per torus of the parent (a stack's lines handle n times these), against Earth benchmarks (orders of magnitude, unsourced): the largest open-pit mines move ~0.5 Mt of material a day, a large steelworks makes ~10 Mt of steel a year. Cargo per window: one usable Ryugu → Eros window every ~5.7 years (dated search, above).

| Stack | Generation | S-type mined a day (share of a large mine) | Metal a day (share of a large steelworks) | Rock placed a day | C-type baked a day | Cargo per window | Mean power |
|---|---|---|---|---|---|---|---|
| 900 m pair | 10 yr | 8.99 kt (1.8%) | 404 t (1.5%) | 3.16 kt | 1.4 kt | 60.1 kt | 75.5 MW |
| 900 m pair | 25 yr | 3.59 kt (0.7%) | 162 t (0.6%) | 1.26 kt | 0.55 kt | 24.0 kt | 30.2 MW |
| 1.6 km six-stack | 10 yr | 45.9 kt (9.2%) | 2,060 t (7.5%) | 9.64 kt | 7.5 kt | 206 kt | 322 MW |
| 1.6 km six-stack | 25 yr | 18.3 kt (3.7%) | 826 t (3.0%) | 3.86 kt | 3.0 kt | 82.4 kt | 129 MW |

**Growth.** A cluster started by one stack, doubling every generation, until Ryugu's nitrogen runs out:

| Stack | Generation | Tori after 50 years | After 100 years | Tori Ryugu supports | Years to reach it |
|---|---|---|---|---|---|
| 900 m pair | 10 yr | 64 | 2,048 | 89 | 55 |
| 900 m pair | 25 yr | 8 | 32 | 89 | 140 |
| 1.6 km six-stack | 10 yr | 192 | 6,144 | 16 | 14 |
| 1.6 km six-stack | 25 yr | 24 | 96 | 16 | 36 |

Not modelled: factory throughput as a function of its own mass (how fast a factory copies itself), people and training, seed transfers to new sites, the freighters' own mass and power (their solar arrays are silicon, a vitamin), failures and spares, low-thrust and multi-revolution transfers, and gravity assists.
