"""Dose inside the torus's tube (plan §3): rays traced through its cross-section.

The tube is a circle of radius a = w/2 (`habitat_model.geometry`), wrapped in the rock jacket, thinner by
the fill's credit under the floor; the floor's fill (~1 m of soil and regolith) lines the bottom of the tube
over the lower half of the tube, as the system model credits it (`habitat_model.mass`). With a tube radius ~1/16 of the torus's radius, the tube is
taken as straight and endless: a ray leaving at an angle ψ to its axis crosses 1/sin ψ times the shield its
projection on the cross-section does. The neighbouring tori, the hub and the farm section, which hide part
of the sky in a stack, are left out (so the dose here is an upper bound for inner tori).

Along each ray the shield is counted as tailings: the high-energy dose per steradian behind L g/cm² of
tailings comes from `shield.Model.profile`; the slow neutrons from the wall are the slab's (`neutrons.py`),
the same everywhere in the tube.
"""

import math

import numpy as np

FILL_HALF_ANGLE = math.radians(90)        # the fill lines the lower half, as the mass model credits it


def directions(n, seed=11):
    """Unit vectors evenly over the sphere (Fibonacci lattice); z is along the tube."""
    i = np.arange(n) + 0.5
    z = 1 - 2 * i / n
    phi = math.pi * (1 + 5 ** 0.5) * i
    r = np.sqrt(1 - z ** 2)
    return np.stack([r * np.cos(phi), r * np.sin(phi), z], axis=1)


def layout(geo, p):
    """The cross-section, in metres: tube radius, jacket thickness (and under the fill), fill depth."""
    a = geo["tube_radius"]
    jacket = geo["jacket"]
    fill = p.fill_depth_m
    soil, regolith = fill * p.fill_soil_frac, fill * (1 - p.fill_soil_frac)
    fill_density = (soil * p.soil_density + regolith * p.regolith_density) / fill
    # The jacket is thinned under the fill by the fill's rock-equivalent mass (as `habitat_model.mass`).
    solids = p.soil_density - p.soil_water_vol_frac
    rock_eq = regolith * p.regolith_density + soil * (solids + p.soil_water_vol_frac * p.rock_per_water_shield)
    credit = rock_eq / p.rock_density
    return {"a": a, "jacket": jacket, "jacket_under_fill": max(jacket - credit, 0.0), "fill": fill,
            "fill_density": fill_density, "rock_density": p.rock_density}


def paths(lay, point, dirs, samples=1500):
    """Areal density (g/cm²) of rock and of fill along each direction from a point (x, y) in the
    cross-section (y up, towards the hub; the floor at y = −a)."""
    a, t, tf, f = lay["a"], lay["jacket"], lay["jacket_under_fill"], lay["fill"]
    q = np.hypot(dirs[:, 0], dirs[:, 1])
    ok = q > 1e-6
    ux = np.where(ok, dirs[:, 0] / np.maximum(q, 1e-12), 0)
    uy = np.where(ok, dirs[:, 1] / np.maximum(q, 1e-12), 0)
    reach = 2 * (a + t) + 2
    s = (np.arange(samples) + 0.5) / samples * reach
    ds = reach / samples
    x = point[0] + ux[:, None] * s[None, :]
    y = point[1] + uy[:, None] * s[None, :]
    rho = np.hypot(x, y)
    from_bottom = np.abs(np.arctan2(x, -y))                 # 0 straight down
    under_fill = from_bottom < FILL_HALF_ANGLE
    outer = a + np.where(under_fill, tf, t)
    rock = (rho >= a) & (rho < outer)
    fill = under_fill & (rho >= a - f) & (rho < a)
    to_g_cm2 = 100.0                                          # t/m³ × m → t/m² → g/cm²
    rock_l = rock.sum(axis=1) * ds * lay["rock_density"] * to_g_cm2
    fill_l = fill.sum(axis=1) * ds * lay["fill_density"] * to_g_cm2
    scale = np.where(ok, 1 / np.maximum(q, 1e-12), np.inf)
    return rock_l * scale, fill_l * scale


def dose_at(lay, point, ray, neutron_floor, n_dirs=6000, cover=None):
    """Dose equivalent (mSv/yr) at a point: ray(L) is the high-energy dose per sr behind L g/cm² of
    tailings (mSv/yr/sr), neutron_floor the slow neutrons' dose from the walls (mSv/yr). cover: an extra
    areal density (g/cm²) on every ray leaving towards the valley's interior (a dwelling in the cliff),
    given as (g/cm², the inward normal (x, y))."""
    dirs = directions(n_dirs)
    rock, fill = paths(lay, point, dirs)
    total = rock + fill
    if cover is not None:
        extra, normal = cover
        facing = dirs[:, 0] * normal[0] + dirs[:, 1] * normal[1] > 0
        total = total + np.where(facing, extra, 0.0)
    total = np.where(np.isfinite(total), total, 1e9)
    high = (4 * math.pi / n_dirs) * ray(total).sum()
    return high + neutron_floor, high
