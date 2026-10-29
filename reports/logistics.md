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

Two-impulse rendezvous, zero-revolution Lambert arcs between the two orbits, with the departure and arrival points and the flight time all free: the "best phase", a lower bound whatever the bodies' positions (`logistics_model/transfers.py`). Elements rounded from JPL's Small-Body Database as recalled: current ephemerides (JPL Horizons) are blocked from this environment, so the notes' dated values stay as quoted. The synodic period is the cycle of the two bodies' mean longitudes, a timescale for windows, not a result: the best-phase geometry does not recur with it (both orbits are eccentric and inclined, so after one synodic period the bodies sit elsewhere on them), and when good windows recur needs a dated search.

| Transfer | Best phase (model) | Best phase (notes) | Dated, 2030–2060 (notes) | Flight (days) | Synodic period (yr) | Perihelion longitudes |
|---|---|---|---|---|---|---|
| Ryugu → Eros | 4.5 km/s | 4.5 km/s | 4.7 km/s | 316 | 4.9 | 103° / 123° |
| Bennu → Eros | 5.7 km/s | 5.8 km/s | 6.2 km/s | 185 | 3.7 | 68.3° / 123° |
| Ryugu → Itokawa | 6.3 km/s | 6.3 km/s | 6.3 km/s | 366 | 8.7 | 103° / 232° |
| Bennu → Itokawa | 8.2 km/s | 8.3 km/s | 8.5 km/s | 199 | 5.6 | 68.3° / 232° |
| Ryugu → Apophis 2029 | 5.4 km/s | 5.5 km/s | — | 330 | 11 | 103° / 331° |
| Bennu → Apophis 2029 | 7.4 km/s | 7.4 km/s | — | 409 | 37 | 68.3° / 331° |
| Ryugu → Torifune | 7.6 km/s | 7.6 km/s | 7.6 km/s | 274 | 5.5 | 103° / 255° |
| Itokawa → Torifune | 3.5 km/s | 3.6 km/s | 3.6 km/s | 162 | 3.4 | 232° / 255° |
| Itokawa → Eros | 7.8 km/s | 7.8 km/s | — | 458 | 11 | 232° / 123° |
| Earth → Eros | 6.9 km/s | 6.9 km/s | — | 295 | 2.3 | 103° / 123° |
| Earth → Torifune | 4.1 km/s | 4.0 km/s | — | 217 | 21 | 103° / 255° |
| Ryugu → Didymos | 7.1 km/s | — | — | 569 | 3.4 | 103° / 32.5° |

The model reproduces the notes' best-phase values within ~0.1 km/s, except to Torifune (0.1–0.4 km/s lower; its elements are the least certain here). Low-thrust transfers need somewhat more than these impulsive values.

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

**Rates for a given generation**, per torus of the parent (a stack's lines handle n times these), against Earth benchmarks (orders of magnitude, unsourced): the largest open-pit mines move ~0.5 Mt of material a day, a large steelworks makes ~10 Mt of steel a year. Cargo per window: **assuming** one Ryugu → Eros window per synodic period (~4.9 years), not a result of the transfer search.

| Stack | Generation | S-type mined a day (share of a large mine) | Metal a day (share of a large steelworks) | Rock placed a day | C-type baked a day | Cargo per window (assumed cadence) | Mean power |
|---|---|---|---|---|---|---|---|
| 900 m pair | 10 yr | 8.99 kt (1.8%) | 404 t (1.5%) | 3.16 kt | 1.4 kt | 52.3 kt | 75.5 MW |
| 900 m pair | 25 yr | 3.59 kt (0.7%) | 162 t (0.6%) | 1.26 kt | 0.55 kt | 20.9 kt | 30.2 MW |
| 1.6 km six-stack | 10 yr | 45.9 kt (9.2%) | 2,060 t (7.5%) | 9.64 kt | 7.5 kt | 179 kt | 322 MW |
| 1.6 km six-stack | 25 yr | 18.3 kt (3.7%) | 826 t (3.0%) | 3.86 kt | 3.0 kt | 71.7 kt | 129 MW |

**Growth.** A cluster started by one stack, doubling every generation, until Ryugu's nitrogen runs out:

| Stack | Generation | Tori after 50 years | After 100 years | Tori Ryugu supports | Years to reach it |
|---|---|---|---|---|---|
| 900 m pair | 10 yr | 64 | 2,048 | 89 | 55 |
| 900 m pair | 25 yr | 8 | 32 | 89 | 140 |
| 1.6 km six-stack | 10 yr | 192 | 6,144 | 16 | 14 |
| 1.6 km six-stack | 25 yr | 24 | 96 | 16 | 36 |

Not modelled: factory throughput as a function of its own mass (how fast a factory copies itself), people and training, seed transfers to new sites, the freighters' own mass and power (their solar arrays are silicon, a vitamin), failures and spares, and dated windows from current ephemerides.
