# Light pipes, the light box and the farm's tiers

Plan §7 (`optics_model/`): how much of the sulfur lamps' light the prism light pipes carry, the valley's magnesium-oxide light box and diffuser pass to the floor, and a farm tier's pipes put on the crops, and how evenly. Most inputs are estimates or guesses (`reports/assumptions.md`).

## From lamp to leaf

The share of the sulfur lamps' light that reaches the valley's floor and the farm's crops, step by step. "Delivered" counts what the floor or the canopy absorbs, divided by its absorptance: the light that, falling once, would be absorbed the same, which is how the sizing's daily light integrals are meant.

| Step | Valley | Farm |
|---|---|---|
| Lamp into the pipe, inside its acceptance cone (`pipe_coupling`) | 85% | 85% |
| Out of the pipe along its length (40 m, fed from both ends) | 72% | 72% |
| Through the light box to the floor / onto the crops | 86% | 99% |
| **Lamp to floor / crops** | **53%** | **60%** |
| Assumed until now (`ceiling_delivery`, `farm_delivery`) | 75% | 85% |

The light box and the tiers do as well as the notes expected, or better: ~86% of the pipes' light reaches the valley's floor (the notes: ~75–85%), ~99% the crops. But the notes' figures counted only the ceiling: getting the lamps' light into the pipes and out along them costs another ~39%, which the sizing left out. Most of the chain's inputs are guesses (the coupling, the film's loss, the extractor); they need measuring on real pipes and lamps (plan §8). If the lamps' efficacy (~1.4 µmol/J) was measured out of their own reflector, part of the coupling is already in it.

## The light pipe

A 25 cm prism light pipe fed by a lamp at each end (`optics_model/pipe.py`). Light enters within ~27.6° of the axis and travels by total internal reflection; ray classes by angle and skewness each reflect tan θ / (2 √(R² − b²)) times a metre. A white extractor strip inside, graded along the pipe for an even glow (at most 30% of reflections), scatters the light out; 85% of what it scatters leaves the pipe. Light reaching the far end enters the other lamp's reflector, which returns 50%.

| Pipe length | Film loss per reflection | Light out | Absorbed by the film | By the extractor | At the far ends | Glow along the pipe |
|---|---|---|---|---|---|---|
| 20 m | 0.50% | **80%** | 4.0% | 14% | 2.1% | ±1.0% |
| 20 m | 1.0% | **77%** | 7.8% | 14% | 2.0% | ±1.0% |
| 20 m | 2.0% | **71%** | 15% | 12% | 1.8% | ±1.0% |
| 40 m | 0.50% | **78%** | 7.4% | 14% | 1.00% | ±1.0% |
| 40 m | 1.0% | **72%** | 14% | 13% | 0.93% | ±1.0% |
| 40 m | 2.0% | **62%** | 27% | 11% | 0.80% | ±1.0% |
| 80 m | 0.50% | **73%** | 14% | 13% | 0.47% | ±1.0% |
| 80 m | 1.0% | **62%** | 26% | 11% | 0.41% | ±1.0% |
| 80 m | 2.0% | **46%** | 46% | 8.1% | 0.31% | ±1.0% |

Long pipes and lossy film compound: each ray reflects ~1–3 times a metre. Shorter pipes (more, smaller lamps) or better film recover some of it.

## The light box

One pipe's width of ceiling, repeating (`optics_model/scenes.py`): the magnesium-oxide top (95%), the pipe glowing from its lower half, a diffuser 0.75 m below it (60% transmitted, 35% reflected, 5% absorbed, all diffusely), and the floor (10% reflected). Traced across the pipes (`optics_model/trace.py`): diffuse rays in three dimensions, projected on the cross-section, which is exact for pipes long against their spacing. At the sky's peak (331 W/m² over a 12 h day) and 300 W a metre of pipe, the pipes sit 0.91 m apart.

| Pipe spacing | To the floor | Back into the pipes | Into the top | Into the diffuser | Stripes on the diffuser (brightest / dimmest) |
|---|---|---|---|---|---|
| 0.35 m | **75%** | 25% | 2.0% | 6.4% | 1.09 |
| 0.50 m | **79%** | 19% | 2.8% | 6.7% | 1.06 |
| 0.91 m (sized) | **87%** | 11% | 3.2% | 7.5% | 1.07 |
| 1.5 m | **91%** | 7.2% | 3.5% | 7.8% | 1.11 |

The diffuser sends back ~a third of the light; the box returns it, so what matters is what absorbs on the way. The pipes themselves take the most: light falling back on them is partly lost inside, so pipes packed side by side (as the notes had them) lose more than pipes ~1 m apart.

| Diffuser below the pipes | To the floor | Stripes (brightest / dimmest) |
|---|---|---|
| 0.1 m | 86% | 2.00 |
| 0.25 m | 86% | 1.31 |
| 0.5 m | 87% | 1.12 |
| 0.75 m | 87% | 1.07 |
| 1 m | 86% | 1.07 |

The stripes fade by ~0.5 m (one to two pipe widths, as the notes proposed); the ratios here are within the tracing's noise (~±3–5%) beyond it.

## A farm tier

One bed (2.4 m) and one aisle (0.6 m), repeating around the ring: the canopy as a block 0.6 m tall (8% reflected), 4 pipes over each bed (0.60 m apart, for 525 W/m² over a 16 h photoperiod), the white underside of the tier above 2.2 m over the floor (2.5 m floor to floor).

| Pipes above the canopy | Onto the crops | Back into the pipes | Into the ceiling | Into the aisles | Light across the bed: lowest / highest, of the mean |
|---|---|---|---|---|---|
| 0.1 m | **99%** | 6.1% | 1.2% | 1.2% | 0.63 / 1.26 |
| 0.3 m | **99%** | 6.2% | 1.3% | 1.9% | 0.80 / 1.10 |
| 0.6 m | **98%** | 6.1% | 1.3% | 2.7% | 0.87 / 1.09 |
| 1 m | **97%** | 6.2% | 1.3% | 3.1% | 0.93 / 1.08 |

The tier is a white box whose main absorber is the crops, so nearly all the pipes' light ends up in them. Close pipes light the bed in stripes; ~0.6 m up the light across the bed is within ~15% of its mean, the dimmest at the bed's edges, where the aisles take some. The pipes can hang at a fixed height and the crops grow towards them.

| Aisle floor reflectance | Onto the crops |
|---|---|
| 20% | 98% |
| 50% | 99% |
| 90% | 100% |

## What moves it

Each input at its low and high, the rest as configured (rays: 80,000 a trace, so ±~0.5 point of noise).

| Input | Range | Status | Valley, lamp to floor | Farm, lamp to crops |
|---|---|---|---|---|
| `pipe_coupling` | 0.750 – 0.920 | guess | 47% – 57% | 53% – 65% |
| `film_loss_per_reflection` | 0.00500 – 0.0200 | estimate | 57% – 45% | 65% – 52% |
| `extractor_efficiency` | 0.750 – 0.950 | guess | 47% – 59% | 53% – 68% |
| `pipe_end_return` | 0.200 – 0.800 | guess | 53% – 53% | 60% – 61% |
| `pipe_albedo` | 0.600 – 0.900 | guess | 48% – 56% | 58% – 62% |
| `mgo_reflectance` | 0.900 – 0.980 | estimate | 51% – 54% | 60% – 61% |
| `diffuser_transmittance` | 0.450 – 0.750 | estimate | 48% – 57% | 60% – 60% |
| `diffuser_absorptance` | 0.0200 – 0.100 | estimate | 55% – 50% | 60% – 60% |
| `floor_albedo` | 0.0500 – 0.200 | estimate | 51% – 58% | 60% – 60% |
| `canopy_reflectance` | 0.0500 – 0.120 | estimate | 53% – 53% | 59% – 62% |
| `aisle_reflectance` | 0.200 – 0.900 | guess | 53% – 53% | 60% – 61% |
| `canopy_height_m` | 0.300 – 1.00 | estimate | 53% – 53% | 59% – 61% |

## What it would mean

The system model with the traced chain (valley 53%, farm 60%) in place of the assumed 75% and 85%: a six-stack at Eros, three tiers lit, and the assembled stack's radiative exchange (`habitat_model/cavity.py`, farm radiators outboard, 4,000 rays). People per tier don't change (the light on the crops sets them); everything that scales with the lamps does. The configured deliveries are left as they are until the chain's guesses are measured.

| Torus |  | Assumed | Traced | Change |
|---|---|---|---|---|
| 900 m | Valley sky, daily average | 52.6 MW | 74.5 MW | +42% |
| 900 m | Per farm tier lit | 32.1 MW | 45.1 MW | +41% |
| 900 m | Electricity and heat per torus, three tiers lit | 154 MW | 214 MW | +40% |
| 900 m | Despun array per torus at the site | 186 ha | 260 ha | +39% |
| 900 m | Radiators: best margin, all panels | 2.5× | 1.8× | -28% |
| 900 m | Radiator panels for 1.5×, per torus | 78.2 ha | 169 ha | +116% |
| 1.6 km | Valley sky, daily average | 166 MW | 236 MW | +42% |
| 1.6 km | Per farm tier lit | 101 MW | 142 MW | +41% |
| 1.6 km | Electricity and heat per torus, three tiers lit | 485 MW | 678 MW | +40% |
| 1.6 km | Despun array per torus at the site | 589 ha | 820 ha | +39% |
| 1.6 km | Radiators: best margin, all panels | 2.4× | 1.7× | -29% |
| 1.6 km | Radiator panels for 1.5×, per torus | 249 ha | 536 ha | +116% |

The radiators still reach 1.5× with every panel in place, but need about twice the panel area (on the 1.5× search's coverage grid): a panel's output falls as coverage rises and the panels shade each other, so ~40% more heat takes ~2× the panels.

Not modelled: the light box's ends and the cliffs' edges (a ~1 m deep box along a ~56 m wide valley loses a little at its sides), the pipes' ends and joints, the sulfur lamp's spectrum (PAR only), angular (not diffuse) scattering by real diffusers and prism film, dust and ageing, the canopy as a volume (leaves at many heights), the ceiling's grading brighter overhead (notes §13), and lamps placed straight in the light box without pipes (an option if the pipes' losses hold up: smaller lamps, ~1 kW, behind the diffuser).
