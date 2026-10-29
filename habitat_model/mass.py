"""Mass per torus: air, rock shield, fill, water, hull, cable spokes and extras (§3c, §5c, §6, §7, §9, §13)."""

import math

R_GAS = 8.314462618
M_N2 = 0.0280134
M_O2 = 0.031998
M_H2O = 0.0180153
WATER_PER_O2 = 2 * M_H2O / M_O2   # 2 H2O -> 2 H2 + O2: ~1.126 kg of water per kg of O2


def air(p, volume, pressure_kpa):
    """N2 and O2 masses (kg) at a total pressure, keeping sea-level O2 partial pressure."""
    if pressure_kpa <= p.o2_partial_kpa:
        raise ValueError(f"pressure {pressure_kpa} kPa is at or below the O2 partial pressure")
    rt = R_GAS * p.air_temperature_k
    p_n2 = (pressure_kpa - p.o2_partial_kpa) * 1e3
    p_o2 = p.o2_partial_kpa * 1e3
    return {
        "n2": p_n2 * volume * M_N2 / rt,
        "o2": p_o2 * volume * M_O2 / rt,
    }


def outer_half_ring_volume(centre, r_in, r_out):
    """Volume of the outer half (away from the spin axis) of a ring section between r_in and r_out
    around a centre line of radius `centre` (Pappus, with the half-annulus centroid)."""
    if r_out <= r_in:
        return 0.0
    area = math.pi / 2 * (r_out ** 2 - r_in ** 2)
    centroid = centre + 4 * (r_out ** 3 - r_in ** 3) / (3 * math.pi * (r_out ** 2 - r_in ** 2))
    return 2 * math.pi * centroid * area


def spoke_factor(p, rim_speed):
    """Uniform cable spokes of length r holding a rim: M_spokes / M_rim = rho v^2 / (sigma - rho v^2 / 2)."""
    rho_v2 = p.steel_density * rim_speed ** 2
    sigma = p.wire_stress_mpa * 1e6
    if sigma <= rho_v2 / 2:
        raise ValueError(f"spokes diverge: rho v^2 / 2 = {rho_v2 / 2e6:.0f} MPa >= {p.wire_stress_mpa} MPa")
    return rho_v2 / (sigma - rho_v2 / 2)


def compute(p, d, geo):
    floor = geo["floor_area"]
    gases = air(p, geo["volume"], p.pressure_kpa)

    soil_depth = p.fill_depth_m * p.fill_soil_frac
    regolith_depth = p.fill_depth_m - soil_depth

    # Rock jacket of finite thickness around the tube (§5e). The fill under the floor shields
    # like rock of the same rock-equivalent mass (regolith 1:1, the soil's water at the
    # rock/water equivalence, §6), so the jacket is thinned by that much on its outer face
    # under the floor's footprint.
    rho = p.rock_density * 1e3
    a, t, centre = geo["tube_radius"], geo["jacket"], geo["radius"] - geo["tube_radius"]
    shield_gross = 2 * math.pi ** 2 * centre * ((a + t) ** 2 - a ** 2) * rho
    soil_solids = p.soil_density - p.soil_water_vol_frac
    fill_rock_eq = (regolith_depth * p.regolith_density
                    + soil_depth * (soil_solids + p.soil_water_vol_frac * p.rock_per_water_shield))  # t/m2
    thinning = min(t, fill_rock_eq / p.rock_density)
    footprint = min(1.0, floor / (2 * math.pi ** 2 * centre * a))   # share of the tube's outer half under the floor
    fill_credit = footprint * outer_half_ring_volume(centre, a + t - thinning, a + t) * rho
    shield = shield_gross - fill_credit
    soil = soil_depth * p.soil_density * 1e3 * floor
    regolith = regolith_depth * p.regolith_density * 1e3 * floor

    # Water to source: soil moisture, lakes, the water electrolysed for the O2, ballast and the
    # vegetation's water. The soil's water is already in its moist density, and the electrolysed
    # water is in the air as O2, so lakes, ballast and vegetation add mass on the rim.
    water_soil = soil_depth * p.soil_water_vol_frac * 1e3 * floor
    water_lakes = p.lake_floor_frac * p.lake_depth_m * 1e3 * floor
    water_biomass = p.biomass_water_kg_m2 * floor
    farm_air = air(p, geo["farm_volume"], p.farm_pressure_kpa)
    water_o2 = (gases["o2"] + farm_air["o2"]) * WATER_PER_O2       # the valley's O2 and the farm ring's

    hull_1g = p.hull_frames_ref_mt * 1e9 * (geo["radius"] / p.hull_frames_ref_radius_m) ** p.hull_frames_exponent
    hull = hull_1g * max(p.hull_min_gauge_frac, d.g)

    dry_rim = shield + soil + regolith + water_lakes + water_biomass + gases["n2"] + gases["o2"] + hull
    # Ballast: a first-harmonic imbalance e of the rim's mass is trimmed by water distributed as
    # 1 - cos around the rim, e M in all, in tanks holding up to twice the mean.
    water_ballast = p.ballast_frac * dry_rim
    water_needed = water_soil + water_lakes + water_o2 + water_ballast + water_biomass
    rim = dry_rim + water_ballast
    spokes = rim * spoke_factor(p, geo["rim_speed"])
    total = rim + spokes

    # Farm section, per farm ring: shell and growing systems, its own spokes (the ring is the
    # rim they hold, at the farm's rim speed), and its own atmosphere.
    farm_shell = geo["farm_shell_area"] * p.farm_shell_m * p.steel_density
    farm_ring = farm_shell + p.farm_growing_kg_m2 * geo["crop_area_per_tier"] * p.farm_tiers_built
    farm_spokes = (farm_ring + farm_air["n2"] + farm_air["o2"]) * spoke_factor(p, geo["farm_rim_speed"])

    return {
        "n2": gases["n2"],
        "o2": gases["o2"],
        "air": gases["n2"] + gases["o2"],
        "shield_gross": shield_gross,
        "fill_credit": fill_credit,
        "fill_rock_eq": fill_rock_eq * 1e3,   # kg/m2
        "shield": shield,
        "soil": soil,
        "regolith": regolith,
        "fill": soil + regolith,
        "water_soil": water_soil,
        "water_lakes": water_lakes,
        "water_o2": water_o2,
        "water_ballast": water_ballast,
        "water_biomass": water_biomass,
        "water_needed": water_needed,
        "hull_frames": hull,
        "rim": rim,
        "spokes": spokes,
        "steel": hull + spokes,
        "total": total,
        "per_floor": total / floor,
        "spinup_propellant": total * geo["rim_speed"] / (p.spinup_exhaust_km_s * 1e3),
        # Not on the rim, so not carried by the spokes and not in the total (§13).
        "farm_ring": farm_ring,                 # shell and growing systems, as in the notes
        "farm_spokes": farm_spokes,
        "farm_steel": farm_shell + farm_spokes,
        "farm_n2": farm_air["n2"],
        "farm_o2": farm_air["o2"],
        "farm_total": farm_ring + farm_spokes + farm_air["n2"] + farm_air["o2"],
    }
