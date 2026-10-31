"""Joints (plan §4): the hub's between its segments, the rim lattice's into the tori, and the
tunnels' across the gaps.

- The hub is built in segments, one per torus or farm ring, joined at the gaps. A joint is a
  rotational spring k (N m/rad) between segments (stack.build's joint_k). The stack's margin falls
  as the joints soften; the requirement is the k keeping KNEE of the continuous hub's margin. A
  bolted flange ring of radius h, bolts of axial stiffness k_b every s along it, gives
  k = (k_b / s) pi h^3, as long as the bolts' preload keeps the flanges closed under the hub's
  largest moment (line load M / (pi h^2)).
- The lattice's struts meet the tori at fittings on the envelope, carried to the hull through the
  jacket and crawl space by shear webs in the bay's tangential-axial plane, sized with the lattice
  for stiffness and strength and in series with its struts (links.lattice). A post bending as a
  cantilever would be far too soft: ~N k_post / 4 sideways, below the stiffness the stack needs.
- A tunnel crosses each gap. Joined rigidly it would be a stiff link at one angle (stiffness
  differing by direction) and would be bent by the rims' relative motion; so it gets an expansion
  joint taking the relative motions between the rims (radial, axial, tangential), stiff enough for
  nothing and soft enough not to load the lattice. Pressure pushes a bellows apart with p pi R^2:
  a pressure-balanced joint carries that inside itself rather than on the rims.
"""

import math

import numpy as np

from . import disturbances as ds
from . import links as lk
from . import stack as st

KNEE = 0.98
BOLT_AREA = 817e-6             # m^2, M36 stress area
BOLT_GRIP = 0.2                # m, two flanges
BOLT_SPACING = 0.1             # m
BOLT_PRELOAD = 0.7 * 640e6 * 817e-6     # N, 70% of grade 8.8 proof load
TUNNEL_RADIUS = 4.0            # m (guess: a walking and service tunnel)
PRESSURE = 70e3                # Pa
ANISOTROPY = 0.01              # largest share of the lattice's stiffness one tunnel may add


def hub_moments(s, q):
    """Largest bending moment along the hub (N m) for a response q (complex amplitudes)."""
    n = len(s.hub_nodes)
    largest = 0.0
    for e in range(n - 1):
        d = q[[2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]]
        f = s.element_stiffness(e) @ d
        largest = max(largest, abs(f[1]), abs(f[3]))
    return largest


def hub_joint(p, d, k_design, tie_frac=1e-4, knee=KNEE):
    """Rotational stiffness the hub's joints need, against a bolted flange's, and its bolts' check
    under the largest hub moment (the ballast tanks' whole capacity untrimmed)."""
    lat, s, info, unbalanced = lk.converged(p, d, k_design, tie_frac=tie_frac)
    continuous = s.forward_ratio()
    geo = info["geometry"]
    h = geo["hub_radius"]

    def ratio(k):
        return st.build(p, d, rim_link=lat["k_lat"], link_tilt=lat["tilt"], tie_frac=tie_frac,
                        joint_k=k)[0].forward_ratio()

    lo, hi = 1e10, 1e18
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        lo, hi = (lo, mid) if ratio(mid) >= knee * continuous else (mid, hi)
        if hi / lo < 1.02:
            break
    k_bolt = st.E * BOLT_AREA / BOLT_GRIP
    flange = k_bolt / BOLT_SPACING * math.pi * h ** 3
    f = np.zeros(s.size(), dtype=complex)
    f[s.body_dof(0)] = p.ballast_frac * info["mass"]["rim"] * geo["radius"] * s.omega ** 2
    moment = hub_moments(s, s.response(s.omega, f))
    line_load = moment / (math.pi * h * h)
    return {"continuous": continuous, "needed": hi, "per_pitch": s.ei / geo["pitch"], "flange": flange,
            "flange_ratio": ratio(flange), "moment": moment, "line_load": line_load,
            "preload_line": BOLT_PRELOAD / BOLT_SPACING, "opening_margin": BOLT_PRELOAD / BOLT_SPACING / line_load}


def fittings(lat):
    """The lattice's fittings (sized with it, links.lattice): shear webs through the jacket and
    crawl space, one at each strut end, in series with the struts."""
    return {"depth": lat["web_depth"], "width": lat["web_width"], "thickness": lat["web_thickness"],
            "set_by": lat["web_set_by"], "per_gap": lat["web_mass"], "k": lat["k_fitting"],
            "k_lat": lat["k_fittings_lat"], "motion": lat["fitting_motion"]}


def tunnel(geo, lat, imposed, unbalanced_link):
    """What a tunnel's expansion joint must take: the rims' relative motions at it, the pressure
    thrust it must hold inside itself, and the most lateral stiffness it may have."""
    elastic = unbalanced_link / lat["k_lat"]
    return {
        "radial": imposed["radial"] + elastic, "axial": imposed["closing"], "tangential": elastic,
        "thrust": PRESSURE * math.pi * TUNNEL_RADIUS ** 2,
        "max_lateral_k": ANISOTROPY * lat["k_lat"],
        "rigid_k": rigid_tunnel(geo), "rigid_stress": rigid_tunnel_stress(geo, imposed["radial"]),
    }


def rigid_tunnel(geo, wall=0.03):
    """Lateral stiffness of a tunnel tube fixed at both rims (bending and shear in series)."""
    length, r = max(geo["gap"], 1.0), TUNNEL_RADIUS
    inertia, area = math.pi * r ** 3 * wall, 2 * math.pi * r * wall
    return 1 / (length ** 3 / (12 * st.E * inertia) + length / (st.SHEAR_KAPPA * st.G * area))


def rigid_tunnel_stress(geo, offset, wall=0.03):
    """Bending stress at a rigid tunnel's ends when one rim moves `offset` radially against the other."""
    length, r = max(geo["gap"], 1.0), TUNNEL_RADIUS
    force = rigid_tunnel(geo, wall) * offset
    return force * length / 2 / (math.pi * r * r * wall)
