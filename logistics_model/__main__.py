"""Replication logistics (plan §5): water budget, transfers, propulsion and the flows of a generation.

python -m logistics_model [--set name=value ...]
"""

import argparse
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import flows, propulsion, transfers, water

MT, KT, PJ, GW = 1e9, 1e6, 1e15, 1e9
SIZES = (900, 1600, 2500)
CASES = ((900, 2, "900 m pair"), (1600, 6, "1.6 km six-stack"))   # at Eros (LL taken), Ryugu as the C-type
# (origin, target, the notes' best phase and dated delta-v, km/s; None where the notes give none)
PAIRS = (
    ("Ryugu", "Eros", 4.5, 4.7), ("Bennu", "Eros", 5.8, 6.2),
    ("Ryugu", "Itokawa", 6.3, 6.3), ("Bennu", "Itokawa", 8.3, 8.5),
    ("Ryugu", "Apophis 2029", 5.5, None), ("Bennu", "Apophis 2029", 7.4, None),
    ("Ryugu", "Torifune", 7.6, 7.6), ("Itokawa", "Torifune", 3.6, 3.6),
    ("Itokawa", "Eros", 7.8, None), ("Earth", "Eros", 6.9, None), ("Earth", "Torifune", 4.0, None),
    ("Ryugu", "Didymos", None, None),
)
GENERATIONS = (10, 25)


def label(r):
    return f"{r / 1000:g} km" if r >= 1000 else f"{r:g} m"


def design(r, n=1):
    return Design(radius_m=r, n_tori=n, host_class="LL", site="Eros", c_partner="Ryugu")


def water_section(p):
    res = {r: evaluate(p, design(r)) for r in SIZES}
    budgets = {r: water.budget(res[r]) for r in SIZES}
    uses = list(budgets[900]["uses"])
    rows = [[u] + [f"{num(budgets[r]['uses'][u] / KT)} kt" for r in SIZES] for u in uses]
    rows.append(["**Total**"] + [f"**{num(budgets[r]['total'] / MT, 2)} Mt**" for r in SIZES])
    rows.append(["Notes until now (fitted, no breakdown)", "~0.15 Mt", "~0.4 Mt", "~0.9 Mt"])
    rows.append(["Spin-up with water thrusters, if chosen"] + [f"{num(budgets[r]['spinup'] / MT, 2)} Mt" for r in SIZES])
    rows.append(["Water in the nitrogen-sized C-type"] + [f"{num(budgets[r]['c_type_contains'] / MT, 2)} Mt" for r in SIZES])

    route_rows, iron_rows = [], []
    for r, n, name in CASES:
        d = design(r, n)
        res_d = evaluate(p, d)
        w = water.routes(p, d, res_d)
        for route, v in w["routes"].items():
            route_rows.append([name, route, f"{num(v['shipped'] / KT)} kt", f"{num(v['shipping'] / PJ)} PJ",
                               f"{num(v['other_energy'] / PJ, 2)} PJ", f"{num(v['total'] / PJ)} PJ"])
        iron_rows.append([name, f"{num(w['iron_for_oxygen'] / MT, 2)} Mt", f"{num(w['iron_shortfall'] / MT, 2)} Mt",
                          f"{num(w['iron_for_oxygen'] * p.moe_mj_kg_fe * 1e6 / PJ, 2)} PJ",
                          f"{num(w['hydrogen'] / KT)} kt", f"{num(w['carbon_in_methane'] / KT)} kt",
                          f"{num(w['organics'] / KT)} kt"])
    return [
        "## Water per torus",
        "Built up from its uses instead of fitted to the notes' totals: soil moisture (25% of 0.5 m of soil), "
        f"lakes and streams on {p.lake_floor_frac:.0%} of the floor at {num(p.lake_depth_m)} m mean depth (a "
        "climate dial, from an arid canyon to a fern gully), the water electrolysed for the O₂, ballast to trim "
        f"an operational imbalance of {p.ballast_frac:.2%} of the rim's mass (water spread as 1 − cos around the "
        f"rim, e M in all), and the vegetation's water (~{num(p.biomass_water_kg_m2)} kg/m² of floor). Not "
        "counted: coolant loops (plan §6), people, stores and pipes (hundreds of tonnes), the algae trays "
        "(~200 m³).",
        table(["Use", *[label(r) for r in SIZES]], rows),
        "Lakes and soil dominate; the C-type sized by nitrogen holds ~2.5–7× the water needed, so water never "
        "sizes the C-type unless spin-up uses water thrusters (900 m). A lake also shields: each tonne of water "
        "stands for ~1.6 t of rock, a credit not taken here (~0.3% of the rim).",
        "## Where the water comes from",
        "Water is 89% oxygen, which the S-type has in its silicates. Ship only the hydrogen (split from the "
        "C-type's water) and take the oxygen as the by-product of molten-oxide electrolysis (notes §10, "
        "proposed; ~0.29 kg of oxygen per kg of iron): on an LL host the iron the free metal lacks already "
        "frees more oxygen than the water needs, so the oxygen costs nothing extra. Hydrogen is hard to store "
        "(20 K); methane (111 K) carries it with carbon, which replaces the organics shipped for the soil. "
        "Shipping by electric thrusters at the notes' Ryugu → Eros Δv; the other energy is splitting the water "
        "at the C-type (and any iron reduced only for its oxygen).",
        table(["Stack (per torus)", "Route", "Shipped", "Shipping", "Other energy", "Total"], route_rows),
        table(["Stack", "Iron reduced to free the water's oxygen", "Iron the free metal lacks (LL host)",
               "Electrolysis if the host mines more rock instead", "Hydrogen", "Carbon in the methane",
               "Organics needed"], iron_rows),
        "On a host that mines more rock for its metal instead of electrolysing its silicates (the baseline on "
        "large hosts such as Eros), the iron reduced only for its oxygen costs the electrolysis in the third "
        "column, still below the shipping it saves.",
    ]


def transfer_section():
    rows = []
    for origin, target, best_notes, dated in PAIRS:
        dv, nu1, nu2, days = transfers.best_phase(origin, target)
        rows.append([f"{origin} → {target}", f"{num(dv / 1e3, 2)} km/s",
                     f"{best_notes} km/s" if best_notes else "—", f"{dated} km/s" if dated else "—",
                     num(days), num(transfers.synodic_period(origin, target), 2),
                     f"{num(transfers.perihelion_longitude(origin))}° / {num(transfers.perihelion_longitude(target))}°"])
    return [
        "## Transfers",
        "Two-impulse rendezvous, zero-revolution Lambert arcs between the two orbits, with the departure and "
        "arrival points and the flight time all free: the \"best phase\", a lower bound whatever the bodies' "
        "positions (`logistics_model/transfers.py`). Elements rounded from JPL's Small-Body Database as "
        "recalled: current ephemerides (JPL Horizons) are blocked from this environment, so the notes' dated "
        "values stay as quoted. The synodic period is how often the same phasing recurs, so how far apart the "
        "good windows are.",
        table(["Transfer", "Best phase (model)", "Best phase (notes)", "Dated, 2030–2060 (notes)", "Flight (days)",
               "Synodic period (yr)", "Perihelion longitudes"], rows),
        "The model reproduces the notes' best-phase values within ~0.1 km/s, except to Torifune (0.1–0.4 km/s "
        "lower; its elements are the least certain here). Low-thrust transfers need somewhat more than these "
        "impulsive values.",
    ]


def propulsion_section(p):
    rows, even = [], []
    for r, n, name in CASES:
        d = design(r, n)
        res = evaluate(p, d)
        mat, rep = res["materials"], res["replication"]
        residue = mat["c_type"] * (1 - p.c_water_wt - p.c_carbon_wt)
        spare = mat["c_water_contained"] - mat["water_to_source"]
        opts = propulsion.options(p, rep["delta_v_km_s"] * 1e3, rep["shipped"], residue, spare)
        # The mass driver's efficiency at which it only matches the baseline's electricity.
        even.append(opts[2]["energy"] * opts[2]["efficiency"] / opts[0]["energy"])
        ratio = opts[2]["thrust_per_w"] / opts[0]["thrust_per_w"]
        for o in opts:
            available = "—" if o["available"] is None else f"{num(o['available'] / MT, 2)} Mt"
            rows.append([name, o["name"], f"{num(o['ve'] / 1e3, 2)} km/s", f"{o['efficiency']:.0%}",
                         f"{num(o['propellant'] / MT, 2)} Mt" + ("" if o["fits"] else " (**too much**)"),
                         available, f"{num(o['energy'] / PJ)} PJ", f"{num(o['thrust_per_w'] * 1e6)} N/MW"])
    return [
        "## Propulsion",
        "Per torus's cargo (the water route), Ryugu → Eros at the notes' 4.7 km/s. Electricity per kg delivered "
        "is ½ (e^(Δv/vₑ) − 1) vₑ² / η, lowest at vₑ ≈ Δv / 1.59 (~3 km/s here): a fast exhaust saves "
        "propellant, not energy. A mass driver (a linear motor throwing pellets, O'Neill's reaction engine) "
        "can run there, using the C-type's baked residue, waste otherwise, as reaction mass; it also gives "
        f"~{num(ratio, 1)}× the thrust per watt, so shorter transfers for the same power.",
        table(["Stack (per torus)", "Option", "Exhaust", "Efficiency", "Propellant", "Available at the C-type",
               "Electricity", "Thrust"], rows),
        f"Efficiencies are estimates or guesses (mass driver {p.mass_driver_efficiency:.0%}, range 30–80%); the "
        f"mass driver uses less electricity than the baseline down to ~{max(even):.0%} efficiency.",
    ]


def generation_section(p):
    comp_rows, time_rows, rate_rows, growth_rows = [], [], [], []
    window = transfers.synodic_period("Ryugu", "Eros")
    for r, n, name in CASES:
        d = design(r, n)
        res = evaluate(p, d)
        c = flows.composition(p, res)
        comp_rows.append([name, f"{num(c['built'] / MT)} Mt", f"{c['local_share']:.2%}",
                          f"{num(c['shipped'] / KT)} kt ({c['shipped'] / c['built']:.2%})",
                          f"{num(c['vitamins'] / 1e3)} t ({c['vitamins'] / c['built']:.3%})"])
        rep = res["replication"]
        # The best combination: methane route, mass driver.
        w = water.routes(p, d, res)["routes"]["Methane, oxygen from the silicates"]
        mat = res["materials"]
        residue = mat["c_type"] * (1 - p.c_water_wt - p.c_carbon_wt)
        md = propulsion.options(p, rep["delta_v_km_s"] * 1e3, w["shipped"], residue, 0.0)[2]
        best = rep["processing"] + md["energy"] + w["other_energy"]
        power = d.factory_power_gw * GW / n      # a stack's factory, per torus
        time_rows.append([name, f"{num(rep['processing'] / PJ)} PJ", f"{num(rep['shipping'] / PJ)} PJ",
                          num(rep["energy_per_torus"] / power / flows.YEAR, 2),
                          f"{num(best / PJ)} PJ", num(best / power / flows.YEAR, 2)])
        for years in GENERATIONS:
            x = flows.rates(res, years, window)
            rate_rows.append([name, f"{years} yr", f"{num(x['s_type_day'] / 1e6)} kt ({x['s_type_day'] / flows.MINE_KG_DAY:.1%})",
                              f"{num(x['metal_day'] / 1e3)} t ({x['metal_day'] / flows.STEELWORKS_KG_DAY:.1%})",
                              f"{num(x['rock_placed_day'] / 1e6)} kt", f"{num(x['c_type_day'] / 1e6, 2)} kt",
                              f"{num(x['shipped_per_window'] / KT)} kt", f"{num(x['power'] / 1e6)} MW"])
            g = flows.growth(p, d, res, years)
            growth_rows.append([name, f"{years} yr", f"{g['after'][50]:,.0f}", f"{g['after'][100]:,.0f}",
                                f"{g['c_type_supports']:,.0f}", num(g["years_to_c_limit"], 2)])
    return [
        "## A generation",
        "A parent stack builds a child stack torus by torus, so a cluster doubles once per generation. "
        "**What a child is made of**, per torus (the torus, its share of the hub and factory metal, its farm "
        "ring and its array), by source: the host's rock and metal, the C-type's shipped products, and "
        f"imported vitamins (the array's silicon at {num(p.pv_silicon_kg_m2)} kg/m², and ~{num(p.other_vitamins_t)} t "
        "of electronics, dopants, catalysts and the like per 900 m torus, a guess).",
        table(["Stack (per torus)", "Built", "From the host", "Shipped from the C-type", "Vitamins"], comp_rows),
        f"**Energy floor on the generation**, with the factory at {num(Design().factory_power_gw)} GW per stack: "
        "processing and shipping as in the system model (water route, electric thrusters), then the cheapest "
        "combination found here (methane route, mass driver).",
        table(["Stack (per torus)", "Processing", "Shipping", "Generation (yr)", "Best combination",
               "Generation (yr)"], time_rows),
        "**Rates for a given generation**, per torus of the parent (a stack's lines handle n times these), against "
        "Earth benchmarks (orders of magnitude, unsourced): the largest open-pit mines move ~0.5 Mt of material a "
        "day, a large steelworks makes ~10 Mt of steel a year. Cargo per window: one Ryugu → Eros window every "
        f"~{num(window, 2)} years (synodic period).",
        table(["Stack", "Generation", "S-type mined a day (share of a large mine)",
               "Metal a day (share of a large steelworks)", "Rock placed a day", "C-type baked a day",
               "Cargo per window", "Mean power"], rate_rows),
        "**Growth.** A cluster started by one stack, doubling every generation, until Ryugu's nitrogen runs out:",
        table(["Stack", "Generation", "Tori after 50 years", "After 100 years", "Tori Ryugu supports",
               "Years to reach it"], growth_rows),
    ]


def report(p):
    parts = [
        "# Replication logistics",
        "Plan §5 (`logistics_model/`): the water per torus by use, where it comes from, the transfers and "
        "propulsion that ship the C-type's products, and the flows of a generation. Designs: 900 m pairs and "
        "1.6 km six-stacks at Eros (LL host), Ryugu as the C-type.",
        *water_section(p),
        *transfer_section(),
        *propulsion_section(p),
        *generation_section(p),
        "Not modelled: factory throughput as a function of its own mass (how fast a factory copies itself), "
        "people and training, seed transfers to new sites, the freighters' own mass and power (their solar "
        "arrays are silicon, a vitamin), failures and spares, and dated windows from current ephemerides.",
    ]
    return "\n\n".join(parts) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m logistics_model", description=__doc__)
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    print(report(params(load(), **dict(args.set))), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
