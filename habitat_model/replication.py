"""Processing and replication: crushing, baking, shipping volatiles and generation time (§5e, §13, §15)."""

import math

from .design import DELTA_V_KM_S

YEAR = 365.25 * 86400
GW_YR = 1e9 * YEAR


def shipping_energy_per_kg(p, delta_v_km_s):
    """Electric propulsion, per kg delivered: 1/2 (e^(dv/ve) - 1) ve^2 / efficiency (§15)."""
    ve = p.ep_exhaust_km_s * 1e3
    return 0.5 * (math.exp(delta_v_km_s * 1e3 / ve) - 1) * ve ** 2 / p.ep_efficiency


def compute(p, d, geo, mass, materials):
    crushing = materials["s_type"] * p.crush_mj_kg * 1e6
    baking = materials["c_type"] * p.bake_mj_kg * 1e6
    processing = crushing + baking

    # The C-type is refined at its source; only the products are shipped (§15).
    shipped = mass["n2"] + materials["water_to_source"] + p.organics_shipped_t_m2 * 1e3 * geo["floor_area"]
    dv = d.delta_v_km_s if d.delta_v_km_s is not None else DELTA_V_KM_S.get((d.c_partner, d.site))
    shipping = shipped * shipping_energy_per_kg(p, dv) if dv is not None else 0.0

    per_torus = processing + shipping
    stack = d.n_tori * per_torus
    return {
        "crushing": crushing,
        "baking": baking,
        "processing": processing,
        "shipped": shipped,
        "delta_v_km_s": dv,
        "shipping": shipping,
        "energy_per_torus": per_torus,
        "energy_stack": stack,
        # Energy alone; logistics and factory throughput are the real pacing items (§13).
        "generation_time_yr": stack / (d.factory_power_gw * 1e9) / YEAR,
    }
