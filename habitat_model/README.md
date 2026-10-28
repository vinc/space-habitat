# Parametric system model

Section 1 of `plan.md`. It recomputes the design notes' numbers from one set of assumptions, checks them against the notes, and ranks the assumptions by how much they move the results.

Plain Python 3.11+ and numpy 2.0+ (`pip install -r requirements.txt`). Run it from the repository root:

```bash
python -m habitat_model --size 900 --stack six --tiers 2 --host L --site Eros
```

| Option | Meaning |
|---|---|
| `--size 900`, `--size 1.6km`, or `--period 80` | floor radius, or rotation period of the 1 g family r = (T/2)² |
| `--stack pair`, `six`, or a number | tori in the co-rotating stack |
| `--tiers 0`–`3` | farm tiers lit |
| `--host H`, `L` or `LL` | ordinary-chondrite class of the S-type host |
| `--site` | orbit for the solar sizing: `1 AU`, `Itokawa`, `Apophis`, `Apophis 2029`, `Eros`, `Didymos`, `Torifune` |
| `--partner Ryugu` or `Bennu` | C-type supplying the volatiles |
| `--gap`, `--g`, `--water-spinup`, `--constant-sky`, `--factory-power`, `--dv` | other design choices |
| `--set name=value` | override one assumption (repeatable) |

Outputs, instead of the default design summary:

| Option | Output |
|---|---|
| `--key-tables` | the notes' §0 tables, regenerated |
| `--validate` | every checked figure of the notes, with the model's value and the difference |
| `--sensitivity` | one-at-a-time sweep of every input over its range, ranked (tornado) |
| `--ranking` | each input's largest effect over representative designs (sizes, host classes, sites) |
| `--monte-carlo N` | independent triangular sampling over every range: 5th, 50th and 95th percentiles (conditional on the ranges, not physical confidence bounds) |
| `--thermal` | ideal heat limit against the preliminary radiative exchange model, by stack, each section alone and assembled; the farm radiators' reach swept |
| `--trace` | trace-element budget: contained, recoverable, demand, surplus |
| `--assumptions-table` | the inputs with their ranges, status and sources |
| `--json FILE` | headline numbers for the 3D model's stats panel |
| `--write-reports DIR` | all of the above as files (see `reports/`) |

Tests: `python -m unittest discover -s tests`. GitHub Actions (`.github/workflows/ci.yml`) runs them, with command-line smoke tests, on Python 3.11 and 3.13 for every pull request and push to `main`.

## Layout

| File | Contents | Notes sections |
|---|---|---|
| `assumptions.toml` | every input: value, unit, low/high, source, status (sourced / estimate / guess / design) | §19 and "Still unsourced" |
| `design.py` | design choices; candidate bodies; C-type → site Δv | §15 |
| `geometry.py` | 1 g family, floor, tube, rock jacket and envelope, hub, pitch and stack length, farm ring, end openings | §1, §2, §3a, §12, §13 |
| `mass.py` | air, finite-thickness rock jacket with the fill's shielding credit, fill, water, hull and frames (r^2.3), cable spokes, farm ring | §3c, §5c, §6, §7, §9 |
| `materials.py` | metal vs host class, S-type and C-type sizing, diameters, trace-element budget, tori supported per body | §7, §10, §15 |
| `food.py` | diet → mol of light per person → crop area, kW per person, people per tier | §13 |
| `power.py` | valley sky, other loads, farm tiers, despun array (survival and seasonal sizing), plain rim PV | §13, §15 |
| `heat.py` | heat per torus and stack, ideal limit of the end openings, break-even, ideal radiator area | §13 |
| `cavity.py` | preliminary radiative exchange per section (Monte Carlo ray tracing): the tori's drum and the open farm section, then the whole stack as one scene; panels needed, stack limits, the farm radiators' reach | §13 |
| `stability.py` | inertia ratio of a rigid stack of rings, maximum tori for a margin | §11 |
| `replication.py` | crushing, baking, shipping energy from Δv (unknown when the Δv is), generation time | §5e, §13, §15 |
| `model.py` | chains the modules; the outputs ranked by the sensitivity sweep | |
| `validation.py` | ~200 figures from the notes, with the reason for each known mismatch | |
| `sensitivity.py`, `report.py`, `__main__.py` | tornado and Monte Carlo, Markdown and JSON, command line | |

All results are in SI units (m, kg, W, J) and converted only for display.

## Modelling choices to know

- **"1 g" is π² m/s²** (1.006 g), the notes' convention for the r = (T/2)² family.
- **Boundaries.** The pressurised tube has radius a = w/2 (the valley, with its fill inside). Outside it: the rock jacket, t = areal density / rock density (~5.5 m), then the empty crawl space (~1.5 m) and the thin bumper. The envelope is everything out to the bumper; the gap is clear space between neighbouring envelopes, so pitch = 2 × envelope + gap. The drum's end openings run from the hub to the envelopes' inner edge. A negative gap, or an envelope reaching the hub, is an error.
- **Shield.** The jacket's volume is that of its finite annulus, 2π² R [(a + t)² − a²] ρ, ~10% more than the thin-shell estimate at 900 m (~22% at 400 m). Under the floor's footprint the jacket is thinned, on its outer face, by the fill's rock-equivalent: regolith counts 1:1, the soil's solids 1:1 and its water at the rock/water shielding equivalence, so ~0.9 m of rock for 1 m of fill. No fill, no credit; the thinning never exceeds the jacket.
- **Water.** The notes give the water need (~0.15 / 0.4 / 0.9 Mt) without a breakdown. The model adds soil moisture (25% of 0.5 m of soil), water electrolysed for the O₂, and lakes at 0.25 t per m² of floor (fitted at 1.6 km; a guess, and now second in the combined ranking because water is most of what is shipped). On the rim it counts only the lakes: the soil's water is already in its moist density and the electrolysed water is in the air as O₂, which the notes' "water + air" column counts twice (~0.05 Mt at 900 m, negligible).
- **Hub, dock and factory metal** is 25% of the torus steel, matching the notes' 1.4 / 7.3 / 27 Mt.
- **Farm ring, array and radiators** are reported but kept out of the torus total, as in the notes: the farm ring isn't on the rim, so the spokes don't carry it.
- **Stability** treats the tori as thin rings at the floor radius, as §11 does; the hub and the array are left out.
- **Δv** comes from the notes' table (`asteroid_transfers.py` isn't in the repository); pass `--dv` for other pairs. **An unknown Δv stays unknown:** shipping, the energy totals and the generation time are then `unknown` (`null` in JSON), and a processing-only lower bound is given; `--dv 0` means a known zero.
- **Energy outputs** in the sensitivity sweep: processing (crushing plus baking), shipping, their total, and the energy-limited generation time; outputs unknown for a design are left out of its sweep.
- **Two sections (proposed, 28 Oct 2026).** The stack is the main section (the tori) and a farm section (one farm ring per torus, ~10 m apart, ~50 m beyond the tori) on the same hub. Each farm ring has its own spokes (sized like the tori's, at the farm's rim speed) and its own atmosphere (`farm_pressure_kpa`, 70 kPa by default), whose N₂ sizes the C-type with the valleys'. The sections are modelled separately; stack length and stability add them up.
- **Heat.** `heat.py` splits the heat by section: the valleys' through the tori's drum, the farm tiers' through the farm section. It gives the drum's ideal limit (its two end openings as black bodies at the radiator temperature) and the ideal (black-body) panel area. `cavity.py` traces rays from finite two-sided panels (emissivity from the assumptions) in each section on its own: the drum, with insulated hub and envelopes; the open farm section, with insulated hub and farm rings and radiators out to `farm_radiator_outer_frac`. `assembled_scene` then traces the whole stack as one scene (the farm radiators shade the drum's farm end, the tori's outer side faces the farm section) and sweeps both sections' coverages together; only this assembled check says whether a stack can be cooled. `farm_sweep` runs it across the farm radiators' reach, which the sensitivity sweep can't see. It leaves out sunlight through the gaps, the spokes and cables, and the envelopes' rounded faces.
- **Trace elements.** The budget compares contained inventory, recoverable supply (an assumed recovery) and demand. Most demands and recoveries are guesses taken from the notes; Cr, Sn, Mo and Zn are marked unbudgeted.

## Findings so far

See `reports/validation.md`, `reports/sensitivity.md` and `reports/thermal.md`.

- **Reproducing the notes:** 189 of 197 figures within 5%, 192 within their configured tolerance (10–15% for 12 counts and energies the notes quote as ranges); 5 known mismatches, all small roundings or the water need, which the notes give without a breakdown. This checks that the model and the notes agree, not that the design is physically sound.
- **Corrections to the notes so far:** the 900 m valley load (~57 MW, not ~60) and what follows from it; then, after the review in GitHub issue #1, the jacket's finite thickness and envelope: a 900 m torus is ~12.8 Mt (~40 t per m² of floor) instead of ~11.9 Mt, the pitch is ~80 m instead of ~66 m, the passive stability limit is ~22 tori instead of ~27, and a six-stack is ~480 m long.
- **Heat, per section:** the tori's drum rejects up to ~84% of its ideal limit. With the farm in its own section, a 900 m six-stack with three tiers lit keeps ~3.9× margin in the drum and ~3.6× in the farm section on their own, ~2.4× and ~2.5× traced together (it was ~1.3× with the farm rings in the tori's planes). Traced together, the stack cools ~16–18 tori of 900 m, just below stability (~22); with the farm radiators at 0.6 r, three tiers lit leave no margin.
- **Combined ranking** over five representative designs: the electric propulsion's exhaust speed and the lake water (which sets most of the water shipped) lead, both through the shipping energy; then nitrogen recovery, baking energy, PV efficiency, free metal in L and LL rock, the shield's areal density and light on the crops.
- With the notes' Δv, shipping the volatiles from Ryugu to Eros takes ~2.5× the energy of crushing and baking (~21 PJ against ~8 PJ per 900 m torus).
