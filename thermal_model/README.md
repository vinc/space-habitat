# Heat rejection (plan §6)

The farm radiators' layout and reach, how many tori the radiators can cool, sunlight on the radiators, the coolant loops and the valley's day/night swing. It builds on the assembled radiative exchange of `habitat_model/cavity.py` (the whole stack traced as one scene) and the system model's geometry and heat loads.

```bash
python -m thermal_model                          # full report (reports/heat_rejection.md), ~5 min
python -m thermal_model --set solar_absorptivity=0.3
```

| File | Contents |
|---|---|
| `layout.py` | farm radiators outboard (pumped) or inboard (passive), the least panel area for a margin, the reach needed, the most tori the stack can cool by tiers lit |
| `sunlight.py` | sun rays marched (sphere tracing) through the tori, hub and farm rings at a given axis tilt; sunlight the panels absorb against what they radiate |
| `coolant.py` | loops in spin gravity: natural circulation (main section), pumped (farm section, radiators outboard), two-phase boiling suppression under the liquid column |
| `valley.py` | the valley's steady-periodic day/night swing, by harmonics: air, plants and ponds as capacity, the soil as a semi-infinite conductor, cooling at U |
| `__main__.py` | the report |

## Model

- **Spin gravity sets the loops.** The potential per kg is −ω² r² / 2, so "up" is towards the hub. The valleys' heat rises from the rim to their radiators (0.4 r to the drum): natural circulation. The farm's heat, from the farm rings at 0.4 r to radiators outboard of them, would have to sink: pumped loops. `habitat_model/cavity.py` now takes a farm radiator layout (`outboard`, the default, or `inboard`, from the hub to the rings).
- **Panels:** the assembled stack's two panel coverages swept on a grid (5% steps), the least total area that keeps both sections at the target margin.
- **Sunlight:** rays parametrised by where they cross the plane through the axis normal to the Sun, marched on the signed distance to the tori (as true tori), the hub and the farm rings (boxes in r, z); the panel planes crossed before a solid intercept the coverage share of what is left; absorptivity `solar_absorptivity`.
- **Coolant:** single-phase water; natural circulation sized so friction (out and back) uses up the buoyancy head of a `coolant_dt_k`-warm leg; pumped loops at 2 m/s, the pump also against the opposing buoyancy. Two-phase: the returning liquid column's pressure at the rim against Clausius-Clapeyron.
- **Valley:** one surface node per m² of floor, a square wave of light by day, each harmonic Q_n / (U + i ω_n C + e √(i ω_n)), e the soil's effusivity. Three looks: arid canyon (dry soil, no ponds), baseline, fern gully.
- **Checks** (`tests/test_thermal.py`): loop sizing against its head, pump power, the boiling suppression and Clausius-Clapeyron's reference point; a capacity-only valley's triangle swing, a wet valley swinging less; edge-on panels seeing nothing, a lone plane's sunlight against α S sin δ A, the tori shading the drum at small tilts; the layouts and the least-area search.

## Findings

- **Farm radiators:** outboard (pumped) keeps ~2.4–2.5× in both sections of a six-stack with three tiers lit; inboard (passive) only ~0.5–0.7× in the farm section, about one tier (a pair's farm cools passively). Proposed: outboard, with an inboard passive fallback.
- **Reach:** ~0.6 r for 1×, ~0.75 r for 1.5× (six-stack, three tiers lit).
- **Capacity:** ~24 / 18 / 18 / 16 tori with 0 / 1 / 2 / 3 tiers lit, at 900 m and 1.6 km.
- **Panels at 1.5×:** ~36 ha (valley) + ~42 ha (farm) per 900 m torus in a six-stack, ~2–3× the black-body area.
- **Sunlight:** none on the drum's panels below ~1.5° of axis tilt; the open farm section ~1.3% of its heat per degree at 1 AU.
- **Loops:** passive water loops of ~0.45 m per 900 m torus (12 loops, ~0.7 m/s, ~1 kt of water); farm pumps ~0.2% of its heat; two-phase ammonia would need throttling at the rim (~1.9 MPa, boiling only above ~48 °C).
- **Valley swing:** ~2–4 K (wet) to ~4–10 K (dry) left to itself; wider swings need scheduled cooling.
- **Not modelled:** the spokes and cables, the envelopes' rounded inner faces, the radiators' tubes, freezing in cold panels at low load, reflected sunlight, the despun array's shadow, air movement in the valley.
