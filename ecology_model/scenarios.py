"""Failures, startup, leaks and the Biosphere 2 replay (plan §7), on `closed`.

The controls are physico-chemical: CO2 taken out of the air and its oxygen given back (a Bosch or Sabatier
reactor with electrolysis), which undoes respiration the way photosynthesis does. Each scenario runs once
uncontrolled (how long until a limit) and once with the controls holding the limits (how much they must do).
"""

import math
from dataclasses import replace

from .closed import DAY, M_O2, R_GAS, YEAR, config, first_crossing, mature, run, steady_valley_co2

FAILURES = (("One farm tier dark", 2 / 3), ("Two tiers dark (the pumps' passive fallback)", 1 / 3),
            ("The whole farm dark", 0.0))


def limits(p):
    return p.co2_limit_pa, p.o2_min_kpa * 1e3


def controlled(c, p, margin=0.8):
    """The same configuration with unlimited regeneration holding CO2 under margin × its limit and O2 above
    its floor plus the margin's share of the way back to the start."""
    co2_limit, o2_min = limits(p)
    o2_start = c.o2 * R_GAS * c.temperature / c.volume
    return replace(c, regen=1e6, co2_target=margin * co2_limit, o2_target=o2_min + (1 - margin) * (o2_start - o2_min))


def summarise(p, uncontrolled, held, horizon_days):
    co2_limit, o2_min = limits(p)
    peak = max(held["regen"]) if held["regen"] else 0.0
    total = sum(held["regen"]) * DAY                      # mol O2 regenerated over the run (daily records)
    food_out = next((t / DAY for t, f in zip(uncontrolled["t"], uncontrolled["food_days"]) if f <= 1e-6), None)
    return {
        "food_out_days": food_out,                        # then people breathe out their body reserves
        "co2_days": first_crossing(uncontrolled, "co2", co2_limit),
        "o2_days": first_crossing(uncontrolled, "o2", o2_min, above=False),
        "food_days_left": uncontrolled["food_days"][-1],
        "regen_peak": peak,                               # mol O2/s
        "regen_peak_t_day": peak * M_O2 * DAY / 1e3,
        "regen_peak_mw": peak * M_O2 * p.o2_regen_mj_kg,
        "regen_total_kt": total * M_O2 / 1e6,
        "horizon_days": horizon_days,
        "o2_min": min(uncontrolled["o2"]),
        "co2_max": max(uncontrolled["co2"]),
    }


def failures(p, results, years=1.0):
    c = config(p, results)
    rows = []
    for name, lit in FAILURES:
        s = mature(c)
        free = run(c, years, state=s, events=[(0, {"lit": lit})])
        held = run(controlled(c, p), years, state=mature(c), events=[(0, {"lit": lit})])
        rows.append({"name": name, **summarise(p, free, held, years * 365.25)})
    return c, rows


def soil_burst(p, results, extra_umol_m2_s=1.0, decay_yr=1.0, years=2.0):
    """Extra soil respiration (a warm spell, tilling, a load of compost), decaying over decay_yr."""
    c = config(p, results)
    extra = extra_umol_m2_s * 1e-6 * results["geometry"]["floor_area"]
    events = [(0, {"soil_excess": extra, "k_excess": 1 / (decay_yr * YEAR)})]
    free = run(c, years, state=mature(c), events=events)
    held = run(controlled(c, p), years, state=mature(c), events=events)
    return {"name": f"Soil burst, +{extra_umol_m2_s:g} µmol/m²/s fading over {decay_yr:g} yr",
            **summarise(p, free, held, years * 365.25)}


def startup(p, results, years=10.0, **changes):
    """A new torus: imported organics in the soil, young vegetation."""
    c = config(p, results, **changes)
    free = run(c, years, dt=1800.0)
    held = run(controlled(c, p), years, dt=1800.0)
    return c, free, held, summarise(p, free, held, years * 365.25)


def leak(p, results, diameters=(0.01, 0.1, 1.0), discharge=0.6, gamma=1.4):
    """A hole in the pressure hull: choked flow of air at the habitat's pressure and temperature.
    Returns, per diameter, the mass flow and the days to lose 10% of the air (and so of the pressure)."""
    m = results["mass"]
    air = m["air"] + m["farm_n2"] + m["farm_o2"]
    rs = 287.05
    t, pr = p.air_temperature_k, p.pressure_kpa * 1e3
    flux = discharge * pr * math.sqrt(gamma / (rs * t)) * (2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1)))
    rows = []
    for dia in diameters:
        flow = flux * math.pi * dia ** 2 / 4
        # Exponential decay of the inventory: 10% in -ln(0.9) time constants.
        tau = air / flow
        rows.append({"diameter": dia, "flow": flow, "days_10pct": -math.log(0.9) * tau / DAY, "tau_days": tau / DAY})
    return rows


# --- Biosphere 2, 1991-1993: O2 fell from ~20.9% to ~14.2% in ~16 months (notes §16). Approximate figures,
# recalled (unsourced): ~1.27 ha under glass, ~1.8e5 m³ of air at ~1 atm, eight people on ~2,000 kcal a day
# from mostly their own farm; the CO2 went largely into the concrete (calcium carbonate).
B2 = {"area": 12700.0, "volume": 1.8e5, "pressure": 101325.0, "temperature": 298.0, "people": 8,
      "kcal": 2000.0, "days": 487.0, "o2_start": 0.209, "o2_end": 0.142}


def biosphere2(p, co2_held_pa=150.0):
    """Replay Biosphere 2's oxygen bookkeeping: the net soil respiration (beyond what photosynthesis returned)
    that takes O2 from 20.9% to 14.2% in 16 months, with the CO2 held near co2_held_pa by the concrete
    (modelled as scrubbing). Returns the fitted excess per m², the CO2 the concrete took and the per-m² air."""
    b = B2
    moles = b["pressure"] * b["volume"] / (R_GAS * b["temperature"])
    o2_per_person = b["kcal"] / p.kcal_per_l_o2 / 22.414 / DAY
    food_c = o2_per_person * p.respiratory_quotient

    def make(excess):
        base = dict(temperature=b["temperature"], volume=b["volume"], n2=moles * (1 - b["o2_start"]),
                    o2=moles * b["o2_start"], people=b["people"], food_c=food_c, rq=p.respiratory_quotient,
                    harvest_index=p.harvest_index, farm_fix=b["people"] * food_c / p.harvest_index, garden=0.0,
                    lit=1.0,
                    farm_co2=40.0, half_sat=p.co2_half_saturation_pa, exchange=1e5,
                    # The residues' own decay at equilibrium; the fitted excess comes on top, drawn from the
                    # compost-rich soil's humus (ample, so it never runs short over the 16 months).
                    soil_labile=(1 - p.harvest_index) * b["people"] * food_c / p.harvest_index * YEAR,
                    soil_stable=1e9, k_labile=1 / YEAR, k_stable=0.0, humification=0.0,
                    veg=1.0, veg_max=1.0, veg_rate=0.0, k_litter=0.0, leak=0.0,
                    food_store=b["people"] * food_c * 365 * DAY, soil_excess=excess,
                    scrub=1e6, co2_target=co2_held_pa)
        from .closed import Config
        return Config(**base)

    def o2_end(excess):
        c = make(excess)
        out = run(c, b["days"] / 365.25, dt=3600.0)
        return out, out["o2_frac"][-1]

    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if o2_end(mid)[1] > b["o2_end"] else (lo, mid)
    out, _ = o2_end(hi)
    absorbed = sum(out["scrub"]) * DAY
    return {"excess_mol_s": hi, "excess_umol_m2_s": hi / b["area"] * 1e6, "co2_absorbed_t": absorbed * 0.04401 / 1e3,
            "air_kg_m2": moles * 0.02897 / b["area"], "o2_mol_m2": moles * b["o2_start"] / b["area"],
            "series": out}


def b2_in_a_torus(p, results, excess_umol_m2_s, years=2.0):
    """The same per-m² excess in a mature torus, uncontrolled: how fast its O2 and CO2 drift."""
    c = config(p, results)
    extra = excess_umol_m2_s * 1e-6 * results["geometry"]["floor_area"]
    out = run(c, years, state=mature(c), events=[(0, {"soil_excess": extra})])
    o2_start = out["o2_frac"][0]
    drop = next((t / DAY for t, f in zip(out["t"], out["o2_frac"]) if f < o2_start * b2_ratio()), None)
    return {"co2_days": first_crossing(out, "co2", p.co2_limit_pa),
            "o2_days": first_crossing(out, "o2", p.o2_min_kpa * 1e3, above=False), "same_drop_days": drop}


def b2_ratio():
    return B2["o2_end"] / B2["o2_start"]


__all__ = ["failures", "soil_burst", "startup", "leak", "biosphere2", "b2_in_a_torus", "steady_valley_co2"]
