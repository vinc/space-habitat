"""Finite solar-electric thrust, changing mass and dated rendezvous.

Direct shooting with piecewise-constant inertial throttle vectors. RK4 is used
inside SLSQP; an independent adaptive DOP853 propagation accepts or rejects the
result. Sun gravity only, integrated Horizons endpoints, no gravity assists.
Units inside the solver: AU, sqrt(AU^3/mu), delivered spacecraft mass.
"""

from dataclasses import asdict, dataclass
import math

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

from .transfers import AU, DAY, MU_SUN, lambert

TIME = math.sqrt(AU**3 / MU_SUN)
SPEED = AU / TIME
ACCELERATION = AU / TIME**2


@dataclass(frozen=True)
class Engine:
    name: str
    power_1au_w: float = 5e6
    exhaust_m_s: float = 30000.
    efficiency: float = .65
    max_wet_ratio: float = 12.

    def __post_init__(self):
        if (self.power_1au_w <= 0 or self.exhaust_m_s <= 0
                or not 0 < self.efficiency <= 1 or self.max_wet_ratio <= 1):
            raise ValueError("invalid engine")

    def power(self, radius_au):
        # Installed electronics limit power inside 1 AU; panel output outside.
        return self.power_1au_w * np.minimum(1., 1 / np.maximum(radius_au, .1)**2)


def derivative(y, u, engine, delivered_kg):
    """Vectorised RHS. Guard values keep failed optimizer trials finite only."""
    radius=np.linalg.norm(y[..., :3],axis=-1)
    power=engine.power(radius)
    throttle=np.linalg.norm(u,axis=-1)
    thrust=2*engine.efficiency*power/engine.exhaust_m_s
    dy=np.empty_like(y)
    dy[..., :3]=y[..., 3:6]
    dy[..., 3:6]=-y[..., :3]/np.maximum(radius,.1)[...,None]**3
    dy[..., 3:6]+=thrust[...,None]*u/(delivered_kg*np.maximum(y[...,6],.1)[...,None]*ACCELERATION)
    dy[..., 6]=-thrust*throttle/engine.exhaust_m_s*TIME/delivered_kg
    return dy


def propagate(r0, v0, controls, wet_ratio, days, engine, delivered_kg, step_days=1.):
    """RK4, batching independent control histories for numerical derivatives."""
    controls=np.asarray(controls,float)
    single=controls.ndim==2
    if single:
        controls=controls[None,:,:]
    ratio=np.broadcast_to(wet_ratio,(len(controls),))
    y=np.empty((len(controls),7))
    y[:,:3]=np.asarray(r0)/AU
    y[:,3:6]=np.asarray(v0)/SPEED
    y[:,6]=ratio
    n=controls.shape[1]
    steps=max(1,math.ceil(abs(days)/n/step_days))
    h=days*DAY/TIME/(n*steps)
    for u in controls.transpose(1,0,2):
        for _ in range(steps):
            a=derivative(y,u,engine,delivered_kg)
            b=derivative(y+h*a/2,u,engine,delivered_kg)
            c=derivative(y+h*b/2,u,engine,delivered_kg)
            d=derivative(y+h*c,u,engine,delivered_kg)
            y+=h/6*(a+2*b+2*c+d)
    return y[0] if single else y


def verify(r0,v0,controls,wet_ratio,days,engine,delivered_kg,r1,v1):
    """Reintegrate each segment independently; no terminal impulsive correction."""
    y=np.r_[np.asarray(r0)/AU,np.asarray(v0)/SPEED,wet_ratio]
    segment=days*DAY/TIME/len(controls)
    min_radius=float(np.linalg.norm(y[:3])); min_mass=float(y[6])
    for u in controls:
        sol=solve_ivp(lambda t,s:derivative(s,u,engine,delivered_kg),
                      (0,segment),y,method="DOP853",rtol=2e-11,atol=2e-12,
                      max_step=.5*DAY/TIME)
        if not sol.success:
            return {"accepted":False,"reason":"verification integration failed"}
        y=sol.y[:,-1]
        min_radius=min(min_radius,float(np.min(np.linalg.norm(sol.y[:3],axis=0))))
        min_mass=min(min_mass,float(np.min(sol.y[6])))
    position=float(np.linalg.norm(y[:3]*AU-r1))
    velocity=float(np.linalg.norm(y[3:6]*SPEED-v1))
    throttle=float(np.max(np.linalg.norm(controls,axis=1)))
    # These are screening tolerances, not docking/navigation requirements.
    accepted=(position<=10000 and velocity<=.1 and min_mass>=1-1e-7
              and min_radius>=.5 and throttle<=1+1e-7)
    return {"accepted":bool(accepted),"position_error_m":position,"velocity_error_m_s":velocity,
            "final_mass_ratio":float(y[6]),"minimum_mass_ratio":min_mass,
            "minimum_radius_au":min_radius,"max_throttle":throttle}


def solve(eph,origin,target,departure_jd,flight_days,engine,delivered_kg,
          segments=16,step_days=1.,maxiter=180):
    """Local minimum-mass search at fixed dates, shot backwards from arrival.

    Backward mass flow increases mass, so trial paths never cross zero mass.
    A 0.1% numerical fuel reserve is targeted at arrival; real contingencies are
    additional. The independently forward-propagated result decides acceptance.
    """
    if delivered_kg<=0 or flight_days<=0 or segments<4 or step_days<=0:
        raise ValueError("invalid leg")
    r0,v0=eph.state(origin,departure_jd)
    r1,v1=eph.state(target,departure_jd+flight_days)
    a,b=lambert(r0,r1,flight_days*DAY)
    impulses=np.array([a-v0,v1-b])
    if not np.all(np.isfinite(impulses)):
        return {"accepted":False,"reason":"Lambert seed failed"}
    dv=float(np.sum(np.linalg.norm(impulses,axis=1)))
    q=math.exp(min(dv/engine.exhaust_m_s,math.log(engine.max_wet_ratio)))
    u=np.zeros((segments,3));count=max(2,segments//3)
    for j,sl in enumerate((slice(0,count),slice(-count,None))):
        r=r0 if j==0 else r1
        thrust=2*engine.efficiency*engine.power(np.linalg.norm(r)/AU)/engine.exhaust_m_s
        demand=impulses[j]*delivered_kg*(q if j==0 else 1)/(thrust*flight_days*DAY*count/segments)
        u[sl]=demand/max(1.,np.linalg.norm(demand))*.8
    wanted=np.r_[r0/AU,v0/SPEED]
    cached_x=None;cached_y=None;cached_j=None
    def final(x):
        nonlocal cached_x,cached_y,cached_j
        if cached_x is None or not np.array_equal(x,cached_x):
            cached_x=x.copy();cached_j=None
            cached_y=propagate(r1,v1,x.reshape(segments,3)[::-1],1.001,-flight_days,engine,delivered_kg,step_days)
        return cached_y
    def jac(x):
        nonlocal cached_j
        baseline=final(x)
        if cached_j is None:
            eps=1e-6
            # Central differences give the zero-throttle mass norm a symmetric
            # subgradient. One-sided differences spuriously favour negative axes.
            trials=np.concatenate([np.tile(x,(len(x),1))+np.eye(len(x))*eps,
                                   np.tile(x,(len(x),1))-np.eye(len(x))*eps])
            ys=propagate(r1,v1,trials.reshape(-1,segments,3)[:,::-1,:],1.001,-flight_days,engine,delivered_kg,step_days)
            cached_j=((ys[:len(x)]-ys[len(x):])/(2*eps)).T
        return cached_j
    def limits(x):
        return np.r_[1-np.sum(x.reshape(-1,3)**2,axis=1),engine.max_wet_ratio-final(x)[6]]
    def limits_jac(x):
        out=np.zeros((segments+1,len(x)))
        for k in range(segments):out[k,3*k:3*k+3]=-2*x[3*k:3*k+3]
        out[-1]=-jac(x)[6]
        return out
    bounds=[(-1.,1.)]*len(u.ravel())
    constraints=[{"type":"eq","fun":lambda x:final(x)[:6]-wanted,"jac":lambda x:jac(x)[:6]},
                 {"type":"ineq","fun":limits,"jac":limits_jac}]
    # Establish a rendezvous before trading its fuel against the constraints.
    # Starting the mass objective directly can settle on the wrong orbit family.
    warm=minimize(lambda x:0.,np.zeros_like(u.ravel()),jac=lambda x:np.zeros_like(x),
        method="SLSQP",bounds=bounds,constraints=constraints,
        options={"maxiter":max(20,maxiter//2),"ftol":1e-9})
    start=warm.x if np.linalg.norm(final(warm.x)[:6]-wanted)<np.linalg.norm(final(u.ravel())[:6]-wanted) else u.ravel()
    opt=minimize(lambda x:final(x)[6],start,jac=lambda x:jac(x)[6],method="SLSQP",
        bounds=bounds,constraints=constraints,options={"maxiter":maxiter,"ftol":1e-8})
    if (np.linalg.norm(final(warm.x)[:6]-wanted)<1e-7
            and np.min(limits(warm.x))>=-1e-7
            and np.linalg.norm(final(opt.x)[:6]-wanted)>1e-5):
        opt=warm
    projection=None
    if np.linalg.norm(final(opt.x)[:6]-wanted)<.02:
        projection=minimize(lambda x:0.,opt.x,jac=lambda x:np.zeros_like(x),method="SLSQP",
            bounds=bounds,constraints=constraints,options={"maxiter":30,"ftol":1e-11})
        if np.linalg.norm(final(projection.x)[:6]-wanted)<np.linalg.norm(final(opt.x)[:6]-wanted):
            opt.x=projection.x
    controls=opt.x.reshape(-1,3)
    wet_ratio=float(final(opt.x)[6])
    check=verify(r0,v0,controls,wet_ratio,flight_days,engine,delivered_kg,r1,v1)
    result={"origin":origin,"target":target,"departure_jd":float(departure_jd),
        "arrival_jd":float(departure_jd+flight_days),"flight_days":float(flight_days),
        "engine":asdict(engine),"delivered_kg":delivered_kg,"segments":segments,"step_days":step_days,
        "optimizer_success":bool(opt.success and opt is not warm),"optimizer_message":str(opt.message),
        "mass_objective_converged":bool(opt.success and opt is not warm),
        "feasibility_projection_success":None if projection is None else bool(projection.success),
        "iterations":int(opt.nit),"wet_ratio":wet_ratio,"controls":controls.tolist(),
        "verification":check,"accepted":bool(check["accepted"] and 1<=wet_ratio<=engine.max_wet_ratio),
        "shooting_direction":"backward","target_numerical_reserve_fraction":.001,
        "seed_impulsive_delta_v_m_s":dv}
    final_mass=check.get("final_mass_ratio",wet_ratio)
    propellant=(wet_ratio-final_mass)*delivered_kg
    result.update(propellant_kg=propellant,energy_j=propellant*engine.exhaust_m_s**2/(2*engine.efficiency),
                  loaded_propellant_kg=(wet_ratio-1)*delivered_kg,
                  final_reserve_kg=(final_mass-1)*delivered_kg,
                  integrated_delta_v_m_s=engine.exhaust_m_s*math.log(wet_ratio/max(final_mass,.1)))
    return polish(eph,result)


def polish(eph,result):
    """Correct near-feasible controls against adaptive, rather than RK4, dynamics.

    The RK4 Jacobian supplies a linearised correction; every residual and final
    mass used here comes from adaptive integration. This removes transcription
    error, particularly around the electrical power cap's derivative corner.
    """
    check=result.get("verification",{})
    if (result.get("accepted") or check.get("position_error_m",float("inf"))>5e7
            or check.get("velocity_error_m_s",float("inf"))>50
            or check.get("max_throttle",float("inf"))>1.001):
        return result
    engine=Engine(**result["engine"]);mass=result["delivered_kg"]
    r0,v0=eph.state(result["origin"],result["departure_jd"])
    r1,v1=eph.state(result["target"],result["arrival_jd"])
    wanted=np.r_[r0/AU,v0/SPEED]
    u=np.array(result["controls"]);n=len(u);days=result["flight_days"]
    def exact(controls):
        y=np.r_[r1/AU,v1/SPEED,1.001]
        for control in controls[::-1]:
            sol=solve_ivp(lambda t,s:derivative(s,control,engine,mass),
                (0,-days*DAY/TIME/n),y,method="DOP853",rtol=2e-11,atol=2e-12,
                max_step=.5*DAY/TIME)
            if not sol.success:raise RuntimeError("adaptive correction failed")
            y=sol.y[:,-1]
        return y
    for iteration in range(7):
        y=exact(u);error=y[:6]-wanted
        if np.linalg.norm(error)<1e-11:break
        x=u.ravel();eps=1e-6
        trials=np.concatenate([x+np.eye(len(x))*eps,x-np.eye(len(x))*eps])
        ys=propagate(r1,v1,trials.reshape(-1,n,3)[:,::-1,:],1.001,-days,engine,mass,result["step_days"])
        jac=((ys[:len(x)]-ys[len(x):])/(2*eps)).T
        correction=minimize(lambda z:.5*np.dot(z,z),np.zeros_like(x),jac=lambda z:z,
            method="SLSQP",constraints=[
                {"type":"eq","fun":lambda z:jac[:6]@z+error,"jac":lambda z:jac[:6]},
                {"type":"ineq","fun":lambda z:1-np.sum((x+z).reshape(n,3)**2,axis=1)},
                {"type":"ineq","fun":lambda z:engine.max_wet_ratio-y[6]-jac[6]@z}],
            options={"maxiter":50,"ftol":1e-12})
        if not correction.success:return result
        u=(x+correction.x).reshape(n,3)
    y=exact(u);q=float(y[6])
    checked=verify(r0,v0,u,q,days,engine,mass,r1,v1)
    if not checked["accepted"] or not 1<=q<=engine.max_wet_ratio:return result
    out=dict(result);final=checked["final_mass_ratio"]
    propellant=(q-final)*mass
    out.update(controls=u.tolist(),wet_ratio=q,verification=checked,accepted=True,
        adaptive_correction_iterations=iteration+1,propellant_kg=propellant,
        energy_j=propellant*engine.exhaust_m_s**2/(2*engine.efficiency),
        loaded_propellant_kg=(q-1)*mass,final_reserve_kg=(final-1)*mass,
        integrated_delta_v_m_s=engine.exhaust_m_s*math.log(q/final))
    return out
