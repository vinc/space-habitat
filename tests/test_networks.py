import math
import unittest
from unittest.mock import patch

import numpy as np

from logistics_model import networks, transfers


class TestNetworkResources(unittest.TestCase):
    def test_inventory_scales_with_volume(self):
        self.assertAlmostEqual(networks.bulk_mass(2,1200)/networks.bulk_mass(1,1200),8)

    def test_no_nitrogen_means_no_complete_habitat(self):
        self.assertEqual(networks.supplier_capacity({"diameter_km":1},0,.7),0)

    def test_nitrogen_recovery_and_water_bottleneck(self):
        body={"diameter_km":1}
        a=networks.supplier_capacity(body,.0005,.5)
        b=networks.supplier_capacity(body,.001,.5)
        self.assertAlmostEqual(b,2*a)
        self.assertAlmostEqual(networks.supplier_capacity(body,.001,.25),a)
        # Abundant N cannot buy more habitats than the fixed water inventory.
        self.assertAlmostEqual(networks.supplier_capacity(body,.5,1),
                               networks.supplier_capacity(body,1,1))

    def test_sunlight_at_perihelion_and_aphelion(self):
        x=networks.sunlight_metrics([1,.2,0,0,0])
        self.assertAlmostEqual(x["season_ratio"],2.25)
        self.assertAlmostEqual(x["min_sunlight"],1/1.44)
        self.assertAlmostEqual(x["year_earth_years"],1)

    def test_h_estimates_are_not_measured_diameters(self):
        # A fourfold albedo changes diameter twofold and mass eightfold.
        a=networks.diameter_from_h(18,.1)
        b=networks.diameter_from_h(18,.4)
        self.assertAlmostEqual(a/b,2)


class TestNetworkWindows(unittest.TestCase):
    def test_network_uses_union_and_horizon_edges(self):
        # Second source fills a gap; duplicate opportunities are counted once.
        x=networks.opportunity_gaps([2,8],0,10)
        y=networks.opportunity_gaps([2,8,5,5,-1,11],0,10)
        self.assertAlmostEqual(x["max_years"]*365.25,6)
        self.assertAlmostEqual(y["max_years"]*365.25,3)
        self.assertEqual(y["count"],3)
        self.assertAlmostEqual(y["initial_years"]*365.25,2)
        self.assertAlmostEqual(y["final_years"]*365.25,2)

    def test_no_service_exposes_entire_horizon(self):
        x=networks.opportunity_gaps([],0,365.25*44)
        self.assertEqual(x["count"],0)
        self.assertAlmostEqual(x["max_years"],44)

    def test_refinement_respects_flight_bounds(self):
        class FakeEphemeris:
            def span(self):return 0,5000
        # An unconstrained optimiser would prefer a >900-day flight.
        cost=lambda eph,o,t,t1,tof: (np.asarray(t1)-100)**2+(np.asarray(tof)-1000)**2
        with patch("logistics_model.networks.windows.delta_v",side_effect=cost):
            dv,t,tof=networks.bounded_refine(FakeEphemeris(),"a","b",101,895,50,150)
        self.assertAlmostEqual(t,100,delta=.03)
        self.assertEqual(tof,900)

    def test_batched_phase_refinement_matches_existing_solver(self):
        transfers.ELEMENTS["network_test_inner"]=(1,0,0,0,0)
        transfers.ELEMENTS["network_test_outer"]=(1.524,0,0,0,0)
        try:
            dv,tof=networks.phase_minimum("network_test_inner","network_test_outer")
            a1,a2=transfers.AU,1.524*transfers.AU
            at=(a1+a2)/2;mu=transfers.MU_SUN
            expected=math.sqrt(mu*(2/a1-1/at))-math.sqrt(mu/a1)+math.sqrt(mu/a2)-math.sqrt(mu*(2/a2-1/at))
            self.assertAlmostEqual(dv/expected,1,delta=.002)
            self.assertAlmostEqual(tof,math.pi*math.sqrt(at**3/mu)/transfers.DAY,delta=3)
        finally:
            del transfers.ELEMENTS["network_test_inner"],transfers.ELEMENTS["network_test_outer"]


if __name__=="__main__":
    unittest.main()
