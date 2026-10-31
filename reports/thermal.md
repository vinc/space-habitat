# Heat rejection, per section and assembled: ideal limit and preliminary radiative exchange

The **main section** (the tori) rejects the valleys' heat from radiators on the tori's spokes, in the drum between hub and tori; its ideal limit treats both end openings as black bodies at the radiator temperature. The **farm section** (one farm ring per torus, on its own spokes) rejects the farm tiers' heat from radiators on the farm spokes, in an open stack with nothing around it. Each is first ray traced on its own (`habitat_model/cavity.py`: finite two-sided panels, emissivity and temperature from the assumptions, insulated hub and rings). Then the **whole stack** is traced as one scene: the drum, the gap and the farm section with its radiators; the tori bound it as insulated surfaces (the last torus's side facing the farm section, out to the envelopes' outer radius, and the envelopes' outer surface). The farm radiators shade the drum's farm end and the main radiators the farm section's near end, so the two panel coverages are swept together and the assembled margins are those of the best pair (the one with the best worse-of-the-two margin). Only the assembled check says whether a stack can be cooled; the **limit** is the most tori (with their farm rings) the assembled stack can cool, the drum through its ends only. Panel areas are one face of two-sided panels.

| Stack, tiers lit | Main heat (MW) | Main, ideal margin | Main alone, ends only | Main alone, ends + gaps | Main alone, panels needed (ha) | Farm heat (MW) | Farm alone | Farm alone, panels needed (ha) | Assembled margins main / farm | Assembled coverage main / farm | Assembled limit (tori) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m pair, 3 tiers | 57.7 | 28 | 22 | 22 | 8.67 | 74.8 | 21 | 11.3 | 12 / 13 | 100% / 100% | ≥ 40 |
| 900 m six, 1 tier | 173 | 9.5 | 8.1 | 8.6 | 27.5 | 74.8 | 28 | 11.5 | 6.7 / 6.8 | 100% / 10% | ≥ 40 |
| 900 m six, 2 tiers | 173 | 9.5 | 8.1 | 8.6 | 27.5 | 150 | 14 | 23.0 | 5.7 / 5.6 | 75% / 20% | ≥ 40 |
| 900 m six, 3 tiers | 173 | 9.5 | 8.1 | 8.6 | 27.5 | 225 | 9.3 | 35.4 | 5.2 / 5.0 | 100% / 35% | ≥ 40 |
| 1.6 km six, 2 tiers | 547 | 9.5 | 8.0 | 8.3 | 86.9 | 473 | 14 | 72.8 | 5.6 / 5.4 | 75% / 20% | ≥ 40 |
| 1.6 km six, 3 tiers | 547 | 9.5 | 8.0 | 8.3 | 86.9 | 710 | 9.1 | 112 | 5.0 / 4.9 | 75% / 35% | ≥ 40 |

# Farm radiators' reach: `farm_radiator_outer_frac` across its range

The farm radiators' outer radius (guess, 0.60–1.4 of the floor radius) sets the farm section's panel area and how much of the drum's farm end it shades. The one-at-a-time sweep and the Monte Carlo can't see it (they use `evaluate`, which ray traces nothing, and their heat metric is the main drum's ideal margin, which leaves the farm section out), so it is swept here with the farm section alone and the assembled stack.

| Stack, tiers lit | Reach (× floor radius) | Farm alone | Assembled farm margin | Assembled main margin | Assembled coverage main / farm | Cools both? |
|---|---|---|---|---|---|---|
| 900 m six, 2 tiers | 0.60 | 4.7 | 3.6 | 4.5 | 20% / 100% | yes |
| 900 m six, 2 tiers | 0.80 | 8.9 | 5.8 | 5.8 | 75% / 75% | yes |
| 900 m six, 2 tiers | 1.0 (default) | 14 | 5.5 | 5.8 | 50% / 20% | yes |
| 900 m six, 2 tiers | 1.2 | 20 | 5.7 | 5.7 | 35% / 10% | yes |
| 900 m six, 2 tiers | 1.4 | 27 | 8.3 | 6.3 | 50% / 10% | yes |
| 900 m six, 3 tiers | 0.60 | 3.1 | 2.6 | 2.8 | 10% / 100% | yes |
| 900 m six, 3 tiers | 0.80 | 5.9 | 4.2 | 5.0 | 35% / 100% | yes |
| 900 m six, 3 tiers | 1.0 (default) | 9.4 | 5.1 | 5.1 | 50% / 35% | yes |
| 900 m six, 3 tiers | 1.2 | 13 | 6.1 | 5.7 | 100% / 20% | yes |
| 900 m six, 3 tiers | 1.4 | 18 | 5.6 | 5.7 | 35% / 10% | yes |
