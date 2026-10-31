# Light pipes, light box and farm optics (plan §7)

How much of the sulfur lamps' light reaches the valley's floor and the farm's crops, and how evenly: the prism light pipes, the valley's magnesium-oxide light box with its diffuser, and a farm tier's pipes over the crops. It uses the system model's assumptions and, for what the delivery would change, its power, array and radiative exchange.

```bash
python -m optics_model                          # full report (reports/optics.md), ~1 min
python -m optics_model --set film_loss_per_reflection=0.005
```

| File | Contents |
|---|---|
| `pipe.py` | a prism light pipe fed from both ends: ray classes along the pipe, the film's loss, a graded extractor for an even glow, the far ends |
| `trace.py` | Monte Carlo ray tracing in a cross-section, periodic sideways: segments and circles, diffuse reflection and transmission |
| `architectures.py` | the same chain for other lighting architectures: shorter or heavier pipes, ~1 kW lamps straight in the light box, 915 MHz sector plants, LEDs (white throughout, or blue + red in the farm); bulb counts |
| `leds.py` | what a torus's LEDs take: die and wafer area, gallium, indium, arsenic, yttrium, ammonia against the source bodies; the fab step by step |
| `scenes.py` | the light box and a farm tier traced across the pipes; the pipe spacing from the lamps' power; the whole chain from lamp to floor and crops |
| `__main__.py` | the report |

## Model

- **The chain:** lamp into the pipe's acceptance cone (`pipe_coupling`), out of the pipe along its length, through the light box or the tier. "Delivered" is what the floor or the canopy absorbs over its absorptance: the light that, falling once, would be absorbed the same.
- **The pipe:** light within `pipe_cone_deg` of the axis, classes by angle and impact parameter, each reflecting tan θ / (2 √(R² − b²)) times a metre; per reflection the film absorbs `film_loss_per_reflection` and the extractor strip catches a share f(z), of which `extractor_efficiency` leaves the pipe. f(z) is solved for an even glow and the most light out (at most `extractor_max_frac`) on a 16 × 16 quadrature of the classes, then checked on 20,000 independently sampled classes (within ~±2%); the far end's reflector returns `pipe_end_return`.
- **The cross-sections:** long pipes make the scene uniform along them, so it is traced in the plane across them: diffuse rays in three dimensions, projected, which is exact for an endless scene. The scene repeats sideways (one pipe's width of ceiling; one bed and aisle). Every surface reflects and transmits diffusely and absorbs the rest; the pipes glow from their lower half (`pipe_emit_arc_deg`) and send back `pipe_albedo` of the light falling on them.
- **Layout:** the valley's pipes are spaced for the sky's peak power at `pipe_w_per_m`; the farm's are enough for a bed's peak over `farm_photoperiod_h`, rounded up. The power depends on the delivery and the delivery on the layout, so the two are iterated until they agree (`scenes.converged`).
- **Checks** (`tests/test_optics.py`): the pipe's light accounted for, its glow holding on independent rays, the quadrature against its distributions, a lossless pipe losing only at its ends, longer and lossier pipes losing more; Hottel's crossed strings for parallel strips; an ideal light box delivering everything; light conserved in the box and the tier; the diffuser blending the stripes; pipes higher above the canopy lighting it more evenly; the chain multiplying; the farm's pipes covering a bed's power, the converged layout carrying its own power.

## Findings

- **The light box works as proposed:** ~82% of the pipes' light reaches the floor (the notes' ~75–85%); the diffuser blends the stripes ~0.5 m below the pipes; the closer the pipes, the more of the returned light they take back (~87% at ~0.9 m apart, ~75% at 0.35 m).
- **A farm tier puts ~93% of the pipes' light on the crops** (~99% with four pipes a bed instead of seven), within ~15% across a bed with the pipes ~0.6 m above the canopy.
- **The pipes cost what the sizing left out:** ~85% into the pipe and ~72% out of a 40 m pipe (guesses). With the pipes laid out for the power that then needs (`scenes.converged`: ~0.6 m apart in the valley, seven over a farm bed), ~50% of the lamps' light reaches the valley and ~57% the crops, against the ~75% and ~85% assumed. If that holds: ~50% more lighting power and array, and ~2–3× the radiator panels for 1.5×. The configured deliveries are left as they are until a lamp on a pipe is measured (plan §8).
- **Lighting architectures** (`architectures.py`): pipes shorter (20 m) or more heavily loaded (600 W/m) recover part of the loss (~197 MW per 900 m torus at both); **~1 kW sulfur lamps straight in the light box, no pipes**, deliver ~81% / ~89% and need ~146 MW on small magnetrons, ~130 MW on 915 MHz sector plants (proposed), against ~228 MW for the pipes as now; LEDs ~66 MW white throughout, ~59 MW with blue + red in the farm. The lamps take ~4× as many bulbs, in the ceiling's service space.
- **LEDs from asteroid material** (`leds.py`, proposed): ~440 m² of epitaxial wafer per 900 m torus, ~200 kg of gallium, ~3 kg of indium (the red dies), ~60 kg of yttrium, each under 1% of the source bodies' content; the ~350 t of PV silicon they save is ~1,000× the finished dies' mass.
- **Not modelled:** the light box's ends and the cliffs' edges, the pipes' ends and joints, the spectrum, angular scattering by real diffusers and film, dust and ageing, the canopy as a volume, the ceiling's grading, the lamps' discreteness along a row, the waveguides' layout.
