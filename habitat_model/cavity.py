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

Each section is modelled on its own, with its ends open; then the whole stack is traced as one
scene (`assembled_scene`: the drum, the gap, the farm section with its radiators, and the tori's
outer side facing it), as the final step that puts the sections together. Only the assembled
check says whether the stack can reject its heat.

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
    bands: tuple               # (r_in, r_out) of each plane's panel annulus
    groups: tuple              # section of each plane: 0 main, 1 farm
    length: float              # the scene spans 0..length; rays leaving it along the axis escape
    hub: float                 # hub radius (insulated cylinder, the whole length)
    drum: Optional[float] = None          # wall radius of the main section's drum, None: no drum
    drum_span: tuple = (0.0, 0.0)         # z range of the drum wall
    envelope_half: float = 0.0            # half-length of each envelope band on the wall
    side_gaps: bool = False               # wall gaps let rays out
    ring_radius: Optional[float] = None   # insulated ring bands around the farm planes
    ring_half: float = 0.0
    open_radius: Optional[float] = None   # moving outward beyond this, a ray is gone
    face: Optional[tuple] = None          # (z, r_in, r_out): the last torus's side, facing +z (insulated)
    body: Optional[tuple] = None          # (radius, z0, z1): the tori's outer surface, seen from outside (insulated)

    def annulus(self, group):
        """Panel annuli of one section, summed over its planes."""
        return sum(math.pi * (b[1] ** 2 - b[0] ** 2) for b, g in zip(self.bands, self.groups) if g == group)


def _section(planes, band, group):
    planes = tuple(planes)
    return dict(planes=planes, bands=(band,) * len(planes), groups=(group,) * len(planes))


def main_scene(geo, n, side_gaps=False):
    pitch, length = geo["pitch"], n * geo["pitch"]
    return Scene(**_section(((k + 0.5) * pitch for k in range(n)), (geo["radiator_inner"], geo["drum_radius"]), 0),
                 length=length, hub=geo["hub_radius"], drum=geo["drum_radius"], drum_span=(0.0, length),
                 envelope_half=geo["envelope_radius"], side_gaps=side_gaps)


FARM_LAYOUTS = ("outboard", "inboard")


def _farm_band(geo, layout="outboard"):
    """The farm radiators' annulus: outboard, from the farm rings out to farm_radiator_outer (heat flows
    outward, against spin gravity: pumped loops), or inboard, from the hub to the rings (heat flows inward,
    with spin gravity: passive thermosiphons)."""
    if layout == "inboard":
        return geo["hub_radius"] + 1.0, geo["farm_radius"]
    if layout != "outboard":
        raise ValueError(f"farm radiator layout must be one of {FARM_LAYOUTS}, not {layout!r}")
    ring_outer = geo["farm_radius"] + geo["farm_height"]
    return ring_outer, max(geo["farm_radiator_outer"], ring_outer + 1.0)


def farm_scene(geo, n, layout="outboard"):
    fp = geo["farm_pitch"]
    band = _farm_band(geo, layout)
    ring_outer = geo["farm_radius"] + geo["farm_height"]
    return Scene(**_section(((k + 0.5) * fp for k in range(n)), band, 1), length=n * fp, hub=geo["hub_radius"],
                 ring_radius=geo["farm_radius"] + geo["farm_height"] / 2, ring_half=geo["farm_width"] / 2,
                 open_radius=max(band[1], ring_outer) + 1.0)


def assembled_scene(geo, n, open_margin=1.0, layout="outboard"):
    """The whole stack: the main section's drum, the gap, then the open farm section, traced together.

    The tori bound the main section physically: at the drum's farm end, the last torus's side (from
    the drum out to the envelopes' outer radius) is an insulated face looking at the farm section, and
    the envelopes' outer surface an insulated cylinder along the main section. The open radius only
    ends the rays: beyond every surface, a ray moving outward never comes back, so its margin
    (open_margin) doesn't change the result.
    """
    main, farm = main_scene(geo, n), farm_scene(geo, n, layout)
    start = geo["main_length"] + geo["farm_section_gap"]
    outer = geo["envelope_outer"]
    open_radius = max(farm.bands[0][1], outer) + open_margin
    return Scene(planes=main.planes + tuple(start + z for z in farm.planes), bands=main.bands + farm.bands,
                 groups=main.groups + farm.groups, length=geo["stack_length"], hub=geo["hub_radius"],
                 drum=main.drum, drum_span=main.drum_span, envelope_half=main.envelope_half,
                 ring_radius=farm.ring_radius, ring_half=farm.ring_half, open_radius=open_radius,
                 face=(geo["main_length"], main.drum, outer), body=(outer, 0.0, geo["main_length"]))


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


def escape_probability(scene, coverage, emissivity, n_rays=20000, seed=0, max_steps=5000, source=None):
    """Share of the rays emitted by the panels (of section `source`, or all) that escape.

    coverage: one fraction for every plane, or one per section (indexed by group).
    """
    rng = np.random.default_rng(seed)
    planes = np.array(scene.planes)
    groups = np.array(scene.groups)
    band_in = np.array([b[0] for b in scene.bands])
    band_out = np.array([b[1] for b in scene.bands])
    cover = np.atleast_1d(np.asarray(coverage, dtype=float))
    cover = (np.full(groups.max() + 1, cover[0]) if cover.size == 1 else cover)[groups]
    wall_planes = planes[groups == 0] if (groups == 0).any() else planes
    ring_planes = planes[groups == 1] if (groups == 1).any() else planes
    z_lo, z_hi = scene.drum_span

    # Emission: uniform over the source's panel annuli, either face, cosine-weighted.
    n = n_rays
    emitting = np.flatnonzero(groups == source) if source is not None else np.arange(len(planes))
    weight = band_out[emitting] ** 2 - band_in[emitting] ** 2
    k = emitting[rng.choice(len(emitting), n, p=weight / weight.sum())]
    rr = np.sqrt(rng.uniform(band_in[k] ** 2, band_out[k] ** 2))
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
        rows = np.arange(m)
        dz = v[:, 2]
        moving = np.abs(dz) > 1e-12
        safe_dz = np.where(moving, dz, 1e-12)
        t_end = np.where(dz > 0, (scene.length - p[:, 2]) / safe_dz, -p[:, 2] / safe_dz)
        t_end = np.where(moving, t_end, np.inf)
        tp = (planes[None, :] - p[:, 2:3]) / safe_dz[:, None]
        tp = np.where((tp > EPS) & moving[:, None], tp, np.inf)
        plane_k = np.argmin(tp, axis=1)
        t_plane = tp[rows, plane_k]
        t_hub, _ = _cylinder_roots(p, v, scene.hub)
        t_hub = np.where(t_hub > EPS, t_hub, np.inf)
        if scene.drum is not None:
            _, t_drum = _cylinder_roots(p, v, scene.drum)
            z_hit = p[:, 2] + np.where(np.isfinite(t_drum), t_drum, 0.0) * dz
            t_drum = np.where((t_drum > EPS) & (z_hit >= z_lo - EPS) & (z_hit <= z_hi + EPS), t_drum, np.inf)
        else:
            t_drum = np.full(m, np.inf)
        if scene.open_radius is not None:
            _, t_open = _cylinder_roots(p, v, scene.open_radius)
            t_open = np.where(t_open > EPS, t_open, np.inf)
        else:
            t_open = np.full(m, np.inf)
        if scene.ring_radius is not None:
            f1, f2 = _cylinder_roots(p, v, scene.ring_radius)
            t_ring = _first_in_band(p, v, f1, f2, ring_planes, scene.ring_half)
        else:
            t_ring = np.full(m, np.inf)
        if scene.face is not None:
            fz, f_in, f_out = scene.face
            t_face = np.where(moving, (fz - p[:, 2]) / safe_dz, np.inf)
            q = p + np.where(np.isfinite(t_face), t_face, 0.0)[:, None] * v
            r_face = np.hypot(q[:, 0], q[:, 1])
            t_face = np.where((t_face > EPS) & (r_face >= f_in) & (r_face <= f_out), t_face, np.inf)
        else:
            t_face = np.full(m, np.inf)

        if scene.body is not None:
            b_r, b_lo, b_hi = scene.body
            t_body, _ = _cylinder_roots(p, v, b_r)          # entry root: from outside only
            z_hit = p[:, 2] + np.where(np.isfinite(t_body), t_body, 0.0) * dz
            t_body = np.where((t_body > EPS) & (z_hit >= b_lo) & (z_hit <= b_hi), t_body, np.inf)
        else:
            t_body = np.full(m, np.inf)

        times = np.stack([t_end, t_plane, t_drum, t_open, t_hub, t_ring, t_face, t_body], axis=1)
        event = np.argmin(times, axis=1)
        t = times[rows, event]
        hit = p + t[:, None] * v
        new_fate = np.zeros(m, dtype=int)
        new_d = v.copy()
        radial = np.stack([hit[:, 0], hit[:, 1], np.zeros(m)], axis=1)
        radial /= np.maximum(np.linalg.norm(radial, axis=1, keepdims=True), 1e-12)

        new_fate[event == 0] = 1

        # Panel planes: semi-transparent within their radiator band.
        on_plane = event == 1
        r_hit = np.hypot(hit[:, 0], hit[:, 1])
        meets = (on_plane & (r_hit >= band_in[plane_k]) & (r_hit <= band_out[plane_k])
                 & (rng.random(m) < cover[plane_k]))
        absorbed = meets & (rng.random(m) < emissivity)
        new_fate[absorbed] = 3
        reflect = meets & ~absorbed
        if reflect.any():
            normal = np.zeros((reflect.sum(), 3))
            normal[:, 2] = -np.sign(v[reflect, 2])
            new_d[reflect] = _diffuse(normal, rng)

        # The drum's wall: envelopes, and gaps if they let rays out.
        drum = event == 2
        if drum.any():
            near = np.min(np.abs(hit[:, 2][:, None] - wall_planes[None, :]), axis=1)
            in_env = near <= scene.envelope_half
            if scene.side_gaps:
                new_fate[drum & ~in_env] = 2
                drum = drum & in_env
            new_d[drum] = _diffuse(-radial[drum], rng)

        new_fate[event == 3] = 2

        hub = event == 4
        if hub.any():
            new_d[hub] = _diffuse(radial[hub], rng)

        ring = event == 5
        if ring.any():
            back = -np.sign(np.einsum("ij,ij->i", v[ring], radial[ring]))[:, None] * radial[ring]
            new_d[ring] = _diffuse(back, rng)

        face = event == 6
        if face.any():
            normal = np.zeros((face.sum(), 3))
            normal[:, 2] = -np.sign(v[face, 2])
            new_d[face] = _diffuse(normal, rng)

        body = event == 7
        if body.any():
            new_d[body] = _diffuse(radial[body], rng)

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
        area = 2 * f * sum(scene.annulus(g) for g in set(scene.groups))   # emitting area, both faces
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


GRID = (0.0, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0)


def check_assembled(p, d, geo, heat, n_rays=8000, seed=0, grid=GRID, stop_when_feasible=False, layout="outboard"):
    """The whole stack, traced as one scene: can both sections reject their heat at once?

    Each section's panels run at the same temperature, so what one absorbs from the other it sends back
    (reciprocity): each section's net output is its own emission times the share of its rays that escape
    the whole stack. The panel coverages of the two sections are swept on a grid (more farm panels
    shade the main drum's farm end, more main panels shade the farm section's near end); the result
    is the grid point with the best worse-of-the-two margin.
    """
    scene = assembled_scene(geo, d.n_tori, layout=layout)
    flux, eps = radiator_flux(p.radiator_temp_k), p.radiator_emissivity
    loads = (heat["main_stack"], heat["farm_stack"])
    annuli = (scene.annulus(0), scene.annulus(1))
    points = []
    for fm in grid:
        for ff in grid:
            escape, output = [], []
            for group, f in ((0, fm), (1, ff)):
                e = escape_probability(scene, (fm, ff), eps, n_rays, seed, source=group)["escape"] if f else 0.0
                escape.append(e)
                output.append(eps * flux * 2 * f * annuli[group] * e)
            margins = [o / load if load else math.inf for o, load in zip(output, loads)]
            points.append({"coverage": (fm, ff), "panel_area": (fm * annuli[0], ff * annuli[1]),
                           "escape": tuple(escape), "output": tuple(output),
                           "margins": tuple(margins), "margin": min(margins)})
            if stop_when_feasible and points[-1]["margin"] >= 1:
                return _assembled(points, loads)
    return _assembled(points, loads)


def _assembled(points, loads):
    best = max(points, key=lambda q: q["margin"])
    return {"loads": loads, "points": points, "best": best, "margin": best["margin"],
            "main_margin": best["margins"][0], "farm_margin": best["margins"][1], "coverage": best["coverage"],
            "panel_area": best["panel_area"],     # one face, per section
            "feasible": best["margin"] >= 1}


def assembled_limit(p, design, n_rays=3000, max_tori=40, layout="outboard"):
    """Most tori (with their farm rings) the whole stack can cool, both sections traced together."""
    from dataclasses import replace

    from .model import evaluate

    def ok(n):
        d = replace(design, n_tori=n)
        r = evaluate(p, d)
        return check_assembled(p, d, r["geometry"], r["heat"], n_rays=n_rays, stop_when_feasible=True,
                               layout=layout)["feasible"]

    if not ok(1):
        return 0
    lo, hi = 1, max_tori                      # ok(lo); the margin falls as the stack grows
    if ok(hi):
        return hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    return lo


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
        rows.append({
            "label": label, "main_load": h["main_stack"], "farm_load": h["farm_stack"], "ideal": h["capacity"],
            "main_ends": check_main(p, d, g, h, side_gaps=False, n_rays=n_rays),
            "main_gaps": check_main(p, d, g, h, side_gaps=True, n_rays=n_rays),
            "farm": check_farm(p, d, g, h, n_rays=n_rays),
            "assembled": check_assembled(p, d, g, h, n_rays=n_rays),
            "limit": assembled_limit(p, d),
        })
    return rows


# The farm radiators' reach is a guess (assumptions.toml: farm_radiator_outer_frac), and it is the
# farm section's dominant thermal uncertainty; the sensitivity sweep can't see it (no ray tracing in
# `evaluate`), so it gets a sweep of its own.
FARM_SWEEP = (("900 m six, 2 tiers", 900, 6, 2), ("900 m six, 3 tiers", 900, 6, 3))


def farm_sweep(assumptions, overrides=None, n_rays=6000, name="farm_radiator_outer_frac", steps=5):
    from .assumptions import params
    from .design import Design
    from .model import evaluate

    a = assumptions[name]
    values = [a.low + (a.high - a.low) * i / (steps - 1) for i in range(steps)]
    rows = []
    for label, radius, n, tiers in FARM_SWEEP:
        d = Design(radius_m=radius, n_tori=n, tiers_lit=tiers)
        for v in values:
            p = params(assumptions, **{**(overrides or {}), name: v})
            r = evaluate(p, d)
            g, h = r["geometry"], r["heat"]
            rows.append({"label": label, "value": v, "default": abs(v - a.value) < 1e-9,
                         "farm": check_farm(p, d, g, h, n_rays=n_rays),
                         "assembled": check_assembled(p, d, g, h, n_rays=n_rays)})
    return name, rows
