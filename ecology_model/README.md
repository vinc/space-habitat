# Closed atmosphere and ecology (plan §7)

A compartment model of one torus's air with its farm ring: O₂, CO₂, N₂ and carbon across the crops, the people, the soil and the valley's woodland. It covers failures, the startup of a new torus, leaks and a replay of Biosphere 2. It uses the system model (`habitat_model`) for the air, the people and the floor.

```bash
python -m ecology_model                          # full report (reports/atmosphere.md), ~6 s
python -m ecology_model --set soil_labile_frac=0.05
```

| File | Contents |
|---|---|
| `closed.py` | the configuration from the system model, the fluxes, the farm's quasi-steady CO₂, a torus in balance (`mature`) or new (`initial`), the integration with events and controls |
| `scenarios.py` | farm tiers dark, a soil burst, a new torus, leaks (choked flow), Biosphere 2's oxygen bookkeeping replayed, the same imbalance in a torus |
| `__main__.py` | the report |

## Model

- **Pools:** O₂, N₂ and CO₂ in the air (valleys and farm ring together), the food store, the soil's labile and stable organic carbon, the valley's standing vegetation.
- **The farm** fixes the carbon for its share of the diet (all but `valley_diet_share`, as the system model sizes it; the valley's gardens fix the rest under the sky) at its reference CO₂ (`farm_co2_pa`) with every tier lit, scaled by the tiers lit and by x / (x + K) of its CO₂. Its air is solved quasi-steady: uptake equals what the hub ducts bring (`duct_exchange_m3_s`), a quadratic in the farm's CO₂. The edible share (`harvest_index`) goes to the store at the photosynthetic quotient 1/RQ that people's respiration undoes; the residues go to the soil.
- **People** eat from the store, as much as it holds, and breathe O₂ at the food energy's cost (`kcal_per_l_o2`), CO₂ at `respiratory_quotient`; once it is empty they breathe out their body reserves (tracked).
- **The soil** decays its labile pool fast (part becomes humus) and its stable pool slowly, as CO₂, while O₂ lasts (one oxygen-limited flux for each, from the pool and into the air); a burst draws on the humus. The startup soil holds the imported organics (`organics_shipped_t_m2`); a mature one, what residues and litter keep up.
- **The valley's woodland** grows logistically towards its full biomass and sheds litter into the soil.
- **Controls:** a recovery plant turning CO₂ back into O₂ (Bosch or Sabatier with electrolysis, `o2_regen_mj_kg`) acts when CO₂ passes, or O₂ falls below, its targets, never converting more CO₂ than the air holds over a step; scrubbing removes CO₂ (Biosphere 2's concrete); the carbon both take out is tracked.
- **Integration:** explicit Euler, hourly (half-hourly at startup).
- **Checks** (`tests/test_ecology.py`): carbon conserved across every pool, also with the O₂, the food or the humus run out and the controls on; recovery bounded by the CO₂ there is; the farm and gardens splitting the diet; a mature torus holding steady; ~0.74 kg of O₂ a person a day; the farm's quasi-steady balance and its saturating response; darker farms failing sooner; choked flow against the textbook coefficient; Biosphere 2's replay landing on 14.2%; composted organics easing the startup.

## Findings

- **The air holds ~5 years of O₂** for a 900 m torus's ~3,050 people (~8 at 1.6 km).
- **Failures, 900 m:** one / two / all farm tiers dark reach the CO₂ limit (0.5 kPa) in ~110 / ~36 / ~22 days and the O₂ limit (17 kPa) in more than a year / ~330 / ~176 days; the 90-day food store runs out at ~170 / ~97 days with two or all tiers dark. A ~1 MW recovery plant holds the whole farm going dark. A soil burst is absorbed by the CO₂-fertilised crops.
- **A new torus:** the imported organics respire ~14× faster than the people breathe. CO₂ passes its limit in ~3 days and O₂ in ~25; recovery needs ~8 MW at first and ~12 kt of O₂ over ten years. Composting them first cuts that to ~1.4 MW; importing half to ~3.4 MW.
- **Biosphere 2:** its oxygen loss takes ~1.2 µmol/m²/s of excess soil respiration, with ~25 t of CO₂ into the concrete. The same in a torus shows as CO₂ within ~8 months.
- **Leaks:** 10% of a 900 m torus's air through a 10 cm hole in ~19 days, through a 1 m hole in ~5 hours.
- **Not modelled:** water and humidity, trace gases, the nitrogen cycle, the valley's daily swing, the algae, seasons, the controls' failures.
