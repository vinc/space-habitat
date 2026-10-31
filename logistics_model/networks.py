"""Screen near-Earth silicate hosts and their carbonaceous/dark suppliers.

An extension of the catalogue search, not a mission design. Network access is
explicit (--fetch); --screen and --report use snapshots. See reports/asteroid-networks.md.
"""

import argparse
import concurrent.futures
import csv
import io
import json
import math
import re
from functools import lru_cache
from datetime import date
from pathlib import Path

import numpy as np

from habitat_model import Design, evaluate, load, params
from habitat_model.materials import s_type_needed
from . import catalogue, transfers
from .ephemeris import DATA, VECTORS, _get, Ephemeris, fetch_vectors, jd_of
from . import windows

HOST_DATA = DATA / "network_hosts.json"
SCREEN_DATA = DATA / "network_screen.json"
WINDOW_DATA = DATA / "network_windows.json"
NETWORK_VECTORS = DATA / "network_vectors.npz"
EVIDENCE_DATA = DATA / "network_evidence.json"
CHECK_DATA = DATA / "network_endpoint_checks.json"
DATED_HOSTS = ("433", "137799", "35107", "98943", "1620", "65803", "25143", "99942")
ALIASES = {"433": "Eros", "25143": "Itokawa", "98943": "Torifune", "65803": "Didymos",
           "99942": "Apophis", "162173": "Ryugu", "101955": "Bennu",
           "275611": "1999 XX262", "252558": "2001 WT1", "2015 DX198": "2015 DX198"}
# A taxonomy letter L is not an L ordinary chondrite. L/K hosts below are only
# silicate candidates; their metallic yield needs separate verification.
HOST_TYPES = {"S", "Sa", "Sk", "Sl", "Sq", "Sr", "Sv", "S(IV)", "Q", "L", "Ld", "K"}
REFERENCE_IDS = {"433", "25143", "98943", "65803", "99942"}


def get_json(url, query):
    return json.loads(_get(url, query, timeout=45))


def post_flyby_apophis(body):
    """Use the post-2029 orbit for settlements; preserve the pre-flyby SBDB data."""
    response=get_json("https://ssd.jpl.nasa.gov/api/horizons.api",{
        "format":"json","COMMAND":"'99942;'","EPHEM_TYPE":"ELEMENTS","CENTER":"500@10",
        "TLIST":str(jd_of(2030)),"REF_PLANE":"ECLIPTIC","OUT_UNITS":"AU-D"})
    block=response["result"].split("$$SOE")[1].split("$$EOE")[0]
    el={k:float(v) for k,v in re.findall(r'\b(EC|IN|OM|W|A)\s*=\s*([-+\d.E]+)',block)}
    body["sbdb_elements"]=body["elements"]
    body["elements"]=[el[k] for k in ("A","EC","IN","OM","W")]
    body["epoch_jd"]=jd_of(2030)
    body["elements_source"]="JPL Horizons, post-2029 flyby, 2030-01-01 TDB"
    body["name"]="99942 Apophis (post-2029)"
    return body


def host_eligible(row):
    bus, tholen = (row.get("spec_B") or "").rstrip(":"), (row.get("spec_T") or "").rstrip(":")
    if bus not in HOST_TYPES and tholen not in {"S", "Q"}:
        return False
    a, e, inc = (float(row[k]) for k in ("a", "e", "i"))
    return (0.7 < a * (1 - e) and a * (1 + e) < 2.5 and e < 0.4
            and inc < 15 and row.get("H") is not None and float(row["H"]) < 20)


def fetch_hosts():
    fields = "full_name,pdes,a,e,i,om,w,H,diameter,albedo,spec_B,spec_T"
    query = {"fields": fields, "sb-kind": "a", "sb-group": "neo",
             "sb-cdata": json.dumps({"OR": ["spec_B|DF", "spec_T|DF"]})}
    snapshot = get_json("https://ssd-api.jpl.nasa.gov/sbdb_query.api", query)
    rows = [dict(zip(snapshot["fields"], r)) for r in snapshot["data"]]
    out = {}
    for row in rows:
        if not host_eligible(row) and row["pdes"] not in REFERENCE_IDS:
            continue
        # Full precision for selected hosts, plus physical-data provenance.
        obj = get_json("https://ssd-api.jpl.nasa.gov/sbdb.api",
                       {"sstr": row["pdes"], "full-prec": "true", "phys-par": "true"})
        el = {e["name"]: float(e["value"]) for e in obj["orbit"]["elements"]}
        phys = {p["name"]: p for p in obj.get("phys_par", [])}
        diameter = float(phys["diameter"]["value"]) if "diameter" in phys else None
        h = float(phys["H"]["value"]) if "H" in phys else float(row["H"])
        out[row["pdes"]] = {
            "name": row["full_name"].strip(), "designation": row["pdes"],
            "elements": [el[k] for k in ("a", "e", "i", "om", "w")],
            "epoch_jd": float(obj["orbit"]["epoch"]), "orbit_id": obj["orbit"]["orbit_id"],
            "H": h, "diameter_km": diameter if diameter else diameter_from_h(h, 0.23),
            "diameter_source": "SBDB physical parameter" if diameter else "H at assumed albedo 0.23",
            "spec": "/".join(x for x in (row["spec_B"], row["spec_T"]) if x),
            "physical_parameters": phys, "screen_eligible": host_eligible(row),
            "jpl_object": obj["object"],
        }
        if row["pdes"]=="99942":
            post_flyby_apophis(out[row["pdes"]])
        print("fetched", out[row["pdes"]]["name"], flush=True)
        # Checkpoint: a failed request never masquerades as a complete host set.
        HOST_DATA.write_text(json.dumps({"fetched": date.today().isoformat(), "complete": False,
                                        "query": query, "query_snapshot": snapshot, "hosts": out}, indent=1)+"\n")
    data = {"fetched": date.today().isoformat(), "complete": True,
            "source": "NASA/JPL SBDB query and individual-object APIs", "query": query,
            "query_snapshot": snapshot, "hosts": out}
    HOST_DATA.write_text(json.dumps(data, indent=1)+"\n")
    return data


def diameter_from_h(h, albedo):
    return 1329 / math.sqrt(albedo) * 10 ** (-h / 5)


def bulk_mass(diameter_km, density):
    return math.pi / 6 * (diameter_km * 1000) ** 3 * density


def sunlight_metrics(el):
    a, e = el[:2]
    q, ap = a * (1 - e), a * (1 + e)
    return {"q_au": q, "Q_au": ap, "min_sunlight": ap ** -2,
            "max_sunlight": q ** -2, "season_ratio": (ap / q) ** 2,
            "array_factor": ap ** 2, "year_earth_years": a ** 1.5}


@lru_cache(maxsize=None)
def reference_design(radius=900):
    return evaluate(params(load()), Design(radius_m=radius, n_tori=2 if radius==900 else 6,
                                          tiers_lit=3, host_class="LL", site="Eros"))


def supplier_capacity(body, nitrogen_wt, recovery, density=1190, diameter_factor=1.0, radius=900):
    """Conditional N+water capacity, not a measured resource or a guaranteed minimum.
    Water follows the existing 6.4 wt% assumption. Unknown N can be zero.
    """
    if not 0 <= nitrogen_wt <= 1 or not 0 <= recovery <= 1 or density <= 0 or diameter_factor <= 0:
        raise ValueError("invalid resource scenario")
    r = reference_design(radius)
    m = r["mass"]
    mass = bulk_mass(body["diameter_km"] * diameter_factor, density)
    by_n = mass * nitrogen_wt * recovery / (m["n2"] + m["farm_n2"])
    by_water = mass * params(load()).c_water_wt / r["materials"]["water_to_source"]
    return min(by_n, by_water)


def host_mass(body):
    """Prefer a measured GM, otherwise show the explicit 2 t/m³ proxy."""
    physical=body["physical_parameters"]
    if "GM" in physical:
        return float(physical["GM"]["value"]) * 1e9 / 6.67430e-11
    return bulk_mass(body["diameter_km"],2000)


def host_capacity(body, radius=900, metal_class="LL"):
    r=reference_design(radius)
    needed=s_type_needed(params(load()),r["mass"],metal_class)["s_type"]
    return host_mass(body)/needed


def pareto_front(hosts, screen):
    """No arbitrary weighted score: central-estimate nondominance on four axes.
    Smaller seasonal ratio, array factor and phase-free delta-v; larger LL inventory.
    Evidence quality is not a numeric score; this front is not uncertainty-robust.
    """
    objectives={}
    for k,h in hosts.items():
        sun=screen["hosts"][k]["sunlight"]
        dv=min(v["best"] for v in screen["hosts"][k]["suppliers"].values() if "best" in v)
        objectives[k]=(sun["season_ratio"],sun["array_factor"],dv,-host_capacity(h))
    return [k for k,v in objectives.items() if not any(
        all(a<=b for a,b in zip(w,v)) and any(a<b for a,b in zip(w,v))
        for j,w in objectives.items() if j!=k)]


def phase_minimum(origin, target):
    """The existing best_phase search, refining its eight seeds in one numpy batch.
    Same grid, trial directions and termination as transfers.best_phase. This
    avoids running the universal-variable solver eight times for each iteration.
    """
    nus=np.radians(np.arange(0,360,10.0))
    g1,g2,gt=np.meshgrid(nus,nus,np.arange(40,801,40)*transfers.DAY,indexing="ij")
    dv=transfers._delta_v(origin,target,g1,g2,gt)
    indices=np.unravel_index(np.argsort(dv,axis=None)[:8],dv.shape)
    x=np.stack([g1[indices],g2[indices],gt[indices]],axis=-1)
    f=dv[indices].copy()
    steps=np.tile([math.radians(5),math.radians(5),20*transfers.DAY],(8,1))
    directions=np.concatenate([np.eye(3),-np.eye(3)])
    for _ in range(10000):
        active=steps[:,0]>math.radians(.01)
        if not np.any(active):
            k=int(np.argmin(f))
            return float(f[k]),float(x[k,2]/transfers.DAY)
        ids=np.flatnonzero(active)
        trial=x[ids,None,:]+steps[ids,None,:]*directions[None,:,:]
        trial[:,:,2]=np.maximum(trial[:,:,2],5*transfers.DAY)
        fs=transfers._delta_v(origin,target,trial[:,:,0],trial[:,:,1],trial[:,:,2])
        best=np.argmin(fs,axis=1)
        values=fs[np.arange(len(ids)),best]
        improved=values<f[ids]
        keep=ids[improved]
        x[keep]=trial[np.flatnonzero(improved),best[improved]]
        f[keep]=values[improved]
        steps[ids[~improved]]/=2
    raise RuntimeError("phase refinement failed to converge")


def screen_hosts(refine_count=6):
    hosts = json.loads(HOST_DATA.read_text())
    if not hosts.get("complete"):
        raise ValueError("host fetch incomplete; rerun --fetch")
    suppliers = catalogue.load()
    saved = dict(transfers.ELEMENTS)
    out = {"host_snapshot": hosts["fetched"], "supplier_snapshot": suppliers["fetched"],
           "method": "prograde, zero-revolution, two-impulse; independent phases; coarse30/refine15/best10",
           "settings": {"coarse_deg": 30, "coarse_tof_days": [60,720,60],
                        "second_pass_count": 18, "refine_count": refine_count}, "hosts": {}}
    if SCREEN_DATA.exists():
        previous=json.loads(SCREEN_DATA.read_text())
        if all(previous.get(k)==out[k] for k in ("host_snapshot","supplier_snapshot","settings")):
            out["hosts"]=previous["hosts"]
    try:
        for host_id, host in hosts["hosts"].items():
            if host_id in out["hosts"]:
                continue
            transfers.ELEMENTS[host_id] = tuple(host["elements"])
            results = {}
            for key, candidate in suppliers["candidates"].items():
                transfers.ELEMENTS[key] = tuple(candidate["elements"])
                results[key] = {"coarse": catalogue.coarse(key, host_id, step_deg=30)}
            shortlist = sorted(results, key=lambda k: results[k]["coarse"])[:18]
            for key in shortlist:
                results[key]["screen15"] = catalogue.coarse(key, host_id)
            refine = sorted(shortlist, key=lambda k: results[k]["screen15"])[:refine_count]
            # The sample-return references are always retained even if distant.
            for key in dict.fromkeys(refine + ["162173", "101955"]):
                dv, tof = phase_minimum(key, host_id)
                results[key].update(best=dv, days=tof)
            out["hosts"][host_id] = {"sunlight": sunlight_metrics(host["elements"]), "suppliers": results}
            SCREEN_DATA.write_text(json.dumps(out, indent=1)+"\n")
            best = sorted(((v["best"], k) for k,v in results.items() if "best" in v))[:3]
            print(host["name"], [(k,round(dv/1000,2)) for dv,k in best], flush=True)
    finally:
        transfers.ELEMENTS.clear()
        transfers.ELEMENTS.update(saved)
    return out


def refine_spectral_candidates():
    """Retain the two best screened C-complex spectra per host even if dark-only
    objects dominate its transport shortlist. Includes sample-return references.
    """
    hosts=json.loads(HOST_DATA.read_text())["hosts"]
    candidates=catalogue.load()["candidates"]
    screen=json.loads(SCREEN_DATA.read_text())
    c_types=set(catalogue.C_COMPLEX_BUS)|set(catalogue.C_COMPLEX_THOLEN)
    spectral=[k for k,c in candidates.items() if any(t in c_types for t in c["spec"].split("/"))]
    saved=dict(transfers.ELEMENTS)
    try:
        for host_id,host in hosts.items():
            results=screen["hosts"][host_id]["suppliers"]
            transfers.ELEMENTS[host_id]=tuple(host["elements"])
            chosen=sorted(spectral,key=lambda k:results[k]["coarse"])[:2]
            for key in chosen:
                if "best" not in results[key]:
                    transfers.ELEMENTS[key]=tuple(candidates[key]["elements"])
                    dv,tof=phase_minimum(key,host_id)
                    results[key].update(best=dv,days=tof)
            screen["hosts"][host_id]["spectral_shortlist"]=chosen
            SCREEN_DATA.write_text(json.dumps(screen,indent=1)+"\n")
    finally:
        transfers.ELEMENTS.clear();transfers.ELEMENTS.update(saved)
    return screen


def dated_pairs(screen):
    """Three low-cost candidates plus both sample-return references per host.
    The third candidate adds redundancy; no unobserved supplier is treated as proven.
    """
    pairs = []
    hosts=json.loads(HOST_DATA.read_text())["hosts"]
    selected=set(DATED_HOSTS)|set(pareto_front(hosts,screen))
    for h in sorted(selected,key=int):
        candidates = screen["hosts"][h]["suppliers"]
        ranked = sorted((v["best"], k) for k,v in candidates.items() if "best" in v)
        spectral=screen["hosts"][h].get("spectral_shortlist",[])
        for k in dict.fromkeys([k for _,k in ranked[:3]] + spectral[:1] + ["162173", "101955"]):
            pairs.append((k,h))
        pairs.append(("Earth",h))
    return pairs


def fetch_network_vectors():
    screen = json.loads(SCREEN_DATA.read_text())
    bodies = sorted(set(k for pair in dated_pairs(screen) for k in pair))
    base = np.load(VECTORS)
    arrays = {"jd": base["jd"]}
    cached=np.load(NETWORK_VECTORS) if NETWORK_VECTORS.exists() else None
    missing=[]
    for key in bodies:
        alias = ALIASES.get(key, key)
        if alias in base.files:
            arrays[key] = base[alias]
        elif cached is not None and key in cached.files and np.array_equal(cached["jd"],arrays["jd"]):
            arrays[key]=cached[key]
        else:
            missing.append(key)
    def one(key):
        # Quote the entire Horizons command, including designations with spaces.
        command = f"'{key};'" if key.isdigit() else f"'DES={key};'"
        for attempt in range(3):
            try:
                return key,fetch_vectors(command)
            except OSError:
                if attempt==2:
                    raise
    metadata={"fetched": date.today().isoformat(),
        "source": "NASA/JPL Horizons API, plus existing 2026-10-30 reference vectors",
        "frame": "heliocentric, ecliptic and mean equinox of J2000", "units": "km, km/s",
        "start": "2027-01-01", "stop": "2077-01-01", "step_days": 10,
        "aliases": ALIASES,"complete":False}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(one,key) for key in missing]
        for future in concurrent.futures.as_completed(futures):
            key,rows=future.result()
            if not np.array_equal(rows[:,0], arrays["jd"]):
                raise ValueError(f"{key}: Horizons dates differ from reference vectors")
            arrays[key] = rows[:,1:]
            print("vectors", key, flush=True)
            arrays["meta"]=np.array(json.dumps(metadata))
            np.savez_compressed(NETWORK_VECTORS,**arrays)
    metadata["complete"]=True
    arrays["meta"] = np.array(json.dumps(metadata))
    np.savez_compressed(NETWORK_VECTORS, **arrays)


def bounded_refine(eph, origin, target, departure, tof, start, end):
    """Refine without silently leaving the advertised 60–900-day flight envelope."""
    lo, hi = eph.span()
    if start < lo or end + 900 > hi:
        raise ValueError("ephemeris does not cover the complete departure/flight envelope")
    x = np.array([np.clip(departure,start,end),np.clip(tof,60,900)],float)
    f = float(windows.delta_v(eph,origin,target,*x))
    steps = np.array([2.5,5.0])
    while steps[0] > 0.01:
        trial = x + np.concatenate([np.diag(steps),-np.diag(steps)])
        trial[:,0] = np.clip(trial[:,0],start,end)
        trial[:,1] = np.clip(trial[:,1],60,900)
        fs = windows.delta_v(eph,origin,target,trial[:,0],trial[:,1])
        k = int(np.argmin(fs))
        if fs[k] < f:
            x,f = trial[k],float(fs[k])
        else:
            steps /= 2
    return [f,float(x[0]),float(x[1])]


def opportunity_gaps(arrivals, start, end):
    """Largest no-delivery interval inside a finite horizon, including its edges.
    These are opportunity gaps, not stock guarantees: payloads and failures are unmodelled.
    """
    if end <= start:
        raise ValueError("invalid horizon")
    dates = sorted(set(float(x) for x in arrivals if start <= x <= end))
    edges = [start]+dates+[end]
    gaps = [b-a for a,b in zip(edges,edges[1:])]
    return {"count":len(dates), "max_years":max(gaps)/365.25,
            "initial_years":(edges[1]-start)/365.25, "final_years":(end-edges[-2])/365.25}


def refine_windows(eph,origin,target,departures,tofs,start,end):
    """Batch the independent bounded pattern searches without changing their moves."""
    lo,hi=eph.span()
    if start<lo or end+900>hi:
        raise ValueError("ephemeris does not cover the full flight envelope")
    x=np.stack([np.clip(departures,start,end),np.clip(tofs,60,900)],axis=-1)
    f=windows.delta_v(eph,origin,target,x[:,0],x[:,1])
    steps=np.tile([2.5,5.0],(len(x),1))
    directions=np.concatenate([np.eye(2),-np.eye(2)])
    for _ in range(10000):
        active=steps[:,0]>.01
        if not np.any(active):
            return [[float(cost),float(a),float(b)] for cost,(a,b) in zip(f,x)]
        ids=np.flatnonzero(active)
        trial=x[ids,None,:]+steps[ids,None,:]*directions[None,:,:]
        trial[:,:,0]=np.clip(trial[:,:,0],start,end)
        trial[:,:,1]=np.clip(trial[:,:,1],60,900)
        fs=windows.delta_v(eph,origin,target,trial[:,:,0],trial[:,:,1])
        best=np.argmin(fs,axis=1); values=fs[np.arange(len(ids)),best]
        improved=values<f[ids]; keep=ids[improved]
        x[keep]=trial[np.flatnonzero(improved),best[improved]]
        f[keep]=values[improved]
        steps[ids[~improved]]/=2
    raise RuntimeError("dated refinement failed to converge")


def compute_dated():
    screen = json.loads(SCREEN_DATA.read_text())
    eph = Ephemeris(NETWORK_VECTORS)
    if not eph.meta.get("complete"):
        raise ValueError("network ephemeris fetch is incomplete")
    start,end = jd_of(2028),jd_of(2072)
    out={"start_jd":start,"end_jd":end,"fetched_vectors":eph.meta,
         "method":"5-day departures; 60–900-day flights in 10-day steps; batched bounded refinement; zero revolution",
         "service_limit_m_s":6000,"pairs":{}}
    if WINDOW_DATA.exists():
        previous=json.loads(WINDOW_DATA.read_text())
        if all(previous.get(k)==out[k] for k in ("start_jd","end_jd","method","fetched_vectors")):
            out["pairs"]=previous["pairs"]
    for origin,target in dated_pairs(screen):
        if origin+"->"+target in out["pairs"]:
            continue
        t,dv,tof = windows.curve(eph,origin,target,start,end)
        picks = windows.local_minima(dv,12)
        # Retain all basins near an absolute service limit, and the grid minimum.
        picks = sorted(set([int(np.argmin(dv))]+[i for i in picks if dv[i] <= max(7000,float(np.min(dv))+1000)]))
        found=refine_windows(eph,origin,target,t[picks],tof[picks],start,end)
        found=windows.deduplicate(found,120)
        best=min(found,key=lambda x:x[0])
        good=[list(w) for w in found if w[0] <= 6000]
        gaps=opportunity_gaps([w[1]+w[2] for w in good],start,end)
        out["pairs"][origin+"->"+target]={"origin":origin,"target":target,"best":list(best),
              "minima":[list(w) for w in found],"service_windows":good,"arrival_gaps":gaps,
              "grid_best_m_s":float(np.min(dv))}
        WINDOW_DATA.write_text(json.dumps(out,indent=1)+"\n")
        print(origin,"->",target,round(best[0]/1000,2),windows.date_str(best[1]),"service",len(good),flush=True)
    return out


def fetch_evidence():
    """Keep the selected suppliers' catalogue provenance and all SsODNet types.
    Unavailable records stay explicitly unavailable; no inferred composition is inserted.
    """
    screen=json.loads(SCREEN_DATA.read_text())
    selected=sorted(set(k for k,_ in dated_pairs(screen) if k!="Earth"))
    def one(key):
        entry={"designation":key}
        for label,url,query in (
            ("sbdb","https://ssd-api.jpl.nasa.gov/sbdb.api",{"sstr":key,"phys-par":"true","full-prec":"true"}),
            ("taxonomy","https://ssp.imcce.fr/webservices/ssodnet/api/datacloud.php",
             {"-name":"id:"+key.replace(" ","_"),"-resource":"taxonomy","-mime":"json"})):
            try:
                if label=="taxonomy" and key.isdigit():
                    fullname=entry.get("sbdb",{}).get("object",{}).get("fullname","")
                    named=re.match(r'^\d+\s+([^()]+)',fullname)
                    provisional=re.search(r'\(([^()]+)\)$',fullname)
                    if named:
                        query["-name"]="id:"+named[1].strip().replace(" ","_")
                    elif provisional:
                        query["-name"]="id:"+provisional[1].replace(" ","_")
                entry[label]=get_json(url,query)
            except Exception as exc:
                entry[label]={"unavailable":str(exc)}
        print("evidence",key,flush=True)
        return key,entry
    # Read-only independent requests; limit concurrency to avoid burdening services.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        entries=dict(pool.map(one,selected))
    base="https://raw.githubusercontent.com/maxmahlke/classy/main/data/mahlke2022/csv/"
    mahlke={}
    for file in ("class_asteroids.csv","class_visnir.csv","reference_spectra.csv"):
        try:
            data=_get(base+file,{})
            rows=list(csv.DictReader(io.StringIO(data)))
            mahlke[file]=[r for r in rows if (r.get("number")=="275611" or r.get("key")=="57")]
        except Exception as exc:
            mahlke[file]={"unavailable":str(exc)}
    out={"fetched":date.today().isoformat(),"sources":{"sbdb":"https://ssd-api.jpl.nasa.gov/sbdb.api",
         "taxonomy":"https://ssp.imcce.fr/webservices/ssodnet/api/datacloud.php",
         "mahlke":base},"suppliers":entries,"xx262_mahlke":mahlke}
    EVIDENCE_DATA.write_text(json.dumps(out,indent=1)+"\n")
    return out


def verify_endpoints():
    """Independent Horizons calls at the exact optimized endpoints for three routes.
    This checks interpolation/identity, not the optimality of the trajectory.
    """
    dated=json.loads(WINDOW_DATA.read_text())
    eph=Ephemeris(NETWORK_VECTORS)
    checks=[]
    for key in ("275611->433","778852->35107","477490->139622"):
        pair=dated["pairs"][key];dv,t,tof=pair["best"]
        states=[];errors=[]
        for body,jd in ((pair["origin"],t),(pair["target"],t+tof)):
            command=f"'{body};'" if body.isdigit() else f"'DES={body};'"
            query={"format":"json","COMMAND":command,"EPHEM_TYPE":"VECTORS","CENTER":"500@10",
                   "TLIST":str(jd),"REF_PLANE":"ECLIPTIC","REF_SYSTEM":"J2000","OUT_UNITS":"KM-S",
                   "VEC_TABLE":"2","CSV_FORMAT":"YES","OBJ_DATA":"NO"}
            for attempt in range(3):
                try:
                    response=get_json("https://ssd.jpl.nasa.gov/api/horizons.api",query)
                    break
                except OSError:
                    if attempt==2:raise
            line=response["result"].split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()[0]
            fields=[v.strip() for v in line.split(",")]
            exact=np.array([float(v) for v in fields[2:8]])*1000
            r,v=eph.state(body,jd)
            errors.append({"body":body,"jd":jd,"position_m":float(np.linalg.norm(exact[:3]-r)),
                           "velocity_m_s":float(np.linalg.norm(exact[3:]-v)),"exact_state_m_m_s":exact.tolist()})
            states.append(exact)
        r1,v1=states[0][:3],states[0][3:];r2,v2=states[1][:3],states[1][3:]
        a,b=transfers.lambert(r1,r2,tof*transfers.DAY)
        actual=float(np.linalg.norm(a-v1)+np.linalg.norm(v2-b))
        checks.append({"pair":key,"interpolated_delta_v_m_s":dv,"exact_endpoint_delta_v_m_s":actual,
                       "difference_m_s":actual-dv,"endpoints":errors})
        print("endpoint check",key,"difference m/s",actual-dv,flush=True)
    CHECK_DATA.write_text(json.dumps({"fetched":date.today().isoformat(),"source":"NASA/JPL Horizons API",
                                     "checks":checks},indent=1)+"\n")
    return checks


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--screen", action="store_true")
    ap.add_argument("--fetch-vectors", action="store_true")
    ap.add_argument("--windows", action="store_true")
    ap.add_argument("--fetch-evidence", action="store_true")
    ap.add_argument("--spectral", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args(argv)
    if args.fetch:
        fetch_hosts()
    if args.screen:
        screen_hosts()
    if args.spectral:
        refine_spectral_candidates()
    if args.fetch_vectors:
        fetch_network_vectors()
    if args.windows:
        compute_dated()
    if args.fetch_evidence:
        fetch_evidence()
    if args.verify:
        verify_endpoints()
    if args.report:
        from .network_report import generate
        print(generate())


if __name__ == "__main__":
    main()
