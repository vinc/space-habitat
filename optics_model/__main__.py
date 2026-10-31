"""Light pipes, the valley's light box and the farm's tiers (plan §7): how much of the lamps' light reaches
the floor and the crops, and how evenly.

python -m optics_model [--set name=value ...]
"""

import argparse
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from thermal_model import layout

from . import architectures, leds, pipe, scenes

N = 200_000          # rays for the main traces
N_SWEEP = 80_000     # rays for the sweeps (stripes resolved to ~±3%)
SWEPT = ("pipe_coupling", "film_loss_per_reflection", "extractor_efficiency", "pipe_end_return", "pipe_albedo",
         "mgo_reflectance", "diffuser_transmittance", "diffuser_absorptance", "floor_albedo",
         "canopy_reflectance", "aisle_reflectance", "canopy_height_m")
PIPE_INPUTS = {"film_loss_per_reflection", "extractor_efficiency", "pipe_end_return"}


def pct(x, sig=2):
    return f"{num(100 * x, sig)}%"


def chain_section(p, d, first):
    pr, box, tier = d["pipe"], d["box"], d["tier"]
    rows = [
        ["Layout: valley pipes apart / farm pipes over each bed", f"{num(box['pitch'], 2)} m", f"{tier['pipes']}"],
        ["Lamp into the pipe, inside its acceptance cone (`pipe_coupling`)", pct(p.pipe_coupling),
         pct(p.pipe_coupling)],
        [f"Out of the pipe along its length ({p.pipe_length_m:g} m, fed from both ends)", pct(pr["efficiency"]),
         pct(pr["efficiency"])],
        ["Through the light box to the floor / onto the crops", pct(box["delivered"]), pct(tier["delivered"])],
        ["**Lamp to floor / crops**", f"**{pct(d['valley'])}**", f"**{pct(d['farm'])}**"],
        [f"… with the layout sized for the assumed deliveries ({num(first['box']['pitch'], 2)} m, "
         f"{first['tier']['pipes']} a bed)", pct(first["valley"]), pct(first["farm"])],
        ["Assumed until now (`ceiling_delivery`, `farm_delivery`)", pct(p.ceiling_delivery), pct(p.farm_delivery)],
    ]
    return [
        "## From lamp to leaf",
        "The share of the sulfur lamps' light that reaches the valley's floor and the farm's crops, step by "
        "step. \"Delivered\" counts what the floor or the canopy absorbs, divided by its absorptance: the light "
        "that, falling once, would be absorbed the same, which is how the sizing's daily light integrals are "
        "meant. The pipes are laid out for the power the traced delivery itself needs at "
        f"{p.pipe_w_per_m:g} W a metre of pipe (valley: spaced for the sky's peak; farm: enough pipes for a "
        "bed's peak, rounded up), traced again until the two agree: more power means pipes closer together, "
        "which take back more of the light (`scenes.converged`).",
        table(["Step", "Valley", "Farm"], rows),
        f"The light box and the tiers do as well as the notes expected, or better: ~{pct(box['delivered'])} of "
        f"the pipes' light reaches the valley's floor (the notes: ~75–85%), ~{pct(tier['delivered'])} the crops "
        "(more with the pipes farther apart, below). "
        "But the notes' figures counted only the ceiling: getting the lamps' light into the pipes and out "
        f"along them costs another ~{pct(1 - d['lamp_to_pipe_out'])}, which the sizing left out. Most of the "
        "chain's inputs are guesses (the coupling, the film's loss, the extractor); they need measuring on "
        "real pipes and lamps (plan §8). If the lamps' efficacy (~1.4 µmol/J) was measured out of their own "
        "reflector, part of the coupling is already in it.",
    ]


def pipe_section(p):
    rows = []
    for length in (20, 40, 80):
        for loss in (0.005, 0.01, 0.02):
            r = pipe.design(length, p.pipe_diameter_m, p.pipe_cone_deg, loss, p.extractor_efficiency,
                            p.pipe_end_return, p.extractor_max_frac)
            rows.append([f"{length} m", pct(loss, 2), f"**{pct(r['efficiency'])}**", pct(r["film"]),
                         pct(r["extractor"]), pct(r["ends"]),
                         f"{num(100 * (r['uniformity'] - 1), 2)}% / +{num(100 * (r['peak'] - 1), 2)}%"])
    return [
        "## The light pipe",
        f"A {p.pipe_diameter_m * 100:g} cm prism light pipe fed by a lamp at each end (`optics_model/pipe.py`). "
        f"Light enters within ~{p.pipe_cone_deg:g}° of the axis and travels by total internal reflection; ray "
        "classes by angle and skewness each reflect tan θ / (2 √(R² − b²)) times a metre. A white extractor "
        f"strip inside, graded along the pipe for an even glow (at most {p.extractor_max_frac:.0%} of "
        f"reflections), scatters the light out; {p.extractor_efficiency:.0%} of what it scatters leaves the "
        f"pipe. Light reaching the far end enters the other lamp's reflector, which returns "
        f"{p.pipe_end_return:.0%}. The extractor is graded on a 16 × 16 quadrature of the classes; the figures "
        "below are that profile checked on 20,000 classes sampled independently.",
        table(["Pipe length", "Film loss per reflection", "Light out", "Absorbed by the film", "By the extractor",
               "At the far ends", "Glow along the pipe: dimmest / brightest, from the mean"], rows),
        "Long pipes and lossy film compound: each ray reflects ~1–3 times a metre. Shorter pipes (more, smaller "
        "lamps) or better film recover some of it.",
    ]


def box_section(p, d):
    rows = []
    q = d["params"]
    base_pitch = d["box"]["pitch"]
    for pitch in (0.35, 0.5, base_pitch, 1.5):
        r = scenes.light_box(p, pitch=pitch, n=N_SWEEP)
        a = r["absorbed"]
        rows.append([f"{num(pitch, 2)} m" + (" (sized)" if pitch == base_pitch else ""), f"**{pct(r['delivered'])}**",
                     pct(a["pipe"]), pct(a["top"]), pct(a["diffuser"]), f"{num(r['glow_ratio'], 3)}"])
    gaps = []
    for gap in (0.1, 0.25, 0.5, 0.75, 1.0):
        r = scenes.light_box(p, pitch=base_pitch, gap=gap, n=N_SWEEP)
        gaps.append([f"{gap:g} m", pct(r["delivered"]), f"{num(r['glow_ratio'], 3)}"])
    return [
        "## The light box",
        f"One pipe's width of ceiling, repeating (`optics_model/scenes.py`): the magnesium-oxide top "
        f"({p.mgo_reflectance:.0%}), the pipe glowing from its lower half, a diffuser "
        f"{p.diffuser_gap_m:g} m below it ({p.diffuser_transmittance:.0%} transmitted, "
        f"{1 - p.diffuser_transmittance - p.diffuser_absorptance:.0%} reflected, "
        f"{p.diffuser_absorptance:.0%} absorbed, all diffusely), and the floor ({p.floor_albedo:.0%} "
        "reflected). Traced across the pipes (`optics_model/trace.py`): diffuse rays in three dimensions, "
        "projected on the cross-section, which is exact for pipes long against their spacing. At the sky's "
        f"peak ({num(scenes.valley_peak_w_m2(q))} W/m² over a {p.valley_day_h:g} h day, at the traced delivery) and "
        f"{p.pipe_w_per_m:g} W a metre of pipe, the pipes sit {num(base_pitch, 2)} m apart.",
        table(["Pipe spacing", "To the floor", "Back into the pipes", "Into the top", "Into the diffuser",
               "Stripes on the diffuser (brightest / dimmest)"], rows),
        "The diffuser sends back ~a third of the light; the box returns it, so what matters is what absorbs on "
        "the way. The pipes themselves take the most: light falling back on them is partly lost inside, so "
        "pipes packed side by side (as the notes had them) lose more than pipes ~1 m apart; the power the "
        "traced delivery needs packs them closer than the assumed one did.",
        table(["Diffuser below the pipes", "To the floor", "Stripes (brightest / dimmest)"], gaps),
        "The stripes fade by ~0.5 m (one to two pipe widths, as the notes proposed); the ratios here are "
        "within the tracing's noise (~±3–5%) beyond it.",
    ]


def farm_section(p, d):
    rows = []
    q = d["params"]
    pipes = d["tier"]["pipes"]
    for gap in (0.1, 0.3, 0.6, 1.0):
        r = scenes.farm_tier(p, pipe_gap=gap, pipes=pipes, n=N_SWEEP)
        a = r["absorbed"]
        rows.append([f"{gap:g} m", f"**{pct(r['delivered'])}**", pct(a["pipe"]), pct(a["ceiling"]), pct(a["aisle"]),
                     f"{num(r['uniformity'], 2)} / {num(r['peak'], 3)}"])
    aisles = []
    for ar in (0.2, 0.5, 0.9):
        r = scenes.farm_tier(p, pipes=pipes, aisle_reflectance=ar, n=N_SWEEP)
        aisles.append([pct(ar), pct(r["delivered"])])
    counts = []
    for k in sorted({max(1, pipes - 3), pipes - 1, pipes}):
        r = scenes.farm_tier(p, pipes=k, n=N_SWEEP)
        counts.append([f"{k}" + (" (sized)" if k == pipes else ""), f"{num(p.bed_width_m / k, 2)} m",
                       f"{num(k * p.pipe_w_per_m / p.bed_width_m)} W/m²", pct(r["delivered"]),
                       pct(r["absorbed"]["pipe"])])
    return [
        "## A farm tier",
        f"One bed ({p.bed_width_m:g} m) and one aisle ({p.aisle_width_m:g} m), repeating around the ring: the "
        f"canopy as a block {p.canopy_height_m:g} m tall ({p.canopy_reflectance:.0%} reflected), {pipes} pipes "
        f"over each bed ({num(p.bed_width_m / pipes, 2)} m apart, for {num(scenes.farm_peak_w_m2(q))} W/m² "
        f"over a {p.farm_photoperiod_h:g} h photoperiod), the white underside of the tier above "
        f"{p.tier_clear_m:g} m over the floor (2.5 m floor to floor).",
        table(["Pipes above the canopy", "Onto the crops", "Back into the pipes", "Into the ceiling",
               "Into the aisles", "Light across the bed: lowest / highest, of the mean"], rows),
        "The tier is a white box whose main absorber is the crops, so nearly all the pipes' light ends up in "
        "them. Close pipes light the bed in stripes; ~0.6 m up the light across the bed is within ~15% of its "
        "mean, the dimmest at the bed's edges, where the aisles take some. The pipes can hang at a fixed "
        "height and the crops grow towards them.",
        table(["Aisle floor reflectance", "Onto the crops"], aisles),
        f"The bed needs {num(scenes.farm_peak_w_m2(q))} W/m² at the traced delivery, so {pipes} pipes of "
        f"{p.pipe_diameter_m * 100:g} cm crowd a {p.bed_width_m:g} m bed and take "
        "back more of the light; fewer pipes, each loaded more, would leave more for the crops (each pipe "
        f"at {p.pipe_w_per_m:g} W/m and above, as the lamps allow):",
        table(["Pipes per bed", "Apart", "Lamp power at 300 W/m, per m² of bed", "Onto the crops",
               "Back into the pipes"], counts),
    ]


def sensitivity_section(p, base):
    rows = []
    pitch, pipes = base["box"]["pitch"], base["tier"]["pipes"]
    pipe_cache = {}
    for name in SWEPT:
        a = load()[name]
        cells = []
        for v in (a.low, a.high):
            q = params(load(), **{**vars(p), name: v})
            if name in PIPE_INPUTS:
                pr = pipe_cache.setdefault((name, v), pipe.efficiency(q))
            else:
                pr = base["pipe"]
            optical = name not in PIPE_INPUTS | {"pipe_coupling"}
            box = scenes.light_box(q, pitch=pitch, n=N_SWEEP) if optical else base["box"]
            tier = scenes.farm_tier(q, pipes=pipes, n=N_SWEEP) if optical else base["tier"]
            d = scenes.delivery(q, pipe_result=pr, box=box, tier=tier)
            cells.append(d)
        rows.append([f"`{name}`", f"{num(a.low, 3)} – {num(a.high, 3)}", a.status,
                     f"{pct(cells[0]['valley'])} – {pct(cells[1]['valley'])}",
                     f"{pct(cells[0]['farm'])} – {pct(cells[1]['farm'])}"])
    return [
        "## What moves it",
        "Each input at its low and high, the rest as configured and the layout held as converged (rays: "
        f"{N_SWEEP:,} a trace, so ±~0.5 point of noise).",
        table(["Input", "Range", "Status", "Valley, lamp to floor", "Farm, lamp to crops"], rows),
    ]


def impact_section(p, d):
    rows = []
    traced = d["params"]
    for radius, name in ((900, "900 m"), (1600, "1.6 km")):
        des = Design(radius_m=radius, n_tori=6, tiers_lit=3, host_class="LL", site="Eros", c_partner="Ryugu")
        before, after = evaluate(p, des), evaluate(traced, des)
        for label, get, unit, scale in (
            ("Valley sky, daily average", lambda r: r["power"]["valley_sky"], "MW", 1e6),
            ("Per farm tier lit", lambda r: r["power"]["farm_per_tier"], "MW", 1e6),
            ("Electricity and heat per torus, three tiers lit", lambda r: r["power"]["total"], "MW", 1e6),
            ("Despun array per torus at the site", lambda r: r["power"]["array_site"], "ha", 1e4),
        ):
            x, y = get(before), get(after)
            rows.append([name, label, f"{num(x / scale)} {unit}", f"{num(y / scale)} {unit}", f"{(y / x - 1) * 100:+.0f}%"])
        # The assembled radiative exchange (plan §6): best margin with every panel, and the least panels for 1.5×.
        checks = [layout._check(q, des, "outboard", 4000) for q in (p, traced)]
        margins = [c["margin"] for c in checks]
        least = [layout.smallest(c["points"], 1.5) for c in checks]
        rows.append([name, "Radiators: best margin, all panels", f"{num(margins[0], 2)}×", f"{num(margins[1], 2)}×",
                     f"{(margins[1] / margins[0] - 1) * 100:+.0f}%"])
        areas = [sum(x["panel_area"]) / des.n_tori / 1e4 if x else None for x in least]
        rows.append([name, "Radiator panels for 1.5×, per torus", f"{num(areas[0])} ha",
                     f"{num(areas[1])} ha" if areas[1] else "out of reach",
                     f"{(areas[1] / areas[0] - 1) * 100:+.0f}%" if areas[1] else "—"])
    return [
        "## What it would mean",
        f"The system model with the traced chain (valley {pct(d['valley'])}, farm {pct(d['farm'])}) in place of "
        f"the assumed {pct(p.ceiling_delivery)} and {pct(p.farm_delivery)}: a six-stack at Eros, three tiers lit, "
        "and the assembled stack's radiative exchange (`habitat_model/cavity.py`, farm radiators outboard, "
        "4,000 rays). People per tier don't change (the light on the crops sets them); everything that scales "
        "with the lamps does. The configured deliveries are left as they are until the chain's guesses are "
        "measured.",
        table(["Torus", "", "Assumed", "Traced", "Change"], rows),
        "The radiators still reach 1.5× with every panel in place, but need about twice the panel area or "
        "more (on the 1.5× search's coverage grid): a panel's output falls as coverage rises and the panels "
        "shade each other, so the extra heat costs more than its share of panels.",
    ]


def architecture_section(p):
    rows, results = [], {}
    for name, over, pipe_eff, what in architectures.options(p):
        d, q = architectures.evaluate_option(p, over, pipe_eff)
        des, r = architectures.system(q)
        check = layout._check(q, des, "outboard", 4000)
        least = layout.smallest(check["points"], 1.5)
        installed, count = architectures.bulbs(p, q, r, over)
        results[name] = (d, q, r, count)
        rows.append([name, pct(d["valley"]), pct(d["farm"]), f"{num(q.lamp_efficacy_umol_j, 3)}",
                     f"{num(r['power']['total'] / 1e6)} MW", f"{num(r['power']['array_site'] / 1e4)} ha",
                     f"{num(check['margin'], 2)}×",
                     f"{num(sum(least['panel_area']) / des.n_tori / 1e4)} ha" if least else "out of reach",
                     f"~{num(count / 1e3)} k" if count else "—", what])
    sens = []
    lamp_name = architectures.options(p)[5]
    for name in ("luminaire_efficiency", "luminaire_albedo"):
        a = load()[name]
        cells = []
        for v in (a.low, a.high):
            q0 = params(load(), **{**vars(p), name: v})
            opt = [o for o in architectures.options(q0) if o[0] == lamp_name[0]][0]
            d, q = architectures.evaluate_option(q0, opt[1], opt[2])
            cells.append(architectures.system(q)[1]["power"]["total"] / 1e6)
        sens.append([f"`{name}`", f"{num(a.low, 2)} – {num(a.high, 2)}", f"{num(cells[0])} – {num(cells[1])} MW"])
    names = [o[0] for o in architectures.options(p)]
    base = results[names[0]][2]["power"]["total"]
    lamps = results[lamp_name[0]][2]["power"]["total"]
    sector_gain = 1 - results[names[6]][2]["power"]["total"] / lamps
    bulb_ratio = results[lamp_name[0]][3] / results[names[0]][3]
    return results, [
        "## Lighting architectures",
        "What the pipes cost and what could replace them (`optics_model/architectures.py`): the same chain, "
        "each layout sized for the power its own delivery needs, then the system model and the assembled "
        "stack's radiators (900 m six-stack at Eros, three tiers lit). Small magnetrons give "
        f"{num(p.lamp_efficacy_umol_j, 3)} µmol/J (the configured value); 915 MHz sector plants "
        f"{num(p.sector_efficacy_umol_j, 3)} µmol/J less {pct(1 - p.waveguide_efficiency)} in waveguides "
        "(notes §13). Lamps straight in the light box: ~1 kW bulbs in reflectors that keep "
        f"{pct(p.luminaire_efficiency)} of the light and send back {pct(p.luminaire_albedo)} of what returns to "
        "them, in rows behind a 1.5 m deep diffuser, and ~0.8 m above the canopy in the farm.",
        table(["Architecture", "To the floor", "To the crops", "µmol/J at the wall", "Electricity per torus",
               "Array", "Radiators' best margin", "Panels for 1.5×", "Bulbs", ""], rows),
        f"**Lamps straight in the light box beat every pipe**: ~{pct((base - lamps) / base)} less electricity than "
        "the pipes as now, and a little less than the sizing's assumed ~75% / ~85% (they deliver more: no "
        "coupling into a pipe, nothing guided over tens of metres, and the reflectors take back less than "
        "rows of pipes). Shorter or more heavily loaded pipes recover part of the gap; 915 MHz plants "
        f"~{pct(sector_gain)} of the power either way (their gain in efficacy, less the waveguides'). LEDs need well under half again (below).",
        f"The price of lamps in the box: ~{num(bulb_ratio, 2)}× as many bulbs as the pipes' lamps, spread through the ceiling's service space and "
        "above each tier, with their heat shed there rather than at the hub (both reachable by the coolant "
        "loops, notes §13), and each one maintained from above the ceiling. Fed by sector plants, the sources "
        "stay few (~100 kW each) and only the electrodeless bulbs are many; with small magnetrons every bulb "
        "has one, ~10,000–20,000 hours each.",
        table(["Lamps in the box: input", "Range", "Electricity per torus"], sens),
    ]


def led_section(p, results):
    names = [o[0] for o in architectures.options(p)]
    lamps, white, mixed = (results[n] for n in (names[6], names[7], names[8]))
    rows, budgets = [], {}
    for name, (_, q, r, _) in ((names[7], white), (names[8], mixed)):
        b = leds.budget(q, r)
        budgets[name] = (b, r)
    els = ("Ga", "In", "As", "Y", "Ce", "Al", "N")
    for el in els:
        cells = []
        for name in (names[7], names[8]):
            b, r = budgets[name]
            cells.append(f"{num(b['use'].get(el, 0.0), 2)} kg" if b["use"].get(el, 0.0) else "—")
        c = leds.contained(mixed[2], el) if el in leds.EXTRA_PPM or el in ("Ga",) else None
        need = budgets[names[8]][0]["use"].get(el, 0.0)
        rows.append([el, *cells, f"~{num(c / 1e3)} t" if c else "plentiful",
                     f"{need / c:.2%}" if c and need else "—"])
    b, r = budgets[names[8]]
    bw, _ = budgets[names[7]]
    silicon = (lamps[2]["power"]["array_site"] - r["power"]["array_site"]) * p.pv_silicon_kg_m2
    wafers = sum(b["wafer_m2"].values())
    chain = [list(c) for c in leds.CHAIN]
    return [
        "## LEDs from asteroid material",
        "White LEDs in the valley (blue InGaN dies under YAG:Ce phosphor), blue + red over the crops (InGaN "
        f"and 660 nm AlGaInP, {pct(p.led_farm_red_share)} of the farm's power on red), at "
        f"{num(p.led_efficacy_umol_j, 3)} and {num(p.led_farm_efficacy_umol_j, 3)} µmol/J "
        "(`optics_model/leds.py`). Installed for the noon peak and the tiers while lit: "
        f"{num(b['valley_w'] / 1e6)} MW in the valley, {num(b['farm_w'] / 1e6)} MW in the farm; at "
        f"{num(p.led_die_w_mm2, 2)} W/mm² that is {num(b['die_m2']['blue'])} m² of blue die and "
        f"{num(b['die_m2']['red'])} m² of red, ~{num(wafers)} m² of epitaxial wafer at "
        f"{pct(p.led_wafer_yield)} yield (white throughout: {num(sum(bw['wafer_m2'].values()))} m²). Each lasts "
        f"~{num(b['life_yr']['valley'])} years in the valley, ~{num(b['life_yr']['farm'])} in the farm: "
        f"~{pct(b['replaced_per_yr'])} replaced a year.",
        table(["Element (kg per torus)", "White throughout", "White + blue/red", "In the source bodies",
               "Share of it needed (white + blue/red)"], rows),
        f"Gallium is fed at {pct(p.mocvd_utilization)} utilization (the rest leaves in the exhaust, "
        "recoverable); the red dies' GaAs substrates, etched away, take most of it and all the arsenic. "
        "Indium is the tight one: grams in the blue wells, kilograms in the red layers (half their group III), "
        "against a few hundred kilograms in the source bodies at ~2–78 ppb, so it comes back from spent dies and "
        "the reactors' exhaust, and only the losses are new. Ammonia: "
        f"~{num(b['ammonia'] / 1e3)} t per torus's wafers ({num(p.mocvd_ammonia_kg_m2)} kg/m²), against "
        "~8 kt of nitrogen recovered from the C-type, and mostly recoverable.",
        table(["Step", "Needs", "From", "Status"], chain),
        f"**The trade against the array's silicon.** Blue + red LEDs need {num(r['power']['array_site'] / 1e4)} ha "
        f"of array against {num(lamps[2]['power']['array_site'] / 1e4)} ha for the proposed sulfur lamps in the "
        f"box: ~{num(silicon / 1e3)} t less imported silicon per torus at {num(p.pv_silicon_kg_m2)} kg/m². "
        f"Importing the finished dies and phosphor instead costs ~{num(b['dies_imported'])} kg per torus "
        f"(dies thinned to {num(leds.DIE_THINNED_M * 1e6)} µm), and ~{pct(b['replaced_per_yr'])} of that a year: "
        f"~{num(silicon / b['dies_imported'])}× less than the silicon saved, and still "
        f"~{num(silicon / (b['dies_imported'] * (1 + 30 * b['replaced_per_yr'])))}× with 30 years of "
        "replacements. Making the dies locally is a small fab: one MOCVD reactor growing ~0.1 m² "
        f"every ~5 h makes ~150 m² a year, so a torus's ~{num(wafers)} m² takes a few reactor-years, and "
        "micron-scale LEDs need none of a chip fab's steppers. What stays imported is the drivers' "
        "electronics, the same vitamin as the rest of the habitat's.",
    ]


def report(p):
    first = scenes.delivery(p, n=N)
    d = scenes.converged(p, n=N, pipe_result=first["pipe"])
    results, arch = architecture_section(p)
    parts = [
        "# Light pipes, the light box and the farm's tiers",
        "Plan §7 (`optics_model/`): how much of the sulfur lamps' light the prism light pipes carry, the "
        "valley's magnesium-oxide light box and diffuser pass to the floor, and a farm tier's pipes put on the "
        "crops, and how evenly. Most inputs are estimates or guesses (`reports/assumptions.md`).",
        *chain_section(p, d, first),
        *pipe_section(p),
        *box_section(p, d),
        *farm_section(p, d),
        *sensitivity_section(p, d),
        *impact_section(p, d),
        *arch,
        *led_section(p, results),
        "Not modelled: the light box's ends and the cliffs' edges (a ~1 m deep box along a ~56 m wide valley "
        "loses a little at its sides), the pipes' ends and joints, the sulfur lamp's spectrum (PAR only), "
        "angular (not diffuse) scattering by real diffusers and prism film, dust and ageing, the canopy as a "
        "volume (leaves at many heights), the ceiling's grading brighter overhead (notes §13), the lamps' discreteness along a "
        "row (traced as line sources), and the waveguides' layout.",
    ]
    return "\n\n".join(parts) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m optics_model", description=__doc__)
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    print(report(params(load(), **dict(args.set))), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
