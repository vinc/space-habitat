"""Heat rejection: radiators on the spokes venting through the stack's two open ends (§13)."""

SIGMA = 5.670374419e-8


def radiator_flux(temp_k):
    """Black-body flux at the radiator temperature, W/m^2."""
    return SIGMA * temp_k ** 4


def compute(p, d, geo, power):
    flux = radiator_flux(p.radiator_temp_k)
    per_torus = power["total"]            # all electricity ends up as heat
    stack = d.n_tori * per_torus
    capacity = 2 * geo["end_opening"] * flux
    surface = per_torus / flux
    return {
        "flux": flux,
        "per_torus": per_torus,
        "stack": stack,
        "openings": 2 * geo["end_opening"],
        "capacity": capacity,
        "margin": capacity / stack,
        "break_even_tori": capacity / per_torus,
        "radiating_surface": surface,
        "radiating_surface_valley": power["valley"] / flux,
        "radiating_surface_per_tier": power["farm_per_tier"] / flux,
        "panel_area": surface / 2,          # two-sided panels
        "panel_mass": surface / 2 * p.radiator_kg_m2,
    }
