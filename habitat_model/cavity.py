"""Preliminary radiative exchange, per section, by Monte Carlo ray tracing (plan §6).

Each section is a "scene" along the spin axis, from z = 0 to its length:

- main section: the drum between the hub and the tori's envelopes (radius R_d), with the
  valleys' radiator panels in each torus plane, on the spokes from radiator_inner out to R_d.
  Escape through the two end openings and, optionally, the side gaps between envelopes (rays
  reaching R_d between two envelopes leave); the envelopes' inner faces are walls;
- farm section: an open stack of farm rings (cylinder bands at the farm radius, the farm
  width wide), with the farm's radiator panels in each farm-ring plane, on the farm spokes
  from just outside the farm rings out to farm_radiator_outer. Nothing encloses it: rays
  escape through its ends or once they head outward beyond everything.

In both: panels are two-sided, face along the axis and cover a fraction f of their annulus
(each crossing of a plane meets a panel with probability f), with emissivity eps, diffuse;
the hub and the rings are insulated (absorb and re-emit diffusely all they receive); all
panels are at one temperature, so the net output is eps sigma T^4 A_panels times the
probability that an emitted ray escapes before it is absorbed by a panel.

Each section is modelled on its own, with its ends open. Their interaction (each section's
end facing the other across the gap) is estimated separately by `coupling`, as the final
step that puts the sections together.

Not included: sunlight entering through the gaps, spokes and cables, the despun array and
dock, the envelopes' rounded shape (taken as a cylinder at R_d), and the actual radiator
layout; the sink is taken at ~0 K.
"""

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np

from .heat import radiator_flux

EPS = 1e-6


@dataclass(frozen=True)
class Scene:
    planes: tuple              # z of each panel plane
    length: float              # the section spans 0..length
    hub: float                 # hub radius (insulated cylinder)
    band: tuple                # (r_in, r_out) of the panel annuli
    drum: Optional[float] = None          # outer wall radius (main section), None: open
    envelope_half: float = 0.0            # half-length of each envelope band on the wall
    side_gaps: bool = False               # wall gaps let rays out
    ring_radius: Optional[float] = None   # insulated ring bands around each plane (farm rings)
    ring_half: float = 0.0
    open_radius: Optional[float] = None   # open scenes: beyond this, moving outward, a ray is gone

    @property
    def panel_annulus(self):
        return math.pi * (self.band[1] ** 2 - self.band[0] ** 2)


def main_scene(geo, n, side_gaps=False):
    pitch = geo["pitch"]
    return Scene(planes=tuple((k + 0.5) * pitch for k in range(n)), length=n * pitch, hub=geo["hub_radius"],
                 band=(geo["radiator_inner"], geo["drum_radius"]), drum=geo["drum_radius"],
                 envelope_half=geo["envelope_radius"], side_gaps=side_gaps)


def farm_scene(geo, n):
    fp = geo["farm_pitch"]
    ring_outer = geo["farm_radius"] + geo["farm_height"]
    outer = max(geo["farm_radiator_outer"], ring_outer + 1.0)
    return Scene(planes=tuple((k + 0.5) * fp for k in range(n)), length=n * fp, hub=geo["hub_radius"],
                 band=(ring_outer, outer), ring_radius=geo["farm_radius"] + geo["farm_height"] / 2,
                 ring_half=geo["farm_width"] / 2, open_radius=outer + 1.0)


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


def _first_in_band(pos, d, t1, t2, planes, half_width):
    """Smallest positive root whose z falls within half_width of one of the planes."""
    best = np.full(len(pos), np.inf)
    for t in (t2, t1):  # t1 <= t2: checked last, so it wins when both qualify
        z = pos[:, 2] + np.where(np.isfinite(t), t, 0.0) * d[:, 2]
        near = np.min(np.abs(z[:, None] - planes[None, :]), axis=1)
        in_band = (t > EPS) & np.isfinite(t) & (near <= half_width)
        best = np.where(in_band, t, best)
    return best


def escape_probability(scene, coverage, emissivity, n_rays=20000, seed=0, max_steps=5000):
    rng = np.random.default_rng(seed)
    planes = np.array(scene.planes)
    n_planes = len(planes)
    r_in, r_out = scene.band

    # Emission: uniform over the panel annuli, either face, cosine-weighted.
    n = n_rays
    k = rng.integers(0, n_planes, n)
    rr = np.sqrt(rng.uniform(r_in ** 2, r_out ** 2, n))
    ph = rng.uniform(0, 2 * math.pi, n)
    pos = np.stack([rr * np.cos(ph), rr * np.sin(ph), planes[k]], axis=1)
    side = np.where(rng.random(n) < 0.5, 1.0, -1.0)
    d = _diffuse(np.stack([np.zeros(n), np.zeros(n), side], axis=1), rng)
    pos = pos + EPS * 10 * d

    fate = np.zeros(n, dtype=int)   # 0 alive, 1 escaped by an end, 2 escaped sideways, 3 absorbed
    for _ in range(max_steps):
        alive = fate == 0
        if not alive.any():
            break
        p, v = pos[alive], d[alive]
        m = len(p)
        dz = v[:, 2]
        safe_dz = np.where(np.abs(dz) > 1e-12, dz, 1e-12)
        t_end = np.where(dz > 0, (scene.length - p[:, 2]) / safe_dz, -p[:, 2] / safe_dz)
        t_end = np.where(np.abs(dz) > 1e-12, t_end, np.inf)
        tp = (planes[None, :] - p[:, 2:3]) / safe_dz[:, None]
        tp = np.where((tp > EPS) & (np.abs(dz)[:, None] > 1e-12), tp, np.inf)
        t_plane = tp[np.arange(m), np.argmin(tp, axis=1)]
        t_hub, _ = _cylinder_roots(p, v, scene.hub)
        t_hub = np.where(t_hub > EPS, t_hub, np.inf)
        outer_radius = scene.drum if scene.drum is not None else scene.open_radius
        _, t_out = _cylinder_roots(p, v, outer_radius)
        t_out = np.where(t_out > EPS, t_out, np.inf)
        if scene.ring_radius is not None:
            f1, f2 = _cylinder_roots(p, v, scene.ring_radius)
            t_ring = _first_in_band(p, v, f1, f2, planes, scene.ring_half)
        else:
            t_ring = np.full(m, np.inf)

        times = np.stack([t_end, t_plane, t_out, t_hub, t_ring], axis=1)
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
        meets = on_plane & (r_hit >= r_in) & (r_hit <= r_out) & (rng.random(m) < coverage)
        absorbed = meets & (rng.random(m) < emissivity)
        new_fate[absorbed] = 3
        reflect = meets & ~absorbed
        if reflect.any():
            normal = np.zeros((reflect.sum(), 3))
            normal[:, 2] = -np.sign(v[reflect, 2])
            new_d[reflect] = _diffuse(normal, rng)

        # Outer boundary: the drum's wall (envelopes, gaps), or open space.
        outer = event == 2
        if scene.drum is None:
            new_fate[outer] = 2
        else:
            near = np.min(np.abs(hit[:, 2][:, None] - planes[None, :]), axis=1)
            in_env = near <= scene.envelope_half
            if scene.side_gaps:
                new_fate[outer & ~in_env] = 2
                wall = outer & in_env
            else:
                wall = outer
            if wall.any():
                new_d[wall] = _diffuse(-radial[wall], rng)

        hub = event == 3
        if hub.any():
            new_d[hub] = _diffuse(radial[hub], rng)

        ring = event == 4
        if ring.any():
            back = -np.sign(np.einsum("ij,ij->i", v[ring], radial[ring]))[:, None] * radial[ring]
            new_d[ring] = _diffuse(back, rng)

        idx = np.flatnonzero(alive)
        fate[idx] = new_fate
        pos[idx] = hit + EPS * 10 * new_d
        d[idx] = new_d
    return {
        "escape": float(((fate == 1) | (fate == 2)).mean()),
        "escape_ends": float((fate == 1).mean()),
        "escape_sides": float((fate == 2).mean()),
        "unresolved": float((fate == 0).mean()),
    }


def check(p, scene, heat_load_w, n_rays=20000, seed=0, coverages=None, ideal_limit=None):
    """Panel coverage needed to reject heat_load_w from a section, and the most it can reject."""
    flux = radiator_flux(p.radiator_temp_k)
    eps = p.radiator_emissivity
    coverages = coverages or (0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0)
    curve = []
    for f in coverages:
        e = escape_probability(scene, f, eps, n_rays, seed)
        area = 2 * f * scene.panel_annulus * len(scene.planes)   # emitting area, both faces
        curve.append({"coverage": f, "panel_area": area / 2, "escape": e["escape"],
                      "escape_ends": e["escape_ends"], "escape_sides": e["escape_sides"],
                      "output": eps * flux * area * e["escape"]})
    best = max(curve, key=lambda c: c["output"])
    # Share of the escaping radiation that leaves through the ends (half of it through each).
    ends_share = best["escape_ends"] / best["escape"] if best["escape"] else 0.0
    needed = None
    if heat_load_w <= curve[0]["output"]:
        needed = {k: curve[0][k] * heat_load_w / curve[0]["output"] if k == "panel_area" else curve[0][k]
                  for k in ("coverage", "panel_area", "escape")}
        needed["coverage"] = curve[0]["coverage"] * heat_load_w / curve[0]["output"]
    else:
        for lo, hi in zip(curve, curve[1:]):
            if lo["output"] < heat_load_w <= hi["output"]:
                s = (heat_load_w - lo["output"]) / (hi["output"] - lo["output"])
                needed = {k: lo[k] + s * (hi[k] - lo[k]) for k in ("coverage", "panel_area", "escape")}
                break
    return {
        "heat_load": heat_load_w,
        "ideal_limit": ideal_limit,
        "curve": curve,
        "max_output": best["output"],
        "max_vs_ideal": best["output"] / ideal_limit if ideal_limit else None,
        "margin": best["output"] / heat_load_w if heat_load_w else math.inf,
        "needed": needed,                     # None: the section can't reject the load
        "ends_share": ends_share,
        "ideal_panel_area": heat_load_w / (eps * flux) / 2,
    }


def check_main(p, d, geo, heat, side_gaps=False, n_rays=20000):
    return check(p, main_scene(geo, d.n_tori, side_gaps), heat["main_stack"], n_rays,
                 ideal_limit=heat["capacity"])


def check_farm(p, d, geo, heat, n_rays=20000):
    return check(p, farm_scene(geo, d.n_tori), heat["farm_stack"], n_rays)


def coupling(geo, n, n_rays=200000, seed=0):
    """The whole stack: how much each section's facing end sees of the other across the gap.

    Main -> farm: of the radiation leaving the main drum's farm-end opening, the share that meets
    the farm section (its rings, or enters within their radius along its length) instead of
    open space. Farm -> main: of the radiation leaving the farm section's near end, the share that
    enters the main drum's opening. Both sections run at the same radiator temperature, so what
    one sends into the other is not lost, but it is not rejected either.
    """
    rng = np.random.default_rng(seed)
    hub, drum = geo["hub_radius"], geo["drum_radius"]
    rf_in, rf_out = geo["farm_radius"], geo["farm_radius"] + geo["farm_height"]
    gap, farm_len = geo["farm_section_gap"], n * geo["farm_pitch"]

    def lambertian(r_lo, r_hi, size):
        rho = np.sqrt(rng.uniform(r_lo ** 2, r_hi ** 2, size))
        ph = rng.uniform(0, 2 * math.pi, size)
        x = np.stack([rho * np.cos(ph), rho * np.sin(ph)], 1)
        u1, u2 = rng.random(size), rng.random(size)
        s, c, a = np.sqrt(u1), np.sqrt(1 - u1), 2 * math.pi * u2
        return x, np.stack([s * np.cos(a), s * np.sin(a)], 1), c

    # Main -> farm.
    x, dxy, dz = lambertian(hub, drum, n_rays)
    meets = np.zeros(n_rays, bool)
    for z in np.linspace(gap, gap + farm_len, 80):
        q = x + dxy * (z / dz)[:, None]
        meets |= np.hypot(q[:, 0], q[:, 1]) <= rf_out
    # Farm -> main: from the farm section's near end (its whole cross-section out to its radiators).
    outer = max(geo["farm_radiator_outer"], rf_out)
    x, dxy, dz = lambertian(hub, outer, n_rays)
    q = x + dxy * (gap / dz)[:, None]
    rho = np.hypot(q[:, 0], q[:, 1])
    enters = (rho >= hub) & (rho <= drum)
    return {"main_to_farm": float(meets.mean()), "farm_to_main": float(enters.mean())}


def stack_limit(p, design, section, n_rays=4000, max_tori=40):
    """Most tori (and farm rings) whose heat the section can still reject, ends only for the main drum."""
    from dataclasses import replace

    from .model import evaluate

    best = 0
    for n in range(1, max_tori + 1):
        d = replace(design, n_tori=n)
        r = evaluate(p, d)
        if section == "main":
            c = check_main(p, d, r["geometry"], r["heat"], side_gaps=False, n_rays=n_rays)
        else:
            c = check_farm(p, d, r["geometry"], r["heat"], n_rays=n_rays)
        if c["margin"] < 1:
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
        g, h = r["geometry"], r["heat"]
        main = check_main(p, d, g, h, side_gaps=False, n_rays=n_rays)
        farm = check_farm(p, d, g, h, n_rays=n_rays)
        c = coupling(g, n)
        rows.append({
            "label": label, "main_load": h["main_stack"], "farm_load": h["farm_stack"], "ideal": h["capacity"],
            "main_ends": main,
            "main_gaps": check_main(p, d, g, h, side_gaps=True, n_rays=n_rays),
            "farm": farm,
            "coupling": c,
            # The whole stack, conservatively: what each section sends into the other counts as not
            # rejected (one of the main drum's two ends faces the farm section).
            "main_whole_margin": main["margin"] * (1 - main["ends_share"] / 2 * c["main_to_farm"]),
            "farm_whole_margin": farm["margin"] * (1 - farm["ends_share"] / 2 * c["farm_to_main"]),
            "main_limit": stack_limit(p, d, "main"),
            "farm_limit": stack_limit(p, d, "farm"),
        })
    return rows
