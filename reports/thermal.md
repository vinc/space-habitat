# Heat rejection, per section: ideal limit and preliminary radiative exchange

The **main section** (the tori) rejects the valleys' heat from radiators on the tori's spokes, in the drum between hub and tori; its ideal limit treats both end openings as black bodies at the radiator temperature. The **farm section** (one farm ring per torus, on its own spokes) rejects the farm tiers' heat from radiators on the farm spokes, in an open stack with nothing around it. Each is ray traced on its own (`habitat_model/cavity.py`: finite two-sided panels, emissivity and temperature from the assumptions, insulated hub and rings), then put together: the **coupling** is the share of each section's facing-end radiation that reaches the other across the gap, and the **whole-stack** margins count it as not rejected (conservative). Panel areas are one face of two-sided panels; the limits are the most tori (with their farm rings) each section can cool on its own, the main section through its ends only.

| Stack, tiers lit | Main heat (MW) | Main, ideal margin | Main margin, ends only | Main margin, ends + gaps | Main panels needed (ha) | Main limit (tori) | Farm heat (MW) | Farm margin | Farm panels needed (ha) | Farm limit (rings) | Coupling main→farm / farm→main | Whole-stack margins main / farm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m pair, 3 tiers | 115 | 14 | 11 | 11 | 17.4 | 28 | 192 | 8.0 | 29.6 | ≥ 40 | 24% / 84% | 9.4 / 5.0 |
| 900 m six, 1 tier | 344 | 4.8 | 3.9 | 4.2 | 58.6 | 28 | 192 | 11 | 30.0 | ≥ 40 | 29% / 84% | 3.3 / 7.7 |
| 900 m six, 2 tiers | 344 | 4.8 | 3.9 | 4.2 | 58.6 | 28 | 385 | 5.3 | 62.7 | ≥ 40 | 29% / 84% | 3.3 / 3.8 |
| 900 m six, 3 tiers | 344 | 4.8 | 3.9 | 4.2 | 58.6 | 28 | 577 | 3.6 | 100 | ≥ 40 | 29% / 84% | 3.3 / 2.6 |
| 1.6 km six, 2 tiers | 1,090 | 4.8 | 3.9 | 4.0 | 184 | 28 | 1,220 | 5.1 | 198 | ≥ 40 | 29% / 86% | 3.3 / 3.6 |
| 1.6 km six, 3 tiers | 1,090 | 4.8 | 3.9 | 4.0 | 184 | 28 | 1,820 | 3.4 | 318 | ≥ 40 | 29% / 86% | 3.3 / 2.4 |
