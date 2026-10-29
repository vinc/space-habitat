"""Stack dynamics (plan §4): whirl modes of the flexible spinning stack and its passive stability.

python -m dynamics_model [--set name=value ...]
"""

import argparse
import math
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import stack as st

CASES = ((900, 2), (900, 6), (1600, 2), (1600, 6))
RIM_LINK = 1e11            # N/m between neighbouring tori's rims, for the stack-length study
TIES = 1e-4                # share of the torus's mass in radial ties, for the stack-length study
DAMPING = 0.01             # dissipation turning with the stack, for the damped check
TARGET = 1.2               # lowest forward whirl over the spin: §11's 20% margin


def size_label(r):
    return f"{r / 1000:g} km" if r >= 1000 else f"{r:g} m"


def link_shell(geo, k, steel_density, shear_modulus=77e9):
    """A thin cylinder joining neighbouring rims across the gap: shear stiffness G pi R t / gap.
    Returns its thickness and mass for a lateral stiffness k."""
    radius, gap = geo["radius"] - geo["tube_radius"], max(geo["gap"], 1.0)
    t = k * gap / (shear_modulus * math.pi * radius)
    return t, 2 * math.pi * radius * t * gap * steel_density


GROWTH_FLOOR = 1e-6       # growth rates below this share of the spin are numerical noise


def growth_note(growth, omega):
    if growth <= GROWTH_FLOOR * omega:
        return "stable"
    return f"grows ×e every {num(1 / growth / 3600, 2)} h"


def report(p):
    base, fixes = [], []
    for r, n in CASES:
        d = Design(radius_m=r, n_tori=n)
        s, info = st.build(p, d)
        m, w = info["mass"]["total"], info["geometry"]["omega"]
        _, growth = s.modes(damping=DAMPING)
        base.append([size_label(r), str(n), num(2 * info["nets"]["k_plane"] / (m * w * w), 2),
                     num(s.rigid_ratio(), 3), num(s.forward_ratio(), 2), growth_note(float(growth.max()), w)])
        link = st.required(p, d, "rim_link", target=TARGET, low=1e6, high=1e13)
        ties = st.required(p, d, "tie_frac", target=TARGET, low=1e-6, high=0.1)
        fixed, _ = st.build(p, d, rim_link=RIM_LINK, tie_frac=TIES)
        _, g_fixed = fixed.modes(damping=DAMPING)
        if link:
            thickness, link_mass = link_shell(info["geometry"], link, p.steel_density)
            link_text = f"{link:.1e} N/m ({num(thickness * 1000, 2)} mm shell, {num(link_mass / 1e3, 2)} t per link)"
        else:
            link_text = "not enough alone"
        fixes.append([size_label(r), str(n), link_text,
                      f"{ties:.2%} ({num(ties * m / 1e6, 2)} kt per torus)" if ties else "not enough alone",
                      num(fixed.forward_ratio(), 3), growth_note(float(g_fixed.max()), w)])
    lengths = []
    for r in (900, 1600):
        for n in (2, 6, 10, 14, 18, 22):
            d = Design(radius_m=r, n_tori=n)
            s, info = st.build(p, d, rim_link=RIM_LINK, tie_frac=TIES)
            h, length = info["geometry"]["hub_radius"], info["geometry"]["stack_length"]
            budget = info["hub_share"] / (2 * math.pi * h * length * p.steel_density)
            need = st.required(p, d, "hub_shell_m", target=TARGET, low=1e-3, high=budget, rim_link=RIM_LINK,
                               tie_frac=TIES)
            best = st.build(p, d, rim_link=RIM_LINK, tie_frac=TIES, hub_shell_m=budget)[0].forward_ratio()
            lengths.append([size_label(r), str(n), num(length), num(s.rigid_ratio(), 3),
                            num(s.forward_ratio(), 3), num(need * 100, 2) if need else "**not enough**",
                            num(budget * 100), num(best, 3)])
    shell_cm = p.hub_shell_m * 100
    return "\n\n".join([
        "# Stack dynamics: whirl modes and passive stability",
        "The stack as one flexible spinning body (`dynamics_model/stack.py`): the shared hub as a thin-walled beam "
        f"(radius from the system model, wall {num(shell_cm)} cm unless stated, its mass the system model's hub, dock "
        "and factory metal spread along it), each torus a rigid thin ring tied to the hub at its two net planes "
        "by the nets' lateral stiffness (`structure_model/hub.py`), each farm ring a rigid ring on radial spokes in "
        "two planes, the despun array a mass at the far end. Lateral motion in the inertial frame, complex "
        "coordinates: M q'' − iωG q' + K q = 0, G the spinning parts' polar inertia.",
        "**Criterion.** Dissipation that turns with the stack (lakes, people, flexing structure) destabilises every "
        "forward whirl slower than the spin, so the stack is passively stable only if its lowest forward mode "
        "whirls faster than the spin (drift and precession aside). For a rigid stack that mode is its nutation, "
        "at J/I_t times the spin: §11's maximum-axis rule. The ratio below is the flexible stack's equivalent of "
        f"§11's inertia ratio; {TARGET:g} keeps its 20% margin. A damped solve ({DAMPING:.0%} of the stiffness, "
        "turning with the stack) checks it.",
        "## The stack as designed: nets only",
        "Torus centring: the nets' lateral stiffness over the centrifugal pull on a torus off the axis (mω²). The "
        "tangent chords carry a torus's spin load from rim to rim, so nothing in the main load path holds it on "
        "the shared axis: only the stabilising lines, deflecting the chords sideways, which comes to ~mω²/2 at "
        "every size. A torus alone just turns about its own centre with its hub; in a stack, held by the others "
        "through the hub, it drifts outward.",
        table(["Torus", "Tori", "Torus centring (K / mω²)", "Rigid J/I_t", "Lowest forward whirl / spin",
               "Damped"], base),
        "## Fixes",
        "Rim links: neighbouring tori joined at their rims (tunnels, or a thin cylinder across the gap; its tilt "
        "stiffness taken as k r²/2, low for a cylinder), so the tori move and tilt together. Radial ties: steel "
        "from the hub to each torus's hub-facing side, in its net planes, stiff along its length and carrying no "
        f"spin load. Each alone, for a margin of {TARGET:g}; then both together ({RIM_LINK:.0e} N/m links and "
        f"{TIES:.2%} ties).",
        table(["Torus", "Tori", "Rim links alone", "Radial ties alone", "Both: lowest forward whirl / spin",
               "Damped"], fixes),
        "## How long a stack: the hub's wall",
        f"With rim links ({RIM_LINK:.0e} N/m) and a trace of ties ({TIES:.2%}), long stacks are limited by the hub "
        "bending with the farm section at its end. Wall needed for a margin of "
        f"{TARGET:g}, against the wall the hub's whole mass budget would make (the system model's hub, dock and "
        "factory metal as a shell along the stack).",
        table(["Torus", "Tori", "Stack length (m)", "Rigid J/I_t", f"Forward whirl / spin, {num(shell_cm)} cm wall",
               "Wall needed (cm)", "Wall from the hub's budget (cm)", "Forward whirl / spin at that wall"], lengths),
        "Not modelled: the hub's shear and joints, the elevator, pipe and power shafts, axial and torsional "
        "motion, the rim links' and ties' preload and details, and disturbances (docking, rim trains, ballast "
        "transfers, the array's bearing, sunlight pressure).",
    ]) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m dynamics_model", description=__doc__)
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    print(report(params(load(), **dict(args.set))), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
