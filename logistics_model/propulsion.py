"""Propulsion for the volatile freighters (plan §5): energy and propellant per kg delivered, by option.

Rocket equation with an electric (or electromagnetic) engine of exhaust speed ve and efficiency eta, per kg
delivered over a delta-v dv: propellant e^(dv/ve) - 1, jet energy (e^(dv/ve) - 1) ve^2 / 2, electricity that
over eta. For a fixed dv the electricity is lowest at ve = dv / 1.594 (x e^x = 2 (e^x - 1)): fast exhaust
saves propellant, not energy. Impulsive delta-v is used throughout; low-thrust transfers need somewhat more.
"""

import math

X_OPT = 1.5936242600400401      # root of x e^x = 2 (e^x - 1)


def per_kg(dv, ve, efficiency):
    """Propellant (kg) and electricity (J) per kg delivered."""
    ratio = math.exp(dv / ve) - 1
    return ratio, 0.5 * ratio * ve ** 2 / efficiency


def energy_optimal_ve(dv, max_propellant_ratio=None):
    """The exhaust speed that minimises electricity per kg delivered, with an optional cap on propellant per kg."""
    x = X_OPT
    if max_propellant_ratio is not None:
        x = min(x, math.log1p(max_propellant_ratio))
    return dv / x


def options(p, dv, shipped, c_type_residue, spare_water):
    """Each option's exhaust speed, propellant and electricity per torus's cargo (kg, J).
    c_type_residue: the C-type's dry residue after baking (a mass driver's reaction mass);
    spare_water: water the C-type holds beyond the cargo (an electrothermal thruster's propellant)."""
    md_ve = energy_optimal_ve(dv, c_type_residue / shipped)
    rows = [
        ("Electric thrusters (baseline)", p.ep_exhaust_km_s * 1e3, p.ep_efficiency,
         "local metal or oxygen (xenon is a vitamin)", None),
        ("Electrothermal, water", p.electrothermal_exhaust_km_s * 1e3, p.electrothermal_efficiency,
         "the C-type's spare water", spare_water),
        ("Mass driver, energy-optimal", md_ve, p.mass_driver_efficiency,
         "the C-type's baked residue", c_type_residue),
    ]
    out = []
    for name, ve, eta, source, available in rows:
        ratio, energy = per_kg(dv, ve, eta)
        out.append({"name": name, "ve": ve, "efficiency": eta, "source": source,
                    "propellant": ratio * shipped, "energy": energy * shipped, "available": available,
                    "fits": available is None or ratio * shipped <= available,
                    # Thrust per watt of electricity: 2 eta / ve.
                    "thrust_per_w": 2 * eta / ve})
    return out
