"""Stocks and flows of a generation (plan §5): what a parent's factory must handle to build a child torus in a given
time, what each child is made of by source, and how a cluster grows until a source body runs out.

A parent stack builds a child stack torus by torus, so the cluster doubles once per generation, the time a
stack's factory takes to build one torus per torus of its own. Energy sets a floor on it (`habitat_model`);
the rates below are what the factory's lines must sustain for longer generations.
"""

import math

from habitat_model.design import SITES
from habitat_model.materials import REFERENCE_FLOOR_900, tori_supported

DAY = 86400.0
YEAR = 365.25 * DAY

# Earth benchmarks, orders of magnitude (general knowledge, unsourced): the largest open-pit mines move
# ~0.5 Mt of material a day; a large integrated steelworks makes ~10 Mt of steel a year.
MINE_KG_DAY = 5e8
STEELWORKS_KG_DAY = 1e10 / 365.25


def composition(p, r):
    """What a torus is made of, by source (kg): the host's rock and metal, the C-type's shipped products,
    imported vitamins. The torus with its share of the hub and factory metal, its farm ring and its array."""
    m, mat, rep, pw = r["mass"], r["materials"], r["replication"], r["power"]
    built = m["total"] + m["steel"] * p.hub_factory_metal_frac + m["farm_total"] + pw["array_site_mass"]
    vitamins = pw["array_site"] * p.pv_silicon_kg_m2 + p.other_vitamins_t * 1e3 * r["geometry"]["floor_area"] / REFERENCE_FLOOR_900
    shipped = rep["shipped"]
    return {"built": built, "host": built - shipped - vitamins, "shipped": shipped, "vitamins": vitamins,
            "local_share": (built - shipped - vitamins) / built, "asteroid_share": (built - vitamins) / built}


def rates(r, years, window_years):
    """Rates a parent's lines must sustain to build one torus in `years` (kg/day, kg per shipping window, W)."""
    m, mat, rep = r["mass"], r["materials"], r["replication"]
    per_day = 1 / (years * YEAR / DAY)
    energy = rep["energy_per_torus"]
    return {
        "s_type_day": mat["s_type"] * per_day,
        "metal_day": mat["metal_needed"] * per_day,
        "rock_placed_day": (m["shield"] + m["fill"]) * per_day,
        "c_type_day": mat["c_type"] * per_day,
        "shipped_per_window": rep["shipped"] * window_years / years,
        "power": None if energy is None else energy / (years * YEAR),
    }


def growth(p, d, r, generation_years, horizon_years=(50, 100)):
    """Tori in a cluster started by one stack, doubling every generation, and when its C-type runs short."""
    supported = tori_supported(p, SITES[d.c_partner], r["mass"], r["materials"])
    doublings_to_limit = math.log2(supported / d.n_tori) if supported and supported > d.n_tori else 0.0
    return {
        "after": {t: d.n_tori * 2 ** (t / generation_years) for t in horizon_years},
        "c_type_supports": supported,
        "years_to_c_limit": doublings_to_limit * generation_years,
    }
