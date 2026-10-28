"""Structure (plan §2), first part: wire strength, the tangent-chord net and the spin-up of a partial ring.

python -m structure_model [--anchor-spacing 10] [--mismatch 0.01] [--set name=value ...]
"""

import argparse
import math
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import cable_net, spinup, wire

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
    rows, build = [], []
    for r in SIZES:
        res = evaluate(p, Design(radius_m=r, n_tori=1))
        g, m = res["geometry"], res["mass"]
        n = cable_net.compute(r, m["rim"], g["omega"], g["hub_radius"], p.wire_stress_mpa * 1e6,
                              p.steel_density, anchor_spacing=spacing)
        rows.append([size_label(r), f"{math.degrees(n['theta']):.1f}°", num(n["mass_uniform"] / 1e9),
                     num(m["spokes"] / 1e9), f"{n['chord_vs_radial']:+.2%}", f"{n['taper_saving']:.1%}",
                     num(n["taper_ratio"]), num(n["tension_end"] / 1e6), num(n["wire_area_end"] * 1e4),
                     num(n["bow"], 2)])
        lam = m["rim"] / (2 * math.pi * r)
        s = spinup.partial_arc(r, n["theta"], lam, g["omega"])
        arc_mass = lam * s["min_arc"]
        build.append([size_label(r), num(s["end_zone"]), num(s["min_arc"]), num(arc_mass / 1e9, 2),
                      num(s["joint_tension"] / 1e6), f"{s['joint_tension_vs_hoop']:.1%}",
                      num(s["joint_steel_area"], 2), num(s["joint_tension"] / 4 / 1e6)])
    return "\n\n".join([
        f"## Tangent-chord net (chords tangent at 1.1 × the hub radius, one anchor every {spacing:g} m)",
        table(["Torus", "Chord angle at the rim", "Net, uniform chords (Mt)", "System model spokes (Mt)",
               "Chords vs radial spokes", "Saved by tapering", "Taper (mid / end area)",
               "Tension per chord end (MN)", "Wire area per chord end (cm²)", "Bow at mid-chord (m)"], rows),
        "## Building the ring: opposite arcs in a partial net\n\n"
        "Each arc's two end zones are single-laced and pull the arc lengthwise; the joints carry that "
        "tension until the ring closes. Values at full spin (they scale with spin²; at half spin, a quarter).",
        table(["Torus", "Single-laced end zone (m)", "Shortest arc (m)", "Its rim mass (Mt)",
               "Joint tension (MN)", "vs a full ring's hoop force", "Plate steel at 500 MPa (m²)",
               "Joint tension at half spin (MN)"], build),
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
        margin = 0.1 * g["hub_radius"]
        rows.append([size_label(r), num(arc / 1e9, 2), num(first, 2), num(margin), num(full * 100, 2)])
    return "\n\n".join([
        f"## Imbalance: one arc {mismatch:.0%} heavier than its partner\n\n"
        "The stack spins freely about its centre of mass, so a mismatch moves the hub off the spin axis "
        "(it doesn't load a bearing). Hub, dock and factory taken as 25% of the torus steel. The gap between "
        "the hub and the chords' tangent circle (0.1 × the hub radius) must exceed the offset.",
        table(["Torus", "Shortest arc (Mt)", "Hub offset, first pair alone (m)", "Gap hub to chords (m)",
               "Hub offset, finished torus if never ballasted (cm)"], rows),
    ])


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m structure_model", description=__doc__)
    ap.add_argument("--anchor-spacing", type=float, default=10.0, help="m of rim per anchor (default 10)")
    ap.add_argument("--mismatch", type=float, default=0.01, help="mass mismatch between paired arcs (default 0.01)")
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    p = params(load(), **dict(args.set))
    print("\n\n".join(["# Structure: wire, cable net and spin-up", wire_section(p),
                       net_section(p, args.anchor_spacing), imbalance_section(p, args.mismatch)]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
