# Structure: wire, cable net and spin-up

## Wire

Working stress (MPa) by guaranteed strength class of bridge wire and safety factor:

| Safety factor | SF | 1570 MPa class | 1770 MPa class | 1960 MPa class |
|---|---|---|---|---|
| new bridge cables (commonly quoted, unverified) | 2.5 | 628 | 708 | 784 |
| long spans such as Akashi (commonly quoted, unverified) | 2.2 | 714 | 805 | 891 |
| NCHRP 534 action level for existing cables | 2.15 | 730 | 823 | 912 |
| static, well-known spin load (proposed here) | 2 | 785 | 885 | 980 |

The model's 1000 MPa needs a safety factor of 1.96 on the strongest bridge class. Thinner wire is stronger (Bekaert's high-strength threshold, a rough guide):

| Wire diameter | High-strength threshold (MPa) | At SF 2 (MPa) |
|---|---|---|
| 5 mm | 1,460 | 730 |
| 2 mm | 1,910 | 955 |
| 1 mm | 2,250 | 1,120 |
| 0.5 mm | 2,590 | 1,300 |
| 0.3 mm | 2,840 | 1,420 |

Long-term creep of a spoke at 1000 MPa on 1,960 MPa wire (relaxation r = 30 f/fu − 10% after 1,000 h, doubled for the long term, read as creep at constant load):

| Torus | Extra stretch over the spoke's length (m) |
|---|---|
| 400 m | 0.21 |
| 900 m | 0.48 |
| 1.6 km | 0.85 |
| 2.5 km | 1.3 |

## Tangent-chord net (chords tangent at 1.1 × the hub radius, one anchor every 10 m)

| Torus | Chord angle at the rim | Net, uniform chords (Mt) | System model spokes (Mt) | Chords vs radial spokes | Saved by tapering | Taper (mid / end area) | Tension per chord end (MN) | Wire area per chord end (cm²) | Bow at mid-chord (m) |
|---|---|---|---|---|---|---|---|---|---|
| 400 m | 4.3° | 0.0816 | 0.0816 | -0.01% | 0.5% | 1.02 | 50.8 | 508 | 0.46 |
| 900 m | 4.3° | 0.868 | 0.868 | -0.02% | 1.2% | 1.04 | 105 | 1,050 | 2.3 |
| 1.6 km | 4.3° | 4.87 | 4.88 | -0.04% | 2.2% | 1.06 | 180 | 1,800 | 7.4 |
| 2.5 km | 4.3° | 19.1 | 19.1 | -0.06% | 3.6% | 1.10 | 279 | 2,790 | 18 |

## Building the ring: opposite arcs in a partial net

Each arc's two end zones are single-laced and pull the arc lengthwise; the joints carry that tension until the ring closes. Values at full spin (they scale with spin²; at half spin, a quarter).

| Torus | Single-laced end zone (m) | Shortest arc (m) | Its rim mass (Mt) | Joint tension (MN) | vs a full ring's hoop force | Plate steel at 500 MPa (m²) | Joint tension at half spin (MN) |
|---|---|---|---|---|---|---|---|
| 400 m | 59.5 | 119 | 0.12 | 44.8 | 1.1% | 0.090 | 11.2 |
| 900 m | 134 | 268 | 0.56 | 208 | 1.1% | 0.42 | 51.9 |
| 1.6 km | 238 | 476 | 1.7 | 637 | 1.1% | 1.3 | 159 |
| 2.5 km | 372 | 743 | 4.2 | 1,540 | 1.1% | 3.1 | 385 |

## Imbalance: one arc 1% heavier than its partner

The stack spins freely about its centre of mass, so a mismatch moves the hub off the spin axis (it doesn't load a bearing). Hub, dock and factory taken as 25% of the torus steel. The gap between the hub and the chords' tangent circle (0.1 × the hub radius) must exceed the offset.

| Torus | Shortest arc (Mt) | Hub offset, first pair alone (m) | Gap hub to chords (m) | Hub offset, finished torus if never ballasted (cm) |
|---|---|---|---|---|
| 400 m | 0.12 | 1.8 | 2.70 | 18 |
| 900 m | 0.56 | 3.6 | 6.08 | 39 |
| 1.6 km | 1.7 | 5.6 | 10.8 | 64 |
| 2.5 km | 4.2 | 7.5 | 16.9 | 92 |

