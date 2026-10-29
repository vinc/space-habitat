# Replication logistics (plan §5)

The water per torus by use and where it comes from, the transfers and propulsion that ship the C-type's products, and the flows of a generation. It uses the system model (`habitat_model`) for masses, materials and energies, and adds a Lambert solver for the transfers. Plain Python and numpy.

```bash
python -m logistics_model                         # full report (reports/logistics.md), ~45 s
python -m logistics_model --set lake_floor_frac=0.2
```

| File | Contents |
|---|---|
| `water.py` | the water budget by use (from the system model) and three ways to supply it: ship water, or ship only its hydrogen (as H₂ or methane) and take the oxygen from the silicates |
| `transfers.py` | orbital elements, a vectorised zero-revolution Lambert solver (universal variables), phase-free ("best phase") rendezvous Δv, synodic periods |
| `propulsion.py` | energy and propellant per kg delivered by engine: electric thrusters, electrothermal on water, an energy-optimal mass driver on the C-type's baked residue |
| `flows.py` | what a child torus is made of by source, the rates a parent's lines sustain for a given generation, the cluster's growth until its C-type runs out |
| `__main__.py` | the report |

## Model

- **Water** (`habitat_model.mass`): soil moisture, lakes and streams (share of floor × mean depth, `lake_floor_frac` and `lake_depth_m`, a climate dial and a guess), the water electrolysed for the O₂, ballast (`ballast_frac` of the rim's mass: water spread as 1 − cos around the rim trims a first-harmonic imbalance e with e M in all), and the vegetation's water. Spin-up with water thrusters is an option, as before.
- **Supply routes:** the cargo always carries the N₂ and the organics. Shipping only the hydrogen needs ~0.89 kg of local oxygen per kg of water. Molten-oxide electrolysis (notes §10) frees ~0.29 kg of oxygen per kg of iron. The iron an LL host's free metal lacks is counted as free (it is reduced anyway, if the host electrolyses its silicates); any iron beyond it costs `moe_mj_kg_fe`. Splitting the water at the C-type costs `electrolysis_mj_kg_water`. Methane's carbon counts against the organics.
- **Transfers:** two impulses, prograde zero-revolution Lambert arcs between osculating two-body orbits, with the departure and arrival points and the flight time free: a coarse grid, then a pattern search from its best points. The elements are rounded from JPL's Small-Body Database, as recalled, not fetched. JPL's APIs are blocked from this environment, so there are no dated windows.
- **Propulsion:** the rocket equation per kg delivered; electricity ½ (e^(Δv/vₑ) − 1) vₑ² / η, lowest at vₑ = Δv / 1.594. The mass driver runs at that speed unless its reaction mass, the C-type's baked residue (the C-type less its water and carbon), runs short. Impulsive Δv throughout.
- **Flows:** a parent stack builds a child stack torus by torus, so a cluster doubles once per generation. The energy floor uses the system model's factory power per stack. The rates are given for set generations and compared with Earth benchmarks, orders of magnitude only: the largest open-pit mines move ~0.5 Mt a day, a large steelworks makes ~10 Mt a year.
- **Checks** (`tests/test_logistics.py`): Lambert along a circular orbit returns its velocity; the best phase between circular orbits is Hohmann (Δv and flight time); Earth–Eros synodic period; Ryugu → Eros reproduces the notes; the rocket equation, the energy-optimal exhaust and the propellant cap; the water budget adds up; the routes' hydrogen and iron; composition shares; rates and growth.

## Findings

- **Water per torus** ~0.12 / 0.38 / 0.96 Mt at 900 m / 1.6 km / 2.5 km, ~90% lakes and soil; the C-type sized by nitrogen holds ~2.7–7× that.
- **The notes' best-phase Δv reproduced** within ~0.1 km/s, Torifune 0.1–0.4 km/s lower. Ryugu → Eros windows recur every ~4.9 years.
- **Ship the hydrogen, not the water (proposed):** as methane, with the oxygen from the silicates, the cargo per 900 m torus falls from ~157 to ~61 kt and the water's energy from ~20 to ~10 PJ.
- **Mass-driver freighters (proposed):** at ~2.9 km/s on the C-type's baked residue, ~3.7× less electricity than electric thrusters at 30 km/s, and ~8× the thrust per watt; the lead holds down to ~13% efficiency.
- **Together** they halve the generation's energy floor at 1 GW per stack: ~1.9 → ~0.9 years for a 900 m pair, ~23 → ~13 years for a 1.6 km six-stack.
- **Rates:** at 10-year generations, ~9 kt of S-type and ~400 t of metal a day per 900 m torus, ~2% of Earth's largest mines and steelworks.
- **Made locally:** ~98.8% from the host, ~1.2% from the C-type, ~0.003% vitamins.
- **Ryugu's nitrogen** caps a 900 m cluster after ~55 years of doubling every 10 years, a 1.6 km one after ~14.
- **Not modelled:** factory throughput against its own mass, people and training, seed transfers to new sites, the freighters' own mass and power, failures and spares, dated windows and low-thrust trajectories.
