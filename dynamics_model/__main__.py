"""Stack dynamics (plan §4): whirl modes of the flexible spinning stack and its passive stability.

python -m dynamics_model [--set name=value ...]
"""

import argparse
import math
import sys

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import axial_torsion as at
from . import disturbances as ds
from . import fatigue as fa
from . import joints as jt
from . import links as lk
from . import stack as st

CASES = ((900, 2), (900, 6), (1600, 2), (1600, 6))
RIM_LINK = 1e11            # N/m between neighbouring tori's rims, for the stack-length study
TIES = 1e-4                # share of the torus's mass in radial ties, for the stack-length study
DAMPING = 0.01             # dissipation turning with the stack, for the damped check
SPINUP = (0.1, 0.25, 0.5, 0.75, 1.0)   # shares of the spin rate, for the stack spun up from rest
HUNG_SHARES = (0.25, 0.5, 0.95)  # shares of a ring hung, for the stack's stability while a torus is built
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
    link_rows, lattice_rows, imposed_rows, dist_rows, slow_rows = links_and_disturbances(p)
    hub_rows, axial_rows, build_rows, fit_rows, fatigue_rows, hung_rows, spinup_rows = details(p)
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
        "## Rim links: what they must resist",
        "Lowest forward whirl over the spin with the links' tilt stiffness as taken above (k r²/2), with none, "
        "and with a lattice's (below), at the design stiffness and with the trace of ties. Only the links' "
        "sideways stiffness matters: they need not be stiff along the axis. And since sideways motion of two "
        "rims is radial at some angles and tangential at others, links stiff only tangentially, spread evenly "
        "around the rim (any three or more), give the same sideways stiffness in every direction: they can be "
        "compliant radially, free of the rims' differential growth (`dynamics_model/links.py`).",
        table(["Torus", "Tori", "Design stiffness (N/m)", "Tilt k r²/2", "No tilt stiffness", "Lattice's tilt"],
              link_rows),
        "## The lattice",
        f"A ring of X-braced bays across each gap at the envelopes' closest approach (r − a), diagonals at 45°, "
        f"pinned tubular struts (D/t {num(lk.STRUT_D_OVER_T)}, no preload: struts, not cables, which would pull "
        "the tori together along the axis, where only the nets hold them). Stiff in shear and along the axis in "
        "its own surface, compliant radially (the struts bend out of it). Design stiffness: "
        f"{lk.KNEE:.0%} of the margin rigid links would give (stiffer buys almost nothing; the nets and the hub's "
        f"bending set the rest), with {TIES:.2%} ties. Struts sized for that stiffness, and for the largest link "
        f"force below (the ballast tanks' whole capacity untrimmed) at a safety factor of {num(lk.SAFETY)} on "
        f"buckling and on {num(lk.YIELD / 1e6)} MPa yield, at least {num(lk.MIN_AREA * 1e4)} cm².",
        table(["Torus", "Tori", "Bays", "Strut (cm², diameter)", "Set by", "Mass per gap (t)",
               "Share of a torus", "Gap blocked", "Forward whirl / spin", "Ties needed for 1.2"], lattice_rows),
        "**Imposed motions** between neighbours. Along the axis the lattice is far stiffer than the nets "
        "(`structure_model/hub.py`, inclined lines included), so the tori follow the lattice and the nets take "
        "the difference.",
        table(["Torus", "Hub 20 K warmer over a pitch", "One rim 4 K warmer", "Struts 100 K colder"], imposed_rows),
        "## Disturbances",
        f"The stack with the lattice and ties above (`dynamics_model/disturbances.py`). Rim train: one "
        f"{num(ds.TRAIN_MASS / 1e3)} t train antispinward in the first torus, a load whirling at ω − v/R, below "
        "the spin, where a passively stable stack has no forward modes. Imbalance: the ballast tanks' whole "
        f"capacity untrimmed ({p.ballast_frac:.2%} of the rim's mass at the first torus's rim), fixed in the "
        f"rotating frame. Docking: a {num(ds.SHIP_MASS / 1e6)} kt ship missing by {num(ds.SHIP_MISS)} m/s "
        f"sideways at the dock, followed for 40 turns with {DAMPING:.0%} damping. Link force: the sideways force "
        "across one gap; torus: the largest torus's motion off the stack's axis.",
        table(["Torus", "Tori", "Train at 20 m/s: link force", "Train: torus moves",
               "Imbalance: link force", "Imbalance: torus moves", "Imbalance: dock moves",
               "Docking: link force (peak)", "Docking: axis turned", "Docking: decay (×1/e)"], dist_rows),
        "**Slow torques.** Sunlight on the despun array (pushed ×"
        f"{num(ds.ARRAY_PUSH)} its absorbed value, the mast {num(ds.MAST)} m beyond the stack) and on the rims "
        "edge-on, about the centre of mass: it turns the axis sideways at τ/H, but the torque turns with the Sun "
        "and falls as 1/d², so by Kepler's second law it sums to zero over every orbit, eccentric or not: the "
        "axis only wobbles (at 1 AU, and on Eros's orbit, a = 1.458 AU, e = 0.223). The despun array's bearing "
        f"(friction Q = {num(ds.BEARING_FRICTION / 1e3)} kN·m, a guess): its friction and the drive holding the "
        "array facing the Sun both act between array and hub, and the drive must cancel the friction on the "
        "array, so its reaction cancels the friction on the hub. Compensated, the stack keeps its spin and the "
        "friction only costs the drive's power, Qω, as heat. Uncompensated (drive off, or the bearing seized), "
        "friction drags the array up to the spin, and the stack gives up the array's share of the spin once.",
        table(["Torus", "Tori", "Sunlight torque (N·m)", "Axis drift (°/yr, if it didn't turn)",
               "Yearly wobble at 1 AU (°)", "On Eros's orbit (°)", "Drive power against the friction (kW)",
               "Drive off: array at the spin in (h)", "Spin given up then"], slow_rows),
        "**Damping.** Every forward mode beats the spin, so no amount of dissipation turning with the stack "
        "destabilises it; it only sets how fast a disturbance dies out (×1/e in hours to days at 1%, ten times longer "
        "at 0.1%). Nothing has to be added for it.",
        "## The hub: shear and joints",
        "The hub is a short, wide tube (radius ~60 m), so its shear flexibility counts: every result above "
        "includes it (Timoshenko, κ = 0.5). It is built in segments, one per torus or farm ring, joined at the "
        "gaps; each joint a rotational spring (`dynamics_model/joints.py`). Needed: the stiffness keeping "
        f"{jt.KNEE:.0%} of a continuous hub's margin, against one pitch of the hub's own wall (EI over the pitch) "
        f"and a bolted flange ring (M36 bolts every {num(jt.BOLT_SPACING * 100)} cm, {num(jt.BOLT_GRIP * 100)} cm "
        "grip), whose bolts' preload must keep it closed under the hub's largest moment (the ballast tanks' "
        "whole capacity untrimmed).",
        table(["Torus", "Tori", "Margin, no shear", "With shear", "Joint needed (N·m/rad)",
               "One pitch of hub (EI/p)", "Bolted flange", "Margin with flanges", "Flange: preload / load"],
              hub_rows),
        "## Along and about the axis",
        "Axial and torsional motion (`dynamics_model/axial_torsion.py`) don't couple to the spin, so "
        "dissipation can't destabilise them, but a once-per-turn load (the despun array's bearing running "
        "slightly off true is the one interface turning against the stack) would pump any mode near the spin. "
        f"Requirement: no mode between 1/{num(at.BAND)} and {num(at.BAND)}× the spin; modes well below or above "
        "are left alone. As built, two sit in that band. The farm rings bounce along the axis at ~1.04–1.09× the "
        "spin: their radial spokes hold them along it only by their tension, giving ~ω√(r_f/L) whatever the "
        "ring's size or mass (the tori had the same weakness in their nets, fixed with inclined lines, plan §2, "
        "and are now also tied by the lattice). And the hub twists between the tori's nets and the farm spokes at "
        "~1.05–1.3×. Fixes, the least that clears the band: a share of each farm ring's spokes crossed between "
        "its two planes (from the front plane at the hub to the back plane at the ring, alternately, like a "
        "bicycle wheel's; still radial seen along the axis), and a small share of the tori's stabilising lines "
        f"laced tangentially at {num(math.degrees(at.NET_LACING_ANGLE))}°. The slower twists (the farm rings on "
        "their spokes, ~0.45×, and the farm section with the hub against the tori, ~0.2–0.35×) stay well below "
        f"the spin. Loads on the fixed stack: a {num(ds.SHIP_MASS / 1e6)} kt ship closing at 0.1 m/s, taken out "
        f"over {num(at.BUFFER)} s by the dock's buffers; a 50 t rim train braking at 0.1 g.",
        table(["Torus", "Tori", "Axial near the spin, as built", "Torsion near the spin, as built",
               "Farm spokes crossed", "Lines laced", "Extra steel (t per stack)", "Axial: lowest above the band",
               "Torsion: lowest above the band", "Torsion below the band", "Docking: largest force",
               "Braking: torque on a lattice"], axial_rows),
        "## Building and losing a lattice",
        "The stack's margin with one gap unlinked: a torus just closed next to the stack, or a lattice lost. "
        "The share of a gap's bays (spread evenly) that restores 1.2.",
        table(["Torus", "Tori", "All linked", "End gap unlinked", "Worst gap unlinked", "Grows ×e (1% damping)",
               "Bays needed in that gap"], build_rows),
        "**Built at rest, spun up together** (the baseline for a child): the finished, linked stack at each "
        "share of its final spin rate. The nets' and farm spokes' centring goes with the spin load, so its ratio "
        "to the centrifugal pull holds; the hub, lattice and ties are elastic, relatively stiffer at low spin, "
        "so the margin only falls as the stack spins up: full spin, checked above, is the worst case for whirl. "
        "Whirl only, at selected rates, the nets' stiffness scaled with the spin load (their pretension at rest "
        "left out, which only adds to it); the ring's own statics through the spin-up, its torque and the fill's "
        "settling are in `reports/structure.md`.",
        table(["Torus", "Tori"] + [f"{f:.0%} of the spin" for f in SPINUP], spinup_rows),
        "**While a torus is hung** at the end of a spinning stack (the option for growing a living stack) (the stack keeps its spin), that torus a "
        "partial ring in two opposite pairs of arcs at right angles, held on the hub by its nets (in proportion "
        "to its chords) and by the temporary radial lines to its arcs' single-laced anchors "
        "(`structure_model/sequence.py`), and linked to its neighbour by the lattice's bays alongside its arcs "
        "(in proportion), or not. Lowest forward whirl over the spin:",
        table(["Torus", "Tori", "Share of the ring hung", "Unlinked, no radial lines", "Unlinked, radial lines",
               "Linked as hung, no radial lines", "Linked as hung, radial lines"], hung_rows),
        "## Fittings and tunnels",
        "Each strut meets the torus at a fitting on the envelope, carried to the hull through the jacket and "
        "crawl space by a shear web in the bay's tangential-axial plane (a jacket bulkhead in that plane: at "
        "the tube's side, where the gap is, the jacket's depth runs along the axis), as wide as the jacket is "
        "deep, loaded in its own plane both tangentially and axially, its weak direction radial: sized with the lattice for stiffness (the "
        "struts take half the bay's compliance, the two fittings the rest) and strength (safety factor 2), and "
        "in series with the struts in every result above. A post bending as a cantilever through the jacket "
        "would be far too soft: sized for strength alone, its compliance would cut a 900 m six-stack's margin "
        f"below 1. A tunnel ({num(jt.TUNNEL_RADIUS)} m radius) crosses each gap on an expansion joint taking "
        "the rims' relative motions (the imposed motions above and the lattice's own give under the largest "
        f"load), holding its pressure thrust inside itself (pressure-balanced), with at most {jt.ANISOTROPY:.0%} "
        "of the lattice's sideways stiffness (more would make the stiffness differ by direction). Without a "
        "joint, a tube fixed at both rims (3 cm wall) has ~7–20% of the lattice's stiffness, at one angle, and is bent by a "
        "rim's growth.",
        table(["Torus", "Tori", "Fitting webs (thickness, mass per gap, their sideways stiffness)", "Joint: radial", "Axial", "Tangential",
               "Pressure thrust", "Joint's sideways stiffness at most", "Rigid tube: stiffness, stress"], fit_rows),
        "## Fatigue",
        f"Load cycles over {num(fa.LIFE)} years (`dynamics_model/fatigue.py`): rim trains (one cycle per lap, "
        f"{fa.TRAIN_SERVICE:.0%} of the time at 20 m/s), ballast trims ({fa.BALLAST_DAILY:.0%} of the tanks' "
        "capacity daily), a docking a day, the rims' daily temperature difference (4 K), sunlight on the struts "
        "each turn. Stress ranges ×1.35 against EN 1993-1-9's cut-off (detail 71 MPa for the struts' and the "
        "hub's welds, 160 MPa for strand): below it, no damage.",
        table(["Torus", "Tori", "Part", "Largest range ×1.35 (MPa)", "Cut-off (MPa)", "Damage (Miner)"],
              fatigue_rows),
        "Not modelled: the elevator, pipe and power shafts, the fittings' local details in the jacket, the "
        "bellows' own design.",
    ]) + "\n"


def details(p):
    from structure_model import hub as hub_model
    hub_rows, axial_rows, build_rows, fit_rows, fatigue_rows, hung_rows, spinup_rows = [], [], [], [], [], [], []
    for r, n in CASES:
        d = Design(radius_m=r, n_tori=n)
        label = [size_label(r), str(n)]
        k, _ = lk.design_stiffness(p, d, tie_frac=TIES)
        lat, s, info, unbalanced = lk.converged(p, d, k, tie_frac=TIES)
        geo = info["geometry"]
        no_shear = st.build(p, d, rim_link=lat["k_lat"], link_tilt=lat["tilt"], tie_frac=TIES,
                            shear=False)[0].forward_ratio()
        j = jt.hub_joint(p, d, k, tie_frac=TIES)
        hub_rows.append(label + [num(no_shear, 3), num(j["continuous"], 3), f"{j['needed']:.1e}",
                                 f"{j['per_pitch']:.1e}", f"{j['flange']:.1e}", num(j["flange_ratio"], 3),
                                 f"{num(j['opening_margin'])}×"])
        a = at.study(p, d, k, tie_frac=TIES)
        axial_rows.append(label + [
            "–".join(num(x, 3) for x in (min(a["axial_bare_near"]), max(a["axial_bare_near"])))
            if a["axial_bare_near"] else "none",
            ", ".join(num(x, 3) for x in a["torsion_bare_near"]) or "none",
            f"{a['farm_crossed']:.0%}", f"{a['nets_laced']:.2%}",
            num((a["farm_extra_mass"] + a["nets_extra_mass"]) * n / 1e3, 2),
            num(a["axial_above"], 3), num(a["torsion_above"], 3),
            ", ".join(num(x, 2) for x in a["torsion_below"]),
            f"{num(a['dock_largest'] / 1e6, 2)} MN", f"{num(a['brake_link_torque'] / 1e6, 2)} MN·m"])
        c = lk.construction(p, d, k, tie_frac=TIES)
        build_rows.append(label + [num(c["full"], 3), num(c["end_gap"], 3),
                                   f"{num(c['worst'], 3)} (gap {c['worst_gap'] + 1})",
                                   f"{num(c['e_folding_hours'], 2)} h" if c["e_folding_hours"] else "—",
                                   f"{c['bays']} of {lat['bays']} ({c['share']:.1%})" if c["share"] else "—"])
        spun = lk.spinup(p, d, SPINUP, tie_frac=TIES, k_design=k)
        spinup_rows.append(label + [num(spun[f], 3) for f in SPINUP])
        if n == 6 or r == 900:
            for share in HUNG_SHARES:
                cells = [num(lk.building_torus(p, d, share, link=link, radial_lines=rad, tie_frac=TIES,
                                               k_design=k)[0], 3)
                         for link in (False, True) for rad in (False, True)]
                hung_rows.append(label + [f"{share:.0%}"] + cells)
        fit = jt.fittings(lat)
        im = lk.imposed(p, geo, hub_model.compute(p, geo, info["mass"]))
        tun = jt.tunnel(geo, lat, im, unbalanced["link"])
        fit_rows.append(label + [
            f"{num(fit['thickness'] * 1000, 2)} mm ({fit['set_by']}), {num(fit['per_gap'] / 1e3, 2)} t, "
            f"{fit['k_lat']:.1e} N/m",
            f"±{num(tun['radial'] * 100, 2)} cm", f"±{num(tun['axial'] * 100, 2)} cm",
            f"±{num(tun['tangential'] * 1000, 2)} mm", f"{num(tun['thrust'] / 1e6, 2)} MN",
            f"{tun['max_lateral_k']:.1e} N/m",
            f"{tun['rigid_k']:.1e} N/m, {num(tun['rigid_stress'] / 1e6, 2)} MPa"])
        if n == 6:
            f = fa.study(p, d, k, tie_frac=TIES)
            for part in fa.DETAIL:
                fatigue_rows.append(label + [part, num(f["largest"][part] / 1e6, 2), num(f["cutoff"][part] / 1e6, 2),
                                             num(f["damage"][part], 2)])
    return hub_rows, axial_rows, build_rows, fit_rows, fatigue_rows, hung_rows, spinup_rows


def links_and_disturbances(p):
    from structure_model import hub as hub_model
    link_rows, lattice_rows, imposed_rows, dist_rows, slow_rows = [], [], [], [], []
    for r, n in CASES:
        d = Design(radius_m=r, n_tori=n)
        k, _ = lk.design_stiffness(p, d, tie_frac=TIES)
        s, info = st.build(p, d, rim_link=k, tie_frac=TIES)
        geo, mass = info["geometry"], info["mass"]
        res = evaluate(p, d)
        label = [size_label(r), str(n)]
        tilt = lk.compare_tilt(p, d, k, tie_frac=TIES)
        link_rows.append(label + [f"{k:.1e}", num(tilt["default"], 3), num(tilt["none"], 3), num(tilt["lattice"], 3)])
        # The finished lattice: struts sized for the force its own stack takes, iterated to agree; the
        # disturbances below run on it.
        lat, s_lat, info_lat, unbalanced = lk.converged(p, d, k, tie_frac=TIES)
        bare = st.build(p, d, rim_link=lat["k_lat"], link_tilt=lat["tilt"])[0].forward_ratio()
        ties = None if bare >= TARGET else st.required(p, d, "tie_frac", target=TARGET, low=1e-7, high=0.1,
                                                         rim_link=lat["k_lat"], link_tilt=lat["tilt"])
        lattice_rows.append(label + [
            num(lat["bays"]), f"{num(lat['area'] * 1e4, 2)} ({num(lat['diameter'] * 100, 2)} cm)", lat["set_by"],
            num(lat["mass"] / 1e3, 2), f"{lat['mass'] / mass['total']:.3%}", f"{lat['blocked']:.1%}",
            num(s_lat.forward_ratio(), 3),
            "none" if ties is None else f"{ties:.3%} ({num(ties * mass['total'] / 1e3, 2)} t)"])
        if n == 6:
            im = lk.imposed(p, geo, hub_model.compute(p, geo, mass))
            imposed_rows.append([size_label(r),
                                 f"{num(im['axial_mismatch'] * 100, 2)} cm, {num(im['axial_force'] / 1e6, 2)} MN",
                                 f"{num(im['radial'] * 100, 2)} cm, hoop {num(im['hoop_stress'] / 1e6, 2)} MPa",
                                 f"gap closes {num(im['closing'] * 100, 2)} cm, {num(im['closing_force'] / 1e6, 2)} MN"])
        train = ds.rim_train(s_lat, geo, speed=20.0)
        dock = ds.docking(s_lat)
        dist_rows.append(label + [
            f"{num(train['link'] / 1e6, 2)} MN", f"{num(train['torus'] * 1000, 2)} mm",
            f"{num(unbalanced['link'] / 1e6, 2)} MN", f"{num(unbalanced['torus'] * 100, 2)} cm",
            f"{num(unbalanced['dock_offset'] * 100, 2)} cm",
            f"{num(dock['link'] / 1e6, 2)} MN", f"{num(math.degrees(dock['axis_turn']), 2)}°",
            f"{num(dock['decay_hours'], 2)} h" if dock["decay_hours"] else "—"])
        array = res["power"]["array_site"] * n
        sun = ds.sunlight(s_lat, geo, array, n)
        eros = ds.sunlight(s_lat, geo, array, n, a_au=1.458, e=0.2227)
        brg = ds.bearing(s_lat, info_lat["array_mass"], array)
        slow_rows.append(label + [num(sun["torque"], 2), num(math.degrees(sun["rate"] * ds.YEAR), 2),
                                  num(math.degrees(sun["wobble"]), 2), num(math.degrees(eros["wobble"]), 2),
                                  num(brg["power"] / 1e3, 2), num(brg["spin_up_hours"], 2),
                                  f"{brg['spin_share']:.1e}"])
    return link_rows, lattice_rows, imposed_rows, dist_rows, slow_rows


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m dynamics_model", description=__doc__)
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    print(report(params(load(), **dict(args.set))), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
