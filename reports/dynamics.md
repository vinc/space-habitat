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
| 900 m | 2 | 1.1e+08 N/m (0.0051 mm shell, 2.2 t per link) | 0.18% (23 kt per torus) | 1.80 | stable |
| 900 m | 6 | 1.2e+09 N/m (0.058 mm shell, 25 t per link) | 1.69% (220 kt per torus) | 1.62 | stable |
| 1.6 km | 2 | 2.1e+08 N/m (0.0055 mm shell, 4.3 t per link) | 0.30% (120 kt per torus) | 1.57 | stable |
| 1.6 km | 6 | not enough alone | 2.81% (1,200 kt per torus) | 1.28 | stable |

## How long a stack: the hub's wall

With rim links (1e+11 N/m) and a trace of ties (0.01%), long stacks are limited by the hub bending with the farm section at its end. Wall needed for a margin of 1.2, against the wall the hub's whole mass budget would make (the system model's hub, dock and factory metal as a shell along the stack).

| Torus | Tori | Stack length (m) | Rigid J/I_t | Forward whirl / spin, 2.00 cm wall | Wall needed (cm) | Wall from the hub's budget (cm) | Forward whirl / spin at that wall |
|---|---|---|---|---|---|---|---|
| 900 m | 2 | 332 | 1.99 | 1.80 | 0.10 | 58.4 | 1.81 |
| 900 m | 6 | 895 | 1.90 | 1.62 | 0.36 | 64.9 | 1.77 |
| 900 m | 10 | 1,460 | 1.73 | 1.10 | 2.7 | 66.4 | 1.62 |
| 900 m | 14 | 2,020 | 1.54 | 0.724 | 12 | 67.1 | 1.42 |
| 900 m | 18 | 2,590 | 1.34 | 0.509 | 63 | 67.4 | 1.20 |
| 900 m | 22 | 3,150 | 1.15 | 0.377 | **not enough** | 67.7 | 1.01 |
| 1.6 km | 2 | 498 | 1.99 | 1.57 | 0.10 | 112 | 1.57 |
| 1.6 km | 6 | 1,390 | 1.92 | 1.28 | 1.2 | 121 | 1.44 |
| 1.6 km | 10 | 2,290 | 1.78 | 0.846 | 10 | 122 | 1.38 |
| 1.6 km | 14 | 3,190 | 1.61 | 0.546 | 53 | 123 | 1.27 |
| 1.6 km | 18 | 4,080 | 1.43 | 0.380 | **not enough** | 123 | 1.11 |
| 1.6 km | 22 | 4,980 | 1.25 | 0.279 | **not enough** | 124 | 0.945 |

Not modelled: the hub's shear and joints, the elevator, pipe and power shafts, axial and torsional motion, the rim links' and ties' preload and details, and disturbances (docking, rim trains, ballast transfers, the array's bearing, sunlight pressure).
