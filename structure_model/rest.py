"""The baseline: a torus built at rest and spun up finished (plan §2).

A child's stack is assembled at rest (every ring closed, the lattice fitted, rock and soil in), then
spun up slowly with the water last. This module checks that sequence in the ring's plane, with the
geometrically nonlinear model (nonlinear.py), and estimates what the ring model leaves out:

1. At rest. The chords are pretensioned (they must stay taut through the temperature swings of
   the assembly, and they hold the hub in its window), and with nothing to resist it but the hull,
   the pretension squeezes the closed ring: the joints between segments bear on stops, closed, and
   the hull carries the chords' pull as a hoop in compression. Checked: the equilibrium, the hull's
   compression against its allowable, every chord taut, the ring's buckling in its plane.
2. The cables taking up tension, the joints settling. The joints slide along the rim but bear on
   stops (closed: compression and bending, up to their compression times the tube's radius; open:
   sliding, on a light spring along the rim). As the spin grows the hoop's compression falls; once
   it is gone the joints open and the chords carry the rim alone, as finished. Checked by stepping
   the spin up from rest, with a scatter in the chords' lengths and in the rim's mass per anchor:
   every chord's, the hull's and the joints' loads against their values at full spin.
   Found: a ring of joints that only slide is barely held along the rim (the near-diametral chords
   hardly resist the segments sliding in odd harmonics), so a 2% scatter in the rim's mass slides
   segments by metres; a light spring in each joint (SLIDE_SPRING) holds them for a few MPa in the
   hull.
3. The hub's stabilising lines from rest to full spin: fixed-length, tension-only, in series with
   chords whose tension and bow grow with the spin (the bow is nil at rest): a line installed snug
   at rest holds back the whole bow and is sized for it (review of #18).
4. The spin-up torque: the angular acceleration's loads on the rims, the farm rings on their radial
   spokes, the hub through its laced lines and the lattice, set against the spin load; the spin-up's
   propellant, energy and time; the water added last.
5. The fill: the rock and soil, placed at rest in compartments, settle as gravity grows. Cells
   filled loose hold less rock than the design (their volume is fixed), short everywhere until
   topped up; the loose fill settles by its porosity, and at the tube's sides that also leaves a
   slot through the jacket at the top of every cell, which the radiation sees.
"""

import math

import numpy as np

from habitat_model import Design, evaluate
from . import hub as hub_model
from . import nonlinear as nl

ALPHA_STEEL = 12e-6           # 1/K, thermal expansion of steel
THERMAL_SWING = 20.0          # K, the chords' temperature swing against the hull's while at rest (guess)
PRESTRAIN = 5e-4              # the chords' strain at rest (proposed): taut through the thermal swing (2.4e-4)
LENGTH_SCATTER = 0.02         # m, the chords' unstretched lengths as made, 1 sigma (guess: ~1e-5 of 1.8 km)
MASS_SCATTER = 0.02           # the rim's mass per anchor (rock, fill, fittings), 1 sigma (guess)
SLIDE_SPRING = 1e8            # N/m, a spring along the rim in each joint once it opens (proposed)
HULL_COMPRESSION = 150e6      # Pa, the hull's allowable in compression (half the plate stress, as tube_section)
SEED = 1

# The spin-up (notes §12): thrusters on each ring's rim, one set per ring sized to its own inertia.
FAST_SPINUP_DAYS = 30.0       # a fast spin-up, to bound the angular acceleration's loads
THRUST_MISMATCH = 0.1         # one torus's thrusters off their share by this much, the lattice carrying it
SHIP_MASS, SHIP_CLOSING, BUFFER = 1e7, 0.1, 10.0   # a 10 kt ship docking at 0.1 m/s over 10 s (as axial_torsion)
ROCK_DRIVER_EXHAUST = 0.5     # km/s, a mass driver throwing host rock for the spin-up (proposed, guess)

# The fill.
GRAIN_DENSITY = 3.5           # t/m^3, L and LL chondrite grains (Consolmagno et al. 2008: ~3.5-3.6)
LOOSE_DENSITY = (1.6, 1.75, 1.9)     # t/m^3, crushed rock placed loose at rest: low, mid, high (guess)
FILL_MODULUS = (20e6, 50e6, 100e6)   # Pa, constrained modulus of the compacted fill (guess)
SETTLE_NONUNIFORM = 0.2       # share of the settlement that differs around the ring (guess)


# -- the ring in its plane -----------------------------------------------------------------------------
def model(p, r, prestrain=PRESTRAIN, scatter=True, seed=SEED, slide=SLIDE_SPRING,
          length_scatter=LENGTH_SCATTER, mass_scatter=MASS_SCATTER):
    """The closed ring with its joints on stops, the chords pretensioned, and (scatter) its chords'
    lengths and its mass per anchor scattered as made."""
    m, info = nl.for_design(p, r, stops=True, prestrain=prestrain, slide_stiffness=slide)
    if scatter:
        rng = np.random.default_rng(seed)
        m.chord_l0 = m.chord_l0 + rng.normal(0.0, length_scatter, len(m.chords))
        anchors = list(m.anchor_node.values())
        m.mass[anchors] *= 1 + rng.normal(0.0, mass_scatter, len(anchors))
    return m, info


def summary(m, info, u, lam):
    """The loads in a state at lambda = (spin / final)^2."""
    om = info["geometry"]["omega"]
    _, _, out = m.assemble(u, lam * om ** 2)
    T = np.array(out["T"])
    N = np.array(out["N"])
    J = out["J"]
    gaps = np.array([j["gap"] for j in J])
    comp = np.array([-j["tension"] for j in J if j["gap"] <= 0] or [0.0])
    area = info["steel_area"]
    a = info["geometry"]["tube_radius"]
    return {
        "lam": lam, "spin": math.sqrt(lam), "T": T, "N": N,
        "tension_min": float(T.min()), "tension_max": float(T.max()), "slack": int((T <= 0).sum()),
        "hull_min": float(N.min()) / area, "hull_max": float(N.max()) / area,
        "hull_bending": 2 * max(out["M"]) / (area * a),
        "open": int((gaps > 0).sum()), "joints": len(gaps),
        "gap_min": float(gaps.min()), "gap_max": float(gaps.max()), "gap_mean": float(gaps.mean()),
        "joint_compression": float(comp.max()),
        "joint_moment": float(max(abs(j["moment"]) for j in J)),
        "peak_stress": m.peak_stress(T, math.sqrt(lam) * om),
        "displacement": m._relative(u),
    }


def at_rest(p, r, prestrain=PRESTRAIN, scatter=True, **kw):
    m, info = model(p, r, prestrain, scatter, **kw)
    C, load_ref = m._setup(info["geometry"]["omega"])
    u = m._newton(np.zeros(m.ndof), 0.0, C, load_ref, max_iter=80)
    if u is None:
        return None, m, info
    return summary(m, info, u, 0.0), m, info


def buckling(p, r, prestrains=(1e-4, 1e-3)):
    """The closed ring at rest, joints closed, under the chords' pretension: the lowest eigenvalue of
    its tangent stiffness (rigid motions removed) at two pretensions, extrapolated to zero (it falls
    linearly with the pretension: the hull's compression and the chords' pull are both linear in it).
    In the ring's plane only."""
    eig = []
    for pre in prestrains:
        m, info = model(p, r, pre, scatter=False)
        C, load_ref = m._setup(info["geometry"]["omega"])
        u = m._newton(np.zeros(m.ndof), 0.0, C, load_ref, max_iter=80)
        _, K, _ = m.assemble(u, 0.0)
        Q, _ = np.linalg.qr(C.T, mode="complete")
        Z = Q[:, C.shape[0]:]
        eig.append(float(np.linalg.eigvalsh(Z.T @ (0.5 * (K + K.T)) @ Z)[0]))
    (p1, p2), (e1, e2) = prestrains, eig
    critical = p1 + e1 * (p2 - p1) / (e1 - e2) if e1 > e2 else math.inf
    area = info["steel_area"]
    return {"eigen": eig, "critical_prestrain": critical, "factor": critical / PRESTRAIN,
            "classic_hoop": 3 * m.rim_ei / r ** 2, "steel_area": area}


def spin_up(p, r, prestrain=PRESTRAIN, scatter=True, record=(0.0, 0.01, 0.03, 0.1, 0.25, 0.5, 1.0), **kw):
    """Step the spin up from rest to full (lambda 0 -> 1), each step from the last equilibrium, the
    step cut where Newton fails. Returns the states at the recorded lambdas, the lambdas where the
    first and the last joint opened, and every load's peak on the way against its value at full
    spin (per chord, the hull, the joints)."""
    m, info = model(p, r, prestrain, scatter, **kw)
    om = info["geometry"]["omega"]
    C, load_ref = m._setup(om)
    u = m._newton(np.zeros(m.ndof), 0.0, C, load_ref, max_iter=80)
    if u is None:
        return {"resolved": False, "reached": 0.0}
    states = [summary(m, info, u, 0.0)]
    marks = sorted(set(record) | {1.0})
    lam, step = 0.0, 0.02
    first_open = all_open = None
    while lam < 1.0 - 1e-12:
        nxt = min(1.0, lam + step)
        upcoming = [x for x in marks if x > lam + 1e-12]
        if upcoming:
            nxt = min(nxt, upcoming[0])
        trial = m._newton(u, nxt * om ** 2, C, load_ref, max_iter=60)
        if trial is None:
            step /= 2
            if step < 1e-5:
                return {"resolved": False, "reached": math.sqrt(lam), "states": states}
            continue
        u, lam = trial, nxt
        step = min(step * 1.5, 0.2)
        s = summary(m, info, u, lam)
        if s["open"] and first_open is None:
            first_open = lam
        if s["open"] == s["joints"] and all_open is None:
            all_open = lam
        states.append(s)
    final = states[-1]
    # Where the hoop's compression runs out: it falls linearly with lambda while the joints are closed.
    closed = [x for x in states if x["open"] == 0 and x["lam"] > 0]
    c0 = states[0]["joint_compression"]
    lam_open = None
    if closed and c0 > closed[-1]["joint_compression"]:
        lc = closed[-1]
        lam_open = lc["lam"] * c0 / (c0 - lc["joint_compression"])
    T_path = np.array([s["T"] for s in states])
    with np.errstate(divide="ignore", invalid="ignore"):
        chord_ratio = float(np.nanmax(T_path / final["T"]))
    hull_peak = max(max(abs(s["hull_min"]), abs(s["hull_max"])) for s in states)
    hull_final = max(abs(final["hull_min"]), abs(final["hull_max"]))
    recorded = [s for s in states if any(abs(s["lam"] - x) < 1e-9 for x in marks)]
    te = info["net"]["tension_end"]
    return {
        "resolved": True, "reached": 1.0, "states": recorded, "steps": len(states),
        "first_open": first_open, "all_open": all_open, "lam_open": lam_open,
        "spin_open": math.sqrt(lam_open) if lam_open else None,
        "chord_path_ratio": chord_ratio,                 # every chord's peak on the way / its full-spin tension
        "hull_peak": hull_peak, "hull_final": hull_final,
        "hull_compression_peak": -min(s["hull_min"] for s in states),
        "bending_peak": max(s["hull_bending"] for s in states), "bending_final": final["hull_bending"],
        "rest": states[0], "final": final, "tension_end": te, "sigma": info["sigma"],
        "hoop": info["line_mass"] * (om * r) ** 2,
    }


def thermal(p, r, swing=THERMAL_SWING):
    """At rest, the chords colder (tighter) and warmer (looser) than the hull by `swing`."""
    out = {}
    for name, sign in (("cold", 1), ("warm", -1)):
        s, _, info = at_rest(p, r, PRESTRAIN + sign * ALPHA_STEEL * swing)
        out[name] = s
    return out


# -- the hub at rest -------------------------------------------------------------------------------------
def take_up(p, r):
    """How the chords' tension grows from rest, as a share of the finished tension: s0 at rest, then
    linearly while the joints bear (the hoop's compression falling) to lambda_open, where it is gone,
    then with the spin load. From the ring as drawn at rest and at a low spin (both joints closed)."""
    m, info = model(p, r, scatter=False)
    om = info["geometry"]["omega"]
    C, load_ref = m._setup(om)
    u0 = m._newton(np.zeros(m.ndof), 0.0, C, load_ref, max_iter=80)
    s0 = summary(m, info, u0, 0.0)
    low = 0.02
    u1 = m._newton(u0, low * om ** 2, C, load_ref, max_iter=80)
    s1 = summary(m, info, u1, low)
    c0, c1 = s0["joint_compression"], s1["joint_compression"]
    lam_open = low * c0 / (c0 - c1)
    te = info["net"]["tension_end"]
    return {"s0": float(s0["T"].mean()) / te, "lam_open": lam_open}


def tension_share(lam, s0, lam_open):
    """The chords' tension as a share of the finished, at lambda (see take_up)."""
    if lam >= lam_open:
        return lam
    return s0 + (lam_open - s0) * lam / lam_open


LAMBDAS = tuple(np.linspace(0.0, 1.0, 101))


def lines(p, r, lambdas=LAMBDAS):
    """The hub's stabilising lines through the spin-up, as fixed-length tension-only lines in series
    with their chords (structure_model.hub; review of #18).

    A chord passes the hub at c = 1.1 h and bows away from the axis under its own spin load,
    b = rho w^2 c L^2 / (2 sigma): b goes as lambda / share (load over tension), nothing at rest,
    the finished bow from where the joints open. A line from the hub's surface to the chord's tangent
    point, cut to a fixed length, is stretched by whatever the chord's free position moves out, less
    what its pull draws the chord in: P = k_s (b + d0), k_s the line and chord in series (the chord's
    k = 2 T beta cot(beta L) at its current tension and spin), d0 the pull-in it is installed with at
    rest. d0 keeps every line taut at rest under a docking ship (TAUT_MARGIN x its swing). So a
    fixed line holds back the whole bow: at full spin it pulls ~k_s b, far above the finished
    sizing's service preload, and the line is sized for it (the area, its stiffness and the pull
    iterated). Alternative: lines paid out by the bow during the spin-up (winches), then locked."""
    res = evaluate(p, Design(radius_m=r, n_tori=1))
    g = res["geometry"]
    h = hub_model.compute(p, g, res["mass"])
    tu = take_up(p, r)
    om, sigma, rho = g["omega"], p.wire_stress_mpa * 1e6, p.steel_density
    net = h["net"]
    n = net["n_chords"]
    n_lines = hub_model.N_NETS * n
    mu_chord = rho * net["wire_area_uniform"] / hub_model.N_NETS
    gap_rest = net["tangent_radius"] - g["hub_radius"]           # no bow at rest
    dock = SHIP_MASS * SHIP_CLOSING / BUFFER
    swing_rest = 2 * dock / n_lines
    swing_full = h["service_swing"]
    mu = h["reduced_mass"]

    def k_chord(lam):
        share = tension_share(lam, tu["s0"], tu["lam_open"])
        return hub_model.chord_stiffness(share * h["tension"], net["half_length"], mu_chord, om * math.sqrt(lam))

    def bow(lam):
        share = tension_share(lam, tu["s0"], tu["lam_open"])
        return net["bow"] * lam / share

    def run(area):
        k_line = hub_model.E_WIRE * area / gap_rest
        ks = [hub_model.series(k_chord(x), k_line) for x in lambdas]
        d0 = hub_model.TAUT_MARGIN * swing_rest / ks[0]
        pull = [k * (bow(x) + d0) for k, x in zip(ks, lambdas)]
        return k_line, ks, d0, pull

    # Fixed lines at the finished sizing (hub.compute), installed snug at rest.
    _, ks_f, d0_f, pull_f = run(h["line_area"])
    as_sized = (pull_f[-1] + swing_full) / (h["line_area"] * sigma)
    # Sized for the bow they hold back.
    area = h["line_area"]
    for _ in range(100):
        k_line, ks, d0, pull = run(area)
        new = max(max(pull) + swing_full, max(pull[0] + swing_rest, 0.0)) / sigma
        if abs(new - area) <= 1e-9 * new:
            break
        area = max(new, h["line_area"])
    k_line, ks, d0, pull = run(area)
    K = [hub_model.N_NETS * n * k / 2 for k in ks]
    margins = [K[i] / (mu * om ** 2 * x) for i, x in enumerate(lambdas) if x > 0]
    kc_full = k_chord(1.0)
    return {
        "s0": tu["s0"], "lam_open": tu["lam_open"], "bow": net["bow"], "gap_rest": gap_rest,
        "gap_finished": h["gap"], "as_sized_ratio": as_sized, "area_finished": h["line_area"],
        "area": area, "pull_full": pull[-1], "pull_rest": pull[0], "d0": d0,
        "service_preload": h["service_preload"],
        "taut": min(pull) > max(swing_rest, 0.0),
        # The chord drawn in by the line at full spin: the window left around the hub.
        "pull_in_full": pull[-1] / kc_full, "gap_full": gap_rest + net["bow"] - pull[-1] / kc_full,
        "k_rest": K[0], "k_full": K[-1], "k_finished": h["k_torus"], "margin_min": min(margins),
        "margin_finished": h["margin"],
        "dock_offset": dock * h["torus_mass"] / (h["torus_mass"] + h["hub_mass"]) / K[0],
        "period_s": 2 * math.pi * math.sqrt(mu / K[0]),
        "mass": n_lines * area * gap_rest * rho, "mass_finished": h["line_mass"],
        # The lines pull the hub's shell outward all round each net's plane: a ring frame there carries
        # the hoop force N P / (2 pi), sized at the plate stress (tube_section's).
        "hub_ring_force": n * pull[-1] / (2 * math.pi),
        "hub_ring_mass": hub_model.N_NETS * 2 * math.pi * g["hub_radius"] * (n * pull[-1] / (2 * math.pi))
                         / (p.plate_stress_mpa * 1e6) * rho,
        "lambdas": list(lambdas), "pull": pull,
    }


# -- torque ------------------------------------------------------------------------------------------------
def torque(p, r, n_tori=6, days=FAST_SPINUP_DAYS):
    """The spin-up's angular acceleration and its loads, per torus, and the spin-up's cost."""
    from dynamics_model import axial_torsion as at
    res = evaluate(p, Design(radius_m=r, n_tori=n_tori))
    g, m = res["geometry"], res["mass"]
    om, h, rf = g["omega"], g["hub_radius"], g["farm_radius"]
    j_torus = m["rim"] * r ** 2 + m["spokes"] * (r ** 2 + h * h) / 3     # rim, and the chords spread to it
    j_hub = p.hub_factory_metal_frac * m["steel"] * h * h
    j_farm = (m["farm_total"] - m["farm_spokes"]) * rf ** 2 + m["farm_spokes"] * rf ** 2 / 3
    j_all = j_torus + j_hub + j_farm
    alpha = om / (days * 86400)
    tau = j_all * alpha
    # Each ring thrusts for itself; the farm ring's thrusters fail or lag: its torque through its radial
    # spokes, which resist a twist by their tension alone (geometric), T h r_f / L, at the spin's share
    # of it plus their pretension's.
    spokes = at.farm_spokes(g, m)
    k_farm_full = 2 * spokes["torsion"]                                   # two planes
    hub_lines = hub_model.compute(p, g, m)
    k_lines, _ = at.net_lacing(hub_lines, h, 0.002)
    tau_hub = (j_hub + j_farm) * alpha                                    # the hub and its farm ring via the lines
    n_laced = 0.002 * hub_lines["n_lines"]
    laced_force = tau_hub / (max(n_laced, 1.0) * h * math.sin(at.NET_LACING_ANGLE))
    # Cost: angular momentum delivered at the torus's outer rim.
    lever = g["envelope_outer"]
    momentum = j_all * om
    rows = {}
    for name, ve, eff in (("water thrusters", p.spinup_exhaust_km_s * 1e3, p.electrothermal_efficiency),
                          ("rock mass driver", ROCK_DRIVER_EXHAUST * 1e3, p.mass_driver_efficiency)):
        mp = momentum / (lever * ve)
        energy = 0.5 * mp * ve ** 2 / eff
        rows[name] = {"exhaust": ve, "propellant": mp, "energy": energy,
                      "days_at_power": energy / res["power"]["total"] / 86400}
    water = m["water_needed"]
    return {
        "j_torus": j_torus, "j_hub": j_hub, "j_farm": j_farm, "alpha": alpha, "torque": tau,
        "thrust": tau / lever, "power": res["power"]["total"],
        "rim_ratio": alpha / om ** 2,                       # tangential over centrifugal load, at full spin
        "euler_equals_spin_below": math.sqrt(alpha) / om,  # spin share below which alpha r > w^2 r
        "farm_torque": j_farm * alpha, "k_farm_full": k_farm_full,
        "hub_torque": tau_hub, "k_lines": k_lines, "hub_twist": tau_hub / k_lines,
        "laced_force": laced_force, "line_capacity": hub_lines["line_area"] * p.wire_stress_mpa * 1e6,
        "mismatch_torque": THRUST_MISMATCH * j_torus * alpha,
        "lattice_force": THRUST_MISMATCH * j_torus * alpha / (r - g["tube_radius"]),   # tangential, across a gap
        "options": rows, "momentum": momentum,
        "water": water, "water_spin_drop": water * r ** 2 / j_all,
        "omega": om, "farm_radius": rf,
    }


def farm_twist(t, share):
    """The farm ring's twist on its radial spokes at rest (their pretension, `share` of the finished
    tension) and at full spin, if it is turned by the hub rather than its own thrusters."""
    rest = t["farm_torque"] / (share * t["k_farm_full"])
    full = t["farm_torque"] / t["k_farm_full"]
    return {"rest": rest, "full": full, "rest_rim": rest * t["farm_radius"], "full_rim": full * t["farm_radius"]}


# -- the fill ----------------------------------------------------------------------------------------------
def fill(p, r, cell=None):
    """The rock jacket's and the fill's settling as the spin grows, placed loose or compacted at rest.

    The jacket's cells have a fixed volume. Filled loose to rho_loose, they hold only rho_loose /
    rho_final of the design's rock (review of #18): settling keeps that mass but can't restore it, so
    the shield is short by that share everywhere, until the cells are topped up (all of them, not
    only the sides) with the missing rock. Settling of loose fill: 1 - rho_loose / rho_final.
    Compacted to its final density as placed: the design's mass, settling only by its elastic
    compression under its own weight at full spin, rho g H^2 / (2 M) over a column H.

    The jacket's thickness lies along the radius on the floor and the ceiling, but at the tube's two
    sides it lies across it, and each cell's column runs along the radius, a cell high: a settled
    side cell also leaves a slot at its top through the jacket's whole thickness. Seen from the
    valley at its height, a slot h high through a wall t thick lets straight through about h / (4 t)
    of all directions (a band h / t of elevation over the wall's half of the azimuth)."""
    from radiation_model import reference
    res = evaluate(p, Design(radius_m=r, n_tori=1))
    g, m = res["geometry"], res["mass"]
    rho = p.rock_density * 1e3
    t = g["jacket"]
    cell = cell or p.cell_size_m
    accel = g["accel"]
    curve = "Lunar regolith (OLTARIS's)"
    design_dose = float(reference.table2(curve, p.shield_areal_t_m2))
    loose = {}
    for name, rho0 in zip(("low", "mid", "high"), LOOSE_DENSITY):
        strain = 1 - rho0 / p.rock_density
        slot = strain * cell
        areal = p.shield_areal_t_m2 * rho0 / p.rock_density
        loose[name] = {"density": rho0, "strain": strain, "floor_settle": strain * t, "slot": slot,
                       "open_share": slot / (4 * t), "areal": areal,
                       "jacket_dose": float(reference.table2(curve, areal)),
                       "top_up": strain * m["shield"]}
    compacted = {}
    for name, mod in zip(("stiff", "mid", "soft"), reversed(FILL_MODULUS)):
        slot = rho * accel * cell ** 2 / (2 * mod)
        compacted[name] = {"modulus": mod, "slot": slot, "open_share": slot / (4 * t),
                           "floor_settle": rho * accel * t ** 2 / (2 * mod), "areal": p.shield_areal_t_m2,
                           "jacket_dose": design_dose, "top_up": 0.0}
    for d in list(loose.values()) + list(compacted.values()):
        # Through the slots, both side walls at their height, against the jacket left around them.
        d["slot_dose"] = d["open_share"] * 2 * (reference.FREE_SPACE - d["jacket_dose"])
        d["dose"] = d["jacket_dose"] + d["slot_dose"]
    # Imbalance: the rock moves out by half its settlement; a share of that differs around the ring.
    mid = loose["mid"]
    shift = SETTLE_NONUNIFORM * mid["floor_settle"] / 2
    rock_share = m["shield"] / m["rim"]
    first_moment = rock_share * shift / 2                     # the first harmonic of a random variation (rough)
    ballast = p.ballast_frac * r
    porosity_final = 1 - p.rock_density / GRAIN_DENSITY
    return {"loose": loose, "compacted": compacted, "jacket": t, "cell": cell, "design_dose": design_dose,
            "porosity_final": porosity_final, "porosity_loose": [1 - d / GRAIN_DENSITY for d in LOOSE_DENSITY],
            "first_moment": first_moment, "ballast": ballast, "shield_mass": m["shield"],
            "spin_drop": 2 * rock_share * mid["floor_settle"] / 2 / r}
