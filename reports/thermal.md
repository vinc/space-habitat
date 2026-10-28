# Heat rejection, per section and assembled: ideal limit and preliminary radiative exchange

The **main section** (the tori) rejects the valleys' heat from radiators on the tori's spokes, in the drum between hub and tori; its ideal limit treats both end openings as black bodies at the radiator temperature. The **farm section** (one farm ring per torus, on its own spokes) rejects the farm tiers' heat from radiators on the farm spokes, in an open stack with nothing around it. Each is first ray traced on its own (`habitat_model/cavity.py`: finite two-sided panels, emissivity and temperature from the assumptions, insulated hub and rings). Then the **whole stack** is traced as one scene: the drum, the gap and the farm section with its radiators, with the tori's outer side facing the farm section as an insulated face. The farm radiators shade the drum's farm end and the main radiators the farm section's near end, so the two panel coverages are swept together and the assembled margins are those of the best pair (the one with the best worse-of-the-two margin). Only the assembled check says whether a stack can be cooled; the **limit** is the most tori (with their farm rings) the assembled stack can cool, the drum through its ends only. Panel areas are one face of two-sided panels.

| Stack, tiers lit | Main heat (MW) | Main, ideal margin | Main alone, ends only | Main alone, ends + gaps | Main alone, panels needed (ha) | Farm heat (MW) | Farm alone | Farm alone, panels needed (ha) | Assembled margins main / farm | Assembled coverage main / farm | Assembled limit (tori) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m pair, 3 tiers | 115 | 14 | 11 | 11 | 17.4 | 192 | 8.1 | 29.5 | 5.8 / 5.3 | 75% / 100% | 17 |
| 900 m six, 1 tier | 344 | 4.8 | 4.1 | 4.3 | 58.0 | 192 | 11 | 30.0 | 2.9 / 4.3 | 100% / 20% | 18 |
| 900 m six, 2 tiers | 344 | 4.8 | 4.1 | 4.3 | 58.0 | 385 | 5.4 | 62.6 | 2.6 / 2.9 | 100% / 35% | 18 |
| 900 m six, 3 tiers | 344 | 4.8 | 4.1 | 4.3 | 58.0 | 577 | 3.6 | 100 | 2.4 / 2.5 | 100% / 75% | 17 |
| 1.6 km six, 2 tiers | 1,090 | 4.8 | 4.0 | 4.2 | 184 | 1,220 | 5.3 | 198 | 2.5 / 2.8 | 100% / 35% | 18 |
| 1.6 km six, 3 tiers | 1,090 | 4.8 | 4.0 | 4.2 | 184 | 1,820 | 3.5 | 318 | 2.3 / 2.4 | 100% / 75% | 16 |

# Farm radiators' reach: `farm_radiator_outer_frac` across its range

The farm radiators' outer radius (guess, 0.60–1.4 of the floor radius) sets the farm section's panel area and how much of the drum's farm end it shades. The one-at-a-time sweep and the Monte Carlo can't see it (they use `evaluate`, which ray traces nothing, and their heat metric is the main drum's ideal margin, which leaves the farm section out), so it is swept here with the farm section alone and the assembled stack.

| Stack, tiers lit | Reach (× floor radius) | Farm alone | Assembled farm margin | Assembled main margin | Assembled coverage main / farm | Cools both? |
|---|---|---|---|---|---|---|
| 900 m six, 2 tiers | 0.60 | 1.8 | 1.4 | 2.2 | 20% / 100% | yes |
| 900 m six, 2 tiers | 0.80 | 3.5 | 2.4 | 2.5 | 35% / 100% | yes |
| 900 m six, 2 tiers | 1.0 (default) | 5.5 | 2.9 | 2.6 | 75% / 35% | yes |
| 900 m six, 2 tiers | 1.2 | 7.8 | 3.3 | 2.8 | 75% / 20% | yes |
| 900 m six, 2 tiers | 1.4 | 11 | 3.0 | 3.3 | 75% / 10% | yes |
| 900 m six, 3 tiers | 0.60 | 1.2 | 1.0 | 1.4 | 10% / 100% | yes |
| 900 m six, 3 tiers | 0.80 | 2.3 | 1.8 | 1.9 | 20% / 100% | yes |
| 900 m six, 3 tiers | 1.0 (default) | 3.7 | 2.5 | 2.4 | 75% / 75% | yes |
| 900 m six, 3 tiers | 1.2 | 5.2 | 2.9 | 2.5 | 75% / 35% | yes |
| 900 m six, 3 tiers | 1.4 | 7.0 | 3.1 | 2.7 | 75% / 20% | yes |
