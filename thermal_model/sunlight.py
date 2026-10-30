"""Sunlight on the radiators (plan §6).

The spin axis points at the ecliptic pole (notes §11), so sunlight arrives in the panel planes, edge-on. Any
tilt delta of the axis away from the orbit's pole (alignment, the orbit plane's slow drift, the Sun's own
0.27° radius) lets it fall on one face of every panel at sin(delta), unless something shades them: the tori
(their envelopes, as true tori) around the drum, the hub, the farm rings.

Sun rays are parametrised by where they cross the plane through the axis normal to the Sun (x = 0), and
marched (sphere tracing on the signed distance to the tori, hub and farm rings) until they hit a solid; the
panel planes they cross before that intercept the coverage share of what is left. The panels absorb a share
alpha (solar absorptivity) of what they intercept; the result is set against what they radiate.
"""

import math

import numpy as np

from habitat_model.cavity import _farm_band
from habitat_model.heat import radiator_flux

SOLAR = 1361.0       # W/m² at 1 AU


def _bodies(geo, n):
    tori = np.array([(k + 0.5) * geo["pitch"] for k in range(n)])
    start = geo["main_length"] + geo["farm_section_gap"]
    rings = np.array([start + (k + 0.5) * geo["farm_pitch"] for k in range(n)])
    return tori, rings


def _distance(x, y, z, geo, tori, rings):
    """Signed distance to the nearest solid: the tori's envelopes, the hub, the farm rings."""
    rho = np.hypot(x, y)
    centre = geo["radius"] - geo["tube_radius"]
    dz = np.min(np.abs(z[:, None] - tori[None, :]), axis=1)
    d_tori = np.hypot(rho - centre, dz) - geo["envelope_radius"]
    d_hub = rho - geo["hub_radius"]
    # Farm rings: boxes in (rho, z), the ring's height radially and its width along the axis.
    qr = np.abs(rho - (geo["farm_radius"] + geo["farm_height"] / 2)) - geo["farm_height"] / 2
    qz = np.min(np.abs(z[:, None] - rings[None, :]), axis=1) - geo["farm_width"] / 2
    d_rings = np.hypot(np.maximum(qr, 0), np.maximum(qz, 0)) + np.minimum(np.maximum(qr, qz), 0)
    return np.minimum(np.minimum(d_tori, d_hub), d_rings)


def absorbed(geo, n, tilt_deg, coverage, layout="outboard", absorptivity=0.15, rays=60000, seed=0,
             min_step=0.1, max_steps=6000):
    """Sunlight absorbed by each section's panels at 1 AU (W), for an axis tilted tilt_deg from the
    orbit's pole. coverage: (main, farm) share of each panel annulus."""
    rng = np.random.default_rng(seed)
    tilt = math.radians(tilt_deg)
    ux, uz = math.cos(tilt), math.sin(tilt)
    tori, rings = _bodies(geo, n)
    farm_band = _farm_band(geo, layout)
    planes = [(z, (geo["radiator_inner"], geo["drum_radius"]), coverage[0], 0) for z in tori]
    planes += [(z, farm_band, coverage[1], 1) for z in rings]
    planes.sort()
    reach = max(geo["envelope_outer"], farm_band[1]) + 10.0
    span = reach * uz
    z_lo, z_hi = -span, geo["stack_length"] + span
    y = rng.uniform(-reach, reach, rays)
    zc = rng.uniform(z_lo, z_hi, rays)
    weight = (2 * reach) * (z_hi - z_lo) * ux / rays         # beam cross-section per ray, m²

    # March from s = -reach to the first solid.
    s = np.full(rays, -reach)
    hit = np.full(rays, np.inf)
    alive = np.ones(rays, dtype=bool)
    for _ in range(max_steps):
        if not alive.any():
            break
        idx = np.flatnonzero(alive)
        d = _distance(s[idx] * ux, y[idx], zc[idx] + s[idx] * uz, geo, tori, rings)
        solid = d < min_step / 2
        hit[idx[solid]] = s[idx[solid]]
        s[idx] += np.maximum(d, min_step)
        alive[idx[solid]] = False
        alive &= s < reach

    out = np.zeros(2)
    transmitted = np.ones(rays)
    if uz > 0:
        for z, (r_in, r_out), f, group in planes:
            sk = (z - zc) / uz
            rho = np.hypot(sk * ux, y)
            crosses = (sk > -reach) & (sk < np.minimum(hit, reach)) & (rho >= r_in) & (rho <= r_out)
            intercepted = np.where(crosses, transmitted * f, 0.0)
            out[group] += intercepted.sum()
            transmitted -= intercepted
    return {"main": absorptivity * SOLAR * weight * out[0], "farm": absorptivity * SOLAR * weight * out[1]}


def emission(p, geo, n, coverage, layout="outboard"):
    """What each section's panels radiate (W): both faces, at the radiator temperature."""
    flux = p.radiator_emissivity * radiator_flux(p.radiator_temp_k)
    main = n * coverage[0] * math.pi * (geo["drum_radius"] ** 2 - geo["radiator_inner"] ** 2)
    b = _farm_band(geo, layout)
    farm = n * coverage[1] * math.pi * (b[1] ** 2 - b[0] ** 2)
    return {"main": 2 * flux * main, "farm": 2 * flux * farm}
