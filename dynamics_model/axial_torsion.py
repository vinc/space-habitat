"""Axial and torsional motion of the stack (plan §4).

Along the axis and about it, nothing couples to the spin to first order (no gyroscopic or
centrifugal terms for a ring sliding along or turning about its own axis), so these motions can't
be destabilised by dissipation; what matters is how stiff they are, how they ring after a load,
and whether any load excites them at their own frequency.

- Along the axis: the hub as a bar (E A, A = 2 pi h t), each torus on its nets (preloaded radial
  lines and the ~10% inclined ones, structure_model.hub), neighbouring tori tied by the rim
  lattice's axial stiffness (links.py), each farm ring on its two planes of radial spokes (a plane
  of taut strings resists a pull out of it by its tension: T / L), the despun array a mass at the
  far end.
- About the axis: the hub as a tube in torsion (G J, J = 2 pi h^3 t), each torus on its nets
  (preload only, structure_model.hub), neighbouring tori tied by the lattice's tangential
  stiffness, each farm ring on its spokes (geometric: T h r_f / L), the despun array free (its
  bearing).

Loads: a ship's axial impulse at the dock; a rim train braking (its tangential force at the rim,
on one torus). Modes from K v = w_n^2 M v, the rigid motions (sliding, turning together) removed.

Requirement: no mode near the spin, within a factor BAND of it either way, where once-per-turn
loads (the despun array's bearing running slightly off true, the one interface turning against
the stack) would pump it. Modes well below or above are left alone.
- The farm rings bounce along the axis at ~w sqrt(r_f / L) (their spokes' tension, whatever their
  size), just above the spin: a share of their spokes crossed between the two planes (front plane
  at the hub to back plane at the ring, alternately, like a bicycle wheel's) lifts it.
- The hub twists between the tori's nets and the farm spokes at ~1.05-1.3x the spin: a small share
  of the tori's stabilising lines laced tangentially lifts it. The farm rings' own twist on their
  spokes (~w sqrt(h / L), ~0.45x) and the farm section with the hub against the tori (~0.2-0.44x)
  stay well below the spin.
"""

import math

import numpy as np

from . import links as lk
from . import stack as st

TRAIN_BRAKE = 0.1 * 9.81       # m/s^2, a rim train's braking (notes §12)
STEEL_DENSITY = 7850.0
BUFFER = 10.0                  # s, a ship's docking impulse spread by the dock's buffers (guess)


def farm_spokes(geo, mass, laced=0.0):
    """A farm ring's spokes, per plane: their total tension, and the stiffness along and about the
    axis. Radial spokes resist both only by their tension (geometric: T / L, and T h r_f / L);
    a share `laced` of them crossed between the planes, each running from one plane's hub end to
    the other plane's rim end (inclined gamma along the axis, still radial seen along it), adds
    E A / L sin^2 gamma along the axis and nothing about it."""
    h, rf = geo["hub_radius"], geo["farm_radius"]
    length = rf - h
    tension = (mass["farm_total"] - mass["farm_spokes"]) * geo["omega"] ** 2 * rf / 2
    area = mass["farm_spokes"] / (STEEL_DENSITY * length) / 2
    ea_l = st.E * area / length
    sin_g2 = geo["farm_width"] ** 2 / (geo["farm_width"] ** 2 + length ** 2)
    return {"tension": tension, "axial": tension / length + laced * ea_l * sin_g2,
            "torsion": tension * h * rf / length}


NET_LACING_ANGLE = math.radians(45)   # stabilising lines laced tangentially, from the radial


def net_lacing(nets, h, share):
    """Torsional stiffness (N m/rad) and mass (kg) of a share of a torus's stabilising lines laced
    tangentially at NET_LACING_ANGLE, each pulling its chord along its length at the tangent point
    (stiff there, taken as rigid): share N (E A / L) sin^2 h^2, L = gap / cos."""
    length = nets["gap"] / math.cos(NET_LACING_ANGLE)
    k = share * nets["n_lines"] * st.E * nets["line_area"] / length * math.sin(NET_LACING_ANGLE) ** 2 * h * h
    mass = share * nets["n_lines"] * nets["line_area"] * (length - nets["gap"]) * STEEL_DENSITY
    return k, mass


def _chain(s, info, kind, lattice, laced=0.0, nets_laced=0.0):
    """Mass (or inertia) and stiffness matrices along the axis ('axial') or about it ('torsion')."""
    p_nodes = s.hub_nodes
    n_hub = len(p_nodes)
    bodies = s.bodies
    size = n_hub + len(bodies)
    m = np.zeros(size)
    k = np.zeros((size, size))
    geo, mass, nets = info["geometry"], info["mass"], info["nets"]
    h, t = geo["hub_radius"], info["hub_shell_m"]
    if kind == "axial":
        m[:n_hub] = s.hub_mass
        for node, extra in s.point_masses.items():
            m[node] += extra
        bar = st.E * 2 * math.pi * h * t
    else:
        m[:n_hub] = s.hub_polar
        bar = st.G * 2 * math.pi * h ** 3 * t
    for e in range(n_hub - 1):
        ke = bar / (p_nodes[e + 1] - p_nodes[e])
        k[np.ix_([e, e + 1], [e, e + 1])] += ke * np.array([[1, -1], [-1, 1]])

    def spring(i, j, stiffness):
        k[np.ix_([i, j], [i, j])] += stiffness * np.array([[1, -1], [-1, 1]])

    spokes = farm_spokes(geo, mass, laced)
    for b, body in enumerate(bodies):
        i = n_hub + b
        m[i] = body.mass if kind == "axial" else body.polar
        torus = body.name.startswith("torus")
        for z, _ in body.springs:
            node = int(np.argmin(np.abs(p_nodes - z)))
            if torus:
                per_plane = ((nets["k_axial"] + nets["k_axial_inclined"]) if kind == "axial"
                             else nets["k_torsion"] + net_lacing(nets, h, nets_laced)[0])
                spring(node, i, per_plane / len(body.springs))
            else:
                spring(node, i, spokes[kind])
    for a, b, _, _ in s.links:
        spring(n_hub + a, n_hub + b, lattice["k_axial"] if kind == "axial" else lattice["k_torsion"])
    return m, k


def modes(s, info, lattice, kind, laced=0.0, nets_laced=0.0):
    """Natural frequencies (rad/s) along or about the axis, the rigid motion removed, and the
    mass-normalised mode shapes. (In torsion the despun array, free on its bearing, isn't in the
    chain: the hub's polar inertia alone is lumped at the nodes.)"""
    m, k = _chain(s, info, kind, lattice, laced, nets_laced)
    sq = 1 / np.sqrt(m)
    w2, vec = np.linalg.eigh(k * np.outer(sq, sq))
    keep = w2 > 1e-9 * w2.max()
    return np.sqrt(w2[keep]), (vec[:, keep].T * sq).T, m, k


def response(s, info, lattice, kind, dof, load, duration=None, laced=0.0, nets_laced=0.0, spins=40,
             samples=4000):
    """Peak spring forces under a load (N, or N m) applied suddenly at `dof` and held, or held for
    `duration` s (a pulse), undamped, through the modes (the rigid motion, which carries the
    momentum, left out: it strains nothing)."""
    w, phi, m, k = modes(s, info, lattice, kind, laced, nets_laced)
    times = np.linspace(0, spins * 2 * math.pi / s.omega, samples)

    def step(t):
        return np.where(t[:, None] > 0, 1 - np.cos(np.outer(np.maximum(t, 0), w)), 0.0) / w ** 2

    shape = step(times) - (step(times - duration) if duration else 0.0)
    q = shape * (phi[dof] * load) @ phi.T
    n_hub = len(s.hub_nodes)
    links = [max(abs(q[:, n_hub + a] - q[:, n_hub + b]).max() for a, b, _, _ in s.links)] if s.links else [0.0]
    link_k = lattice["k_axial"] if kind == "axial" else lattice["k_torsion"]
    # The largest force (or torque) carried by any spring: hub elements, nets, lattices.
    forces = []
    for i in range(len(m)):
        for j in range(i + 1, len(m)):
            if k[i, j] != 0:
                forces.append(-k[i, j] * abs(q[:, i] - q[:, j]).max())
    return {"link_motion": links[0], "link_force": link_k * links[0], "largest": max(forces),
            "lowest": float(w.min())}


def lowest(s, info, lattice, kind, laced=0.0, nets_laced=0.0):
    return float(modes(s, info, lattice, kind, laced, nets_laced)[0].min()) / s.omega


def _bisect(f, target):
    """Smallest share in [0, 1] with f(share) >= target, or None."""
    if f(1.0) < target:
        return None
    if f(0.0) >= target:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if f(mid) >= target else (mid, hi)
    return hi


BAND = 1.4                     # no axial or torsional mode between 1/BAND and BAND times the spin


def near_spin(w_ratio, band=BAND):
    return [float(x) for x in w_ratio if 1 / band < x < band]


def above_band(s, info, lattice, kind, laced, nets_laced, band=BAND):
    """The lowest mode above the band's lower edge, over the spin (inf if none)."""
    w = modes(s, info, lattice, kind, laced, nets_laced)[0] / s.omega
    w = w[w > 1 / band]
    return float(w.min()) if len(w) else math.inf


def study(p, d, k_design, tie_frac=1e-4, ship=1e7, closing=0.1, train_mass=50e3, band=BAND):
    """Axial and torsional modes of the stack with its rim lattice: as built (radial farm spokes,
    radial stabilising lines), then with the least crossing of the farm spokes and lacing of the
    tori's lines that clears the band around the spin; and the docking and braking loads."""
    lat, s, info, _ = lk.converged(p, d, k_design, tie_frac=tie_frac)
    geo, nets, h = info["geometry"], info["nets"], info["geometry"]["hub_radius"]
    bare = {kind: modes(s, info, lat, kind)[0] / s.omega for kind in ("axial", "torsion")}
    farm_share = _bisect(lambda x: above_band(s, info, lat, "axial", x, 0.0, band), band)
    farm_share = 1.0 if farm_share is None else farm_share
    nets_share = _bisect(lambda x: above_band(s, info, lat, "torsion", farm_share, x, band), band)
    nets_share = 1.0 if nets_share is None else nets_share
    w_ax = modes(s, info, lat, "axial", farm_share, nets_share)[0] / s.omega
    w_to = modes(s, info, lat, "torsion", farm_share, nets_share)[0] / s.omega
    n_hub = len(s.hub_nodes)
    # Docking: the ship's axial momentum taken out by the dock's buffers over BUFFER seconds.
    dock = response(s, info, lat, "axial", 0, ship * closing / BUFFER, duration=BUFFER, laced=farm_share,
                    nets_laced=nets_share)
    radius = geo["radius"] - geo["width"]
    brake_torque = train_mass * TRAIN_BRAKE * radius
    brake = response(s, info, lat, "torsion", n_hub, brake_torque, laced=farm_share, nets_laced=nets_share)
    spoke_length = geo["farm_radius"] - h
    farm_extra = farm_share * info["mass"]["farm_spokes"] * (math.hypot(geo["farm_width"], spoke_length)
                                                            / spoke_length - 1)
    return {
        "axial_bare_near": near_spin(bare["axial"], band), "torsion_bare_near": near_spin(bare["torsion"], band),
        "axial_bare": float(bare["axial"].min()), "torsion_bare": float(bare["torsion"].min()),
        "farm_crossed": farm_share, "nets_laced": nets_share,
        "farm_extra_mass": farm_extra, "nets_extra_mass": net_lacing(nets, h, nets_share)[1],
        "axial_near": near_spin(w_ax, band), "torsion_near": near_spin(w_to, band),
        "axial_lowest": float(w_ax.min()), "torsion_lowest": float(w_to.min()),
        "axial_above": float(w_ax[w_ax > 1 / band].min()), "torsion_above": float(w_to[w_to > 1 / band].min()),
        "torsion_below": [float(x) for x in np.unique(np.round(w_to[w_to <= 1 / band], 3))],
        "dock_force": ship * closing / BUFFER, "dock_link_force": dock["link_force"], "dock_largest": dock["largest"],
        "brake_torque": brake_torque, "brake_link_torque": brake["link_force"], "brake_largest": brake["largest"],
        "lattice": lat,
    }
