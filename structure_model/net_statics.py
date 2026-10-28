"""Assembled statics of a ring, or of two opposite partial arcs, hung in the tangent-chord net.

Each chord is one elastic member with a single tension (its two ends sit at the same spin
radius, so the tension is the same at both ends). The rim is cut into rigid segments; the
segments of an arc are linked at their joints by springs along the rim (axial), across it
(shear) and, optionally, in bending. Their stiffness is given relative to one chord's:
"locked" joints are stiff in all three, "sliding" joints are compliant along the rim, as the
notes intend once the ring is closed ("joints only seal and carry shear"), so the hull
doesn't take the load in hoop tension. The rim's centrifugal load, and each chord's own,
are the external loads. Solving the displacement method (small displacements, in the
rotating frame) gives every chord's tension and every joint's forces; chords can't push, so
slack ones are removed and the system solved again. The residuals of each segment's force and
moment balance are reported as a check.

Left out: the change of centrifugal load as parts move (second order), the chords' sag
geometry (the across-chord self-load is applied at the ends), the hub and its stabilising
lines (the net floats free), and pre-tension.
"""

import math

import numpy as np

E_STEEL = 200e9


def _perp(v):
    return np.array([-v[1], v[0]])


def solve(radius, tangent_radius, line_mass, omega, chord_area, density, arc_length=None,
          segment_length=56.25, anchor_spacing=10.0, joints="locked", stress_pa=1e9, max_iter=50):
    """Two opposite arcs of arc_length each (None: the whole ring).

    Anchors every ~anchor_spacing metres, each carrying one chord of each handedness (as in
    cable_net.compute: as many chords as anchors). So that every chord ends on an anchor, the
    chord spans a whole number of anchor steps; the tangent circle is adjusted slightly to fit.
    """
    r = radius
    n_anchors = round(2 * math.pi * r / anchor_spacing)
    step = 2 * math.pi / n_anchors
    m_steps = round((math.pi - 2 * math.asin(tangent_radius / r)) / step)
    span = m_steps * step
    theta = (math.pi - span) / 2
    c = r * math.sin(theta)
    full = arc_length is None or arc_length >= math.pi * r
    alpha = math.pi if full else arc_length / r

    # Segments: arc A centred on phi = 0, arc B on phi = pi (each split into equal rigid pieces).
    n_per_arc = max(1, round(alpha * r / segment_length))
    seg_span = alpha / n_per_arc
    segs = []  # (start, end) angles
    for centre in (0.0, math.pi):
        start = centre - alpha / 2
        for i in range(n_per_arc):
            segs.append((start + i * seg_span, start + (i + 1) * seg_span))
    n = len(segs)
    refs = np.array([[r * math.cos((a + b) / 2), r * math.sin((a + b) / 2)] for a, b in segs])

    def seg_of(phi):
        phi = phi % (2 * math.pi)
        for k, (a, b) in enumerate(segs):
            lo, hi = a % (2 * math.pi), b % (2 * math.pi)
            inside = lo <= phi < hi if lo < hi else (phi >= lo or phi < hi)
            if inside:
                return k
        return None

    def point(phi):
        return np.array([r * math.cos(phi), r * math.sin(phi)])

    # Chords: anchor k to anchor k + m_steps (that chord is also anchor k + m's other-handed one).
    chords = []  # (seg_p, P, seg_q, Q)
    for k in range(n_anchors):
        phi = (k + 0.5) * step
        psi = phi + span
        sp, sq = seg_of(phi), seg_of(psi)
        if sp is not None and sq is not None:
            chords.append((sp, point(phi), sq, point(psi)))

    half_length = math.sqrt(r * r - c * c)
    k_chord = E_STEEL * chord_area / (2 * half_length)
    mu = density * chord_area

    K = np.zeros((3 * n, 3 * n))
    F = np.zeros(3 * n)

    def jac(seg, x):
        """Displacement of material point x on segment seg = J @ (ux, uy, rot)."""
        d = x - refs[seg]
        return np.array([[1.0, 0.0, -d[1]], [0.0, 1.0, d[0]]])

    def add_load(seg, x, f):
        J = jac(seg, x)
        F[3 * seg:3 * seg + 3] += J.T @ f

    # Rim load: lumped on 1 m pieces.
    for k, (a, b) in enumerate(segs):
        m = max(4, round((b - a) * r))
        for phi in np.linspace(a, b, m, endpoint=False) + (b - a) / m / 2:
            x = point(phi)
            add_load(k, x, line_mass * (b - a) * r / m * omega ** 2 * x)

    # Chords: axial springs between their two end points; their own centrifugal load to the ends.
    chord_dofs = []
    for sp, P, sq, Q in chords:
        e = (Q - P) / np.linalg.norm(Q - P)
        B = np.zeros(3 * n)
        B[3 * sq:3 * sq + 3] += e @ jac(sq, Q)
        B[3 * sp:3 * sp + 3] -= e @ jac(sp, P)
        K += k_chord * np.outer(B, B)
        chord_dofs.append(B)
        own = mu * 2 * half_length * omega ** 2 * (P + Q) / 2
        add_load(sp, P, own / 2)
        add_load(sq, Q, own / 2)

    # Joints between consecutive segments of the same arc (and across the seams of a full ring).
    stiff = 1e4 * k_chord
    axial_k, shear_k, bending = {
        "locked": (stiff, stiff, True),       # welded or bolted: carries tension, shear and moment
        "pinned": (stiff, stiff, False),      # carries tension and shear, no moment
        "sliding": (1e-6 * k_chord, stiff, False),   # free along the rim: shear only
    }[joints]
    pairs = []
    for arc in range(2):
        idx = list(range(arc * n_per_arc, (arc + 1) * n_per_arc))
        pairs += [(idx[i], idx[i + 1]) for i in range(len(idx) - 1)]
    if full:
        pairs += [(n_per_arc - 1, n_per_arc), (n - 1, 0)]
    joint_rows = []
    for a, b in pairs:
        phi = segs[a][1]
        J = point(phi)
        t = _perp(J / r)                  # along the rim
        nrm = J / r                       # radial
        Da = jac(a, J)
        Db = jac(b, J)
        rows = {}
        for name, vec, kk in (("axial", t, axial_k), ("shear", nrm, shear_k)):
            B = np.zeros(3 * n)
            B[3 * b:3 * b + 3] += vec @ Db
            B[3 * a:3 * a + 3] -= vec @ Da
            K += kk * np.outer(B, B)
            rows[name] = (B, kk)
        if bending:
            B = np.zeros(3 * n)
            B[3 * b + 2] += 1.0
            B[3 * a + 2] -= 1.0
            k_rot = stiff * segment_length ** 2
            K += k_rot * np.outer(B, B)
            rows["moment"] = (B, k_rot)
        joint_rows.append(((a, b), phi, rows))

    # The assembly floats free (no hub): tie it to the axis with springs far too weak to carry
    # anything, only to remove the three rigid-body modes the loads don't excite.
    K_ground = 1e-9 * k_chord * np.eye(3 * n)
    for k in range(n):
        K_ground[3 * k + 2, 3 * k + 2] *= r * r

    # Tension-only chords: drop the slack ones and solve again until none is in compression.
    active = np.ones(len(chords), dtype=bool)
    K_chords = [k_chord * np.outer(B, B) for B in chord_dofs]
    K_base = K.copy()
    for B, Kc in zip(chord_dofs, K_chords):
        K_base -= Kc
    for _ in range(max_iter):
        K = K_base + K_ground + sum(Kc for Kc, on in zip(K_chords, active) if on)
        u = np.linalg.solve(K, F)
        stretch = np.array([B @ u for B in chord_dofs])
        slack = active & (stretch < 0)
        if not slack.any():
            break
        active &= ~slack
    tensions = np.where(active, k_chord * stretch, 0.0)
    joint_forces = []
    for (a, b), phi, rows in joint_rows:
        # Positive axial: the joint pulled open (tension).
        joint_forces.append({name: k * (B @ u) for name, (B, k) in rows.items()} | {"phi": phi})

    # Residual check: each segment's balance of loads, chord pulls and joint forces.
    residual = F - (K - K_ground) @ u
    load_scale = line_mass * omega ** 2 * r * seg_span * r
    worst = 0.0
    for k in range(n):
        f = residual[3 * k:3 * k + 2]
        m = residual[3 * k + 2]
        worst = max(worst, np.linalg.norm(f) / load_scale, abs(m) / (load_scale * seg_span * r))

    stress = tensions / chord_area + density * omega ** 2 * half_length ** 2 / 2   # peak, at mid-chord
    peak = float(stress.max()) if len(stress) else 0.0
    axial = np.array([j["axial"] for j in joint_forces]) if joint_forces else np.zeros(0)
    return {
        "tangent_radius": c,
        "theta": theta,
        "equilibrium": worst < 1e-3,
        "n_segments": n,
        "n_chords": len(chords),
        "tensions": tensions,
        "slack_chords": int((~active).sum()),
        "tension_min": float(tensions.min()) if len(tensions) else 0.0,
        "tension_max": float(tensions.max()) if len(tensions) else 0.0,
        "joint_forces": joint_forces,
        "joint_axial_max": float(axial.max()) if len(axial) else 0.0,
        "joint_axial_min": float(axial.min()) if len(axial) else 0.0,
        "joint_shear_max": max((abs(j["shear"]) for j in joint_forces), default=0.0),
        "joint_moment_max": max((abs(j.get("moment", 0.0)) for j in joint_forces), default=0.0),
        "hoop_full_ring": line_mass * (omega * r) ** 2,
        "peak_stress": peak,
        # Stresses scale with spin^2 (rim and chord loads alike), so the stage stays within the
        # allowable up to this fraction of the final spin rate.
        "max_spin_fraction": math.sqrt(stress_pa / peak) if peak > 0 else math.inf,
        "residual": worst,
    }
