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
| 1.6 km | 6 | 0.44 | 1.92 | 0.17 | grows ×e every 3.1 h |

## Fixes

Rim links: neighbouring tori joined at their rims (tunnels, or a thin cylinder across the gap; its tilt stiffness taken as k r²/2, low for a cylinder), so the tori move and tilt together. Radial ties: steel from the hub to each torus's hub-facing side, in its net planes, stiff along its length and carrying no spin load. Each alone, for a margin of 1.2; then both together (1e+11 N/m links and 0.01% ties).

| Torus | Tori | Rim links alone | Radial ties alone | Both: lowest forward whirl / spin | Damped |
|---|---|---|---|---|---|
| 900 m | 2 | 1.1e+08 N/m (0.0050 mm shell, 2.2 t per link) | 0.18% (23 kt per torus) | 1.81 | stable |
| 900 m | 6 | 1.2e+09 N/m (0.057 mm shell, 25 t per link) | 1.69% (220 kt per torus) | 1.62 | stable |
| 1.6 km | 2 | 2.0e+08 N/m (0.0055 mm shell, 4.2 t per link) | 0.30% (120 kt per torus) | 1.57 | stable |
| 1.6 km | 6 | not enough alone | 2.81% (1,200 kt per torus) | 1.29 | stable |

## How long a stack: the hub's wall

With rim links (1e+11 N/m) and a trace of ties (0.01%), long stacks are limited by the hub bending with the farm section at its end. Wall needed for a margin of 1.2, against the wall the hub's whole mass budget would make (the system model's hub, dock and factory metal as a shell along the stack).

| Torus | Tori | Stack length (m) | Rigid J/I_t | Forward whirl / spin, 2.00 cm wall | Wall needed (cm) | Wall from the hub's budget (cm) | Forward whirl / spin at that wall |
|---|---|---|---|---|---|---|---|
| 900 m | 2 | 332 | 1.99 | 1.81 | 0.10 | 58.2 | 1.81 |
| 900 m | 6 | 895 | 1.90 | 1.62 | 0.36 | 64.7 | 1.77 |
| 900 m | 10 | 1,460 | 1.73 | 1.11 | 2.7 | 66.2 | 1.62 |
| 900 m | 14 | 2,020 | 1.54 | 0.727 | 11 | 66.8 | 1.42 |
| 900 m | 18 | 2,590 | 1.34 | 0.512 | 62 | 67.2 | 1.21 |
| 900 m | 22 | 3,150 | 1.15 | 0.379 | **not enough** | 67.4 | 1.01 |
| 1.6 km | 2 | 498 | 1.99 | 1.57 | 0.10 | 112 | 1.57 |
| 1.6 km | 6 | 1,390 | 1.92 | 1.29 | 1.2 | 120 | 1.44 |
| 1.6 km | 10 | 2,290 | 1.78 | 0.848 | 10 | 122 | 1.38 |
| 1.6 km | 14 | 3,190 | 1.61 | 0.548 | 52 | 123 | 1.27 |
| 1.6 km | 18 | 4,080 | 1.43 | 0.381 | **not enough** | 123 | 1.11 |
| 1.6 km | 22 | 4,980 | 1.25 | 0.280 | **not enough** | 123 | 0.946 |

## Rim links: what they must resist

Lowest forward whirl over the spin with the links' tilt stiffness as taken above (k r²/2), with none, and with a lattice's (below), at the design stiffness and with the trace of ties. Only the links' sideways stiffness matters: they need not be stiff along the axis. And since sideways motion of two rims is radial at some angles and tangential at others, links stiff only tangentially, spread evenly around the rim (any three or more), give the same sideways stiffness in every direction: they can be compliant radially, free of the rims' differential growth (`dynamics_model/links.py`).

| Torus | Tori | Design stiffness (N/m) | Tilt k r²/2 | No tilt stiffness | Lattice's tilt |
|---|---|---|---|---|---|
| 900 m | 2 | 7.3e+08 | 1.77 | 1.77 | 1.77 |
| 900 m | 6 | 8.7e+09 | 1.59 | 1.59 | 1.59 |
| 1.6 km | 2 | 9.7e+08 | 1.54 | 1.54 | 1.54 |
| 1.6 km | 6 | 1.0e+10 | 1.26 | 1.26 | 1.26 |

## The lattice

A ring of X-braced bays across each gap at the envelopes' closest approach (r − a), diagonals at 45°, pinned tubular struts (D/t 20.0, no preload: struts, not cables, which would pull the tori together along the axis, where only the nets hold them). Stiff in shear and along the axis in its own surface, compliant radially (the struts bend out of it). Design stiffness: 98% of the margin rigid links would give (stiffer buys almost nothing; the nets and the hub's bending set the rest), with 0.01% ties. Struts sized for that stiffness, and for the largest link force below (the ballast tanks' whole capacity untrimmed) at a safety factor of 2.00 on buckling and on 350 MPa yield, at least 2.00 cm².

| Torus | Tori | Bays | Strut (cm², diameter) | Set by | Mass per gap (t) | Share of a torus | Gap blocked | Forward whirl / spin | Ties needed for 1.2 |
|---|---|---|---|---|---|---|---|---|---|
| 900 m | 2 | 548 | 45 (17 cm) | buckling | 550 | 0.004% | 4.8% | 1.81 | none |
| 900 m | 6 | 548 | 58 (19 cm) | buckling | 710 | 0.006% | 5.5% | 1.61 | none |
| 1.6 km | 2 | 974 | 60 (20 cm) | buckling | 1,300 | 0.003% | 5.5% | 1.57 | none |
| 1.6 km | 6 | 974 | 77 (22 cm) | buckling | 1,700 | 0.004% | 6.3% | 1.28 | 0.001% (550 t) |

**Imposed motions** between neighbours. Along the axis the lattice is far stiffer than the nets (`structure_model/hub.py`, inclined lines included), so the tori follow the lattice and the nets take the difference.

| Torus | Hub 20 K warmer over a pitch | One rim 4 K warmer | Struts 100 K colder |
|---|---|---|---|
| 900 m | 1.9 cm, 0.23 MN | 4.2 cm, hoop 9.6 MPa | gap closes 2.4 cm, 0.28 MN |
| 1.6 km | 3.0 cm, 0.63 MN | 7.4 cm, hoop 9.6 MPa | gap closes 2.4 cm, 0.51 MN |

## Disturbances

The stack with the lattice and ties above (`dynamics_model/disturbances.py`). Rim train: one 50.0 t train antispinward in the first torus, a load whirling at ω − v/R, below the spin, where a passively stable stack has no forward modes. Imbalance: the ballast tanks' whole capacity untrimmed (0.05% of the rim's mass at the first torus's rim), fixed in the rotating frame. Docking: a 10.0 kt ship missing by 0.100 m/s sideways at the dock, followed for 40 turns with 1% damping. Link force: the sideways force across one gap; torus: the largest torus's motion off the stack's axis.

| Torus | Tori | Train at 20 m/s: link force | Train: torus moves | Imbalance: link force | Imbalance: torus moves | Imbalance: dock moves | Docking: link force (peak) | Docking: axis turned | Docking: decay (×1/e) |
|---|---|---|---|---|---|---|---|---|---|
| 900 m | 2 | 0.14 MN | 1.6 mm | 31 MN | 20 cm | 18 cm | 0.18 MN | 0.0000022° | 6.2 h |
| 900 m | 6 | 0.24 MN | 0.58 mm | 52 MN | 7.8 cm | 4.1 cm | 0.46 MN | 0.0000022° | 2.1 h |
| 1.6 km | 2 | 0.17 MN | 0.87 mm | 97 MN | 34 cm | 27 cm | 0.077 MN | 0.00000045° | 52 h |
| 1.6 km | 6 | 0.28 MN | 0.31 mm | 160 MN | 12 cm | 3.8 cm | 0.65 MN | 0.00000044° | 14 h |

**Slow torques.** Sunlight on the despun array (pushed ×1.30 its absorbed value, the mast 100 m beyond the stack) and on the rims edge-on, about the centre of mass: it turns the axis sideways at τ/H, but the torque turns with the Sun and falls as 1/d², so by Kepler's second law it sums to zero over every orbit, eccentric or not: the axis only wobbles (at 1 AU, and on Eros's orbit, a = 1.458 AU, e = 0.223). The despun array's bearing (friction Q = 10.0 kN·m, a guess): its friction and the drive holding the array facing the Sun both act between array and hub, and the drive must cancel the friction on the array, so its reaction cancels the friction on the hub. Compensated, the stack keeps its spin and the friction only costs the drive's power, Qω, as heat. Uncompensated (drive off, or the bearing seized), friction drags the array up to the spin, and the stack gives up the array's share of the spin once.

| Torus | Tori | Sunlight torque (N·m) | Axis drift (°/yr, if it didn't turn) | Yearly wobble at 1 AU (°) | On Eros's orbit (°) | Drive power against the friction (kW) | Drive off: array at the spin in (h) | Spin given up then |
|---|---|---|---|---|---|---|---|---|
| 900 m | 2 | 620 | 0.00052 | 0.00016 | 0.00014 | 1.0 | 53 | 8.8e-07 |
| 900 m | 6 | 4,000 | 0.0011 | 0.00036 | 0.00030 | 1.0 | 480 | 2.7e-06 |
| 1.6 km | 2 | 2,600 | 0.00029 | 0.000091 | 0.000078 | 0.79 | 400 | 8.6e-07 |
| 1.6 km | 6 | 19,000 | 0.00069 | 0.00022 | 0.00019 | 0.79 | 3,600 | 2.6e-06 |

**Damping.** Every forward mode beats the spin, so no amount of dissipation turning with the stack destabilises it; it only sets how fast a disturbance dies out (×1/e in hours to days at 1%, ten times longer at 0.1%). Nothing has to be added for it.

Not modelled: the hub's shear and joints, the elevator, pipe and power shafts, axial and torsional motion, the ties' and lattice's joints and how they are built into the construction sequence, a tunnel (one stiff link at one angle makes the stiffness differ by direction; it stays clear of trouble while the lattice's even stiffness dominates), fatigue.
