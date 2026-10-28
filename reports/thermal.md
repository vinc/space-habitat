# Heat rejection: ideal limit and preliminary radiative exchange

The ideal limit treats both end openings as black bodies at the radiator temperature. The radiative exchange model (`habitat_model/cavity.py`) traces rays from finite panels (emissivity and temperature from the assumptions) through the drum between hub and tori, with the hub, farm rings and the tori's inner faces insulated, and escape through the ends only or also through the side gaps. Panel areas are one face of two-sided panels.

| Stack, tiers lit | Heat (MW) | Ideal limit (GW) | Ideal margin | Drum maximum, ends only (GW) | Margin, ends only | Margin, ends + gaps | Panels, ideal (ha) | Panels needed, ends only (ha) | Max tori by heat, ends only |
|---|---|---|---|---|---|---|---|---|---|
| 900 m pair, 3 tiers | 307 | 1.6 | 5.3 | 1.2 | 3.8 | 3.9 | 45.6 | 49.5 | 8 |
| 900 m six, 1 tier | 537 | 1.6 | 3.1 | 1.2 | 2.3 | 2.5 | 79.7 | 101 | 15 |
| 900 m six, 2 tiers | 729 | 1.6 | 2.2 | 1.2 | 1.7 | 1.8 | 108 | 165 | 11 |
| 900 m six, 3 tiers | 922 | 1.6 | 1.8 | 1.2 | 1.3 | 1.4 | 137 | 248 | 8 |
| 1.6 km six, 2 tiers | 2,300 | 5.2 | 2.3 | 3.9 | 1.7 | 1.7 | 342 | 511 | 11 |
| 1.6 km six, 3 tiers | 2,910 | 5.2 | 1.8 | 3.9 | 1.3 | 1.4 | 433 | 743 | 8 |
