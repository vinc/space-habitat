"""Preliminary radiative exchange in the drum between hub and tori (plan §6, brought forward).

The ideal limit (heat.py) treats the two end openings as black bodies at the radiator
temperature. Here the radiators are finite panels, and their radiation has to find its way
out of the drum, by Monte Carlo ray tracing:

- the drum: the space from the hub (radius r_hub) out to the inner edge of the tori's
  envelopes (radius R_d), from z = 0 to the stack length L along the spin axis;
- escape paths: the two end openings (z = 0, z = L), and optionally the side gaps between
  neighbouring envelopes (rays reaching R_d between two envelopes leave the drum);
- radiator panels: two-sided, in each torus plane, on the spokes between the farm ring and
  R_d, facing along the axis, covering a fraction f of that annulus (each crossing of the
  plane meets a panel with probability f); emissivity eps, diffuse;
- the farm rings (cylinder bands at ~0.4 r, 0.9 w wide), the hub and the envelopes' inner
  faces: insulated (the rock jacket is a near-perfect insulator), so they absorb and
  re-emit diffusely all they receive;
- all panels at one temperature, so radiation one panel sends to another is no net gain:
  the net output is eps sigma T^4 A_panels times the probability that an emitted ray
  escapes before it is absorbed by a panel.

Not included: sunlight entering through the gaps, spokes and cables, the despun array
and dock, the envelopes' rounded shape (taken as a cylinder at R_d), and the actual
radiator layout; the sink is taken at ~0 K.
"""

import math

import numpy as np

from .heat import radiator_flux

EPS = 1e-6


def _diffuse(normal, rng):
    """Cosine-weighted directions about unit normals (n, 3)."""
    n = len(normal)
    u1, u2 = rng.random(n), rng.random(n)
    sin_t, cos_t = np.sqrt(u1), np.sqrt(1 - u1)
    phi = 2 * math.pi * u2
    helper = np.where(np.abs(normal[:, 0:1]) < 0.9, [[1.0, 0, 0]], [[0, 1.0, 0]])
    t1 = np.cross(normal, helper)
    t1 /= np.linalg.norm(t1, axis=1, keepdims=True)
    t2 = np.cross(normal, t1)
    return (sin_t * np.cos(phi))[:, None] * t1 + (sin_t * np.sin(phi))[:, None] * t2 + cos_t[:, None] * normal


def _cylinder_roots(pos, d, radius):
    a = d[:, 0] ** 2 + d[:, 1] ** 2
    b = 2 * (pos[:, 0] * d[:, 0] + pos[:, 1] * d[:, 1])
    c = pos[:, 0] ** 2 + pos[:, 1] ** 2 - radius ** 2
    disc = b * b - 4 * a * c
    ok = (disc >= 0) & (a > 1e-12)
    sq = np.sqrt(np.where(ok, disc, 0.0))
    a_safe = np.where(a > 1e-12, a, 1.0)
    t1 = np.where(ok, (-b - sq) / (2 * a_safe), np.inf)
    t2 = np.where(ok, (-b + sq) / (2 * a_safe), np.inf)
    return t1, t2


def _first_in_band(pos, d, t1, t2, pitch, n_bands, half_width):
    """Smallest positive root whose z falls within a band centred on a torus plane ((k + 1/2) pitch)."""
    best = np.full(len(pos), np.inf)
    for t in (t2, t1):  # t1 <= t2: checked last, so it wins when both qualify
        z = pos[:, 2] + np.where(np.isfinite(t), t, 0.0) * d[:, 2]
        k = np.clip(np.floor(z / pitch), 0, n_bands - 1)
        in_band = (t > EPS) & np.isfinite(t) & (np.abs(z - (k + 0.5) * pitch) <= half_width)
        best = np.where(in_band, t, best)
    return best


def escape_probability(geo, n_tori, coverage, emissivity, side_gaps=True, n_rays=20000, seed=0, max_steps=5000):
    rng = np.random.default_rng(seed)
    pitch, r_hub, r_drum = geo["pitch"], geo["hub_radius"], geo["drum_radius"]
    length = n_tori * pitch
    planes = (np.arange(n_tori) + 0.5) * pitch
    env = geo["envelope_radius"]
    farm_r = geo["farm_radius"]
    farm_half = geo["farm_width"] / 2
    r_in = geo["farm_radius"] + geo["farm_height"]

    # Emission: uniform over the panel annuli, either face, cosine-weighted.
    n = n_rays
    k = rng.integers(0, n_tori, n)
    rr = np.sqrt(rng.uniform(r_in ** 2, r_drum ** 2, n))
    ph = rng.uniform(0, 2 * math.pi, n)
    pos = np.stack([rr * np.cos(ph), rr * np.sin(ph), planes[k]], axis=1)
    side = np.where(rng.random(n) < 0.5, 1.0, -1.0)
    d = _diffuse(np.stack([np.zeros(n), np.zeros(n), side], axis=1), rng)
    pos = pos + EPS * 10 * d

    fate = np.zeros(n, dtype=int)   # 0 alive, 1 escaped by an end, 2 escaped by a gap, 3 absorbed
    for _ in range(max_steps):
        alive = fate == 0
        if not alive.any():
            break
        p, v = pos[alive], d[alive]
        m = len(p)
        dz = v[:, 2]
        safe_dz = np.where(np.abs(dz) > 1e-12, dz, 1e-12)
        t_end = np.where(dz > 0, (length - p[:, 2]) / safe_dz, -p[:, 2] / safe_dz)
        t_end = np.where(np.abs(dz) > 1e-12, t_end, np.inf)
        tp = (planes[None, :] - p[:, 2:3]) / safe_dz[:, None]
        tp = np.where((tp > EPS) & (np.abs(dz)[:, None] > 1e-12), tp, np.inf)
        plane_idx = np.argmin(tp, axis=1)
        t_plane = tp[np.arange(m), plane_idx]
        _, t_out = _cylinder_roots(p, v, r_drum)
        t_out = np.where(t_out > EPS, t_out, np.inf)
        t_hub, _ = _cylinder_roots(p, v, r_hub)
        t_hub = np.where(t_hub > EPS, t_hub, np.inf)
        f1, f2 = _cylinder_roots(p, v, farm_r)
        t_farm = _first_in_band(p, v, f1, f2, pitch, n_tori, farm_half)

        times = np.stack([t_end, t_plane, t_out, t_hub, t_farm], axis=1)
        event = np.argmin(times, axis=1)
        t = times[np.arange(m), event]
        hit = p + t[:, None] * v
        new_fate = np.zeros(m, dtype=int)
        new_d = v.copy()
        radial = np.stack([hit[:, 0], hit[:, 1], np.zeros(m)], axis=1)
        radial /= np.maximum(np.linalg.norm(radial, axis=1, keepdims=True), 1e-12)

        new_fate[event == 0] = 1

        # Panel planes: semi-transparent within the radiator band.
        on_plane = event == 1
        r_hit = np.hypot(hit[:, 0], hit[:, 1])
        meets = on_plane & (r_hit >= r_in) & (r_hit <= r_drum) & (rng.random(m) < coverage)
        absorbed = meets & (rng.random(m) < emissivity)
        new_fate[absorbed] = 3
        reflect = meets & ~absorbed
        if reflect.any():
            normal = np.zeros((reflect.sum(), 3))
            normal[:, 2] = -np.sign(v[reflect, 2])
            new_d[reflect] = _diffuse(normal, rng)

        # Outer boundary: envelope (insulated) or side gap.
        outer = event == 2
        kz = np.clip(np.floor(hit[:, 2] / pitch), 0, n_tori - 1).astype(int)
        in_env = np.abs(hit[:, 2] - planes[kz]) <= env
        gap = outer & ~in_env
        if side_gaps:
            new_fate[gap] = 2
            wall = outer & in_env
        else:
            wall = outer
        if wall.any():
            new_d[wall] = _diffuse(-radial[wall], rng)

        hub = event == 3
        if hub.any():
            new_d[hub] = _diffuse(radial[hub], rng)

        farm = event == 4
        if farm.any():
            back = -np.sign(np.einsum("ij,ij->i", v[farm], radial[farm]))[:, None] * radial[farm]
            new_d[farm] = _diffuse(back, rng)

        idx = np.flatnonzero(alive)
        fate[idx] = new_fate
        pos[idx] = hit + EPS * 10 * new_d
        d[idx] = new_d
    unresolved = int((fate == 0).sum())
    return {
        "escape": float(((fate == 1) | (fate == 2)).mean()),
        "escape_ends": float((fate == 1).mean()),
        "escape_gaps": float((fate == 2).mean()),
        "unresolved": unresolved / n,
    }


def check(p, d, geo, heat_load_w, side_gaps=True, n_rays=20000, seed=0, coverages=None):
    """Panel coverage needed to reject heat_load_w from the whole stack, and the most the drum can reject."""
    flux = radiator_flux(p.radiator_temp_k)
    eps = p.radiator_emissivity
    r_in = geo["farm_radius"] + geo["farm_height"]
    annulus = math.pi * (geo["drum_radius"] ** 2 - r_in ** 2)
    coverages = coverages or (0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0)
    curve = []
    for f in coverages:
        e = escape_probability(geo, d.n_tori, f, eps, side_gaps, n_rays, seed)
        area = 2 * f * annulus * d.n_tori          # emitting area, both faces
        curve.append({"coverage": f, "panel_area": area / 2, "escape": e["escape"],
                      "escape_gaps": e["escape_gaps"], "output": eps * flux * area * e["escape"]})
    ideal = 2 * geo["end_opening"] * flux
    best = max(curve, key=lambda c: c["output"])
    needed = None
    for lo, hi in zip(curve, curve[1:]):
        if lo["output"] < heat_load_w <= hi["output"]:
            s = (heat_load_w - lo["output"]) / (hi["output"] - lo["output"])
            needed = {k: lo[k] + s * (hi[k] - lo[k]) for k in ("coverage", "panel_area", "escape")}
            break
    if needed is None and curve[0]["output"] >= heat_load_w:
        needed = {k: curve[0][k] for k in ("coverage", "panel_area", "escape")}
    return {
        "heat_load": heat_load_w,
        "ideal_limit": ideal,
        "curve": curve,
        "max_output": best["output"],
        "max_vs_ideal": best["output"] / ideal,
        "margin": best["output"] / heat_load_w,
        "needed": needed,                     # None: the drum can't reject the load
        "ideal_panel_area": heat_load_w / (eps * flux) / 2,
        "side_gaps": side_gaps,
    }


def stack_limit(p, design, side_gaps=False, n_rays=4000, max_tori=40):
    """Most tori whose heat the drum can still reject (same size, tiers lit and gaps)."""
    from dataclasses import replace

    from .model import evaluate

    best = 0
    for n in range(1, max_tori + 1):
        d = replace(design, n_tori=n)
        r = evaluate(p, d)
        if check(p, d, r["geometry"], r["heat"]["stack"], side_gaps, n_rays)["margin"] < 1:
            break
        best = n
    return best


STUDY = (("900 m pair, 3 tiers", 900, 2, 3), ("900 m six, 1 tier", 900, 6, 1), ("900 m six, 2 tiers", 900, 6, 2),
         ("900 m six, 3 tiers", 900, 6, 3), ("1.6 km six, 2 tiers", 1600, 6, 2), ("1.6 km six, 3 tiers", 1600, 6, 3))


def study(p, n_rays=8000):
    from .design import Design
    from .model import evaluate

    rows = []
    for label, radius, n, tiers in STUDY:
        d = Design(radius_m=radius, n_tori=n, tiers_lit=tiers)
        r = evaluate(p, d)
        load = r["heat"]["stack"]
        rows.append({
            "label": label, "load": load, "ideal": r["heat"]["capacity"],
            "ideal_panels": load / (p.radiator_emissivity * radiator_flux(p.radiator_temp_k)) / 2,
            "ends": check(p, d, r["geometry"], load, side_gaps=False, n_rays=n_rays),
            "gaps": check(p, d, r["geometry"], load, side_gaps=True, n_rays=n_rays),
            "limit": stack_limit(p, d),
        })
    return rows
