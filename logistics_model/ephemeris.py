"""Ephemerides of the candidate bodies from JPL (plan §5): Horizons state vectors and Small-Body Database elements.

Fetched once and kept in the repository (`logistics_model/data/`), so the report runs offline:

python -m logistics_model.ephemeris --fetch          # refresh from JPL (needs the network)

Horizons' vectors come from JPL's integrated orbits, planets' perturbations included (Apophis's 2029 Earth
flyby among them): heliocentric, ecliptic and mean equinox of J2000, every 10 days. Between the samples the
positions are interpolated with cubic Hermite splines on positions and velocities. The Small-Body Database's
osculating elements replace the rounded ones the phase-free transfers used.
"""

import argparse
import json
import math
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import numpy as np

DATA = Path(__file__).with_name("data")
VECTORS = DATA / "horizons_vectors.npz"
ELEMENTS = DATA / "sbdb_elements.json"
START, STOP, STEP_DAYS = "2027-01-01", "2077-01-01", 10
KM = 1e3
DAY = 86400.0
JD_J2000 = 2451545.0

# Horizons command for each body (an asteroid's number followed by ";" selects the small body); Earth's
# centre for Earth. The SBDB designation for elements.
BODIES = {
    "Earth": ("399", None),
    "Ryugu": ("162173;", "162173"),
    "Bennu": ("101955;", "101955"),
    "Eros": ("433;", "433"),
    "Itokawa": ("25143;", "25143"),
    "Apophis": ("99942;", "99942"),
    "Didymos": ("65803;", "65803"),
    "Torifune": ("98943;", "98943"),
    # The catalogue's best C-type partners (`catalogue.py`): dark, low-Δv to the hosts.
    "1999 XX262": ("275611;", "275611"),
    "2001 WT1": ("252558;", "252558"),
    "2015 DX198": ("'DES=2015 DX198;'", "2015 DX198"),
}


def _get(url, params, timeout=120):
    with urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params), timeout=timeout) as r:
        return r.read().decode()


def fetch_vectors(command):
    """Heliocentric ecliptic J2000 state vectors (JD, km, km/s) from JPL Horizons."""
    text = _get("https://ssd.jpl.nasa.gov/api/horizons.api", {
        "format": "text", "COMMAND": command, "EPHEM_TYPE": "VECTORS", "CENTER": "500@10",
        "START_TIME": START, "STOP_TIME": STOP, "STEP_SIZE": f"{STEP_DAYS} d", "REF_PLANE": "ECLIPTIC",
        "REF_SYSTEM": "J2000", "OUT_UNITS": "KM-S", "VEC_TABLE": "2", "CSV_FORMAT": "YES", "OBJ_DATA": "NO"})
    if "$$SOE" not in text:
        raise RuntimeError(f"Horizons returned no ephemeris for {command!r}:\n{text[:2000]}")
    rows = []
    for line in text.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines():
        f = [x.strip() for x in line.split(",")]
        rows.append([float(f[0])] + [float(x) for x in f[2:8]])
    return np.array(rows)


def fetch_elements(sstr):
    """Osculating elements (a AU, e, i, node, argument of perihelion, degrees; epoch JD) from the SBDB API."""
    data = json.loads(_get("https://ssd-api.jpl.nasa.gov/sbdb.api", {"sstr": sstr, "full-prec": "true"}))
    orbit = data["orbit"]
    el = {e["name"]: float(e["value"]) for e in orbit["elements"]}
    return {"a": el["a"], "e": el["e"], "i": el["i"], "node": el["om"], "peri": el["w"], "epoch_jd": float(orbit["epoch"]),
            "name": data["object"]["fullname"], "orbit_id": orbit["orbit_id"]}


def fetch():
    DATA.mkdir(exist_ok=True)
    arrays, elements = {}, {"fetched": date.today().isoformat(), "source": "NASA/JPL Small-Body Database API"}
    jd = None
    for name, (command, sstr) in BODIES.items():
        rows = fetch_vectors(command)
        if jd is None:
            jd = rows[:, 0]
        elif not np.allclose(jd, rows[:, 0]):
            raise RuntimeError(f"{name}: dates don't match")
        arrays[name] = rows[:, 1:]
        if sstr:
            elements[name] = fetch_elements(sstr)
    meta = np.array(json.dumps({"fetched": date.today().isoformat(), "source": "NASA/JPL Horizons API",
                                "frame": "heliocentric, ecliptic and mean equinox of J2000", "units": "km, km/s",
                                "start": START, "stop": STOP, "step_days": STEP_DAYS}))
    np.savez_compressed(VECTORS, jd=jd, meta=meta, **arrays)
    ELEMENTS.write_text(json.dumps(elements, indent=1) + "\n")
    return jd, arrays, elements


class Ephemeris:
    """States of the bodies at any Julian date in the table's span: positions (m) and velocities (m/s)."""

    def __init__(self, path=VECTORS):
        data = np.load(path)
        self.jd = data["jd"]
        self.meta = json.loads(str(data["meta"]))
        self.tables = {k: data[k] for k in data.files if k not in ("jd", "meta")}
        self.step = (self.jd[1] - self.jd[0]) * DAY

    @property
    def bodies(self):
        return list(self.tables)

    def span(self):
        return float(self.jd[0]), float(self.jd[-1])

    def state(self, body, jd):
        """Position and velocity (m, m/s) at Julian dates jd (array), by cubic Hermite interpolation."""
        tab = self.tables[body]
        jd = np.asarray(jd, float)
        u = (jd - self.jd[0]) / (self.jd[1] - self.jd[0])
        if np.any(u < 0) or np.any(u > len(self.jd) - 1):
            raise ValueError("date outside the ephemeris")
        k = np.clip(np.floor(u).astype(int), 0, len(self.jd) - 2)
        s = (u - k)[..., None]
        p0, p1 = tab[k, :3] * KM, tab[k + 1, :3] * KM
        v0, v1 = tab[k, 3:] * KM, tab[k + 1, 3:] * KM
        h = self.step
        h00, h10, h01, h11 = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s, -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
        pos = h00 * p0 + h10 * h * v0 + h01 * p1 + h11 * h * v1
        d00, d10, d01, d11 = 6 * s ** 2 - 6 * s, 3 * s ** 2 - 4 * s + 1, -6 * s ** 2 + 6 * s, 3 * s ** 2 - 2 * s
        vel = (d00 * p0 + d01 * p1) / h + d10 * v0 + d11 * v1
        return pos, vel


def elements():
    """{body: (a AU, e, i, node, argument of perihelion)} from the stored SBDB elements."""
    data = json.loads(ELEMENTS.read_text())
    return {k: (v["a"], v["e"], v["i"], v["node"], v["peri"]) for k, v in data.items() if isinstance(v, dict)}


def jd_of(year, month=1, day=1):
    """Julian date at 0h UT (proleptic Gregorian)."""
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return jdn - 0.5


def calendar(jd):
    """(year, month, day) of a Julian date."""
    z = int(math.floor(jd + 0.5))
    a = z + 32044
    b = (4 * a + 3) // 146097
    c = a - 146097 * b // 4
    d = (4 * c + 3) // 1461
    e = c - 1461 * d // 4
    m = (5 * e + 2) // 153
    return 100 * b + d - 4800 + m // 10, m + 3 - 12 * (m // 10), e - (153 * m + 2) // 5 + 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m logistics_model.ephemeris", description=__doc__)
    ap.add_argument("--fetch", action="store_true", help="refresh the stored ephemerides from JPL")
    args = ap.parse_args(argv)
    if args.fetch:
        jd, arrays, els = fetch()
        print(f"{len(arrays)} bodies, {len(jd)} dates {START} – {STOP}; elements for {len(els) - 2} bodies")
    else:
        e = Ephemeris()
        print(e.meta, e.bodies)
    return 0


if __name__ == "__main__":
    sys.exit(main())
