# Parametric system model

Section 1 of `plan.md`. It recomputes the design notes' numbers from one set of assumptions, checks them against the notes, and ranks the assumptions by how much they move the results.

Plain Python 3.11+ and numpy. Run it from the repository root:

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
| `--monte-carlo N` | triangular sampling over every range: 5th, 50th and 95th percentiles |
| `--assumptions-table` | the inputs with their ranges, status and sources |
| `--json FILE` | headline numbers for the 3D model's stats panel |
| `--write-reports DIR` | all of the above as files (see `reports/`) |

Tests: `python -m unittest discover -s tests`.

## Layout

| File | Contents | Notes sections |
|---|---|---|
| `assumptions.toml` | every input: value, unit, low/high, source, status (sourced / estimate / guess / design) | §19 and "Still unsourced" |
| `design.py` | design choices; candidate bodies; C-type → site Δv | §15 |
| `geometry.py` | 1 g family, floor, tube, hub, pitch and stack length, farm ring, end openings | §1, §2, §3a, §12, §13 |
| `mass.py` | air, rock shield with fill credit, fill, water, hull and frames (r^2.3), cable spokes, farm ring | §3c, §5c, §6, §7, §9 |
| `materials.py` | metal vs host class, S-type and C-type sizing, diameters, trace elements, tori supported per body | §7, §10, §15 |
| `food.py` | diet → mol of light per person → crop area, kW per person, people per tier | §13 |
| `power.py` | valley sky, other loads, farm tiers, despun array (survival and seasonal sizing), plain rim PV | §13, §15 |
| `heat.py` | heat per torus and stack, capacity of the end openings, break-even, radiator area | §13 |
| `stability.py` | inertia ratio of a rigid stack of rings, maximum tori for a margin | §11 |
| `replication.py` | crushing, baking, shipping energy from Δv, generation time | §5e, §13, §15 |
| `model.py` | chains the modules; the outputs ranked by the sensitivity sweep | |
| `validation.py` | ~200 figures from the notes, with the reason for each known mismatch | |
| `sensitivity.py`, `report.py`, `__main__.py` | tornado and Monte Carlo, Markdown and JSON, command line | |

All results are in SI units (m, kg, W, J) and converted only for display.

## Modelling choices to know

- **"1 g" is π² m/s²** (1.006 g), the notes' convention for the r = (T/2)² family.
- **Water.** The notes give the water need (~0.15 / 0.4 / 0.9 Mt) without a breakdown. The model adds soil moisture (25% of 0.5 m of soil), water electrolysed for the O₂, and lakes at 0.25 t per m² of floor (fitted at 1.6 km). On the rim it counts only the lakes: the soil's water is already in its moist density and the electrolysed water is in the air as O₂, which the notes' "water + air" column counts twice (~0.05 Mt at 900 m, negligible).
- **Hub, dock and factory metal** is 25% of the torus steel, matching the notes' 1.4 / 7.3 / 27 Mt.
- **Farm ring, array and radiators** are reported but kept out of the torus total, as in the notes: the farm ring isn't on the rim, so the spokes don't carry it.
- **Stability** treats the tori as thin rings at the floor radius, as §11 does; the hub and the array are left out.
- **Δv** comes from the notes' table (`asteroid_transfers.py` isn't in the repository); pass `--dv` for other pairs.
- **Processing energy** (the sensitivity output) is crushing plus baking; shipping is reported separately and added for the generation time, which counts energy only.

## Findings so far

See `reports/validation.md` and `reports/sensitivity.md`.

- 185 of 197 figures checked were within 5% at first; the others were rounding in the notes. The main one, the 900 m valley load quoted as ~60 MW where the same formulas give ~57 MW (52.6 MW of sky + 4.8 MW of other loads), is now corrected in the notes along with the 900 m arrays and heat break-even that follow from it: 191 of 197 now match. The 6 left are small roundings, and the water need at 900 m and 2.5 km, which doesn't scale with the floor in the notes for no stated reason.
- For a 900 m six-stack with two tiers lit on an L host at Eros, the inputs that move the outputs most are nitrogen recovery (C-type −22% to +40%), C-type baking energy, PV efficiency (array −11% to +39%), free metal in L rock (S-type mined −18% to +29%), and light on the crops (people −17% to +25%). The shield's areal density moves the mass per m² by ±18%. The wire's working stress moved the S-type by −12% to +33% over 700–1,200 MPa; with the range narrowed by the wire literature (800–1,200 MPa, `structure_model/README.md`) it is −12% to +19%.
- With the notes' Δv, shipping the volatiles from Ryugu to Eros takes ~2.5× the energy of crushing and baking (~21 PJ against ~8 PJ per 900 m torus).
