"""Checks on the stack dynamics model (plan §4)."""

import math
import unittest

import numpy as np

from habitat_model import Design, evaluate, load, params
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


if __name__ == "__main__":
    unittest.main()
