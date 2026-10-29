# Replication logistics

Plan §5 (`logistics_model/`): the water per torus by use, where it comes from, the transfers and propulsion that ship the C-type's products, and the flows of a generation. Designs: 900 m pairs and 1.6 km six-stacks at Eros (LL host), Ryugu as the C-type.

## Water per torus

Built up from its uses instead of fitted to the notes' totals: soil moisture (25% of 0.5 m of soil), ponds and streams on 2% of the floor at 1.00 m mean depth (kept small: water access for the biosphere, not a main feature; within the fill), the water electrolysed for the O₂, ballast to trim an operational imbalance of 0.05% of the rim's mass (water spread as 1 − cos around the rim, e M in all), and the vegetation's water (~10.0 kg/m² of floor). Not counted: coolant loops (plan §6), people, stores and pipes (hundreds of tonnes), the algae trays (~200 m³).

| Use | 900 m | 1.6 km | 2.5 km |
|---|---|---|---|
| Soil moisture | 39.8 kt | 126 kt | 307 kt |
| Ponds and streams | 6.36 kt | 20.1 kt | 49.1 kt |
| Electrolysed for the O₂ (valley and farm ring) | 4.45 kt | 24.2 kt | 91.2 kt |
| Ballast | 5.94 kt | 18.2 kt | 44.0 kt |
| Vegetation | 3.18 kt | 10.1 kt | 24.5 kt |
| **Total** | **0.060 Mt** | **0.20 Mt** | **0.52 Mt** |
| Notes until now (fitted, no breakdown) | ~0.15 Mt | ~0.4 Mt | ~0.9 Mt |
| Spin-up with water thrusters, if chosen | 0.40 Mt | 1.7 Mt | 5.6 Mt |
| Water in the nitrogen-sized C-type | 0.32 Mt | 1.8 Mt | 6.6 Mt |

Soil moisture is about two thirds of it, the ponds about a tenth. The C-type sized by nitrogen holds ~5–13× the water needed, so water never sizes the C-type unless spin-up uses water thrusters (900 m).

## Where the water comes from

Water is 89% oxygen, which the S-type has in its silicates. Ship only the hydrogen (split from the C-type's water) and take the oxygen as the by-product of molten-oxide electrolysis (notes §10, proposed; ~0.29 kg of oxygen per kg of iron): on an LL host the iron the free metal lacks already frees more oxygen than the water needs, so the oxygen costs nothing extra. Hydrogen is hard to store (20 K); methane (111 K) carries it with carbon, which replaces the organics shipped for the soil, and burnt with the same oxygen it is a storable rocket propellant (methalox, ~3.6 km/s) for tugs and docking. Shipping by electric thrusters at the notes' Ryugu → Eros Δv; the other energy is splitting the water at the C-type (and any iron reduced only for its oxygen). Hydrogen and methane ship the same mass while the methane's carbon stays below the organics needed: its carbon replaces as much organics.

| Stack (per torus) | Route | Shipped | Shipping | Other energy | Total |
|---|---|---|---|---|---|
| 900 m pair | Water | 100.0 kt | 12.7 PJ | 0 PJ | 12.7 PJ |
| 900 m pair | Hydrogen (H₂), oxygen from the silicates | 47.0 kt | 5.97 PJ | 1.2 PJ | 7.17 PJ |
| 900 m pair | Methane, oxygen from the silicates | 47.0 kt | 5.97 PJ | 1.2 PJ | 7.17 PJ |
| 1.6 km six-stack | Water | 345 kt | 43.9 PJ | 0 PJ | 43.9 PJ |
| 1.6 km six-stack | Hydrogen (H₂), oxygen from the silicates | 169 kt | 21.5 PJ | 4.0 PJ | 25.5 PJ |
| 1.6 km six-stack | Methane, oxygen from the silicates | 169 kt | 21.5 PJ | 4.0 PJ | 25.5 PJ |

| Stack | Iron reduced to free the water's oxygen | Iron the free metal lacks (LL host) | Electrolysis if the host mines more rock instead | Hydrogen | Carbon in the methane | Organics needed |
|---|---|---|---|---|---|---|
| 900 m pair | 0.19 Mt | 0.94 Mt | 1.9 PJ | 6.68 kt | 19.9 kt | 31.8 kt |
| 1.6 km six-stack | 0.61 Mt | 5.9 Mt | 6.1 PJ | 22.2 kt | 66.1 kt | 101 kt |

On a host that mines more rock for its metal instead of electrolysing its silicates (the baseline on large hosts such as Eros), the iron reduced only for its oxygen costs the electrolysis in the third column, still below the shipping it saves.

## Transfers

Two-impulse rendezvous, zero-revolution Lambert arcs between the two orbits, with the departure and arrival points and the flight time all free: the "best phase", a lower bound whatever the bodies' positions (`logistics_model/transfers.py`). Elements rounded from JPL's Small-Body Database as recalled: current ephemerides (JPL Horizons) are blocked from this environment, so the notes' dated values stay as quoted. The synodic period is how often the same phasing recurs, so how far apart the good windows are.

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
| 900 m pair | Electric thrusters (baseline) | 30 km/s | 60% | 0.017 Mt | — | 12.7 PJ | 40.0 N/MW |
| 900 m pair | Electrothermal, water | 6.0 km/s | 35% | 0.12 Mt | 0.26 Mt | 6.11 PJ | 117 N/MW |
| 900 m pair | Mass driver, energy-optimal | 2.9 km/s | 50% | 0.39 Mt | 4.5 Mt | 3.41 PJ | 339 N/MW |
| 1.6 km six-stack | Electric thrusters (baseline) | 30 km/s | 60% | 0.059 Mt | — | 43.9 PJ | 40.0 N/MW |
| 1.6 km six-stack | Electrothermal, water | 6.0 km/s | 35% | 0.41 Mt | 1.6 Mt | 21.1 PJ | 117 N/MW |
| 1.6 km six-stack | Mass driver, energy-optimal | 2.9 km/s | 50% | 1.4 Mt | 25 Mt | 11.8 PJ | 339 N/MW |

Efficiencies are estimates or guesses (mass driver 50%, range 30–80%); the mass driver uses less electricity than the baseline down to ~13% efficiency.

## A generation

A parent stack builds a child stack torus by torus, so a cluster doubles once per generation. **What a child is made of**, per torus (the torus, its share of the hub and factory metal, its farm ring and its array), by source: the host's rock and metal, the C-type's shipped products, and imported vitamins (the array's silicon at 0.400 kg/m², and ~50.0 t of electronics, dopants, catalysts and the like per 900 m torus, a guess).

| Stack (per torus) | Built | From the host | Shipped from the C-type | Vitamins |
|---|---|---|---|---|
| 900 m pair | 13.1 Mt | 99.23% | 100.0 kt (0.76%) | 420 t (0.003%) |
| 1.6 km six-stack | 43.0 Mt | 99.19% | 345 kt (0.80%) | 1,330 t (0.003%) |

**Energy floor on the generation**, with the factory at 1.00 GW per stack: processing and shipping as in the system model (water route, electric thrusters), then the cheapest combination found here (methane route, mass driver).

| Stack (per torus) | Processing | Shipping | Generation (yr) | Best combination | Generation (yr) |
|---|---|---|---|---|---|
| 900 m pair | 10.4 PJ | 12.7 PJ | 1.5 | 13.2 PJ | 0.83 |
| 1.6 km six-stack | 55.5 PJ | 43.9 PJ | 19 | 65.3 PJ | 12 |

**Rates for a given generation**, per torus of the parent (a stack's lines handle n times these), against Earth benchmarks (orders of magnitude, unsourced): the largest open-pit mines move ~0.5 Mt of material a day, a large steelworks makes ~10 Mt of steel a year. Cargo per window: one Ryugu → Eros window every ~4.9 years (synodic period).

| Stack | Generation | S-type mined a day (share of a large mine) | Metal a day (share of a large steelworks) | Rock placed a day | C-type baked a day | Cargo per window | Mean power |
|---|---|---|---|---|---|---|---|
| 900 m pair | 10 yr | 8.98 kt (1.8%) | 404 t (1.5%) | 3.16 kt | 1.4 kt | 49.3 kt | 73.1 MW |
| 900 m pair | 25 yr | 3.59 kt (0.7%) | 162 t (0.6%) | 1.26 kt | 0.55 kt | 19.7 kt | 29.3 MW |
| 1.6 km six-stack | 10 yr | 45.9 kt (9.2%) | 2,060 t (7.5%) | 9.64 kt | 7.5 kt | 170 kt | 315 MW |
| 1.6 km six-stack | 25 yr | 18.3 kt (3.7%) | 825 t (3.0%) | 3.86 kt | 3.0 kt | 68.1 kt | 126 MW |

**Growth.** A cluster started by one stack, doubling every generation, until Ryugu's nitrogen runs out:

| Stack | Generation | Tori after 50 years | After 100 years | Tori Ryugu supports | Years to reach it |
|---|---|---|---|---|---|
| 900 m pair | 10 yr | 64 | 2,048 | 89 | 55 |
| 900 m pair | 25 yr | 8 | 32 | 89 | 140 |
| 1.6 km six-stack | 10 yr | 192 | 6,144 | 16 | 14 |
| 1.6 km six-stack | 25 yr | 24 | 96 | 16 | 36 |

Not modelled: factory throughput as a function of its own mass (how fast a factory copies itself), people and training, seed transfers to new sites, the freighters' own mass and power (their solar arrays are silicon, a vitamin), failures and spares, and dated windows from current ephemerides.
