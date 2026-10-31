"""Heat rejection (plan §6): the farm radiators' layout and reach, capacity against stack length, sunlight on
the radiators, the coolant loops and the valley's day/night swing.

python -m thermal_model [--set name=value ...]
"""

import argparse
import math
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import coolant, layout, sunlight, valley

MW, HA = 1e6, 1e4
TARGET = 1.5            # margin sought in both sections when sizing panels
GRID = (0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.35, 0.5, 0.75, 1.0)
LAYOUT_CASES = (("900 m pair, 3 tiers", 900, 2, 3), ("900 m six, 2 tiers", 900, 6, 2),
                ("900 m six, 3 tiers", 900, 6, 3), ("1.6 km six, 3 tiers", 1600, 6, 3))
TILTS = (0.27, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0)
DAY_HOURS = 12


def label(r):
    return f"{r / 1000:g} km" if r >= 1000 else f"{r:g} m"


def layout_section(a, p, overrides):
    rows = layout.compare(p, LAYOUT_CASES, target=TARGET, grid=GRID)
    out, per_torus, coverages, inboard = [], {}, {}, {}
    for row in rows:
        case = next(c for c in LAYOUT_CASES if c[0] == row["label"])
        d = Design(radius_m=case[1], n_tori=case[2], tiers_lit=case[3])
        per_tier = evaluate(p, d)["power"]["farm_per_tier"] * case[2]
        least = row["least"]
        area = (f"{num(least['panel_area'][0] / HA)} / {num(least['panel_area'][1] / HA)}" if least
                else "**not reached**")
        if row["layout"] == "outboard":
            coverages[row["label"]] = layout.sizing_coverage(row)
            if least:
                per_torus[row["label"]] = [x / case[2] / HA for x in least["panel_area"]]
        passive = num(layout.passive_tiers(row, per_tier), 2) if row["layout"] == "inboard" else "—"
        if row["layout"] == "inboard":
            inboard[row["label"]] = (row["farm"], layout.passive_tiers(row, per_tier), least is not None)
        out.append([row["label"], row["layout"], f"{num(row['main'], 2)} / {num(row['farm'], 2)}",
                    f"{row['coverage'][0]:.0%} / {row['coverage'][1]:.0%}", area, passive])
    reach = []
    for lab, radius, n, tiers in (("900 m six, 3 tiers", 900, 6, 3), ("1.6 km six, 3 tiers", 1600, 6, 3),
                                  ("900 m six, 2 tiers", 900, 6, 2)):
        d = Design(radius_m=radius, n_tori=n, tiers_lit=tiers)
        reach.append([lab, *[num(x, 2) if (x := layout.reach_needed(a, d, t, overrides)) else "beyond 1.4"
                             for t in (1.0, TARGET)]])
    return per_torus, coverages, [
        "## The farm radiators: where, and how far out",
        "Heat flows from the farm rings at 0.4 r to their radiators. **Outboard** (the baseline, from the rings "
        "out to ~1 r), the warm coolant must sink against spin gravity: pumped loops. **Inboard** (from the hub "
        "to the rings), it rises: passive thermosiphons, as in the main section, but the radiators then sit in "
        "the space the farm rings enclose. The whole stack traced as one scene (`habitat_model/cavity.py`), "
        "both sections' panel coverages swept on a finer grid; best margins main / farm, and the least panel "
        f"area (one face, main / farm section) that keeps both at {TARGET:g}× (coverage in steps of 5%, so "
        "areas move in steps of ~25%).",
        table(["Stack, tiers lit", "Farm radiators", "Best margins, main / farm", "At coverage, main / farm",
               f"Least panels for {TARGET:g}× (ha), main / farm", "Tiers the passive set alone carries"], out),
        inboard_text(inboard),
        "**How far out the outboard radiators must reach** (× floor radius) for each margin, both sections:",
        table(["Stack, tiers lit", "Reach for 1×", f"Reach for {TARGET:g}×"], reach),
    ]


def inboard_text(inboard):
    """What the passive (inboard) farm radiators manage, from the six-stacks' rows."""
    six = {k: v for k, v in inboard.items() if "six" in k}
    worst = min(v[0] for v in six.values())
    tiers = min(v[1] for v in six.values())
    if all(v[2] for v in six.values()):
        return (f"**Inboard radiators cool a six-stack's farm passively, at {TARGET:g}× or better** (~{num(worst, 2)}× "
                "at worst): no pumps needed. Outboard radiators keep a wider margin.")
    if worst >= 1.0:
        return (f"**Inboard radiators cool a six-stack's farm passively, but below {TARGET:g}× in some cases** "
                f"(~{num(worst, 2)}× at worst, ~{num(tiers, 2)} tiers' heat): no pumps needed with all tiers lit, "
                "outboard pumped radiators for a full margin, the inboard set as their passive fallback.")
    return (f"**Inboard radiators can't cool a six-stack's farm** (~{num(worst, 2)}× at worst): the farm rings "
            "enclose them. Outboard, with pumps, is needed for all the tiers lit; the inboard set is a passive "
            f"fallback that keeps about {num(tiers, 1)} tiers lit if the pumps stop. A pair's farm cools passively.")


def capacity_section(p, per_torus):
    rows = []
    for radius in (900, 1600):
        rows.append([label(radius), *[str(layout.capacity(p, radius, t)) for t in range(4)]])
    area_rows = [[k, f"{num(v[0], 2)} ha", f"{num(v[1], 2)} ha"] for k, v in per_torus.items()]
    return [
        "## How many tori the radiators can cool",
        "Most tori (with their farm rings) the assembled stack can cool, farm radiators outboard to 1 r, by "
        "farm tiers lit (any margin above 1×; the search stops at 40, beyond passive stability's ~22–25):",
        table(["Torus", "0 tiers lit", "1 tier", "2 tiers", "3 tiers"], rows),
        f"Panels per torus at {TARGET:g}× (one face, outboard farm radiators). Finite panels that see each "
        "other, and the farm radiators shading the drum's farm end, need ~2–3× the black-body area "
        f"(`reports/thermal.md`). Areas at the grid's smallest coverage step ({GRID[1]:.0%}) are an upper "
        "bound: fewer panels may do.",
        table(["Stack, tiers lit", "Main section (valley)", "Farm section"], area_rows),
    ]


def sunlight_section(p, coverage, met):
    d = Design(radius_m=900, n_tori=6, tiers_lit=3)
    r = evaluate(p, d)
    g, h = r["geometry"], r["heat"]
    rows, onset = [], None
    for tilt in TILTS:
        a = sunlight.absorbed(g, d.n_tori, tilt, coverage, absorptivity=p.solar_absorptivity)
        if onset is None and a["main"] > 0:
            onset = tilt
        if tilt == 1.0:
            per_degree = a["farm"] / h["farm_stack"]
        rows.append([f"{tilt:g}°", f"{num(a['main'] / MW, 2)} MW ({a['main'] / h['main_stack']:.1%})",
                     f"{num(a['farm'] / MW, 2)} MW ({a['farm'] / h['farm_stack']:.1%})"])
    return [
        "## Sunlight on the radiators",
        "The axis points at the orbit's pole (notes §11), so sunlight arrives edge-on to the panels. A tilt "
        "lets it fall on one face of each, unless the tori (as true tori), the hub or the farm rings shade "
        "them. Sun rays marched through a 900 m six-stack (`thermal_model/sunlight.py`), panels at "
        f"{coverage[0]:.0%} / {coverage[1]:.0%} coverage (main / farm, "
        + (f"the least panels for {TARGET:g}×" if met else
           f"**{TARGET:g}× is out of reach here: the best achievable coverage**") + "), solar absorptivity "
        f"{p.solar_absorptivity:g} (white paint), at 1 AU; as a share of each section's heat (three tiers lit). "
        "0.27° is the Sun's own radius, the least tilt any panel sees.",
        table(["Axis tilt from the pole", "Main section (drum)", "Farm section (open)"], rows),
        f"The drum's panels see no direct sunlight below ~{onset:g}° of tilt: the tori shade them, through "
        f"the ends and through the gaps alike. The open farm section takes ~{per_degree:.1%} of its heat per "
        "degree of tilt at 1 AU, up to ×1.5–1.8 at the nearest candidates' perihelia and ×2 as the paint ages "
        "towards ~0.3: **a few degrees cost a few percent**, so the axis needs holding only roughly (within "
        "~1–2°), trimmed as the orbit plane drifts over centuries.",
    ]


def coolant_section(p):
    rows, two_phase, first = [], [], None
    for radius in (900, 1600):
        d = Design(radius_m=radius, n_tori=6, tiers_lit=3)
        r = evaluate(p, d)
        g, h = r["geometry"], r["heat"]
        omega = g["omega"]
        source = g["radius"] - g["tube_radius"]
        sink = coolant.annulus_centroid(g["radiator_inner"], g["drum_radius"])
        nat = coolant.size_natural(h["main_per_torus"], omega, source, sink, p.coolant_dt_k,
                                   p.coolant_loops_per_torus)
        ring = g["farm_radius"] + g["farm_height"] / 2
        farm_sink = coolant.annulus_centroid(g["farm_radius"] + g["farm_height"], g["farm_radiator_outer"])
        pump = coolant.size_pumped(h["farm_per_ring"], omega, ring, farm_sink, p.coolant_dt_k,
                                   p.coolant_loops_per_torus, pump_efficiency=p.pump_efficiency)
        rows.append([label(radius), f"{num(h['main_per_torus'] / MW)} MW", f"{num(nat['diameter'], 2)} m",
                     f"{num(nat['speed'], 2)} m/s", f"{num(nat['head'] / 1e3, 2)} kPa",
                     f"{num(nat['inventory'] / 1e6, 2)} kt",
                     f"{num(h['farm_per_ring'] / MW)} MW", f"{num(pump['diameter'], 2)} m",
                     f"{num(pump['pump_power'] / 1e3)} kW ({pump['pump_power'] / h['farm_per_ring']:.2%})"])
        if first is None:
            first = (nat, pump, h, r["mass"]["water_needed"])
        for name, rho, sat in (("ammonia", coolant.AMMONIA["rho_l"], coolant.AMMONIA),
                               ("water", coolant.WATER["rho"], coolant.WATER_SAT)):
            x = coolant.two_phase_rim(omega, source, sink, rho, sat)
            two_phase.append([label(radius), name, f"{num(sat['p_sat'] / 1e3)} kPa",
                              f"{num(x['pressure'] / 1e6, 2)} MPa", f"{num(x['t_sat'] - 273.15)} °C"])
    return [
        "## Coolant loops",
        f"Single-phase water, {p.coolant_dt_k:g} K warmer leaving the heat source, "
        f"{p.coolant_loops_per_torus:g} loops per torus or farm ring (`thermal_model/coolant.py`). Main "
        "section: natural circulation from the rim to the radiators' centroid, pipes sized so that friction "
        "uses up the buoyancy head (out and back, radiators' own tubes not counted). Farm section, radiators "
        "outboard: pumped at 2 m/s, the pump also working against the buoyancy that resists the warm coolant "
        "sinking. Per torus or farm ring, six-stacks with three tiers lit.",
        table(["Torus", "Valley's heat", "Pipe (each loop)", "Speed", "Buoyancy head", "Water in the loops",
               "Farm ring's heat", "Pipe (each loop)", "Pumping"], rows),
        "**Main section: passive, as intended.** A few tenths of a kPa per kelvin of buoyancy, over hundreds of "
        f"metres of spin gravity, drive ~{num(first[0]['diameter'], 1)} m pipes at under 1 m/s; the loops hold "
        f"~{num(first[0]['inventory'] / 1e6, 1)} kt of water per 900 m torus (~{first[0]['inventory'] / first[3]:.1%} "
        f"of its water budget, local). **Farm section: pumps** of ~{first[1]['pump_power'] / first[2]['farm_per_ring']:.1%} of its heat.",
        "**Two-phase loops need throttling.** An evaporating loop (ammonia, as on the ISS) would carry the heat "
        "in far smaller pipes, but the liquid returning outward from the radiators builds a column of "
        "hundreds of metres of near-1 g head: at the rim it is far above its saturation pressure and can't "
        "boil at the valley's temperature unless throttled (or run through a turbine) just before the "
        "evaporator.",
        table(["Torus", "Fluid", "Saturation pressure at 285 K", "Liquid pressure at the rim", "Boils at"],
              two_phase),
    ]


def valley_section(p):
    d = Design(radius_m=900, n_tori=2, tiers_lit=1)
    g = evaluate(p, d)["geometry"]
    height = g["volume"] / g["floor_area"]
    light = valley.light_on_floor(p, DAY_HOURS)
    air_c = valley.air_heat_capacity(p)
    rows = []
    for name, case in valley.CASES.items():
        s = [valley.swing(case, light, DAY_HOURS, u, height, air_c) for u in (3, p.valley_cooling_u, 15)]
        rows.append([name, f"{num(s[0]['capacity'] / 1e3)} kJ/m²K", f"{num(s[0]['effusivity'])}",
                     *[f"{num(x['swing'], 2)} K" for x in s]])
    return [
        "## The valley's day and night",
        f"Steady-periodic swing of a 900 m valley under a {DAY_HOURS} h day "
        f"(`thermal_model/valley.py`): the sky's {num(p.valley_light_mol)} mol/m² of light, ~{num(light)} W/m² "
        "while lit, all ending as heat in the valley; the air "
        f"(~{num(height)} m of it per m² of floor, {num(air_c)} J/m³K at {num(p.pressure_kpa)} kPa), the vegetation's water and the ponds as heat capacity; the soil "
        "as a semi-infinite conductor (its daily swing reaches ~10–13 cm); the cooling taking heat out at U "
        "towards a coolant at a fixed temperature (the cold ceiling's radiation and the air handling). "
        "Peak-to-peak, at three couplings:",
        table(["Valley", "Capacity (air, plants, ponds)", "Soil effusivity (W s½/m²K)", "U = 3 W/m²K",
               f"U = {p.valley_cooling_u:g} (baseline)", "U = 15"], rows),
        "Left to itself the valley swings a few kelvin: the soil's admittance (~5–17 W/m²K at a daily "
        "period) and the ponds hold it, so a wet valley stays within ~2–4 K and a dry canyon ~4–11 K. Wider "
        "swings (the notes' ~15 °C canyon) need the cooling scheduled: more at night through the cold "
        "ceiling, less by day.",
    ]


def report(a, overrides=None):
    p = params(a, **(overrides or {}))
    per_torus, coverages, lay = layout_section(a, p, overrides)
    parts = [
        "# Heat rejection: radiator layout, sunlight, coolant loops and the valley's swing",
        "Plan §6 (`thermal_model/`), building on the assembled radiative exchange of `habitat_model/cavity.py` "
        "(`reports/thermal.md`): radiators at ~285 K, emissivity ~0.9.",
        *lay,
        *capacity_section(p, per_torus),
        *sunlight_section(p, *coverages["900 m six, 3 tiers"]),
        *coolant_section(p),
        *valley_section(p),
        "Not modelled: the spokes and cables in the ray tracing, the envelopes' rounded inner faces, the "
        "radiators' own tubes and their pressure, freezing in cold panels when the load drops, sunlight "
        "reflected between panels, the despun array's shadow, and the valley's air movement.",
    ]
    return "\n\n".join(parts) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m thermal_model", description=__doc__)
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    print(report(load(), dict(args.set)), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
