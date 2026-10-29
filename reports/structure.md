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
| 400 m | 4.3° | 0.0815 | 0.0816 | -0.01% | 0.5% | 1.02 | 50.7 | 515 | 507 | 0.46 |
| 900 m | 4.3° | 0.868 | 0.868 | -0.02% | 1.2% | 1.04 | 105 | 1,080 | 1,050 | 2.3 |
| 1.6 km | 4.3° | 4.87 | 4.87 | -0.04% | 2.2% | 1.06 | 180 | 1,920 | 1,800 | 7.4 |
| 2.5 km | 4.3° | 19.1 | 19.1 | -0.06% | 3.6% | 1.10 | 279 | 3,090 | 2,790 | 18 |

## Building the ring: assembled statics (provisional)

Each chord is one elastic member with a single tension; the rim is cut into rigid segments one tube width long, linked by joints that are *sliding* (shear only: free along the rim, as intended once the ring is closed), *pinned* (tension and shear) or *locked* (also bending). Chords are tension-only: the taut set is iterated both ways until it is exactly the set of stretched chords. Loads at full spin; cable stresses scale with spin². The chords are sized for the finished ring (uniform area).

A stage is **resolved** only if the taut set converges, every segment balances (residual: the worst force or moment imbalance relative to the segment's load) and, after removing the assembly's rigid motion, segment rotations stay below 0.05 rad and displacements below 1% of the radius at the spin rate reported. Otherwise it is left unresolved for a geometrically nonlinear analysis: a mechanism, or displacements too large for the linear geometry. Rotation / displacement are at full spin.

| Torus | Stage | Joints | Status | Chord tensions (MN) | Max chord vs finished | Peak cable stress (MPa) | Max spin fraction within 1 GPa | Max joint tension (MN, share of full hoop) | Max joint moment (GN·m) | Rotation / displacement | Residual |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m | finished ring | sliding | resolved | 99.6–109 | 1.0 | 1,040 | 0.98 | — | — | 0.021 rad / 6.4 m | 3e-09 |
| 900 m | finished ring | locked | resolved | 37.9–38.0 | 0.36 | 386 | 1.0 | 12,000 (63.8%) | 0.072 | 4.7e-07 rad / 1.6 m | 2e-11 |
| 1.6 km | finished ring | sliding | resolved | 179–181 | 1.0 | 1,000 | 1.00 | — | — | 0.0014 rad / 9.0 m | 1e-10 |
| 1.6 km | finished ring | locked | resolved | 90.6–90.9 | 0.50 | 535 | 1.0 | 28,600 (49.7%) | 0.11 | 6.1e-07 rad / 3.8 m | 1e-11 |
| 400 m | two arcs of 119 m (shortest) | locked | resolved | 99.7–100.0 | 2.0 | 1,960 | 0.72 | 34.6 (0.9%) | 2.2 | 3.9e-05 rad / 3.9 m | 7e-06 |
| 400 m | two arcs of 119 m (shortest) | pinned | **unresolved:** no equilibrium (mechanism) |  |  |  |  |  |  | — | 7e-02 |
| 900 m | two arcs of 268 m (shortest) | locked | resolved | 213–214 | 2.0 | 2,010 | 0.71 | 176 (0.9%) | 6.0 | 2.3e-05 rad / 8.9 m | 8e-06 |
| 900 m | two arcs of 268 m (shortest) | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 0.52 rad / 27 m | 8e-06 |
| 1.6 km | two arcs of 476 m (shortest) | locked | resolved | 355–356 | 2.0 | 1,910 | 0.72 | 545 (0.9%) | 26 | 3.2e-05 rad / 15 m | 8e-06 |
| 1.6 km | two arcs of 476 m (shortest) | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 1.2 rad / 78 m | 8e-06 |
| 2.5 km | two arcs of 743 m (shortest) | locked | resolved | 556–557 | 2.0 | 1,900 | 0.72 | 1,400 (1.0%) | 59 | 2.9e-05 rad / 23 m | 1e-05 |
| 2.5 km | two arcs of 743 m (shortest) | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 0.53 rad / 80 m | 9e-06 |
| 900 m | two arcs of 401 m | locked | resolved | 153–155 | 1.5 | 1,460 | 0.83 | 234 (1.2%) | 68 | 0.0003 rad / 6.4 m | 1e-05 |
| 900 m | two arcs of 401 m | pinned | **unresolved:** no equilibrium (mechanism) |  |  |  |  |  |  | — | 2e-01 |
| 900 m | two arcs of 803 m | locked | resolved | 122–125 | 1.2 | 1,190 | 0.92 | 373 (2.0%) | 220 | 0.0023 rad / 5.6 m | 1e-05 |
| 900 m | two arcs of 803 m | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 1.9 rad / 74 m | 2e-05 |

Rigid segments make this a crude model: even resolved stages settle the force balance, not the construction sequence, and the joint moments of the longer locked arcs depend on the segments' real flexibility.

## Imbalance: one arc 1% heavier than its partner

The stack spins freely about its centre of mass, so a mismatch moves the spin axis away from the assembly's geometric centre: an estimate of that offset only. The hub and the net move together, so this is not a loss of clearance between them; their relative motion needs the stabilising lines' stiffness (still open). Hub, dock and factory taken as 25% of the torus steel.

| Torus | Shortest arc (Mt) | Axis offset, first pair alone (m) | Axis offset, finished torus if never ballasted (cm) |
|---|---|---|---|
| 400 m | 0.12 | 1.8 | 18 |
| 900 m | 0.56 | 3.6 | 39 |
| 1.6 km | 1.7 | 5.6 | 64 |
| 2.5 km | 4.2 | 7.5 | 92 |

## The hub in the nets: stabilising lines

Each torus has two chord nets, one in each side plane of its tube. In each, the chords pass the hub tangent to a circle 1.1 × its radius, bowed outward by their spin load, leaving a window gap around it. A short line runs from the hub to every chord's tangent point (`structure_model/hub.py`). A chord pulled sideways at its middle resists like a taut string, 2T/L, a little less under its own spin load (shown in brackets); lines and chords act in series, and N lines spread around the window give N k / 2 in any direction of a net's plane, twice that for the torus's two nets. The hub's share is the system model's hub, dock and factory metal (25% of the torus steel). The torus and its hub move relative to each other with their reduced mass μ; off the axis they are pulled apart by μω²x, so the margin is K / μω². In the rotating frame Coriolis couples the two directions of the window's plane: the relative motion has two modes, at |√(K/μ) ∓ ω| (√(K/μ) seen from outside). Lines are preloaded 1.5× their largest swing of tension, in service and while building, and the area, preload, stiffness and loads are iterated until they agree, every line taut and within the wire stress.

### Finished torus

| Torus | Hub share (Mt) | Window gap (m) | Lines | Chord stiffness (kN/m) | Lateral stiffness (MN/m) | Margin K / μω² | Natural frequency / spin: inertial; rotating modes | Tilt stiffness (GN·m/rad) | Axial stiffness (MN/m): radial lines / 10% inclined | Axial natural frequency / spin | Torsional stiffness (GN·m/rad) | Line area (mm²) | Service preload (kN) | Lines' mass (t), + inclined option |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 400 m | 0.032 | 3.2 | 502 | 128 (-1%) | 30.6 | 39 | 6.3; 5.3 and 7.3 | 9.92 | 0.21 / 4.86 | 0.51 / 2.5 | 0.17 | 41.5 | 1.3 | 0.52 (+0.25) |
| 900 m | 0.29 | 8.4 | 1,130 | 118 (-2%) | 64.7 | 21 | 4.5; 3.5 and 5.5 | 73.1 | 0.71 / 11.2 | 0.48 / 1.9 | 3.0 | 170 | 5.3 | 13 (+4.0) |
| 1.6 km | 1.5 | 18 | 2,010 | 115 (-4%) | 114 | 13 | 3.6; 2.6 and 4.6 | 350 | 1.7 / 19.6 | 0.44 / 1.5 | 24 | 500 | 16 | 140 (+32) |
| 2.5 km | 5.6 | 35 | 3,142 | 116 (-7%) | 179 | 8.6 | 2.9; 1.9 and 3.9 | 1,250 | 3.4 / 29.7 | 0.41 / 1.3 | 120 | 1,240 | 38 | 1,100 (+170) |

Radial lines hold the hub along the axis only through their preload: its axial natural frequency is below the spin rate. Running 10% of the lines from the hub's mid-plane out to the side nets, over their full length (the gap and the nets' offset from the mid-plane), holds it ~8–25× more stiffly (second figure; a chord resists sideways pulls out of its plane alike), for the extra line mass shown. Torsion is likewise held by preload only.

### Loads on the hub (finished torus, full spin): offset of the hub from the torus / force in the lines

Hub imbalance: 1% of the hub's mass at its rim. Torus imbalance: a 1% mismatch between two opposite arcs of 4θr, never ballasted. Orbit thrust: 1e-05 m/s² for the torus, pushed through its hub (notes §15). The torus and its hub turn about their common centre of mass.

| Torus | Hub imbalance | Torus imbalance | Orbit thrust |
|---|---|---|---|
| 400 m | 0.71 cm / 0.22 MN | 0.48 cm / 0.15 MN | 0.089 cm / 0.027 MN |
| 900 m | 3.1 cm / 2.0 MN | 2.0 cm / 1.3 MN | 0.21 cm / 0.13 MN |
| 1.6 km | 9.2 cm / 10 MN | 5.7 cm / 6.5 MN | 0.40 cm / 0.45 MN |
| 2.5 km | 22 cm / 40 MN | 13 cm / 23 MN | 0.68 cm / 1.2 MN |

### Building: the first arcs

At 0.71 of the final spin (net_statics), with a 1% mismatch between the arcs of a pair. A pair's chords run between its two arcs, nearly parallel: the lines hold the hub across them, but along them only through the arcs' small spread and the lines' preload. A second pair at right angles holds that direction. The preload is the larger of what gives the stiffness margin and what keeps every line 1.5× above its swing; the stiffness differs by direction, so the modes are solved: without preload a single pair is an asymmetric rotor and the hub's motion grows. Pull-in: how far the preload draws those chords into the window.

| Torus | First stage | Chords per net | Margin without preload | Without preload | Preload (kN) | Swing of tension (kN) | Chord pull-in (m) | Hub offset from the arcs (m) | Force in the lines (MN) |
|---|---|---|---|---|---|---|---|---|---|
| 400 m | one opposite pair | 12 | 0.062 | grows ×e every 0.20 turns | 110 | 73.2 | 0.85 | 4.0 (**more than the gap**) | 2.1 |
| 400 m | two pairs at right angles | 24 | 7.9 | stable | 24.9 | 16.6 | 0.19 | 0.13 | 0.42 |
| 900 m | one opposite pair | 27 | 0.036 | grows ×e every 0.22 turns | 292 | 156 | 2.4 | 9.0 (**more than the gap**) | 17 |
| 900 m | two pairs at right angles | 54 | 4.4 | stable | 102 | 67.9 | 0.85 | 0.58 | 4.0 |
| 1.6 km | one opposite pair | 48 | 0.025 | grows ×e every 0.25 turns | 909 | 276 | 7.6 | 16 | 78 |
| 1.6 km | two pairs at right angles | 96 | 2.9 | stable | 300 | 200 | 2.5 | 1.7 | 22 |
| 2.5 km | one opposite pair | 74 | 0.019 | grows ×e every 0.28 turns | 2,320 | 439 | 19 | 25 | 250 |
| 2.5 km | two pairs at right angles | 148 | 2.1 | stable | 745 | 496 | 6.2 | 4.2 | 87 |

Not modelled: the hub as a beam between tori and the stack's modes (plan §4), the elevator, pipe and power shafts and their compliant joints, docking loads (set by the dock's buffers), and torque through the lines.

## Tube cross-section: hull and frames by finite elements

One metre of tube in the plane of its cross-section (`structure_model/tube_section.py`): the pressure hull and the outer cell wall as membrane skins, the jacket's transverse bulkheads (one every 10 m) smeared into a plane-stress annulus between them, the rock, fill, lakes, air, bumper and steel under spin gravity, 70 kPa on the hull, and the chords' anchors on the outer wall holding the section along the radius. Every part is sized fully stressed at 300 MPa (von Mises at every integration point; half that in compression, blended with tension by the compression's share of the stress state, an allowance for stiffeners), or held at its minimum gauge (1 cm for the skins, 5 mm for bulkheads and cell walls). The skins also carry the hull's lengthwise pressure load and the pillowing of their panels between bulkheads; the hub-facing hull panels pressed in by the rock get stiffeners (vaulted ceiling), or the rock rests on hung cell floors instead (hung). Panels, cell walls and bumper are together in one column. Each anchor is a fitting through the jacket's depth, spreading the chord's pull over the radial line of nodes at its angle and pinned at the chord's attachment on the outer wall (a force, no couple). **Sizing:** *fully stressed* when every part is within 2% of its allowable or at its minimum gauge; *safe* when none is over it but some still have spare capacity after 200 rounds (heavier than needed); *over* when some part still exceeds it (not a design).

### Chords anchored at the tube's two sides (one net in each side plane), vaulted ceiling

| Torus | Load (MN per m of tube) | Hull (Mt) | Outer wall (Mt) | Bulkheads (Mt) | Panels, cell walls, bumper (Mt) | Hull and frames (Mt) | System model, r^2.3 (Mt) | Difference | Steel per torus (with spokes) vs model | Sizing |
|---|---|---|---|---|---|---|---|---|---|---|
| 400 m | 10.1 | 0.015 | 0.022 | 0.0080 | 0.011 | **0.055** | 0.046 | +19% | +7% | fully stressed |
| 900 m | 20.7 | 0.077 | 0.091 | 0.061 | 0.045 | **0.27** | 0.30 | -8% | -2% | fully stressed |
| 1.6 km | 35.9 | 0.32 | 0.29 | 0.39 | 0.14 | **1.1** | 1.1 | +1% | +0% | fully stressed |
| 2.5 km | 56.4 | 1.4 | 0.99 | 1.9 | 0.32 | **4.6** | 3.1 | +46% | +6% | fully stressed |

### Where the chords anchor

Anchors on the hub-facing crest (one net in the torus's mid-plane), at the two sides, or spread over the hub-facing half (anchors that would push are released; the rest share the load). Anchor loads per metre of tube; compression is the largest compressive force in a skin; displacement includes the section's ovalisation.

| Torus | Anchors | Ceiling | Steel (t per m of tube) | Per torus (Mt) | Anchor loads (MN/m) | Max skin compression (MN/m) | Max displacement (m) | Sizing |
|---|---|---|---|---|---|---|---|---|
| 900 m | crest | vaulted | 167 | 0.92 | 180°: 21.8 | 29 | 0.41 | fully stressed |
| 900 m | crest | hung | 179 | 0.98 | 180°: 21.9 | 29 | 0.41 | fully stressed |
| 900 m | sides | vaulted | 50.2 | 0.27 | 90°: 10.4, 270°: 10.4 | 1.3 | 0.079 | fully stressed |
| 900 m | sides | hung | 53.4 | 0.29 | 90°: 10.4, 270°: 10.4 | 2.2 | 0.11 | fully stressed |
| 900 m | fan | vaulted | 49.3 | 0.27 | 90°: 8.78, 120°: 1.04, 150°: 0.213, 180°: 0.674, 210°: 0.213, 240°: 1.04, 270°: 8.78 | 1.4 | 0.11 | fully stressed |
| 900 m | fan | hung | 52.8 | 0.29 | 90°: 9.51, 120°: 0.609, 150°: 0.0642, 180°: 0.402, 210°: 0.0642, 240°: 0.609, 270°: 9.51 | 2.8 | 0.12 | fully stressed |
| 1.6 km | crest | vaulted | 831 | 8.1 | 180°: 42.6 | 97 | 1.1 | safe, up to 4% spare |
| 1.6 km | crest | hung | 852 | 8.3 | 180°: 42.8 | 96 | 1.1 | fully stressed |
| 1.6 km | sides | vaulted | 117 | 1.1 | 90°: 17.9, 270°: 17.9 | 4.1 | 0.20 | fully stressed |
| 1.6 km | sides | hung | 123 | 1.2 | 90°: 18.0, 270°: 18.0 | 3.6 | 0.27 | fully stressed |
| 1.6 km | fan | vaulted | 112 | 1.1 | 90°: 17.3, 180°: 1.22, 270°: 17.3 | 3.1 | 0.28 | fully stressed |
| 1.6 km | fan | hung | 121 | 1.2 | 90°: 17.6, 180°: 0.678, 270°: 17.6 | 5.0 | 0.32 | fully stressed |
| 2.5 km | crest | vaulted | 3,600 | 55 | 180°: 87.4 | 300 | 2.4 | safe, up to 3% spare |
| 2.5 km | sides | vaulted | 302 | 4.6 | 90°: 28.2, 270°: 28.2 | 10 | 0.61 | fully stressed |
| 2.5 km | fan | vaulted | 284 | 4.3 | 90°: 27.2, 180°: 1.80, 270°: 27.2 | 6.0 | 0.83 | fully stressed |

### Sensitivity at 900 m (sides, vaulted)

| Change | Hull and frames (Mt) | vs base |
|---|---|---|
| `plate_stress_mpa` = 200 | 0.331 | +20% |
| `plate_stress_mpa` = 500 | 0.247 | -10% |
| `skin_min_gauge_m` = 0.005 | 0.222 | -19% |
| `skin_min_gauge_m` = 0.02 | 0.430 | +56% |
| `cell_wall_min_gauge_m` = 0.01 | 0.310 | +13% |
| `bumper_m` = 0.003 | 0.285 | +3% |

Not modelled: buckling of the parts in compression (sized with an allowance only), segment joints and seals, the anchors' local details, and the valley's buildings, light box and ceiling.

