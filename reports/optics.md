# Light pipes, the light box and the farm's tiers

Plan §7 (`optics_model/`): how much of the sulfur lamps' light the prism light pipes carry, the valley's magnesium-oxide light box and diffuser pass to the floor, and a farm tier's pipes put on the crops, and how evenly. Most inputs are estimates or guesses (`reports/assumptions.md`).

## From lamp to leaf

The share of the sulfur lamps' light that reaches the valley's floor and the farm's crops, step by step. "Delivered" counts what the floor or the canopy absorbs, divided by its absorptance: the light that, falling once, would be absorbed the same, which is how the sizing's daily light integrals are meant. The pipes are laid out for the power the traced delivery itself needs at 300 W a metre of pipe (valley: spaced for the sky's peak; farm: enough pipes for a bed's peak, rounded up), traced again until the two agree: more power means pipes closer together, which take back more of the light (`scenes.converged`).

| Step | Valley | Farm |
|---|---|---|
| Layout: valley pipes apart / farm pipes over each bed | 0.60 m | 7 |
| Lamp into the pipe, inside its acceptance cone (`pipe_coupling`) | 85% | 85% |
| Out of the pipe along its length (40 m, fed from both ends) | 72% | 72% |
| Through the light box to the floor / onto the crops | 82% | 93% |
| **Lamp to floor / crops** | **50%** | **57%** |
| … with the layout sized for the assumed deliveries (0.91 m, 5 a bed) | 53% | 59% |
| Assumed until now (`ceiling_delivery`, `farm_delivery`) | 75% | 85% |

The light box and the tiers do as well as the notes expected, or better: ~82% of the pipes' light reaches the valley's floor (the notes: ~75–85%), ~93% the crops (more with the pipes farther apart, below). But the notes' figures counted only the ceiling: getting the lamps' light into the pipes and out along them costs another ~39%, which the sizing left out. Most of the chain's inputs are guesses (the coupling, the film's loss, the extractor); they need measuring on real pipes and lamps (plan §8). If the lamps' efficacy (~1.4 µmol/J) was measured out of their own reflector, part of the coupling is already in it.

## The light pipe

A 25 cm prism light pipe fed by a lamp at each end (`optics_model/pipe.py`). Light enters within ~27.6° of the axis and travels by total internal reflection; ray classes by angle and skewness each reflect tan θ / (2 √(R² − b²)) times a metre. A white extractor strip inside, graded along the pipe for an even glow (at most 30% of reflections), scatters the light out; 85% of what it scatters leaves the pipe. Light reaching the far end enters the other lamp's reflector, which returns 50%. The extractor is graded on a 16 × 16 quadrature of the classes; the figures below are that profile checked on 20,000 classes sampled independently.

| Pipe length | Film loss per reflection | Light out | Absorbed by the film | By the extractor | At the far ends | Glow along the pipe: dimmest / brightest, from the mean |
|---|---|---|---|---|---|---|
| 20 m | 0.50% | **80%** | 4.0% | 14% | 2.2% | -1.5% / +1.9% |
| 20 m | 1.0% | **77%** | 7.9% | 14% | 2.1% | -1.5% / +1.9% |
| 20 m | 2.0% | **70%** | 15% | 12% | 1.9% | -1.5% / +2.0% |
| 40 m | 0.50% | **78%** | 7.5% | 14% | 1.1% | -1.7% / +2.0% |
| 40 m | 1.0% | **72%** | 14% | 13% | 1.1% | -1.7% / +2.0% |
| 40 m | 2.0% | **61%** | 27% | 11% | 0.93% | -1.7% / +2.0% |
| 80 m | 0.50% | **72%** | 14% | 13% | 0.60% | -1.8% / +2.0% |
| 80 m | 1.0% | **62%** | 27% | 11% | 0.54% | -1.8% / +2.0% |
| 80 m | 2.0% | **45%** | 46% | 8.0% | 0.43% | -1.6% / +1.9% |

Long pipes and lossy film compound: each ray reflects ~1–3 times a metre. Shorter pipes (more, smaller lamps) or better film recover some of it.

## The light box

One pipe's width of ceiling, repeating (`optics_model/scenes.py`): the magnesium-oxide top (95%), the pipe glowing from its lower half, a diffuser 0.75 m below it (60% transmitted, 35% reflected, 5% absorbed, all diffusely), and the floor (10% reflected). Traced across the pipes (`optics_model/trace.py`): diffuse rays in three dimensions, projected on the cross-section, which is exact for pipes long against their spacing. At the sky's peak (498 W/m² over a 12 h day, at the traced delivery) and 300 W a metre of pipe, the pipes sit 0.60 m apart.

| Pipe spacing | To the floor | Back into the pipes | Into the top | Into the diffuser | Stripes on the diffuser (brightest / dimmest) |
|---|---|---|---|---|---|
| 0.35 m | **75%** | 25% | 2.0% | 6.4% | 1.09 |
| 0.50 m | **79%** | 19% | 2.8% | 6.7% | 1.06 |
| 0.60 m (sized) | **82%** | 17% | 3.0% | 7.1% | 1.09 |
| 1.5 m | **91%** | 7.2% | 3.5% | 7.8% | 1.11 |

The diffuser sends back ~a third of the light; the box returns it, so what matters is what absorbs on the way. The pipes themselves take the most: light falling back on them is partly lost inside, so pipes packed side by side (as the notes had them) lose more than pipes ~1 m apart; the power the traced delivery needs packs them closer than the assumed one did.

| Diffuser below the pipes | To the floor | Stripes (brightest / dimmest) |
|---|---|---|
| 0.1 m | 82% | 1.36 |
| 0.25 m | 82% | 1.11 |
| 0.5 m | 82% | 1.06 |
| 0.75 m | 82% | 1.09 |
| 1 m | 82% | 1.10 |

The stripes fade by ~0.5 m (one to two pipe widths, as the notes proposed); the ratios here are within the tracing's noise (~±3–5%) beyond it.

## A farm tier

One bed (2.4 m) and one aisle (0.6 m), repeating around the ring: the canopy as a block 0.6 m tall (8% reflected), 7 pipes over each bed (0.34 m apart, for 787 W/m² over a 16 h photoperiod), the white underside of the tier above 2.2 m over the floor (2.5 m floor to floor).

| Pipes above the canopy | Onto the crops | Back into the pipes | Into the ceiling | Into the aisles | Light across the bed: lowest / highest, of the mean |
|---|---|---|---|---|---|
| 0.1 m | **94%** | 11% | 1.1% | 1.4% | 0.67 / 1.09 |
| 0.3 m | **93%** | 12% | 1.0% | 1.9% | 0.73 / 1.13 |
| 0.6 m | **92%** | 12% | 1.1% | 2.7% | 0.84 / 1.11 |
| 1 m | **91%** | 12% | 1.2% | 3.0% | 0.92 / 1.07 |

The tier is a white box whose main absorber is the crops, so nearly all the pipes' light ends up in them. Close pipes light the bed in stripes; ~0.6 m up the light across the bed is within ~15% of its mean, the dimmest at the bed's edges, where the aisles take some. The pipes can hang at a fixed height and the crops grow towards them.

| Aisle floor reflectance | Onto the crops |
|---|---|
| 20% | 92% |
| 50% | 93% |
| 90% | 94% |

The bed needs 787 W/m² at the traced delivery, so 7 pipes of 25 cm crowd a 2.4 m bed and take back more of the light; fewer pipes, each loaded more, would leave more for the crops (each pipe at 300 W/m and above, as the lamps allow):

| Pipes per bed | Apart | Lamp power at 300 W/m, per m² of bed | Onto the crops | Back into the pipes |
|---|---|---|---|---|
| 4 | 0.60 m | 500 W/m² | 99% | 6.2% |
| 6 | 0.40 m | 750 W/m² | 95% | 9.6% |
| 7 (sized) | 0.34 m | 875 W/m² | 93% | 12% |

## What moves it

Each input at its low and high, the rest as configured and the layout held as converged (rays: 80,000 a trace, so ±~0.5 point of noise).

| Input | Range | Status | Valley, lamp to floor | Farm, lamp to crops |
|---|---|---|---|---|
| `pipe_coupling` | 0.750 – 0.920 | guess | 44% – 54% | 50% – 61% |
| `film_loss_per_reflection` | 0.00500 – 0.0200 | estimate | 54% – 42% | 61% – 48% |
| `extractor_efficiency` | 0.750 – 0.950 | guess | 44% – 56% | 50% – 63% |
| `pipe_end_return` | 0.200 – 0.800 | guess | 49% – 50% | 56% – 57% |
| `pipe_albedo` | 0.600 – 0.900 | guess | 44% – 54% | 52% – 60% |
| `mgo_reflectance` | 0.900 – 0.980 | estimate | 49% – 51% | 56% – 57% |
| `diffuser_transmittance` | 0.450 – 0.750 | estimate | 44% – 54% | 57% – 57% |
| `diffuser_absorptance` | 0.0200 – 0.100 | estimate | 52% – 47% | 57% – 57% |
| `floor_albedo` | 0.0500 – 0.200 | estimate | 48% – 54% | 57% – 57% |
| `canopy_reflectance` | 0.0500 – 0.120 | estimate | 50% – 50% | 55% – 58% |
| `aisle_reflectance` | 0.200 – 0.900 | guess | 50% – 50% | 56% – 57% |
| `canopy_height_m` | 0.300 – 1.00 | estimate | 50% – 50% | 55% – 57% |

## What it would mean

The system model with the traced chain (valley 50%, farm 57%) in place of the assumed 75% and 85%: a six-stack at Eros, three tiers lit, and the assembled stack's radiative exchange (`habitat_model/cavity.py`, farm radiators outboard, 4,000 rays). People per tier don't change (the light on the crops sets them); everything that scales with the lamps does. The configured deliveries are left as they are until the chain's guesses are measured.

| Torus |  | Assumed | Traced | Change |
|---|---|---|---|---|
| 900 m | Valley sky, daily average | 52.6 MW | 79.3 MW | +51% |
| 900 m | Per farm tier lit | 32.1 MW | 48.1 MW | +50% |
| 900 m | Electricity and heat per torus, three tiers lit | 154 MW | 228 MW | +49% |
| 900 m | Despun array per torus at the site | 186 ha | 276 ha | +48% |
| 900 m | Radiators: best margin, all panels | 2.5× | 1.7× | -32% |
| 900 m | Radiator panels for 1.5×, per torus | 78.2 ha | 169 ha | +116% |
| 1.6 km | Valley sky, daily average | 166 MW | 251 MW | +51% |
| 1.6 km | Per farm tier lit | 101 MW | 152 MW | +50% |
| 1.6 km | Electricity and heat per torus, three tiers lit | 485 MW | 721 MW | +49% |
| 1.6 km | Despun array per torus at the site | 589 ha | 873 ha | +48% |
| 1.6 km | Radiators: best margin, all panels | 2.4× | 1.6× | -33% |
| 1.6 km | Radiator panels for 1.5×, per torus | 249 ha | 790 ha | +218% |

The radiators still reach 1.5× with every panel in place, but need about twice the panel area or more (on the 1.5× search's coverage grid): a panel's output falls as coverage rises and the panels shade each other, so the extra heat costs more than its share of panels.

Not modelled: the light box's ends and the cliffs' edges (a ~1 m deep box along a ~56 m wide valley loses a little at its sides), the pipes' ends and joints, the sulfur lamp's spectrum (PAR only), angular (not diffuse) scattering by real diffusers and prism film, dust and ageing, the canopy as a volume (leaves at many heights), the ceiling's grading brighter overhead (notes §13), and lamps placed straight in the light box without pipes (an option if the pipes' losses hold up: smaller lamps, ~1 kW, behind the diffuser).
