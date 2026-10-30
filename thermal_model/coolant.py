"""Coolant loops between the heat sources and the radiators, in spin gravity (plan §6).

Spin gravity points outward along the spokes, so a fluid's potential per kg is -omega^2 r^2 / 2 and "up"
is towards the hub. Between radii r_a and r_b a column of density rho holds rho omega^2 (r_a^2 - r_b^2) / 2.

- Main section: the valleys sit at the rim and their radiators inboard (0.4 r to the drum), so warm coolant
  rises to the radiators and cooled coolant sinks back: natural circulation, no pumps.
- Farm section: the farm rings sit at 0.4 r. Radiators outboard of them (the baseline, out to ~1 r) need the
  warm coolant to sink, against its buoyancy: pumped loops. Radiators inboard would run passively.

Single-phase water is sized for each; two-phase ammonia is checked for boiling at the source, where the
liquid column returning from the radiators raises the pressure far above saturation.
"""

import math

G_REF = 9.80665
WATER = {"rho": 1000.0, "cp": 4186.0, "beta": 2.1e-4, "mu": 1.1e-3}        # ~15-20 °C
# Ammonia, saturated near 285 K: liquid density, vapour density, latent heat, saturation pressure, and the
# molar heat of vaporisation for Clausius-Clapeyron (general handbook values, rounded; unsourced).
AMMONIA = {"rho_l": 620.0, "rho_v": 5.0, "h_fg": 1.22e6, "p_sat": 6.2e5, "t_sat": 285.0, "dh_mol": 23.3e3,
           "molar": 0.017031}
WATER_SAT = {"p_sat": 1.4e3, "t_sat": 285.0, "dh_mol": 44.0e3, "molar": 0.018015}
R_GAS = 8.314462618


def potential(omega, r_a, r_b):
    """Specific potential drop (J/kg) going outward from r_b to r_a (r_a > r_b)."""
    return omega ** 2 * (r_a ** 2 - r_b ** 2) / 2


def annulus_centroid(r_in, r_out):
    """Area centroid radius of an annulus: where the radiators' heat leaves the coolant on average."""
    return 2 / 3 * (r_out ** 3 - r_in ** 3) / (r_out ** 2 - r_in ** 2)


def friction_factor(re):
    """Smooth pipe, turbulent (Blasius below 1e5, McAdams above); laminar 64/Re."""
    if re < 2300:
        return 64 / re
    return 0.316 * re ** -0.25 if re < 1e5 else 0.184 * re ** -0.2


def pipe_drop(m_dot, diameter, length, fluid=WATER):
    """Friction pressure drop (Pa) of water flowing at m_dot (kg/s) through a pipe."""
    area = math.pi * diameter ** 2 / 4
    v = m_dot / (fluid["rho"] * area)
    re = fluid["rho"] * v * diameter / fluid["mu"]
    return friction_factor(re) * length / diameter * fluid["rho"] * v ** 2 / 2, v


def size_natural(q, omega, r_source, r_sink, dt, loops, fluid=WATER):
    """Single-phase natural circulation: the pipe diameter at which friction around the loop (out and back)
    uses up the buoyancy head of a dt-warm leg. Returns per-loop flow, diameter, speed and head."""
    m_dot = q / loops / (fluid["cp"] * dt)
    head = fluid["rho"] * fluid["beta"] * dt * potential(omega, r_source, r_sink)
    length = 2 * (r_source - r_sink)
    lo, hi = 0.01, 10.0
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        lo, hi = (mid, hi) if pipe_drop(m_dot, mid, length, fluid)[0] > head else (lo, mid)
    d = hi
    return {"m_dot": m_dot, "diameter": d, "speed": pipe_drop(m_dot, d, length, fluid)[1], "head": head,
            "length": length, "inventory": loops * length * math.pi * d ** 2 / 4 * fluid["rho"]}


def size_pumped(q, omega, r_source, r_sink, dt, loops, speed=2.0, pump_efficiency=0.7, fluid=WATER):
    """Single-phase pumped loop with radiators outboard of the source: the pump overcomes friction and the
    buoyancy that opposes the flow (warm coolant must sink). Pipes sized for a set speed."""
    m_dot = q / loops / (fluid["cp"] * dt)
    d = math.sqrt(4 * m_dot / (fluid["rho"] * speed * math.pi))
    length = 2 * abs(r_sink - r_source)
    friction, _ = pipe_drop(m_dot, d, length, fluid)
    opposing = fluid["rho"] * fluid["beta"] * dt * potential(omega, r_sink, r_source)
    power = loops * m_dot / fluid["rho"] * (friction + opposing) / pump_efficiency
    return {"m_dot": m_dot, "diameter": d, "friction": friction, "opposing": opposing, "pump_power": power,
            "length": length, "inventory": loops * length * math.pi * d ** 2 / 4 * fluid["rho"]}


def saturation_temperature(p, sat):
    """Clausius-Clapeyron from one reference point."""
    return 1 / (1 / sat["t_sat"] - R_GAS / (sat["dh_mol"] / 1.0) * math.log(p / sat["p_sat"]))


def two_phase_rim(omega, r_source, r_sink, rho_liquid, sat):
    """Pressure and saturation temperature where the liquid returns to the evaporator at r_source, with
    condensation at sat["t_sat"] at r_sink: the liquid column suppresses boiling unless it is throttled."""
    p = sat["p_sat"] + rho_liquid * potential(omega, r_source, r_sink)
    return {"pressure": p, "t_sat": saturation_temperature(p, sat)}
