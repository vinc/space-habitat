"""Tangent-chord cable net: geometry, tension along a chord, taper, mass and bowing (notes §12, plan §2).

Each chord runs straight from rim to rim, passing at a distance c from the spin axis
(tangent to a circle slightly larger than the hub). Every rim anchor carries two chords,
one of each handedness, so their pulls along the rim cancel ("crossed lacing").

In the rotating frame a chord element at distance s from its tangent point feels
w^2 s along the chord and w^2 c across it (away from the axis). So:
  - along the chord, tension peaks at the tangent point, as at the hub end of a radial spoke:
      dT/ds = -mu w^2 s
  - across it, the chord bows away from the axis: y'' = -mu w^2 c / T
"""

import math

import numpy as np


def chord_geometry(radius, tangent_radius):
    c, r = tangent_radius, radius
    theta = math.asin(c / r)                     # angle of the chord from the inward radial, at the rim
    half_length = math.sqrt(r * r - c * c)
    return {
        "tangent_radius": c,
        "theta": theta,
        "half_length": half_length,
        "span_angle": math.pi - 2 * theta,      # angle between a chord's two rim ends
        "offset_arc": 2 * theta * r,             # how far a chord's far end lands from the point opposite
        "efficiency": math.cos(theta),           # radial share of the chord's pull at the rim
    }


def chord_mass_factor(rim_speed, stress_pa, density, cos_theta, tapered):
    """Net mass / rim mass for a rim held at rim_speed (independent of the number of chords).

    Uniform chords sized for the stress at the tangent point:
        rho v^2 / (sigma - rho v^2 cos^2(theta) / 2)
    Tapered chords at uniform stress (area ~ exp(rho w^2 (L^2 - s^2) / 2 sigma)):
        rho v^2 * integral_0^1 exp(b (1 - u^2)) du,  b = rho v^2 cos^2(theta) / (2 sigma)
    With cos(theta) = 1 these are radial spokes; the uniform form is the system model's formula.
    """
    k = density * rim_speed ** 2 / stress_pa
    b = k * cos_theta ** 2 / 2
    if not tapered:
        if b >= 1:
            raise ValueError("uniform chords diverge")
        return k / (1 - b)
    u = np.linspace(0.0, 1.0, 2001)
    return k * float(np.trapezoid(np.exp(b * (1 - u * u)), u))


def anchor_tension(rim_mass, omega, radius, n_chords, cos_theta):
    """Tension at each chord end: 2 n_chords ends share the rim's total radial pull M w^2 r."""
    return rim_mass * omega ** 2 * radius / (2 * n_chords * cos_theta)


def bowing(omega, tangent_radius, half_length, stress_pa, density):
    """Mid-chord bow away from the axis for a uniform-stress chord: y = rho w^2 c L^2 / (2 sigma)."""
    return density * omega ** 2 * tangent_radius * half_length ** 2 / (2 * stress_pa)


def compute(radius, rim_mass, omega, hub_radius, stress_pa, density, anchor_spacing=10.0, tangent_margin=1.1):
    """One anchor (two chord ends) every anchor_spacing metres of rim, so as many chords as anchors."""
    n_chords = round(2 * math.pi * radius / anchor_spacing)
    c = tangent_margin * hub_radius
    g = chord_geometry(radius, c)
    v = omega * radius
    uniform = chord_mass_factor(v, stress_pa, density, g["efficiency"], tapered=False)
    tapered = chord_mass_factor(v, stress_pa, density, g["efficiency"], tapered=True)
    radial = chord_mass_factor(v, stress_pa, density, 1.0, tapered=False)
    t_end = anchor_tension(rim_mass, omega, radius, n_chords, g["efficiency"])
    self_load = density * v ** 2 * g["efficiency"] ** 2 / 2   # stress the chord's own spin adds at mid-chord
    return {
        **g,
        "n_chords": n_chords,
        "anchor_spacing": 2 * math.pi * radius / n_chords,
        "mass_uniform": uniform * rim_mass,
        "mass_tapered": tapered * rim_mass,
        "mass_radial": radial * rim_mass,
        "taper_saving": 1 - tapered / uniform,
        "chord_vs_radial": uniform / radial - 1,
        "tension_end": t_end,
        "tension_mid_uniform": t_end * stress_pa / (stress_pa - self_load),
        "self_load_stress": self_load,
        "taper_ratio": math.exp(density * v ** 2 * g["efficiency"] ** 2 / (2 * stress_pa)),
        # A tapered chord at uniform stress needs t_end / sigma at its ends and more toward the middle;
        # a uniform chord needs one area all along, sized where its own spin load adds most (mid-chord).
        "wire_area_tapered_end": t_end / stress_pa,
        "wire_area_uniform": t_end / (stress_pa - self_load),
        "uniform_peak_stress": t_end / (t_end / (stress_pa - self_load)) + self_load,
        "bow": bowing(omega, c, g["half_length"], stress_pa, density),
    }
