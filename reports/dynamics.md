# Stack dynamics: whirl modes and passive stability

The stack as one flexible spinning body (`dynamics_model/stack.py`): the shared hub as a thin-walled beam (radius from the system model, wall 2.00 cm unless stated, its mass the system model's hub, dock and factory metal spread along it), each torus a rigid thin ring tied to the hub at its two net planes by the nets' lateral stiffness (`structure_model/hub.py`), each farm ring a rigid ring on radial spokes in two planes, the despun array a mass at the far end. Lateral motion in the inertial frame, complex coordinates: M q'' − iωG q' + K q = 0, G the spinning parts' polar inertia.

**Criterion.** Dissipation that turns with the stack (lakes, people, flexing structure) destabilises every forward whirl slower than the spin, so the stack is passively stable only if its lowest forward mode whirls faster than the spin (drift and precession aside). For a rigid stack that mode is its nutation, at J/I_t times the spin: §11's maximum-axis rule. The ratio below is the flexible stack's equivalent of §11's inertia ratio; 1.2 keeps its 20% margin. A damped solve (1% of the stiffness, turning with the stack) checks it.

## The stack as designed: nets only

Torus centring: the nets' lateral stiffness over the centrifugal pull on a torus off the axis (mω²). The tangent chords carry a torus's spin load from rim to rim, so nothing in the main load path holds it on the shared axis: only the stabilising lines, deflecting the chords sideways, which comes to ~mω²/2 at every size. A torus alone just turns about its own centre with its hub; in a stack, held by the others through the hub, it drifts outward.

| Torus | Tori | Torus centring (K / mω²) | Rigid J/I_t | Lowest forward whirl / spin | Damped |
|---|---|---|---|---|---|
| 900 m | 2 | 0.46 | 1.99 | 0.45 | grows ×e every 2.3 h |
| 900 m | 6 | 0.46 | 1.90 | 0.16 | grows ×e every 2.4 h |
| 1.6 km | 2 | 0.44 | 1.99 | 0.46 | grows ×e every 3.1 h |
| 1.6 km | 6 | 0.44 | 1.92 | 0.16 | grows ×e every 3.1 h |

## Fixes

Rim links: neighbouring tori joined at their rims (tunnels, or a thin cylinder across the gap; its tilt stiffness taken as k r²/2, low for a cylinder), so the tori move and tilt together. Radial ties: steel from the hub to each torus's hub-facing side, in its net planes, stiff along its length and carrying no spin load. Each alone, for a margin of 1.2; then both together (1e+11 N/m links and 0.01% ties).

| Torus | Tori | Rim links alone | Radial ties alone | Both: lowest forward whirl / spin | Damped |
|---|---|---|---|---|---|
| 900 m | 2 | 1.1e+08 N/m (0.0050 mm shell, 2.2 t per link) | 0.18% (23 kt per torus) | 1.80 | stable |
| 900 m | 6 | 1.2e+09 N/m (0.059 mm shell, 26 t per link) | 1.81% (230 kt per torus) | 1.60 | stable |
| 1.6 km | 2 | 2.1e+08 N/m (0.0055 mm shell, 4.3 t per link) | 0.30% (120 kt per torus) | 1.56 | stable |
| 1.6 km | 6 | not enough alone | 3.07% (1,300 kt per torus) | 1.25 | stable |

## How long a stack: the hub's wall

With rim links (1e+11 N/m) and a trace of ties (0.01%), long stacks are limited by the hub bending with the farm section at its end. Wall needed for a margin of 1.2, against the wall the hub's whole mass budget would make (the system model's hub, dock and factory metal as a shell along the stack).

| Torus | Tori | Stack length (m) | Rigid J/I_t | Forward whirl / spin, 2.00 cm wall | Wall needed (cm) | Wall from the hub's budget (cm) | Forward whirl / spin at that wall |
|---|---|---|---|---|---|---|---|
| 900 m | 2 | 332 | 1.99 | 1.80 | 0.10 | 58.2 | 1.81 |
| 900 m | 6 | 895 | 1.90 | 1.60 | 0.43 | 64.7 | 1.77 |
| 900 m | 10 | 1,460 | 1.73 | 1.08 | 2.9 | 66.2 | 1.62 |
| 900 m | 14 | 2,020 | 1.54 | 0.714 | 12 | 66.8 | 1.42 |
| 900 m | 18 | 2,590 | 1.34 | 0.503 | 64 | 67.2 | 1.20 |
| 900 m | 22 | 3,150 | 1.15 | 0.374 | **not enough** | 67.4 | 1.01 |
| 1.6 km | 2 | 498 | 1.99 | 1.56 | 0.10 | 112 | 1.57 |
| 1.6 km | 6 | 1,390 | 1.92 | 1.25 | 1.4 | 120 | 1.44 |
| 1.6 km | 10 | 2,290 | 1.78 | 0.825 | 11 | 122 | 1.38 |
| 1.6 km | 14 | 3,190 | 1.61 | 0.535 | 55 | 123 | 1.27 |
| 1.6 km | 18 | 4,080 | 1.43 | 0.373 | **not enough** | 123 | 1.11 |
| 1.6 km | 22 | 4,980 | 1.25 | 0.275 | **not enough** | 123 | 0.944 |

## Rim links: what they must resist

Lowest forward whirl over the spin with the links' tilt stiffness as taken above (k r²/2), with none, and with a lattice's (below), at the design stiffness and with the trace of ties. Only the links' sideways stiffness matters: they need not be stiff along the axis. And since sideways motion of two rims is radial at some angles and tangential at others, links stiff only tangentially, spread evenly around the rim (any three or more), give the same sideways stiffness in every direction: they can be compliant radially, free of the rims' differential growth (`dynamics_model/links.py`).

| Torus | Tori | Design stiffness (N/m) | Tilt k r²/2 | No tilt stiffness | Lattice's tilt |
|---|---|---|---|---|---|
| 900 m | 2 | 7.2e+08 | 1.77 | 1.77 | 1.77 |
| 900 m | 6 | 8.1e+09 | 1.57 | 1.56 | 1.57 |
| 1.6 km | 2 | 9.6e+08 | 1.53 | 1.53 | 1.53 |
| 1.6 km | 6 | 9.8e+09 | 1.23 | 1.23 | 1.23 |

## The lattice

A ring of X-braced bays across each gap at the envelopes' closest approach (r − a), diagonals at 45°, pinned tubular struts (D/t 20.0, no preload: struts, not cables, which would pull the tori together along the axis, where only the nets hold them). Stiff in shear and along the axis in its own surface, compliant radially (the struts bend out of it). Design stiffness: 98% of the margin rigid links would give (stiffer buys almost nothing; the nets and the hub's bending set the rest), with 0.01% ties. Struts sized for that stiffness, and for the largest link force below (the ballast tanks' whole capacity untrimmed) at a safety factor of 2.00 on buckling and on 350 MPa yield, at least 2.00 cm².

| Torus | Tori | Bays | Strut (cm², diameter) | Set by | Mass per gap (t) | Share of a torus | Gap blocked | Forward whirl / spin | Ties needed for 1.2 |
|---|---|---|---|---|---|---|---|---|---|
| 900 m | 2 | 548 | 45 (17 cm) | buckling | 550 | 0.004% | 4.8% | 1.80 | none |
| 900 m | 6 | 548 | 59 (19 cm) | buckling | 720 | 0.006% | 5.5% | 1.58 | none |
| 1.6 km | 2 | 974 | 60 (20 cm) | buckling | 1,300 | 0.003% | 5.5% | 1.56 | none |
| 1.6 km | 6 | 974 | 78 (22 cm) | buckling | 1,700 | 0.004% | 6.3% | 1.25 | 0.004% (1,700 t) |

**Imposed motions** between neighbours. Along the axis the lattice is far stiffer than the nets (`structure_model/hub.py`, inclined lines included), so the tori follow the lattice and the nets take the difference.

| Torus | Hub 20 K warmer over a pitch | One rim 4 K warmer | Struts 100 K colder |
|---|---|---|---|
| 900 m | 1.9 cm, 0.23 MN | 4.2 cm, hoop 9.6 MPa | gap closes 2.4 cm, 0.28 MN |
| 1.6 km | 3.0 cm, 0.63 MN | 7.4 cm, hoop 9.6 MPa | gap closes 2.4 cm, 0.51 MN |

## Disturbances

The stack with the lattice and ties above (`dynamics_model/disturbances.py`). Rim train: one 50.0 t train antispinward in the first torus, a load whirling at ω − v/R, below the spin, where a passively stable stack has no forward modes. Imbalance: the ballast tanks' whole capacity untrimmed (0.05% of the rim's mass at the first torus's rim), fixed in the rotating frame. Docking: a 10.0 kt ship missing by 0.100 m/s sideways at the dock, followed for 40 turns with 1% damping. Link force: the sideways force across one gap; torus: the largest torus's motion off the stack's axis.

| Torus | Tori | Train at 20 m/s: link force | Train: torus moves | Imbalance: link force | Imbalance: torus moves | Imbalance: dock moves | Docking: link force (peak) | Docking: axis turned | Docking: decay (×1/e) |
|---|---|---|---|---|---|---|---|---|---|
| 900 m | 2 | 0.15 MN | 1.6 mm | 31 MN | 20 cm | 18 cm | 0.18 MN | 0.0000022° | 6.5 h |
| 900 m | 6 | 0.24 MN | 0.59 mm | 52 MN | 7.9 cm | 3.7 cm | 0.30 MN | 0.0000022° | 2.3 h |
| 1.6 km | 2 | 0.17 MN | 0.87 mm | 97 MN | 34 cm | 27 cm | 0.085 MN | 0.00000045° | 53 h |
| 1.6 km | 6 | 0.28 MN | 0.31 mm | 160 MN | 12 cm | 2.6 cm | 0.47 MN | 0.00000044° | 13 h |

**Slow torques.** Sunlight on the despun array (pushed ×1.30 its absorbed value, the mast 100 m beyond the stack) and on the rims edge-on, about the centre of mass: it turns the axis sideways at τ/H, but the torque turns with the Sun and falls as 1/d², so by Kepler's second law it sums to zero over every orbit, eccentric or not: the axis only wobbles (at 1 AU, and on Eros's orbit, a = 1.458 AU, e = 0.223). The despun array's bearing (friction Q = 10.0 kN·m, a guess): its friction and the drive holding the array facing the Sun both act between array and hub, and the drive must cancel the friction on the array, so its reaction cancels the friction on the hub. Compensated, the stack keeps its spin and the friction only costs the drive's power, Qω, as heat. Uncompensated (drive off, or the bearing seized), friction drags the array up to the spin, and the stack gives up the array's share of the spin once.

| Torus | Tori | Sunlight torque (N·m) | Axis drift (°/yr, if it didn't turn) | Yearly wobble at 1 AU (°) | On Eros's orbit (°) | Drive power against the friction (kW) | Drive off: array at the spin in (h) | Spin given up then |
|---|---|---|---|---|---|---|---|---|
| 900 m | 2 | 620 | 0.00052 | 0.00016 | 0.00014 | 1.0 | 53 | 8.8e-07 |
| 900 m | 6 | 4,000 | 0.0011 | 0.00036 | 0.00030 | 1.0 | 480 | 2.7e-06 |
| 1.6 km | 2 | 2,600 | 0.00029 | 0.000091 | 0.000078 | 0.79 | 400 | 8.6e-07 |
| 1.6 km | 6 | 19,000 | 0.00069 | 0.00022 | 0.00019 | 0.79 | 3,600 | 2.6e-06 |

**Damping.** Every forward mode beats the spin, so no amount of dissipation turning with the stack destabilises it; it only sets how fast a disturbance dies out (×1/e in hours to days at 1%, ten times longer at 0.1%). Nothing has to be added for it.

## The hub: shear and joints

The hub is a short, wide tube (radius ~60 m), so its shear flexibility counts: every result above includes it (Timoshenko, κ = 0.5). It is built in segments, one per torus or farm ring, joined at the gaps; each joint a rotational spring (`dynamics_model/joints.py`). Needed: the stiffness keeping 98% of a continuous hub's margin, against one pitch of the hub's own wall (EI over the pitch) and a bolted flange ring (M36 bolts every 10.0 cm, 20.0 cm grip), whose bolts' preload must keep it closed under the hub's largest moment (the ballast tanks' whole capacity untrimmed).

| Torus | Tori | Margin, no shear | With shear | Joint needed (N·m/rad) | One pitch of hub (EI/p) | Bolted flange | Margin with flanges | Flange: preload / load |
|---|---|---|---|---|---|---|---|---|
| 900 m | 2 | 1.80 | 1.80 | 2.5e+12 | 3.5e+13 | 5.8e+15 | 1.80 | 387× |
| 900 m | 6 | 1.61 | 1.58 | 1.4e+14 | 3.5e+13 | 5.8e+15 | 1.58 | 92.2× |
| 1.6 km | 2 | 1.57 | 1.56 | 8.7e+12 | 1.3e+14 | 3.2e+16 | 1.56 | 196× |
| 1.6 km | 6 | 1.28 | 1.25 | 5.8e+14 | 1.3e+14 | 3.2e+16 | 1.25 | 28.0× |

## Along and about the axis

Axial and torsional motion (`dynamics_model/axial_torsion.py`) don't couple to the spin, so dissipation can't destabilise them, but a once-per-turn load (the despun array's bearing running slightly off true is the one interface turning against the stack) would pump any mode near the spin. Requirement: no mode between 1/1.40 and 1.40× the spin; modes well below or above are left alone. As built, two sit in that band. The farm rings bounce along the axis at ~1.04–1.09× the spin: their radial spokes hold them along it only by their tension, giving ~ω√(r_f/L) whatever the ring's size or mass (the tori had the same weakness in their nets, fixed with inclined lines, plan §2, and are now also tied by the lattice). And the hub twists between the tori's nets and the farm spokes at ~1.05–1.3×. Fixes, the least that clears the band: a share of each farm ring's spokes crossed between its two planes (from the front plane at the hub to the back plane at the ring, alternately, like a bicycle wheel's; still radial seen along the axis), and a small share of the tori's stabilising lines laced tangentially at 45.0°. The slower twists (the farm rings on their spokes, ~0.45×, and the farm section with the hub against the tori, ~0.2–0.35×) stay well below the spin. Loads on the fixed stack: a 10.0 kt ship closing at 0.1 m/s, taken out over 10.0 s by the dock's buffers; a 50 t rim train braking at 0.1 g.

| Torus | Tori | Axial near the spin, as built | Torsion near the spin, as built | Farm spokes crossed | Lines laced | Extra steel (t per stack) | Axial: lowest above the band | Torsion: lowest above the band | Torsion below the band | Docking: largest force | Braking: torque on a lattice |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m | 2 | 1.05–1.09 | 1.28 | 15% | 0.07% | 2.3 | 1.40 | 1.40 | 0.25, 0.45 | 0.17 MN | 41 MN·m |
| 900 m | 6 | 1.05–1.09 | 1.28 | 15% | 0.07% | 7.1 | 1.40 | 1.40 | 0.25, 0.45 | 0.17 MN | 67 MN·m |
| 1.6 km | 2 | 1.04–1.09 | 1.05 | 30% | 0.22% | 27 | 1.40 | 1.40 | 0.34, 0.45 | 0.22 MN | 74 MN·m |
| 1.6 km | 6 | 1.04–1.09 | 1.05 | 32% | 0.22% | 83 | 1.40 | 1.40 | 0.34, 0.45 | 0.25 MN | 120 MN·m |

## Building and losing a lattice

The stack's margin with one gap unlinked: a torus just closed next to the stack, or a lattice lost. The share of a gap's bays (spread evenly) that restores 1.2.

| Torus | Tori | All linked | End gap unlinked | Worst gap unlinked | Grows ×e (1% damping) | Bays needed in that gap |
|---|---|---|---|---|---|---|
| 900 m | 2 | 1.80 | 0.521 | 0.521 (gap 1) | 2.3 h | 5 of 548 (0.8%) |
| 900 m | 6 | 1.58 | 0.585 | 0.398 (gap 3) | 2.3 h | 15 of 548 (2.6%) |
| 1.6 km | 2 | 1.56 | 0.505 | 0.505 (gap 1) | 3.1 h | 7 of 974 (0.7%) |
| 1.6 km | 6 | 1.25 | 0.532 | 0.365 (gap 3) | 3.1 h | 50 of 974 (5.1%) |

**While a torus is hung** at the end of a spinning stack (the stack keeps its spin), that torus a partial ring in two opposite pairs of arcs at right angles, held on the hub by its nets (in proportion to its chords) and by the temporary radial lines to its arcs' single-laced anchors (`structure_model/sequence.py`), and linked to its neighbour by the lattice's bays alongside its arcs (in proportion), or not. Lowest forward whirl over the spin:

| Torus | Tori | Share of the ring hung | Unlinked, no radial lines | Unlinked, radial lines | Linked as hung, no radial lines | Linked as hung, radial lines |
|---|---|---|---|---|---|---|
| 900 m | 2 | 25% | 0.568 | 1.34 | 1.23 | 1.99 |
| 900 m | 2 | 50% | 0.533 | 1.12 | 1.48 | 1.99 |
| 900 m | 2 | 95% | 0.521 | 0.879 | 1.77 | 1.99 |
| 900 m | 6 | 25% | 0.707 | 1.11 | 1.32 | 1.88 |
| 900 m | 6 | 50% | 0.651 | 0.967 | 1.43 | 1.87 |
| 900 m | 6 | 95% | 0.590 | 0.770 | 1.57 | 1.86 |
| 1.6 km | 6 | 25% | 0.639 | 0.958 | 1.04 | 1.84 |
| 1.6 km | 6 | 50% | 0.589 | 0.858 | 1.12 | 1.85 |
| 1.6 km | 6 | 95% | 0.536 | 0.698 | 1.24 | 1.82 |

## Fittings and tunnels

Each strut meets the torus at a fitting on the envelope, carried to the hull through the jacket and crawl space by a shear web in the bay's tangential-axial plane (a jacket bulkhead in that plane: at the tube's side, where the gap is, the jacket's depth runs along the axis), as wide as the jacket is deep, loaded in its own plane both tangentially and axially, its weak direction radial: sized with the lattice for stiffness (the struts take half the bay's compliance, the two fittings the rest) and strength (safety factor 2), and in series with the struts in every result above. A post bending as a cantilever through the jacket would be far too soft: sized for strength alone, its compliance would cut a 900 m six-stack's margin below 1. A tunnel (4.00 m radius) crosses each gap on an expansion joint taking the rims' relative motions (the imposed motions above and the lattice's own give under the largest load), holding its pressure thrust inside itself (pressure-balanced), with at most 1% of the lattice's sideways stiffness (more would make the stiffness differ by direction). Without a joint, a tube fixed at both rims (3 cm wall) has ~7–20% of the lattice's stiffness, at one angle, and is bent by a rim's growth.

| Torus | Tori | Fitting webs (thickness, mass per gap, their sideways stiffness) | Joint: radial | Axial | Tangential | Pressure thrust | Joint's sideways stiffness at most | Rigid tube: stiffness, stress |
|---|---|---|---|---|---|---|---|---|
| 900 m | 2 | 9.8 mm (buckling), 4,200 t, 3.8e+10 N/m | ±4.4 cm | ±2.4 cm | ±2.6 mm | 3.5 MN | 1.2e+08 N/m | 2.4e+09 N/m, 340 MPa |
| 900 m | 6 | 12 mm (buckling), 4,900 t, 4.5e+10 N/m | ±4.5 cm | ±2.4 cm | ±3.5 mm | 3.5 MN | 1.5e+08 N/m | 2.4e+09 N/m, 340 MPa |
| 1.6 km | 2 | 12 mm (buckling), 8,900 t, 8.1e+10 N/m | ±7.8 cm | ±2.4 cm | ±3.6 mm | 3.5 MN | 2.7e+08 N/m | 2.4e+09 N/m, 600 MPa |
| 1.6 km | 6 | 14 mm (buckling), 11,000 t, 9.6e+10 N/m | ±7.9 cm | ±2.4 cm | ±4.8 mm | 3.5 MN | 3.4e+08 N/m | 2.4e+09 N/m, 600 MPa |

## Fatigue

Load cycles over 100 years (`dynamics_model/fatigue.py`): rim trains (one cycle per lap, 75% of the time at 20 m/s), ballast trims (20% of the tanks' capacity daily), a docking a day, the rims' daily temperature difference (4 K), sunlight on the struts each turn. Stress ranges ×1.35 against EN 1993-1-9's cut-off (detail 71 MPa for the struts' and the hub's welds, 160 MPa for strand): below it, no damage.

| Torus | Tori | Part | Largest range ×1.35 (MPa) | Cut-off (MPa) | Damage (Miner) |
|---|---|---|---|---|---|
| 900 m | 6 | lattice struts | 13 | 29 | 0 |
| 900 m | 6 | hub wall | 0.54 | 29 | 0 |
| 900 m | 6 | stabilising lines | 9.6 | 65 | 0 |
| 1.6 km | 6 | lattice struts | 13 | 29 | 0 |
| 1.6 km | 6 | hub wall | 1.8 | 29 | 0 |
| 1.6 km | 6 | stabilising lines | 8.7 | 65 | 0 |

Not modelled: the elevator, pipe and power shafts, the fittings' local details in the jacket, the bellows' own design.
