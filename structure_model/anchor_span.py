"""Fewer, thicker chords: the tube spanning between anchors (notes §12, anchor spacing option).

The net's mass doesn't depend on the number of chords (cable_net), and the hub model's margins don't
either; what changes is the rim. The baseline anchors every ~10 m, at every bulkhead of the jacket, and
the cross-section model (tube_section) assumes the load reaches an anchor at every bulkhead. With k
anchors per ring segment (segments as long as the tube is wide), the tube must carry its load lengthwise
to the anchors, as a beam.

Each segment is a free-free beam (its joints carry shear only, and sit midway between two anchors, so by
symmetry they carry none) on k evenly spaced anchors, the outer ones moved to give equal reactions (equal
chords). The beam's section is the two skins as tube_section sizes them. Its lengthwise bending (M x / I)
and shear flow (V Q / I) add to the skins' hoop and lengthwise forces; each skin element is thickened
where von Mises exceeds the allowable (with the model's compression knockdown), station by station. The
anchored bulkheads carry the load of s metres instead of one cell (their steel scaled from what their
stresses use); the bulkheads between them stay, at their minimum gauge, as the rock's cell walls.

First-order only: the segment is a deep beam (its span about the tube's width), so plane sections are an
approximation, and the cross-section's own forces are taken from the every-bulkhead model. A 3D shell model
of a segment with its anchors and joints is still open, as are the anchor fittings at the larger loads.
"""

import math
import numpy as np

from . import tube_section as ts

STATIONS = 161


def beam(length, supports, q, n=801):
    """Free-free Euler-Bernoulli beam, uniform stiffness, rigid point supports, uniform load q (N/m).
    Returns x, M(x), V(x) and the reactions."""
    x = np.linspace(0, length, n)
    h = length / (n - 1)
    k = np.zeros((2 * n, 2 * n))
    f = np.zeros(2 * n)
    ke = np.array([[12, 6 * h, -12, 6 * h], [6 * h, 4 * h * h, -6 * h, 2 * h * h],
                   [-12, -6 * h, 12, -6 * h], [6 * h, 2 * h * h, -6 * h, 4 * h * h]]) / h ** 3
    fe = q * np.array([h / 2, h * h / 12, h / 2, -h * h / 12])
    for e in range(n - 1):
        d = slice(2 * e, 2 * e + 4)
        k[d, d] += ke
        f[d] += fe
    nodes = [int(round(s / h)) for s in supports]
    free = np.setdiff1d(np.arange(2 * n), [2 * j for j in nodes])
    u = np.zeros(2 * n)
    u[free] = np.linalg.solve(k[np.ix_(free, free)], f[free])
    reactions = -(k @ u - f)[[2 * j for j in nodes]]
    xs = x[nodes]
    shear = -q * x + sum(np.where(x >= s, r, 0.0) for s, r in zip(xs, reactions))
    moment = -q * x ** 2 / 2 + sum(np.where(x >= s, r * (x - s), 0.0) for s, r in zip(xs, reactions))
    return x, moment, shear, reactions


def supports(length, k, q):
    """k anchors evenly spaced (half a spacing from each end), the outer pair moved so the reactions agree."""
    s = length / k
    base = [(i + 0.5) * s for i in range(k)]
    if k <= 2:
        return base, beam(length, base, q)
    best = None
    for shift in np.linspace(-0.3 * s, 0.3 * s, 241):
        pos = list(base)
        pos[0] += shift
        pos[-1] -= shift
        res = beam(length, pos, q)
        spread = np.ptp(res[3]) / res[3].mean()
        if best is None or spread < best[0]:
            best = (spread, pos, res)
    return best[1], best[2]


_SECTIONS = {}


def _section(p, radius):
    """The sized cross-section, once per set of parameters and radius."""
    key = (radius, repr(sorted(vars(p).items())))
    if key not in _SECTIONS:
        out = ts.run(p, radius)
        _SECTIONS[key] = (out, ts.Model(out["inputs"]))
    return _SECTIONS[key]


def check(p, radius, k, segment_length=None):
    """The tube between k anchors per segment: added skin and bulkhead steel per torus, peak stresses."""
    out, model = _section(p, radius)
    inp, sol, m = out["inputs"], out["solution"], model.mesh
    length = segment_length or 2 * inp.a
    q = out["load"]
    phi = m.phi + math.pi / m.nt
    r_c = inp.cell / (8 * ts.PANEL_SAG)
    hull_q, outer_q, _ = model._panel_pressures()
    pill_h, pill_o = np.clip(hull_q, 0, None) * r_c / 2, outer_q * r_c / 2
    skins = [
        {"rho": inp.a, "l": model.lh, "t": out["t_hull"], "hoop": sol["n_hull"] + pill_h,
         "long": inp.pressure * inp.a / 2 + pill_h, "xg": model.hx},
        {"rho": inp.a + inp.jacket, "l": model.lo, "t": out["t_outer"], "hoop": sol["n_outer"] + pill_o,
         "long": pill_o, "xg": model.ox},
    ]
    for s in skins:
        s["x"] = s["rho"] * np.cos(phi)        # distance from the bending axis, along the spin's radial
    pos, (x, moment, shear, reactions) = supports(length, k, q)
    added, peak_bending, peak_shear = [], 0.0, 0.0
    for i in np.linspace(0, len(x) - 1, STATIONS).astype(int):
        t_new = [s["t"].copy() for s in skins]
        for _ in range(30):
            inertia = sum((t * s["l"] * s["x"] ** 2).sum() for t, s in zip(t_new, skins))
            nxt = []
            for t, s in zip(t_new, skins):
                n1 = s["hoop"]
                n2 = s["long"] + moment[i] * s["x"] / inertia * t
                n12 = shear[i] * np.cumsum(t * s["l"] * s["x"]) / inertia
                c, rr = (n1 + n2) / 2, np.hypot((n1 - n2) / 2, n12)
                vm = np.sqrt(n1 * n1 - n1 * n2 + n2 * n2 + 3 * n12 * n12)
                nxt.append(np.maximum(s["t"], vm / (inp.sigma * ts.allowance(c + rr, c - rr))))
            if all(np.allclose(a, b, rtol=1e-4) for a, b in zip(nxt, t_new)):
                break
            t_new = nxt
        inertia0 = sum((s["t"] * s["l"] * s["x"] ** 2).sum() for s in skins)
        peak_bending = max(peak_bending, abs(moment[i]) * skins[1]["rho"] / inertia0)
        peak_shear = max(peak_shear, max(abs(shear[i]) * np.abs(np.cumsum(s["t"] * s["l"] * s["x"])).max()
                                         / inertia0 / s["t"].min() for s in skins))
        added.append(sum(((tn - s["t"]) * s["l"] * s["xg"]).sum() for tn, s in zip(t_new, skins)))
    per_torus = 2 * math.pi * inp.centre
    rho = inp.steel_density
    skin = float(np.mean(added)) / inp.centre * rho * per_torus
    # Bulkheads: anchored ones carry s metres of load, the others stay at the minimum gauge.
    spacing = length / k
    area = model.qarea * model.qx / inp.centre
    need = out["tau"] * np.minimum(out["solution"]["utilisation"], 1.0)
    base = float((out["tau"] * area).sum()) * rho * per_torus
    bulk = 0.0
    if spacing > inp.cell:
        new = (area * (np.maximum(inp.wall_min, need * spacing) / spacing
                       + inp.wall_min * (1 / inp.cell - 1 / spacing))).sum() * rho * per_torus
        bulk = float(new) - base
    return {
        "radius": radius, "k": k, "spacing": spacing, "segment": length, "supports": pos,
        "reactions": reactions, "load": q, "anchor_force": float(reactions.mean()),
        "moment_max": float(np.abs(moment).max()), "shear_max": float(np.abs(shear).max()),
        "bending_stress": peak_bending, "shear_stress": peak_shear,
        "skin_added": skin, "bulkheads_added": bulk, "hull_frames": out["per_torus"]["total"],
    }
