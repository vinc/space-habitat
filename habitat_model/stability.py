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


def compute(p, d, geo):
    r, pitch = geo["radius"], geo["pitch"]
    ratio = inertia_ratio(d.n_tori, r, pitch)
    limit = max_tori(r, pitch, p.stability_margin)
    return {
        "inertia_ratio": ratio,
        "margin": ratio - 1,
        "stable": ratio > 1 + p.stability_margin,
        "max_tori": limit,
        "max_tori_no_margin": max_tori(r, pitch, 0.0),
        "max_tori_10pct": max_tori(r, pitch, 0.1),
        "stack_length_at_limit": limit * pitch,
    }
