# Light pipes, the light box, the farm's tiers and LEDs

Plan §7 (`optics_model/`): how much of the lamps' light reaches the valley's floor through its magnesium-oxide light box and diffuser, and the crops in a farm tier, and how evenly. The first sections trace the design first proposed, sulfur lamps feeding prism light pipes (sized at 1.40 µmol/J and an assumed 75% / 85%); the architectures that followed, and the LEDs now adopted (sized at 85% / 95%), come after. Most inputs are estimates or guesses (`reports/assumptions.md`).

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
| Assumed by the first sizing | 75% | 85% |

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

The system model with the traced chain (valley 50%, farm 57%) in place of the assumed 75% and 85%: a six-stack at Eros, three tiers lit, and the assembled stack's radiative exchange (`habitat_model/cavity.py`, farm radiators outboard, 4,000 rays). People per tier don't change (the light on the crops sets them); everything that scales with the lamps does. The pipes' guesses would need measuring; the LEDs, adopted since, avoid the pipes altogether (below).

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

## Lighting architectures

What the pipes cost and what could replace them (`optics_model/architectures.py`): the same chain, each layout sized for the power its own delivery needs, then the system model and the assembled stack's radiators (900 m six-stack at Eros, three tiers lit). Small magnetrons give 1.40 µmol/J; 915 MHz sector plants 1.75 µmol/J less 10.0% in waveguides (notes §13). Lamps straight in the light box: ~1 kW bulbs in reflectors that keep 88% of the light and send back 60% of what returns to them, in rows behind a 1.5 m deep diffuser, and ~0.8 m above the canopy in the farm.

| Architecture | To the floor | To the crops | µmol/J at the wall (valley / farm) | Electricity per torus | Array | Radiators' best margin | Panels for 1.5× | Bulbs |  |
|---|---|---|---|---|---|---|---|---|---|
| Pipes, 40 m at 300 W/m (as first proposed) | 50% | 57% | 1.40 | 228 MW | 276 ha | 1.7× | 169 ha | ~62.5 k | pairs of ~6 kW lamps, small magnetrons |
| Pipes, 20 m | 54% | 62% | 1.40 | 211 MW | 255 ha | 1.8× | 169 ha | ~115 k | pairs of ~3 kW lamps |
| Pipes at 600 W/m | 55% | 62% | 1.40 | 210 MW | 255 ha | 1.8× | 169 ha | ~28.6 k | pairs of ~12 kW lamps per 40 m pipe |
| Pipes, 20 m at 600 W/m | 59% | 66% | 1.40 | 197 MW | 239 ha | 1.9× | 137 ha | ~53.6 k | pairs of ~6 kW lamps per 20 m pipe |
| Pipes, 20 m at 600 W/m, 915 MHz plants | 59% | 66% | 1.57 | 175 MW | 213 ha | 2.2× | 110 ha | ~47.4 k | the same, fed by sector plants through waveguides |
| ~1 kW lamps in the light box | 81% | 89% | 1.40 | 146 MW | 177 ha | 2.6× | 78.2 ha | ~236 k | rows of lamps 1.5 m apart in reflectors, small magnetrons, a 1.5 m deep diffuser |
| ~1 kW lamps in the light box, 915 MHz plants | 81% | 89% | 1.57 | 130 MW | 158 ha | 2.9× | 78.2 ha | ~209 k | the same, fed by sector plants through waveguides |
| LEDs, white throughout | 86% | 96% | 3.00 | 65.7 MW | 80.6 ha | 5.7× | 39.1 ha | — | strips at 200 W/m, 3 µmol/J |
| LEDs, white in the valley, blue + red in the farm (adopted) | 86% | 96% | 3.00 / 3.60 | 59.1 MW | 70.9 ha | 5.8× | 39.1 ha | — | the farm at 3.6 µmol/J (magenta light, no phosphor) |

**Lamps straight in the light box beat every pipe**: ~36% less electricity than the pipes as first proposed, and more than that design's assumed ~75% / ~85% (they deliver more: no coupling into a pipe, nothing guided over tens of metres, and the reflectors take back less than rows of pipes). Shorter or more heavily loaded pipes recover part of the gap; 915 MHz plants ~11% of the power either way (their gain in efficacy, less the waveguides'). LEDs, adopted, need well under half again (below); the light box and the tiers are as traced for the pipes, with strips in place of pipes.

The price of lamps in the box: ~3.8× as many bulbs as the pipes' lamps, spread through the ceiling's service space and above each tier, with their heat shed there rather than at the hub (both reachable by the coolant loops, notes §13), and each one maintained from above the ceiling. Fed by sector plants, the sources stay few (~100 kW each) and only the electrodeless bulbs are many; with small magnetrons every bulb has one, ~10,000–20,000 hours each.

| Lamps in the box: input | Range | Electricity per torus |
|---|---|---|
| `luminaire_efficiency` | 0.80 – 0.93 | 160 – 138 MW |
| `luminaire_albedo` | 0.40 – 0.80 | 149 – 143 MW |

## LEDs from asteroid material

White LEDs in the valley (blue InGaN dies under YAG:Ce phosphor), blue + red over the crops (InGaN and 660 nm AlGaInP, 80% of the farm's power on red), at 3.00 and 3.60 µmol/J (`optics_model/leds.py`). Installed for the noon peak and the tiers while lit: 42.8 MW in the valley, 49.5 MW in the farm; at 0.30 W/mm² that is 176 m² of blue die and 132 m² of red, ~439 m² of epitaxial wafer at 70% yield (white throughout: 486 m²). Each lasts ~11.4 years in the valley, ~8.56 in the farm: ~10% replaced a year.

| Element (kg per torus) | White throughout | White + blue/red | In the source bodies | Share of it needed (white + blue/red) |
|---|---|---|---|---|
| Ga | 50 kg | 200 kg | ~231 t | 0.08% |
| In | 0.17 kg | 3.3 kg | ~0.459 t | 0.73% |
| As | — | 180 kg | ~61.1 t | 0.30% |
| Y | 130 kg | 56 kg | ~73.2 t | 0.08% |
| Ce | 4.3 kg | 1.8 kg | ~32.6 t | 0.01% |
| Al | 740 kg | 370 kg | plentiful | — |
| N | 10 kg | 5.2 kg | plentiful | — |

Gallium is fed at 25% utilization (the rest leaves in the exhaust, recoverable); the red dies' GaAs substrates, etched away, take most of it and all the arsenic. Indium is the tight one: grams in the blue wells, kilograms in the red layers (half their group III), against a few hundred kilograms in the source bodies at ~2–78 ppb, so it comes back from spent dies and the reactors' exhaust, and only the losses are new. Ammonia: ~25.1 t per torus's wafers (100 kg/m²), against ~8 kt of nitrogen recovered from the C-type, and mostly recoverable.

| Step | Needs | From | Status |
|---|---|---|---|
| Gallium | 6N–7N metal, kilograms | ~5–10 ppm in the rock, with the aluminium in the silicates and clays; a by-product of the leach line, then electrowinning and zone refining | ⚠ recovery at ~10 ppm |
| Indium | grams (blue) to kilograms (red AlGaInP) | ~2 ppb (S-type) to ~78 ppb (C-type): the scarcest input, from the leach line's zinc and copper streams | ⚠ / ✗ for red |
| Precursors | trimethylgallium, -indium, -aluminium; 7N ammonia; silane, Cp₂Mg; phosphine (red) | metals + methyl chloride (methanol + HCl, C-type carbon and chlorine); Haber–Bosch ammonia from the C-type's nitrogen; distillation to 6N | ✓ chemistry, ⚠ purity |
| Substrates | sapphire wafers (blue), GaAs (red) | 5N alumina from the silicates' plagioclase, Kyropoulos growth (~2,050 °C), sawn and polished; or GaN on silicon, from a semiconductor-silicon line (the one local PV would need) | ⚠ |
| Epitaxy | MOCVD reactors: steel chamber, SiC-coated graphite susceptor, ~1,050 °C, ~100 mbar | steel, carbon, silicon carbide: all local; the controls are electronics (vitamins) | ✓ |
| Patterning | ~5–7 mask layers at micron scale: contact or proximity lithography, no steppers | chromium-on-quartz masks, novolac resists (phenol, formaldehyde), chlorine plasma etching | ✓ |
| Contacts | p-contact and current spreading (ITO, or Ni/Ag), n-contact (Ti/Al) | ITO needs indium again: a thin nickel–silver or ZnO:Al instead; titanium, nickel, aluminium local | ⚠ |
| Phosphor (valley) | YAG:Ce, ~0.1–0.4 t per torus | yttrium ~2 ppm, cerium ~1 ppm: rare-earth separation by solvent extraction, at kilogram scale a lab process | ⚠ |
| Packaging | lead frames or chip-on-board, encapsulant, heat spreaders | copper or steel boards, phosphor in glass (local glass) instead of silicone, copper bond wire | ✓ |
| Drivers | constant-current converters, ~100 kW–1 MW per sector feeding long series strings | power transistors and diodes from the semiconductor works' silicon (or GaN from the LED reactors), film capacitors, ferrite and copper magnetics, analog or simple bipolar control | ✓ (a 1980s power-device process) |

**LEDs halve the semiconductor works' silicon.** The array is made at the host (notes §2, §13), by the works that can also make the LEDs and their drivers. Blue + red LEDs need 70.9 ha of array against 158 ha for sulfur lamps in the box (the fallback): ~349 t less wafer silicon per torus at 0.400 kg/m². Until a new site's works runs, importing the finished dies and phosphor instead costs ~338 kg per torus (dies thinned to 150 µm), and ~10% of that a year: ~1,030× less than the silicon saved, and still ~252× with 30 years of replacements. Making the dies locally is a small fab: one MOCVD reactor growing ~0.1 m² every ~5 h makes ~150 m² a year, so a torus's ~439 m² takes a few reactor-years, and micron-scale LEDs need none of a chip fab's steppers.

Not modelled: the light box's ends and the cliffs' edges (a ~1 m deep box along a ~56 m wide valley loses a little at its sides), the pipes' ends and joints, the sulfur lamp's spectrum (PAR only), angular (not diffuse) scattering by real diffusers and prism film, dust and ageing, the canopy as a volume (leaves at many heights), the ceiling's grading brighter overhead (notes §13), the lamps' discreteness along a row (traced as line sources), and the waveguides' layout.
