"""The flexible spinning stack: whirl modes and passive stability (plan §4).

The stack spins at w about its axis z. Every part is axisymmetric and every connection the same
in all directions across the axis, so the lateral motion is written with complex coordinates
(x + i y for a displacement, the same for a slope dx/dz + i dy/dz) in the inertial frame:

    M q'' - i w G q' + K q = 0

with M the masses and transverse moments of inertia, G the polar moments of inertia (each
spinning part's gyroscopic coupling) and K the stiffness. Modes go as exp(i lambda t): lambda > 0
whirls forward (with the spin), lambda < 0 backward.

- The hub is a beam (Euler-Bernoulli, thin-walled tube of radius h and wall thickness t:
  EI = E pi h^3 t), its mass lumped at the nodes, spinning with the stack.
- Each torus is a rigid thin ring (mass m, J = m r^2, I_t = m r^2 / 2, as in §11), tied to the
  hub at its two net planes, a = +-(a + t) from its mid-plane, by the nets' lateral stiffness
  (structure_model.hub).
- Each farm ring is a rigid thin ring on its own spokes, radial, in two planes at its sides
  (like the tori's nets); each plane holds it laterally by its spokes' axial stiffness and
  tension (N/2 (EA + T)/L).
- The despun array is a point mass at the far end of the hub (it doesn't spin: no G).

Passive stability with energy dissipation (lakes, people, flexing structure): dissipation that
turns with the stack destabilises every forward whirl slower than the spin, so a stack stays
stable without control only if every forward mode whirls faster than the spin, lambda > w
(apart from the rigid motions: drift and precession, at lambda = 0). For a rigid stack the only
such mode is its nutation, at lambda = (J / I_t) w: the criterion is the maximum-axis rule of
§11, J > I_t. The ratio of the lowest forward mode to the spin is the flexible stack's margin,
the same measure as §11's inertia ratio (1.2 for a 20% margin). A damped solve (dissipation
proportional to stiffness, turning with the stack) checks it.

Forced and transient motion (disturbances.py): a load whirling at lambda in the inertial frame,
F exp(i lambda t), gives Q = (K - lambda^2 M + lambda w G)^-1 F; an impulse is followed through the
modes of the damped first-order system.

The hub's elements are Timoshenko beams (shear, kappa G A, by default), and its segment joints
rotational springs folded into an element's flexibility (build's joint_k). Axial and torsional
motion, which don't couple to the spin, are in axial_torsion.py.

Not modelled: the hub's joints to the dock and array mast, the elevator, pipe and power shafts.
"""

import math
from dataclasses import dataclass, field

import numpy as np

E = 200e9


@dataclass
class Body:
    """A rigid ring (or point mass) on the hub: mass, polar and transverse inertia, its centre's z,
    and its attachments to the hub (z, lateral stiffness)."""
    name: str
    mass: float
    polar: float
    transverse: float
    z: float
    springs: list = field(default_factory=list)


@dataclass
class Stack:
    hub_nodes: np.ndarray         # z of the hub's nodes
    hub_mass: np.ndarray          # lumped at the nodes
    hub_polar: np.ndarray
    hub_transverse: np.ndarray
    ei: float
    bodies: list
    omega: float
    point_masses: dict = field(default_factory=dict)   # node index -> mass (not spinning)
    links: list = field(default_factory=list)          # (body i, body j, lateral k, tilt k) between bodies
    ga: object = None              # shear stiffness kappa G A (float or per element); None: no shear
    hinges: dict = field(default_factory=dict)         # element index -> rotational stiffness of a joint at its first node

    def element_stiffness(self, e):
        """The hub element e's stiffness, from its flexibility as a cantilever from its first node:
        bending, shear (Timoshenko, when ga is set) and a joint's rotational spring k at its first
        node (relative rotation (P L + M) / k at the tip's lever arm L), K = B^T F^-1 B."""
        length = self.hub_nodes[e + 1] - self.hub_nodes[e]
        ei = self.ei
        ga = self.ga[e] if np.ndim(self.ga) else self.ga
        flex = np.array([[length ** 3 / (3 * ei), length ** 2 / (2 * ei)],
                         [length ** 2 / (2 * ei), length / ei]])
        if ga:
            flex[0, 0] += length / ga
        k_joint = self.hinges.get(e)
        if k_joint:
            flex += np.array([[length ** 2, length], [length, 1.0]]) / k_joint
        b = np.array([[-1.0, -length, 1.0, 0.0], [0.0, -1.0, 0.0, 1.0]])
        return b.T @ np.linalg.inv(flex) @ b

    def matrices(self):
        """M, G, K over the hub's (displacement, slope) per node, then each body's (displacement, slope)."""
        n = len(self.hub_nodes)
        size = 2 * n + 2 * len(self.bodies)
        m, g, k = np.zeros(size), np.zeros(size), np.zeros((size, size))
        m[0:2 * n:2] = self.hub_mass
        m[1:2 * n:2] = self.hub_transverse
        g[1:2 * n:2] = self.hub_polar
        for node, mass in self.point_masses.items():
            m[2 * node] += mass
        for e in range(n - 1):
            ke = self.element_stiffness(e)
            dofs = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
            k[np.ix_(dofs, dofs)] += ke
        for b, body in enumerate(self.bodies):
            i = 2 * n + 2 * b
            m[i], m[i + 1], g[i + 1] = body.mass, body.transverse, body.polar
        # The body's point at z moves by u_b + (z - z_b) beta_b; the hub's node by u_h.
        for _, _, stiffness, c in self.spring_vectors():
            k += stiffness * np.outer(c, c)
        for (i, j, k_lat, k_tilt), (c_lat, c_tilt) in zip(self.links, self.link_vectors()):
            k += k_lat * np.outer(c_lat, c_lat) + k_tilt * np.outer(c_tilt, c_tilt)
        return np.diag(m), np.diag(g), k

    def size(self):
        return 2 * len(self.hub_nodes) + 2 * len(self.bodies)

    def body_dof(self, b):
        """Index of body b's displacement (its slope is the next one)."""
        return 2 * len(self.hub_nodes) + 2 * b

    def link_vectors(self):
        """Per link, the vectors giving the relative displacement of the two bodies at the link's
        mid-plane and their relative tilt (c . q)."""
        out = []
        for i, j, _, _ in self.links:
            a, b = self.body_dof(i), self.body_dof(j)
            mid = (self.bodies[i].z + self.bodies[j].z) / 2
            c = np.zeros(self.size())
            c[a], c[a + 1], c[b], c[b + 1] = 1.0, mid - self.bodies[i].z, -1.0, -(mid - self.bodies[j].z)
            t = np.zeros(self.size())
            t[a + 1], t[b + 1] = 1.0, -1.0
            out.append((c, t))
        return out

    def spring_vectors(self):
        """Per body and attachment, (body, z, stiffness, vector giving the body's point at z less the
        hub's node there)."""
        out = []
        for b, body in enumerate(self.bodies):
            i = self.body_dof(b)
            for z, stiffness in body.springs:
                node = int(np.argmin(np.abs(self.hub_nodes - z)))
                c = np.zeros(self.size())
                c[i], c[i + 1], c[2 * node] = 1.0, z - body.z, -1.0
                out.append((b, z, stiffness, c))
        return out

    def response(self, lam, force):
        """Steady response Q to a load F exp(i lam t) (complex, per degree of freedom: forces on the
        displacements, moments on the slopes), whirling at lam in the inertial frame."""
        m, g, k = self.matrices()
        return np.linalg.solve(k - lam ** 2 * m + lam * self.omega * g, np.asarray(force, dtype=complex))

    def transient(self, velocity, times, damping=0.0):
        """Motion after an impulse: q(t) for the velocities `velocity` given at t = 0 (q = 0), the
        stack's free drift removed (its centre of mass held). Returns an array (time, dof)."""
        m, g, k = self.matrices()
        s = 1 / np.sqrt(np.diag(m))
        basis = self._basis(s)
        k_n, g_n = basis.T @ (k * np.outer(s, s)) @ basis, basis.T @ (g * np.outer(s, s)) @ basis
        d_n = damping / self.omega * k_n
        size = len(k_n)
        a = np.zeros((2 * size, 2 * size), dtype=complex)
        a[:size, size:] = np.eye(size)
        a[size:, :size] = k_n - 1j * self.omega * d_n
        a[size:, size:] = self.omega * g_n + 1j * d_n
        lam, vec = np.linalg.eig(a)
        # State (v, lambda v) = (v, -i v'), v the reduced mass-normalised coordinates (x = q / s).
        v_dot = basis.T @ (np.asarray(velocity, dtype=complex) / s)
        state0 = np.concatenate([np.zeros(size, dtype=complex), -1j * v_dot])
        coef = np.linalg.solve(vec, state0)
        phase = np.exp(1j * np.outer(np.asarray(times), lam))           # (time, mode)
        v = (phase * coef) @ vec[:size].T
        return (v @ basis.T) * s

    def _basis(self, s):
        drift = np.zeros(len(s))
        drift[self.displacements()] = 1 / s[self.displacements()]
        drift /= np.linalg.norm(drift)
        return np.linalg.svd(np.eye(len(s)) - np.outer(drift, drift))[0][:, :len(s) - 1]

    def modes(self, damping=0.0):
        """Whirl frequencies lambda (rad/s, inertial frame) and growth rates.

        damping: dissipation proportional to stiffness, D = damping K / w, turning with the stack
        (forces -D (q' - i w q) in the inertial frame)."""
        m, g, k = self.matrices()
        s = 1 / np.sqrt(np.diag(m))                       # mass-normalised coordinates
        k_n, g_n = k * np.outer(s, s), g * np.outer(s, s)
        # The stack drifts freely (a double zero): hold its centre of mass, the drift's direction in
        # mass-normalised coordinates being sqrt(m) on every displacement.
        basis = self._basis(s)
        k_n, g_n = basis.T @ k_n @ basis, basis.T @ g_n @ basis
        d_n = damping / self.omega * k_n
        size = len(k_n)
        # lambda^2 v - lambda (w G + i D) v - (K - i w D) v = 0, as a first-order system.
        a = np.zeros((2 * size, 2 * size), dtype=complex)
        a[:size, size:] = np.eye(size)
        a[size:, :size] = k_n - 1j * self.omega * d_n
        a[size:, size:] = self.omega * g_n + 1j * d_n
        lam = np.linalg.eigvals(a)
        return lam.real, -lam.imag          # frequency, growth rate (exp(i lambda t))

    def displacements(self):
        n = len(self.hub_nodes)
        return np.concatenate([np.arange(0, 2 * n, 2), 2 * n + 2 * np.arange(len(self.bodies))])

    def forward_ratio(self):
        """Lowest forward whirl over the spin, the rigid motions (lambda ~ 0) left out."""
        freq, _ = self.modes()
        forward = freq[freq > 1e-6 * self.omega]
        return float(forward.min() / self.omega)

    def rigid_ratio(self):
        """J / I_t of the whole stack taken as rigid, about its centre of mass (the §11 rule)."""
        masses = np.concatenate([self.hub_mass, [b.mass for b in self.bodies],
                                 list(self.point_masses.values())])
        zs = np.concatenate([self.hub_nodes, [b.z for b in self.bodies],
                             [self.hub_nodes[i] for i in self.point_masses]])
        zc = float((masses * zs).sum() / masses.sum())
        polar = self.hub_polar.sum() + sum(b.polar for b in self.bodies)
        transverse = (self.hub_transverse.sum() + sum(b.transverse for b in self.bodies)
                      + float((masses * (zs - zc) ** 2).sum()))
        return polar / transverse


def farm_ring_plane_stiffness(p, geo, mass):
    """Lateral stiffness of one of a farm ring's two planes of radial spokes: N/2 (EA + T)/L,
    with half the spokes' area and tension in each plane (radial spokes of length L)."""
    length = geo["farm_radius"] - geo["hub_radius"]
    area = mass["farm_spokes"] / (p.steel_density * length) / 2      # total spoke area per plane
    tension = (mass["farm_total"] - mass["farm_spokes"]) * geo["omega"] ** 2 * geo["farm_radius"] / 2
    return (E * area + tension) / (2 * length)


def tie_plane_stiffness(geo, torus_mass, tie_frac, density):
    """Radial ties from the hub to a torus's hub-facing side, in its two net planes: steel
    tie_frac of the torus's mass, stiff along their length (N/2 EA / L per plane). They carry no
    spin load, only the torus's centring."""
    length = geo["radius"] - 2 * geo["tube_radius"] - geo["jacket"] - geo["hub_radius"]
    area = tie_frac * torus_mass / (density * length) / 2
    return E * area / (2 * length), length


SHEAR_KAPPA = 0.5             # shear coefficient of a thin-walled circular tube
G = 77e9


def build(p, d, hub_shell_m=None, element=20.0, farm_planes=2, tie_frac=0.0, rim_link=None, link_tilt=None,
          shear=True, joint_k=None, links_skip=()):
    """The stack of design d: tori, their farm rings, the hub and the despun array.

    tie_frac: radial ties from the hub to each torus (share of its mass); rim_link: lateral
    stiffness of links between neighbouring tori's rims (N/m), None for none; link_tilt: their
    tilt stiffness (N m/rad), by default k r^2 / 2 (the links' spread around the rim).
    shear: the hub's shear flexibility (Timoshenko); joint_k: rotational stiffness (N m/rad) of
    joints in the hub between its segments, one at every gap between tori and farm rings, None for
    a continuous hub; links_skip: gaps (0 = between tori 1 and 2) left unlinked."""
    from habitat_model import evaluate
    from structure_model import hub as hub_model

    res = evaluate(p, d)
    geo, mass, power = res["geometry"], res["mass"], res["power"]
    n, r, h, w = d.n_tori, geo["radius"], geo["hub_radius"], geo["omega"]
    t = p.hub_shell_m if hub_shell_m is None else hub_shell_m
    nets = hub_model.compute(p, geo, mass)
    k_plane, offset = nets["k_plane"], nets["plane_offset"]
    k_farm = farm_ring_plane_stiffness(p, geo, mass)
    k_tie, tie_length = tie_plane_stiffness(geo, mass["total"], tie_frac, p.steel_density)

    pitch, fp = geo["pitch"], geo["farm_pitch"]
    length = geo["stack_length"]
    bodies, marks = [], [0.0, length]
    for k in range(n):
        z = (k + 0.5) * pitch
        m = mass["total"]
        planes = [(z - offset, k_plane + k_tie), (z + offset, k_plane + k_tie)]
        bodies.append(Body(f"torus {k + 1}", m, m * r * r, m * r * r / 2, z, planes))
        marks += [z - offset, z + offset]
    start = geo["main_length"] + geo["farm_section_gap"]
    half = geo["farm_width"] / 2
    for k in range(n):
        z = start + (k + 0.5) * fp
        m, rf = mass["farm_total"], geo["farm_radius"]
        planes = ([(z - half, k_farm), (z + half, k_farm)] if farm_planes == 2 else [(z, 2 * k_farm)])
        bodies.append(Body(f"farm ring {k + 1}", m, m * rf * rf, m * rf * rf / 2, z, planes))
        marks += [z for z, _ in planes]

    # Hub nodes at every attachment, and in between at most `element` apart.
    joints = []
    if joint_k:
        joints = [k * pitch for k in range(1, n)] + [geo["main_length"] + geo["farm_section_gap"] / 2]
        joints += [start + k * fp for k in range(1, n)]
        marks += joints
    marks = sorted(set(round(x, 6) for x in marks))
    nodes = [marks[0]]
    for a, b in zip(marks, marks[1:]):
        steps = max(1, math.ceil((b - a) / element))
        nodes += list(np.linspace(a, b, steps + 1)[1:])
    nodes = np.array(nodes)
    # Hub mass: the system model's hub, dock and factory metal, spread along it (at least its shell).
    share = p.hub_factory_metal_frac * mass["steel"] * n
    shell = 2 * math.pi * h * t * p.steel_density * length
    line = max(share, shell) / length
    tributary = np.diff(np.concatenate([[nodes[0]], (nodes[1:] + nodes[:-1]) / 2, [nodes[-1]]]))
    hub_mass = line * tributary
    hub_polar = hub_mass * h * h
    hub_transverse = hub_mass * (h * h / 2 + tributary ** 2 / 12)
    array = power["array_site"] * n * p.array_kg_m2
    links = []
    if rim_link:
        # Neighbouring tori joined at their rims, spread evenly around them: lateral k, and tilt
        # k r^2 / 2 about the link's mid-plane.
        tilt = rim_link * r * r / 2 if link_tilt is None else link_tilt
        links = [(i, i + 1, rim_link, tilt) for i in range(n - 1) if i not in links_skip]
    ga = SHEAR_KAPPA * G * 2 * math.pi * h * t if shear else None
    hinges = {int(np.argmin(np.abs(nodes[:-1] - z))): joint_k for z in joints}
    stack = Stack(nodes, hub_mass, hub_polar, hub_transverse, E * math.pi * h ** 3 * t, bodies, w,
                  {len(nodes) - 1: array}, links, ga, hinges)
    info = {"geometry": geo, "mass": mass, "nets": nets, "k_farm_plane": k_farm, "k_tie_plane": k_tie,
            "tie_length": tie_length, "tie_mass": tie_frac * mass["total"], "hub_line_mass": line,
            "hub_shell_mass": shell, "hub_share": share, "array_mass": array, "hub_shell_m": t,
            "joints": joints}
    return stack, info


def required(p, d, name, target=1.2, low=1e-6, high=1.0, **kw):
    """Smallest value of a build() argument (hub_shell_m, tie_frac, rim_link) giving a forward
    margin of `target`, by bisection on a log scale; None if `high` isn't enough."""
    def ratio(x):
        return build(p, d, **{**kw, name: x})[0].forward_ratio()
    if ratio(high) < target:
        return None
    if ratio(low) >= target:
        return low
    for _ in range(60):
        mid = math.sqrt(low * high)
        low, high = (low, mid) if ratio(mid) >= target else (mid, high)
        if high / low < 1.02:
            break
    return high


def required_shell(p, d, target=1.2, low=1e-4, high=1.0, **kw):
    """Thinnest hub wall (m) for the lowest forward whirl to reach `target` times the spin, or None."""
    def ratio(t):
        return build(p, d, hub_shell_m=t, **kw)[0].forward_ratio()
    if ratio(high) < target:
        return None
    if ratio(low) >= target:
        return low
    for _ in range(40):
        mid = math.sqrt(low * high)
        low, high = (low, mid) if ratio(mid) >= target else (mid, high)
        if high / low < 1.02:
            break
    return high
