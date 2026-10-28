"""Structure (plan §2), first part: wire strength, the tangent-chord net and the spin-up of a partial ring.

python -m structure_model [--anchor-spacing 10] [--mismatch 0.01] [--set name=value ...]
"""

import argparse
import math
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import cable_net, net_statics, spinup, wire

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


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m structure_model", description=__doc__)
    ap.add_argument("--anchor-spacing", type=float, default=10.0, help="m of rim per anchor (default 10)")
    ap.add_argument("--mismatch", type=float, default=0.01, help="mass mismatch between paired arcs (default 0.01)")
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    p = params(load(), **dict(args.set))
    print("\n\n".join(["# Structure: wire, cable net and spin-up", wire_section(p),
                       net_section(p, args.anchor_spacing), construction_section(p),
                       imbalance_section(p, args.mismatch)]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
