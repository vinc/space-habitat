"""Closed atmosphere of one torus with its farm ring (plan §7): a compartment model of O2, CO2, N2 and carbon.

Pools: the air (O2, N2 and CO2 summed over valley and farm), the farm's food store, the soil's labile and
stable organic carbon, and the valley's standing vegetation. The farm's air is small next to the valley's
and exchanged with it through the hub ducts, so its CO2 is solved quasi-steady: the crops' uptake, which
saturates with CO2 (x / (x + K)), equals what the ducts bring.

Fluxes, in mol per second (carbon and O2 one for one for the residues, the litter and decay; the edible crop
is made at the photosynthetic quotient 1 / RQ that the people's respiration undoes, so the loop closes):
- the farm fixes its share of the diet (all but the valley's), scaled by the tiers lit and its CO2; the
  valley's gardens fix the rest under the sky; the edible share goes to the food store, the rest (composted
  residues) to the soil's labile pool;
- people eat from the store, as much as it holds, and breathe it out: O2 at the food energy's oxygen cost,
  CO2 at the respiratory quotient; once the store is empty they breathe out their body reserves (tracked);
- the soil decays: labile carbon fast (part of it becoming humus), humus slowly, as CO2 into the valley; a
  burst of extra respiration draws on the humus; all of it needs oxygen, and stops below ~1 kPa;
- the valley's vegetation grows logistically towards its full biomass and sheds litter into the soil;
- leaks take air out in proportion; controls can scrub CO2 and regenerate O2 from it, never more than the
  air holds in a step; the carbon they take out is tracked.

All amounts in mol (gases, carbon) and seconds; partial pressures in Pa.
"""

import math
from dataclasses import dataclass, replace

R_GAS = 8.314462618
DAY = 86400.0
YEAR = 365.25 * DAY
M_O2, M_CO2, M_C, M_N2 = 0.031998, 0.04401, 0.012011, 0.0280134


@dataclass(frozen=True)
class Config:
    temperature: float          # K
    volume: float               # m³, valley and farm air together
    n2: float                   # mol
    o2: float                   # mol, at the start
    people: float
    food_c: float               # mol C eaten per person per second
    rq: float
    harvest_index: float
    farm_fix: float             # mol C/s the farm fixes at its reference CO2 with every tier lit
    garden: float               # mol C/s the valley's gardens fix (their share of the diet), under the sky
    lit: float                  # share of the farm's tiers lit
    farm_co2: float             # Pa, the crops' reference CO2
    half_sat: float             # Pa
    exchange: float             # m³/s between the valleys and the farm ring
    soil_labile: float          # mol C, at the start
    soil_stable: float          # mol C, at the start
    k_labile: float             # 1/s
    k_stable: float             # 1/s
    humification: float
    veg: float                  # mol C, at the start
    veg_max: float              # mol C
    veg_rate: float             # 1/s (logistic)
    k_litter: float             # 1/s
    leak: float                 # 1/s
    food_store: float = 0.0     # mol C, at the start
    soil_excess: float = 0.0    # mol C/s of extra soil respiration, decaying with k_excess (a burst)
    k_excess: float = 0.0
    scrub: float = 0.0          # mol CO2/s removed, at most
    regen: float = 0.0          # mol O2/s made from CO2, at most (removes as much CO2)
    co2_target: float = 0.0     # Pa: controls act above this valley CO2 (scrub, regenerate)
    o2_target: float = 0.0      # Pa: regeneration acts below this O2


def config(p, results, tiers_lit=None, **changes):
    """A torus and its farm ring from the system model's results (`habitat_model.evaluate`)."""
    g, m, f = results["geometry"], results["mass"], results["food"]
    t = p.air_temperature_k
    floor = g["floor_area"]
    tiers = tiers_lit if tiers_lit is not None else max(1, round(f["people"] / f["people_per_tier"]))
    people = f["people_per_tier"] * tiers
    o2_per_person = p.diet_kcal / p.kcal_per_l_o2 / 22.414 / DAY        # mol/s
    food_c = o2_per_person * p.respiratory_quotient                    # carbon breathed out = carbon eaten
    organics = p.organics_shipped_t_m2 * 1e3 * floor * p.organics_carbon_frac / M_C
    # A farm built for three tiers: its full fixation feeds three tiers' people their farm share of the diet,
    # as the system model sizes it (`habitat_model.food`); the valley's gardens grow the rest.
    farm_share = 1 - p.valley_diet_share
    full = f["people_per_tier"] * p.farm_tiers_built * food_c * farm_share / p.harvest_index
    garden = people * food_c * p.valley_diet_share / p.harvest_index
    cfg = Config(
        temperature=t, volume=g["volume"] + g["farm_volume"],
        n2=(m["n2"] + m["farm_n2"]) / M_N2, o2=(m["o2"] + m["farm_o2"]) / M_O2,
        people=people, food_c=food_c, rq=p.respiratory_quotient, harvest_index=p.harvest_index,
        farm_fix=full, garden=garden, lit=tiers / p.farm_tiers_built, farm_co2=p.farm_co2_pa, half_sat=p.co2_half_saturation_pa,
        exchange=p.duct_exchange_m3_s,
        soil_labile=organics * p.soil_labile_frac, soil_stable=organics * (1 - p.soil_labile_frac),
        k_labile=1 / (p.soil_labile_turnover_yr * YEAR), k_stable=1 / (p.soil_stable_turnover_yr * YEAR),
        humification=p.humification_frac,
        veg=p.valley_biomass_start * floor / M_C, veg_max=p.valley_biomass_max * floor / M_C,
        veg_rate=p.valley_growth_rate / YEAR, k_litter=1 / (p.litter_turnover_yr * YEAR),
        leak=p.leak_frac_yr / YEAR,
        food_store=people * food_c * 90 * DAY,        # ~3 months of food in store
    )
    return replace(cfg, **changes)


def farm_uptake(c, p_valley, lit):
    """The farm's CO2 uptake (mol/s) and its CO2 (Pa), quasi-steady: P0 x / (x + K) = a (p_v - x)."""
    p0 = c.farm_fix * lit * (c.farm_co2 + c.half_sat) / c.farm_co2       # uptake = p0 x / (x + K)
    a = c.exchange / (R_GAS * c.temperature)                              # mol/s per Pa of difference
    if p0 <= 0 or p_valley <= 0:
        return 0.0, max(p_valley, 0.0)
    b = a * p_valley - a * c.half_sat - p0
    x = (b + math.sqrt(b * b + 4 * a * a * p_valley * c.half_sat)) / (2 * a)
    return p0 * x / (x + c.half_sat), x


def steady_valley_co2(c, demand):
    """Valley CO2 (Pa) at which the farm takes up `demand` mol/s."""
    lo, hi = 0.0, 1e5
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if farm_uptake(c, mid, c.lit)[0] < demand else (lo, mid)
    return hi


@dataclass
class State:
    o2: float
    n2: float
    co2: float
    food: float
    labile: float
    stable: float
    veg: float
    excess: float
    body: float = 0.0       # mol C breathed out of the people's own bodies once the store ran out
    removed: float = 0.0    # mol C the controls took out of the air (as solid carbon or vented CO2)


def demand(c):
    """Carbon the farm must fix for its share of the people's food (mol/s); the gardens fix the rest."""
    return max(0.0, c.people * c.food_c / c.harvest_index - c.garden)


def initial(c, co2_pa=None):
    """A new torus: the imported organics in its soil, its vegetation as planted, the valley's CO2 where the
    farm fixes what feeding the people needs."""
    if co2_pa is None:
        co2_pa = steady_valley_co2(c, demand(c))
    co2 = co2_pa * c.volume / (R_GAS * c.temperature)
    return State(o2=c.o2, n2=c.n2, co2=co2, food=c.food_store, labile=c.soil_labile, stable=c.soil_stable,
                 veg=c.veg, excess=c.soil_excess, body=0.0, removed=0.0)


def mature(c):
    """A torus at equilibrium: vegetation grown, the soil's pools fed only by residues and litter."""
    s = initial(c)
    litter = c.k_litter * c.veg_max
    s.veg = c.veg_max
    s.labile = ((1 - c.harvest_index) * (demand(c) + c.garden) + litter) / c.k_labile
    s.stable = c.humification * c.k_labile * s.labile / c.k_stable
    return s


def pressures(c, s):
    rt = R_GAS * c.temperature / c.volume
    return {"o2": s.o2 * rt, "co2": s.co2 * rt, "n2": s.n2 * rt, "total": (s.o2 + s.co2 + s.n2) * rt,
            "o2_frac": s.o2 / (s.o2 + s.co2 + s.n2)}


def fluxes(c, s, lit, dt=3600.0):
    """Every flux (mol/s) for a step of dt seconds; consumption is bounded by what the pools hold over it."""
    rt = R_GAS * c.temperature / c.volume
    p_co2 = s.co2 * rt
    h = c.harvest_index
    # Respiration needs oxygen: it stops as the O2 runs out (below ~1 kPa).
    aerobic = min(1.0, max(0.0, s.o2 * rt / 1000.0))
    uptake, farm_co2 = farm_uptake(c, p_co2, lit)
    fixed = uptake + c.garden
    eat = min(c.people * c.food_c, max(0.0, s.food / dt + h * fixed))
    breathe_co2 = c.people * c.food_c * aerobic
    body = breathe_co2 - eat                               # > 0: the store is empty, bodies make up the rest
    breathe_o2 = breathe_co2 / c.rq
    labile_decay = c.k_labile * s.labile * aerobic
    stable_decay = c.k_stable * s.stable * aerobic
    excess = min(s.excess, max(0.0, s.stable / dt - stable_decay)) * aerobic   # a burst draws on the humus
    soil = (1 - c.humification) * labile_decay + stable_decay + excess
    growth = c.veg_rate * s.veg * (1 - s.veg / c.veg_max)
    litter = c.k_litter * s.veg
    npp = growth + litter                                  # the valley fixes what it grows and sheds
    # Controls, only above or below their targets, and never taking more CO2 than the step leaves.
    other = breathe_co2 + soil - fixed - npp - c.leak * s.co2
    available = max(0.0, s.co2 / dt + other)
    over = max(0.0, p_co2 - c.co2_target) / rt if c.co2_target else 0.0
    under = max(0.0, c.o2_target - s.o2 * rt) / rt if c.o2_target else 0.0
    regen = min(c.regen, max(over, under) / 3600, available) if (c.regen and (over or under)) else 0.0
    scrub = min(c.scrub, max(0.0, over / 3600 - regen), available - regen) if c.scrub else 0.0
    return {
        "uptake": uptake, "garden": c.garden, "farm_co2": farm_co2, "eat": eat, "breathe_o2": breathe_o2,
        "breathe_co2": breathe_co2, "body": body, "soil": soil, "labile_decay": labile_decay,
        "stable_decay": stable_decay, "excess": excess, "growth": growth, "litter": litter, "npp": npp,
        "regen": regen, "scrub": scrub,
        "d_o2": fixed * (h / c.rq + 1 - h) + npp - breathe_o2 - soil + regen - c.leak * s.o2,
        "d_co2": breathe_co2 + soil - fixed - npp - regen - scrub - c.leak * s.co2,
        "d_n2": -c.leak * s.n2,
        "d_food": h * fixed - eat,
        "d_labile": (1 - h) * fixed + litter - labile_decay,
        "d_stable": c.humification * labile_decay - stable_decay - excess,
        "d_veg": growth,
        "d_body": body,
        "d_removed": regen + scrub,
        "d_excess": -c.k_excess * s.excess,
    }


def run(c, years, dt=3600.0, lit=None, events=(), state=None, record_every=DAY):
    """Integrate (explicit Euler). events: (time s, dict of Config changes) applied from that time on.
    Returns the recorded series: time, partial pressures, pools, and the first times limits were crossed."""
    s = state or initial(c)
    lit = c.lit if lit is None else lit
    events = sorted(events, key=lambda e: e[0])
    t, end, k = 0.0, years * YEAR, 0
    out = {"t": [], "o2": [], "co2": [], "o2_frac": [], "total": [], "food_days": [], "labile": [], "stable": [],
           "veg": [], "soil": [], "uptake": [], "farm_co2": [], "regen": [], "scrub": [], "body": []}
    next_record = 0.0
    while t <= end:
        while k < len(events) and events[k][0] <= t:
            changes = dict(events[k][1])
            lit = changes.pop("lit", lit)
            c = replace(c, **changes)
            if "soil_excess" in changes:
                s.excess = c.soil_excess
            k += 1
        f = fluxes(c, s, lit, dt)
        if t >= next_record:
            pr = pressures(c, s)
            for key in ("o2", "co2", "o2_frac", "total"):
                out[key].append(pr[key])
            out["t"].append(t)
            out["food_days"].append(s.food / max(c.people * c.food_c * DAY, 1e-30))
            for key in ("labile", "stable", "veg", "body"):
                out[key].append(getattr(s, key))
            for key in ("soil", "uptake", "farm_co2", "regen", "scrub"):
                out[key].append(f[key])
            next_record += record_every
        s.o2 += f["d_o2"] * dt
        s.co2 += f["d_co2"] * dt
        s.n2 += f["d_n2"] * dt
        s.food += f["d_food"] * dt
        s.labile += f["d_labile"] * dt
        s.stable += f["d_stable"] * dt
        s.veg += f["d_veg"] * dt
        s.body += f["d_body"] * dt
        s.removed += f["d_removed"] * dt
        s.excess += f["d_excess"] * dt
        t += dt
    return out


def first_crossing(series, key, limit, above=True):
    """Days until series[key] first crosses limit (None if never)."""
    for t, v in zip(series["t"], series[key]):
        if (v > limit) if above else (v < limit):
            return t / DAY
    return None
