"""Passive spin stability of a rigid co-rotating stack of thin rings (§11)."""

import math


def inertia_ratio(n, radius, pitch):
    """I_axis / I_transverse for n equal thin rings of this radius, spaced by pitch along the axis."""
    offsets = [(i - (n - 1) / 2) * pitch for i in range(n)]
    i_axis = n * radius ** 2
    i_transverse = n * radius ** 2 / 2 + sum(z * z for z in offsets)
    return i_axis / i_transverse


def max_tori(radius, pitch, margin):
    """Largest n with I_axis > (1 + margin) I_transverse: n^2 - 1 < 12 (r/p)^2 [1/(1+m) - 1/2]."""
    k = 12 * (radius / pitch) ** 2 * (1 / (1 + margin) - 0.5)
    return math.floor(math.sqrt(1 + k)) if k > 0 else 0


def stack_items(geo, n, torus_mass, farm_mass):
    """(mass, radius, z) of every ring of the whole stack: n tori, then the farm section."""
    pitch, fp = geo["pitch"], geo["farm_pitch"]
    items = [(torus_mass, geo["radius"], (k + 0.5) * pitch) for k in range(n)]
    start = n * pitch + geo["farm_section_gap"]
    items += [(farm_mass, geo["farm_radius"], start + (k + 0.5) * fp) for k in range(n)]
    return items


def stack_ratio(items):
    """I_axis / I_transverse of thin rings (mass, radius, z) about the stack's centre of mass."""
    total = sum(m for m, _, _ in items)
    zc = sum(m * z for m, _, z in items) / total
    i_axis = sum(m * r * r for m, r, _ in items)
    i_transverse = sum(m * r * r / 2 + m * (z - zc) ** 2 for m, r, z in items)
    return i_axis / i_transverse


def compute(p, d, geo, torus_mass=None, farm_mass=None):
    """Main section alone (closed form, as in §11), and the whole stack with its farm section."""
    r, pitch = geo["radius"], geo["pitch"]
    ratio = inertia_ratio(d.n_tori, r, pitch)
    limit = max_tori(r, pitch, p.stability_margin)
    out = {
        "inertia_ratio": ratio,
        "margin": ratio - 1,
        "stable": ratio > 1 + p.stability_margin,
        "max_tori": limit,
        "max_tori_no_margin": max_tori(r, pitch, 0.0),
        "max_tori_10pct": max_tori(r, pitch, 0.1),
        "stack_length_at_limit": limit * pitch,
    }
    if torus_mass is not None:
        whole = stack_ratio(stack_items(geo, d.n_tori, torus_mass, farm_mass))
        n = 1
        while stack_ratio(stack_items(geo, n + 1, torus_mass, farm_mass)) > 1 + p.stability_margin and n < 200:
            n += 1
        out.update({
            "whole_inertia_ratio": whole,
            "whole_stable": whole > 1 + p.stability_margin,
            "whole_max_tori": n,
        })
    return out
