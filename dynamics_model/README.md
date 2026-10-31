# Stack dynamics (plan §4)

Whirl modes of the flexible spinning stack and its passive stability. It uses the system model (`habitat_model`) for masses and geometry, and the structural model (`structure_model.hub`) for the nets' stiffness.

```bash
python -m dynamics_model                        # full report (reports/dynamics.md)
python -m dynamics_model --set hub_shell_m=0.05 --set ballast_frac=0.001
```

| File | Contents |
|---|---|
| `stack.py` | the stack's bodies, hub beam and springs; whirl modes (gyroscopic, inertial frame), damped modes with dissipation turning with the stack, the rigid J/I_t, the fixes (rim links, radial ties) and the bisection for what each needs |
| `links.py` | what the rim links must resist (sideways shear only), the X-braced rim lattice that does it, and the motions imposed between neighbours |
| `disturbances.py` | rim trains, imbalance, docking, sunlight pressure and the array's bearing: steady responses, impulses through the damped modes, slow torques |
| `axial_torsion.py` | motion along and about the axis: modes, the farm spokes' crossing and stabilising lines' lacing that keep them clear of the spin, docking and braking loads |
| `joints.py` | the hub's segment joints (needed stiffness, bolted flange), the lattice's fittings, the tunnels' expansion joints |
| `fatigue.py` | load cycles over a life against EN 1993-1-9's curves |
| `__main__.py` | the report |

## Model

- **The stack** spins at ω about z. The shared hub is an Euler-Bernoulli beam, a thin-walled tube of the hub's radius and wall `hub_shell_m` (2 cm, a guess), its mass the system model's hub, dock and factory metal (or its shell, if heavier) spread along it and lumped at nodes ≤ 20 m apart. Each torus is a rigid thin ring (J = m r², I_t = m r²/2, as in §11), tied to the hub at its two net planes by the nets' lateral stiffness. Each farm ring is a rigid ring on radial spokes in two planes at its sides (N/2 (EA + T)/L per plane). The despun array is a point mass at the far end.
- **Equations.** Every part is axisymmetric and every connection the same across the axis, so lateral motion is written with complex coordinates (displacement and slope) in the inertial frame: M q'' − iωG q' + K q = 0, G the spinning parts' polar inertia. Modes go as exp(iλt), λ > 0 forward. The free drift of the whole stack is removed by holding its centre of mass.
- **Criterion.** Dissipation that turns with the stack (lakes, people, flexing structure) destabilises every forward whirl slower than the spin. So the stack is passively stable only if its lowest forward mode exceeds the spin. For a rigid stack that mode is the nutation, at (J/I_t) ω: §11's maximum-axis rule. The ratio of the lowest forward mode to the spin is the flexible stack's inertia ratio; 1.2 keeps §11's 20% margin. A damped solve (dissipation proportional to stiffness, turning with the stack: −D(q' − iωq)) checks it.
- **Checks:** a ring alone nutates at 2ω; a body on a spring whirls at ±√(k/m); a stiff stack reproduces §11's rigid ratio (within the hub's mass); without dissipation every mode is neutral.

## Findings

- **The nets alone don't keep a stack passively stable.** The tangent chords carry each torus's spin load from rim to rim, so nothing in the main load path keeps a torus on the shared axis: only the stabilising lines, deflecting the chords sideways, ~mω²/2 at every size (0.42–0.47). A torus alone just turns about its own centre with its hub. In a stack, though, it is held by the others through the hub, so it drifts outward. Its forward whirl sits at ~0.68ω for a pair, and the stack's tilt (tori sliding instead of tilting) at ~0.16ω for a six-stack. With 1% damping the motion grows ×e every ~2–3 hours.
- **Fixes:**
  - **Rim links** between neighbouring tori (tunnels, or a thin cylinder across the gap). They are enough for a pair (~1e8 N/m at 900 m, a few tonnes of steel) and a 900 m six-stack (~1.2e9 N/m).
  - **Radial ties** from the hub to each torus, stiff along their length and carrying no spin load. Alone they need ~0.2% of a torus's mass for a pair, ~1.7–2.8% for a six-stack.
  - **Together** (1e11 N/m links and 0.01% ties): lowest forward whirl ~1.8 / 1.6 × the spin at 900 m (pair / six), ~1.6 / 1.3 at 1.6 km, stable in the damped solve.
- **Long stacks are limited by the hub bending** with the farm section at its end. The wall needed for a margin of 1.2 is ~0.4 cm (6 tori), ~3 cm (10), ~12 cm (14) and ~63 cm (18) at 900 m, against ~65 cm if the hub's whole mass budget went into its wall. At 1.6 km it is ~1 / 10 / 53 cm for 6 / 10 / 14 tori. So the flexible limit is ~18 tori of 900 m and ~14–17 of 1.6 km, against §11's rigid 22 and 25.
- **The rim links need only sideways stiffness.** Their tilt stiffness (stiffness along the axis) moves the margin by under 1%, and links stiff only tangentially, spread evenly around the rim (three or more), give the same sideways stiffness every way, so they can be compliant radially. Proposed: an X-braced lattice of pinned struts across each gap, no preload, designed for 98% of the margin rigid links give (~0.7–1 × 10¹⁰ N/m), sized by buckling under the untrimmed ballast: ~0.55–0.7 kt per gap at 900 m, ~1.3–1.7 kt at 1.6 km (~0.005% of a torus), ~5–6% of the gap covered. With it the ties are needed only for 1.6 km six-stacks (~0.004%). Imposed motions (the hub 20 K warmer, struts 100 K colder, a rim 4 K warmer) cost ~0.2–0.6 MN and ~10 MPa: along the axis the nets give way, not the lattice.
- **Disturbances are small.** Rim trains whirl below the spin, where the stack has no forward modes (~0.2 MN, mm). The ballast tanks' whole capacity untrimmed moves the tori ~8–34 cm and loads a lattice with 31–160 MN (its design load, iterated with the struts it sizes). A 10 kt ship missing the dock by 0.1 m/s turns the axis ~2 × 10⁻⁶°; the nutation dies out in hours to days at 1% damping. Sunlight on the array sums to zero over every orbit (Kepler's second law), leaving a yearly wobble under 0.0004°. The array's bearing costs no spin while its drive works: the drive's reaction cancels the friction on the hub, leaving only its power (~1 kW per 10 kN·m) as heat; drive off, the stack gives up the array's share, ~10⁻⁶, once.
- **Damping:** none needs adding; with every forward mode above the spin, dissipation only sets how fast a disturbance dies out.
- **Checks (disturbances, links):** a body on a spring under a whirling load and after a kick; a lattice bay's stiffness from its struts' geometry; tangential links isotropic; a train at the rim's speed pulls on nothing, and the response falls monotonically below the spin; an imbalance shifts the stack about its centre of mass; sunlight's push over a Kepler orbit closes and its excursion matches the wobble formula.
- **The hub's shear** (Timoshenko, in every result) costs ~1–3% of the margin; its **segment joints** must be full-strength (up to ~6 × 10¹⁴ N·m/rad for 98% of a continuous hub's margin); a bolted flange gives 10–2,000× that and its bolts never let it open.
- **Along and about the axis** no mode may sit within 1/1.4–1.4× the spin (once-per-turn loads from the despun array's bearing). As built the farm rings bounce at ~1.04–1.09× (their radial spokes hold them along the axis only by their tension, ~ω√(r_f/L) at any size) and the hub twists at ~1.05–1.3×. Crossing ~15–30% of the farm spokes between their planes and lacing ~0.1–0.2% of the stabilising lines clears the band (~2–80 t per stack); the slower twists stay below it.
- **Building and losing a lattice:** one gap unlinked destabilises the stack again (×e in ~2–3 h at 1% damping); 1–5% of its bays restore it.
- **Fittings and tunnels:** shear webs through the jacket, in series with the struts in every stiffness and sized for it as well as for strength (~1.0–1.4 cm, ~4–11 kt per gap; cantilever posts would be far too soft); tunnels on pressure-balanced expansion joints taking ±4–8 cm radially and ±2.4 cm axially, with at most ~1% of the lattice's sideways stiffness.
- **Fatigue:** every stress range over 100 years (×1.35) under EN 1993-1-9's cut-off.
- **Checks (hub, joints, axial, fatigue):** a Timoshenko cantilever with and without a joint; stiff joints leave the margin; a farm ring bounces at about ω √(r_f / L) on its spokes' tension; the flange's stiffness; crossing and lacing clear the band around the spin, and crossed spokes leave the twist alone; an unlinked gap loses the margin and a few bays restore it; the fatigue curve's knees; the lattice's stiffnesses agree (struts and fittings in series, torsion 2 k_lat R²); a cantilever post would be too soft; a web's stiffness.
- **Not modelled:** the elevator, pipe and power shafts, the lattice's erection on a torus still hung in arcs, the fittings' local details, the bellows' own design.
