# Structure: wire, cable net, spin-up and the tube's cross-section

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

Uniform chords keep one area all along, sized at mid-chord where their own spin load adds most; tapered chords at uniform stress need only the end area at their ends.

| Torus | Chord angle at the rim | Net, uniform chords (Mt) | System model spokes (Mt) | Chords vs radial spokes | Saved by tapering | Taper (mid / end area) | Tension per chord end (MN) | Uniform chord area (cm²) | Tapered chord, end area (cm²) | Bow at mid-chord (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| 400 m | 4.3° | 0.0816 | 0.0816 | -0.01% | 0.5% | 1.02 | 50.8 | 516 | 508 | 0.46 |
| 900 m | 4.3° | 0.868 | 0.868 | -0.02% | 1.2% | 1.04 | 105 | 1,080 | 1,050 | 2.3 |
| 1.6 km | 4.3° | 4.87 | 4.88 | -0.04% | 2.2% | 1.06 | 180 | 1,920 | 1,800 | 7.4 |
| 2.5 km | 4.3° | 19.1 | 19.1 | -0.06% | 3.6% | 1.10 | 279 | 3,090 | 2,790 | 18 |

## Building the ring: assembled statics (provisional)

Each chord is one elastic member with a single tension; the rim is cut into rigid segments one tube width long, linked by joints that are *sliding* (shear only: free along the rim, as intended once the ring is closed), *pinned* (tension and shear) or *locked* (also bending). Chords are tension-only: the taut set is iterated both ways until it is exactly the set of stretched chords. Loads at full spin; cable stresses scale with spin². The chords are sized for the finished ring (uniform area).

A stage is **resolved** only if the taut set converges, every segment balances (residual: the worst force or moment imbalance relative to the segment's load) and, after removing the assembly's rigid motion, segment rotations stay below 0.05 rad and displacements below 1% of the radius at the spin rate reported. Otherwise it is left unresolved for a geometrically nonlinear analysis: a mechanism, or displacements too large for the linear geometry. Rotation / displacement are at full spin.

| Torus | Stage | Joints | Status | Chord tensions (MN) | Max chord vs finished | Peak cable stress (MPa) | Max spin fraction within 1 GPa | Max joint tension (MN, share of full hoop) | Max joint moment (GN·m) | Rotation / displacement | Residual |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m | finished ring | sliding | resolved | 99.7–109 | 1.0 | 1,040 | 0.98 | — | — | 0.021 rad / 6.4 m | 3e-09 |
| 900 m | finished ring | locked | resolved | 37.9–38.0 | 0.36 | 386 | 1.0 | 12,000 (63.8%) | 0.072 | 4.7e-07 rad / 1.6 m | 2e-11 |
| 1.6 km | finished ring | sliding | resolved | 179–181 | 1.0 | 1,000 | 1.00 | — | — | 0.0014 rad / 9.0 m | 1e-10 |
| 1.6 km | finished ring | locked | resolved | 90.7–91.0 | 0.50 | 535 | 1.0 | 28,600 (49.7%) | 0.11 | 6.1e-07 rad / 3.8 m | 1e-11 |
| 400 m | two arcs of 119 m (shortest) | locked | resolved | 99.8–100 | 2.0 | 1,960 | 0.72 | 34.6 (0.9%) | 2.2 | 3.9e-05 rad / 3.9 m | 7e-06 |
| 400 m | two arcs of 119 m (shortest) | pinned | **unresolved:** no equilibrium (mechanism) |  |  |  |  |  |  | — | 7e-02 |
| 900 m | two arcs of 268 m (shortest) | locked | resolved | 213–214 | 2.0 | 2,010 | 0.71 | 176 (0.9%) | 6.0 | 2.3e-05 rad / 8.9 m | 8e-06 |
| 900 m | two arcs of 268 m (shortest) | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 0.52 rad / 27 m | 8e-06 |
| 1.6 km | two arcs of 476 m (shortest) | locked | resolved | 355–356 | 2.0 | 1,910 | 0.72 | 546 (0.9%) | 26 | 3.1e-05 rad / 15 m | 8e-06 |
| 1.6 km | two arcs of 476 m (shortest) | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 1.2 rad / 78 m | 8e-06 |
| 2.5 km | two arcs of 743 m (shortest) | locked | resolved | 556–557 | 2.0 | 1,900 | 0.72 | 1,400 (1.0%) | 59 | 2.9e-05 rad / 23 m | 1e-05 |
| 2.5 km | two arcs of 743 m (shortest) | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 0.53 rad / 80 m | 8e-06 |
| 900 m | two arcs of 401 m | locked | resolved | 153–155 | 1.5 | 1,460 | 0.83 | 234 (1.2%) | 68 | 0.0003 rad / 6.4 m | 1e-05 |
| 900 m | two arcs of 401 m | pinned | **unresolved:** no equilibrium (mechanism) |  |  |  |  |  |  | — | 2e-01 |
| 900 m | two arcs of 803 m | locked | resolved | 122–125 | 1.2 | 1,190 | 0.92 | 373 (2.0%) | 220 | 0.0023 rad / 5.6 m | 1e-05 |
| 900 m | two arcs of 803 m | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 1.9 rad / 74 m | 1e-05 |

Rigid segments make this a crude model: even resolved stages settle the force balance, not the construction sequence, and the joint moments of the longer locked arcs depend on the segments' real flexibility.

## Imbalance: one arc 1% heavier than its partner

The stack spins freely about its centre of mass, so a mismatch moves the spin axis away from the assembly's geometric centre: an estimate of that offset only. The hub and the net move together, so this is not a loss of clearance between them; their relative motion needs the stabilising lines' stiffness (still open). Hub, dock and factory taken as 25% of the torus steel.

| Torus | Shortest arc (Mt) | Axis offset, first pair alone (m) | Axis offset, finished torus if never ballasted (cm) |
|---|---|---|---|
| 400 m | 0.12 | 1.8 | 18 |
| 900 m | 0.56 | 3.6 | 39 |
| 1.6 km | 1.7 | 5.6 | 64 |
| 2.5 km | 4.2 | 7.5 | 92 |

## Tube cross-section: hull and frames by finite elements

One metre of tube in the plane of its cross-section (`structure_model/tube_section.py`): the pressure hull and the outer cell wall as membrane skins, the jacket's transverse bulkheads (one every 10 m) smeared into a plane-stress annulus between them, the rock, fill, lakes, air, bumper and steel under spin gravity, 70 kPa on the hull, and the chords' anchors on the outer wall holding the section along the radius. Every part is sized fully stressed at 300 MPa (von Mises; half that in compression, an allowance for stiffeners), or held at its minimum gauge (1 cm for the skins, 5 mm for bulkheads and cell walls). The skins also carry the hull's lengthwise pressure load and the pillowing of their panels between bulkheads; the hub-facing hull panels pressed in by the rock get stiffeners (vaulted ceiling), or the rock rests on hung cell floors instead (hung). Panels, cell walls and bumper are together in one column.

### Chords anchored at the tube's two sides (one net in each side plane), vaulted ceiling

| Torus | Load (MN per m of tube) | Hull (Mt) | Outer wall (Mt) | Bulkheads (Mt) | Panels, cell walls, bumper (Mt) | Hull and frames (Mt) | System model, r^2.3 (Mt) | Difference | Steel per torus (with spokes) vs model |
|---|---|---|---|---|---|---|---|---|---|
| 400 m | 10.1 | 0.015 | 0.022 | 0.0081 | 0.011 | **0.056** | 0.046 | +20% | +7% |
| 900 m | 20.8 | 0.080 | 0.093 | 0.057 | 0.045 | **0.28** | 0.30 | -8% | -2% |
| 1.6 km | 36.0 | 0.42 | 0.32 | 0.30 | 0.14 | **1.2** | 1.1 | +4% | +1% |
| 2.5 km | 56.5 | 2.1 | 1.2 | 0.99 | 0.32 | **4.6** | 3.1 | +47% | +7% |

### Where the chords anchor

Anchors on the hub-facing crest (one net in the torus's mid-plane), at the two sides, or spread over the hub-facing half (anchors that would push are released; the rest share the load). Anchor loads per metre of tube; compression is the largest compressive force in a skin; displacement includes the section's ovalisation.

| Torus | Anchors | Ceiling | Steel (t per m of tube) | Per torus (Mt) | Anchor loads (MN/m) | Max skin compression (MN/m) | Max displacement (m) |
|---|---|---|---|---|---|---|---|
| 900 m | crest | vaulted | 159 | 0.87 | 180°: 21.8 | 33 | 0.44 |
| 900 m | crest | hung | 164 | 0.90 | 180°: 21.8 | 33 | 0.44 |
| 900 m | sides | vaulted | 50.3 | 0.28 | 90°: 10.4, 270°: 10.4 | 2.9 | 0.10 |
| 900 m | sides | hung | 53.1 | 0.29 | 90°: 10.4, 270°: 10.4 | 3.4 | 0.11 |
| 900 m | fan | vaulted | 49.6 | 0.27 | 90°: 9.16, 120°: 0.891, 150°: 0.110, 180°: 0.431, 210°: 0.110, 240°: 0.891, 270°: 9.16 | 3.3 | 0.12 |
| 900 m | fan | hung | 52.7 | 0.29 | 90°: 9.33, 120°: 0.826, 150°: 0.0634, 180°: 0.355, 210°: 0.0634, 240°: 0.826, 270°: 9.33 | 3.4 | 0.13 |
| 1.6 km | crest | vaulted | 766 | 7.5 | 180°: 42.1 | 110 | 1.1 |
| 1.6 km | crest | hung | 776 | 7.6 | 180°: 42.2 | 110 | 1.1 |
| 1.6 km | sides | vaulted | 120 | 1.2 | 90°: 18.0, 270°: 18.0 | 5.8 | 0.25 |
| 1.6 km | sides | hung | 125 | 1.2 | 90°: 18.0, 270°: 18.0 | 6.7 | 0.27 |
| 1.6 km | fan | vaulted | 117 | 1.1 | 90°: 17.6, 180°: 0.704, 270°: 17.6 | 7.1 | 0.31 |
| 1.6 km | fan | hung | 123 | 1.2 | 90°: 17.7, 180°: 0.550, 270°: 17.7 | 7.4 | 0.32 |
| 2.5 km | crest | vaulted | 3,170 | 48 | 180°: 83.5 | 320 | 2.5 |
| 2.5 km | sides | vaulted | 305 | 4.6 | 90°: 28.2, 270°: 28.2 | 10 | 0.68 |
| 2.5 km | fan | vaulted | 297 | 4.5 | 90°: 27.5, 180°: 1.32, 270°: 27.5 | 14 | 0.84 |

### Sensitivity at 900 m (sides, vaulted)

| Change | Hull and frames (Mt) | vs base |
|---|---|---|
| `plate_stress_mpa` = 200 | 0.337 | +22% |
| `plate_stress_mpa` = 500 | 0.247 | -10% |
| `skin_min_gauge_m` = 0.005 | 0.228 | -17% |
| `skin_min_gauge_m` = 0.02 | 0.431 | +57% |
| `cell_wall_min_gauge_m` = 0.01 | 0.310 | +12% |
| `bumper_m` = 0.003 | 0.285 | +3% |

Not modelled: buckling of the parts in compression (sized with an allowance only), segment joints and seals, the anchors' local details, and the valley's buildings, light box and ceiling.

