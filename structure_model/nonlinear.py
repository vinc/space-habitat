"""Geometrically nonlinear statics of a ring, or of partial arcs, hung in the tangent-chord net
(plan §2, the spin-up sequence).

The linear model (net_statics.py) cuts the rim into rigid segments and holds the geometry fixed;
stages with pinned or sliding joints came out as mechanisms or with rotations far too large for
it. Here, in the ring's plane and the rotating frame:

- the rim is a chain of flexible beams (corotational Euler-Bernoulli frames, one per anchor
  spacing), with the hull and frames' steel: E A, and E I = E A a^2 / 2 for a thin tube of the
  tube's radius a bending in the ring's plane;
- the segments are joined at joints (two nodes, penalty springs in the rim's tangent, normal and
  rotation): "locked" (all three), "pinned" (no rotation), "sliding" (no tangent, no rotation);
- each chord is one tension-only cable between its two anchors, with its geometric stiffness
  (T / L across it), pretensioned slightly so that the net is taut before the spin;
- loads follow the parts: the rim's centrifugal load m w^2 x at the current position, and each
  chord's own, lumped at its ends from its current mid-point; their load stiffness (-m w^2) is in
  the tangent;
- the assembly floats free: its centre of mass and mean rotation are held by multipliers (the
  stack turns about its centre of mass), whose reactions must stay ~0 for a balanced stage;
- the spin is stepped up as lambda = (w / w_final)^2, with Newton iterations at each step and
  the step cut when they fail. A stage is resolved up to the spin where equilibrium was last
  found; a mechanism shows as Newton failing at small steps, or as the displacements running off.

Several opposite or crossed pairs of arcs can be hung at once (arcs given as anchor ranges).
"""

import math

import numpy as np

E = 200e9
PRESTRAIN = 1e-4               # chords pretensioned to this strain before the spin
DIVERGED = 0.05                # displacement (share of the radius) taken as running off
RELEASED = 1e-9                # joint stiffness (share of locked) counted as fully released


class Model:
    def __init__(self, radius, tangent_radius, rim_line_mass, rim_ea, rim_ei, chord_area, density,
                 arcs=None, anchor_spacing=10.0, segment_anchors=6, joints="locked", n_anchors=None,
                 end_zone_factor=1.0, radial_lines=0.0, hub_radius=0.0, hub_mass=0.0, sliding_at=()):
        """arcs: list of (first anchor, number of anchors), anchors numbered 0..n-1 around the ring;
        None for the whole ring. Segments are `segment_anchors` anchors long, joined at joints."""
        r = radius
        n = n_anchors or 2 * round(math.pi * r / anchor_spacing)       # even, so arcs can be opposite
        self.n_anchors, self.r = n, r
        step = 2 * math.pi / n
        m_steps = round((math.pi - 2 * math.asin(tangent_radius / r)) / step)
        self.m_steps = m_steps
        self.theta = (math.pi - m_steps * step) / 2
        full = arcs is None
        if full:
            arcs = [(0, n)]
        self.full = full
        on = np.zeros(n, dtype=bool)
        for start, count in arcs:
            on[[(start + i) % n for i in range(count)]] = True
        self.on = on

        # Nodes: one per anchor on an arc (at its angle), plus a second node at every joint, so a joint
        # is a pair of nodes at the segment boundary. Rim elements join consecutive nodes of an arc.
        coords, mass, node_angle = [], [], []
        anchor_node = {}
        elements, joint_pairs = [], []
        lam = rim_line_mass
        for start, count in arcs:
            prev = None
            for i in range(count):
                k = (start + i) % n
                phi = (k + 0.5) * step
                if prev is not None and i % segment_anchors == 0:
                    # A joint halfway between the previous anchor and this one: two coincident nodes.
                    psi = (k) * step
                    a = len(coords)
                    coords.append([r * math.cos(psi), r * math.sin(psi)]); mass.append(0.0); node_angle.append(psi)
                    b = len(coords)
                    coords.append([r * math.cos(psi), r * math.sin(psi)]); mass.append(0.0); node_angle.append(psi)
                    elements.append((prev, a))
                    joint_pairs.append((a, b, psi))
                    prev = b
                idx = len(coords)
                coords.append([r * math.cos(phi), r * math.sin(phi)])
                mass.append(lam * r * step)
                node_angle.append(phi)
                anchor_node[k] = idx
                if prev is not None:
                    elements.append((prev, idx))
                prev = idx
            if full:
                # Close the ring: a joint between the last anchor and the first.
                psi = 0.0
                a = len(coords)
                coords.append([r, 0.0]); mass.append(0.0); node_angle.append(psi)
                b = len(coords)
                coords.append([r, 0.0]); mass.append(0.0); node_angle.append(psi)
                elements.append((prev, a))
                elements.append((b, anchor_node[start % n]))
                joint_pairs.append((a, b, psi))
        self.X = np.array(coords)
        self.mass = np.array(mass)
        self.elements = elements
        self.joints = joint_pairs
        self.anchor_node = anchor_node
        self.rim_ea, self.rim_ei = rim_ea, rim_ei

        # Chords: anchor k to anchor k + m (one per anchor, both ends on arcs).
        chords = []
        for k in range(n):
            q = (k + m_steps) % n
            if on[k] and on[q]:
                chords.append((anchor_node[k], anchor_node[q]))
        self.chords = chords
        # Single-laced anchors: only one of their two chords lands on an arc.
        laced = {k: int(on[(k + m_steps) % n]) + int(on[(k - m_steps) % n]) for k in range(n) if on[k]}
        single = {anchor_node[k] for k, c in laced.items() if c == 1}
        self.single_laced = len(single)
        factor = np.array([end_zone_factor if (i in single or j in single) else 1.0 for i, j in chords])
        self.chord_areas = chord_area * factor
        self.chord_eas = E * self.chord_areas
        self.chord_mus = density * self.chord_areas
        self.chord_l0 = np.array([np.linalg.norm(self.X[j] - self.X[i]) for i, j in chords]) / (1 + PRESTRAIN)
        self.chord_area = chord_area
        self.chord_mu = density * chord_area
        self.extra_cable_mass = float(((factor - 1) * chord_area * density * self.chord_l0).sum())
        # Temporary radial lines from the hub to the single-laced anchors.
        self.radials = []
        if radial_lines > 0:
            hub = len(coords)
            coords.append([0.0, 0.0]); mass.append(hub_mass); node_angle.append(0.0)
            self.X = np.array(coords)
            self.mass = np.array(mass)
            for node in sorted(single):
                l0 = (np.linalg.norm(self.X[node]) - hub_radius)
                self.radials.append((hub, node, l0 / (1 + PRESTRAIN), hub_radius))
            self.extra_cable_mass += len(self.radials) * radial_lines * chord_area * density * (r - hub_radius)
        self.radial_ea = E * radial_lines * chord_area

        # Joint stiffness: far stiffer than a rim element.
        le = r * step
        k_lin = 1e2 * max(rim_ea / le, 12 * rim_ei / le ** 3)
        k_rot = 1e2 * 4 * rim_ei / le
        self.k_joint = {
            "locked": (k_lin, k_lin, k_rot),
            "pinned": (k_lin, k_lin, 0.0),
            "sliding": (1e-9 * k_lin, k_lin, 0.0),
        }[joints]
        self.joint_type = joints
        self.sliding = np.zeros(len(joint_pairs), dtype=bool)
        for ang in sliding_at:
            gaps = [abs((psi - ang + math.pi) % (2 * math.pi) - math.pi) for _, _, psi in joint_pairs]
            self.sliding[int(np.argmin(gaps))] = True
        self.ndof = 3 * len(coords)

    # -- forces and tangent -----------------------------------------------------------------------
    def assemble(self, u, lam_w2):
        """Internal minus external force (residual) and tangent at displacements u, spin w^2."""
        nd = self.ndof
        R = np.zeros(nd)
        K = np.zeros((nd, nd))
        X = self.X
        x = X + np.column_stack([u[0::3], u[1::3]])
        th = u[2::3]
        out = {"N": [], "M": [], "T": []}
        # Rim beams.
        for (i, j) in self.elements:
            d0 = X[j] - X[i]
            l0 = np.linalg.norm(d0)
            b0 = math.atan2(d0[1], d0[0])
            d = x[j] - x[i]
            length = np.linalg.norm(d)
            beta = math.atan2(d[1], d[0])
            c, s = d / length
            alpha = (beta - b0 + math.pi) % (2 * math.pi) - math.pi
            t1, t2 = th[i] - alpha, th[j] - alpha
            ul = length - l0
            ea, ei = self.rim_ea, self.rim_ei
            n_f = ea * ul / l0
            m1 = ei / l0 * (4 * t1 + 2 * t2)
            m2 = ei / l0 * (2 * t1 + 4 * t2)
            rv = np.array([-c, -s, 0, c, s, 0])
            zv = np.array([s, -c, 0, -s, c, 0])
            B = np.vstack([rv, -zv / length + np.array([0, 0, 1, 0, 0, 0]),
                           -zv / length + np.array([0, 0, 0, 0, 0, 1])])
            D = np.array([[ea / l0, 0, 0], [0, 4 * ei / l0, 2 * ei / l0], [0, 2 * ei / l0, 4 * ei / l0]])
            f = B.T @ np.array([n_f, m1, m2])
            ke = B.T @ D @ B + n_f / length * np.outer(zv, zv) + (m1 + m2) / length ** 2 * (
                np.outer(rv, zv) + np.outer(zv, rv))
            dofs = [3 * i, 3 * i + 1, 3 * i + 2, 3 * j, 3 * j + 1, 3 * j + 2]
            R[dofs] += f
            K[np.ix_(dofs, dofs)] += ke
            out["N"].append(n_f)
            out["M"].append(max(abs(m1), abs(m2)))
        # Chords: tension-only cables with geometric stiffness; their own spin load at the ends.
        for c_idx, ((i, j), l0, ea, mu) in enumerate(zip(self.chords, self.chord_l0, self.chord_eas, self.chord_mus)):
            d = x[j] - x[i]
            length = np.linalg.norm(d)
            e = d / length
            stretch = length - l0
            t = ea / l0 * stretch if stretch > 0 else 0.0
            dofs = [3 * i, 3 * i + 1, 3 * j, 3 * j + 1]
            f = t * np.concatenate([-e, e])
            ev = np.concatenate([-e, e])
            zt = np.concatenate([[-e[1], e[0]], [e[1], -e[0]]])
            k_ax = ea / l0 if stretch > 0 else 0.0
            ke = k_ax * np.outer(ev, ev) + (t / length) * np.outer(zt, zt)
            R[dofs] += f
            K[np.ix_(dofs, dofs)] += ke
            # Own load: mu l0 w^2 (x_i + x_j) / 4 at each end (centroid at mid-chord).
            w = mu * l0 * lam_w2 / 4
            mid = x[i] + x[j]
            for node in (i, j):
                R[[3 * node, 3 * node + 1]] -= w * mid
                for other in (i, j):
                    K[np.ix_([3 * node, 3 * node + 1], [3 * other, 3 * other + 1])] -= w * np.eye(2)
            out["T"].append(t)
        # Temporary radial lines: hub node to anchor, length measured from the hub's surface.
        for hub, node, l0, h in self.radials:
            d = x[node] - x[hub]
            dist = np.linalg.norm(d)
            e = d / dist
            length = dist - h
            stretch = length - l0
            t = self.radial_ea / l0 * stretch if stretch > 0 else 0.0
            dofs = [3 * hub, 3 * hub + 1, 3 * node, 3 * node + 1]
            ev = np.concatenate([-e, e])
            zt = np.concatenate([[-e[1], e[0]], [e[1], -e[0]]])
            R[dofs] += t * ev
            k_ax = self.radial_ea / l0 if stretch > 0 else 0.0
            K[np.ix_(dofs, dofs)] += k_ax * np.outer(ev, ev) + (t / dist) * np.outer(zt, zt)
            out.setdefault("R", []).append(t)
        if self.radials:
            hub = self.radials[0][0]
            K[3 * hub + 2, 3 * hub + 2] += self.rim_ei / self.r      # the hub's rotation: no load, held
        # Joints: springs in the rim's tangent and normal at node a's current rotation, and rotation.
        out["J"] = []
        for (a, b, psi), slide in zip(self.joints, self.sliding):
            kt, kn, kr = self.k_joint
            if slide:
                kt, kr = 1e-9 * kn, 0.0
            ang = psi + th[a]
            nrm = np.array([math.cos(ang), math.sin(ang)])
            tan = np.array([-math.sin(ang), math.cos(ang)])
            d = x[b] - x[a]
            fa = np.zeros(2)
            for vec, k in ((tan, kt), (nrm, kn)):
                force = k * (d @ vec)
                R[[3 * b, 3 * b + 1]] += force * vec
                R[[3 * a, 3 * a + 1]] -= force * vec
                kk = k * np.outer(vec, vec)
                for p_, q_, sgn in ((b, b, 1), (a, a, 1), (a, b, -1), (b, a, -1)):
                    K[np.ix_([3 * p_, 3 * p_ + 1], [3 * q_, 3 * q_ + 1])] += sgn * kk
            moment = kr * (th[b] - th[a])
            R[3 * b + 2] += moment
            R[3 * a + 2] -= moment
            K[3 * b + 2, 3 * b + 2] += kr
            K[3 * a + 2, 3 * a + 2] += kr
            K[3 * a + 2, 3 * b + 2] -= kr
            K[3 * b + 2, 3 * a + 2] -= kr
            out["J"].append({"tension": kt * (d @ tan), "shear": kn * (d @ nrm), "moment": moment})
        # Rim's centrifugal load at current positions.
        for node, m in enumerate(self.mass):
            if m:
                R[[3 * node, 3 * node + 1]] -= m * lam_w2 * x[node]
                K[np.ix_([3 * node, 3 * node + 1], [3 * node, 3 * node + 1])] -= m * lam_w2 * np.eye(2)
        return R, K, out

    def constraints(self):
        """Hold the centre of mass (x, y) and the mean rotation about the axis."""
        C = np.zeros((3, self.ndof))
        for node, m in enumerate(self.mass):
            w = m if m else 0.0
            C[0, 3 * node] = w
            C[1, 3 * node + 1] = w
            C[2, 3 * node] = -w * self.X[node, 1]
            C[2, 3 * node + 1] = w * self.X[node, 0]
        return C

    def _newton(self, u, w2, C, load_ref, tol=1e-5, max_iter=40):
        """Newton iterations from u at spin w^2: the equilibrium, or None if they fail."""
        trial = u.copy()
        for _ in range(max_iter):
            R, K, out = self.assemble(trial, w2)
            A = np.block([[K, C.T], [C, np.zeros((3, 3))]])
            rhs = -np.concatenate([R, C @ trial])
            try:
                sol = np.linalg.solve(A, rhs)
            except np.linalg.LinAlgError:
                return None
            du = sol[:self.ndof]
            # Backtrack while the out-of-balance force grows (a step overshooting a soft mode).
            base = np.linalg.norm(R)
            alpha = 1.0
            for _ in range(8):
                R_try, _, _ = self.assemble(trial + alpha * du, w2)
                lagr = C.T @ sol[self.ndof:]
                if np.linalg.norm(R_try + lagr) <= max(base, 1e-12) * 1.5 or alpha < 0.01:
                    break
                alpha /= 2
            du = alpha * du
            trial += du
            if not np.all(np.isfinite(trial)):
                return None
            if np.abs(du[0::3]).max() > DIVERGED * self.r or np.abs(du[1::3]).max() > DIVERGED * self.r:
                return None
            # Converged: the step negligible and the out-of-balance force small next to a node's load
            # (round-off sets the floor, the joints' penalty stiffness being large).
            if np.abs(du).max() < 1e-9 * self.r and \
                    np.linalg.norm(R + C.T @ sol[self.ndof:]) < tol * load_ref * math.sqrt(self.ndof):
                if np.hypot(trial[0::3], trial[1::3]).max() > DIVERGED * self.r:
                    return None
                return trial
        return None

    def _setup(self, omega):
        C = self.constraints()
        C = C / np.abs(C).max(axis=1)[:, None]
        return C, self.mass.max() * omega ** 2 * self.r

    def solve(self, omega, target=1.0, steps=10, min_step=1e-4):
        """Step the spin up to `target` of omega (as lambda = fraction^2) and return the last
        equilibrium found, with how far it got."""
        C, load_ref = self._setup(omega)
        u = np.zeros(self.ndof)
        lam_done, step = 0.0, 1.0 / steps
        lam_target = target ** 2
        found = None
        while lam_done < lam_target - 1e-12:
            lam = min(lam_target, lam_done + step)
            trial = self._newton(u, lam * omega ** 2, C, load_ref)
            if trial is None:
                step /= 2
                if step < min_step:
                    break
                continue
            u, lam_done = trial, lam
            found = u.copy()
            step = min(step * 1.5, 0.25)
        if found is None:
            return {"reached": 0.0, "resolved": False}
        return self.report(found, lam_done, omega, lam_done >= lam_target - 1e-9)

    def peak_stress(self, tensions, omega_now):
        """Largest chord stress: tension over area plus the chord's own spin load at mid-chord."""
        length = float(self.chord_l0.mean()) * (1 + PRESTRAIN)
        self_load = self.chord_mu / self.chord_area * omega_now ** 2 * (length / 2) ** 2 / 2
        return (float((tensions / self.chord_areas).max()) if len(tensions) else 0.0) + self_load

    def spin_limit(self, omega, sigma, steps=8):
        """Largest share of the spin at which every chord stays within sigma (the stage held with its
        joints as they are), by continuation and interpolation; with the equilibrium there."""
        C, load_ref = self._setup(omega)
        u = np.zeros(self.ndof)
        prev = (0.0, 0.0)
        lam, step = 0.0, 1.0 / steps
        while lam < 1.0 - 1e-12:
            nxt = min(1.0, lam + step)
            trial = self._newton(u, nxt * omega ** 2, C, load_ref)
            if trial is None:
                step /= 2
                if step < 1e-4:
                    return {"limit": math.sqrt(lam), "by": "equilibrium lost", "state": self.report(u, lam, omega, False)}
                continue
            _, _, out = self.assemble(trial, nxt * omega ** 2)
            stress = self.peak_stress(np.array(out["T"]), math.sqrt(nxt) * omega)
            if stress >= sigma:
                # Interpolate in lambda between the last two states (stress ~ linear in lambda).
                l0, s0 = prev
                lam_c = l0 + (sigma - s0) / (stress - s0) * (nxt - l0)
                trial_c = self._newton(u, lam_c * omega ** 2, C, load_ref) if lam_c > lam else u
                if trial_c is None:
                    trial_c, lam_c = u, lam
                return {"limit": math.sqrt(lam_c), "by": "chord stress", "state": self.report(trial_c, lam_c, omega, True)}
            u, lam, prev = trial, nxt, (nxt, stress)
        return {"limit": 1.0, "by": "full spin", "state": self.report(u, 1.0, omega, True)}

    def release(self, omega, target, to="pinned", factors=(1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-9)):
        """Hang the arcs at `target` of the spin with locked joints, then release them towards `to`
        (pinned: no moment; sliding: no moment and nothing along the rim) step by step, each from
        the last equilibrium. If equilibrium is lost on the way, the released stage is a mechanism
        at that spin (none exists without the stiffness last removed). Released fully means down to
        RELEASED of the locked stiffness (exactly zero is singular: a sliding joint has no stiffness
        along the rim at all)."""
        first = self.solve(omega, target)
        if not first["resolved"]:
            return {"released": 0.0, "resolved": False, "locked": first}
        C, load_ref = self._setup(omega)
        u = first["u"]
        kt0, kn0, kr0 = self.k_joint
        last, released = first, None
        w2 = target ** 2 * omega ** 2
        for f in factors:
            self.k_joint = (kt0 * (f if to == "sliding" else 1.0), kn0, kr0 * f)
            trial = self._newton(u, w2, C, load_ref, max_iter=80)
            if trial is None:
                break
            u, released = trial, f
            last = self.report(u, target ** 2, omega, True)
        self.k_joint = (kt0, kn0, kr0)
        out = dict(last)
        out.update({"released": released, "resolved": released is not None and released <= RELEASED,
                    "locked": first})
        return out

    def report(self, u, lam, omega, resolved):
        R, K, out = self.assemble(u, lam * omega ** 2)
        T = np.array(out["T"])
        return {
            "reached": math.sqrt(lam), "resolved": resolved, "u": u,
            "tensions": T, "tension_max": float(T.max()) if len(T) else 0.0,
            "stress_max": float((T / self.chord_areas).max()) if len(T) else 0.0,
            "tension_min": float(T.min()) if len(T) else 0.0, "slack": int((T <= 0).sum()),
            "rim_tension_max": float(max(out["N"])) if out["N"] else 0.0,
            "rim_compression_max": float(-min(out["N"])) if out["N"] else 0.0,
            "rim_moment_max": float(max(out["M"])) if out["M"] else 0.0,
            "joint_tension_max": float(max((j["tension"] for j in out["J"]), default=0.0)),
            "joint_moment_max": float(max((abs(j["moment"]) for j in out["J"]), default=0.0)),
            "rotation_max": float(np.abs(u[2::3]).max()),
            "displacement_max": self._relative(u),
        }

    def _relative(self, u):
        """Largest displacement after the assembly's best-fit rigid motion is removed."""
        G = np.zeros((self.ndof, 3))
        for k in range(len(self.X)):
            x, y = self.X[k]
            G[3 * k] = [1.0, 0.0, -y]
            G[3 * k + 1] = [0.0, 1.0, x]
        coeffs, *_ = np.linalg.lstsq(G[np.r_[0:self.ndof:3, 1:self.ndof:3]],
                                     u[np.r_[0:self.ndof:3, 1:self.ndof:3]], rcond=None)
        rel = u - G @ coeffs
        return float(np.hypot(rel[0::3], rel[1::3]).max())


def for_design(p, r, arcs_fn=None, joints="locked", radial_lines=0.0, **kw):
    """A Model for the torus of radius r from the system model: rim mass, hull and frames, net."""
    from habitat_model import Design, evaluate
    from . import cable_net
    res = evaluate(p, Design(radius_m=r, n_tori=1))
    g, m = res["geometry"], res["mass"]
    sigma = p.wire_stress_mpa * 1e6
    net = cable_net.compute(r, m["rim"], g["omega"], g["hub_radius"], sigma, p.steel_density)
    lam = m["rim"] / (2 * math.pi * r)
    steel_area = m["hull_frames"] / (2 * math.pi * r * p.steel_density)
    a = g["tube_radius"]
    n = 2 * round(math.pi * r / net["anchor_spacing"])
    segment = max(1, round(g["width"] / (2 * math.pi * r / n)))
    arcs = arcs_fn(n, net) if arcs_fn else None
    model = Model(r, net["tangent_radius"], lam, E * steel_area, E * steel_area * a * a / 2,
                  net["wire_area_uniform"], p.steel_density, arcs=arcs, anchor_spacing=net["anchor_spacing"],
                  segment_anchors=segment, joints=joints, n_anchors=n, radial_lines=radial_lines,
                  hub_radius=g["hub_radius"], hub_mass=p.hub_factory_metal_frac * m["steel"], **kw)
    return model, {"geometry": g, "mass": m, "net": net, "sigma": sigma, "line_mass": lam,
                   "steel_area": steel_area}


def opposite_pairs(n, count, pairs=1):
    """Arcs of `count` anchors in `pairs` opposite pairs spread evenly around the ring (two pairs:
    at right angles)."""
    arcs = []
    for k in range(pairs):
        centre = k * n // (2 * pairs)
        start = centre - count // 2
        arcs += [(start % n, count), ((start + n // 2) % n, count)]
    return arcs
