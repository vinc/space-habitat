import math
import json
import tempfile
import unittest
from pathlib import Path
from contextlib import ExitStack
from unittest.mock import patch

import numpy as np

from logistics_model import networks, transfers


class TestNetworkResources(unittest.TestCase):
    def test_sampled_bodies_have_separate_nitrogen_scenarios(self):
        body={"diameter_km":.896}
        low,base,high=networks.supplier_scenarios("162173",body)
        self.assertAlmostEqual(base,networks.supplier_capacity(body,.001454,.7))
        self.assertAlmostEqual(low/base,(.001437*.5)/(.001454*.7))
        self.assertAlmostEqual(high/base,(.001471*.9)/(.001454*.7))
        bennu=networks.supplier_scenarios("101955",body)[1]
        self.assertAlmostEqual(base/bennu,.001454/.0024)

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


class TestNetworkCache(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.stack=ExitStack()
        self.addCleanup(self.stack.close)
        self.root=Path(self.tmp.name)
        for name in ("HOST_DATA","SCREEN_DATA","WINDOW_DATA","NETWORK_VECTORS","VECTORS"):
            filename=name+".npz" if name.endswith("VECTORS") else name+".json"
            self.stack.enter_context(patch.object(networks,name,self.root/filename))

    def test_same_day_input_change_recomputes_screen(self):
        hosts={"complete":True,"fetched":"2026-10-31","hosts":{
            "1":{"name":"host","elements":[1,.2,0,0,0]}}}
        suppliers={"fetched":"2026-10-31","candidates":{
            k:{"elements":[1,.1,0,0,0]} for k in ("162173","101955")}}
        networks.HOST_DATA.write_text(json.dumps(hosts))
        with patch.object(networks.catalogue,"load",return_value=suppliers), \
             patch.object(networks.catalogue,"coarse",return_value=1000), \
             patch.object(networks,"phase_minimum",return_value=(900,100)) as calculate:
            first=networks.screen_hosts()
            networks.screen_hosts()
            self.assertEqual(calculate.call_count,2)
            hosts["hosts"]["1"]["elements"][1]=.01
            networks.HOST_DATA.write_text(json.dumps(hosts))
            with self.assertRaisesRegex(ValueError,"screen inputs changed"):
                networks.require_current_screen(first)
            second=networks.screen_hosts()
            self.assertEqual(calculate.call_count,4)
            self.assertAlmostEqual(second["hosts"]["1"]["sunlight"]["season_ratio"],(1.01/.99)**2)
            suppliers["candidates"]["162173"]["elements"][0]=1.5
            networks.screen_hosts()
            self.assertEqual(calculate.call_count,6)

    def vectors(self, path, **bodies):
        np.savez_compressed(str(path)+".npz",jd=np.array([0.,10.]),
            meta=np.array(json.dumps({"complete":True,"fetched":"2020-01-01","source":"old snapshot"})),
            **bodies)
        Path(str(path)+".npz").rename(path)

    def test_resume_preserves_snapshot_and_refresh_fetches_every_body(self):
        networks.SCREEN_DATA.write_text("{}")
        old=np.ones((2,6))
        self.vectors(networks.VECTORS,Earth=old)
        self.vectors(networks.NETWORK_VECTORS,Earth=old,**{"1":old})
        before=networks.NETWORK_VECTORS.read_bytes()
        fresh=np.column_stack(([0.,10.],old*9))
        with patch.object(networks,"dated_pairs",return_value=[("Earth","1")]), \
             patch.object(networks,"fetch_vectors",return_value=fresh) as fetch:
            networks.fetch_network_vectors()
            fetch.assert_not_called()
            self.assertEqual(networks.NETWORK_VECTORS.read_bytes(),before)
            networks.fetch_network_vectors(refresh=True)
            self.assertEqual({call.args[0] for call in fetch.call_args_list},{"'399'","'1;'"})
        with np.load(networks.NETWORK_VECTORS) as data:
            np.testing.assert_array_equal(data["Earth"],old*9)
            np.testing.assert_array_equal(data["1"],old*9)
            meta=json.loads(str(data["meta"]))
            self.assertTrue(meta["complete"])
            self.assertEqual(set(meta["body_sources"]),{"Earth","1"})

    def test_dated_windows_invalidate_on_changed_vectors_with_same_metadata(self):
        networks.SCREEN_DATA.write_text("{}")
        self.vectors(networks.NETWORK_VECTORS,**{"1":np.ones((2,6))})
        class FakeEphemeris:
            meta={"complete":True,"fetched":"2026-10-31"}
        t=networks.jd_of(2030)
        with patch.object(networks,"Ephemeris",return_value=FakeEphemeris()), \
             patch.object(networks,"dated_pairs",return_value=[("1","2")]), \
             patch.object(networks.windows,"curve",return_value=(np.array([t]),np.array([5000.]),np.array([100.]))) as curve, \
             patch.object(networks,"refine_windows",return_value=[[5000.,t,100.]]):
            first=networks.compute_dated()
            networks.compute_dated()
            self.assertEqual(curve.call_count,1)
            self.vectors(networks.NETWORK_VECTORS,**{"1":np.ones((2,6))*2})
            second=networks.compute_dated()
            self.assertEqual(curve.call_count,2)
            self.assertNotEqual(first["vector_hash"],second["vector_hash"])


if __name__=="__main__":
    unittest.main()
