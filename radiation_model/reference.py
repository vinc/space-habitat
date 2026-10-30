"""OLTARIS results from the literature, for checking the model and sizing the jacket (plan §3).

Globus & Strout, "Orbital Space Settlement Radiation Shielding", NSS Space Settlement Journal (April 2017),
Table 2: free space, the 1977–78 solar minimum, effective dose equivalent (mSv/yr) on OLTARIS's female
voxel phantom at the centre of a sphere of the given shield, by tonnes per m².

Janhunen, "Shielded Dumbbell L5 Settlement" (arXiv:2004.02241, 2020), also with OLTARIS: 0.18 t/m² of iron,
8.68 t/m² of dry (lunar) regolith, 0.177 t/m² of water and 1 kg/m² of boron-10 give 20 mSv/yr at the
sphere's centre at solar minimum; in slab geometry, near the wall, 9.97 mSv/yr (half); at solar maximum
14.87 mSv/yr (25% less).
"""

import numpy as np

TONNES = np.arange(1.0, 12.0)
TABLE2 = {
    "Lunar regolith (OLTARIS's)": [281, 275, 240, 194, 149, 109, 77, 52, 34.9, 22.8, 14.5],
    "Water": [200, 147, 101, 67, 43, 26.5, 16.1],
    "Polyethylene": [194, 137, 91, 57, 35, 21.0, 12.3],
}
FREE_SPACE = 462.0                       # mSv/yr, "~0" t/m² (a microgram of regolith)

JANHUNEN = {"layers_t_m2": {"Steel": 0.18, "Lunar regolith (OLTARIS's)": 8.683, "Water": 0.177, "Boron-10": 0.001},
            "sphere_centre": 20.0, "slab_wall": 9.97, "solar_max_centre": 14.87}
WALL_FACTOR = JANHUNEN["slab_wall"] / JANHUNEN["sphere_centre"]          # ~0.5


def table2(material, tonnes):
    """OLTARIS's sphere-centre dose (mSv/yr) behind tonnes per m², interpolated in log; beyond the table,
    extended at the slope of its last two tonnes."""
    ref = np.log(np.array(TABLE2[material], float))
    t = TONNES[:len(ref)]
    slope = ref[-1] - ref[-2]
    x = np.asarray(tonnes, float)
    return np.exp(np.where(x <= t[-1], np.interp(x, t, ref), ref[-1] + slope * (x - t[-1])))


def needed(material, limit, factor=1.0, low=0.0, high=30.0):
    """Tonnes per m² at which factor × OLTARIS's curve falls to the limit (log interpolation, the curve
    extended past its table); low if it is already below the limit there, None if not even at high."""
    xs = np.linspace(max(low, 1.0), high, int(round((high - max(low, 1.0)) * 100)) + 1)
    d = factor * table2(material, xs)
    ok = d <= limit
    if not ok.any():
        return None
    i = int(np.argmax(ok))
    if i == 0:
        return float(xs[0])
    # Between xs[i - 1] and xs[i], in log dose.
    l0, l1 = np.log(d[i - 1]), np.log(d[i])
    return float(xs[i - 1] + (xs[i] - xs[i - 1]) * (l0 - np.log(limit)) / (l0 - l1))
