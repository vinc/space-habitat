# Heat rejection, per section and assembled: ideal limit and preliminary radiative exchange

The **main section** (the tori) rejects the valleys' heat from radiators on the tori's spokes, in the drum between hub and tori; its ideal limit treats both end openings as black bodies at the radiator temperature. The **farm section** (one farm ring per torus, on its own spokes) rejects the farm tiers' heat from radiators on the farm spokes, in an open stack with nothing around it. Each is first ray traced on its own (`habitat_model/cavity.py`: finite two-sided panels, emissivity and temperature from the assumptions, insulated hub and rings). Then the **whole stack** is traced as one scene: the drum, the gap and the farm section with its radiators; the tori bound it as insulated surfaces (the last torus's side facing the farm section, out to the envelopes' outer radius, and the envelopes' outer surface). The farm radiators shade the drum's farm end and the main radiators the farm section's near end, so the two panel coverages are swept together and the assembled margins are those of the best pair (the one with the best worse-of-the-two margin). Only the assembled check says whether a stack can be cooled; the **limit** is the most tori (with their farm rings) the assembled stack can cool, the drum through its ends only. Panel areas are one face of two-sided panels.

| Stack, tiers lit | Main heat (MW) | Main, ideal margin | Main alone, ends only | Main alone, ends + gaps | Main alone, panels needed (ha) | Farm heat (MW) | Farm alone | Farm alone, panels needed (ha) | Assembled margins main / farm | Assembled coverage main / farm | Assembled limit (tori) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m pair, 3 tiers | 52.9 | 31 | 24 | 24 | 7.93 | 67.0 | 23 | 10.1 | 14 / 14 | 100% / 75% | ≥ 40 |
| 900 m six, 1 tier | 159 | 10 | 8.8 | 9.4 | 25.0 | 67.0 | 31 | 10.3 | 7.3 / 7.6 | 100% / 10% | ≥ 40 |
| 900 m six, 2 tiers | 159 | 10 | 8.8 | 9.4 | 25.0 | 134 | 16 | 20.6 | 6.2 / 6.2 | 75% / 20% | ≥ 40 |
| 900 m six, 3 tiers | 159 | 10 | 8.8 | 9.4 | 25.0 | 201 | 10 | 31.4 | 5.7 / 5.6 | 100% / 35% | ≥ 40 |
| 1.6 km six, 2 tiers | 501 | 10 | 8.7 | 9.1 | 78.8 | 423 | 15 | 65.2 | 6.2 / 6.0 | 75% / 20% | ≥ 40 |
| 1.6 km six, 3 tiers | 501 | 10 | 8.7 | 9.1 | 78.8 | 635 | 10 | 99.5 | 5.5 / 5.5 | 75% / 35% | ≥ 40 |

# Farm radiators' reach: `farm_radiator_outer_frac` across its range

The farm radiators' outer radius (guess, 0.60–1.4 of the floor radius) sets the farm section's panel area and how much of the drum's farm end it shades. The one-at-a-time sweep and the Monte Carlo can't see it (they use `evaluate`, which ray traces nothing, and their heat metric is the main drum's ideal margin, which leaves the farm section out), so it is swept here with the farm section alone and the assembled stack.

| Stack, tiers lit | Reach (× floor radius) | Farm alone | Assembled farm margin | Assembled main margin | Assembled coverage main / farm | Cools both? |
|---|---|---|---|---|---|---|
| 900 m six, 2 tiers | 0.60 | 5.2 | 4.0 | 4.9 | 20% / 100% | yes |
| 900 m six, 2 tiers | 0.80 | 10.0 | 6.5 | 6.3 | 75% / 75% | yes |
| 900 m six, 2 tiers | 1.0 (default) | 16 | 6.2 | 6.3 | 50% / 20% | yes |
| 900 m six, 2 tiers | 1.2 | 22 | 6.3 | 6.3 | 35% / 10% | yes |
| 900 m six, 2 tiers | 1.4 | 30 | 9.3 | 6.9 | 50% / 10% | yes |
| 900 m six, 3 tiers | 0.60 | 3.5 | 2.9 | 3.1 | 10% / 100% | yes |
| 900 m six, 3 tiers | 0.80 | 6.6 | 4.7 | 5.5 | 35% / 100% | yes |
| 900 m six, 3 tiers | 1.0 (default) | 11 | 5.6 | 5.7 | 100% / 35% | yes |
| 900 m six, 3 tiers | 1.2 | 15 | 6.8 | 6.2 | 100% / 20% | yes |
| 900 m six, 3 tiers | 1.4 | 20 | 6.2 | 6.9 | 75% / 10% | yes |
