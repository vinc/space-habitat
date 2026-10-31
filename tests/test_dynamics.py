"""Checks on the stack dynamics model (plan §4)."""

import math
import unittest

import numpy as np

from habitat_model import Design, evaluate, load, params
from dynamics_model import axial_torsion as at
from dynamics_model import disturbances as ds
from dynamics_model import fatigue as fa
from dynamics_model import joints as jt
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

    def test_lattice_sized_on_its_own_stack(self):
        # The struts are sized for the force the finished lattice's stack takes: resizing for it
        # changes nothing.
        d = Design(radius_m=900, n_tori=2)
        k, _ = lk.design_stiffness(self.p, d, tie_frac=1e-4)
        lat, s, info, unbalanced = lk.converged(self.p, d, k, tie_frac=1e-4)
        self.assertAlmostEqual(s.links[0][2], lat["k_lat"], delta=1e-3 * lat["k_lat"])
        again = ds.imbalance(s, info["geometry"], self.p.ballast_frac * info["mass"]["rim"])
        resized = lk.lattice(info["geometry"], k, self.p.steel_density, force=again["link"])
        self.assertAlmostEqual(resized["area"] / lat["area"], 1, delta=1e-3)

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

    def test_compensated_bearing_leaves_no_torque_on_the_stack(self):
        res = ds.bearing(self.s, self.info["array_mass"], 1e6, friction=1e4)
        self.assertEqual(res["net_torque"], 0.0)
        self.assertAlmostEqual(res["power"], 1e4 * self.s.omega)
        # Uncompensated, the stack gives up only the array's share of the spin: tiny.
        self.assertLess(res["spin_share"], 1e-3)

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


def two_node(length, ei, ga=None, hinge=None):
    nodes = np.array([0.0, length])
    return st.Stack(nodes, np.ones(2), np.ones(2), np.ones(2), ei, [], 0.1, ga=ga,
                    hinges={0: hinge} if hinge else {})


class TestHubElement(unittest.TestCase):
    def tip(self, s):
        # Clamp the first node: the tip's flexibility under a tip force.
        k = s.element_stiffness(0)[2:, 2:]
        return np.linalg.inv(k)[0, 0]

    def test_euler_bernoulli_cantilever(self):
        self.assertAlmostEqual(self.tip(two_node(20.0, 1e12)) / (20.0 ** 3 / 3e12), 1, places=9)

    def test_shear_adds_l_over_ga(self):
        flex = self.tip(two_node(20.0, 1e12, ga=1e9))
        self.assertAlmostEqual(flex / (20.0 ** 3 / 3e12 + 20.0 / 1e9), 1, places=9)

    def test_joint_adds_l2_over_k(self):
        flex = self.tip(two_node(20.0, 1e12, hinge=1e10))
        self.assertAlmostEqual(flex / (20.0 ** 3 / 3e12 + 20.0 ** 2 / 1e10), 1, places=9)

    def test_stiff_joints_leave_the_margin(self):
        p = params(load())
        d = Design(radius_m=900, n_tori=6)
        base = st.build(p, d, rim_link=5e10, tie_frac=1e-4)[0].forward_ratio()
        stiff = st.build(p, d, rim_link=5e10, tie_frac=1e-4, joint_k=1e18)[0].forward_ratio()
        soft = st.build(p, d, rim_link=5e10, tie_frac=1e-4, joint_k=1e12)[0].forward_ratio()
        self.assertAlmostEqual(stiff / base, 1, places=4)
        self.assertLess(soft, 0.6 * base)

    def test_shear_lowers_the_margin_a_little(self):
        p = params(load())
        d = Design(radius_m=1600, n_tori=6)
        bending = st.build(p, d, rim_link=5e10, tie_frac=1e-4, shear=False)[0].forward_ratio()
        both = st.build(p, d, rim_link=5e10, tie_frac=1e-4)[0].forward_ratio()
        self.assertLess(both, bending)
        self.assertGreater(both, 0.95 * bending)


class TestDetails(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = params(load())
        cls.d = Design(radius_m=900, n_tori=2)
        cls.k, _ = lk.design_stiffness(cls.p, cls.d, tie_frac=1e-4)

    def test_flange_is_far_stiffer_than_needed(self):
        j = jt.hub_joint(self.p, self.d, self.k, tie_frac=1e-4)
        self.assertGreater(j["flange"], 10 * j["needed"])
        self.assertGreater(j["opening_margin"], 10)
        h = evaluate(self.p, self.d)["geometry"]["hub_radius"]
        self.assertAlmostEqual(j["flange"], st.E * jt.BOLT_AREA / jt.BOLT_GRIP / jt.BOLT_SPACING * math.pi * h ** 3)

    def test_lacing_lifts_the_axial_and_torsional_modes(self):
        a = at.study(self.p, self.d, self.k, tie_frac=1e-4)
        self.assertLess(a["axial_bare"], 1.2)
        self.assertLess(a["torsion_bare"], 1.0)
        self.assertGreaterEqual(a["axial_lowest"], at.TARGET * 0.999)
        self.assertGreaterEqual(a["torsion_lowest"], at.TARGET * 0.999)

    def test_a_farm_ring_bounces_on_its_spokes_tension(self):
        # Two planes of radial spokes, each T / L along the axis: w^2 = 2 T / (L m), T = m w^2 r_f / 2
        # less the spokes' own share, so about w sqrt(r_f / L).
        res = evaluate(self.p, self.d)
        geo, mass = res["geometry"], res["mass"]
        spokes = at.farm_spokes(geo, mass)
        natural = math.sqrt(2 * spokes["axial"] / mass["farm_total"]) / geo["omega"]
        estimate = math.sqrt(geo["farm_radius"] / (geo["farm_radius"] - geo["hub_radius"]))
        self.assertAlmostEqual(natural / estimate, 1, delta=0.02)

    def test_an_unlinked_gap_loses_the_margin_and_a_few_bays_restore_it(self):
        c = lk.construction(self.p, self.d, self.k, tie_frac=1e-4)
        self.assertLess(c["worst"], 1.0)
        self.assertGreater(c["e_folding_hours"], 0)
        self.assertLess(c["share"], 0.1)

    def test_fatigue_curve(self):
        detail = 71e6
        d_d = fa.D_RATIO * detail
        self.assertAlmostEqual(fa.endurance(detail, detail), 2e6)
        self.assertAlmostEqual(fa.endurance(detail, d_d * 1.000001) / 5e6, 1, delta=1e-4)
        self.assertAlmostEqual(fa.endurance(detail, fa.L_RATIO * d_d * 1.000001) / 1e8, 1, delta=1e-4)
        self.assertEqual(fa.endurance(detail, 0.5 * d_d), math.inf)

    def test_no_fatigue_damage(self):
        f = fa.study(self.p, self.d, self.k, tie_frac=1e-4)
        self.assertTrue(all(v == 0 for v in f["damage"].values()))


if __name__ == "__main__":
    unittest.main()
