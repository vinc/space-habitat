"""Run or reproduce the first dated finite-thrust shipping study.

python -m logistics_model.shipping_study --solve   # minutes, saved Horizons only
python -m logistics_model.shipping_study --report  # offline, saved results
"""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

import numpy as np

from . import low_thrust, shipping, windows
from .ephemeris import Ephemeris, jd_of
from .networks import DATA, NETWORK_VECTORS, content_hash, reference_design, vector_hash, bounded_refine

RESULTS=DATA/"low_thrust_shipping.json"
REPORT=Path(__file__).resolve().parents[1]/"reports"/"shipping-schedule.md"
SETTINGS={"start_year":2030,"end_year":2050,"departure_end_year":2047,
    "payload_kg":1e6,"dry_kg":2e5,"power_1au_w":2e7,"turnaround_days":30.,
    "segments":16,"step_days":1.,"maxiter":50,"cycles_per_source":3,
    "fleets":[60,120,240],"construction_tori_per_year":.1,
    "engines":[{"name":"electric","exhaust_m_s":30000.,"efficiency":.65},
               {"name":"residue mass driver (hypothetical)","exhaust_m_s":3000.,"efficiency":.5}]}
SOURCES={"162173":"Ryugu","275611":"1999 XX262"}


def identity():
    code={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
          (Path(__file__),Path(low_thrust.__file__),Path(shipping.__file__))}
    return content_hash({"settings":SETTINGS,"code":code,"vectors":vector_hash(),
                         "annual_demand_kg":annual_demand()})


def annual_demand():
    return reference_design()["replication"]["shipped"]*SETTINGS["construction_tori_per_year"]


def trajectory_identity():
    return content_hash({"solver":hashlib.sha256(Path(low_thrust.__file__).read_bytes()).hexdigest(),
        "vectors":vector_hash(),"segments":SETTINGS["segments"],
        "step_days":SETTINGS["step_days"],"maxiter":SETTINGS["maxiter"]})


def candidates(eph,origin,target,start,end,count=3):
    """Sparse impulsive seeds, not a global low-thrust launch-window search."""
    t,dv,tof=windows.curve(eph,origin,target,start,end,tofs=np.arange(240.,721.,60.))
    dips=windows.local_minima(dv,24)
    eligible=[bounded_refine(eph,origin,target,float(t[i]),float(tof[i]),start,end)
              for i in dips if dv[i]<=7000]
    # Keep the better nearby seed, then retain the earliest basins for startup.
    return windows.deduplicate(eligible,500)[:count]


def run():
    signature=identity()
    data={"input_hash":signature,"trajectory_hash":trajectory_identity(),"settings":SETTINGS,"annual_demand_kg":annual_demand(),
          "vector_hash":vector_hash(),"complete":False,"attempts":{},"networks":{}}
    if RESULTS.exists():
        previous=json.loads(RESULTS.read_text())
        if previous.get("input_hash")==signature:data=previous
        elif previous.get("trajectory_hash")==data["trajectory_hash"]:
            data["attempts"]=previous["attempts"]
    eph=Ephemeris(NETWORK_VECTORS)
    # A changed optimiser need not discard a physically verified upper bound.
    # Recheck old controls against current dynamics/endpoints before reusing;
    # failed attempts must be searched again under the changed algorithm.
    if RESULTS.exists() and previous.get("trajectory_hash")!=data["trajectory_hash"]:
        for key,record in previous["attempts"].items():
            if record.get("segments")!=SETTINGS["segments"] or record.get("step_days")!=SETTINGS["step_days"]:
                continue
            engine=low_thrust.Engine(**record["engine"])
            r0,v0=eph.state(record["origin"],record["departure_jd"])
            r1,v1=eph.state(record["target"],record["arrival_jd"])
            checked=low_thrust.verify(r0,v0,np.array(record["controls"]),record["wet_ratio"],
                record["flight_days"],engine,record["delivered_kg"],r1,v1)
            seed=dict(record,verification=checked,accepted=bool(checked["accepted"] and
                1<=record["wet_ratio"]<=engine.max_wet_ratio))
            seed=low_thrust.polish(eph,seed)
            if seed["accepted"]:
                q=seed["wet_ratio"];final=seed["verification"]["final_mass_ratio"]
                propellant=(q-final)*seed["delivered_kg"]
                seed.update(propellant_kg=propellant,
                    energy_j=propellant*engine.exhaust_m_s**2/(2*engine.efficiency),
                    loaded_propellant_kg=(q-1)*seed["delivered_kg"],
                    final_reserve_kg=(final-1)*seed["delivered_kg"],
                    integrated_delta_v_m_s=engine.exhaust_m_s*float(np.log(q/final)))
                seed["optimizer_success"]=False
                seed["mass_objective_converged"]=False
                seed["optimizer_message"]="Revalidated feasible controls from an earlier optimiser; objective not reoptimised"
                seed["revalidated_from_solver_hash"]=previous["trajectory_hash"]
                data["attempts"][key]=seed
    start,end=jd_of(SETTINGS["start_year"]),jd_of(SETTINGS["end_year"])
    def save():RESULTS.write_text(json.dumps(data,indent=1,allow_nan=False)+"\n")
    def leg(origin,target,t,days,engine,delivered):
        key=content_hash([origin,target,t,days,asdict(engine),delivered])
        if key not in data["attempts"]:
            print("solve",engine.name,origin,"->",target,windows.date_str(t),days,flush=True)
            result=low_thrust.solve(eph,origin,target,t,days,engine,delivered,
                segments=SETTINGS["segments"],step_days=SETTINGS["step_days"],maxiter=SETTINGS["maxiter"])
            data["attempts"][key]=result;save()
            print("  accepted",result["accepted"],result.get("verification"),flush=True)
        return data["attempts"][key]
    for source in SOURCES:
        seeds=candidates(eph,source,"433",start,jd_of(SETTINGS["departure_end_year"]),SETTINGS["cycles_per_source"])
        for specification in SETTINGS["engines"]:
            engine=low_thrust.Engine(**specification,power_1au_w=SETTINGS["power_1au_w"])
            key=source+":"+engine.name
            cycles=[]
            for dv,t,days in seeds:
                outbound=None
                for duration in dict.fromkeys([days,min(900.,days+90)]):
                    trial=leg(source,"433",t,duration,engine,SETTINGS["dry_kg"]+SETTINGS["payload_kg"])
                    if trial["accepted"]:outbound=trial;break
                if outbound is None:continue
                earliest=outbound["arrival_jd"]+SETTINGS["turnaround_days"]
                returns=candidates(eph,"433",source,earliest,min(earliest+365.25*5,jd_of(2073)),count=3)
                inbound=None
                for _,rt,rf in returns:
                    trial=leg("433",source,rt,rf,engine,SETTINGS["dry_kg"])
                    if trial["accepted"]:inbound=trial;break
                if inbound is not None:
                    cycles.append(shipping.cycle(outbound,inbound,SETTINGS["payload_kg"],SETTINGS["dry_kg"],SETTINGS["turnaround_days"]))
            data["networks"][key]={"source":source,"engine":asdict(engine),"cycles":cycles,
                "schedules":{str(n):shipping.schedule(cycles,start,end,annual_demand(),n) for n in SETTINGS["fleets"]}}
            save()
    data["complete"]=True;save()
    return data


def report():
    d=json.loads(RESULTS.read_text())
    if not d.get("complete") or d.get("input_hash")!=identity():
        raise ValueError("shipping results incomplete or stale; rerun --solve")
    s=d["settings"]
    lines=["# Finite-thrust trajectories and a dated shipping schedule", "",
        "First computational study, 31 October 2026. Feasible trajectories and schedules are conditional on "
        "the assumed freighter hardware and refuelling infrastructure. This is not a flight-ready mission or a "
        "proof of the optimal supplier, fleet, propulsion system or construction schedule. "
        "2030–2050 are illustrative orbital epochs, not a proposed habitat construction timeline.","",
        "## Assumptions", "",
        f"A ship delivers {s['payload_kg']/1e6:g} kt of mixed N₂, water and organics. Its dry mass is "
        f"{s['dry_kg']/1e3:g} t, including the array, power electronics, propulsion and tanks. "
        f"It has {s['power_1au_w']/1e6:g} MW at 1 AU, capped at that electrical power inside 1 AU and "
        "falling as 1/r² outside. These hardware numbers are guesses, not sourced mass budgets. "
        "The assumed dry mass is held equal between propulsion cases for comparison; no mass-driver hardware "
        "design or containment/handling system for its large propellant loads is established.","",
        f"Electric propulsion: {s['engines'][0]['exhaust_m_s']/1000:g} km/s exhaust, "
        f"{100*s['engines'][0]['efficiency']:g}% electrical-to-jet efficiency. The hypothetical onboard "
        f"residue mass driver: {s['engines'][1]['exhaust_m_s']/1000:g} km/s, "
        f"{100*s['engines'][1]['efficiency']:g}%. Both may load up to eleven times their delivered vehicle-plus-payload "
        "mass in propellant. Every departure refuels locally: the supplier provides outbound propellant, Eros "
        "provides return propellant. Producing and storing compatible propellant at both ends is an explicit "
        "infrastructure assumption, not a demonstrated capability. Tank capacity is not separately constrained.","",
        f"One 900 m torus per ten years consumes {d['annual_demand_kg']/1e6:.2f} kt of shipped products per year. "
        "Demand is continuous and constant, not exponential cluster growth. Ships begin at their supplier; "
        f"unloading/refuelling and return loading each take {s['turnaround_days']:g} days. Initial cargo stock "
        "at Eros is supplied before the horizon, outside this schedule. There are no construction-line, "
        "supplier mining/processing, propellant production, docking or launch-rate limits, losses, spares, "
        "hotel power or contingency reserves. Aggregate cargo is treated as fungible; individual commodity "
        "inventories and fuel reserves still need a coupled source-processing model.","",
        "Ryugu is the sampled chemical reference. XX262's recoverable nitrogen remains unmeasured; "
        "its shipments are conditional on useful resources being established. See the "
        "[composition evidence audit](asteroid-evidence.md). Cargo capacity and propellant production "
        "are not deducted from supplier inventories in this study.","",
        "## Trajectory method and acceptance", "",
        "Backward direct shooting from the arrival state, with constant inertial throttle vectors in equal-duration segments; Sun gravity, "
        "variable mass, and distance-dependent solar power. A feasibility phase starts from a zero-thrust "
        "guess, before SLSQP minimises initial mass at fixed dates, "
        "with rendezvous constraints and throttle norm ≤1. Backward mass flow stays positive during optimisation. "
        "The arrival target carries a 0.1% numerical fuel reserve above dry vehicle and cargo; real contingency "
        "reserves are additional. A final feasibility projection "
        "can refine the constraints. Near-feasible controls can also be corrected against adaptive backward "
        "integration before the final independent forward check, removing RK4 error near the power-cap corner. "
        "Integrated Horizons states define the endpoints; planetary forces along "
        "the flight, gravity assists and close approaches are not modelled. The dynamics can make multiple "
        "revolutions, but the search does not enumerate revolution families.","",
        "The equations are `F_max = 2 η P / v_e`, `dm/dt = -F_max |u| / v_e`, "
        "and `dv/dt = -μ r / |r|³ + F_max u / m`, with `|u| ≤ 1`. For fixed exhaust speed "
        "and efficiency, flight electricity is `m_propellant v_e² / (2 η)`. Unused arrival fuel "
        "is not counted as consumed propellant or as cargo.","",
        "Each result is reintegrated with adaptive DOP853, segment by segment, independently of the RK4 "
        "used in optimisation. It must arrive within 10 km and 0.1 m/s, stay above 0.5 AU, respect throttle "
        "within 1e-7 and retain the required delivered mass within 1e-7 of it. These are screening tolerances, "
        "not docking requirements. Feasible iteration-limited results are retained as upper bounds; objective "
        "convergence is recorded separately and does not establish global optimality. Failed solves are "
        "recorded as 'not found', not as proof that a route is impossible.","",
        "Only a sparse menu is searched: three promising departure dates per source, seeded by local "
        "minima of a 5-day impulsive scan with 240–720-day flights, refined within 60–900 days, dates separated by ≥500 days, and "
        "one alternative duration 90 days longer if needed. Return seeds are searched after the outbound "
        "arrival and turnaround, up to five years later. This does not compare all possible off-window "
        "departures, low-thrust windows, payloads, power levels or exhaust speeds.","",
        "Method references: [ESA zero-order-hold low-thrust transcription](https://esa.github.io/pykep/trajopt.html), "
        "[SciPy SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html), "
        "[SciPy solve_ivp / DOP853](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html). "
        "This implementation uses SciPy, not pykep.","",
        "## Verified reusable cycles", "",
        "Return arrivals are followed by the source turnaround before a ship is available again. "
        "Electrical energy and propellant below include both flights. Energy to manufacture propellant "
        "or process cargo is additional.","",
        "| Supplier / propulsion | Cargo departure | Delivery | Return departure | Ready at supplier | Flight propellant kt | Flight electricity PJ |",
        "|---|---|---|---|---|---:|---:|"]
    for network in d["networks"].values():
        name=SOURCES[network["source"]]+" / "+network["engine"]["name"]
        if not network["cycles"]:lines.append(f"| {name} | No verified round trip found in the sampled menu | | | | | |")
        for c in network["cycles"]:
            prop=c["outbound"]["propellant_kg"]+c["return"]["propellant_kg"]
            energy=c["outbound"]["energy_j"]+c["return"]["energy_j"]
            dates=[windows.date_str(c[k]) for k in ("departure_jd","delivery_jd","return_departure_jd","ready_jd")]
            lines.append(f"| {name} | "+" | ".join(dates)+f" | {prop/1e6:.2f} | {energy/1e15:.3f} |")
    lines += ["","## Fleet and host-stock trade-offs", "",
        "An integer linear programme allocates voyages to the verified cycles. A ship cannot depart again "
        "before its return and turnaround; explicit ship IDs verify the allocation. Host inventory is checked "
        "immediately before every delivery and at horizon end. Final stock must be at least initial stock, "
        "so a large initial stock cannot hide a net shipping deficit. First minimise initial stock, then voyages, "
        "then flight electricity among the remaining ties. Tie-break solver statuses are saved. "
        "'Not supported' means this fleet cannot meet the stated demand on this sparse menu, not that no "
        "better schedule exists. No inference is made beyond 2050.","",
        "| Supplier / propulsion | Ships | Installed electrical power at 1 AU GW | Voyages | Initial host stock kt | Delivered kt | Flight electricity PJ |",
        "|---|---:|---:|---:|---:|---:|---:|"]
    for network in d["networks"].values():
        name=SOURCES[network["source"]]+" / "+network["engine"]["name"]
        for n,v in network["schedules"].items():
            power=int(n)*network["engine"]["power_1au_w"]/1e9
            if not v["feasible"]:lines.append(f"| {name} | {n} | {power:.2f} | Not supported | | | |")
            else:lines.append(f"| {name} | {n} | {power:.2f} | {v['voyages']} | {v['initial_stock_kg']/1e6:.1f} | {v['delivered_kg']/1e6:.1f} | {v['energy_j']/1e15:.2f} |")
    lines += ["", "## Dated deliveries for the smallest supported tested fleet", "",
        "These are actual allocations from the integer schedule, not merely candidate launch windows. "
        "The smallest feasible fleet among the three tested sizes is shown; this is not the minimum fleet "
        "over all possible trajectories. Stock values are immediately before and after each delivery. "
        "Ship identities and return availability are saved in the JSON.", "",
        "| Supplier / propulsion | Fleet ships | Ships sailing | Cargo departure | Delivery | Cargo kt | Host stock before / after kt |",
        "|---|---:|---:|---|---|---:|---:|"]
    for network in d["networks"].values():
        supported=[(int(n),v) for n,v in network["schedules"].items() if v["feasible"]]
        if not supported:continue
        n,v=min(supported,key=lambda pair:pair[0])
        name=SOURCES[network["source"]]+" / "+network["engine"]["name"]
        inventory={row["jd"]:row for row in v["inventory"]}
        for event in v["events"]:
            stock=inventory[event["delivery_jd"]]
            lines.append(f"| {name} | {n} | {event['voyages']} | "
                f"{windows.date_str(event['departure_jd'])} | {windows.date_str(event['delivery_jd'])} | "
                f"{event['cargo_kg']/1e6:.1f} | {stock['before_kg']/1e6:.1f} / "
                f"{(stock['before_kg']+stock['delivered_kg'])/1e6:.1f} |")
    attempts=list(d["attempts"].values());accepted=[v for v in attempts if v["accepted"]]
    lines += ["","## Numerical record", "",
        f"{len(attempts)} trajectory attempts, {len(accepted)} independently accepted. "
        f"{sum(not v['optimizer_success'] for v in accepted)} accepted legs did not converge the mass objective; "
        "their costs are feasible upper bounds. The JSON saves every control vector, engine setting, "
        "epoch, mass, optimizer status, verification error and selected ship ID. Input hashes cover code, "
        "settings, cargo demand and the saved orbital data; stale reports are rejected.","",
        "## Reproduce", "", "```bash", "python -m pip install -r requirements.txt",
        "python -m logistics_model.shipping_study --solve --report",
        "python -m unittest tests.test_shipping", "```", "",
        "Solving uses saved ephemerides and no network. Individual trajectory attempts are cached by solver/data/numerical "
        "settings plus leg parameters; changing fleet sizes or report text can reuse them. Older feasible controls "
        "are reused only after revalidation against current dynamics and endpoints, labelled "
        "as upper bounds rather than a new converged optimisation. Failed attempts are not reused after an optimiser change. "
        "The full report also validates the study code, settings and demand. --report alone is fast. This closes a first finite-thrust and "
        "dated-fleet modelling step; it leaves hardware sizing, propellant sourcing, denser launch searches, "
        "source throughput, reserves and uncertainty sweeps open.", ""]
    REPORT.write_text("\n".join(lines))
    return REPORT


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solve",action="store_true")
    parser.add_argument("--report",action="store_true")
    args=parser.parse_args()
    if args.solve:run()
    if args.report:print(report())


if __name__=="__main__":main()
