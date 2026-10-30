"""A prism light pipe fed from both ends (plan §7, notes §13).

Light enters each end inside the film's acceptance cone and travels by total internal reflection. At each
reflection the film absorbs a share (`film_loss_per_reflection`). A white extractor strip inside the pipe
scatters out of the cone whatever lands on it (a share `extractor_efficiency` leaves through the film, the
rest is absorbed), and its width along the pipe is graded so the pipe glows evenly. What reaches the far
end goes into the other lamp's reflector, which returns a share (`pipe_end_return`).

Rays are grouped into classes by their angle to the axis and their impact parameter (skew rays reflect more
often). A class reflects tan θ / (2 √(R² − b²)) times per metre. Each class is followed along the pipe in
segments, both ways, and the extractor's coverage is solved for even output on a quadrature of classes,
then checked on a large independent random sample.
"""

import math

import numpy as np


def quadrature(cone_deg, n_angle=16, n_skew=16):
    """Ray classes on a midpoint grid of equal weights: evenly in solid angle within the cone, and in impact
    parameter b / R by its distribution (4/π) √(1 − b²) for light entering evenly over the face in every
    transverse direction. Returns (tan θ, b / R)."""
    u = (np.arange(n_angle) + 0.5) / n_angle
    cos_t = 1 - u * (1 - math.cos(math.radians(cone_deg)))
    # Inverse of the cumulative distribution (2/π)(b √(1 − b²) + asin b), by interpolation.
    grid = np.linspace(0, 1, 20001)
    cdf = (2 / math.pi) * (grid * np.sqrt(1 - grid ** 2) + np.arcsin(grid))
    b = np.interp((np.arange(n_skew) + 0.5) / n_skew, cdf, grid)
    tan_t = np.sqrt(1 - cos_t ** 2) / cos_t
    return np.repeat(tan_t, n_skew), np.tile(b, n_angle)


def classes(cone_deg, n=600, seed=1):
    """Ray classes sampled at random, filling the acceptance cone evenly in solid angle and the pipe's face
    evenly in area: (tan θ, b / R), with equal weights. For checking the quadrature."""
    rng = np.random.default_rng(seed)
    cos_t = 1 - rng.random(n) * (1 - math.cos(math.radians(cone_deg)))
    # A point uniform in the unit disc and a transverse direction uniform in angle: |impact parameter|.
    r = np.sqrt(rng.random(n))
    a = 2 * math.pi * rng.random(n)
    psi = 2 * math.pi * rng.random(n)
    b = np.abs(r * np.sin(a - psi))
    return np.sqrt(1 - cos_t ** 2) / cos_t, np.minimum(b, 0.995)


def _march(f, nu, dz, loss, eta_x, inject):
    """One direction: every class followed along the segments for extractor coverage f (per reflection),
    starting with `inject` per class. Returns what each segment emits, what the film and the extractor
    absorb, and what reaches the far end, per class."""
    n_seg = len(f)
    emitted, film, extractor = np.empty(n_seg), np.empty(n_seg), np.empty(n_seg)
    x = inject.copy()
    reflections = nu * dz
    for j in range(n_seg):
        survive = ((1 - f[j]) * (1 - loss)) ** reflections
        removed = (x * (1 - survive)).sum()
        share = f[j] / (f[j] + loss * (1 - f[j])) if f[j] + loss > 0 else 0.0
        emitted[j] = removed * share * eta_x
        extractor[j] = removed * share * (1 - eta_x)
        film[j] = removed * (1 - share)
        x = x * survive
    return emitted, film, extractor, x


def evaluate(f, length, diameter, cone_deg, loss, eta_x, end_return, rays=None):
    """Both lamps feeding, extractor coverage f per segment (symmetric about the middle), for the ray
    classes `rays` (default: the quadrature). Per unit of light the lamps put in: emitted per segment, and
    the losses."""
    tan_t, b = quadrature(cone_deg) if rays is None else rays
    nu = tan_t / (diameter * np.sqrt(1 - b ** 2))       # reflections per metre: tan θ / (2 √(R² − b²))
    dz = length / len(f)
    one = np.full(nu.size, 1.0 / nu.size)
    # Light reaching the far end goes into the other lamp's reflector, which sends a share back the other
    # way, and so on: per class, a geometric series. By symmetry each direction carries the same.
    t = _march(f, nu, dz, loss, eta_x, one)[3] * nu.size
    e, film, extractor, out = _march(f, nu, dz, loss, eta_x, one / (1 - end_return * t))
    emitted = (e + e[::-1]) / 2                          # the other direction is the mirror image
    return {
        "emitted": emitted,                              # per segment, of what the lamps put in
        "efficiency": emitted.sum(),
        "film": film.sum(),
        "extractor": extractor.sum(),
        "ends": out.sum() * (1 - end_return),
        "uniformity": emitted.min() / emitted.mean(),
    }


def design(length, diameter, cone_deg, loss, eta_x, end_return, f_max, n_seg=40, tol=0.01, n_check=20_000):
    """Grade the extractor for even output and the most light out: the largest output per metre for which
    a coverage profile (at most f_max per reflection) gives an even glow within tol, solved on the
    quadrature. The profile is then checked on n_check independently sampled ray classes, whose glow and
    losses are what is returned."""
    rays = quadrature(cone_deg)

    def solve(q):
        f = np.full(n_seg, min(f_max, 0.01))
        for _ in range(200):
            r = evaluate(f, length, diameter, cone_deg, loss, eta_x, end_return, rays)
            ratio = q / np.maximum(r["emitted"], 1e-15)
            g = np.minimum(f_max, f * ratio ** 0.8)
            g = (g + g[::-1]) / 2                         # keep it symmetric
            if np.max(np.abs(g - f)) < 1e-6:
                break
            f = g
        r = evaluate(f, length, diameter, cone_deg, loss, eta_x, end_return, rays)
        return f, r, np.max(np.abs(r["emitted"] / q - 1)) < tol

    lo, hi = 0.0, 1.0 / n_seg                            # all the light out, evenly
    best = None
    for _ in range(30):
        q = (lo + hi) / 2
        f, r, ok = solve(q)
        if ok:
            lo, best = q, (f, r)
        else:
            hi = q
    if best is None:
        raise ValueError("no even extraction profile found")
    f, r = best
    check = evaluate(f, length, diameter, cone_deg, loss, eta_x, end_return, classes(cone_deg, n_check, seed=7))
    return {**check, "peak": check["emitted"].max() / check["emitted"].mean(),
            "design_uniformity": r["uniformity"], "coverage": f, "segments": n_seg}


def efficiency(p, length=None):
    """The configured pipe: share of the light entering it that it emits, with its losses."""
    return design(p.pipe_length_m if length is None else length, p.pipe_diameter_m, p.pipe_cone_deg,
                  p.film_loss_per_reflection, p.extractor_efficiency, p.pipe_end_return, p.extractor_max_frac)
