"""The hub held in the chord nets by stabilising lines (notes §12, plan §2).

Each torus has two chord nets, one in each side plane of its tube (y = ±(a + t) from its
mid-plane, tube_section.py). In each, the chords pass the hub tangent to a circle c = 1.1 h
(h the hub radius), bowed outward by their own spin load, so a window of gap
l = c + bow - h opens around the hub. Short stabilising lines run from the hub's surface to
every chord's tangent point, preloaded so none goes slack.

- A chord pulled sideways at its middle resists like a taut string: k_c = 2 T beta cot(beta L),
  with beta^2 = mu w^2 / T for its own spin load (a slightly negative foundation); ~2 T / L.
- A line and its chord act in series; N lines evenly spread give K = N k / 2 in any direction
  of the net's plane (sum of cos^2); the two nets of a torus give twice that, and, ~2(a + t)
  apart, a tilt stiffness.
- The hub off the axis by x feels M w^2 x outward: a negative stiffness the lines must beat.
- Preloaded lines also resist motion they don't stretch (geometric stiffness P0 / l): along
  the axis and in torsion. That is weak; as an option, a share of the lines run from the hub's
  mid-plane out to the side nets, inclined at gamma (tan gamma = (a + t) / l), and hold the hub
  along the axis by k sin^2(gamma) each (a chord resists sideways pulls out of its plane alike).

Load cases, per torus (the hub's share of a long shared hub, rigid over one torus):
an imbalance carried on the hub, an unbalanced torus, and the orbit-raising thrust applied at
the hub tips (notes §15). The torus and its hub turn about their common centre of mass: two
bodies, two springs' worth of statics in the rotating frame.

While building, only the first arcs have chords. A single opposite pair's chords are nearly
parallel: the lines hold the hub across them, but along them only through their preload, which
must then beat the hub's own divergence and pulls those few chords well into the window. A
second pair at right angles holds that direction instead.

Not modelled: the hub as a beam between tori and the stack's modes (plan §4), the elevator,
pipe and power shafts and their compliant joints, docking loads (set by the dock's buffers),
and torque through the lines (radial lines carry it only by their preload).
"""

import math

from . import cable_net

HUB_IMBALANCE_FRAC = 0.01     # share of the hub's mass that may sit off-centre, at its rim (guess)
ARC_MISMATCH = 0.01           # mass mismatch between paired arcs while building (spinup, net_statics)
ORBIT_ACCEL = 1e-5            # m/s^2, orbit raising by thrusters at the hub tips (notes §15)
BUILD_SPIN = 0.71             # share of the final spin while the first pair is hung (net_statics)
TAUT_MARGIN = 1.5             # preload / largest swing of line tension in service
E_WIRE = 200e9
N_NETS = 2                    # chord nets per torus, one in each side plane of its tube
INCLINED_FRAC = 0.1           # share of lines run out of the nets' planes, from the hub's mid-plane (option)


def chord_stiffness(tension, half_length, line_mass, omega):
    """Sideways stiffness of a taut chord at its middle, under its own spin load (N/m)."""
    beta = math.sqrt(line_mass * omega ** 2 / tension)
    if beta * half_length < 1e-9:
        return 2 * tension / half_length
    return 2 * tension * beta / math.tan(beta * half_length)


def two_bodies(m_torus, m_hub, k, omega, f_torus, f_hub):
    """Offsets of a torus and its hub (rotating frame) under forces on each, joined by a spring k.

    m_t w^2 x_t + k (x_h - x_t) + f_t = 0 and m_h w^2 x_h + k (x_t - x_h) + f_h = 0.
    Returns the hub's offset relative to the torus and the spring force."""
    w2 = omega ** 2
    a11, a12, a21, a22 = m_torus * w2 - k, k, k, m_hub * w2 - k
    det = a11 * a22 - a12 * a21
    x_t = (-f_torus * a22 + a12 * f_hub) / det
    x_h = (-a11 * f_hub + a21 * f_torus) / det
    return {"x_torus": x_t, "x_hub": x_h, "relative": x_h - x_t, "force": k * (x_h - x_t)}


def compute(p, geo, mass, anchor_spacing=10.0, build_pairs=2):
    """The finished nets and the first arcs (build_pairs opposite pairs), for one torus and its share
    of the hub. The lines are sized for service and for that first stage."""
    r, h, omega = geo["radius"], geo["hub_radius"], geo["omega"]
    sigma, rho = p.wire_stress_mpa * 1e6, p.steel_density
    net = cable_net.compute(r, mass["rim"], omega, h, sigma, rho, anchor_spacing=anchor_spacing)
    n = net["n_chords"]                                  # per net: each net has an anchor every spacing
    tension = net["tension_mid_uniform"] / N_NETS       # each net holds half the rim
    mu = rho * net["wire_area_uniform"] / N_NETS
    gap = net["tangent_radius"] + net["bow"] - h
    k_chord = chord_stiffness(tension, net["half_length"], mu, omega)
    m_hub = p.hub_factory_metal_frac * mass["steel"]
    m_torus = mass["total"]
    w2 = omega ** 2
    plane_offset = geo["tube_radius"] + geo["jacket"]

    # Design forces on the hub (finished torus, full spin), per torus.
    arc_mass = mass["rim"] / (2 * math.pi * r) * 4 * net["theta"] * r
    cases = {
        "hub imbalance": (0.0, HUB_IMBALANCE_FRAC * m_hub * w2 * h),
        "torus imbalance": (ARC_MISMATCH * arc_mass * w2 * r, 0.0),
        "orbit thrust": (-m_torus * ORBIT_ACCEL, m_torus * ORBIT_ACCEL),
    }

    # Lines: sized for the largest swing of tension, preloaded so none goes slack. With stiff lines
    # the force splits as cos(psi) over N lines per net: the most loaded takes 2 F / (N n_nets).
    def plane_stiffness(k_line):
        k = 1 / (1 / k_chord + 1 / k_line)
        return n * k / 2, k

    k_line = math.inf
    for _ in range(3):        # line stiffness depends on its size, which depends (weakly) on the forces
        k_plane, k_series = plane_stiffness(k_line)
        k_torus = N_NETS * k_plane
        results = {name: two_bodies(m_torus, m_hub, k_torus, omega, ft, fh) for name, (ft, fh) in cases.items()}
        design = max(abs(res["force"]) for res in results.values())
        swing = 2 * design / (n * N_NETS)
        preload = TAUT_MARGIN * swing
        line_area = (preload + swing) / sigma
        k_line = E_WIRE * line_area / gap

    # Building: the first arcs (4 theta r each, at BUILD_SPIN), in one opposite pair or two pairs at
    # right angles. A pair's chords run between its two arcs, nearly parallel, so their tangent
    # points sit on two sides of the window: the lines hold the hub across the chords but along
    # them only by the arcs' spread (mean sin^2 of the chord directions, ~ alpha^2 / 3 for an arc's
    # half-angle alpha) and by their preload (P0 / l per line). A second pair at right angles holds
    # the first one's weak direction.
    arc = 4 * net["theta"] * r
    n_build = round((2 * arc - 4 * net["theta"] * r) / net["anchor_spacing"])  # chords between a pair's arcs
    spin2 = BUILD_SPIN ** 2
    k_chord_build = chord_stiffness(net["tension_mid_uniform"] * 2 * spin2 / N_NETS, net["half_length"], mu,
                                    omega * BUILD_SPIN)
    k_build = 1 / (1 / k_chord_build + 1 / k_line)
    spread = (arc / (2 * r)) ** 2 / 3
    hub_pull_build = m_hub * w2 * spin2
    build = {}
    for pairs in (1, 2):
        # Weakest direction: along one pair's chords (held by the other pair, if any).
        weak = N_NETS * n_build * k_build * (spread + (1 - spread) * (pairs - 1))
        needed = max(0.0, (TAUT_MARGIN * hub_pull_build - weak) * gap / (N_NETS * n_build * pairs))
        k_weak = weak + N_NETS * n_build * pairs * needed / gap
        mismatch = ARC_MISMATCH * arc_mass
        res = two_bodies(2 * pairs * arc_mass, m_hub, k_weak, omega * BUILD_SPIN, mismatch * w2 * spin2 * r, 0.0)
        build[pairs] = {
            "chords": n_build * pairs, "weak_unbraced": weak, "hub_pull": hub_pull_build,
            "stable_unbraced": weak > hub_pull_build, "margin_unbraced": weak / hub_pull_build,
            "preload": needed, "k_weak": k_weak, "offset": res["relative"], "force": res["force"],
            "pull_in": needed / k_chord_build,
        }

    first = build[build_pairs]
    line_area = max(line_area, (first["preload"] + 2 * abs(first["force"]) / (N_NETS * first["chords"])) / sigma)
    line_mass = N_NETS * n * line_area * gap * rho
    k_torus = N_NETS * plane_stiffness(E_WIRE * line_area / gap)[0]
    gamma = math.atan2(plane_offset, gap)
    k_axial_inclined = INCLINED_FRAC * N_NETS * n * plane_stiffness(E_WIRE * line_area / gap)[1] * math.sin(gamma) ** 2
    natural = math.sqrt(max(k_torus - m_hub * w2, 0) / m_hub)
    return {
        "net": net, "n_lines": N_NETS * n, "gap": gap, "tension": tension, "k_chord": k_chord,
        "k_chord_string": 2 * tension / net["half_length"],
        "k_plane": k_torus / N_NETS, "k_torus": k_torus, "hub_mass": m_hub, "torus_mass": m_torus,
        "hub_pull": m_hub * w2, "margin": k_torus / (m_hub * w2),
        "natural_vs_spin": natural / omega,
        "k_tilt": 2 * (k_torus / N_NETS) * plane_offset ** 2, "plane_offset": plane_offset,
        # Geometric stiffness of the preloaded lines, in service (the build preload is let off after closure).
        "k_axial": N_NETS * n * preload / gap,
        "k_torsion": N_NETS * n * preload * h * (h + gap) / gap,
        "k_axial_inclined": k_axial_inclined, "inclination": gamma,
        "axial_natural_vs_spin": math.sqrt(N_NETS * n * preload / gap / m_hub) / omega,
        "axial_inclined_natural_vs_spin": math.sqrt(k_axial_inclined / m_hub) / omega,
        "cases": results, "design_force": design,
        "service_preload": preload, "chord_pull_in": preload / k_chord,
        "line_area": line_area, "line_mass": line_mass,
        "build": build, "build_pairs": build_pairs,
    }
