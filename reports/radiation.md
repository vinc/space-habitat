# Radiation transport: how much shield

Plan §3 (`radiation_model/`). Galactic cosmic rays carried through the shield by a one-dimensional straight-ahead transport along each ray (`transport.py`, as HZETRN does in its classic form): protons, neutrons, helium and three heavier groups, and the charged pions they make, slowing down and colliding (leading nucleons, cascade nucleons, evaporation neutrons, knocked-out light ions, fragments); the slow neutrons followed by two-group diffusion across the shield (`neutrons.py`); then the directions, at a sphere's centre or inside the torus's tube (`tube.py`). Geant4 and OLTARIS can't run here; this is a stand-in, with its cascade's inputs guessed, checked against the figures below and against OLTARIS's published results (`reference.py`), which in the end size the jacket. Left out: the neutral pions' showers, muons, elastic scattering, angular spread, and the fragments that recoil in the body's own tissue.

## Checks

Against figures the model should reproduce (all but PSTAR's recalled, not looked up):

|  | Model | Reference |
|---|---|---|
| Proton range in water, 100 MeV | 7.71 g/cm² | 7.72 g/cm² (NIST PSTAR) |
| … 1 GeV | 325 g/cm² | ~324 g/cm² (PSTAR) |
| Inelastic cross section, p + O | 309 mb | ~300 mb (measured) |
| … C + C | 869 mb | ~850–900 mb (measured) |
| Nucleons above 1 GeV in air, attenuation length | 115 g/cm² | ~120 g/cm² (Gaisser; this air's interaction length is ~7% short) |
| Free space behind 5 g/cm², solar minimum | 1.7 Sv/yr, 0.36 Gy/yr | ~1 Sv/yr, ~0.2–0.3 Gy/yr (recalled): the model runs ~1.5× high here, from its heavy ions |

## Dose against areal density

Dose equivalent (mSv/yr, ICRP 60 quality factors, at a point with no body around it) at the centre of a large spherical shell, every direction crossing the same shield (as OLTARIS's sphere), galactic cosmic rays at a deep solar minimum (φ = 300 MV); in brackets, the share from neutrons (above 20 MeV straight ahead, and the slow ones diffusing from the walls).

| Shield | Tailings (L/LL, metal removed) | CI-like clays | Water | Polyethylene |
|---|---|---|---|---|
| 0 t/m² (unshielded) | 2,600 | 2,600 | 2,600 | 2,600 |
| 1 t/m² | 690 (48%) | 530 (32%) | 440 (24%) | 390 (26%) |
| 2 t/m² | 550 (52%) | 430 (37%) | 330 (31%) | 270 (34%) |
| 3 t/m² | 380 (54%) | 300 (41%) | 210 (37%) | 160 (40%) |
| 5 t/m² | 150 (57%) | 120 (48%) | 69 (46%) | 46 (50%) |
| 7 t/m² | 54 (61%) | 43 (54%) | 19 (52%) | 11 (57%) |
| 9 t/m² | 18 (64%) | 14 (59%) | 4.8 (58%) | 2.3 (63%) |
| 11 t/m² | 5.4 (67%) | 4.1 (62%) | 1.1 (62%) | 0.46 (67%) |
| 13 t/m² | 1.6 (69%) | 1.2 (65%) | 0.24 (65%) | 0.087 (71%) |
| 15 t/m² | 0.44 (71%) | 0.32 (68%) | 0.052 (68%) | 0.015 (73%) |
| 20 t/m² | 0.016 (75%) | 0.011 (72%) | 0.00090 (73%) | 0.00018 (78%) |
| **20 mSv/yr reached at** | **8.8 t/m²** | **8.4 t/m²** | **6.9 t/m²** | **6.2 t/m²** |

Per tonne, hydrogen shields best: it makes no neutrons of its own and slows the others. The tailings, rich in iron and magnesium, are the worst of the four; the clays' bound water helps a little. Behind a few t/m² the dose is mostly secondaries: neutrons (two thirds of it, deep in rock), pions and the protons and light ions the cascade knocks out, regenerated all the way through; the heavy ions are gone by ~1 t/m².

These are the model's own figures; against OLTARIS (next) they fall too fast with depth in rock.

## Against OLTARIS

OLTARIS (NASA's HZETRN, with its neutrons' angular spread) for the same sphere, from Globus & Strout (2017, Table 2: the 1977–78 solar minimum, effective dose on a female body model). Model / OLTARIS, mSv/yr:

| Shield | Lunar regolith | Water | Polyethylene |
|---|---|---|---|
| 1 t/m² | 700 / 281 | 440 / 200 | 390 / 194 |
| 2 t/m² | 560 / 275 | 330 / 147 | 270 / 137 |
| 3 t/m² | 390 / 240 | 210 / 101 | 160 / 91.0 |
| 4 t/m² | 250 / 194 | 120 / 67.0 | 88 / 57.0 |
| 5 t/m² | 150 / 149 | 69 / 43.0 | 46 / 35.0 |
| 6 t/m² | 92 / 109 | 37 / 26.5 | 23 / 21.0 |
| 7 t/m² | 54 / 77.0 | 19 / 16.1 | 11 / 12.3 |
| 8 t/m² | 31 / 52.0 | — | — |
| 9 t/m² | 17 / 34.9 | — | — |
| 10 t/m² | 9.6 / 22.8 | — | — |
| 11 t/m² | 5.3 / 14.5 | — | — |
| **20 mSv/yr** | **8.8 / 10.3 t/m²** | **6.9 / 6.57 t/m²** | **6.2 / 6.10 t/m²** |

Two differences, both expected: shallow, the model's point dose runs ~2× OLTARIS's dose averaged over a body, which shields its own organs from the heavy ions; deep, the model falls too fast, e-fold every ~1.7 t/m² of rock against OLTARIS's ~2.3, so behind 9–11 t/m² of regolith it is 2–3× low. For water the two cross near the limit and agree on the thickness; for rock the model's ~8.8 t/m² is too thin, and OLTARIS's ~10.3 t/m² (the notes' ~11) stands. Two cascade inputs can't match all three materials at once (fitting rock's slope puts water ~2.5× high), so the model is kept for what it compares, and the sizing below rests on OLTARIS's curve.

Its comparison of rock types holds better than its depth: the tailings, richer in iron and magnesium than lunar regolith, come out within ~2% of it at 9–11 t/m² (about as much neutron-making per tonne), so OLTARIS's regolith curve stands for the tailings.

## Inside the tube, straight ahead

The 900 m torus's cross-section (`radiation_model/tube.py`): the tube (radius 28 m), the jacket (thinner under the fill by its credit, as the system model has it), the 1 m fill over the lower half. Rays to every direction, their path through rock and fill counted as tailings, the tube taken as straight (its radius is 1/32 of the torus's); slow neutrons as from the slab. Neighbouring tori, the hub and the farm section, which hide some of the sky in a stack, are left out.

| Jacket | Sphere centre | On the floor (1.5 m up) | Tube's centre | Under the ceiling | Cliff dwelling behind 2 m of soil |
|---|---|---|---|---|---|
| 7 t/m² (3.5 m; 2.6 m under the fill) | 54 | 19 | 33 | 19 | 15 |
| 9 t/m² (4.5 m; 3.6 m under the fill) | 18 | 5.1 | 9.5 | 5.2 | 4.1 |
| 11 t/m² (5.5 m; 4.6 m under the fill) | 5.4 | 1.4 | 2.7 | 1.4 | 1.1 |
| 13 t/m² (6.5 m; 5.6 m under the fill) | 1.6 | 0.34 | 0.73 | 0.35 | 0.28 |

Straight ahead, a long tube shields better than a sphere of the same wall: a ray leaving at an angle ψ to its axis crosses 1/sin ψ times the wall, so the model puts the floor and the walls at ~¼ of the sphere's dose and the axis at ~½. That overstates it: in OLTARIS a point at the wall of a slab gets ~50% of the sphere's centre (Janhunen 2020), because deep in the shield the dose comes from particles spread in angle (neutrons above all), which slant paths don't stop as well. The sizing takes OLTARIS's ½ near the walls.

## A hydrogen-rich inner layer

9.0 t/m² of tailings (sphere centre: 18 mSv/yr, 2.6 of it from slow neutrons), then an inner layer: more tailings, water (moist soil, ponds, tanks) or polyethylene. The slow neutrons are traced at every slant through the layers.

| Inner layer | More tailings | Water | Polyethylene | Water saves, against tailings |
|---|---|---|---|---|
| 0.25 t/m² | 15 | 13 | 12 | 2.3 |
| 0.5 t/m² | 13 | 11 | 9.6 | 2.3 |
| 1 t/m² | 9.8 | 7.6 | 6.5 | 2.2 |
| 2 t/m² | 5.4 | 3.7 | 2.9 | 1.7 |

A water layer stops the neutrons that diffuse out of the dry rock (a few cm of it already) and shields the high-energy particles about as well as rock per tonne; the floor's moist fill, the cliff dwellings' soil and any tanks against the walls do this already.

OLTARIS agrees on the direction (Janhunen 2020): 8.68 t/m² of dry regolith with 0.18 t/m² of water and 1 kg/m² of boron-10 inside it (and 0.18 t/m² of iron outside) gives 20 mSv/yr at a sphere's centre, ~9.04 t/m² in all against ~10.3 t/m² of bare regolith.

## A solar particle event

The August 1972 event's protons (King 1974), taken as isotropic over the event: dose equivalent (Sv) for the whole event at the centre of the shell.

| Shield | Tailings | Water |
|---|---|---|
| 1 g/cm² | 29 | 33 |
| 5 g/cm² | 4.9 | 4.1 |
| 10 g/cm² | 1.4 | 0.91 |
| 20 g/cm² | 0.28 | 0.13 |
| 50 g/cm² | 0.065 | 0.019 |
| 100 g/cm² | 0.029 | 0.011 |

Lethal in a light spacecraft, nothing behind the jacket: the event's protons are spent within a few tens of g/cm², and what reaches ~1 t/m² is a trickle of neutrons. Crews outside the jacket (the hub, the farm, the factory) need a storm shelter of ~20–50 g/cm², as the notes have it.

## What moves it

Each input at its low and high, the rest as configured: the tailings at the sphere's centre.

| Input | Range | Status | Dose at 11 t/m², mSv/yr | For 20 mSv/yr |
|---|---|---|---|---|
| `solar_min_phi_mv` | 250 – 450 | estimate | 5.5 – 5.0 | 8.8 – 8.6 t/m² |
| `leading_nucleon_z` | 0.250 – 0.350 | estimate | 3.3 – 8.6 | 8.2 – 9.5 t/m² |
| `cascade_nucleons_coeff` | 0.300 – 0.800 | guess | 3.7 – 8.6 | 8.2 – 9.5 t/m² |
| `cascade_nucleon_mev` | 60.0 – 150 | guess | 4.0 – 7.1 | 8.4 – 9.2 t/m² |
| `evaporation_neutrons_coeff` | 0.100 – 0.300 | guess | 5.1 – 5.6 | 8.7 – 8.9 t/m² |
| `knockout_alphas_coeff` | 0.0500 – 0.200 | guess | 5.0 – 6.2 | 8.6 – 9.0 t/m² |
| `fast_neutron_dose_psv_cm2` | 250 – 420 | estimate | 5.2 – 5.5 | 8.7 – 8.8 t/m² |

The cascade's guessed inputs move the model's dose behind 11 t/m² by about −40% / +60%, its thickness for the limit by ±0.6 t/m²; none of them closes the gap to OLTARIS at depth on its own.

## The jacket's thickness

OLTARIS's lunar regolith curve (Globus & Strout, Table 2, extended past 11 t/m² at its last slope), scaled to the tailings by the model, for a sphere's centre, which bounds the tube's middle; near the walls (the floor, the cliff dwellings, under the ceiling) OLTARIS's slab factor, ~0.50. Solar maximum: 25% less (Janhunen). mSv/yr:

| Jacket | Sphere's centre (the tube's middle, at most) | Near the walls, where people live | Sphere's centre, solar maximum |
|---|---|---|---|
| 8 t/m² | 53 | 26 | 39 |
| 9 t/m² | 36 | 18 | 26 |
| 10 t/m² (proposed) | 23 | 12 | 17 |
| 11 t/m² (configured) | 15 | 7.4 | 11 |
| 12 t/m² | 9.4 | 4.7 | 7.0 |

**20 mSv/yr is met at a sphere's centre with ~10.3 t/m² and near the walls with ~8.7 t/m².** The configured 11 t/m² gives ~15 mSv/yr at a sphere's centre and ~7.4 near the walls. **Proposed: 10 t/m²** (~5 m of rock): ~12 mSv/yr where people live, and ~23 at worst in the middle of the tube, where nobody lives (less still with the stack's shading and the body's own). The system model keeps 11 t/m² until a run in the tube's own geometry (OLTARIS or Geant4) confirms the factor near the walls.

## What it would mean

The system model with a 10 t/m² jacket in place of 11 t/m²: a six-stack at Eros (LL host, Ryugu as the C-type), three tiers lit.

| Torus |  | 11 t/m² | 10 t/m² | Change |
|---|---|---|---|---|
| 900 m | Rock shield per torus | 11.0 Mt | 9.87 Mt | -10% |
| 900 m | Mass per torus | 12.7 Mt | 11.5 Mt | -10% |
| 900 m | Mass per m² of floor | 40.1 t | 36.2 t | -10% |
| 900 m | S-type mined per torus | 32.8 Mt | 30.5 Mt | -7% |
| 900 m | Generation time, six-stack | 4.53 yr | 4.47 yr | -1% |
| 1.6 km | Rock shield per torus | 33.5 Mt | 30.1 Mt | -10% |
| 1.6 km | Mass per torus | 41.3 Mt | 37.5 Mt | -9% |
| 1.6 km | Mass per m² of floor | 41.1 t | 37.3 t | -9% |
| 1.6 km | S-type mined per torus | 168 Mt | 155 Mt | -7% |
| 1.6 km | Generation time, six-stack | 19.3 yr | 19.1 yr | -1% |

Not modelled: the stack's neighbouring tori, hub and farm section shading the sky (less dose), the hub-facing side's services and train tube, the body's self-shielding in the model's own figures (OLTARIS's include it), capture gamma rays from the slow neutrons, and seasonal or long-term changes of the heliosphere (OLTARIS's 1977–78 minimum is milder than 2009–10's).
