# Radiation transport (plan §3)

How much shield the habitat needs against galactic cosmic rays: dose against areal density for the shield materials, the neutrons' share, a hydrogen-rich inner layer, a solar particle event, the torus's tube against a sphere, and what the dose means for the jacket's thickness. Geant4 and OLTARIS can't run here, so this is a stand-in: a simplified transport with its cascade's inputs guessed, checked against the figures it should reproduce and against OLTARIS's published results, which size the jacket.

```bash
python -m radiation_model                          # full report (reports/radiation.md), ~4 min
python -m radiation_model --set cascade_nucleons_coeff=0.8
```

| File | Contents |
|---|---|
| `physics.py` | elements and shield materials, Bethe stopping powers and CSDA ranges, nuclear cross sections (Letaw, Sihver), two-group neutron constants, ICRP 60 quality factor, neutron dose coefficients |
| `environment.py` | galactic cosmic rays (an interstellar spectrum, force-field modulation, six species groups with pions made in the shield), the August 1972 solar particle event |
| `transport.py` | straight-ahead transport along a ray through layers: slowing down, nuclear collisions and their products, slow neutrons handed to the diffusion |
| `neutrons.py` | two-group diffusion of the slow neutrons across a layered slab, the source summed over incoming directions |
| `shield.py` | dose at the centre of a spherical shell, for one material at many thicknesses or for layers |
| `tube.py` | rays traced through the tube's cross-section: jacket, fill, a cliff dwelling's soil |
| `reference.py` | OLTARIS's published results: Globus & Strout's Table 2, Janhunen's layered shield and slab factor |
| `__main__.py` | the report |

## Model

- **Environment:** the interstellar proton spectrum of Usoskin et al. (2005), modulated by the force-field approximation (φ ~300 MV at a deep solar minimum, ~1,000 MV at maximum); helium and three heavier groups (Z 3–10, 11–20, 21–28) at rough abundances, same spectrum per nucleon. Solar events: King's fit to August 1972.
- **Transport along a ray** (as classic HZETRN): charged particles slow down continuously (Bethe, CSDA ranges); every species collides at its interaction length. A collision leaves a leading nucleon (its energy share set by the spectrum-weighted moment `leading_nucleon_z`), charged pions above their threshold (two thirds of the rest of the energy, rest masses included), cascade nucleons and evaporation neutrons from the target, knocked-out light ions, and, for ions, lighter fragments at the same energy per nucleon. Pions interact like nucleons (in rock they collide long before they decay). Short-ranged particles come to equilibrium in fine steps before each recorded depth.
- **Slow neutrons** (below 20 MeV) leave the ray and diffuse across the shield in two groups (fast and thermal), slowing mostly on hydrogen; at the inner face they cross the habitat and re-enter the wall, so its fluence is the habitat's.
- **Dose:** dose equivalent at a point (ICRP 60 Q(L) for charged particles, fluence coefficients for neutrons), no body around it.
- **Geometry:** the centre of a large spherical shell (every direction through the same shield, as OLTARIS's sphere), and points inside the torus's tube, taken as straight: a ray at an angle ψ to its axis crosses 1/sin ψ times the shield its projection does.
- **Checks** (`tests/test_radiation.py`): proton ranges against PSTAR, no pions below threshold and every collision within its energy, ranges below the Bethe formula, cross sections, the quality factor, modulation; a thick slab's neutron balance, the slab source over directions, water absorbing the rock's neutrons; the free-space dose, dose falling with depth, water beating rock, neutrons dominating deep in rock, the nucleon attenuation length in air, the fine steps settling the short-ranged particles; the tube's axis against quadrature, the tube shielding better than a sphere; OLTARIS's table, the thickness search beyond its range, and the model matching it for water.

## Findings

- **Against OLTARIS** (`reference.py`: Globus & Strout 2017, Table 2; Janhunen 2020), for 20 mSv/yr at a sphere's centre: water ~6.6 t/m² (OLTARIS ~6.6), polyethylene ~5.8 (~6.1), lunar regolith ~8.4 (~10.3). The model falls too fast in rock (e-fold every ~1.7 t/m² against ~2.3), so the sizing uses OLTARIS's regolith curve; the tailings come out within ~2% of lunar regolith per tonne.
- **Geometry:** straight ahead, the tube's floor would get ~¼ of the sphere's dose; OLTARIS's slab gives ~½ near a wall (the deep dose is spread in angle), and the sizing uses ½.
- **Deep in rock about two thirds of the dose is neutrons.** A hydrogen-rich inner layer saves ~2 mSv/yr per t/m² of water over rock (model); OLTARIS: water and boron-10 inside save ~1.3 t/m².
- **Solar particle events** don't reach behind the jacket (August 1972: ~0.03 Sv behind 1 t/m²).
- **Behind 11 t/m²:** ~15 mSv/yr at a sphere's centre, ~7 near the walls. **Proposed: 10 t/m²** (~12 near the walls; ~−10% rock and mass per torus), kept at 11 in the system model until a run in the tube's own geometry.
- **Not modelled:** neutral pions' showers, muons, elastic scattering and angular spread, fragments recoiling in tissue; the stack's shading; capture gamma rays.
