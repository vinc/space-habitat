"""Monte Carlo ray tracing in a cross-section, periodic sideways (plan §7).

The light pipes, the light box and the farm's tiers are long compared with their cross-section, so the
scene is traced in the plane across the pipes, as if it went on forever along them. Rays are diffuse
(Lambertian) in three dimensions; only their projection on the plane matters for what they hit, since
nothing absorbs along the way, so the trace in the plane is exact for an endless scene.

The scene repeats every `period` sideways (x); rays leaving one side come back in on the other. It is made
of straight segments and circles (the pipes). Every surface reflects (ρ) and transmits (τ) diffusely,
from each of its two sides, and absorbs the rest.
"""

import math
from dataclasses import dataclass, field

import numpy as np

EPS = 1e-9


@dataclass
class Surface:
    name: str
    kind: str                     # "segment" or "circle"
    a: tuple                      # segment: start point; circle: centre
    b: object                     # segment: end point; circle: radius
    front: tuple = (0.0, 0.0)     # (ρ, τ) seen from the front (the left of a → b; outside a circle)
    back: tuple = (0.0, 0.0)


@dataclass
class Scene:
    period: float
    surfaces: list = field(default_factory=list)

    def add(self, *args, **kwargs):
        self.surfaces.append(Surface(*args, **kwargs))
        return self


def lambertian(normal, rng):
    """Diffuse directions about the (2D) normals, projected on the plane: the 3D cosine law, with the
    component along the pipes dropped."""
    n = normal.shape[0]
    u1, u2 = rng.random(n), rng.random(n)
    sin_t = np.sqrt(u1)
    cos_t = np.sqrt(1 - u1)
    along = sin_t * np.cos(2 * math.pi * u2)            # in the plane, along the surface
    tangent = np.stack([-normal[:, 1], normal[:, 0]], axis=1)
    d = cos_t[:, None] * normal + along[:, None] * tangent
    return d / np.maximum(np.linalg.norm(d, axis=1, keepdims=True), 1e-12)


def _hit(surface, o, d):
    """Distance along each ray to the surface (inf if missed) and the surface's front normal there."""
    if surface.kind == "segment":
        a, b = np.asarray(surface.a, float), np.asarray(surface.b, float)
        e = b - a
        denom = d[:, 0] * e[1] - d[:, 1] * e[0]
        w = a - o
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (w[:, 0] * e[1] - w[:, 1] * e[0]) / denom
            u = (w[:, 0] * d[:, 1] - w[:, 1] * d[:, 0]) / denom
        ok = (np.abs(denom) > 1e-15) & (t > EPS) & (u >= 0) & (u <= 1)
        n = np.array([-e[1], e[0]]) / np.linalg.norm(e)    # the left of a -> b
        return np.where(ok, t, np.inf), np.broadcast_to(n, o.shape)
    c, r = np.asarray(surface.a, float), float(surface.b)
    w = o - c
    bq = (w * d).sum(axis=1)
    cq = (w * w).sum(axis=1) - r * r
    disc = bq * bq - cq
    root = np.sqrt(np.maximum(disc, 0))
    t1, t2 = -bq - root, -bq + root
    t = np.where(t1 > EPS, t1, np.where(t2 > EPS, t2, np.inf))
    t = np.where(disc > 0, t, np.inf)
    p = o + d * np.where(np.isfinite(t), t, 0)[:, None]
    n = (p - c) / r
    return t, n


def trace(scene, origins, directions, rng, max_events=400):
    """Follow rays until they are absorbed. Returns, per surface, the x positions where light was absorbed,
    and the x positions where it went through each surface downward (−y) and upward."""
    o, d = origins.astype(float).copy(), directions.astype(float).copy()
    alive = np.ones(len(o), bool)
    absorbed = {s.name: [] for s in scene.surfaces}
    down = {s.name: [] for s in scene.surfaces}
    up = {s.name: [] for s in scene.surfaces}
    lost = 0
    P = scene.period
    for _ in range(max_events * 4):
        idx = np.flatnonzero(alive)
        if idx.size == 0:
            break
        oo, dd = o[idx], d[idx]
        best = np.full(idx.size, np.inf)
        which = np.full(idx.size, -1)
        normal = np.zeros_like(oo)
        for k, s in enumerate(scene.surfaces):
            t, n = _hit(s, oo, dd)
            closer = t < best
            best = np.where(closer, t, best)
            which = np.where(closer, k, which)
            normal = np.where(closer[:, None], n, normal)
        # The periodic sides: a ray reaching x = 0 or x = P before any surface comes back on the other side.
        with np.errstate(divide="ignore", invalid="ignore"):
            t_side = np.where(dd[:, 0] > 0, (P - oo[:, 0]) / dd[:, 0],
                              np.where(dd[:, 0] < 0, -oo[:, 0] / dd[:, 0], np.inf))
        wrap = t_side < best
        if wrap.any():
            w = idx[wrap]
            o[w] = oo[wrap] + dd[wrap] * t_side[wrap, None]
            o[w, 0] = np.where(dd[wrap, 0] > 0, 0.0, P)
        hit = ~wrap & np.isfinite(best)
        lost += int((~wrap & ~np.isfinite(best)).sum())
        alive[idx[~wrap & ~np.isfinite(best)]] = False
        if not hit.any():
            continue
        h = idx[hit]
        p = oo[hit] + dd[hit] * best[hit, None]
        n = normal[hit]
        k = which[hit]
        from_front = (dd[hit] * n).sum(axis=1) < 0
        u = rng.random(h.size)
        rho = np.empty(h.size)
        tau = np.empty(h.size)
        for j, s in enumerate(scene.surfaces):
            m = k == j
            rho[m] = np.where(from_front[m], s.front[0], s.back[0])
            tau[m] = np.where(from_front[m], s.front[1], s.back[1])
        side = np.where(from_front[:, None], n, -n)       # normal on the side the ray came from
        refl = u < rho
        trans = ~refl & (u < rho + tau)
        absb = ~refl & ~trans
        new_d = np.zeros_like(p)
        if refl.any():
            new_d[refl] = lambertian(side[refl], rng)
        if trans.any():
            new_d[trans] = lambertian(-side[trans], rng)
        for j, s in enumerate(scene.surfaces):
            m = k == j
            if not m.any():
                continue
            absorbed[s.name].append(p[m & absb, 0])
            going_down = m & trans & (side[:, 1] > 0)
            going_up = m & trans & (side[:, 1] < 0)
            down[s.name].append(p[going_down, 0])
            up[s.name].append(p[going_up, 0])
        o[h] = p
        d[h] = new_d
        alive[h[absb]] = False
    stuck = int(alive.sum())
    cat = {name: np.concatenate(v) if v else np.empty(0) for name, v in absorbed.items()}
    return {"absorbed": cat,
            "down": {name: np.concatenate(v) if v else np.empty(0) for name, v in down.items()},
            "up": {name: np.concatenate(v) if v else np.empty(0) for name, v in up.items()},
            "n": len(origins), "lost": lost, "stuck": stuck}


def emit_from_circle(centre, radius, n, rng, arc_deg=360.0, facing=(0.0, -1.0)):
    """Diffuse emission from a circle's surface, over an arc centred on `facing` (a lamp pipe glowing
    on one side), evenly by length of arc."""
    half = math.radians(arc_deg) / 2
    base = math.atan2(facing[1], facing[0])
    phi = base + (rng.random(n) * 2 - 1) * half
    normal = np.stack([np.cos(phi), np.sin(phi)], axis=1)
    origins = np.asarray(centre, float) + radius * (1 + 1e-7) * normal
    return origins, lambertian(normal, rng)
