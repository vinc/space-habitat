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
- The hub off the axis by x feels M w^2 x outward. A torus and its hub move relative to each
  other with their reduced mass mu; in the rotating frame Coriolis couples the two directions of
  the window's plane, so the relative motion has two modes at |sqrt(K / mu) -/+ w| (sqrt(K / mu)
  in the inertial frame). Static loads fixed in the rotating frame need K > mu w^2.
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
second pair at right angles holds that direction instead. The preload is set both by that
stiffness and by the tension swing under a mismatch between the arcs, so no line goes slack, and
the lines are sized for it; the stiffness differs by direction, so the modes are checked for
growth (an asymmetric rotor).

Not modelled: the hub as a beam between tori and the stack's modes (plan §4), the elevator,
pipe and power shafts and their compliant joints, docking loads (set by the dock's buffers),
and torque through the lines (radial lines carry it only by their preload).
"""

import math

import numpy as np

from . import cable_net

HUB_IMBALANCE_FRAC = 0.01     # share of the hub's mass that may sit off-centre, at its rim (guess)
ARC_MISMATCH = 0.01           # mass mismatch between paired arcs while building (spinup, net_statics)
ORBIT_ACCEL = 1e-5            # m/s^2, orbit raising by thrusters at the hub tips (notes §15)
BUILD_SPIN = 0.71             # share of the final spin while the first pair is hung (net_statics)
TAUT_MARGIN = 1.5             # preload / largest swing of line tension (in service and while building)
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


def series(k_a, k_b):
    return 1 / (1 / k_a + 1 / k_b)


def modes(mu, k_x, k_y, omega):
    """Relative motion of a torus and its hub in the rotating frame, reduced mass mu:
    mu (q'' + 2 w x q' - w^2 q) + diag(k_x, k_y) q = 0 (Coriolis and centrifugal terms).

    Returns the rotating-frame frequencies of its two modes (rad/s, ascending) and the largest
    growth rate (0 when stable). For k_x = k_y = k they are |sqrt(k / mu) -/+ w|; with unequal
    stiffness the motion can grow between the two directions' frequencies (an asymmetric rotor)."""
    w = omega
    a = np.zeros((4, 4))
    a[0, 2] = a[1, 3] = 1.0
    a[2, 0], a[3, 1] = w * w - k_x / mu, w * w - k_y / mu
    a[2, 3], a[3, 2] = 2 * w, -2 * w
    lam = np.linalg.eigvals(a)
    growth = float(max(0.0, lam.real.max()))
    freqs = sorted({round(abs(x.imag), 12) for x in lam})
    return {"frequencies": freqs, "growth": growth if growth > 1e-9 * max(abs(lam)) else 0.0}


def compute(p, geo, mass, anchor_spacing=10.0, build_pairs=2):
    """The finished nets and the first arcs (build_pairs opposite pairs), for one torus and its share
    of the hub. The lines' area, preloads, stiffnesses and load cases are iterated together until
    they agree: every line taut and within the wire stress in service and while building."""
    r, h, omega = geo["radius"], geo["hub_radius"], geo["omega"]
    sigma, rho = p.wire_stress_mpa * 1e6, p.steel_density
    net = cable_net.compute(r, mass["rim"], omega, h, sigma, rho, anchor_spacing=anchor_spacing)
    n = net["n_chords"]                                  # per net: each net has an anchor every spacing
    tension = net["tension_mid_uniform"] / N_NETS       # each net holds half the rim
    mu_chord = rho * net["wire_area_uniform"] / N_NETS
    gap = net["tangent_radius"] + net["bow"] - h
    k_chord = chord_stiffness(tension, net["half_length"], mu_chord, omega)
    m_hub = p.hub_factory_metal_frac * mass["steel"]
    m_torus = mass["total"]
    mu = m_torus * m_hub / (m_torus + m_hub)
    w2 = omega ** 2
    plane_offset = geo["tube_radius"] + geo["jacket"]

    arc = 4 * net["theta"] * r                          # the shortest arcs (net_statics)
    arc_mass = mass["rim"] / (2 * math.pi * r) * arc
    cases_in = {
        "hub imbalance": (0.0, HUB_IMBALANCE_FRAC * m_hub * w2 * h),
        "torus imbalance": (ARC_MISMATCH * arc_mass * w2 * r, 0.0),
        "orbit thrust": (-m_torus * ORBIT_ACCEL, m_torus * ORBIT_ACCEL),
    }
    n_build = round((2 * arc - 4 * net["theta"] * r) / net["anchor_spacing"])  # chords between a pair's arcs
    w_build = omega * BUILD_SPIN
    k_chord_build = chord_stiffness(net["tension_mid_uniform"] * 2 * BUILD_SPIN ** 2 / N_NETS,
                                    net["half_length"], mu_chord, w_build)
    alpha = arc / (2 * r)                              # half-angle of an arc: spread of a pair's chords
    spread = alpha ** 2 / 3                             # mean sin^2 of their directions

    def service(area):
        k_line = E_WIRE * area / gap
        k_torus = N_NETS * n * series(k_chord, k_line) / 2
        cases = {name: two_bodies(m_torus, m_hub, k_torus, omega, ft, fh) for name, (ft, fh) in cases_in.items()}
        # Lines evenly spread: the most loaded swings by k delta = 2 F / (N n_nets).
        swing = max(2 * abs(c["force"]) / (N_NETS * n) for c in cases.values())
        preload = TAUT_MARGIN * swing
        return {"k_line": k_line, "k_torus": k_torus, "cases": cases, "swing": swing, "preload": preload,
                "area": (preload + swing) / sigma}

    def building(pairs, area):
        """The first stage: its weak direction runs along one pair's chords. There, a second pair's
        lines resist elastically (and those of the first pair by their spread); the first pair's
        lines, across the motion, add their preload's geometric stiffness. Preload: enough for the
        stiffness margin over the pair's and hub's reduced mass, and to keep every line taut."""
        k_s = series(k_chord_build, E_WIRE * area / gap)
        mu_b = 2 * pairs * arc_mass * m_hub / (2 * pairs * arc_mass + m_hub)
        elastic = N_NETS * n_build * k_s * (spread + (pairs - 1) * (1 - spread))
        cos_max = 1.0 if pairs > 1 else math.sin(alpha)  # the most stretched line's share of the motion
        perpendicular = N_NETS * n_build                 # the first pair's lines, across the weak direction
        across = N_NETS * n_build * k_s * (1 - spread) + (pairs - 1) * N_NETS * n_build * k_s * spread
        mismatch = ARC_MISMATCH * arc_mass * w_build ** 2 * r
        preload = 0.0
        for _ in range(200):
            k_weak = elastic + perpendicular * preload / gap
            res = two_bodies(2 * pairs * arc_mass, m_hub, k_weak, w_build, mismatch, 0.0)
            swing = k_s * abs(res["relative"]) * cos_max
            stiff_need = max(0.0, (TAUT_MARGIN * mu_b * w_build ** 2 - elastic) * gap / perpendicular)
            new = max(stiff_need, TAUT_MARGIN * swing)
            if abs(new - preload) <= 1e-9 * max(new, 1.0):
                break
            preload = new
        k_across = across + (pairs - 1) * perpendicular * preload / gap
        mode = modes(mu_b, k_weak, k_across, w_build)
        bare = modes(mu_b, elastic, across, w_build)       # the same lines without preload
        return {
            "chords": n_build * pairs, "weak_unbraced": elastic, "hub_pull": mu_b * w_build ** 2,
            "stable_unbraced": elastic > mu_b * w_build ** 2, "margin_unbraced": elastic / (mu_b * w_build ** 2),
            "preload": preload, "swing": swing, "k_weak": k_weak, "k_across": k_across,
            "offset": res["relative"], "force": res["force"], "pull_in": preload / k_chord_build,
            "growth": mode["growth"], "frequencies": mode["frequencies"], "growth_unbraced": bare["growth"],
            "e_folding_unbraced_spins": (w_build / (2 * math.pi * bare["growth"])) if bare["growth"] else None,
            "line_stress": (preload + swing) / area, "slack_margin": preload - swing,
            "area": (preload + swing) / sigma,
        }

    # Line area: iterate service and the chosen first stage until they agree.
    area = 1e-6
    for _ in range(200):
        svc = service(area)
        first = building(build_pairs, area)
        new = max(svc["area"], first["area"])
        if abs(new - area) <= 1e-9 * new:
            area = new
            break
        area = new
    svc = service(area)
    build = {pairs: building(pairs, area) for pairs in (1, 2)}
    k_torus = svc["k_torus"]
    natural = math.sqrt(k_torus / mu)
    mode = modes(mu, k_torus, k_torus, omega)

    # Along the axis and in torsion, radial lines resist by their preload only (geometric stiffness).
    k_axial = N_NETS * n * svc["preload"] / gap
    # Option: a share of the lines run from the hub's mid-plane to the side nets, length
    # hypot(gap, plane offset), inclined at gamma; each holds the hub along the axis by k sin^2(gamma).
    inclined = math.hypot(gap, plane_offset)
    gamma = math.atan2(plane_offset, gap)
    k_inclined = series(k_chord, E_WIRE * area / inclined)
    k_axial_inclined = INCLINED_FRAC * N_NETS * n * k_inclined * math.sin(gamma) ** 2
    line_mass = N_NETS * n * area * gap * rho
    return {
        "net": net, "n_lines": N_NETS * n, "gap": gap, "tension": tension, "k_chord": k_chord,
        "k_chord_string": 2 * tension / net["half_length"],
        "k_line": svc["k_line"], "k_plane": k_torus / N_NETS, "k_torus": k_torus,
        "hub_mass": m_hub, "torus_mass": m_torus, "reduced_mass": mu,
        "hub_pull": mu * w2, "margin": k_torus / (mu * w2),
        # Inertial frame: sqrt(k / mu); rotating frame (Coriolis): |sqrt(k / mu) -/+ w|.
        "natural_vs_spin": natural / omega,
        "rotating_vs_spin": [f / omega for f in mode["frequencies"]], "growth": mode["growth"],
        "k_tilt": 2 * (k_torus / N_NETS) * plane_offset ** 2, "plane_offset": plane_offset,
        "k_axial": k_axial,
        "k_torsion": N_NETS * n * svc["preload"] * h * (h + gap) / gap,
        "k_axial_inclined": k_axial_inclined, "inclination": gamma, "inclined_length": inclined,
        "inclined_extra_mass": INCLINED_FRAC * N_NETS * n * area * (inclined - gap) * rho,
        # Along the axis there is no centrifugal or Coriolis term.
        "axial_natural_vs_spin": math.sqrt(k_axial / mu) / omega,
        "axial_inclined_natural_vs_spin": math.sqrt((k_axial + k_axial_inclined) / mu) / omega,
        "cases": svc["cases"], "design_force": max(abs(c["force"]) for c in svc["cases"].values()),
        "service_swing": svc["swing"], "service_preload": svc["preload"],
        "chord_pull_in": svc["preload"] / k_chord,
        "line_area": area, "line_mass": line_mass,
        "build": build, "build_pairs": build_pairs,
    }
