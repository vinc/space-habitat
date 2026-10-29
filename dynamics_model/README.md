# Stack dynamics (plan §4)

Whirl modes of the flexible spinning stack and its passive stability. It uses the system model (`habitat_model`) for masses and geometry, and the structural model (`structure_model.hub`) for the nets' stiffness.

```bash
python -m dynamics_model                        # full report (reports/dynamics.md)
python -m dynamics_model --set hub_shell_m=0.05
```

| File | Contents |
|---|---|
| `stack.py` | the stack's bodies, hub beam and springs; whirl modes (gyroscopic, inertial frame), damped modes with dissipation turning with the stack, the rigid J/I_t, the fixes (rim links, radial ties) and the bisection for what each needs |
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
- **Not modelled:** the hub's shear and joints, the elevator, pipe and power shafts, axial and torsional motion, the rim links' and ties' preload and details, and the disturbances (docking, rim trains, ballast transfers, the array's bearing, sunlight pressure).
