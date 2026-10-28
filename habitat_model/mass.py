"""Mass per torus: air, rock shield, fill, water, hull, cable spokes and extras (§3c, §5c, §6, §7, §9, §13)."""

import math

R_GAS = 8.314462618
M_N2 = 0.0280134
M_O2 = 0.031998
M_H2O = 0.0180153
WATER_PER_O2 = 2 * M_H2O / M_O2   # 2 H2O -> 2 H2 + O2: ~1.126 kg of water per kg of O2


def air(p, geo):
    """N2 and O2 masses (kg) at the design pressure, keeping sea-level O2 partial pressure."""
    rt = R_GAS * p.air_temperature_k
    p_n2 = (p.pressure_kpa - p.o2_partial_kpa) * 1e3
    p_o2 = p.o2_partial_kpa * 1e3
    return {
        "n2": p_n2 * geo["volume"] * M_N2 / rt,
        "o2": p_o2 * geo["volume"] * M_O2 / rt,
    }


def spoke_factor(p, rim_speed):
    """Uniform cable spokes of length r holding a rim: M_spokes / M_rim = rho v^2 / (sigma - rho v^2 / 2)."""
    rho_v2 = p.steel_density * rim_speed ** 2
    sigma = p.wire_stress_mpa * 1e6
    if sigma <= rho_v2 / 2:
        raise ValueError(f"spokes diverge: rho v^2 / 2 = {rho_v2 / 2e6:.0f} MPa >= {p.wire_stress_mpa} MPa")
    return rho_v2 / (sigma - rho_v2 / 2)


def compute(p, d, geo):
    floor = geo["floor_area"]
    gases = air(p, geo)

    # Rock jacket, with the fill under the floor credited as shielding (§5e, §6).
    shield_gross = p.shield_areal_t_m2 * 1e3 * geo["hull_area"]
    fill_credit = p.fill_water_equiv_t_m2 * p.rock_per_water_shield * 1e3 * floor
    shield = shield_gross - fill_credit

    soil_depth = p.fill_depth_m * p.fill_soil_frac
    regolith_depth = p.fill_depth_m - soil_depth
    soil = soil_depth * p.soil_density * 1e3 * floor
    regolith = regolith_depth * p.regolith_density * 1e3 * floor

    # Water to source: soil moisture, lakes, and the water electrolysed for the O2.
    # The soil's water is already in its moist density, and the electrolysed water
    # is in the air as O2, so only the lakes add mass on the rim.
    water_soil = soil_depth * p.soil_water_vol_frac * 1e3 * floor
    water_lakes = p.lake_water_t_m2 * 1e3 * floor
    water_o2 = gases["o2"] * WATER_PER_O2
    water_needed = water_soil + water_lakes + water_o2

    hull_1g = p.hull_frames_ref_mt * 1e9 * (geo["radius"] / p.hull_frames_ref_radius_m) ** p.hull_frames_exponent
    hull = hull_1g * max(p.hull_min_gauge_frac, d.g)

    rim = shield + soil + regolith + water_lakes + gases["n2"] + gases["o2"] + hull
    spokes = rim * spoke_factor(p, geo["rim_speed"])
    total = rim + spokes

    farm_ring = (geo["farm_shell_area"] * p.farm_shell_m * p.steel_density
                 + p.farm_growing_kg_m2 * geo["crop_area_per_tier"] * p.farm_tiers_built)

    return {
        "n2": gases["n2"],
        "o2": gases["o2"],
        "air": gases["n2"] + gases["o2"],
        "shield_gross": shield_gross,
        "fill_credit": fill_credit,
        "shield": shield,
        "soil": soil,
        "regolith": regolith,
        "fill": soil + regolith,
        "water_soil": water_soil,
        "water_lakes": water_lakes,
        "water_o2": water_o2,
        "water_needed": water_needed,
        "hull_frames": hull,
        "rim": rim,
        "spokes": spokes,
        "steel": hull + spokes,
        "total": total,
        "per_floor": total / floor,
        "spinup_propellant": total * geo["rim_speed"] / (p.spinup_exhaust_km_s * 1e3),
        # Not on the rim, so not carried by the spokes and not in the total (§13).
        "farm_ring": farm_ring,
    }
