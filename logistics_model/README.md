# Replication logistics (plan §5)

The water per torus by use and where it comes from, the transfers and propulsion that ship the C-type's products, and the flows of a generation. It uses the system model (`habitat_model`) for masses, materials and energies, and adds a Lambert solver for the transfers. Plain Python and numpy.

```bash
python -m logistics_model                         # full report (reports/logistics.md), ~2 min
python -m logistics_model.ephemeris --fetch       # refresh JPL Horizons' ephemerides and SBDB elements (network)
python -m logistics_model.catalogue --fetch       # refresh the C-type candidates and their Δv (network, ~10 min)
python -m logistics_model.networks --report       # saved host–supplier network study (offline)
python -m logistics_model --set lake_floor_frac=0.05
```

| File | Contents |
|---|---|
| `water.py` | the water budget by use (from the system model) and three ways to supply it: ship water, or ship only its hydrogen (as H₂ or methane) and take the oxygen from the silicates |
| `transfers.py` | orbital elements, a vectorised zero-revolution Lambert solver (universal variables), phase-free ("best phase") rendezvous Δv, synodic periods |
| `ephemeris.py` | JPL Horizons' state vectors (2027–2077, every 10 days) and the Small-Body Database's elements: fetched, stored in `data/`, interpolated (cubic Hermite) |
| `windows.py` | dated launch windows: the best flight for each departure date, its dips refined, how often usable ones recur |
| `catalogue.py` | C-type candidates from the Small-Body Database (C complex or dark), their phase-free Δv to the hosts, stored in `data/` |
| `networks.py`, `network_report.py` | compare silicate hosts with several suppliers, dated opportunities, sunlight and resource uncertainty; [study and reproduction commands](../reports/asteroid-networks.md), [evidence audit](../reports/asteroid-evidence.md) |
| `propulsion.py` | energy and propellant per kg delivered by engine: electric thrusters, electrothermal on water, an energy-optimal mass driver on the C-type's baked residue |
| `flows.py` | what a child torus is made of by source, the rates a parent's lines sustain for a given generation, the cluster's growth until its C-type runs out |
| `__main__.py` | the report |

## Model

- **Water** (`habitat_model.mass`): soil moisture, ponds and streams (share of floor × mean depth, `lake_floor_frac` and `lake_depth_m`: kept small, water access for the biosphere within the 1 m fill; a guess), the water electrolysed for the O₂, ballast (`ballast_frac`: an unbalanced mass e M at the rim, trimmed by water spread as A (1 − cos) around it; its first moment is only half its mass times the radius, so 2 e M of water), and the vegetation's water. Spin-up with water thrusters is an option, as before.
- **Supply routes:** the cargo always carries the N₂ and the organics. Shipping only the hydrogen needs ~0.89 kg of local oxygen per kg of water. Molten-oxide electrolysis (notes §10) frees ~0.29 kg of oxygen per kg of iron. The baseline host gets its metal as free metal and electrolyses nothing, so all that iron is charged: `moe_mj_kg_fe` of electricity and `moe_heat_mj_kg_fe` of furnace heat, less the crushing of the free-metal rock it replaces. `supply()` pairs every route with both freighters. Splitting the water at the C-type costs `electrolysis_mj_kg_water`. Methane's carbon counts against the organics.
- **Transfers:** two impulses, prograde zero-revolution Lambert arcs between osculating two-body orbits, with the departure and arrival points and the flight time free: a coarse grid, then a pattern search from its best points. The elements are JPL's Small-Body Database's (fetched; within rounding of the recalled ones used before). **Dated windows** on JPL Horizons' ephemerides (planets' perturbations included): departures every 5 days, flights of 60–900 days, one window per basin of the best-flight curve, refined by a pattern search within the span, then deduplicated (none within 120 days of a better one); a usable window lies within 1 km/s of the pair's best in 2028–2072. **Catalogue:** near-Earth asteroids classified in the C complex (H < 19.5) or dark in NEOWISE's albedos (< 0.08, ≥ 0.3 km), screened on a coarse grid and the best dozen per host refined; mass at Ryugu's bulk density.
- **Propulsion:** the rocket equation per kg delivered; electricity ½ (e^(Δv/vₑ) − 1) vₑ² / η, lowest at vₑ = Δv / 1.594. The mass driver runs at that speed unless its reaction mass, the C-type's baked residue (the C-type less its water and carbon), runs short. Impulsive Δv throughout.
- **Flows:** a parent stack builds a child stack torus by torus, so a cluster doubles once per generation. The energy floor uses the system model's factory power per stack. The rates are given for set generations and compared with Earth benchmarks, orders of magnitude only: the largest open-pit mines move ~0.5 Mt a day, a large steelworks makes ~10 Mt a year.
- **Checks** (`tests/test_logistics.py`): Lambert along a circular orbit returns its velocity; the best phase between circular orbits is Hohmann (Δv and flight time); Earth–Eros synodic period; Ryugu → Eros reproduces the notes; the ephemeris interpolation against the table and a two-body step, the calendar; dated windows above the phase-free bound and on the notes' 4.7 km/s, refined to a local minimum and kept within the span, one per basin and separated, the longest gap reported, a body's rendezvous with itself free; the catalogue's ranking, its screen above the refined value, a stored result reproduced; the rocket equation, the energy-optimal exhaust and the propellant cap; the water budget adds up; the ballast's first moment cancels the imbalance; the routes charge the oxygen's electrolysis, furnace heat and crushing saved; every route with both freighters; composition shares; rates and growth.

## Findings

- **Water per torus** ~0.066 / 0.22 / 0.56 Mt at 900 m / 1.6 km / 2.5 km, about 60% soil moisture and a fifth ballast; the C-type sized by nitrogen holds ~5–12× that.
- **The notes' best-phase Δv reproduced** within ~0.1 km/s; **dated, on Horizons' ephemerides**, the notes' values hold within ~0.1 km/s (Ryugu → Eros 4.66 km/s in 2031, best 4.52 in 2061); usable windows on average every ~2–7 years but clustered, with gaps of up to ~20 years (Ryugu → Eros, 2036–2056): ~60 kt of cargo per window on average per 900 m torus at 10-year generations, ~210 kt to stock through the longest gap.
- **Better C-type partners (proposed: spectra first):** 1999 XX262 for Eros (~3.6 km/s phase-free, ~4.0 dated, ~1.5 km, usable windows on average every ~2.3 years, longest gap ~16; −16% shipping for a 1.6 km six-stack), 2001 WT1 for Itokawa and Torifune (~3.9 / ~3.0 km/s dated, against Ryugu's 6.3 / 7.7). 1999 XX262 has B spectra and a tentative Ch feature in a reanalysis of the same 2014 spectrum, not independent hydration confirmation; its diameter has substantial thermal-model uncertainty. Neither candidate has a measured recoverable-nitrogen inventory. See the [evidence audit](../reports/asteroid-evidence.md).
- **Mass-driver freighters (proposed):** at ~2.9 km/s on the C-type's baked residue, ~3.7× less electricity than electric thrusters at 30 km/s, and ~8× the thrust per watt; the lead holds down to ~13% efficiency.
- **Ship water, not hydrogen:** shipping only the hydrogen (as methane, ~48 instead of ~106 kt per 900 m torus) needs the oxygen from the silicates; charged for the electrolysis and furnace heat (~6.4 PJ), it only just beats water by electric thrusters (~12.5 against ~13.5 PJ) and loses by mass driver (~8 against ~3.6 PJ). It pays only on a host that electrolyses its silicates for iron anyway. Methane stays useful as a storable fuel.
- **The generation's energy floor** at 1 GW per stack, water by mass driver: ~1.5 → ~0.9 years for a 900 m pair, ~19 → ~13 years for a 1.6 km six-stack.
- **Rates:** at 10-year generations, ~9 kt of S-type and ~400 t of metal a day per 900 m torus, ~2% of Earth's largest mines and steelworks.
- **Made locally:** ~99.2% from the host, ~0.8% from the C-type, ~0.0004% vitamins (computing, sensors, catalysts); the array's silicon is made at the host.
- **Ryugu's nitrogen** caps a 900 m cluster after ~55 years of doubling every 10 years, a 1.6 km one after ~14.
- **Not modelled:** factory throughput against its own mass, people and training, seed transfers to new sites, the freighters' own mass and power, failures and spares, low-thrust and multi-revolution trajectories, gravity assists.
