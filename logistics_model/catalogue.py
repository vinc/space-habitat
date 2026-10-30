"""A catalogue search for C-type partners (plan §5): near-Earth asteroids that could supply the hosts' volatiles.

Candidates from JPL's Small-Body Database, both kinds kept:
- classified in the C complex (Bus: B, C, Cb, Cg, Ch, Cgh; Tholen: B, C, F, G), H < 19.5;
- dark in NEOWISE's albedos (< 0.08: carbonaceous, or D/P-like), at least 0.3 km across.

For each candidate and host: the phase-free rendezvous Δv (`transfers.best_phase`) on the SBDB's osculating
elements, first on a coarse grid for all, then refined for the best few per host. Fetched and computed once
and kept in `logistics_model/data/` (the report reads it):

python -m logistics_model.catalogue --fetch          # needs the network, ~10 min
"""

import argparse
import json
import math
import sys
import urllib.parse
import urllib.request
from datetime import date

import numpy as np

from . import transfers
from .ephemeris import DATA, elements

CATALOGUE = DATA / "c_type_candidates.json"
HOSTS = ("Eros", "Itokawa", "Torifune", "Didymos")
C_COMPLEX_BUS = ("B", "C", "Cb", "Cg", "Ch", "Cgh", "C:", "Cb:", "Ch:")
C_COMPLEX_THOLEN = ("B", "C", "F", "G", "CF", "CG", "CB", "BF", "BC", "FC", "GC")
DENSITY = 1190.0              # kg/m³, Ryugu's bulk density (Hayabusa2), for every candidate
REFINE = 12                   # candidates per host refined with the full search


def _query(cdata):
    params = {"fields": "full_name,pdes,a,e,i,om,w,H,diameter,albedo,spec_B,spec_T", "sb-kind": "a",
              "sb-group": "neo", "sb-cdata": json.dumps(cdata)}
    url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=120) as r:
        data = json.loads(r.read().decode())
    return [dict(zip(data["fields"], row)) for row in data["data"]]


def candidates():
    """Fetch the candidates: {designation: {name, elements, H, diameter km, albedo, spectral types, why}}."""
    out = {}
    for row in _query({"OR": ["spec_B|DF", "spec_T|DF"]}):
        bus, tholen = (row["spec_B"] or "").strip(), (row["spec_T"] or "").strip()
        if (bus in C_COMPLEX_BUS or tholen in C_COMPLEX_THOLEN) and row["H"] and float(row["H"]) < 19.5:
            out[row["pdes"]] = _entry(row, "spectrum")
    for row in _query({"AND": ["albedo|LT|0.08", "diameter|GE|0.3"]}):
        if row["pdes"] in out:
            out[row["pdes"]]["why"] = "spectrum and albedo"
        else:
            out[row["pdes"]] = _entry(row, "albedo")
    return out


def _entry(row, why):
    d = float(row["diameter"]) if row["diameter"] else None
    if d is None and row["H"]:
        # Diameter from H at a C-type albedo of 0.05.
        d = 1329 / math.sqrt(0.05) * 10 ** (-float(row["H"]) / 5)
    return {"name": row["full_name"].strip(), "elements": [float(row[k]) for k in ("a", "e", "i", "om", "w")],
            "H": float(row["H"]) if row["H"] else None, "diameter_km": d,
            "albedo": float(row["albedo"]) if row["albedo"] else None,
            "spec": "/".join(x for x in ((row["spec_B"] or "").strip(), (row["spec_T"] or "").strip()) if x),
            "why": why}


def mass_kg(diameter_km):
    return math.pi / 6 * (diameter_km * 1e3) ** 3 * DENSITY


def coarse(origin, target, step_deg=15.0, tof_days=np.arange(60, 721, 60)):
    """The lowest Δv (m/s) on a grid of departure and arrival points and flight times, unrefined: a cheap
    screen, a little above the refined value."""
    nus = np.radians(np.arange(0, 360, step_deg))
    g1, g2, gt = np.meshgrid(nus, nus, np.asarray(tof_days, float) * transfers.DAY, indexing="ij")
    return float(np.min(transfers._delta_v(origin, target, g1, g2, gt)))


def compute(cands, hosts=HOSTS, refine=REFINE):
    """Phase-free Δv (m/s) from every candidate to every host: coarse for all, refined for the best few."""
    host_el = elements()
    results = {h: {} for h in hosts}
    saved = dict(transfers.ELEMENTS)
    try:
        for h in hosts:
            transfers.ELEMENTS[h] = host_el[h]
            for key, c in cands.items():
                transfers.ELEMENTS[key] = tuple(c["elements"])
                results[h][key] = {"coarse": coarse(key, h)}
            for key in sorted(results[h], key=lambda k: results[h][k]["coarse"])[:refine]:
                dv, nu1, nu2, days = transfers.best_phase(key, h)
                results[h][key].update({"best": dv, "days": days})
    finally:
        transfers.ELEMENTS.clear()
        transfers.ELEMENTS.update(saved)
    return results


def fetch():
    cands = candidates()
    results = compute(cands)
    CATALOGUE.write_text(json.dumps({"fetched": date.today().isoformat(),
                                     "source": "NASA/JPL Small-Body Database query API",
                                     "candidates": cands, "delta_v": results}, indent=1) + "\n")
    return cands, results


def load():
    return json.loads(CATALOGUE.read_text())


def ranked(data, host, n=8):
    """The refined candidates for a host, lowest Δv first: [(designation, entry, Δv m/s, flight days)]."""
    res = data["delta_v"][host]
    rows = [(k, data["candidates"][k], v["best"], v["days"]) for k, v in res.items() if "best" in v]
    return sorted(rows, key=lambda r: r[2])[:n]


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m logistics_model.catalogue", description=__doc__)
    ap.add_argument("--fetch", action="store_true", help="fetch the candidates and compute their Δv (network)")
    args = ap.parse_args(argv)
    if args.fetch:
        cands, results = fetch()
        print(f"{len(cands)} candidates")
    data = load()
    for h in HOSTS:
        print(h, [(r[1]["name"], round(r[2] / 1e3, 2)) for r in ranked(data, h, 5)])
    return 0


if __name__ == "__main__":
    sys.exit(main())
