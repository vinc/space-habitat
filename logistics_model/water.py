"""Water per torus, by use, and where it comes from (plan §5).

The system model sizes the parts (`habitat_model.mass`); this module lays out the budget and compares three
ways to supply it: ship water from the C-type, or ship only its hydrogen (as H2 or as methane) and take the
oxygen from the S-type's silicates, a by-product of molten-oxide electrolysis (notes §10, proposed).
"""

from habitat_model.mass import M_H2O

from . import propulsion

M_H, M_O, M_C, M_FE, M_CH4 = 0.001008, 0.015999, 0.012011, 0.055845, 0.016043
H_PER_WATER = 2 * M_H / M_H2O               # ~0.112 kg of hydrogen per kg of water
O_PER_WATER = M_O / M_H2O                   # ~0.888
O_PER_FE = M_O / M_FE                       # FeO -> Fe + O: ~0.286 kg of oxygen per kg of iron
H_IN_CH4, C_IN_CH4 = 4 * M_H / M_CH4, M_C / M_CH4


def budget(r, water_spinup=False):
    """Water per torus by use (kg), from the system model's results."""
    m = r["mass"]
    uses = {
        "Soil moisture": m["water_soil"],
        "Ponds and streams": m["water_lakes"],
        "Electrolysed for the O₂ (valley and farm ring)": m["water_o2"],
        "Ballast": m["water_ballast"],
        "Vegetation": m["water_biomass"],
    }
    total = sum(uses.values())
    spinup = m["spinup_propellant"]
    return {"uses": uses, "total": total, "spinup": spinup,
            "needed": total + (spinup if water_spinup else 0.0),
            "c_type_contains": r["materials"]["c_water_contained"]}


def routes(p, d, r, per_kg=None):
    """Mass shipped per torus and the energy to supply it, by route (kg, J). per_kg: shipping energy per kg
    delivered (default: the system model's electric thrusters). The N2 and organics are shipped in every route;
    methane's carbon counts against the organics.

    The baseline host gets all its metal as free metal and electrolyses nothing, so the water's oxygen is
    charged in full: molten-oxide electrolysis of ~3.1 kg of iron per kg of water (~0.29 kg of oxygen per kg
    of iron), its electricity and the furnace heat to melt the rock, less the crushing of the free-metal rock
    that iron replaces. A host that electrolyses its silicates for iron anyway would get the oxygen free."""
    m, mat, rep = r["mass"], r["materials"], r["replication"]
    water = mat["water_to_source"]
    n2 = m["n2"] + m["farm_n2"]
    organics = p.organics_shipped_t_m2 * 1e3 * r["geometry"]["floor_area"]
    if per_kg is None:
        per_kg = rep["shipping"] / rep["shipped"] if rep["shipping"] is not None else None
    hydrogen = water * H_PER_WATER
    oxygen = water * O_PER_WATER
    methane = hydrogen / H_IN_CH4
    carbon = methane * C_IN_CH4

    iron = oxygen / O_PER_FE
    f = _metal_fraction(p, d.host_class)
    rock_saved = min(iron / f, max(0.0, mat["s_for_metal"] - mat["s_for_rock"]))
    local_oxygen = {
        "split": water * p.electrolysis_mj_kg_water * 1e6,      # at the C-type, to free the hydrogen
        "moe_electric": iron * p.moe_mj_kg_fe * 1e6,
        "moe_heat": iron * p.moe_heat_mj_kg_fe * 1e6,
        "crushing_saved": rock_saved * p.crush_mj_kg * 1e6,
    }
    other = (local_oxygen["split"] + local_oxygen["moe_electric"] + local_oxygen["moe_heat"]
             - local_oxygen["crushing_saved"])

    out = {}
    for name, cargo, energy in (
        ("Water", water + n2 + organics, 0.0),
        ("Hydrogen (H₂), oxygen from the silicates", hydrogen + n2 + organics, other),
        ("Methane, oxygen from the silicates", methane + n2 + max(0.0, organics - carbon), other),
    ):
        shipping = cargo * per_kg if per_kg is not None else None
        out[name] = {"shipped": cargo, "shipping": shipping, "other_energy": energy,
                     "total": None if shipping is None else shipping + energy}
    return {"routes": out, "iron_for_oxygen": iron, "rock_saved": rock_saved, "local_oxygen": local_oxygen,
            "hydrogen": hydrogen, "carbon_in_methane": carbon, "organics": organics}


def supply(p, d, r):
    """Every route with every freighter: electric thrusters (the system model's) and the energy-optimal mass
    driver on the C-type's baked residue. Returns {(route, engine): {shipped, shipping, other_energy, total}} (J)."""
    rep, mat = r["replication"], r["materials"]
    residue = mat["c_type"] * (1 - p.c_water_wt - p.c_carbon_wt)
    out = {}
    for route, v in routes(p, d, r)["routes"].items():
        out[(route, "Electric thrusters")] = v
        md = propulsion.options(p, rep["delta_v_km_s"] * 1e3, v["shipped"], residue, 0.0)[2]
        out[(route, "Mass driver")] = {"shipped": v["shipped"], "shipping": md["energy"],
                                       "other_energy": v["other_energy"], "total": md["energy"] + v["other_energy"]}
    return out


def _metal_fraction(p, host_class):
    return {"H": p.metal_wt_H, "L": p.metal_wt_L, "LL": p.metal_wt_LL}[host_class]
