"""Neutrons below 20 MeV in the shield: two-group diffusion across a layered slab (plan §3).

The transport (`transport.py`) counts the neutrons that fall below 20 MeV along each ray: evaporation from
struck nuclei and the cascade's slow end. Inside a shield thick against their mean free path they scatter
and diffuse, so they are followed here in one dimension across the shield: a fast group (~0.1–20 MeV) that
diffuses and is slowed into a thermal group, which diffuses and is absorbed (`physics.neutron_groups`).
Hydrogen slows them in a few collisions; in dry rock they take dozens and wander far.

Boundaries: at the outer face neutrons leave for good (Marshak's vacuum condition); at the inner face they
cross the habitat and enter the wall again elsewhere, so the inner face reflects (no net current), and the
fluence inside the habitat equals the fluence at the wall's inner face.

The source per g/cm² of depth x adds up every incoming direction: s(x) = 2π ∫ P(x/μ) dμ, with P the
production per g/cm² of path along a ray at slant depth x/μ.
"""

import math

import numpy as np

from . import physics


def _solve(d, sig, src, h):
    """−(D φ')' + Σ φ = S on cells of width h; vacuum (Marshak) at cell 0's outer face, reflecting at the
    last cell's. d, sig, src: per cell. Returns φ per cell."""
    n = len(d)
    a = np.zeros(n)
    b = sig * h
    c = np.zeros(n)
    face = 2 * d[:-1] * d[1:] / (d[:-1] + d[1:]) / h                 # harmonic D at inner faces, over h
    b[:-1] += face
    b[1:] += face
    c[:-1] = -face
    a[1:] = -face
    b[0] += (d[0] / h) / (0.5 + 2 * d[0] / h)                           # leakage through the outer face
    r = src * h
    # Thomas algorithm.
    cp = np.zeros(n)
    rp = np.zeros(n)
    cp[0] = c[0] / b[0]
    rp[0] = r[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m if i < n - 1 else 0.0
        rp[i] = (r[i] - a[i] * rp[i - 1]) / m
    phi = np.zeros(n)
    phi[-1] = rp[-1]
    for i in range(n - 2, -1, -1):
        phi[i] = rp[i] - cp[i] * phi[i + 1]
    return phi


def fluence(layers, source, cells=400):
    """Fast and thermal neutron fluence rates at the inner face of a slab of layers [(Material, g/cm²)],
    outer first, with source(x) the neutrons per cm² per s per g/cm² of depth. Returns (fast, thermal),
    per cm² per s, and the profile."""
    total = sum(t for _, t in layers)
    if total <= 0:
        return 0.0, 0.0, None
    h = total / cells
    x = (np.arange(cells) + 0.5) * h
    bounds = np.cumsum([t for _, t in layers])
    which = np.searchsorted(bounds, x, side="right").clip(0, len(layers) - 1)
    groups = [physics.neutron_groups(m) for m, _ in layers]
    tr_f = np.array([groups[k][0][0] for k in which])
    rem = np.array([groups[k][0][1] for k in which])
    tr_t = np.array([groups[k][1][0] for k in which])
    ab = np.array([groups[k][1][1] for k in which])
    s = source(x)
    fast = _solve(1 / (3 * tr_f), rem, s, h)
    thermal = _solve(1 / (3 * tr_t), ab, rem * fast, h)
    return fast[-1], thermal[-1], {"x": x, "fast": fast, "thermal": thermal}


def slab_source(production, mu_points=10, cap=4000.0):
    """s(x) from a ray's production P(L) per g/cm² of path (a callable), over incoming directions."""
    mu, w = np.polynomial.legendre.leggauss(mu_points)
    mu, w = 0.5 * (mu + 1), 0.5 * w

    def s(x):
        x = np.asarray(x, float)
        total = np.zeros_like(x)
        for m, wt in zip(mu, w):
            path = x / m
            total += wt * np.where(path < cap, production(path, m), 0.0)
        return 2 * math.pi * total
    return s
