"""Heat rejection, per section (§13).

Main section: the valleys' heat, from radiators on the tori's spokes in the drum between hub and
tori, venting through the drum's two open ends (and the side gaps). Ideal limit: both end
openings as black bodies at the radiator temperature.

Farm section: the farm tiers' heat, from radiators on the farm rings' own spokes, in an open
stack with no tori around it (cavity.py models it; there is no enclosed-drum ideal limit).
"""

SIGMA = 5.670374419e-8


def radiator_flux(temp_k):
    """Black-body flux at the radiator temperature, W/m^2."""
    return SIGMA * temp_k ** 4


def compute(p, d, geo, power):
    flux = radiator_flux(p.radiator_temp_k)
    main = power["valley"]                     # all electricity ends up as heat
    farm = d.tiers_lit * power["farm_per_tier"]
    capacity = 2 * geo["end_opening"] * flux
    surface = (main + farm) / flux
    return {
        "flux": flux,
        "per_torus": main + farm,
        "stack": d.n_tori * (main + farm),
        "main_per_torus": main,
        "main_stack": d.n_tori * main,
        "farm_per_ring": farm,
        "farm_stack": d.n_tori * farm,
        "openings": 2 * geo["end_opening"],
        "capacity": capacity,                  # ideal limit of the main section's drum
        "margin": capacity / (d.n_tori * main),
        "break_even_tori": capacity / main,
        "radiating_surface": surface,          # black body, both sections, lower bound
        "radiating_surface_valley": power["valley"] / flux,
        "radiating_surface_per_tier": power["farm_per_tier"] / flux,
        "panel_area": surface / 2,             # two-sided panels
        "panel_mass": surface / 2 * p.radiator_kg_m2,
    }
