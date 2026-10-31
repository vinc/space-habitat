"""Checks on the stack dynamics model (plan §4)."""

import math
import unittest

import numpy as np

from habitat_model import Design, evaluate, load, params
from dynamics_model import disturbances as ds
from dynamics_model import links as lk
from dynamics_model import stack as st
from dynamics_model.__main__ import GROWTH_FLOOR


def single(mass, polar, transverse, springs=(), omega=0.1, z=0.0, hub=1e-9):
    """One rigid body on a short, stiff hub of `hub` times its mass (light: free; heavy: ground)."""
    nodes = np.array([z - 1.0, z, z + 1.0])
    hub_mass = np.full(3, hub * mass / 3)
    body = st.Body("body", mass, polar, transverse, z, list(springs))
    # Stiff enough to be rigid next to the springs, not so stiff the eigenvalues lose precision.
    ei = 1e3 * max([k for _, k in springs], default=1e3)
    # The hub is ring-like too (J = 2 I_t), so a rigid assembly nutates at 2 w.
    return st.Stack(nodes, hub_mass, 2 * hub_mass, hub_mass, ei, [body], omega)


class TestWhirl(unittest.TestCase):
    def test_spinning_ring_nutates_at_twice_the_spin(self):
        # A thin ring held stiffly on a light hub: J = 2 I_t, nutation at (J / I_t) w, forward.
        s = single(1e9, 2e15, 1e15, [(-0.5, 1e10), (0.5, 1e10)], hub=1e-3)
        self.assertAlmostEqual(s.forward_ratio(), 2.0, places=3)

    def test_ring_on_springs_whirls_at_sqrt_k_over_m(self):
        # Translation of a body on a lateral spring at its centre, on a hub heavy enough to be ground:
        # +-sqrt(k / m) in the inertial frame, whatever the spin.
        m, k = 1e6, 4e4
        s = single(m, 1e-6, 1e-3 * m, [(0.0, k)], omega=0.1, hub=1e6)
        freq, growth = s.modes()
        self.assertTrue(np.any(np.isclose(np.abs(freq), math.sqrt(k / m), rtol=1e-3)))
        self.assertLessEqual(growth.max(), 1e-9)

    def test_rigid_stack_follows_the_maximum_axis_rule(self):
        p = params(load())
        d = Design(radius_m=900, n_tori=6)
        s, _ = st.build(p, d, hub_shell_m=0.5, tie_frac=0.05, rim_link=1e14)
        self.assertAlmostEqual(s.forward_ratio() / s.rigid_ratio(), 1, delta=0.02)
        # The model's rigid ratio is §11's, a little lower for the hub's mass.
        whole = evaluate(p, d)["stability"]["whole_inertia_ratio"]
        self.assertAlmostEqual(s.rigid_ratio() / whole, 1, delta=0.01)
        self.assertLess(s.rigid_ratio(), whole)


class TestStack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = params(load())

    def test_nets_centre_a_torus_at_about_half_its_centrifugal_pull(self):
        # The chords carry the rim's spin load from rim to rim: their sideways stiffness at the hub sums to
        # about (rim mass) w^2 r / 2L ~ m w^2 / 2, less the spokes' own share of the torus.
        for r in (400, 900, 1600, 2500):
            s, info = st.build(self.p, Design(radius_m=r, n_tori=2))
            m, w = info["mass"]["total"], info["geometry"]["omega"]
            ratio = 2 * info["nets"]["k_plane"] / (m * w * w)
            self.assertGreater(ratio, 0.35)
            self.assertLess(ratio, 0.55)

    def test_nets_alone_are_not_passively_stable(self):
        for r, n in ((900, 2), (900, 6), (1600, 6)):
            s, _ = st.build(self.p, Design(radius_m=r, n_tori=n))
            self.assertLess(s.forward_ratio(), 1)
            _, growth = s.modes(damping=0.01)
            self.assertGreater(growth.max(), 1e-4 * s.omega)

    def test_rim_links_and_ties_make_a_six_stack_stable(self):
        for r in (900, 1600):
            s, _ = st.build(self.p, Design(radius_m=r, n_tori=6), rim_link=1e11, tie_frac=1e-4)
            self.assertGreater(s.forward_ratio(), 1.2)
            _, growth = s.modes(damping=0.01)
            self.assertLessEqual(growth.max(), GROWTH_FLOOR * s.omega)

    def test_without_dissipation_the_whirl_is_neutral(self):
        s, _ = st.build(self.p, Design(radius_m=900, n_tori=6))
        _, growth = s.modes()
        self.assertLess(np.abs(growth).max(), 1e-6 * s.omega)

    def test_long_stacks_need_a_thicker_hub(self):
        d = Design(radius_m=900, n_tori=14)
        thin = st.build(self.p, d, rim_link=1e11, tie_frac=1e-4, hub_shell_m=0.02)[0].forward_ratio()
        thick = st.build(self.p, d, rim_link=1e11, tie_frac=1e-4, hub_shell_m=0.2)[0].forward_ratio()
        self.assertLess(thin, 1)
        self.assertGreater(thick, 1.2)

    def test_tie_stiffness(self):
        geo = evaluate(self.p, Design(radius_m=900, n_tori=1))["geometry"]
        k, length = st.tie_plane_stiffness(geo, 1e10, 1e-3, 7900)
        area = 1e-3 * 1e10 / (7900 * length) / 2
        self.assertAlmostEqual(k, st.E * area / (2 * length))
        self.assertAlmostEqual(length, 900 - 2 * geo["tube_radius"] - geo["jacket"] - geo["hub_radius"])


class TestForced(unittest.TestCase):
    def test_response_of_a_body_on_a_spring(self):
        # Heavy hub as ground: a load whirling at lam gives F / (k - m lam^2) (no gyroscopic term on
        # a displacement through the centre).
        m, k, lam = 1e6, 4e4, 0.05
        s = single(m, 1e-6, 1e-3 * m, [(0.0, k)], omega=0.1, hub=1e6)
        f = np.zeros(s.size(), dtype=complex)
        f[s.body_dof(0)] = 1e3
        q = s.response(lam, f)
        self.assertAlmostEqual(abs(q[s.body_dof(0)]), 1e3 / (k - m * lam ** 2), delta=1e-3 * 1e3 / (k - m * lam ** 2))

    def test_impulse_on_a_body_on_a_spring(self):
        # Kicked at v0, it swings to v0 / sqrt(k / m) (the heavy hub barely moves).
        m, k, v0 = 1e6, 4e4, 0.01
        s = single(m, 1e-6, 1e-3 * m, [(0.0, k)], omega=0.1, hub=1e6)
        v = np.zeros(s.size(), dtype=complex)
        v[s.body_dof(0)] = v0
        times = np.linspace(0, 4 * math.pi / math.sqrt(k / m), 400)
        q = s.transient(v, times)
        self.assertAlmostEqual(np.abs(q[:, s.body_dof(0)]).max(), v0 / math.sqrt(k / m), delta=0.02 * v0 / math.sqrt(k / m))
        self.assertLess(np.abs(q[0]).max(), 1e-12)


class TestLinks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = params(load())
        cls.geo = evaluate(cls.p, Design(radius_m=900, n_tori=6))["geometry"]

    def test_bay_stiffness_from_the_struts_geometry(self):
        # Shift one rim tangentially by u: one diagonal stretches, the other shortens; the tangential
        # components of their forces sum to k_bay u.
        lat = lk.lattice(self.geo, 1e10, 7900)
        w, h, a, u = lat["width"], lat["height"], lat["area"], 1e-4
        force = 0.0
        for sign in (1, -1):
            length0 = math.hypot(w, h)
            length = math.hypot(w + sign * u, h)
            tension = lk.E * a / length0 * (length - length0)
            force += tension * sign * (w / length0)
        k_bay = 2 * lat["k_lat"] / lat["bays"]
        self.assertAlmostEqual(force / u, k_bay, delta=1e-3 * k_bay)

    def test_tangential_links_give_the_same_stiffness_every_way(self):
        # N >= 3 links stiff only tangentially: sum of k sin^2 = N k / 2 in every direction.
        for n in (3, 4, 7, 548):
            angles = 2 * math.pi * np.arange(n) / n
            for direction in (0.0, 0.3, 1.1):
                total = (np.sin(angles - direction) ** 2).sum()
                self.assertAlmostEqual(total, n / 2, places=9)

    def test_only_the_links_sideways_stiffness_matters(self):
        for r in (900, 1600):
            d = Design(radius_m=r, n_tori=6)
            ratios = lk.compare_tilt(self.p, d, 1e10, tie_frac=1e-4)
            self.assertLess(abs(ratios["none"] / ratios["default"] - 1), 0.01)

    def test_design_stiffness_is_near_rigid_links(self):
        d = Design(radius_m=900, n_tori=6)
        k, rigid = lk.design_stiffness(self.p, d, tie_frac=1e-4)
        ratio = st.build(self.p, d, rim_link=k, tie_frac=1e-4)[0].forward_ratio()
        self.assertGreater(ratio, 0.97 * rigid)
        self.assertGreater(ratio, 1.2)

    def test_struts_hold_the_largest_force(self):
        force = 5e7
        lat = lk.lattice(self.geo, 1e9, 7900, force=force)
        buckling = math.pi ** 2 * lk.E * lat["area"] * lat["diameter"] ** 2 / (8 * lat["diagonal"] ** 2)
        self.assertGreaterEqual(buckling, lk.SAFETY * lat["strut_force"] * (1 - 1e-9))
        self.assertGreaterEqual(lat["area"] * lk.YIELD, lk.SAFETY * lat["strut_force"] * (1 - 1e-9))


class TestDisturbances(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = params(load())
        cls.d = Design(radius_m=900, n_tori=6)
        cls.s, cls.info = st.build(cls.p, cls.d, rim_link=1e10, tie_frac=1e-4)

    def test_a_train_at_rim_speed_pulls_on_nothing(self):
        geo = self.info["geometry"]
        speed = self.s.omega * (geo["radius"] - geo["width"])
        self.assertLess(ds.rim_train(self.s, geo, speed=speed)["force"], 1e-6)

    def test_trains_meet_no_resonance_below_the_spin(self):
        # Loads whirling forward slower than the spin: the response grows smoothly toward the
        # imbalance's at lam = w, never above it (no forward modes there).
        geo = self.info["geometry"]
        links = [ds.rim_train(self.s, geo, speed=v)["link"] for v in np.linspace(0, 80, 17)]
        self.assertTrue(all(a >= b for a, b in zip(links, links[1:])))

    def test_imbalance_shifts_the_stack_about_its_centre_of_mass(self):
        # Rigid estimate: the spin axis moves to the new centre of mass, m e / M from the old one; the end
        # torus moves a little more, the stack also tilting about its principal axis.
        geo, mass_e = self.info["geometry"], 1e6
        res = ds.imbalance(self.s, geo, mass_e)
        m, _, _ = self.s.matrices()
        ratio = res["torus"] / (mass_e * geo["radius"] / m.diagonal()[self.s.displacements()].sum())
        self.assertGreater(ratio, 1.0)
        self.assertLess(ratio, 1.5)

    def test_docking_turns_the_axis_by_the_angular_impulse(self):
        res = ds.docking(self.s, spins=4, samples=200)
        h, _ = ds.angular_momentum(self.s)
        arm = ds.centre_of_mass(self.s) - self.s.hub_nodes[0]
        self.assertAlmostEqual(res["axis_turn"], ds.SHIP_MASS * ds.SHIP_MISS * arm / h)
        self.assertIsNotNone(res["decay_hours"])

    def test_sunlight_sums_to_zero_over_an_eccentric_orbit(self):
        # Integrate (a / d)^2 times the Sun's direction over time on a Kepler orbit: it closes, and
        # its largest excursion is the wobble's 2 a^2 / h.
        a, e = 1.458 * ds.AU, 0.2227
        n = math.sqrt(ds.GM_SUN / a ** 3)
        mean = np.linspace(0, 2 * math.pi, 20001)
        ecc = mean.copy()
        for _ in range(50):
            ecc = mean + e * np.sin(ecc)
        nu = 2 * np.arctan2(math.sqrt(1 + e) * np.sin(ecc / 2), math.sqrt(1 - e) * np.cos(ecc / 2))
        d = a * (1 - e * np.cos(ecc))
        dt = (mean[1] - mean[0]) / n
        path = np.cumsum((a / d) ** 2 * np.exp(1j * nu)) * dt
        h = math.sqrt(ds.GM_SUN * a * (1 - e * e))
        self.assertLess(abs(path[-1]) / (2 * a * a / h), 1e-3)
        self.assertAlmostEqual(np.abs(path - path[0]).max() / (2 * a * a / h), 1, delta=1e-3)


if __name__ == "__main__":
    unittest.main()
