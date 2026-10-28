"""Materials and mining: S-type for metal and shield, C-type sized by nitrogen (§7, §10, §15)."""

import math

# §10, trace elements: (S-type ordinary chondrite, C-type Ryugu), ppm by mass.
# None where the notes give no value. S-type majors are H values (less in L, LL).
TRACE_PPM = {
    "Cu": (91, 126),
    "Ni": (16000, 11900),
    "Co": (800, 582),
    "Cr": (None, 2681),
    "Mn": (2300, 2489),
    "Ti": (600, 474),
    "Zn": (50, 346),
    "P": (1100, 1302),
    "K": (800, 522),
    "Na": (6000, 6099),
    "Cl": (None, 776),
    "B": (None, 1.33),
    "Li": (1.3, 1.38),
    "Ga": (5.5, 10),
    "Ge": (9.5, 33),
    "Mo": (2, 1.02),
    "W": (None, 0.125),
    "Sn": (0.46, 1.85),
    "Ag": (0.051, 0.195),
}


def metal_fraction(p, host_class):
    return {"H": p.metal_wt_H, "L": p.metal_wt_L, "LL": p.metal_wt_LL}[host_class]


def sphere_diameter(mass_kg, bulk_density_t_m3):
    """d = (6 M / (pi rho))^(1/3)."""
    return (6 * mass_kg / (math.pi * bulk_density_t_m3 * 1e3)) ** (1 / 3)


def s_type_needed(p, mass, host_class):
    """S-type rock per torus: enough free metal for the steel, and enough tailings for shield and regolith."""
    f = metal_fraction(p, host_class)
    metal = mass["steel"] * (1 + p.hub_factory_metal_frac)
    silicate = mass["shield"] + mass["regolith"]
    for_metal = metal / f
    for_rock = silicate / (1 - f)
    return {
        "metal_needed": metal,
        "silicate_needed": silicate,
        "s_for_metal": for_metal,
        "s_for_rock": for_rock,
        "s_type": max(for_metal, for_rock),
        "s_sized_by": "metal" if for_metal > for_rock else "shield",
    }


def compute(p, d, geo, mass):
    s = s_type_needed(p, mass, d.host_class)
    tailings = s["s_type"] * (1 - metal_fraction(p, d.host_class))

    water = mass["water_needed"] + (mass["spinup_propellant"] if d.water_spinup else 0.0)
    c_for_n = mass["n2"] / (p.c_nitrogen_wt * p.nitrogen_recovery)
    c_for_water = water / p.c_water_wt
    c_type = max(c_for_n, c_for_water)

    trace = {}
    for element, (s_ppm, c_ppm) in TRACE_PPM.items():
        trace[element] = {
            "s_type": None if s_ppm is None else s["s_type"] * s_ppm * 1e-6,
            "c_type": c_type * c_ppm * 1e-6,
        }

    return {
        **s,
        "tailings": tailings,
        "spare_tailings": tailings - s["silicate_needed"],
        "s_diameter": sphere_diameter(s["s_type"], p.s_bulk_density),
        "water_to_source": water,
        "c_for_nitrogen": c_for_n,
        "c_for_water": c_for_water,
        "c_type": c_type,
        "c_sized_by": "water" if c_for_water > c_for_n else "nitrogen",
        "c_diameter": sphere_diameter(c_type, p.c_bulk_density),
        "c_water_contained": c_type * p.c_water_wt,
        "c_carbon_contained": c_type * p.c_carbon_wt,
        "mined": s["s_type"] + c_type,
        "trace": trace,
    }


def tori_supported(p, body, mass, materials):
    """How many tori of this size a body supplies: an S-type by its own class's free metal, a C-type by nitrogen."""
    if body.mass_mt is None:
        return None
    if body.kind == "S":
        needed = s_type_needed(p, mass, body.host_class)["s_type"]
    else:
        needed = materials["c_type"]
    return body.mass_mt * 1e9 / needed
