"""Replication logistics (plan §5): water budget, transfers, propulsion and the flows of a generation.

python -m logistics_model [--set name=value ...]
"""

import argparse
import functools
import sys

import numpy as np

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import catalogue, flows, propulsion, transfers, water, windows
from .ephemeris import Ephemeris, jd_of

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
# The catalogue's best new partners (`catalogue.py`), with dated windows.
NEW_PAIRS = (("1999 XX262", "Eros"), ("2015 DX198", "Eros"), ("2001 WT1", "Itokawa"), ("2001 WT1", "Torifune"))
SPAN = (2028, 2072)
GOOD = 1000.0            # m/s above a pair's best: a usable window


@functools.lru_cache(maxsize=None)
def dated(origin, target):
    """Dated windows on JPL Horizons' ephemerides, 2028–2072 (Apophis after its 2029 flyby): the best, the best
    in 2030–2060 (the notes' span), the usable windows (within GOOD of the best) and their mean interval."""
    eph = _eph()
    body = "Apophis" if target == "Apophis 2029" else target
    start = jd_of(2029, 6) if target == "Apophis 2029" else jd_of(SPAN[0])
    s = windows.summary(eph, origin, body, start, jd_of(SPAN[1]), within=GOOD)
    in_notes = [w for w in s["all"] if jd_of(2030) <= w[1] < jd_of(2060)]
    usable = [w for w in s["all"] if w[0] <= s["best"][0] + GOOD]
    gaps = np.diff([w[1] for w in usable]) / 365.25
    return {"best": s["best"], "notes_span": min(in_notes) if in_notes else None, "usable": usable,
            "interval": float(np.mean(gaps)) if len(gaps) else None}


@functools.lru_cache(maxsize=None)
def _eph():
    return Ephemeris()


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

    route_rows, oxygen_rows = [], []
    for r, n, name in CASES:
        d = design(r, n)
        res_d = evaluate(p, d)
        w = water.routes(p, d, res_d)
        combos = water.supply(p, d, res_d)
        for route in w["routes"]:
            ep, md = combos[(route, "Electric thrusters")], combos[(route, "Mass driver")]
            route_rows.append([name, route, f"{num(ep['shipped'] / KT)} kt", f"{num(ep['other_energy'] / PJ, 2)} PJ",
                               f"{num(ep['shipping'] / PJ)} PJ", f"**{num(ep['total'] / PJ)} PJ**",
                               f"{num(md['shipping'] / PJ, 2)} PJ", f"**{num(md['total'] / PJ)} PJ**"])
        o = w["local_oxygen"]
        oxygen_rows.append([name, f"{num(w['iron_for_oxygen'] / MT, 2)} Mt", f"{num(o['split'] / PJ, 2)} PJ",
                            f"{num(o['moe_electric'] / PJ, 2)} PJ", f"{num(o['moe_heat'] / PJ, 2)} PJ",
                            f"−{num(o['crushing_saved'] / PJ, 2)} PJ", f"{num(w['hydrogen'] / KT)} kt",
                            f"{num(w['carbon_in_methane'] / KT)} kt", f"{num(w['organics'] / KT)} kt"])
    return [
        "## Water per torus",
        "Built up from its uses instead of fitted to the notes' totals: soil moisture (25% of 0.5 m of soil), "
        f"ponds and streams on {p.lake_floor_frac:.0%} of the floor at {num(p.lake_depth_m)} m mean depth (kept "
        "small: water access for the biosphere, not a main feature; within the fill), the water electrolysed "
        f"for the O₂, ballast to trim an unbalanced mass of {p.ballast_frac:.2%} of the rim's at the rim (water "
        "spread as A (1 − cos) around it: its first moment is only half its mass times the radius, so 2 e M of "
        f"water), and the vegetation's water (~{num(p.biomass_water_kg_m2)} kg/m² of floor). Not counted: coolant "
        "loops (plan §6), people, stores and pipes (hundreds of tonnes), the algae trays (~200 m³).",
        table(["Use", *[label(r) for r in SIZES]], rows),
        "Soil moisture is about 60% of it, the ballast about a fifth, the ponds about a tenth. The C-type sized "
        "by nitrogen holds ~5–12× the water needed, so water never sizes the C-type unless spin-up uses water "
        "thrusters (900 m).",
        "## Where the water comes from",
        "Water is 89% oxygen, which the S-type has in its silicates. The alternative to shipping water: split "
        "it at the C-type, ship only the hydrogen and take the oxygen from the silicates by molten-oxide "
        "electrolysis (notes §10, proposed; ~0.29 kg of oxygen per kg of iron, so ~3.1 kg of iron per kg of "
        "water). Hydrogen is hard to store (20 K); methane (111 K) carries it with carbon, which replaces the "
        "organics shipped for the soil (the same mass as bare hydrogen while its carbon stays below the organics "
        "needed), and burnt with the same oxygen it is a storable rocket propellant (methalox, ~3.6 km/s) for "
        "tugs and docking. The baseline host gets all its metal as free metal and electrolyses nothing, so the "
        "oxygen is charged in full: the electrolysis's electricity and the furnace heat to melt the rock, less "
        "the crushing of the free-metal rock its iron replaces. Each route with each freighter (next section): "
        "electric thrusters at the notes' Ryugu → Eros Δv, or the energy-optimal mass driver.",
        table(["Stack (per torus)", "Route", "Shipped", "Local oxygen and splitting",
               "Electric thrusters: shipping", "Total", "Mass driver: shipping", "Total"], route_rows),
        table(["Stack", "Iron electrolysed for the oxygen", "Splitting the water", "Electrolysis (electricity)",
               "Melting the rock (furnace heat)", "Crushing saved", "Hydrogen", "Carbon in the methane",
               "Organics needed"], oxygen_rows),
        "With electric thrusters, shipping the hydrogen saves a little; with mass drivers, shipping costs less "
        "than making the oxygen, so water is the cheaper cargo. Only a host that electrolyses its silicates for "
        "its iron anyway (a small LL host, notes §10) gets the oxygen without the electrolysis and the furnace "
        "heat: then only the splitting is left.",
    ]


def transfer_section():
    rows = []
    for origin, target, best_notes, dated_notes in PAIRS:
        dv, nu1, nu2, days = transfers.best_phase(origin, target)
        d = dated(origin, target)
        b, n30 = d["best"], d["notes_span"]
        rows.append([f"{origin} → {target}", f"{num(dv / 1e3, 3)} km/s", f"{best_notes} km/s" if best_notes else "—",
                     f"{num(n30[0] / 1e3, 3)} km/s ({windows.date_str(n30[1])[:7]})" if n30 else "—",
                     f"{dated_notes} km/s" if dated_notes else "—",
                     f"{num(b[0] / 1e3, 3)} km/s ({windows.date_str(b[1])[:7]}, {num(b[2])} d)",
                     f"{len(d['usable'])}, every ~{num(d['interval'], 2)} yr" if d["interval"] else "1"])
    eph = _eph()
    return [
        "## Transfers",
        "Two-impulse rendezvous on zero-revolution Lambert arcs (`logistics_model/transfers.py`). **Phase-free** "
        "(\"best phase\"): departure and arrival points and flight time all free, a lower bound whatever the "
        "bodies' positions, on the osculating elements of JPL's Small-Body Database (fetched "
        f"{eph.meta['fetched']}; within rounding of the ones recalled before). **Dated** (`windows.py`): on JPL "
        f"Horizons' ephemerides ({eph.meta['start'][:4]}–{eph.meta['stop'][:4]}, planets' perturbations and "
        "Apophis's 2029 flyby included, `logistics_model/data/`), departures every 5 days and flights of "
        "60–900 days, each dip of the best-flight curve refined. A usable window: within "
        f"{GOOD / 1e3:g} km/s of the pair's best in {SPAN[0]}–{SPAN[1]}.",
        table(["Transfer", "Best phase (model)", "Best phase (notes)", "Dated, 2030–2060", "Dated (notes)",
               f"Best, {SPAN[0]}–{SPAN[1]}", "Usable windows"], rows),
        "The dated search lands on the notes' quoted values within ~0.1 km/s (Bennu → Eros 0.3 lower), and "
        "on the phase-free bound within ~0.1–0.3 km/s at its best window: the bound is reached about once in "
        "a few decades. Usable windows come every ~2–7 years, not once per synodic period on the dot; a "
        "freighter fleet times its departures to them. Low-thrust transfers need somewhat more than these "
        "impulsive values.",
    ]


def partner_section(p):
    data = catalogue.load()
    ref = Design(radius_m=900, n_tori=6, tiers_lit=3, host_class="LL", site="Eros", c_partner="Ryugu")
    c_per_torus = evaluate(p, ref)["materials"]["c_type"]
    cand_rows = []
    for host in catalogue.HOSTS:
        for key, c, dv, days in catalogue.ranked(data, host, 4):
            m = catalogue.mass_kg(c["diameter_km"])
            cand_rows.append([host, c["name"], c["spec"] or "—", num(c["albedo"], 2) if c["albedo"] else "—",
                              f"{num(c['diameter_km'], 2)} km", f"{num(m / MT)} Mt", f"~{m / c_per_torus:,.0f}",
                              f"**{num(dv / 1e3, 2)} km/s**"])
    ryugu = catalogue.mass_kg(0.896)
    ref_rows = []
    for (origin, target) in (("Ryugu", "Eros"),) + NEW_PAIRS[:2] + (("Ryugu", "Itokawa"), NEW_PAIRS[2],
                                                                  ("Ryugu", "Torifune"), NEW_PAIRS[3]):
        d = dated(origin, target)
        b, n30 = d["best"], d["notes_span"]
        ref_rows.append([f"{origin} → {target}", f"{num(n30[0] / 1e3, 3)} km/s ({windows.date_str(n30[1])[:7]})",
                         f"{num(b[0] / 1e3, 3)} km/s ({windows.date_str(b[1])[:7]})",
                         f"every ~{num(d['interval'], 2)} yr" if d["interval"] else "—"])
    energy_rows = []
    for partner, dv_pair in (("Ryugu", ("Ryugu", "Eros")), ("1999 XX262", NEW_PAIRS[0]), ("2015 DX198", NEW_PAIRS[1])):
        dv = dated(*dv_pair)["notes_span"][0] / 1e3
        res = evaluate(p, Design(radius_m=1600, n_tori=6, tiers_lit=3, host_class="LL", site="Eros",
                                 c_partner="Ryugu", delta_v_km_s=dv))
        rep_ = res["replication"]
        energy_rows.append([f"{partner} → Eros", f"{num(dv, 3)} km/s", f"{num(rep_['shipping'] / PJ)} PJ",
                            f"{num(rep_['energy_per_torus'] / PJ)} PJ", num(rep_["generation_time_yr"], 3)])
    xx_mass = catalogue.mass_kg(data["candidates"]["275611"]["diameter_km"])

    def gain(partner, host):
        return (dated("Ryugu", host)["notes_span"][0] - dated(partner, host)["notes_span"][0]) / 1e3

    n_cand = len(data["candidates"])
    n_spec = sum(1 for c in data["candidates"].values() if "spectrum" in c["why"])
    return [
        "## Better C-type partners",
        f"A catalogue search (`logistics_model/catalogue.py`, JPL's Small-Body Database, fetched "
        f"{data['fetched']}): {n_cand} near-Earth asteroids that are classified in the C complex ({n_spec}) or "
        "dark in NEOWISE's albedos (< 0.08, at least 0.3 km across), each with its phase-free Δv to the hosts, "
        "screened on a coarse grid and refined for the best dozen per host. Mass at Ryugu's bulk density "
        f"(1.19 t/m³); tori its nitrogen could supply at ~{num(c_per_torus / MT, 2)} Mt of C-type per 900 m torus "
        "(the system model's).",
        table(["Host", "Candidate", "Type", "Albedo", "Diameter", "Mass", "900 m tori supplied", "Best phase"],
              cand_rows),
        f"Ryugu ({num(ryugu / MT)} Mt, ~{ryugu / c_per_torus:,.0f} tori) is at 4.5 km/s from Eros, 6.3 from "
        "Itokawa and 7.6 from Torifune. Dated, on Horizons' ephemerides:",
        table(["Transfer", "Best, 2030–2060", f"Best, {SPAN[0]}–{SPAN[1]}", "Usable windows"], ref_rows),
        "And what the lower Δv saves, per torus of a 1.6 km six-stack at Eros (electric thrusters, the system "
        "model's baseline):",
        table(["Volatiles from", "Δv (best, 2030–2060)", "Shipping", "Energy per torus", "Generation (yr)"],
              energy_rows),
        "**Proposed: characterise 1999 XX262 for Eros and 2001 WT1 for Itokawa and Torifune.** 1999 XX262 is "
        f"~1.5 km across, ~{xx_mass / ryugu:.1f}× Ryugu's mass, ~{num(gain('1999 XX262', 'Eros'), 2)} km/s closer "
        f"to Eros at its 2030–2060 windows and with usable windows ~3× as often; 2001 WT1 (~0.5 km) is "
        f"~{num(gain('2001 WT1', 'Itokawa'), 2)} km/s closer to Itokawa and ~{num(gain('2001 WT1', 'Torifune'), 2)} "
        "closer to Torifune than Ryugu. Both are known only by their "
        "albedo: dark (C-, D- or P-like) is not yet carbonaceous with nitrogen, and NEOWISE's diameters are "
        "good to ~±20–30%. A spectrum (and, for the chosen one, a sample) comes first; Ryugu stays the "
        "baseline.",
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
    comp_rows, time_rows, rate_rows, growth_rows, best_names = [], [], [], [], []
    window = dated("Ryugu", "Eros")["interval"]
    for r, n, name in CASES:
        d = design(r, n)
        res = evaluate(p, d)
        c = flows.composition(p, res)
        comp_rows.append([name, f"{num(c['built'] / MT)} Mt", f"{c['local_share']:.2%}",
                          f"{num(c['shipped'] / KT)} kt ({c['shipped'] / c['built']:.2%})",
                          f"{num(c['vitamins'] / 1e3)} t ({c['vitamins'] / c['built']:.3%})"])
        rep = res["replication"]
        # The cheapest consistent combination of route and freighter.
        (route, engine), v = min(water.supply(p, d, res).items(), key=lambda kv: kv[1]["total"])
        best = rep["processing"] + v["total"]
        best_names.append(f"{name}: {route.split(',')[0].lower()} by {engine.lower()}")
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
        f"combination of route and freighter above ({'; '.join(best_names)}).",
        table(["Stack (per torus)", "Processing", "Shipping", "Generation (yr)", "Best combination",
               "Generation (yr)"], time_rows),
        "**Rates for a given generation**, per torus of the parent (a stack's lines handle n times these), against "
        "Earth benchmarks (orders of magnitude, unsourced): the largest open-pit mines move ~0.5 Mt of material a "
        "day, a large steelworks makes ~10 Mt of steel a year. Cargo per window: one usable Ryugu → Eros "
        f"window every ~{num(window, 2)} years (dated search, above).",
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
        *partner_section(p),
        *propulsion_section(p),
        *generation_section(p),
        "Not modelled: factory throughput as a function of its own mass (how fast a factory copies itself), "
        "people and training, seed transfers to new sites, the freighters' own mass and power (their solar "
        "arrays are silicon, a vitamin), failures and spares, low-thrust and multi-revolution transfers, and gravity "
        "assists.",
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
