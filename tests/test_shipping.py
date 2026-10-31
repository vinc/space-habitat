import math
import unittest
from dataclasses import asdict

import numpy as np

from logistics_model import low_thrust as lt, shipping


class CircularEphemeris:
    def state(self,body,jd):
        phase=jd*lt.DAY/lt.TIME
        return (lt.AU*np.array([math.cos(phase),math.sin(phase),0.]),
                lt.SPEED*np.array([-math.sin(phase),math.cos(phase),0.]))


class TestFiniteThrust(unittest.TestCase):
    def test_power_thrust_and_mass_flow(self):
        engine=lt.Engine("test",power_1au_w=1e6,exhaust_m_s=10000,efficiency=.5)
        y=np.array([2.,0,0,0,0,0,2.])
        dy=lt.derivative(y,np.array([1.,0,0]),engine,1000)
        self.assertAlmostEqual(engine.power(.8),1e6)
        self.assertAlmostEqual(engine.power(2.),.25e6)
        thrust=25.
        self.assertAlmostEqual((dy[3]+.25)*lt.ACCELERATION,thrust/2000)
        self.assertAlmostEqual(-dy[6]*1000/lt.TIME,thrust/10000)

    def test_zero_thrust_matches_keplerian_coast_and_batch(self):
        eph=CircularEphemeris();r,v=eph.state("a",0)
        engine=lt.Engine("test")
        result=lt.propagate(r,v,np.zeros((4,3)),1.,20,engine,1000,step_days=.2)
        rt,vt=eph.state("b",20)
        np.testing.assert_allclose(result[:3]*lt.AU,rt,rtol=0,atol=20)
        np.testing.assert_allclose(result[3:6]*lt.SPEED,vt,rtol=0,atol=.0001)
        batch=lt.propagate(r,v,np.zeros((2,4,3)),[1,2],20,engine,1000,step_days=.2)
        np.testing.assert_allclose(batch[:,:6],np.broadcast_to(result[:6],(2,6)))
        np.testing.assert_array_equal(batch[:,6],[1,2])

    def test_solver_and_independent_verification_on_coast(self):
        r=lt.solve(CircularEphemeris(),"a","b",0.,20.,lt.Engine("test"),1000.,
                   segments=4,step_days=.5,maxiter=25)
        self.assertTrue(r["accepted"],r)
        self.assertLess(r["verification"]["position_error_m"],10000)
        self.assertLess(abs(r["propellant_kg"]),.01)

    def test_verification_rejects_missing_mass_and_endpoint_mismatch(self):
        eph=CircularEphemeris();r,v=eph.state("a",0);rt,vt=eph.state("b",20)
        engine=lt.Engine("test")
        check=lt.verify(r,v,np.ones((4,3))*.1,1.,20,engine,1000,rt,vt)
        self.assertFalse(check["accepted"])
        self.assertLess(check["minimum_mass_ratio"],1.)
        check=lt.verify(r,v,np.zeros((4,3)),1.,20,engine,1000,rt+1e6,vt)
        self.assertFalse(check["accepted"])

    def test_adaptive_correction_removes_nearby_endpoint_error(self):
        eph=CircularEphemeris();engine=lt.Engine("test")
        r,v=eph.state("a",0);rt,vt=eph.state("b",20)
        controls=np.full((4,3),1e-5)
        check=lt.verify(r,v,controls,1.001,20,engine,1000,rt,vt)
        self.assertFalse(check["accepted"])
        result={"origin":"a","target":"b","departure_jd":0.,"arrival_jd":20.,
            "flight_days":20.,"engine":asdict(engine),"delivered_kg":1000.,
            "controls":controls.tolist(),"wet_ratio":1.001,"step_days":.5,
            "accepted":False,"verification":check}
        fixed=lt.polish(eph,result)
        self.assertTrue(fixed["accepted"],fixed)
        self.assertLess(fixed["verification"]["position_error_m"],10000)
        self.assertGreaterEqual(fixed["verification"]["final_mass_ratio"],1-1e-7)


def leg(origin,target,start,end,mass):
    return {"accepted":True,"verification":{"accepted":True},"origin":origin,"target":target,
        "departure_jd":start,"arrival_jd":end,"delivered_kg":mass,"engine":{"name":"test"},
        "energy_j":100.,"propellant_kg":2.}


def route(start,delivery,return_arrival):
    return shipping.cycle(leg("source","host",start,delivery,110),
        leg("host","source",delivery+1,return_arrival,10),100,10,1)


class TestDatedShipping(unittest.TestCase):
    def test_energy_breaks_ties_after_stock_and_voyage_count(self):
        expensive=route(0,10,50)
        expensive["outbound"]["energy_j"]=1000
        cheap=route(0,10,50)
        result=shipping.schedule([expensive,cheap],0,100,365.25,1)
        self.assertTrue(result["feasible"])
        self.assertTrue(result["energy_tiebreak_success"])
        self.assertEqual(result["voyages"],1)
        self.assertAlmostEqual(result["initial_stock_kg"],10,places=3)
        self.assertAlmostEqual(result["energy_j"],200)

    def test_return_and_turnaround_enable_reusing_one_ship(self):
        cycles=[route(0,10,30),route(31,41,60)]
        s=shipping.schedule(cycles,0,200,365.25,1)
        self.assertTrue(s["feasible"],s)
        self.assertEqual(s["voyages"],2)
        self.assertAlmostEqual(s["initial_stock_kg"],10,places=3)
        self.assertAlmostEqual(s["final_stock_kg"],10,places=3)
        self.assertEqual([e["ships"] for e in s["events"]],[[0],[0]])
        self.assertAlmostEqual(s["energy_j"],400)
        self.assertAlmostEqual(s["propellant_kg"],8)

    def test_overlap_cannot_be_hidden_by_initial_stock(self):
        cycles=[route(0,10,50),route(20,30,70)]
        self.assertFalse(shipping.schedule(cycles,0,200,365.25,1)["feasible"])
        self.assertTrue(shipping.schedule(cycles,0,200,365.25,2)["feasible"])

    def test_inadequate_deliveries_are_not_filled_by_unlimited_seed_stock(self):
        self.assertFalse(shipping.schedule([route(0,10,50)],0,200,365.25,1)["feasible"])

    def test_unverified_or_teleporting_return_is_rejected(self):
        out=leg("source","host",0,10,110)
        back=leg("host","source",11,20,10)
        out["verification"]["accepted"]=False
        with self.assertRaisesRegex(ValueError,"unverified"):
            shipping.cycle(out,back,100,10,1)
        out["verification"]["accepted"]=True
        back["departure_jd"]=10
        with self.assertRaisesRegex(ValueError,"return leg"):
            shipping.cycle(out,back,100,10,1)


if __name__=="__main__":unittest.main()
