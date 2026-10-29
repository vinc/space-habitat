"""The tube's cross-section by finite elements (plan §2.1): the steel that carries the rim to the chords.

One metre of tube, in the plane of its cross-section: x points away from the spin axis (spin
gravity w^2 x), y along it. The tube's centre is at x = R; an angle phi around it is 0 on the
floor side (away from the axis) and 180° on the hub-facing side.

- The pressure hull (radius a) and the outer cell wall (radius a + t, the jacket's outer face,
  behind the crawl space and the bumper) are membrane skins: bars, one per element edge.
- The jacket's transverse bulkheads, one every `cell_size_m` along the tube, are smeared into a
  plane-stress annulus between the two skins; their steel per metre of tube is its thickness.
  These are the frames: with the skins they make a ring girder ~5.5 m deep.
- Loads: spin gravity on the rock (resting on the outer wall on the floor side, on the hull on the
  hub-facing side), on the valley's fill, lakes and air (on the floor half of the hull), on the
  bumper and on the steel itself; the air pressure on the hull.
- Supports: the chords' anchors at chosen angles, each a fitting through the jacket's depth that
  holds the radial line of nodes at its angle along x, pinned at the chord's attachment on the
  outer wall: it may turn about that point, so it passes on a force but no couple. A chord sized at the working stress stretches by sigma L / E whatever its load, so all the
  anchors move together and fixed supports are exact. Anchors that would push are released.

The sizing is fully stressed: each skin element and each bulkhead element is resized until its
von Mises stress reaches the working stress at every integration point, or held at its minimum
gauge. Thin plates in compression buckle long before that, so compression is allowed only half the
working stress, blended with tension by the compression's share of the stress state (pure shear
gets three quarters): an allowance for stiffeners rather than a buckling analysis. The skins also carry
the hull's lengthwise pressure load (p a / 2) and the pillowing of their panels between bulkheads
and cell walls. Where the rock presses on the hull against the air (a vaulted ceiling), the hull's
panels need stiffeners; hung cell floors (the alternative, notes §5e) are membranes instead.

Not modelled: buckling of the parts in compression (the hub-facing half), segment joints and
their seals, the torus's curvature (a/R = 1/31) beyond the loads, local details around the
anchors, and the valley's buildings, light box and ceiling.
"""

import math
from dataclasses import dataclass

import numpy as np

E = 200e9
NU = 0.3
PANEL_SAG = 0.1           # sag / span of skin panels pillowing between bulkheads and cell walls
STIFFENER_DEPTH = 1.0     # m, stiffeners of hull panels pressed inward by the rock (vaulted ceiling)
COMPRESSION_KNOCKDOWN = 0.5   # working stress allowed in compression, as a share of the tension one
ANCHORS = {
    "crest": (180,),                                  # one line of anchors on the hub-facing crest
    "sides": (90, 270),                               # two lines, at the tube's sides
    "fan": (90, 120, 150, 180, 210, 240, 270),        # seven lines over the hub-facing half
}
CEILINGS = ("vaulted", "hung")


@dataclass(frozen=True)
class Inputs:
    radius: float          # floor radius r
    centre: float          # R = r - a
    a: float               # tube radius
    jacket: float          # rock jacket thickness t
    crawl: float           # crawl space
    omega: float
    rock_density: float    # kg/m3
    floor_scale: float     # rock left on the floor side after the fill credit (share)
    floor_mass: float      # fill, lakes and air, kg per m of tube
    pressure: float        # Pa
    sigma: float           # working stress, Pa
    steel_density: float
    skin_min: float
    wall_min: float
    cell: float
    bumper: float


def inputs(p, d, geo, mass):
    """The section's inputs from the system model's assumptions and results."""
    a, t, centre = geo["tube_radius"], geo["jacket"], geo["radius"] - geo["tube_radius"]
    rho = p.rock_density * 1e3
    # The fill credit thins the floor side's rock (mass.py); spread over the floor half here.
    outer_half = math.pi ** 2 * (centre + 4 * ((a + t) ** 3 - a ** 3) / (3 * math.pi * ((a + t) ** 2 - a ** 2))) \
        * ((a + t) ** 2 - a ** 2) * rho
    per_metre = 2 * math.pi * centre
    return Inputs(
        radius=geo["radius"], centre=centre, a=a, jacket=t, crawl=p.crawl_space_m, omega=geo["omega"],
        rock_density=rho, floor_scale=1 - mass["fill_credit"] / outer_half,
        floor_mass=(mass["fill"] + mass["water_lakes"] + mass["air"]) / per_metre,
        pressure=p.pressure_kpa * 1e3, sigma=p.plate_stress_mpa * 1e6, steel_density=p.steel_density,
        skin_min=p.skin_min_gauge_m, wall_min=p.cell_wall_min_gauge_m, cell=p.cell_size_m, bumper=p.bumper_m)


# --- Mesh and elements ------------------------------------------------------

class Mesh:
    def __init__(self, inp, n_radial=4, n_around=144):
        assert n_around % 12 == 0
        self.nr, self.nt = n_radial, n_around
        rho = inp.a + inp.jacket * np.arange(n_radial + 1) / n_radial
        phi = 2 * math.pi * np.arange(n_around) / n_around
        self.phi = phi
        rr, pp = np.meshgrid(rho, phi, indexing="ij")
        self.xy = np.stack([inp.centre + rr * np.cos(pp), rr * np.sin(pp)], axis=-1).reshape(-1, 2)
        self.n_nodes = len(self.xy)
        nid = np.arange(self.n_nodes).reshape(n_radial + 1, n_around)
        nxt = np.roll(nid, -1, axis=1)
        # Counter-clockwise quads: (i, j), (i+1, j), (i+1, j+1), (i, j+1).
        self.quads = np.stack([nid[:-1], nid[1:], nxt[1:], nxt[:-1]], axis=-1).reshape(-1, 4)
        self.quad_phi = np.repeat((phi + math.pi / n_around)[None, :], n_radial, axis=0).reshape(-1)
        self.hull = np.stack([nid[0], nxt[0]], axis=-1)            # edges j -> j+1
        self.outer = np.stack([nid[-1], nxt[-1]], axis=-1)
        self.hull_nodes, self.outer_nodes = nid[0], nid[-1]
        self.symmetry_nodes = np.concatenate([nid[:, 0], nid[:, n_around // 2]])
        self.columns = nid.T                                       # nodes through the jacket, per angle

    def column_at(self, degrees):
        return int(round(degrees / 360 * self.nt)) % self.nt


def allowance(s1, s2):
    """Share of the working stress allowed for principal stresses s1, s2 (or forces per unit length):
    1 in pure tension, COMPRESSION_KNOCKDOWN in pure compression, and in between in proportion to the
    compression's share of the stress state (pure shear: halfway). Continuous, so the sizing settles."""
    compression = np.maximum(0, -s1) + np.maximum(0, -s2)
    total = np.abs(s1) + np.abs(s2)
    share = np.divide(compression, total, out=np.zeros_like(total, dtype=float), where=total > 0)
    return 1 - (1 - COMPRESSION_KNOCKDOWN) * share


def _plane_stress(nu=NU):
    return E / (1 - nu * nu) * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])


def _shape_gradients(xi, eta):
    return 0.25 * np.array([[-(1 - eta), -(1 - xi)], [(1 - eta), -(1 + xi)],
                            [(1 + eta), (1 + xi)], [-(1 + eta), (1 - xi)]])


def _b_matrix(coords, xi, eta):
    """Strain-displacement matrices (n, 3, 8) and Jacobian determinants at (xi, eta)."""
    dn = _shape_gradients(xi, eta)                       # (4, 2)
    jac = np.einsum("ka,nkb->nab", dn, coords)           # d(x, y)/d(xi, eta): (n, 2, 2)
    det = np.linalg.det(jac)
    dndx = np.einsum("ka,nba->nkb", dn, np.linalg.inv(jac))   # (n, 4, 2)
    b = np.zeros((len(coords), 3, 8))
    b[:, 0, 0::2] = dndx[:, :, 0]
    b[:, 1, 1::2] = dndx[:, :, 1]
    b[:, 2, 0::2] = dndx[:, :, 1]
    b[:, 2, 1::2] = dndx[:, :, 0]
    return b, det


def quad_unit_stiffness(coords):
    """Q4 plane-stress stiffness per unit thickness, 2 x 2 Gauss points: (n, 8, 8)."""
    d = _plane_stress()
    k = np.zeros((len(coords), 8, 8))
    g = 1 / math.sqrt(3)
    for xi in (-g, g):
        for eta in (-g, g):
            b, det = _b_matrix(coords, xi, eta)
            k += np.einsum("nia,ij,njb->nab", b, d, b) * np.abs(det)[:, None, None]
    return k


def quad_areas(coords):
    x, y = coords[..., 0], coords[..., 1]
    return 0.5 * np.abs(x[:, 0] * y[:, 1] - x[:, 1] * y[:, 0] + x[:, 1] * y[:, 2] - x[:, 2] * y[:, 1]
                        + x[:, 2] * y[:, 3] - x[:, 3] * y[:, 2] + x[:, 3] * y[:, 0] - x[:, 0] * y[:, 3])


def bar_unit_stiffness(coords):
    """Bars per unit area: (n, 4, 4), with their directions and lengths."""
    vec = coords[:, 1] - coords[:, 0]
    length = np.linalg.norm(vec, axis=1)
    e = vec / length[:, None]
    ee = np.einsum("na,nb->nab", e, e)
    k = np.zeros((len(coords), 4, 4))
    k[:, :2, :2], k[:, 2:, 2:], k[:, :2, 2:], k[:, 2:, :2] = ee, ee, -ee, -ee
    return E * k / length[:, None, None], e, length


def _dofs(elements):
    return np.stack([2 * elements, 2 * elements + 1], axis=-1).reshape(len(elements), -1)


# --- Solution ---------------------------------------------------------------

class Model:
    def __init__(self, inp, anchors="sides", ceiling="vaulted", n_radial=4, n_around=144):
        if ceiling not in CEILINGS:
            raise ValueError(f"ceiling must be one of {CEILINGS}")
        self.inp, self.ceiling = inp, ceiling
        self.angles = ANCHORS[anchors] if isinstance(anchors, str) else tuple(anchors)
        m = self.mesh = Mesh(inp, n_radial, n_around)
        self.qc = m.xy[m.quads]
        self.kq = quad_unit_stiffness(self.qc)
        g = 1 / math.sqrt(3)
        self.bg = np.stack([_b_matrix(self.qc, xi, eta)[0] for xi in (-g, g) for eta in (-g, g)])  # (4, n, 3, 8)
        self.qarea = quad_areas(self.qc)
        self.qx = self.qc[..., 0].mean(axis=1)
        self.kh, self.eh, self.lh = bar_unit_stiffness(m.xy[m.hull])
        self.ko, self.eo, self.lo = bar_unit_stiffness(m.xy[m.outer])
        self.hx = m.xy[m.hull][..., 0].mean(axis=1)
        self.ox = m.xy[m.outer][..., 0].mean(axis=1)
        self.qdofs, self.hdofs, self.odofs = _dofs(m.quads), _dofs(m.hull), _dofs(m.outer)
        self.n_dofs = 2 * m.n_nodes
        self._fixed_loads()

    # Loads that don't depend on the steel.
    def _fixed_loads(self):
        inp, m = self.inp, self.mesh
        w2 = inp.omega ** 2
        f = np.zeros(self.n_dofs)
        # Rock: each element's weight goes to the wall it rests on.
        cos = np.cos(m.quad_phi)
        rock = inp.rock_density * self.qarea * self.qx / inp.centre * np.where(cos >= 0, inp.floor_scale, 1.0)
        force = rock * w2 * self.qx
        floor_side = cos >= 0
        on_outer = floor_side | (self.ceiling == "hung")
        # Onto the two wall nodes of each element's column (j, j+1): the outer wall's or the hull's.
        col = np.arange(len(m.quads)) % m.nt
        for wall, mask in ((m.outer_nodes, on_outer), (m.hull_nodes, ~on_outer)):
            for pair in (col, (col + 1) % m.nt):
                np.add.at(f, 2 * wall[pair[mask]], force[mask] / 2)
        # Fill, lakes and air on the floor half of the hull, by projected width.
        hx, hy = m.xy[m.hull_nodes, 0], m.xy[m.hull_nodes, 1]
        width = np.abs(np.roll(hy, -1) - np.roll(hy, 1)) / 2
        width = np.where(hx >= inp.centre, width, 0.0)
        np.add.at(f, 2 * m.hull_nodes, inp.floor_mass * width / width.sum() * w2 * hx)
        # Air pressure on the hull, outward from the tube's centre.
        normal = np.stack([self.eh[:, 1], -self.eh[:, 0]], axis=1)      # right of j -> j+1 (ccw): outward
        pf = inp.pressure * self.lh[:, None] * normal
        for k in (0, 1):
            np.add.at(f, 2 * m.hull[:, k], pf[:, 0] / 2)
            np.add.at(f, 2 * m.hull[:, k] + 1, pf[:, 1] / 2)
        # Bumper, on standoffs from the outer wall.
        scale = (inp.a + inp.jacket + inp.crawl) / (inp.a + inp.jacket)
        bumper = inp.bumper * inp.steel_density * self.lo * scale * self.ox / inp.centre * w2 * self.ox
        for k in (0, 1):
            np.add.at(f, 2 * m.outer[:, k], bumper / 2)
        self.f_fixed = f
        self.rock_load = float(force.sum())
        self.bumper_mass = float((inp.bumper * inp.steel_density * self.lo * scale * self.ox / inp.centre).sum())

    def _steel_loads(self, t_hull, t_outer, tau, extra_hull):
        m, w2, rho = self.mesh, self.inp.omega ** 2, self.inp.steel_density
        f = np.zeros(self.n_dofs)
        for edges, t, length, x in ((m.hull, t_hull + extra_hull, self.lh, self.hx), (m.outer, t_outer, self.lo, self.ox)):
            load = t * length * rho * x / self.inp.centre * w2 * x
            for k in (0, 1):
                np.add.at(f, 2 * edges[:, k], load / 2)
        load = tau * self.qarea * rho * self.qx / self.inp.centre * w2 * self.qx
        for k in range(4):
            np.add.at(f, 2 * m.quads[:, k], load / 4)
        return f

    def _stiffness(self, t_hull, t_outer, tau):
        k = np.zeros((self.n_dofs, self.n_dofs))
        for dofs, ke in ((self.qdofs, self.kq * tau[:, None, None]), (self.hdofs, self.kh * t_hull[:, None, None]),
                         (self.odofs, self.ko * t_outer[:, None, None])):
            np.add.at(k, (dofs[:, :, None], dofs[:, None, :]), ke)
        return k

    def solve(self, t_hull, t_outer, tau, extra_hull=0.0):
        """Displacements, forces and reactions for given sizes; anchors that would push are released."""
        m = self.mesh
        k = self._stiffness(t_hull, t_outer, tau)
        f = self.f_fixed + self._steel_loads(t_hull, t_outer, tau, extra_hull)
        # Each anchor is a fitting through the jacket's depth, spreading the chord's pull over the
        # radial line of nodes at its angle (a single node would be a point load, with stresses
        # growing without bound as the plate around it is thickened). The chord can only pull along
        # its line, at its attachment on the outer wall: the fitting is pinned there, so it holds the
        # line's x displacements to a rotation about that point (u_x = -theta (y - y_attach)), with
        # theta free. Lagrange multipliers carry the constraints; a fitting that would push is released.
        anchors = [m.column_at(a) for a in self.angles]
        free = np.setdiff1d(np.arange(self.n_dofs), 2 * m.symmetry_nodes + 1)
        index = np.full(self.n_dofs, -1)
        index[free] = np.arange(len(free))
        kff = k[np.ix_(free, free)]
        while True:
            rows, n_theta = [], 0
            for j in anchors:
                column = m.columns[j]
                arm = m.xy[column, 1] - m.xy[column[-1], 1]
                theta = n_theta if np.abs(arm).max() > 1e-9 else None   # a line along x can't turn the pull
                n_theta += theta is not None
                rows += [(index[2 * node], theta, a) for node, a in zip(column, arm)]
            n, size = len(free), len(free) + n_theta + len(rows)
            a_mat = np.zeros((size, size))
            a_mat[:n, :n] = kff
            rhs = np.zeros(size)
            rhs[:n] = f[free]
            for r, (dof, theta, arm) in enumerate(rows):
                i = n + n_theta + r
                a_mat[i, dof] = a_mat[dof, i] = 1.0
                if theta is not None:
                    a_mat[i, n + theta] = a_mat[n + theta, i] = arm
            x = np.linalg.solve(a_mat, rhs)
            u = np.zeros(self.n_dofs)
            u[free] = x[:n]
            reaction = k @ u - f
            pull = {j: -float(reaction[2 * m.columns[j]].sum()) for j in anchors}
            # Moment of the support's reactions about the chord's attachment: zero for a pinned fitting.
            moment = {j: float(((m.xy[m.columns[j], 1] - m.xy[m.columns[j][-1], 1])
                                * reaction[2 * m.columns[j]]).sum()) for j in anchors}
            pushing = [j for j in anchors if pull[j] < -1e-6 * abs(f).max()]
            if not pushing or len(pushing) == len(anchors):
                break
            anchors = [j for j in anchors if j not in pushing]
        ue = u[self.qdofs]
        # Stresses at the four Gauss points (per unit thickness: Pa), and each point's use of its
        # allowable (the working stress, or the compression allowance where compression dominates).
        stress = np.einsum("ij,gnjk,nk->gni", _plane_stress(), self.bg, ue)
        sx, sy, txy = stress[..., 0], stress[..., 1], stress[..., 2]
        vm = np.sqrt(sx * sx - sx * sy + sy * sy + 3 * txy * txy)
        centre, radius = (sx + sy) / 2, np.hypot((sx - sy) / 2, txy)
        utilisation = (vm / (self.inp.sigma * allowance(centre + radius, centre - radius))).max(axis=0)
        vm = vm.max(axis=0)
        n_hull = E * t_hull * np.einsum("na,na->n", (u[self.hdofs[:, 2:]] - u[self.hdofs[:, :2]]), self.eh) / self.lh
        n_outer = E * t_outer * np.einsum("na,na->n", (u[self.odofs[:, 2:]] - u[self.odofs[:, :2]]), self.eo) / self.lo
        return {"u": u, "f": f, "reaction": reaction, "anchors": anchors, "pull": pull, "moment": moment,
                "vm": vm, "stress": stress,
                "utilisation": utilisation,
                "n_hull": n_hull, "n_outer": n_outer, "pushing": len(pushing) == len(anchors) and bool(pushing)}

    # Local panel loads on the skins (normal pressures, Pa), per edge.
    def _panel_pressures(self):
        inp, m = self.inp, self.mesh
        phi = m.phi + math.pi / m.nt
        g_hull = inp.omega ** 2 * self.hx
        g_out = inp.omega ** 2 * self.ox
        cos = np.cos(phi)
        rock_column = inp.rock_density * inp.jacket
        # Hull: air outward; on the floor half the fill presses outward too (projected); on the hub-facing
        # half the rock presses inward (vaulted) or hangs from cell floors (hung).
        fill = inp.floor_mass / (2 * inp.a) * g_hull * np.clip(cos, 0, None) ** 2
        rock_on_hull = rock_column * g_hull * np.clip(-cos, 0, None)
        outward = inp.pressure + fill - (rock_on_hull if self.ceiling == "vaulted" else 0.0)
        rock_on_outer = rock_column * inp.floor_scale * g_out * np.clip(cos, 0, None)
        return outward, rock_on_outer, rock_on_hull

    def _skin_sizes(self, s, loads):
        """Skin thicknesses needed for the forces of a solution."""
        inp = self.inp
        hull_pillow, outer_pillow, n_long = loads
        h1, h2 = s["n_hull"] + hull_pillow, n_long + hull_pillow
        o1, o2 = s["n_outer"] + outer_pillow, outer_pillow
        need_h = np.sqrt(h1 * h1 - h1 * h2 + h2 * h2) / (inp.sigma * allowance(h1, h2))
        need_o = np.sqrt(o1 * o1 - o1 * o2 + o2 * o2) / (inp.sigma * allowance(o1, o2))
        return need_h, need_o

    def size(self, max_iter=200, tol=0.02):
        """Fully stressed sizing, until every part is within `tol` of its allowable (or at its minimum gauge)
        and none is over it by more than `tol`; the stresses are checked at every integration point.
        The result says whether that was reached (`converged`), and if not, whether at least no part is
        over its allowable (`sized`: safe but heavier than needed) or some still are (not a design)."""
        inp = self.inp
        nt, ne = self.mesh.nt, len(self.mesh.quads)
        t_hull, t_outer = np.full(nt, inp.skin_min), np.full(nt, inp.skin_min)
        tau_min = inp.wall_min / inp.cell
        tau = np.full(ne, tau_min)
        r_c = inp.cell / (8 * PANEL_SAG)                   # radius of curvature of a pillowed panel
        hull_q, outer_q, rock_q = self._panel_pressures()
        n_long = inp.pressure * inp.a / 2                  # lengthwise pressure load in the hull, N/m
        # Local panels: pillowing in tension; or, pressed inward by the rock, stiffened in bending.
        hull_pillow = np.clip(hull_q, 0, None) * r_c / 2
        stiffener = np.clip(-hull_q, 0, None) * inp.cell ** 2 / 8 * 2 / (inp.sigma * STIFFENER_DEPTH)
        cell_floor = (np.where(rock_q > 0, np.maximum(inp.wall_min, rock_q * r_c / 2 / inp.sigma), 0.0)
                      if self.ceiling == "hung" else np.zeros(nt))
        outer_pillow = outer_q * r_c / 2
        extra_hull = stiffener + cell_floor
        loads = (hull_pillow, outer_pillow, n_long)
        converged = False
        for it in range(1, max_iter + 1):
            s = self.solve(t_hull, t_outer, tau, extra_hull)
            need_h, need_o = self._skin_sizes(s, loads)
            util = self._utilisation(s, t_hull, t_outer, tau, need_h, need_o, tau_min)
            if util["max"] <= 1 + tol and util["slack"] <= tol:
                converged = True
                break
            # Skins: von Mises of (hoop + pillow, lengthwise + pillow) per unit length.
            t_hull, t_outer = np.maximum(inp.skin_min, need_h), np.maximum(inp.skin_min, need_o)
            tau = np.maximum(tau_min, tau * s["utilisation"])
        if not converged:      # report the sizes returned, not the ones before the last resizing
            s = self.solve(t_hull, t_outer, tau, extra_hull)
            util = self._utilisation(s, t_hull, t_outer, tau, *self._skin_sizes(s, loads), tau_min)
        out = self._result(s, t_hull, t_outer, tau, extra_hull, stiffener, cell_floor, it)
        out.update(converged=converged, sized=util["max"] <= 1 + tol, utilisation=util["max"], slack=util["slack"])
        return out

    def _utilisation(self, s, t_hull, t_outer, tau, need_h, need_o, tau_min):
        """Worst use of an allowable over all parts, and the worst spare capacity of a part above its
        minimum gauge (which a fully stressed design leaves at ~0)."""
        skin = self.inp.skin_min
        parts = ((need_h / t_hull, t_hull, skin), (need_o / t_outer, t_outer, skin), (s["utilisation"], tau, tau_min))
        worst = max(float(u.max()) for u, _, _ in parts)
        slack = 0.0
        for u, t, minimum in parts:
            above = t > minimum * (1 + 1e-6)
            if above.any():
                slack = max(slack, float((1 - u[above]).max()))
        return {"max": worst, "slack": slack}

    def masses(self, t_hull, t_outer, tau, extra_hull):
        """Steel per metre of tube (kg/m), by part."""
        inp, rho = self.inp, self.inp.steel_density
        arc = 1 / inp.centre
        hull = float((t_hull * self.lh * self.hx).sum() * arc * rho)
        outer = float((t_outer * self.lo * self.ox).sum() * arc * rho)
        bulkheads = float((tau * self.qarea * self.qx).sum() * arc * rho)
        panels = float((extra_hull * self.lh * self.hx).sum() * arc * rho)
        n_walls = max(1, round(2 * math.pi * (inp.a + inp.jacket / 2) / inp.cell))
        cell_walls = n_walls * inp.jacket * inp.wall_min * rho
        out = {"hull": hull, "outer_wall": outer, "bulkheads": bulkheads, "panels": panels,
               "cell_walls": cell_walls, "bumper": self.bumper_mass}
        out["total"] = sum(out.values())
        return out

    def _result(self, s, t_hull, t_outer, tau, extra_hull, stiffener, cell_floor, iterations):
        inp, m = self.inp, self.mesh
        per_m = self.masses(t_hull, t_outer, tau, extra_hull)
        per_torus = {k: v * 2 * math.pi * inp.centre for k, v in per_m.items()}
        load = float(s["f"][0::2].sum())
        anchor_force = {round(math.degrees(m.phi[j])): s["pull"][j] for j in s["anchors"]}
        compression = min(float(s["n_hull"].min()), float(s["n_outer"].min()))
        disp = np.hypot(s["u"][0::2], s["u"][1::2])
        return {
            "inputs": inp, "anchors": self.angles, "ceiling": self.ceiling, "iterations": iterations,
            "per_metre": per_m, "per_torus": per_torus,
            "t_hull": t_hull, "t_outer": t_outer, "tau": tau, "stiffener": stiffener, "cell_floor": cell_floor,
            "load": load, "rock_load": self.rock_load, "anchor_force": anchor_force,
            "reaction_sum": sum(s["pull"][j] for j in s["anchors"]),
            "max_compression": compression,            # N/m, most negative skin force
            "max_displacement": float(disp.max()),
            "vm_max": float(s["vm"].max()), "solution": s,
        }


def run(p, radius, anchors="sides", ceiling="vaulted", n_radial=4, n_around=144):
    from habitat_model import Design, evaluate

    res = evaluate(p, Design(radius_m=radius, n_tori=1))
    inp = inputs(p, Design(radius_m=radius), res["geometry"], res["mass"])
    out = Model(inp, anchors, ceiling, n_radial, n_around).size()
    out["model_hull_frames"] = res["mass"]["hull_frames"]
    out["model_rim"] = res["mass"]["rim"]
    return out
