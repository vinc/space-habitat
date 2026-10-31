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

Each strut end meets the torus at a fitting: a shear web through the jacket and crawl space to
the hull, in the bay's tangential-axial plane (a jacket bulkhead in that plane), in series with
the struts in every stiffness (lattice()).

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
STRUT_SHARE = 2.0              # struts sized for twice the bay's stiffness, the fittings take the rest
WEB_KAPPA = 5 / 6              # shear coefficient of a plate's rectangular section
MIN_WEB = 0.006                # m, thinnest fitting web
WEB_BUCKLING_K = 9.34          # shear buckling coefficient of a square plate, simply supported


def link_radius(geo):
    """The lattice's radius: the tube's centre (r - a). Neighbouring envelopes come closest there,
    at the tubes' flat sides facing each other along the habitat's axis (the gap is axial: pitch =
    2 x envelope radius + gap)."""
    return geo["radius"] - geo["tube_radius"]


def fitting_depth(geo):
    """How far a fitting reaches from the envelope to the hull, through the jacket and crawl space.
    At the tube's side, where the lattice is, that depth runs along the habitat's axis."""
    return geo["envelope_radius"] - geo["tube_radius"]


def web_stiffness(depth, width):
    """A fitting's shear web per metre of thickness. At the tube's side the jacket's depth runs along
    the habitat's axis, so the web spans `depth` along the axis (from the envelope to the hull) and is
    `width` wide tangentially: it lies in the tangential-axial plane, its normal radial. Both loads
    the lattice gives it are in that plane: tangential, at its envelope end (bending and shear in
    series, k = t / (L^3 / (3 E w^3 / 12) + L / (kappa G w))), and axial, along its span (E w t / L).
    Its weak direction, out of its plane, is the habitat's radial one, where the lattice is meant to
    give way."""
    tangential = 1 / (depth ** 3 / (3 * E * width ** 3 / 12) + depth / (WEB_KAPPA * st.G * width))
    return tangential, E * width / depth


def lattice(geo, k_lat, steel_density, force=0.0):
    """An X-braced ring across one gap and its fittings, together giving lateral stiffness k_lat
    (N/m): its bays, struts, fittings and mass. force: the largest lateral force it carries (N), for
    the struts' buckling and yield and the fittings' strength.

    Each strut end meets the torus at a fitting carried to the hull through the jacket and crawl
    space by a shear web in the bay's tangential-axial plane (a jacket bulkhead in that plane): the
    bay's struts and the fittings at its two ends act in series, 1/k = 1/k_struts + 2/k_fitting.
    Sizing: the struts for twice the bay's share of k_lat (or their strength), then the webs for the
    rest of the compliance (or their strength), so the finished lattice gives at least k_lat."""
    radius, height = link_radius(geo), max(geo["gap"], 1.0)
    bays = max(3, round(2 * math.pi * radius / height))
    width = 2 * math.pi * radius / bays
    diagonal = math.hypot(width, height)
    k_bay = 2 * k_lat / bays
    cos = width / diagonal
    # A tangential motion u_t stretches each diagonal by u_t cos: k_bay = 2 (E A / L) cos^2.
    area_stiff = STRUT_SHARE * k_bay * diagonal / (2 * E * cos ** 2)
    # The lateral force F spreads as F sin(theta) / (N / 2) per bay: the largest bay shear is 2F / N,
    # each diagonal carrying half of it along its length.
    shear = 2 * force / bays
    strut_force = shear / (2 * cos)
    area_yield = SAFETY * strut_force / YIELD
    # Euler, pinned: P = pi^2 E I / L^2, I = A D^2 / 8 for a thin tube, D = sqrt(D/t A / pi).
    area_buckle = math.sqrt(SAFETY * strut_force * 8 * diagonal ** 2 * math.pi
                            / (math.pi ** 2 * E * STRUT_D_OVER_T)) if force else 0.0
    area = max(area_stiff, area_yield, area_buckle, MIN_AREA)
    set_by = max((area_stiff, "stiffness"), (area_yield, "yield"), (area_buckle, "buckling"),
                 (MIN_AREA, "minimum size"))[1]
    diameter = math.sqrt(STRUT_D_OVER_T * area / math.pi)
    k_struts = 2 * E * area / diagonal * cos ** 2                 # per bay, tangential
    k_struts_axial = 2 * E * area / diagonal * (height / diagonal) ** 2
    # Fittings: webs as wide as the jacket is deep (or the bay, if narrower).
    depth = fitting_depth(geo)
    web_width = min(depth, width)
    per_t, axial_per_t = web_stiffness(depth, web_width)
    # Stiffness: 1/k_bay >= 1/k_struts + 2/k_fit.
    spare = 1 / k_bay - 1 / k_struts
    t_stiff = 2 / (spare * per_t) if spare > 0 else math.inf
    # Strength: the bay's shear at the web's envelope end, bending at its root (6 V L / (t w^2)) and
    # shear (1.5 V / (t w)).
    t_bend = SAFETY * 6 * shear * depth / (YIELD * web_width ** 2)
    t_shear = SAFETY * 1.5 * shear / (YIELD / math.sqrt(3) * web_width)
    # Shear buckling of the unstiffened panel (its shorter side b): tau_cr = k pi^2 E / (12 (1 - nu^2))
    # (t / b)^2 against the mean shear V / (t w): t^3 = SAFETY V b^2 / (w C).
    side = min(depth, web_width)
    c_buckle = WEB_BUCKLING_K * math.pi ** 2 * E / (12 * (1 - 0.3 ** 2))
    t_buckle = (SAFETY * shear * side ** 2 / (web_width * c_buckle)) ** (1 / 3) if shear else 0.0
    web_t = max(t_stiff, t_bend, t_shear, t_buckle, MIN_WEB)
    web_set_by = max((t_stiff, "stiffness"), (t_bend, "bending"), (t_shear, "shear"), (t_buckle, "buckling"),
                     (MIN_WEB, "minimum"))[1]
    k_fit, k_fit_axial = per_t * web_t, axial_per_t * web_t
    k_bay_tan = 1 / (1 / k_struts + 2 / k_fit)
    k_bay_ax = 1 / (1 / k_struts_axial + 2 / k_fit_axial)
    k_actual = bays * k_bay_tan / 2
    mass = 2 * bays * area * diagonal * steel_density
    web_mass = 2 * bays * web_t * web_width * depth * steel_density
    return {
        "bays": bays, "width": width, "height": height, "diagonal": diagonal, "area": area,
        "set_by": set_by, "diameter": diameter, "mass": mass, "k_lat": k_actual, "radius": radius,
        # Share of the gap's cylinder the struts cover (seen radially), for the gap vents.
        "blocked": 2 * diagonal * diameter / (width * height),
        "strut_force": strut_force, "shear": shear,
        "k_struts_lat": bays * k_struts / 2,
        "web_thickness": web_t, "web_set_by": web_set_by, "web_width": web_width, "web_depth": depth,
        "web_mass": web_mass, "k_fitting": k_fit, "k_fittings_lat": bays * k_fit / 4,
        "fitting_motion": shear / k_fit,
        # Along the axis (both diagonals stretch alike) and in torsion (tangential, all bays), each bay
        # with its fittings in series; torsion N k_t R^2 = 2 k_lat R^2.
        "k_axial": bays * k_bay_ax,
        "k_torsion": bays * k_bay_tan * radius ** 2,
        "tilt": bays * k_bay_ax * radius ** 2 / 2,
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


def building_torus(p, d, share, link=True, radial_lines=True, tie_frac=1e-4, k_design=None):
    """The stack while its last torus is being hung, at full spin: that torus a partial ring of
    `share` of its rim in two opposite pairs of arcs at right angles (so its transverse inertia is
    half its polar one, as for a ring), held on the hub by its nets (their stiffness in proportion to
    its chords), by the temporary radial lines from the hub to its arcs' single-laced anchors
    (structure_model.nonlinear and sequence.SUPPORT: N / 2 E A / L sideways, N counted from the arcs'
    own geometry, if radial_lines) and, if link, by the rim
    lattice's bays alongside its arcs (in proportion). Returns the stack's lowest forward whirl over
    the spin, the lines' stiffness and their number."""
    if k_design is None:
        k_design, _ = design_stiffness(p, d, tie_frac=tie_frac)
    lat, s, info, _ = converged(p, d, k_design, tie_frac=tie_frac)
    geo, mass = info["geometry"], info["mass"]
    r = geo["radius"]
    last = d.n_tori - 1
    body = s.bodies[last]
    k_lines, n_single = 0.0, 0
    if radial_lines:
        # The single-laced anchors of the very arcs being hung (two pairs at right angles), counted from
        # the construction model's own geometry, and the proposed lines' area there.
        from structure_model import nonlinear as nl
        from structure_model import sequence
        model, built = nl.for_design(
            p, r, arcs_fn=lambda n, net: nl.opposite_pairs(n, max(1, round(share * n / 4)), pairs=2),
            **sequence.SUPPORT)
        n_single = len(model.radials)
        length = r - geo["hub_radius"]
        k_lines = n_single / 2 * E * model.radial_area / length
    m_part = share * body.mass
    springs = [(z, k * share + k_lines / len(body.springs)) for z, k in body.springs]
    s.bodies[last] = st.Body(body.name, m_part, share * body.polar, share * body.transverse, body.z, springs)
    s.links = [(i, j, kl * (share if link else 0.0), kt * (share if link else 0.0)) if j == last else (i, j, kl, kt)
               for i, j, kl, kt in s.links]
    return s.forward_ratio(), k_lines, n_single
