"""Offline report from the saved network search and dated transfers."""

import json
from pathlib import Path

from . import catalogue, networks, windows

REPORT = Path(__file__).resolve().parents[1] / "reports" / "asteroid-networks.md"


def label(key, hosts, candidates):
    return "Earth" if key=="Earth" else hosts[key]["name"] if key in hosts else candidates[key]["name"]


def evidence_class(key, body, audit):
    if key in ("162173","101955"):
        return "sample return"
    if key=="275611":
        return "B spectra; tentative Ch feature"
    if key=="778852":
        return "D? spectrum / radar size; N unknown"
    if key=="2015 AY245":
        return "T spectrum; N unknown"
    # Catalogue types are observations, not hydration or N measurements.
    if body["spec"] and body["spec"] in set(catalogue.C_COMPLEX_BUS)|set(catalogue.C_COMPLEX_THOLEN):
        return body["spec"]+" spectrum; N unknown"
    entry=audit.get("suppliers",{}).get(key,{})
    try:
        types=entry["taxonomy"]["data"][0]["datacloud"]["taxonomy"]
        carbon=[x for x in types if x.get("class") in ("B","C","Cb","Cg","Ch","Cgh") and x.get("method")=="Spec"]
        if carbon:
            return "/".join(sorted(set(x["class"] for x in carbon)))+" spectrum; N unknown"
        spectra=[x["class"] for x in types if x.get("method")=="Spec"]
        if spectra:
            return "/".join(sorted(set(spectra)))+" spectrum; N unknown"
        if types:
            return "/".join(sorted(set(x["class"] for x in types)))+" colours only; N unknown"
    except (KeyError,IndexError,TypeError):
        pass
    return (body["spec"]+" / dark; N unknown") if body["spec"] else "dark only; N unknown"


def generate():
    hd=json.loads(networks.HOST_DATA.read_text())
    hosts=hd["hosts"]
    screen=json.loads(networks.SCREEN_DATA.read_text())
    if set(screen["hosts"])!=set(hosts):
        raise ValueError("screen incomplete")
    dated=json.loads(networks.WINDOW_DATA.read_text())
    if dated.get("vector_hash") != networks.vector_hash():
        raise ValueError("ephemeris changed; rerun --windows before generating the report")
    expected={o+"->"+h for o,h in networks.dated_pairs(screen)}
    if set(dated["pairs"])!=expected:
        raise ValueError("dated search incomplete or selection changed; rerun --windows")
    candidates=catalogue.load()["candidates"]
    audit=json.loads(networks.EVIDENCE_DATA.read_text()) if networks.EVIDENCE_DATA.exists() else {}
    front=networks.pareto_front(hosts,screen)
    lines=["# Asteroid host–supplier networks", "",
        "A first screening study, 31 October 2026. Extends the Eros reference to other silicate near-Earth hosts. "
        "The result is a shortlist for investigation, not a verified resource inventory or an executable transport plan.", "",
        "## Ranked research shortlist", "",
        "This is a judgement about which networks to investigate first for this project's near-Earth, "
        "locally built habitats. It is not a universal optimum. Long-term inventory and evidence quality "
        "take precedence over a small saving in the best transfer found.", "",
        "| Priority | Host and supplier network | Reason to investigate | Main reservation |",
        "|---|---|---|---|",
        "| 1 | Eros + 1999 XX262 / 2015 DX198; Ryugu and Bennu as sampled comparisons | Large, spacecraft-characterised host; several alternative delivery routes | Strong seasons; XX262 hydration is tentative and the dark suppliers' nitrogen is unknown |",
        "| 2 | 1991 VH + 2011 AM24 / 2015 CV13 / 2015 AY245 | Milder seasons and an unusually inexpensive AM24 route | Finite LL-like metal inventory; fast-rotating binary; no sampled supplier below the adopted cutoff |",
        "| 3 | 1999 YB + Bennu and the additional candidates in the dated table | Mildest seasons among the retained hosts, with a sampled-source comparison | Host diameter is inferred from H and assumed albedo; potentially only a few small tori |",
        "| 4 | Torifune + 2001 WT1 / 2009 FD | Smaller solar array and a low-cost WT1 route; possible nursery | Limited host inventory, uncertain WT1 resources; catalogue size needs replacing with a volume model |", "",
        "Geographos, Bacchus, Norwan and 2001 QQ142 remain trade-off alternatives in the tables; their "
        "presence on the central-estimate Pareto front does not establish a superior settlement site. "
        "Itokawa and Apophis are useful transport comparisons, but the conservative LL free-metal model "
        "gives only about one complete 900 m torus, before recovery/accessibility losses: that does not "
        "support a self-reproducing pair at those sites without another material source. "
        "L/H-rich material or silicate iron extraction changes that conclusion and needs its own evidence.", "",
        "## What was searched", "",
        f"The JPL SBDB query returned {len(hd['query_snapshot']['data'])} asteroids with a recorded spectral classification. "
        f"The stated cuts retained {len(hosts)} hosts: S-complex/Q, or L/K silicate candidates, with q > 0.7 AU, Q < 2.5 AU, "
        "eccentricity < 0.4, inclination < 15° and H < 20; the existing reference hosts are retained explicitly. "
        "This is limited by SBDB's sparse taxonomy coverage, not a census of every potentially suitable NEO. "
        "Spectral L does not mean L ordinary chondrite. Differentiated objects and unclassified metal-rich hosts are outside this search.", "",
        f"Each host was screened against the existing {len(candidates)} C-complex/dark candidates (snapshot 30 October 2026). "
        "The first grid used 30° departure/arrival true-anomaly steps and 60–720-day flights in 60-day steps; "
        "the best 18 per host were screened again at 15°. The best six were refined with the existing 10° grid and "
        "eight-seed pattern search, as were Bennu, Ryugu and the two best screened C-complex spectral candidates. "
        "Rounded supplier elements are adequate for screening but not final mission design. Host elements were fetched at full precision; "
        "Apophis uses Horizons' post-flyby orbit at 1 January 2030 instead of its current pre-2029 orbit. "
        "Grid screening can miss narrow minima: these are the best solutions found, not certified global minima.", "",
        "The dated stage uses JPL Horizons' integrated states, every ten days from 2027 to 2077, interpolated using "
        "the existing cubic Hermite method. Departure dates span 2028–2072 in five-day steps; flights span 60–900 days "
        "in ten-day steps and are refined while keeping those bounds. Transfers are prograde, zero-revolution, "
        "two-impulse rendezvous. Both acceleration and braking are charged. Earth departure figures are heliocentric "
        "rendezvous costs: launch, Earth escape, capture and the spacecraft's mass are additional.", "",
        "## Host comparison", "",
        "Compare the columns rather than one weighted score. Array × is Q²: panel area relative to the same constant "
        "load at 1 AU, sized at aphelion. Seasonal ratio is perihelion/aphelion sunlight, not a prediction of interior temperature. "
        "Tori are complete 900 m or 1.6 km designs with three farm tiers; capacity uses the existing free-metal/shield "
        "budget, including the hub/factory allowance. LL/L capacities are material scenarios unless composition is established. "
        "They assume the entire asteroid is accessible and the model's assumed metal is recovered.", "",
        "| Host | Spectral record | D km | Year yr | Sunlight range × Earth | Seasonal ratio | Array × | 900 m tori LL / L | 1.6 km tori LL / L | Lowest phase-free Δv found |",
        "|---|---|---:|---:|---|---:|---:|---:|---:|---:|"]
    for k,h in sorted(hosts.items(),key=lambda kv:networks.sunlight_metrics(kv[1]["elements"])["season_ratio"]):
        sun=screen["hosts"][k]["sunlight"]
        best=min(v["best"] for v in screen["hosts"][k]["suppliers"].values() if "best" in v)/1000
        marker="*" if h["diameter_source"].startswith("H ") else ""
        caps=[networks.host_capacity(h,r,c) for r,c in ((900,"LL"),(900,"L"),(1600,"LL"),(1600,"L"))]
        lines.append(f"| {h['name']} | {h['spec']} | {h['diameter_km']:.3g}{marker} | {sun['year_earth_years']:.2f} | "
            f"{sun['min_sunlight']:.2f}–{sun['max_sunlight']:.2f} | {sun['season_ratio']:.2f} | {sun['array_factor']:.2f} | "
            f"{caps[0]:.1f} / {caps[1]:.1f} | {caps[2]:.1f} / {caps[3]:.1f} | {best:.2f} km/s |")
    lines += ["", "* Diameter estimated from H at an assumed albedo of 0.23. These are not measured sizes. "
        "Mass uses measured GM where present (notably Eros and Itokawa); otherwise it uses diameter and 2 t/m³. "
        "For H-only sizes, albedos 0.1–0.4 change mass to about 0.44–3.49× the tabulated proxy, before density uncertainty. "
        "For a thermally modelled diameter, even a small formal error may exclude substantial model uncertainty.", "",
        "Central-estimate Pareto front (smaller array, smaller seasonal ratio, smaller best Δv, larger LL inventory): "
        + "; ".join(hosts[k]["name"] for k in front)+". This front ignores evidence quality and is not robust to uncertain sizes/compositions. "
        "The dated stage covers it plus Eros, 1999 YB, 1991 VH, Torifune, Geographos, Didymos and Itokawa.", "",
        "## Dated host–supplier routes", "",
        "All routes use the same 6 km/s service cutoff for comparison; it is a study choice, not an engineering limit. "
        "A retained opportunity is a refined local minimum, with no two departures within 120 days. "
        "The gap is the largest spacing between these selected arrival opportunities, including the beginning and end "
        "of the 2028–2072 horizon. It is not a continuous no-service interval: departures away from minima may also be usable.", "",
        "| Host | Supplier | Composition evidence | Best Δv km/s | Departure | Flight days | Retained ≤6 km/s opportunities | Largest selected-arrival gap yr |",
        "|---|---|---|---:|---|---:|---:|---:|"]
    for key,v in dated["pairs"].items():
        if v["origin"]=="Earth":continue
        o,h=v["origin"],v["target"];dv,t,tof=v["best"]
        lines.append(f"| {hosts[h]['name']} | {candidates[o]['name']} | {evidence_class(o,candidates[o],audit)} | "
                     f"{dv/1000:.2f} | {windows.date_str(t)} | {tof:.0f} | {len(v['service_windows'])} | {v['arrival_gaps']['max_years']:.1f} |")
    lines += ["", "## Supplier redundancy and stock", "",
        "Two alternatives are shown: sampled bodies only (Bennu/Ryugu), and all dated candidate routes. "
        "The latter assumes every listed candidate proves useful; it is an exploration target, not assured supply. "
        "Suppliers are counted once per host. Their inventory cannot also be allocated in full to every other host.", "",
        "The illustrative stock covers constant construction of one 900 m torus per ten years, using its shipped "
        "N₂ + water + organics demand. It is gap × annual cargo, with no freighter payload, processing rate, loss, "
        "contingency reserve or exponential cluster growth. It is not a complete logistics stock requirement.", "",
        "| Host | Earth → host best km/s | Sampled-source selected-arrival gap yr | All-candidate gap yr | Illustrative cargo stock kt |",
        "|---|---:|---:|---:|---:|"]
    target_ids=sorted(set(v["target"] for v in dated["pairs"].values()),key=int)
    shipped=networks.reference_design()["replication"]["shipped"]
    for h in target_ids:
        routes=[v for v in dated["pairs"].values() if v["target"]==h and v["origin"]!="Earth"]
        all_dates=[w[1]+w[2] for v in routes for w in v["service_windows"]]
        sample_dates=[w[1]+w[2] for v in routes if v["origin"] in ("101955","162173") for w in v["service_windows"]]
        g=networks.opportunity_gaps(all_dates,dated["start_jd"],dated["end_jd"])
        gs=networks.opportunity_gaps(sample_dates,dated["start_jd"],dated["end_jd"])
        earth=dated["pairs"]["Earth->"+h]["best"][0]/1000
        lines.append(f"| {hosts[h]['name']} | {earth:.2f} | {gs['max_years']:.1f} | {g['max_years']:.1f} | {shipped*g['max_years']/10/1e6:.0f} |")
    lines += ["", "## Resource sensitivity", "",
        "For unmeasured suppliers the evidence-based lower bound is **zero useful nitrogen**. "
        "The positive cases below are deliberately illustrative, not confidence intervals or measured ore grades. "
        "For unvisited suppliers the base case borrows the existing model's 0.24 wt% N and 70% recovery; it does not assign those values "
        "as observations of other asteroids. Carbonaceous taxonomy and hydration do not establish nitrogen abundance.", "",
        "For unvisited bodies the lower positive scenario uses 0.8× diameter, 1.0 t/m³, 0.05 wt% N and 50% recovery; "
        "the higher uses 1.2× diameter, 1.6 t/m³, 0.25 wt% N and 90% recovery. Both retain the model's "
        "6.4 wt% available-water assumption and enforce the smaller of N and water capacity. These water assumptions "
        "also need validation. For Bennu/Ryugu, diameter and density stay fixed. Bennu uses 0.23 / 0.24 / 0.25 wt% N "
        "(Glavin et al. 2025); Ryugu uses 0.1437 / 0.1454 / 0.1471 wt% N (Yokoyama et al. 2025, Table 1). "
        "The Ryugu interval is the published ±2σ uncertainty on the sample-based mean, not a bound on the whole asteroid. "
        "Both bodies use 50 / 70 / 90% industrial recovery, an assumption separate from the sample measurements. "
        "Ryugu's base capacity is consequently ~54 small tori rather than ~89 under the common Bennu-like proxy. "
        "The wider habitat model retains that common proxy; only this network comparison uses body-specific N. "
        "Extracting soil organics/other nutrients, excavation accessibility and maintaining "
        "a residual asteroid are outside this capacity calculation.", "",
        "| Supplier | Catalogue D km | Evidence | 900 m tori: lower positive / base / higher | 1.6 km tori: lower positive / base / higher |",
        "|---|---:|---|---:|---:|"]
    used=sorted(set(v["origin"] for v in dated["pairs"].values())-{"Earth"})
    for k in used:
        b=candidates[k];caps=[]
        for radius in (900,1600):
            low,base,high=networks.supplier_scenarios(k,b,radius)
            caps.append(f"{low:.1f} / {base:.1f} / {high:.1f}")
        lines.append(f"| {b['name']} | {b['diameter_km']:.3g} | {evidence_class(k,b,audit)} | {caps[0]} | {caps[1]} |")
    lines += ["", "These are alternative allocations of the same supplier, not cumulative counts of 900 m and 1.6 km tori. "
        "For XX262, 1.48 km remains the working diameter; the published 2.426 km alternative would multiply volume "
        "and conditional inventory by about 4.4. It is not folded into the higher scenario as though it were established.", "",
        "## Evidence audit and research priorities", "",
        "See [asteroid-evidence.md](asteroid-evidence.md) for the composition and size audit. "
        "The raw supplier records are in `logistics_model/data/network_evidence.json`; selected host physical "
        "parameters retain their original JPL references in `network_hosts.json`. Multiple catalogue entries or "
        "taxonomies need not represent independent observations.", "",
        "1. Keep Eros as the large, spacecraft-characterised reference; compare 1991 VH as a smaller mild-season "
        "LL-like host and 1999 YB as a low-eccentricity but poorly sized host. Their finite metal inventory matters "
        "more than a small Δv saving if the goal is many generations at the same site.",
        "2. Treat Torifune and Itokawa as nursery candidates rather than automatically extrapolating to an indefinitely "
        "growing cluster. Keep all mass estimates separate from measured free-metal abundance.",
        "3. Obtain or reanalyse spectra for the low-cost dark candidates before resource planning; for XX262, "
        "confirm the weak hydration feature and measure the 3 µm region. No unvisited candidate here has a verified "
        "recoverable-nitrogen inventory.",
        "4. Re-run the selected routes with low-thrust trajectories, propulsion/power/dry-mass constraints, full launch "
        "intervals and supplier throughput. Include multi-revolution arcs and perturbations along the transfer itself. "
        "The current model uses integrated endpoint states but a two-body transfer arc.",
        "5. Assess mining mechanics separately: spin, binaries, gravity, anchoring and excavation can distinguish "
        "otherwise similar orbits. 1991 VH is a binary and a fast rotator; low seasonal variation does not make "
        "its surface operations easy.", "",
        "## Validation", "",
        "The logistics and network tests cover a circular-orbit Lambert solution, the Hohmann transfer, "
        "resource bottlenecks, orbital sunlight, opportunity unions and the flight-time bounds. "
        "The saved endpoint checks independently query Horizons at the exact optimized dates for "
        "XX262 → Eros, AM24 → 1991 VH and 2010 CG18 → 2001 QQ142. "
        "They test interpolation and object identity, not global optimality or a full perturbed transfer. "
        "See `logistics_model/data/network_endpoint_checks.json` for the states and numerical differences.", "",
        "## Reproduce", "", "```bash", "python -m logistics_model.networks --fetch",
        "python -m logistics_model.networks --screen --spectral",
        "python -m logistics_model.networks --fetch-vectors --fetch-evidence",
        "python -m logistics_model.networks --windows",
        "python -m logistics_model.networks --verify",
        "python -m logistics_model.networks --report", "python -m unittest tests.test_networks tests.test_logistics", "```", "",
        "Use --fetch-vectors to resume missing bodies without changing the acquisition dates of cached data. "
        "Use --refresh-vectors to fetch every selected body again, then --windows to recompute routes. "
        "Screen caches are matched to hashes of their host/supplier inputs, and dated windows to a hash of the ephemeris bytes. "
        "The report rejects stale inputs/results. Only --fetch, --fetch-vectors, --refresh-vectors, --fetch-evidence and --verify "
        "need network access. The dated selection is the "
        "central-estimate Pareto front plus the named reference/comparison hosts, each with its three lowest refined "
        "costs, best screened spectral C-complex supplier, Ryugu, Bennu and Earth. Snapshots contain the exact selection "
        "and results. Start a fresh --screen by removing `network_screen.json`; an interrupted run resumes its saved hosts.", "",
        "Sources: [JPL SBDB query API](https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html), "
        "[SBDB object API](https://ssd-api.jpl.nasa.gov/doc/sbdb.html), "
        "[Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html), "
        "[SsODNet](https://ssp.imcce.fr/webservices/ssodnet/). "
        "Sample N sources: [Glavin et al. 2025](https://doi.org/10.1038/s41550-024-02472-9), "
        "[Yokoyama et al. 2025, Table 1](https://doi.org/10.2343/geochemj.GJ25002). The complete habitat demand comes from the "
        "current checked-in `habitat_model/assumptions.toml`; all resource assumptions remain provisional.", ""]
    REPORT.write_text("\n".join(lines))
    return REPORT
