"""Water per torus, by use, and where it comes from (plan §5).

The system model sizes the parts (`habitat_model.mass`); this module lays out the budget and compares three
ways to supply it: ship water from the C-type, or ship only its hydrogen (as H2 or as methane) and take the
oxygen from the S-type's silicates, a by-product of molten-oxide electrolysis (notes §10, proposed).
"""

from habitat_model.mass import M_H2O

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
        "Lakes and streams": m["water_lakes"],
        "Electrolysed for the O₂ (valley and farm ring)": m["water_o2"],
        "Ballast": m["water_ballast"],
        "Vegetation": m["water_biomass"],
    }
    total = sum(uses.values())
    spinup = m["spinup_propellant"]
    return {"uses": uses, "total": total, "spinup": spinup,
            "needed": total + (spinup if water_spinup else 0.0),
            "c_type_contains": r["materials"]["c_water_contained"]}


def routes(p, d, r):
    """Mass shipped per torus and the energy to supply its water, by route (kg, J).
    The N2 and organics are shipped in every route; methane's carbon counts against the organics."""
    m, mat, rep = r["mass"], r["materials"], r["replication"]
    water = mat["water_to_source"]
    n2 = m["n2"] + m["farm_n2"]
    organics = p.organics_shipped_t_m2 * 1e3 * r["geometry"]["floor_area"]
    per_kg = rep["shipping"] / rep["shipped"] if rep["shipping"] is not None else None
    hydrogen = water * H_PER_WATER
    oxygen = water * O_PER_WATER
    methane = hydrogen / H_IN_CH4
    carbon = methane * C_IN_CH4

    # Oxygen from the silicates: molten-oxide electrolysis frees ~0.29 kg per kg of iron. A host whose free
    # metal falls short of the steel gets that much iron this way at no extra cost; beyond it, the iron
    # reduced only for its oxygen costs the electrolysis.
    shortfall = max(0.0, mat["metal_needed"] - mat["s_for_rock"] * _metal_fraction(p, d.host_class))
    iron_for_oxygen = oxygen / O_PER_FE
    extra_iron = max(0.0, iron_for_oxygen - shortfall)
    moe = extra_iron * p.moe_mj_kg_fe * 1e6
    split = water * p.electrolysis_mj_kg_water * 1e6       # at the C-type, to free the hydrogen

    out = {}
    for name, cargo, energy in (
        ("Water", water + n2 + organics, 0.0),
        ("Hydrogen (H₂), oxygen from the silicates", hydrogen + n2 + organics, split + moe),
        ("Methane, oxygen from the silicates", methane + n2 + max(0.0, organics - carbon), split + moe),
    ):
        shipping = cargo * per_kg if per_kg is not None else None
        out[name] = {"shipped": cargo, "shipping": shipping, "other_energy": energy,
                     "total": None if shipping is None else shipping + energy}
    return {"routes": out, "iron_for_oxygen": iron_for_oxygen, "iron_shortfall": shortfall,
            "extra_iron": extra_iron, "hydrogen": hydrogen, "carbon_in_methane": carbon, "organics": organics}


def _metal_fraction(p, host_class):
    return {"H": p.metal_wt_H, "L": p.metal_wt_L, "LL": p.metal_wt_LL}[host_class]
