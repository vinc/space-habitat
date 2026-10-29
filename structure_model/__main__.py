"""Structure (plan §2): wire strength, the tangent-chord net, the spin-up of a partial ring and the tube's cross-section.

python -m structure_model [--anchor-spacing 10] [--mismatch 0.01] [--set name=value ...]
"""

import argparse
import math
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import cable_net, net_statics, spinup, tube_section, wire

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


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m structure_model", description=__doc__)
    ap.add_argument("--anchor-spacing", type=float, default=10.0, help="m of rim per anchor (default 10)")
    ap.add_argument("--mismatch", type=float, default=0.01, help="mass mismatch between paired arcs (default 0.01)")
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    p = params(load(), **dict(args.set))
    print("\n\n".join(["# Structure: wire, cable net, spin-up and the tube's cross-section", wire_section(p),
                       net_section(p, args.anchor_spacing), construction_section(p),
                       imbalance_section(p, args.mismatch), tube_section_report(p)]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
