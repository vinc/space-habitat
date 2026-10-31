"""The spin-up sequence of a torus, by the geometrically nonlinear model (nonlinear.py; plan §2).

Stages, in the order they are built:
1. Joints: hold the shortest arcs at 0.7 of the spin with locked joints, then release them towards
   pinned or sliding: whether the partial ring keeps an equilibrium without moment joints.
2. Flexible arcs, locked, nothing temporary: the spin each stage reaches within the chords'
   allowable, and the hull's bending at full spin (E I of the hull and frames as a thin tube).
3. Temporary support at full spin (a torus added to a spinning stack): the single-laced anchors'
   cables doubled, or temporary radial lines from the hub to them, or the proposed mix (SUPPORT),
   every chord and line checked at its peak (its own spin load included).
4. The arcs grown to closure at full spin with the radial lines: chords, hull, joints, the pull the
   hub carries across.
5. Closure: the ring closed with every joint locked (the hull a hoop), or with the closure joints
   made sliding, then every joint released: the finished net.
"""

import math

from . import nonlinear as nl

HULL_STRESS = 300e6            # Pa, working stress of the hull's plate (as in tube_section)
# The temporary support proposed: radial lines from the hub to the single-laced anchors, of this share
# of a chord's area, and the cables at those anchors thickened by this factor (a sleeve alongside),
# chosen so that the lines, the chords and the hull all stay near or within their allowables at full
# spin at every stage (the chords, sized to 1 GPa in the finished net, can't stay below it wherever a
# stage loads them past their finished tension).
SUPPORT = {"radial_lines": 1.15, "end_zone_factor": 1.05}
ARC_FACTORS = (1.0, 1.5, 3.0)  # arcs, in multiples of the shortest (4 theta r)


def arc_count(n, net, factor):
    return math.ceil(factor * 4 * net["theta"] * n / (2 * math.pi))


def hull_bending(info, moment):
    """Bending stress in the hull and frames' steel (a thin tube of the tube's radius) under a moment
    in the ring's plane: M a / I, I = A a^2 / 2."""
    return 2 * moment / (info["steel_area"] * info["geometry"]["tube_radius"])


def joints_study(p, r=900, spin=0.7):
    rows = []
    for f in ARC_FACTORS:
        for to in ("pinned", "sliding"):
            m, info = nl.for_design(p, r, arcs_fn=lambda n, net: nl.opposite_pairs(n, arc_count(n, net, f)))
            res = m.release(info["geometry"]["omega"], spin, to=to)
            lk = res["locked"]
            rows.append({"factor": f, "to": to, "arc": arc_count(m.n_anchors, info["net"], f) * 2 * math.pi * r / m.n_anchors,
                         "released": res["released"], "resolved": res["resolved"],
                         "locked_stress": lk["peak_stress"], "locked_rotation": lk["rotation_max"],
                         "locked_joint_moment": lk["joint_moment_max"],
                         "stress": res.get("peak_stress"), "rotation": res.get("rotation_max"),
                         "displacement": res.get("displacement_max"), "sigma": info["sigma"]})
    return rows


def flexible_study(p, sizes=(900, 1600)):
    rows = []
    for r in sizes:
        for f in ARC_FACTORS:
            m, info = nl.for_design(p, r, arcs_fn=lambda n, net: nl.opposite_pairs(n, arc_count(n, net, f)))
            om = info["geometry"]["omega"]
            lim = m.spin_limit(om, info["sigma"])
            full = m.solve(om, 1.0)
            rows.append({"r": r, "factor": f, "limit": lim["limit"], "by": lim["by"],
                         "tension_ratio": full["tension_max"] / info["net"]["tension_end"],
                         "hull": hull_bending(info, full["rim_moment_max"]),
                         "hull_at_limit": hull_bending(info, lim["state"]["rim_moment_max"]),
                         "joint_tension": full["joint_tension_max"], "joint_moment": full["joint_moment_max"]})
    return rows


def support_study(p, sizes=(900, 1600), factors=(1.5, 3.0)):
    rows = []
    for r in sizes:
        for f in factors:
            for kind, kw in (("none", {}), ("cables doubled at the single-laced anchors", {"end_zone_factor": 2.0}),
                             ("radial lines, a chord's area", {"radial_lines": 1.0}),
                             ("proposed: radial lines 1.15×, end cables 1.05×", SUPPORT)):
                m, info = nl.for_design(p, r, arcs_fn=lambda n, net: nl.opposite_pairs(n, arc_count(n, net, f)), **kw)
                full = m.solve(info["geometry"]["omega"], 1.0)
                rows.append({"r": r, "factor": f, "kind": kind, "reached": full["reached"],
                             "stress": full["peak_stress"], "line_stress": full["line_peak_stress"],
                             "sigma": info["sigma"],
                             "hull": hull_bending(info, full["rim_moment_max"]),
                             "joint_tension": full["joint_tension_max"], "extra": m.extra_cable_mass})
    return rows


GROWTH = {900: (0.1, 0.3, 0.6, 0.95), 1600: (0.1, 0.3, 0.6)}   # shares of a half ring per arc


def growth_study(p, sizes=(900, 1600)):
    """One opposite pair of arcs growing from ~the shortest to nearly half the ring each, at full
    spin, with the radial lines at their single-laced anchors."""
    rows = []
    for r in sizes:
        for share in GROWTH[r]:
            m, info = nl.for_design(p, r, arcs_fn=lambda n, net: nl.opposite_pairs(n, max(1, round(share * n / 2))),
                                    **SUPPORT)
            om = info["geometry"]["omega"]
            full = m.solve(om, 1.0)
            _, _, out = m.assemble(full["u"], om ** 2)
            worst = max(full["peak_stress"], full["line_peak_stress"])
            rows.append({"r": r, "share": share, "arc": share * math.pi * r, "reached": full["reached"],
                         "stress": full["peak_stress"], "line_stress": full["line_peak_stress"], "sigma": info["sigma"],
                         # Stresses go as the spin squared: the spin within every allowable.
                         "spin_within": min(1.0, math.sqrt(info["sigma"] / worst)),
                         "hull": hull_bending(info, full["rim_moment_max"]),
                         "joint_tension": full["joint_tension_max"], "joint_moment": full["joint_moment_max"],
                         "hub_pull": sum(out.get("R", [])) / 2, "lines": len(m.radials), "extra": m.extra_cable_mass,
                         "hoop": info["line_mass"] * (om * r) ** 2})
    return rows


def closure_study(p, r=900):
    """The closed ring at full spin: every joint locked (the hull a hoop), or the two closure joints
    made sliding; then every joint released to sliding (the finished net)."""
    out = {}
    m, info = nl.for_design(p, r)
    om = info["geometry"]["omega"]
    te = info["net"]["tension_end"]
    locked = m.solve(om, 1.0)
    out["locked"] = {"hull_axial": locked["rim_tension_max"] / info["steel_area"],
                     "tension_ratio": float(locked["tensions"].mean()) / te}
    m, info = nl.for_design(p, r, sliding_at=(math.pi / 2, 3 * math.pi / 2))
    res = m.release(om, 1.0, to="sliding")
    lk = res["locked"]
    out["closure_sliding"] = {"hull_axial": lk["rim_tension_max"] / info["steel_area"],
                              "hull_bending": hull_bending(info, lk["rim_moment_max"]),
                              "tension_min": lk["tension_min"] / te, "tension_max": lk["tension_max"] / te}
    out["closure_sliding"]["peak"] = lk["peak_stress"] / info["sigma"]
    out["released"] = {"resolved": res["resolved"], "tension_min": res["tension_min"] / te,
                       "tension_max": res["tension_max"] / te, "path_peak": res["path_peak_stress"] / info["sigma"],
                       "peak": res["peak_stress"] / info["sigma"]}
    return out
