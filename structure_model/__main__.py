"""Structure (plan §2): wire strength, the tangent-chord net, the spin-up of a partial ring and the tube's cross-section.

python -m structure_model [--anchor-spacing 10] [--mismatch 0.01] [--set name=value ...]
"""

import argparse
import math
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import cable_net, hub, net_statics, nonlinear, rest, sequence, spinup, tube_section, wire

SIZES = (400, 900, 1600, 2500)


def size_label(r):
    return f"{r / 1000:g} km" if r >= 1000 else f"{r:g} m"


def wire_section(p):
    rows = [[name, f"{sf:g}"] + [num(wire.working_stress(g, sf)) for g in wire.BRIDGE_CLASSES]
            for name, sf in wire.SAFETY_FACTORS.items()]
    thin = [[f"{d:g} mm", num(wire.thin_wire_strength(d)), num(wire.thin_wire_strength(d) / 2)]
            for d in (5, 2, 1, 0.5, 0.3)]
    creep = [[size_label(r), num(wire.creep_elongation(p.wire_stress_mpa * 1e6, g * 1e6, r), 2)]
             for r in SIZES for g in (1960,)]
    return "\n\n".join([
        "## Wire\n\nWorking stress (MPa) by guaranteed strength class of bridge wire and safety factor:",
        table(["Safety factor", "SF"] + [f"{g} MPa class" for g in wire.BRIDGE_CLASSES], rows),
        f"The model's {p.wire_stress_mpa:g} MPa needs a safety factor of {num(1960 / p.wire_stress_mpa)} on the "
        "strongest bridge class. Thinner wire is stronger (Bekaert's high-strength threshold, a rough guide):",
        table(["Wire diameter", "High-strength threshold (MPa)", "At SF 2 (MPa)"], thin),
        f"Long-term creep of a spoke at {p.wire_stress_mpa:g} MPa on 1,960 MPa wire (relaxation r = 30 f/fu − 10% "
        "after 1,000 h, doubled for the long term, read as creep at constant load):",
        table(["Torus", "Extra stretch over the spoke's length (m)"], creep),
    ])


def net_section(p, spacing):
    rows = []
    for r in SIZES:
        res = evaluate(p, Design(radius_m=r, n_tori=1))
        g, m = res["geometry"], res["mass"]
        n = cable_net.compute(r, m["rim"], g["omega"], g["hub_radius"], p.wire_stress_mpa * 1e6,
                              p.steel_density, anchor_spacing=spacing)
        rows.append([size_label(r), f"{math.degrees(n['theta']):.1f}°", num(n["mass_uniform"] / 1e9),
                     num(m["spokes"] / 1e9), f"{n['chord_vs_radial']:+.2%}", f"{n['taper_saving']:.1%}",
                     num(n["taper_ratio"]), num(n["tension_end"] / 1e6), num(n["wire_area_uniform"] * 1e4),
                     num(n["wire_area_tapered_end"] * 1e4), num(n["bow"], 2)])
    return "\n\n".join([
        f"## Tangent-chord net (chords tangent at 1.1 × the hub radius, one anchor every {spacing:g} m)",
        "Uniform chords keep one area all along, sized at mid-chord where their own spin load adds most; "
        "tapered chords at uniform stress need only the end area at their ends.",
        table(["Torus", "Chord angle at the rim", "Net, uniform chords (Mt)", "System model spokes (Mt)",
               "Chords vs radial spokes", "Saved by tapering", "Taper (mid / end area)",
               "Tension per chord end (MN)", "Uniform chord area (cm²)", "Tapered chord, end area (cm²)",
               "Bow at mid-chord (m)"], rows),
    ])


def _stage(p, r, arc_factor, joints):
    res = evaluate(p, Design(radius_m=r, n_tori=1))
    g, m = res["geometry"], res["mass"]
    sigma = p.wire_stress_mpa * 1e6
    n = cable_net.compute(r, m["rim"], g["omega"], g["hub_radius"], sigma, p.steel_density)
    lam = m["rim"] / (2 * math.pi * r)
    arc = None if arc_factor is None else arc_factor * 4 * n["theta"] * r
    s = net_statics.solve(r, n["tangent_radius"], lam, g["omega"], n["wire_area_uniform"], p.steel_density,
                          arc_length=arc, segment_length=g["width"], joints=joints, stress_pa=sigma)
    return n, s, arc


def construction_section(p):
    rows = []
    cases = [(r, None, j) for r in (900, 1600) for j in ("sliding", "locked")]
    cases += [(r, f, j) for r in (400, 900, 1600, 2500) for f, j in ((1, "locked"), (1, "pinned"))]
    cases += [(900, f, j) for f in (1.5, 3) for j in ("locked", "pinned")]
    for r, f, j in cases:
        n, s, arc = _stage(p, r, f, j)
        stage = "finished ring" if arc is None else f"two arcs of {num(arc)} m" + (" (shortest)" if f == 1 else "")
        kin = f"{s['max_rotation']:.2g} rad / {num(s['max_displacement'], 2)} m"
        if not s["equilibrium"]:
            rows.append([size_label(r), stage, j, f"**unresolved:** {s['status']}", "", "", "", "", "", "",
                         kin if s["converged"] and s["residual"] < 1e-3 else "—", f"{s['residual']:.0e}"])
            continue
        rows.append([size_label(r), stage, j, "resolved",
                     f"{num(s['tension_min'] / 1e6)}–{num(s['tension_max'] / 1e6)}"
                     + (f" ({s['slack_chords']} slack)" if s["slack_chords"] else ""),
                     num(s["tension_max"] / n["tension_end"], 2),
                     num(s["peak_stress"] / 1e6), num(min(s["max_spin_fraction"], 1.0), 2),
                     "—" if j == "sliding" else
                     f"{num(s['joint_axial_max'] / 1e6)} ({s['joint_axial_max'] / s['hoop_full_ring']:.1%})",
                     num(s["joint_moment_max"] / 1e9, 2) if j == "locked" else "—",
                     kin, f"{s['residual']:.0e}"])
    return "\n\n".join([
        "## Building the ring: assembled statics (provisional)",
        "Each chord is one elastic member with a single tension; the rim is cut into rigid segments one tube "
        "width long, linked by joints that are *sliding* (shear only: free along the rim, as intended once the "
        "ring is closed), *pinned* (tension and shear) or *locked* (also bending). Chords are tension-only: the "
        "taut set is iterated both ways until it is exactly the set of stretched chords. Loads at full spin; "
        "cable stresses scale with spin². The chords are sized for the finished ring (uniform area).",
        "A stage is **resolved** only if the taut set converges, every segment balances (residual: the worst "
        "force or moment imbalance relative to the segment's load) and, after removing the assembly's rigid "
        f"motion, segment rotations stay below {net_statics.ROTATION_LIMIT} rad and displacements below "
        f"{net_statics.DISPLACEMENT_LIMIT:.0%} of the radius at the spin rate reported. Otherwise it is left "
        "unresolved for a geometrically nonlinear analysis: a mechanism, or displacements too large for the "
        "linear geometry. Rotation / displacement are at full spin.",
        table(["Torus", "Stage", "Joints", "Status", "Chord tensions (MN)", "Max chord vs finished",
               "Peak cable stress (MPa)", "Max spin fraction within 1 GPa",
               "Max joint tension (MN, share of full hoop)", "Max joint moment (GN·m)", "Rotation / displacement",
               "Residual"], rows),
        "Rigid segments make this a crude model: even resolved stages settle the force balance, not the "
        "construction sequence, and the joint moments of the longer locked arcs depend on the segments' real "
        "flexibility.",
    ])


def sequence_section(p):
    mpa = lambda x: num(x / 1e6)
    joint_rows = []
    for row in sequence.joints_study(p):
        if row["resolved"]:
            status = (f"held, but rotations {num(row['rotation'], 2)} rad, {num(row['displacement'])} m, chords "
                      f"{num(row['stress'] / row['sigma'], 2)}× the allowable")
        else:
            status = (f"**no equilibrium** below {row['released']:.0e} of the locked moment stiffness"
                      if row["released"] is not None else "**no equilibrium**")
        joint_rows.append([f"{num(row['factor'])}× ({num(row['arc'])} m)", row["to"],
                           f"{num(row['locked_stress'] / row['sigma'], 2)}× the allowable, "
                           f"{num(row['locked_joint_moment'] / 1e9, 2)} GN·m in the joints", status])
    flex_rows = []
    linear = {}
    for f in sequence.ARC_FACTORS:
        n, s_lin, _ = _stage(p, 900, f, "locked")
        linear[f] = s_lin["max_spin_fraction"]
    for row in sequence.flexible_study(p):
        flex_rows.append([size_label(row["r"]), f"{num(row['factor'])}×", num(row["limit"], 2),
                          num(min(linear[row["factor"]], 1.0), 2) if row["r"] == 900 else "—",
                          num(row["tension_ratio"], 2), mpa(row["hull"]), mpa(row["hull_at_limit"]),
                          num(row["joint_tension"] / 1e6), num(row["joint_moment"] / 1e9, 2)])
    support_rows = [[size_label(row["r"]), f"{num(row['factor'])}×", row["kind"],
                     "full spin" if row["reached"] >= 1 else f"{num(row['reached'], 2)} of the spin",
                     f"{mpa(row['stress'])} ({num(row['stress'] / row['sigma'], 3)}×)",
                     f"{mpa(row['line_stress'])} ({num(row['line_stress'] / row['sigma'], 3)}×)" if row["line_stress"]
                     else "—", mpa(row["hull"]),
                     num(row["joint_tension"] / 1e6), num(row["extra"] / 1e6, 2) if row["extra"] else "—"]
                    for row in sequence.support_study(p)]
    growth_rows = [[size_label(row["r"]), f"{num(row['arc'])} m ({row['share']:.0%} of a half ring)",
                    "full spin" if row["reached"] >= 1 else f"{num(row['reached'], 2)}",
                    f"{mpa(row['stress'])} ({num(row['stress'] / row['sigma'], 3)}×)",
                    f"{mpa(row['line_stress'])} ({num(row['line_stress'] / row['sigma'], 3)}×)",
                    num(row["spin_within"], 3), mpa(row["hull"]),
                    f"{num(row['joint_tension'] / 1e6)} ({row['joint_tension'] / row['hoop']:.1%})",
                    num(row["joint_moment"] / 1e9, 2), num(row["hub_pull"] / 1e9, 2), str(row["lines"]),
                    num(row["extra"] / 1e6, 2)] for row in sequence.growth_study(p)]
    c = sequence.closure_study(p)
    closure = (f"**Closure (900 m, full spin).** Closed with every joint locked, the hull becomes a hoop: "
               f"~{mpa(c['locked']['hull_axial'])} MPa along it, the chords at ~{num(c['locked']['tension_ratio'], 2)}× "
               "their finished tension. Made instead with its two closure joints sliding, the ring never becomes a "
               f"hoop: the hull at ~{mpa(c['closure_sliding']['hull_axial'])} MPa along it and "
               f"~{mpa(c['closure_sliding']['hull_bending'])} MPa in bending, the chords at "
               f"{num(c['closure_sliding']['tension_min'], 2)}–{num(c['closure_sliding']['tension_max'], 2)}× their "
               f"finished tension (peak {num(c['closure_sliding']['peak'], 3)}× the allowable), every anchor now "
               "double-laced (the radial lines can go). Then every joint is released to sliding, step by step from "
               "the last equilibrium: "
               + (f"the finished net, chords at {num(c['released']['tension_min'], 3)}–"
                  f"{num(c['released']['tension_max'], 3)}× the formula (peak {num(c['released']['peak'], 3)}× the "
                  f"allowable; {num(c['released']['path_peak'], 3)}× at worst on the way)."
                  if c["released"]["resolved"] else "**not reached**."))
    return "\n\n".join([
        "## Adding a torus to a spinning stack: geometrically nonlinear",
        "**The baseline is simpler** (previous section): a child is built at rest and spun up finished, so the "
        "partial-ring stages below don't arise. What follows is the harder option: "
        "a torus added to a living stack, which can't stop, so its arcs are hung at full spin. It checks "
        "selected stages of that sequence, not the whole process.",
        "`structure_model/nonlinear.py`, in the ring's plane and the rotating frame: the rim a chain of flexible "
        "beams (corotational, one per anchor spacing, E A and E I of the hull and frames as a thin tube of the "
        "tube's radius), joined at the segment joints (locked, pinned or sliding: penalty springs); each chord a "
        "tension-only cable with its geometric stiffness, pretensioned slightly; the rim's and the chords' "
        "centrifugal loads following the parts as they move; the assembly's centre of mass and mean rotation "
        "held (it turns about its centre of mass); the spin stepped up with Newton iterations and line search. "
        "It reproduces the linear model on the shortest locked arcs (chords ~1.94× their finished tension, "
        "joints ~186 MN and ~6 GN·m at full spin) and the finished net (within 1% of the formula). Sequence "
        "studies: `structure_model/sequence.py`.",
        "**Joints.** The shortest and longer arcs held at 0.7 of the spin with locked joints, then released "
        "step by step, each from the last equilibrium, towards pinned or sliding joints.",
        table(["Arcs (× the shortest)", "Released to", "Locked", "Released"], joint_rows),
        "**Flexible arcs, locked, nothing temporary.** The spin each stage reaches with every chord within its "
        "allowable, against the linear rigid-segment model's, and the hull's bending.",
        table(["Torus", "Arcs", "Spin limit (chords)", "Linear, rigid segments", "Chords at full spin (× finished)",
               "Hull bending at full spin (MPa)", "At the spin limit (MPa)", "Joint tension (MN)",
               "Joint moment (GN·m)"], flex_rows),
        f"With flexible segments, longer arcs don't relieve the chords: the single-laced end zones load theirs "
        f"to ~1.8× whatever the arc's length, and the arcs bend the hull far past its ~{mpa(sequence.HULL_STRESS)} MPa "
        "plate stress. A torus added to a spinning stack is hung at full spin, so it needs temporary support:",
        "Every chord and line at its peak: tension over area plus its own spin load (a chord's at mid-chord; "
        "a radial line's, conservatively, all of it, at its hub end).",
        table(["Torus", "Arcs", "Temporary support", "Reached", "Peak chord stress (MPa, × allowable)",
               "Peak radial-line stress (MPa, × allowable)", "Hull bending (MPa)", "Joint tension (MN)",
               "Temporary steel (kt)"], support_rows),
        "Doubling the cables at the single-laced anchors keeps the chords within their allowable but leaves "
        "the hull bending. Temporary radial lines from the hub to those anchors (pulling straight in, nothing "
        "along the rim) take the bending away; at a chord's area they are themselves ~5% over at their hub "
        "end, thicker they stiffen the ends and bend the hull again. Proposed: lines of 1.15× a chord's area "
        "and a 1.05× sleeve on the end-zone cables. The chords are sized to their allowable in the finished "
        "net (here at ~1.007× it, from the anchors' discrete positions), so wherever a stage loads them past "
        "their finished tension (the mid-arc chords by ~1%) they are past it too at full spin; the worst step "
        "is the release after closure (below, ~7%): building at ~0.97 of the spin for it, or a lower safety "
        "factor while building, covers it. The hub carries the two arcs' pull across its diameter.",
        "**Growing to closure at full spin** (one opposite pair; two pairs at right angles behave the same, each "
        "arc at least the shortest, with twice the lines), with the proposed support:",
        table(["Torus", "Each arc", "Reached", "Peak chord stress (MPa, × allowable)",
               "Peak radial-line stress", "Spin within every allowable", "Hull bending (MPa)",
               "Joint tension (MN, share of hoop)", "Joint moment (GN·m)", "Pull across the hub (GN)",
               "Radial lines", "Their steel (kt)"], growth_rows),
        closure,
    ])


def imbalance_section(p, mismatch):
    rows = []
    for r in SIZES:
        res = evaluate(p, Design(radius_m=r, n_tori=1))
        g, m = res["geometry"], res["mass"]
        n = cable_net.chord_geometry(r, 1.1 * g["hub_radius"])
        lam = m["rim"] / (2 * math.pi * r)
        arc = lam * 4 * n["theta"] * r
        hub = 0.25 * m["steel"]  # hub, dock and factory metal, as in the system model
        first = spinup.imbalance_offset(mismatch * arc, r, 2 * arc + hub)
        full = spinup.imbalance_offset(mismatch * arc, r, m["total"] + hub)
        rows.append([size_label(r), num(arc / 1e9, 2), num(first, 2), num(full * 100, 2)])
    return "\n\n".join([
        f"## Imbalance: one arc {mismatch:.0%} heavier than its partner\n\n"
        "The stack spins freely about its centre of mass, so a mismatch moves the spin axis away from the "
        "assembly's geometric centre: an estimate of that offset only. The hub and the net move together, "
        "so this is not a loss of clearance between them; their relative motion needs the stabilising "
        "lines' stiffness (still open). Hub, dock and factory taken as 25% of the torus steel.",
        table(["Torus", "Shortest arc (Mt)", "Axis offset, first pair alone (m)",
               "Axis offset, finished torus if never ballasted (cm)"], rows),
    ])


MT = 1e9


def sizing_status(out):
    if out["converged"]:
        return "fully stressed"
    if out["sized"]:
        return f"safe, up to {out['slack']:.0%} spare"
    return f"**over by {out['utilisation'] - 1:.0%}**"


def tube_section_report(p):
    ts = tube_section
    rows = []
    for r in SIZES:
        res = evaluate(p, Design(radius_m=r, n_tori=1))
        m = res["mass"]
        out = ts.run(p, r, "sides", "vaulted")
        t = out["per_torus"]
        steel_model = m["steel"]
        steel_fe = m["spokes"] + t["total"]
        rows.append([size_label(r), num(out["load"] / 1e6), num(t["hull"] / MT, 2), num(t["outer_wall"] / MT, 2),
                     num(t["bulkheads"] / MT, 2), num((t["panels"] + t["cell_walls"] + t["bumper"]) / MT, 2),
                     f"**{num(t['total'] / MT, 2)}**", num(out["model_hull_frames"] / MT, 2),
                     f"{t['total'] / out['model_hull_frames'] - 1:+.0%}", f"{steel_fe / steel_model - 1:+.0%}",
                     sizing_status(out)])
    layout = []
    for r in (900, 1600, 2500):
        for anchors in ts.ANCHORS:
            for ceiling in ts.CEILINGS:
                if r == 2500 and ceiling == "hung":
                    continue
                out = ts.run(p, r, anchors, ceiling)
                forces = ", ".join(f"{a}°: {num(f / 1e6)}" for a, f in sorted(out["anchor_force"].items()) if f > 0)
                layout.append([size_label(r), anchors, ceiling, num(out["per_metre"]["total"] / 1e3),
                               num(out["per_torus"]["total"] / MT, 2), forces,
                               num(-out["max_compression"] / 1e6, 2), num(out["max_displacement"], 2),
                               sizing_status(out)])
    sens = []
    base = ts.run(p, 900, "sides", "vaulted")["per_torus"]["total"]
    for name, value in (("plate_stress_mpa", 200), ("plate_stress_mpa", 500), ("skin_min_gauge_m", 0.005),
                        ("skin_min_gauge_m", 0.02), ("cell_wall_min_gauge_m", 0.01), ("bumper_m", 0.003)):
        q = params(load(), **{**vars(p), name: value})
        t = ts.run(q, 900, "sides", "vaulted")["per_torus"]["total"]
        sens.append([f"`{name}` = {value:g}", num(t / MT, 3), f"{t / base - 1:+.0%}"])
    return "\n\n".join([
        "## Tube cross-section: hull and frames by finite elements",
        "One metre of tube in the plane of its cross-section (`structure_model/tube_section.py`): the pressure "
        "hull and the outer cell wall as membrane skins, the jacket's transverse bulkheads (one every "
        f"{p.cell_size_m:g} m) smeared into a plane-stress annulus between them, the rock, fill, lakes, air, "
        "bumper and steel under spin gravity, 70 kPa on the hull, and the chords' anchors on the outer wall "
        "holding the section along the radius. Every part is sized fully stressed at "
        f"{p.plate_stress_mpa:g} MPa (von Mises at every integration point; half that in compression, blended "
        "with tension by the compression's share of the stress state, an allowance for stiffeners), or held "
        f"at its minimum gauge ({p.skin_min_gauge_m * 100:g} cm for the skins, {p.cell_wall_min_gauge_m * 1000:g} mm "
        "for bulkheads and cell walls). The skins also carry the hull's lengthwise pressure load and the pillowing "
        "of their panels between bulkheads; the hub-facing hull panels pressed in by the rock get stiffeners "
        "(vaulted ceiling), or the rock rests on hung cell floors instead (hung). Panels, cell walls and bumper are "
        "together in one column. Each anchor is a fitting through the jacket's depth, spreading the chord's pull over "
        "the radial line of nodes at its angle and pinned at the chord's attachment on the outer wall (a force, no "
        "couple). **Sizing:** *fully stressed* when every part is within 2% of its allowable or at "
        "its minimum gauge; *safe* when none is over it but some still have spare capacity after 200 rounds "
        "(heavier than needed); *over* when some part still exceeds it (not a design).",
        "### Chords anchored at the tube's two sides (one net in each side plane), vaulted ceiling",
        table(["Torus", "Load (MN per m of tube)", "Hull (Mt)", "Outer wall (Mt)", "Bulkheads (Mt)",
               "Panels, cell walls, bumper (Mt)", "Hull and frames (Mt)", "System model, r^2.3 (Mt)",
               "Difference", "Steel per torus (with spokes) vs model", "Sizing"], rows),
        "### Where the chords anchor",
        "Anchors on the hub-facing crest (one net in the torus's mid-plane), at the two sides, or spread over the "
        "hub-facing half (anchors that would push are released; the rest share the load). Anchor loads per metre "
        "of tube; compression is the largest compressive force in a skin; displacement includes the section's "
        "ovalisation.",
        table(["Torus", "Anchors", "Ceiling", "Steel (t per m of tube)", "Per torus (Mt)",
               "Anchor loads (MN/m)", "Max skin compression (MN/m)", "Max displacement (m)", "Sizing"], layout),
        "### Sensitivity at 900 m (sides, vaulted)",
        table(["Change", "Hull and frames (Mt)", "vs base"], sens),
        "Not modelled: buckling of the parts in compression (sized with an allowance only), segment joints and "
        "seals, the anchors' local details, and the valley's buildings, light box and ceiling.",
    ])


def rest_section(p):
    """The baseline: built at rest, spun up finished (rest.py)."""
    mpa = lambda x: num(x / 1e6)
    rows, path_rows, path_text = [], [], []
    for r in (900, 1600):
        s, m, info = rest.at_rest(p, r)
        te = info["net"]["tension_end"]
        th = rest.thermal(p, r)
        b = rest.buckling(p, r) if r == 900 else None
        rows.append([size_label(r), f"{num(s['tension_min'] / te * 100, 2)}–{num(s['tension_max'] / te * 100, 2)}%",
                     mpa(-s["hull_min"]), num(s["joint_compression"] / 1e6),
                     f"{mpa(-th['cold']['hull_min'])} / {num(th['warm']['tension_min'] / te * 100, 2)}%, "
                     f"{th['warm']['slack'] + th['cold']['slack']} slack",
                     num(b["factor"]) + "×" if b else "—"])
    for scatter in (False, True):
        res = rest.spin_up(p, 900, scatter=scatter)
        te = res["tension_end"]
        label = "as drawn" if not scatter else (f"scattered: chords ±{rest.LENGTH_SCATTER * 100:g} cm, mass per "
                                                  f"anchor ±{rest.MASS_SCATTER:.0%} (1σ)")
        for st in res["states"]:
            path_rows.append([label, num(st["spin"], 2),
                              f"{num(st['tension_min'] / te, 3)}–{num(st['tension_max'] / te, 3)}",
                              f"{mpa(st['hull_min'])} to {mpa(st['hull_max'])}", num(st["hull_bending"] / 1e6, 2),
                              f"{st['open']}/{st['joints']}",
                              f"{num(st['gap_min'] * 100)}–{num(st['gap_max'] * 100)}" if st["open"] else "closed",
                              num(st["joint_compression"] / 1e6)])
        path_text.append(
            f"{label.capitalize()}: the joints open at ~{num(res['spin_open'], 2)} of the spin; every chord's tension "
            f"on the way is at most {num(res['chord_path_ratio'], 4)}× its own at full spin; the hull's worst is "
            f"{mpa(res['hull_compression_peak'])} MPa of compression at rest ({mpa(res['hull_final'])} MPa along it "
            f"at full spin), its bending at most {num(res['bending_peak'] / 1e6, 2)} MPa "
            f"({num(res['bending_final'] / 1e6, 2)} at full spin); finished, the chords at "
            f"{num(res['final']['tension_min'] / te, 3)}–{num(res['final']['tension_max'] / te, 3)}× the formula "
            f"(peak {num(res['final']['peak_stress'] / res['sigma'], 3)}× the allowable) and the joints open by "
            f"{num(res['final']['gap_min'] * 100)}–{num(res['final']['gap_max'] * 100)} cm.")
    hub_rows, torque_rows, cost_rows = [], [], []
    for r in (900, 1600):
        s, _, info = rest.at_rest(p, r)
        share = (s["tension_min"] + s["tension_max"]) / 2 / info["net"]["tension_end"]
        ln = rest.lines(p, r)
        hub_rows.append([size_label(r), f"{ln['s0']:.1%}", num(ln["bow"], 2),
                         f"{num(ln['as_sized_ratio'], 2)}×",
                         f"{num(ln['area'] * 1e6)} ({num(ln['area'] / ln['area_finished'], 2)}×)",
                         f"{num(ln['pull_rest'])} N / {num(ln['pull_full'] / 1e3)} kN",
                         f"{num(ln['gap_rest'], 2)} / {num(ln['gap_full'], 2)} ({num(ln['gap_finished'], 2)})",
                         f"{num(ln['k_rest'] / 1e6, 2)} / {num(ln['k_full'] / 1e6)}",
                         f"{num(ln['margin_min'], 2)} ({num(ln['margin_finished'], 2)})",
                         num(ln["dock_offset"] * 100), num(ln["period_s"]),
                         f"{num(ln['mass'] / 1e3)} ({num(ln['mass_finished'] / 1e3)})",
                         f"{num(ln['hub_ring_force'] / 1e6)} MN; {num(ln['hub_ring_mass'] / 1e3)} t"])
        t = rest.torque(p, r)
        ft = rest.farm_twist(t, share)
        torque_rows.append([size_label(r), f"{t['alpha']:.1e}", num(t["torque"] / 1e6), num(t["thrust"] / 1e3),
                            f"{t['rim_ratio']:.0e}", f"{num(ft['rest_rim'] * 100)} / {num(ft['full_rim'] * 100, 2)}",
                            f"{t['hub_twist']:.0e}; {num(t['laced_force'] / 1e3, 2)} of {num(t['line_capacity'] / 1e3)}",
                            f"{num(t['mismatch_torque'] / 1e6)} MN·m; {num(t['lattice_force'] / 1e3)} kN",
                            f"{t['water_spin_drop']:.1%}"])
        for name, o in t["options"].items():
            cost_rows.append([size_label(r), name, num(o["exhaust"] / 1e3, 2), num(o["propellant"] / MT, 2),
                              num(o["energy"] / 1e15, 2), num(o["days_at_power"])])
    f = rest.fill(p, 900)
    fill_rows = [[f"loose, {d['density']:g} t/m³", num(d["areal"], 3), num(d["jacket_dose"]),
                  f"{d['strain']:.0%}", num(d["floor_settle"] * 100), num(d["slot"] * 100), num(d["slot_dose"]),
                  num(d["top_up"] / MT, 2)] for d in f["loose"].values()]
    fill_rows += [[f"compacted at rest, M = {num(d['modulus'] / 1e6)} MPa", num(d["areal"], 3), num(d["jacket_dose"]),
                   "—", num(d["floor_settle"] * 100, 2), num(d["slot"] * 100, 2), num(d["slot_dose"], 2), "—"]
                  for d in f["compacted"].values()]
    return "\n\n".join([
        "## The baseline: built at rest, spun up finished",
        "A child's stack is assembled at rest (`structure_model/rest.py`): every ring closed, the lattice "
        "fitted, the rock and soil in; then spun up slowly with the water last. In the ring's plane, with the "
        "geometrically nonlinear model above, the joints sliding along the rim but **bearing on stops**: closed "
        "(compression) they act locked, rocking once their moment passes their compression times the tube's "
        f"radius; open, they slide on a light spring along the rim (~10⁸ N/m, below). The "
        "chords are pretensioned to a strain of 5 × 10⁻⁴ as installed, to stay taut through a "
        f"±{rest.THERMAL_SWING:g} K swing of their temperature against the hull's (a guess; α ΔT = "
        f"{rest.ALPHA_STEEL * rest.THERMAL_SWING:.1e}).",
        "### At rest",
        "With no spin load, only the hull resists the chords' pull: the closed ring is squeezed, its joints "
        "bear, and most of the installed stretch goes into the hull's shortening (the chords keep only a few % "
        f"of their finished tension). Allowable compression {mpa(rest.HULL_COMPRESSION)} MPa (half the plate "
        "stress, as in the cross-section). Thermal swing: the chords colder (hull's compression) / warmer (the "
        "least chord tension). Buckling in the plane: the pretension at which the ring's lowest stiffness "
        f"vanishes, over the 5 × 10⁻⁴ used (the chords hold it far beyond the free ring's 3EI/r²). "
        "Scattered as built (below).",
        table(["Torus", "Chords (% of finished)", "Hull compression (MPa)", "Joints' compression (MN)",
               "Cold: hull (MPa) / warm: least chord", "Buckling margin"], rows),
        "### Spinning up: the cables take up tension, the joints open",
        "The spin stepped up from rest to full at 900 m, each step from the last equilibrium. Spin as a share of "
        "the final rate; chords as a share of the finished tension; hull stress along the rim (negative: "
        "compression) and in bending; joints open and their gap.",
        table(["Ring", "Spin", "Chords (× finished)", "Hull along the rim (MPa)", "Hull bending (MPa)",
               "Joints open", "Gap (cm)", "Joints' compression (MN)"], path_rows),
        " ".join(path_text),
        "**So nothing exceeds the finished state on the way, except the at-rest pretension:** the hoop's "
        "compression in the hull and on the joints' stops, which falls linearly with the spin load and is gone "
        "by about a third of the spin, when the joints open together and the chords carry the rim alone, as "
        "finished. The scattered ring's finished chords spread by ±~7% (mostly the mass scatter): the "
        "finished net's own tolerance, not the spin-up's; it needs the rim's mass placed within ~2% per anchor, "
        "or the chords trimmed after spin-up, or a little more safety margin.",
        f"**The joints need a spring along the rim.** With joints that only slide, the segments' positions "
        "along the rim are barely held: the chords are nearly diametral, so segments sliding in odd harmonics "
        "hardly stretch them, and a 2% scatter in the rim's mass slides segments by up to ~1–2 m at a fifth of "
        f"the spin (and the solution doesn't converge). A spring of ~10⁸ N/m in each joint "
        "holds them to the gaps above for a few MPa along the hull; ~10⁷ N/m is too soft to settle, ~10⁹ N/m "
        "puts ~30 MPa in the hull. The joints travel ~0.15–0.4 m each by full spin (and ~2 cm more each as the chords "
        "creep, ~0.5 m per chord at 900 m: the wire, above).",
        "### The hub's stabilising lines, from rest to full spin",
        "The lines (section on the hub, below) as fixed-length, tension-only lines from the hub's surface to the "
        "chords' tangent points, in series with chords whose tension and bow grow with the spin. A chord bows "
        "away from the axis by its own spin load over its tension: nothing at rest, the finished bow from where "
        "the joints open (its tension grows from its at-rest share, linearly while the joints bear, then with "
        "the spin). A line cut to a fixed length is stretched by the chord's free movement outward less what its "
        "pull draws the chord in: P = k_s (bow + d0), k_s the line and chord in series at the current tension "
        "and spin, d0 the pull-in it is installed with at rest, enough to stay taut "
        f"({hub.TAUT_MARGIN:g}× the swing) under a {rest.SHIP_MASS / 1e6:g} kt ship docking at "
        f"{rest.SHIP_CLOSING:g} m/s over {rest.BUFFER:g} s. **So a fixed line holds back the whole bow,** and the "
        "lines sized for the finished net (its service preload, a few kN) would be overloaded; sized for it, "
        "with their stiffness and pull iterated. Window: the gap around the hub at rest / at full spin with the "
        "chords drawn in (finished sizing's, bowed). Margin: the hub's lateral stiffness over its divergence, "
        "the least through the spin-up (finished). The lines' pull loads the hub's shell outward all round each "
        "net's plane: a ring frame there, at the plate stress.",
        table(["Torus", "Chords at rest", "Finished bow (m)", "Fixed lines at the finished sizing: peak / allowable",
               "Line area sized for the bow (mm²)", "Line pull at rest / full spin", "Window, rest / full (m)",
               "Lateral stiffness, rest / full (MN/m)", "Least margin", "Docking offset at rest (cm)",
               "Hub's period at rest (s)", "Lines' mass (t)", "Hub ring frames, per net; both nets"], hub_rows),
        "**Lines installed snug at rest and sized for the bow (proposed)** keep every line taut and the hub held "
        "from rest to full spin, its margin never below the finished one; they cost ~1.7× the finished sizing's "
        "area but are shorter (the window narrower by the bow), so only a little more mass, plus a ring frame in "
        "the hub at each net. The alternative, lines paid out by the bow as the spin grows (winches, locked at "
        "full spin), keeps the finished sizing and window but adds machinery that must work during the spin-up.",
        "### The spin-up's torque",
        f"Thrusters on each ring's rim sized to its own inertia; bounded by a fast spin-up, {rest.FAST_SPINUP_DAYS:g} "
        "days. Per torus with its hub share and farm ring. Rim: the tangential load over the centrifugal at "
        "full spin. Farm ring: its twist at its rim if it is turned by the hub through its radial spokes rather "
        "than its own thrusters (at rest / full spin; the spokes resist only by their tension, pretensioned like "
        "the chords). Hub: its twist (rad) through 0.2% of the stabilising lines laced (section 11), and the "
        f"force per laced line against its strength. Lattice: one torus's thrusters {rest.THRUST_MISMATCH:.0%} off "
        "their share, carried across a gap (a braking rim train puts ~40–120 MN·m on a lattice). Water: the "
        "spin lost as the water arrives from the axis, made up by thrust.",
        table(["Torus", "α (rad/s²)", "Torque (MN·m)", "Thrust (kN)", "Rim: tangential / spin load",
               "Farm ring twist at its rim (cm)", "Hub twist; laced line force (kN)", "Thrust mismatch; lattice force",
               "Water last: spin lost"], torque_rows),
        "The spin-up's cost, for the angular momentum of a torus with its hub and farm ring at full spin, "
        "delivered at the envelope's outer rim, at the torus's own power (its array, `habitat_model`):",
        table(["Torus", "Reaction mass", "Exhaust (km/s)", "Propellant (Mt)", "Energy (PJ)", "Days at the torus's power"],
              cost_rows),
        "**The angular acceleration is negligible:** even at the fast rate its loads are millionths of the "
        "spin's; a farm ring turned through its radial spokes alone lags ~0.25–0.8 m at its rim at rest "
        "(centimetres at full spin), so it gets its own thrusters or simply follows; the laced lines and the "
        "lattice carry it with ample margin. What sets the spin-up is energy: water thrusters take years of the "
        f"torus's own power, host rock thrown by a mass driver at ~{rest.ROCK_DRIVER_EXHAUST:g} km/s ~5–7 months "
        "(proposed; ~6× the reaction mass, of rock mined anyway). The stack at rest has no gyroscopic stiffness, "
        "so the thrusters' sideways torques must be balanced or held by the attitude thrusters until the spin "
        "builds (not modelled).",
        "### The fill as gravity grows",
        "The rock and soil are placed at rest, in the jacket's cells, whose volume is fixed "
        f"({f['jacket']:g} m of jacket, {p.rock_density:g} t/m³ finished, ~{f['porosity_final']:.0%} porosity on "
        f"~{rest.GRAIN_DENSITY:g} t/m³ chondrite grains). **Filled loose, a cell holds less rock than the design:** "
        f"the shield is short of its {p.shield_areal_t_m2:g} t/m² everywhere, floor and ceiling included, and "
        "settling keeps that mass without restoring it (review of #18). Dose at a sphere's centre behind what "
        "is installed, OLTARIS's regolith curve (the design's at "
        f"{p.shield_areal_t_m2:g} t/m²: {num(f['design_dose'])} mSv/yr). Loose fill also settles by its porosity as "
        "the spin grows: through the jacket's thickness on the floor and ceiling, but at the tube's two sides its "
        f"cells' columns run along the radius, a cell high ({f['cell']:g} m), and a settled cell leaves a slot at "
        "its top through the jacket's whole thickness. A slot h high in a wall t thick lets through, "
        "unshielded, ~h/4t of the directions seen from the valley at its height, both side walls together twice "
        "that: the dose it adds there, against the jacket left around it, is rough. Compacted to its final "
        "density as placed, the fill holds the design's mass and settles only by its elastic compression under "
        "its own weight at full spin. Top-up: the rock that loose cells lack, per 900 m torus, to be added to "
        "every cell.",
        table(["Fill placed", "Shield installed (t/m²)", "Dose behind it (mSv/yr)", "Settling strain",
               "Settling through the jacket (cm)", "Slot at the sides (cm)", "Added at the slots' height (mSv/yr)",
               "Top-up to the design (Mt)"], fill_rows),
        "**The fill must be compacted as it is placed (proposed).** Loose, the shield is short everywhere "
        "(~19–38 mSv/yr behind it, against the design's ~15) and the slots add tens of mSv/yr where they face; "
        "making it good would take topping up every cell, not only the sides, with ~0.55–2.2 Mt of rock per "
        "900 m torus, after spin-up and through fill ports. Settling unevenly moves the rim's first moment by ~"
        f"{num(f['first_moment'] * 100)} cm × its mass even loose, within the ballast's {f['ballast'] * 100:g} "
        f"cm, and slows the spin by ~{f['spin_drop']:.2%}. The loads the fill puts on its cells grow with the "
        "spin to their finished values (the cross-section above).",
        "Not modelled: out of the ring's plane (the ring's buckling sideways, the two nets apart), the joints' "
        "stops and springs as hardware, the fill's flow and arching in its cells, the stack's attitude while at "
        "rest, the despun array.",
    ])


def hub_report(p):
    finished, cases, build = [], [], []
    for r in SIZES:
        res = evaluate(p, Design(radius_m=r, n_tori=1))
        out = hub.compute(p, res["geometry"], res["mass"])
        low, high = out["rotating_vs_spin"]
        finished.append([
            size_label(r), num(out["hub_mass"] / MT, 2), num(out["gap"], 2), f"{out['n_lines']:,}",
            f"{num(out['k_chord'] / 1e3)} ({out['k_chord'] / out['k_chord_string'] - 1:+.0%})",
            num(out["k_torus"] / 1e6), num(out["margin"], 2),
            f"{num(out['natural_vs_spin'], 2)}; {num(low, 2)} and {num(high, 2)}",
            num(out["k_tilt"] / 1e9), f"{num(out['k_axial'] / 1e6, 2)} / {num(out['k_axial_inclined'] / 1e6)}",
            f"{num(out['axial_natural_vs_spin'], 2)} / {num(out['axial_inclined_natural_vs_spin'], 2)}",
            num(out["k_torsion"] / 1e9, 2), num(out["line_area"] * 1e6), num(out["service_preload"] / 1e3, 2),
            f"{num(out['line_mass'] / 1e3, 2)} (+{num(out['inclined_extra_mass'] / 1e3, 2)})"])
        cases.append([size_label(r)] + [f"{num(abs(c['relative']) * 100, 2)} cm / {num(abs(c['force']) / 1e6, 2)} MN"
                                        for c in out["cases"].values()])
        for pairs, b in out["build"].items():
            unbraced = ("grows ×e every " + num(b["e_folding_unbraced_spins"], 2) + " turns"
                        if b["growth_unbraced"] else "stable")
            offset = num(abs(b["offset"]), 2) + (" (**more than the gap**)" if abs(b["offset"]) > out["gap"] else "")
            build.append([size_label(r), "one opposite pair" if pairs == 1 else "two pairs at right angles",
                          str(b["chords"]), num(b["margin_unbraced"], 2), unbraced,
                          num(b["preload"] / 1e3), num(b["swing"] / 1e3), num(b["pull_in"], 2), offset,
                          num(abs(b["force"]) / 1e6, 2)])
    names = list(out["cases"])
    return "\n\n".join([
        "## The hub in the nets: stabilising lines",
        "Each torus has two chord nets, one in each side plane of its tube. In each, the chords pass the hub "
        "tangent to a circle 1.1 × its radius, bowed outward by their spin load, leaving a window gap around it. "
        "A short line runs from the hub to every chord's tangent point (`structure_model/hub.py`). A chord pulled "
        "sideways at its middle resists like a taut string, 2T/L, a little less under its own spin load (shown in "
        "brackets); lines and chords act in series, and N lines spread around the window give N k / 2 in any "
        "direction of a net's plane, twice that for the torus's two nets. The hub's share is the system model's "
        f"hub, dock and factory metal ({p.hub_factory_metal_frac:.0%} of the torus steel). The torus and its hub "
        "move relative to each other with their reduced mass μ; off the axis they are pulled apart by μω²x, so the "
        "margin is K / μω². In the rotating frame Coriolis couples the two directions of the window's plane: the "
        "relative motion has two modes, at |√(K/μ) ∓ ω| (√(K/μ) seen from outside). Lines are preloaded "
        f"{hub.TAUT_MARGIN:g}× their largest swing of tension, in service and while building, and the area, "
        "preload, stiffness and loads are iterated until they agree, every line taut and within the wire stress.",
        "### Finished torus",
        table(["Torus", "Hub share (Mt)", "Window gap (m)", "Lines", "Chord stiffness (kN/m)",
               "Lateral stiffness (MN/m)", "Margin K / μω²", "Natural frequency / spin: inertial; rotating modes",
               "Tilt stiffness (GN·m/rad)", f"Axial stiffness (MN/m): radial lines / {hub.INCLINED_FRAC:.0%} inclined",
               "Axial natural frequency / spin", "Torsional stiffness (GN·m/rad)", "Line area (mm²)",
               "Service preload (kN)", "Lines' mass (t), + inclined option"], finished),
        "Radial lines hold the hub along the axis only through their preload: its axial natural frequency is "
        f"below the spin rate. Running {hub.INCLINED_FRAC:.0%} of the lines from the hub's mid-plane out to the side "
        "nets, over their full length (the gap and the nets' offset from the mid-plane), holds it ~8–25× more "
        "stiffly (second figure; a chord resists sideways pulls out of its plane alike), for the extra line mass "
        "shown. Torsion is likewise held by preload only.",
        "### Loads on the hub (finished torus, full spin): offset of the hub from the torus / force in the lines",
        f"Hub imbalance: {hub.HUB_IMBALANCE_FRAC:.0%} of the hub's mass at its rim. Torus imbalance: a "
        f"{hub.ARC_MISMATCH:.0%} mismatch between two opposite arcs of 4θr, never ballasted. Orbit thrust: "
        f"{hub.ORBIT_ACCEL:g} m/s² for the torus, pushed through its hub (notes §15). The torus and its hub turn "
        "about their common centre of mass.",
        table(["Torus"] + [n.capitalize() for n in names], cases),
        "### Building: the first arcs",
        f"At {hub.BUILD_SPIN:g} of the final spin (net_statics), with a {hub.ARC_MISMATCH:.0%} mismatch between the "
        "arcs of a pair. A pair's chords run between its two arcs, nearly parallel: the lines hold the hub across "
        "them, but along them only through the arcs' small spread and the lines' preload. A second pair at right "
        "angles holds that direction. The preload is the larger of what gives the stiffness margin and what keeps "
        f"every line {hub.TAUT_MARGIN:g}× above its swing; the stiffness differs by direction, so the modes are "
        "solved: without preload a single pair is an asymmetric rotor and the hub's motion grows. Pull-in: how far "
        "the preload draws those chords into the window.",
        table(["Torus", "First stage", "Chords per net", "Margin without preload", "Without preload",
               "Preload (kN)", "Swing of tension (kN)", "Chord pull-in (m)", "Hub offset from the arcs (m)",
               "Force in the lines (MN)"], build),
        "Not modelled: the hub as a beam between tori and the stack's modes (plan §4), the elevator, pipe and "
        "power shafts and their compliant joints, docking loads (set by the dock's buffers), and torque through "
        "the lines.",
    ])


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m structure_model", description=__doc__)
    ap.add_argument("--anchor-spacing", type=float, default=10.0, help="m of rim per anchor (default 10)")
    ap.add_argument("--mismatch", type=float, default=0.01, help="mass mismatch between paired arcs (default 0.01)")
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    p = params(load(), **dict(args.set))
    print("\n\n".join(["# Structure: wire, cable net, spin-up and the tube's cross-section", wire_section(p),
                       net_section(p, args.anchor_spacing), construction_section(p), rest_section(p), sequence_section(p),
                       imbalance_section(p, args.mismatch), hub_report(p), tube_section_report(p)]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
