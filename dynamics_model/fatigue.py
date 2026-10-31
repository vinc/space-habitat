"""Fatigue (plan §4): the load cycles the stack's parts see over a life, against a fatigue limit.

Each source gives a stress range and a number of cycles over LIFE years:
- rim trains: a load fixed to the train, so turning against the structure once per lap
  (v / 2 pi R), while running TRAIN_SERVICE of the time; its stress range twice the amplitude;
- ballast trims: a share of the tanks' capacity shifted and trimmed back each day (people, stores);
- docking: one ship a day;
- the rims' daily temperature difference (the valleys' days offset): the lattice's hoop strain;
- sunlight on the struts once per turn (the Sun shines into the gaps, edge-on): their temperature
  swing over half a turn, restrained around the hoop.
The parts: the lattice's struts (welded tube joints, detail category 71 MPa), the hub's wall
(welded plate, 71 MPa) and the stabilising lines (strand, 160 MPa). Eurocode 3's curves (EN
1993-1-9): slope 3 to 5e6 cycles, 5 to 1e8, then the cut-off; a range below the cut-off does no
damage. Miner's sum over the sources, with a partial factor on the stress.
"""

import math

import numpy as np

from . import disturbances as ds
from . import joints as jt
from . import links as lk

LIFE = 100.0                   # years
TRAIN_SERVICE = 0.75           # share of the time a train runs
BALLAST_DAILY = 0.2            # share of the tanks' capacity shifted and trimmed each day (guess)
DOCKINGS_PER_DAY = 1.0
RIM_DT = 4.0                   # K, the rims' daily difference
ABSORPTIVITY = 0.5             # struts' coating
HEAT_CAPACITY = 500.0          # J/kg/K, steel
GAMMA_F = 1.35                 # partial factor on the stress ranges
DETAIL = {"lattice struts": 71e6, "hub wall": 71e6, "stabilising lines": 160e6}
SOLAR = 1361.0
D_RATIO = (2 / 5) ** (1 / 3)   # constant-amplitude limit (5e6) over the category (2e6), slope 3
L_RATIO = (5 / 100) ** (1 / 5)  # cut-off (1e8) over that limit, slope 5


def endurance(detail, stress_range):
    """Cycles to failure at a stress range (EN 1993-1-9's curves; infinite below the cut-off)."""
    d_c = detail
    d_d = D_RATIO * d_c        # at 5e6
    d_l = L_RATIO * d_d        # cut-off at 1e8
    if stress_range <= d_l:
        return math.inf
    if stress_range >= d_d:
        return 2e6 * (d_c / stress_range) ** 3
    return 5e6 * (d_d / stress_range) ** 5


def study(p, d, k_design, tie_frac=1e-4):
    lat, s, info, unbalanced = lk.converged(p, d, k_design, tie_frac=tie_frac)
    geo, nets = info["geometry"], info["nets"]
    h, t = geo["hub_radius"], info["hub_shell_m"]
    year = 365.25 * 86400
    radius_train = geo["radius"] - geo["width"]
    speed = 20.0
    days = LIFE * 365.25

    strut = lambda force: (2 * force / lat["bays"]) / (2 * (lat["width"] / lat["diagonal"])) / lat["area"]
    hub = lambda moment: moment / (math.pi * h * h * t)
    lines_per_plane = nets["n_lines"] / 2
    line = lambda net_force: (2 * net_force / lines_per_plane) / nets["line_area"]

    def loads_and_moment(lam, force):
        f = np.zeros(s.size(), dtype=complex)
        f[s.body_dof(0)] = force
        q = s.response(lam, f)
        return ds.loads(s, q), jt.hub_moments(s, q)

    train = ds.rim_train(s, geo, speed=speed)
    tl, tm = loads_and_moment(train["lambda"], train["force"])
    mass_e = p.ballast_frac * info["mass"]["rim"] * BALLAST_DAILY
    bl, bm = loads_and_moment(s.omega, mass_e * geo["radius"] * s.omega ** 2)
    dock = ds.docking(s, spins=10, samples=400)
    # Sunlight on a strut over half a turn: absorbed a D S per metre, heat capacity rho c pi D t.
    wall = lat["diameter"] / lk.STRUT_D_OVER_T
    swing = ABSORPTIVITY * SOLAR * (math.pi / s.omega) / (p.steel_density * HEAT_CAPACITY * math.pi * wall)
    sources = {
        "rim trains": (TRAIN_SERVICE * LIFE * year * speed / (2 * math.pi * radius_train),
                       {"lattice struts": 2 * strut(tl["link"]), "hub wall": 2 * hub(tm),
                        "stabilising lines": 2 * line(tl["net"])}),
        "ballast trims": (days, {"lattice struts": strut(bl["link"]), "hub wall": hub(bm),
                                 "stabilising lines": line(bl["net"])}),
        "docking": (days * DOCKINGS_PER_DAY, {"lattice struts": 2 * strut(dock["link"]),
                                              "stabilising lines": 2 * line(dock["net"])}),
        "rims' daily temperature": (days, {"lattice struts": lk.E * lk.THERMAL_EXPANSION * RIM_DT}),
        "sunlight each turn": (LIFE * year * s.omega / (2 * math.pi),
                               {"lattice struts": lk.E * lk.THERMAL_EXPANSION * swing}),
    }
    damage = {part: 0.0 for part in DETAIL}
    largest = {part: 0.0 for part in DETAIL}
    for cycles, ranges in sources.values():
        for part, rng in ranges.items():
            largest[part] = max(largest[part], GAMMA_F * rng)
            damage[part] += cycles / endurance(DETAIL[part], GAMMA_F * rng)
    cutoff = {part: L_RATIO * D_RATIO * DETAIL[part] for part in DETAIL}
    return {"sources": sources, "damage": damage, "largest": largest, "cutoff": cutoff, "strut_swing": swing}
