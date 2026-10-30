"""Closed atmosphere and ecology (plan §7): a compartment model of a torus's air, crops, people, soil and
vegetation; failures, startup, leaks and a replay of Biosphere 2.

python -m ecology_model [--set name=value ...]
"""

import argparse
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import closed, scenarios

SIZES = ((900, "900 m"), (1600, "1.6 km"))


def days(x):
    return "never (1 yr)" if x is None else f"{x:,.0f} days"


def results_for(p, radius):
    return evaluate(p, Design(radius_m=radius, n_tori=6, tiers_lit=3))


def baseline_section(p):
    rows = []
    for radius, name in SIZES:
        r = results_for(p, radius)
        c = closed.config(p, r)
        s = closed.mature(c)
        pr = closed.pressures(c, s)
        _, farm = closed.farm_uptake(c, pr["co2"], c.lit)
        rows.append([name, num(c.people), f"{num(c.o2 * closed.M_O2 / 1e6)} kt",
                     f"{num(c.people * c.food_c / c.rq * closed.M_O2 * closed.DAY / 1e3, 2)} t",
                     f"{num(c.o2 / (c.people * c.food_c / c.rq) / closed.YEAR, 2)} yr",
                     f"{num(pr['co2'])} Pa", f"{num(farm)} Pa",
                     f"{num((s.labile + s.stable) * closed.M_C / r['geometry']['floor_area'], 2)} kg/m²"])
    return [
        "## A torus in balance",
        "Per torus of a six-stack, three farm tiers lit (`ecology_model/closed.py`). The farm fixes its share "
        "of its people's food and the valley's gardens the rest, half of it edible (`harvest_index`); people "
        "eat it and breathe it out; the inedible half "
        "is composted into the soil and respired; the valley's grown woodland sheds as much as it grows. The "
        "farm's air is held at ~1,000 ppm-equivalent of CO2 (100 Pa), exchanged with the valleys' through the "
        f"hub ducts at {num(p.duct_exchange_m3_s)} m³/s, so the valleys sit a little above it. The O2 store "
        "is the air's own: years of breathing.",
        table(["Torus", "People", "O2 in the air", "O2 breathed a day", "Air's O2 / breathing",
               "Valley CO2", "Farm CO2", "Soil carbon, at equilibrium"], rows),
    ]


def failure_section(p):
    out = []
    for radius, name in SIZES:
        r = results_for(p, radius)
        _, rows = scenarios.failures(p, r)
        rows.append(scenarios.soil_burst(p, r))
        for x in rows:
            out.append([name, x["name"], days(x["co2_days"]), days(x["o2_days"]),
                        f"{num(x['co2_max'])} Pa", f"{num(x['o2_min'] / 1e3, 3)} kPa",
                        days(x["food_out_days"]) if x["food_out_days"] is not None
                        else f"never ({x['food_days_left']:,.0f} days left)",
                        f"{num(x['regen_peak_t_day'], 2)} t/day ({num(x['regen_peak_mw'], 2)} MW)"])
    return [
        "## Failures",
        f"From a torus in balance, uncontrolled for a year: days until the valleys' CO2 passes "
        f"{p.co2_limit_pa:g} Pa (~5,000 ppm at sea level) and the O2 falls below {p.o2_min_kpa:g} kPa, "
        "the worst of each; then the oxygen a physico-chemical plant must recover from CO2 (a Bosch or "
        "Sabatier reactor with electrolysis, undoing respiration as photosynthesis does) to hold both, at "
        f"{p.o2_regen_mj_kg:g} MJ per kg of O2. The farm's crops take up more CO2 as it rises "
        f"(x / (x + {p.co2_half_saturation_pa:g} Pa)), which buffers small upsets on its own.",
        table(["Torus", "Scenario", "CO2 limit after", "O2 limit after", "Peak CO2", "Lowest O2",
               "Food store (90 days) runs out after", "Recovery needed at peak"], out),
        "A dark tier costs food before it costs air: the crops fertilised by the extra CO2 make up only part "
        "of it, and the store runs down. Once it is empty the model has people breathe out their body "
        "reserves (tracked, so the carbon still closes); later crossings assume no resupply, so read them as "
        "bounds. Relighting the tiers or bringing food in ends it.",
    ]


def startup_section(p):
    r = results_for(p, 900)
    rows = []
    for name, changes in (("As planned: imported organics, 30% fast-decaying", {}),
                          ("Organics composted before they go in (5% fast-decaying)", {"soil_labile_frac": 0.05}),
                          ("Half the organics, the rest grown from residues", {"organics_shipped_t_m2":
                                                                                p.organics_shipped_t_m2 / 2})):
        q = params(load(), **{**vars(p), **changes}) if changes else p
        _, free, held, x = scenarios.startup(q, r if not changes else evaluate(q, Design(radius_m=900, n_tori=6,
                                                                                          tiers_lit=3)))
        yearly = [held["regen"][min(int(y * 365.25), len(held["regen"]) - 1)] * closed.M_O2 * closed.DAY / 1e3
                  for y in (0.5, 2, 5)]
        rows.append([name, days(x["co2_days"]), days(x["o2_days"]), f"{num(x['regen_peak_mw'], 2)} MW",
                     " / ".join(num(v, 2) for v in yearly), f"{num(x['regen_total_kt'], 2)} kt"])
    return [
        "## A new torus",
        f"A 900 m torus filled with its soil (imported organics at {p.organics_shipped_t_m2:g} t/m², "
        f"~{p.organics_shipped_t_m2 * 1e3 * p.organics_carbon_frac:g} kg C/m²) and young woodland "
        f"({p.valley_biomass_start:g} kg C/m², growing towards {p.valley_biomass_max:g}), its farm lit for "
        "its people. The soil's organic carbon respires towards the much smaller stock the residues and litter "
        "keep up: as Biosphere 2's compost-rich soil did, it draws down the O2 and loads the air with CO2, far "
        "faster than people do. Ten years, uncontrolled and with recovery:",
        table(["Soil", "CO2 limit after", "O2 limit after", "Recovery at peak", "O2 recovered, t/day at 0.5 / 2 / 5 yr",
               "O2 recovered over 10 yr"], rows),
    ]


def leak_section(p):
    r = results_for(p, 900)
    rows = [[f"{x['diameter'] * 100:g} cm", f"{num(x['flow'], 2)} kg/s", days(x["days_10pct"]) if x["days_10pct"] >= 1
             else f"{num(x['days_10pct'] * 24, 2)} hours"] for x in scenarios.leak(p, r)]
    return [
        "## Leaks",
        "A hole in a 900 m torus's pressure hull, air escaping at the speed of sound (choked flow, discharge "
        f"coefficient 0.6) from {p.pressure_kpa:g} kPa: time to lose a tenth of the air, and so of the "
        f"pressure. A background leak of {p.leak_frac_yr:.1%} of the air a year (seals, docking, airlocks) is in "
        "every run above.",
        table(["Hole", "Air lost", "10% of the air gone after"], rows),
        "The rock jacket and the crawl space keep meteoroids off the pressure hull (notes §13); holes would come "
        "from failures, so a 10 cm one leaves weeks and a 1 m one hours.",
    ]


def biosphere2_section(p):
    b = scenarios.biosphere2(p)
    r = results_for(p, 900)
    t = scenarios.b2_in_a_torus(p, r, b["excess_umol_m2_s"])
    g = r["geometry"]
    air_torus = (r["mass"]["air"] + r["mass"]["farm_n2"] + r["mass"]["farm_o2"]) / g["floor_area"]
    return [
        "## Biosphere 2, replayed",
        "Biosphere 2 (1991–1993): O2 fell from ~20.9% to ~14.2% in ~16 months, as the compost-rich soil respired "
        "and the CO2 went largely into the concrete. Its figures here are approximate, recalled, not sourced "
        "(~1.27 ha, ~1.8 × 10⁵ m³ of air at ~1 atm, eight people on ~2,000 kcal a day). The replay runs its "
        "oxygen bookkeeping through the same model, with the CO2 held near 1,500 ppm by the concrete, and fits "
        "the net soil respiration that photosynthesis didn't return. It checks the model's accounting, not its "
        "soil: Biosphere 2's soil data aren't in the notes.",
        table(["", "Biosphere 2", "900 m torus"], [
            ["Air per m² of floor", f"{num(b['air_kg_m2'])} kg", f"{num(air_torus)} kg"],
            ["Net soil respiration beyond photosynthesis, fitted", f"{num(b['excess_umol_m2_s'], 2)} µmol/m²/s", "—"],
            ["CO2 into the concrete over the 16 months", f"{num(b['co2_absorbed_t'])} t", "no concrete"],
            ["The same excess per m²: CO2 limit after", "(held by the concrete)", days(t["co2_days"])],
            ["… O2 limit after", "~a year to 14%", days(t["o2_days"])],
        ]),
        "~1 µmol/m²/s is a fraction of ordinary soil respiration (several µmol/m²/s), so a small imbalance "
        "is enough. In a torus the same imbalance shows first as CO2, within months, because nothing like the "
        "concrete absorbs it, and the farm's crops, fertilised by it, return most of the oxygen.",
    ]


def report(p):
    parts = [
        "# Closed atmosphere: balance, failures, startup and Biosphere 2",
        "Plan §7 (`ecology_model/`): a compartment model of one torus's air (O2, CO2, N2), its farm ring's crops, "
        "its people, the soil's organic carbon and the valley's vegetation; the farm's air quasi-steady, "
        "exchanged with the valleys' through the hub ducts. Most inputs are estimates or guesses "
        "(`reports/assumptions.md`).",
        *baseline_section(p),
        *failure_section(p),
        *startup_section(p),
        *leak_section(p),
        *biosphere2_section(p),
        "Not modelled: water and humidity (condensed and recycled, notes §13), trace gases (methane, ethylene, "
        "volatiles from materials), nitrogen fixation and denitrification, the valley's daily CO2 swing, "
        "people's movement between tori, the seasons of a seasonal sky, and the controls' own failures.",
    ]
    return "\n\n".join(parts) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m ecology_model", description=__doc__)
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    print(report(params(load(), **dict(args.set))), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
