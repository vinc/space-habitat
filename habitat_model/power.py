"""Power and light: valley sky, farm tiers, other loads and the despun solar array (§13, §15)."""

import math

from .design import SITES
from .food import DAY


def farm_efficacy(p):
    """The farm's lamps (umol/J at the wall): `farm_lamp_efficacy_umol_j`, or the valley's when it is 0."""
    return p.farm_lamp_efficacy_umol_j or p.lamp_efficacy_umol_j


def array_area(p, power_w, sunlight):
    """Despun array sized so that, locked to the stack, it still delivers power_w (m^2)."""
    return power_w / p.locked_output_frac / (p.solar_constant_w_m2 * p.pv_efficiency * sunlight)


def compute(p, d, geo):
    lamp = p.lamp_efficacy_umol_j * 1e-6   # mol/J
    floor = geo["floor_area"]
    sky = floor * p.valley_light_mol / DAY / lamp / p.ceiling_delivery
    other = floor * p.other_loads_w_m2
    valley = sky + other
    per_tier = geo["crop_area_per_tier"] * p.crop_light_mol / DAY / (farm_efficacy(p) * 1e-6) / p.farm_delivery
    total = valley + d.tiers_lit * per_tier

    # At the site: the valley's share sized at aphelion (half the sky with the seasonal sky),
    # the farm at full output all year (§15).
    sunlight = SITES[d.site].aphelion_sunlight
    valley_site = (sky * p.seasonal_sky_frac if d.seasonal_sky else sky) + other
    array_site_valley = array_area(p, valley_site, sunlight)
    array_site_per_tier = array_area(p, per_tier, sunlight)
    array_site = array_site_valley + d.tiers_lit * array_site_per_tier

    return {
        "valley_sky": sky,
        "other_loads": other,
        "valley": valley,
        "farm_per_tier": per_tier,
        "total": total,
        # Panels on the rim, lit half of every turn: ~1/pi of full sunlight (§13).
        "plain_rim_pv": floor * p.solar_constant_w_m2 * p.pv_efficiency / math.pi,
        # Constant sky at 1 AU, as in §0.
        "array_1au_valley": array_area(p, valley, 1.0),
        "array_1au_per_tier": array_area(p, per_tier, 1.0),
        "array_1au": array_area(p, total, 1.0),
        "site_aphelion_sunlight": sunlight,
        "array_site_valley": array_site_valley,
        "array_site_per_tier": array_site_per_tier,
        "array_site": array_site,
        "array_site_mass": array_site * p.array_kg_m2,
        # Sunlight a concentrator must collect for the same need (no survival factor), §13.
        "sunlight_needed": total / p.pv_efficiency,
    }
