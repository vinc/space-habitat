"""Rim links between neighbouring tori: what they must resist, and a lattice that does it (plan §4).

The flexible stack (stack.py) needs the tori held on the shared axis by links across the gaps
between their envelopes. What the links must resist follows from the modes:

- Only their lateral stiffness matters: relative sideways motion of neighbouring rims at the
  link's mid-plane. Their tilt stiffness (relative tilt, from stiffness along the axis) moves the
  lowest forward whirl by under 1% (compare_tilt), so the links need not be stiff along the axis.
- A lateral relative motion u of two rims is, at an angle theta around them, u cos(theta) radially
  and u sin(theta) tangentially. N links stiff only tangentially (k_t each), spread evenly around
  the rim (any N >= 3), give a lateral stiffness of N k_t / 2, the same in every direction: links
  compliant radially (and so free of the rims' differential radial growth) do the job.

The lattice: a ring of X-braced bays in the cylinder across the gap, at the envelopes' closest
approach (radius r - a, a the tube radius), its diagonals at 45 degrees (bays as wide as the gap).
In its own surface it is stiff in shear (tangential) and along the axis; out of its surface
(radially) its struts bend, so it follows the rims' differential growth. Per bay, a tangential
relative motion u_t stretches one diagonal and shortens the other by u_t / sqrt(2): k_bay = E A /
L_d; N bays give k_lat = N k_bay / 2. Pinned tubular struts (D/t fixed): Euler buckling
pi^2 E A D^2 / (8 L^2); no preload (struts, not cables: preloaded cables would pull the tori
together along the axis, where only the nets' weak axial stiffness holds them).

Differential motion between neighbours, imposed, and what it costs the lattice:
- radial (a warmer or more loaded rim): the struts bend out of the surface; their hoop share
  strains by about delta / R;
- axial (the hub warmer than the rims between two net planes): the lattice is far stiffer than the
  nets along the axis (structure_model.hub), so the tori move with the lattice and the nets take
  the difference: force = the nets' axial stiffness x the mismatch;
- the struts' own temperature: X-braced diagonals shrinking alike close the gap (along the axis)
  rather than strain, since along the axis only the nets hold the tori.
"""

import math

from . import stack as st

E = st.E
STRUT_D_OVER_T = 20.0          # tubular struts' diameter over wall thickness
SAFETY = 2.0                   # on buckling and yield, for the struts' design load
YIELD = 350e6                  # Pa, structural steel for the struts (not the cable wire)
MIN_AREA = 2e-4                # m^2, smallest strut worth building (a ~6 cm tube)
KNEE = 0.98                    # design stiffness: this share of the margin with rigid links
STIFF = 1e13                   # N/m, links taken as rigid
THERMAL_EXPANSION = 12e-6      # 1/K, steel


def link_radius(geo):
    return geo["radius"] - geo["tube_radius"]


def lattice(geo, k_lat, steel_density, force=0.0):
    """An X-braced ring across one gap giving lateral stiffness k_lat (N/m): its bays, struts and
    mass. force: the largest lateral force it carries (N), for the struts' buckling and yield."""
    radius, height = link_radius(geo), max(geo["gap"], 1.0)
    bays = max(3, round(2 * math.pi * radius / height))
    width = 2 * math.pi * radius / bays
    diagonal = math.hypot(width, height)
    k_bay = 2 * k_lat / bays
    cos = width / diagonal
    # A tangential motion u_t stretches each diagonal by u_t cos: k_bay = 2 (E A / L) cos^2.
    area_stiff = k_bay * diagonal / (2 * E * cos ** 2)
    # The lateral force F spreads as F sin(theta) / (N / 2) per bay: the largest bay shear is 2F / N,
    # each diagonal carrying half of it along its length.
    strut_force = (2 * force / bays) / (2 * cos)
    area_yield = SAFETY * strut_force / YIELD
    # Euler, pinned: P = pi^2 E I / L^2, I = A D^2 / 8 for a thin tube, D = sqrt(D/t A / pi).
    area_buckle = math.sqrt(SAFETY * strut_force * 8 * diagonal ** 2 * math.pi
                            / (math.pi ** 2 * E * STRUT_D_OVER_T)) if force else 0.0
    area = max(area_stiff, area_yield, area_buckle, MIN_AREA)
    set_by = max((area_stiff, "stiffness"), (area_yield, "yield"), (area_buckle, "buckling"),
                 (MIN_AREA, "minimum size"))[1]
    diameter = math.sqrt(STRUT_D_OVER_T * area / math.pi)
    k_actual = bays * 2 * E * area / diagonal * cos ** 2 / 2
    mass = 2 * bays * area * diagonal * steel_density
    return {
        "bays": bays, "width": width, "height": height, "diagonal": diagonal, "area": area,
        "set_by": set_by, "diameter": diameter, "mass": mass, "k_lat": k_actual, "radius": radius,
        # Share of the gap's cylinder the struts cover (seen radially), for the gap vents.
        "blocked": 2 * diagonal * diameter / (width * height),
        "strut_force": strut_force,
        # Stiffness along the axis (both diagonals stretch alike) and in torsion (tangential, all bays).
        "k_axial": bays * 2 * E * area / diagonal * (height / diagonal) ** 2,
        "k_torsion": bays * k_bay * radius ** 2,
        "tilt": bays * 2 * E * area / diagonal * (height / diagonal) ** 2 * radius ** 2 / 2,
    }


def compare_tilt(p, d, k_lat, tie_frac=0.0):
    """Lowest forward whirl over the spin with the links' tilt stiffness as taken by default
    (k r^2 / 2), none, and a lattice's (from its axial stiffness)."""
    from habitat_model import evaluate
    geo = evaluate(p, d)["geometry"]
    lat = lattice(geo, k_lat, p.steel_density)
    out = {}
    for name, tilt in (("default", None), ("none", 0.0), ("lattice", lat["tilt"])):
        out[name] = st.build(p, d, rim_link=k_lat, tie_frac=tie_frac, link_tilt=tilt)[0].forward_ratio()
    return out


def design_stiffness(p, d, tie_frac=0.0, knee=KNEE):
    """Lateral link stiffness giving `knee` of the margin rigid links would give: past it, stiffer
    links buy almost nothing (the nets and the hub's bending set the rest)."""
    rigid = st.build(p, d, rim_link=STIFF, tie_frac=tie_frac)[0].forward_ratio()
    k = st.required(p, d, "rim_link", target=knee * rigid, low=1e6, high=STIFF, tie_frac=tie_frac)
    return k, rigid


def imposed(p, geo, nets, hub_dt=20.0, rim_dt=4.0, strut_dt=100.0):
    """Differential motions between neighbours and what they cost.

    hub_dt: the hub warmer (or colder) than the rims, over a pitch between two tori's net planes
    (K); rim_dt: one rim warmer than its neighbour (K, about the valleys' daily swing); strut_dt:
    the struts colder than the rims (K, in shadow facing space)."""
    radius = link_radius(geo)
    axial_mismatch = THERMAL_EXPANSION * hub_dt * geo["pitch"]
    k_axial_nets = nets["k_axial"] + nets["k_axial_inclined"]
    radial = THERMAL_EXPANSION * rim_dt * radius
    gap = max(geo["gap"], 1.0)
    # Struts shrinking by strut_dt at 45 degrees close the gap by twice their strain times its height.
    closing = 2 * THERMAL_EXPANSION * strut_dt * gap
    return {
        "axial_mismatch": axial_mismatch, "axial_force": k_axial_nets * axial_mismatch,
        "k_axial_nets": k_axial_nets,
        "radial": radial, "hoop_strain": radial / radius, "hoop_stress": E * radial / radius,
        "closing": closing, "closing_force": k_axial_nets * closing,
    }


def converged(p, d, k_design, tie_frac=0.0, iterations=20):
    """The lattice sized for k_design and for the link force its own stack takes under the largest
    imbalance (the ballast tanks' whole capacity untrimmed), iterated until the struts agree: sizing
    by buckling stiffens the lattice, which changes the force. Returns (lattice, stack, info,
    imbalance) on the finished lattice."""
    from . import disturbances as ds
    s, info = st.build(p, d, rim_link=k_design, tie_frac=tie_frac)
    geo, mass_e = info["geometry"], p.ballast_frac * info["mass"]["rim"]
    force, area = ds.imbalance(s, geo, mass_e)["link"], None
    for _ in range(iterations):
        lat = lattice(geo, k_design, p.steel_density, force=force)
        s, info = st.build(p, d, rim_link=lat["k_lat"], tie_frac=tie_frac, link_tilt=lat["tilt"])
        unbalanced = ds.imbalance(s, geo, mass_e)
        if area is not None and abs(lat["area"] / area - 1) < 1e-4:
            break
        area, force = lat["area"], unbalanced["link"]
    lat = lattice(geo, k_design, p.steel_density, force=unbalanced["link"])
    return lat, s, info, unbalanced


def construction(p, d, k_design, tie_frac=0.0, target=1.2):
    """Building and losing lattices: the stack's margin with one gap left unlinked (a torus just
    closed next to the stack, or a lattice lost), the worst gap, and the share of a gap's bays
    that must be in place (spread evenly around it) to restore `target`."""
    lat, s, info, _ = converged(p, d, k_design, tie_frac=tie_frac)
    n = d.n_tori
    full = s.forward_ratio()
    missing = {}
    for gap in range(n - 1):
        missing[gap] = st.build(p, d, rim_link=lat["k_lat"], link_tilt=lat["tilt"], tie_frac=tie_frac,
                                links_skip=(gap,))[0].forward_ratio()
    worst = min(missing, key=missing.get) if missing else None

    def with_share(gap, share):
        stack, _ = st.build(p, d, rim_link=lat["k_lat"], link_tilt=lat["tilt"], tie_frac=tie_frac)
        stack.links = [(i, j, kl * (share if i == gap else 1.0), kt * (share if i == gap else 1.0))
                       for i, j, kl, kt in stack.links]
        return stack.forward_ratio()

    share = None
    if worst is not None:
        if with_share(worst, 1.0) >= target:
            lo, hi = 1e-6, 1.0
            if with_share(worst, lo) >= target:
                hi = lo
            else:
                for _ in range(40):
                    mid = math.sqrt(lo * hi)
                    lo, hi = (lo, mid) if with_share(worst, mid) >= target else (mid, hi)
                    if hi / lo < 1.01:
                        break
            share = hi
    end = missing.get(n - 2)
    growth = None
    if worst is not None:
        _, g = st.build(p, d, rim_link=lat["k_lat"], link_tilt=lat["tilt"], tie_frac=tie_frac,
                        links_skip=(worst,))[0].modes(damping=0.01)
        growth = float(g.max())
    return {"full": full, "missing": missing, "worst_gap": worst, "growth": growth,
            "e_folding_hours": (1 / growth / 3600) if growth and growth > 0 else None,
            "worst": missing[worst] if worst is not None else None, "end_gap": end,
            "share": share, "bays": math.ceil(share * lat["bays"]) if share else None, "lattice": lat}
