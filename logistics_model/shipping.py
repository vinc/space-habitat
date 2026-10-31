"""Dated reusable fleets and continuous construction demand on a finite horizon.

Each candidate cycle contains an independently accepted outbound and return leg.
All ships start at the supplier. They refuel at both ends. The MILP allocates
integer voyages under fleet availability, then minimises the initial host stock.
End inventory must cover initial inventory: a schedule cannot hide inadequate
deliveries by simply spending down a seed stock over the whole study horizon.
"""

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def cycle(outbound, inbound, payload_kg, dry_kg, turnaround_days=30.):
    if payload_kg<=0 or dry_kg<=0 or turnaround_days<0:
        raise ValueError("invalid freighter")
    for leg in (outbound,inbound):
        if not leg.get("accepted") or not leg.get("verification",{}).get("accepted"):
            raise ValueError("unverified trajectory cannot enter a shipping schedule")
    if (outbound["origin"]!=inbound["target"] or outbound["target"]!=inbound["origin"]
            or inbound["departure_jd"]<outbound["arrival_jd"]+turnaround_days):
        raise ValueError("return leg does not follow cargo delivery")
    if not (np.isclose(outbound["delivered_kg"],dry_kg+payload_kg)
            and np.isclose(inbound["delivered_kg"],dry_kg)
            and outbound["engine"]==inbound["engine"]):
        raise ValueError("legs must use the same vehicle and the correct payload masses")
    return {"departure_jd":outbound["departure_jd"],"delivery_jd":outbound["arrival_jd"],
        "ready_jd":inbound["arrival_jd"]+turnaround_days,"return_departure_jd":inbound["departure_jd"],
        "payload_kg":payload_kg,"dry_kg":dry_kg,"outbound":outbound,"return":inbound}


def schedule(cycles, start_jd, end_jd, annual_demand_kg, fleet_size):
    """Minimum host seed stock for this menu of cycles and this fleet size.

    No claims about departures outside the menu, launch cadence, mining rate,
    supplier inventory, or an indefinitely repeating schedule follow from this.
    """
    if end_jd<=start_jd or annual_demand_kg<=0 or fleet_size<1 or int(fleet_size)!=fleet_size:
        raise ValueError("invalid schedule")
    useful=[c for c in cycles if c["departure_jd"]>=start_jd and c["delivery_jd"]<=end_jd]
    if not useful:
        return {"feasible":False,"reason":"no verified deliveries inside the horizon"}
    # Keep separate commodity/vehicle networks. Mixing source fleets needs transfers.
    identity={(c["outbound"]["origin"],c["outbound"]["target"],c["payload_kg"],c["dry_kg"],
               tuple(sorted(c["outbound"]["engine"].items()))) for c in useful}
    if len(identity)!=1:
        raise ValueError("schedule requires one source, engine and vehicle configuration")
    payload=useful[0]["payload_kg"]
    daily=annual_demand_kg/365.25/payload
    total=daily*(end_jd-start_jd)
    n=len(useful); rows=[]; lower=[]; upper=[]
    # A vessel stays busy from source departure through source turnaround.
    for t in sorted(set(c["departure_jd"] for c in useful)):
        rows.append([float(c["departure_jd"]<=t<c["ready_jd"]) for c in useful]+[0.])
        lower.append(-np.inf);upper.append(fleet_size)
    # Inventory troughs immediately BEFORE each delivery, then at horizon end.
    for t in sorted(set(c["delivery_jd"] for c in useful)):
        rows.append([float(c["delivery_jd"]<t) for c in useful]+[1.])
        lower.append(daily*(t-start_jd));upper.append(np.inf)
    rows.append([1.]*n+[1.]);lower.append(total);upper.append(np.inf)
    # Final stock >= initial stock: full horizon demand must actually be shipped.
    rows.append([1.]*n+[0.]);lower.append(total);upper.append(np.inf)
    constraints=LinearConstraint(np.array(rows),lower,upper)
    # Lexicographic objectives: initial stock, voyages, then flight electricity.
    objective=np.r_[np.zeros(n),1.]
    bounds=Bounds(np.zeros(n+1),np.r_[np.full(n,fleet_size),np.inf])
    integrality=np.r_[np.ones(n),0]
    opt=milp(objective,integrality=integrality,bounds=bounds,constraints=constraints)
    if not opt.success:
        return {"feasible":False,"reason":"fleet cannot balance horizon demand on the sampled cycles",
                "solver_message":str(opt.message)}
    stock=float(opt.x[-1]); objective=np.r_[np.ones(n),0.]
    lo=np.zeros(n+1);hi=np.r_[np.full(n,fleet_size),stock+1e-6]
    second=milp(objective,integrality=integrality,bounds=Bounds(lo,hi),constraints=constraints)
    if second.success:opt=second
    voyage_count=int(round(sum(opt.x[:n])))
    costs=np.array([c["outbound"]["energy_j"]+c["return"]["energy_j"] for c in useful],float)
    costs/=max(float(np.max(costs)),1.)
    count_constraint=LinearConstraint(np.r_[np.ones(n),0.][None,:],voyage_count,voyage_count)
    third=milp(np.r_[costs,0.],integrality=integrality,bounds=Bounds(lo,hi),
               constraints=[constraints,count_constraint])
    if third.success:opt=third
    counts=np.rint(opt.x[:n]).astype(int)
    initial=float(opt.x[-1])*payload
    # Assign identities to show that no ship teleports or overlaps another voyage.
    ready=np.full(fleet_size,start_jd);events=[]
    for j in sorted(range(n),key=lambda j:useful[j]["departure_jd"]):
        c=useful[j];available=np.flatnonzero(ready<=c["departure_jd"]+1e-8)
        if len(available)<counts[j]:raise RuntimeError("MILP fleet assignment failed")
        ids=available[:counts[j]]
        ready[ids]=c["ready_jd"]
        if len(ids):events.append({"cycle_index":j,"ships":ids.tolist(),"voyages":int(counts[j]),
            "departure_jd":c["departure_jd"],"delivery_jd":c["delivery_jd"],"ready_jd":c["ready_jd"],
            "cargo_kg":len(ids)*payload})
    inventory=[];stock_now=initial;last=start_jd
    for t in sorted(set(e["delivery_jd"] for e in events)):
        stock_now-=(t-last)*annual_demand_kg/365.25
        inventory.append({"jd":t,"before_kg":stock_now,
            "delivered_kg":sum(e["cargo_kg"] for e in events if e["delivery_jd"]==t)})
        stock_now+=inventory[-1]["delivered_kg"];last=t
    stock_now-=(end_jd-last)*annual_demand_kg/365.25
    if min([v["before_kg"] for v in inventory]+[stock_now]) < -1:
        raise RuntimeError("negative inventory after schedule verification")
    energy=sum(counts[j]*(c["outbound"]["energy_j"]+c["return"]["energy_j"]) for j,c in enumerate(useful))
    prop=sum(counts[j]*(c["outbound"]["propellant_kg"]+c["return"]["propellant_kg"]) for j,c in enumerate(useful))
    return {"feasible":True,"fleet_size":int(fleet_size),"voyages":int(sum(counts)),
        "voyage_tiebreak_success":bool(second.success),"energy_tiebreak_success":bool(third.success),
        "initial_stock_kg":initial,"final_stock_kg":stock_now,"demand_kg":total*payload,
        "delivered_kg":float(sum(counts)*payload),"events":events,"inventory":inventory,
        "energy_j":float(energy),"propellant_kg":float(prop)}
