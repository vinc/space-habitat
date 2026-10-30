"""Rendezvous delta-v between two heliocentric orbits (plan §5): zero-revolution Lambert transfers, two impulses.

Phase-free ("best phase"): the departure and arrival points are free on each orbit, as are the flight time,
so the result is a lower bound for the pair, whatever the bodies' positions. Dated windows, on JPL Horizons'
ephemerides, are in `windows.py`.
"""

import math

import numpy as np

MU_SUN = 1.32712440018e20       # m^3/s^2
AU = 1.495978707e11             # m
DAY = 86400.0
YEAR = 365.25 * DAY


# Osculating elements (a AU, e, i deg, node deg, argument of perihelion deg), J2000 ecliptic: Earth's mean
# elements, and the asteroids' from JPL's Small-Body Database (fetched, `logistics_model/data/`, below; the
# values here are the rounded ones they replace, kept if the data file is missing). Enough for phase-free
# transfers, which use the orbits' shapes and orientations only. Apophis after its 2029 flyby: a and e
# approximated, angles kept (§15); its dated windows use Horizons' integrated orbit instead.
ELEMENTS = {
    "Earth": (1.00000, 0.0167, 0.000, 0.00, 102.94),
    "Ryugu": (1.1896, 0.1902, 5.884, 251.29, 211.43),
    "Bennu": (1.1264, 0.2037, 6.035, 2.06, 66.22),
    "Eros": (1.4580, 0.2227, 10.828, 304.27, 178.93),
    "Itokawa": (1.3241, 0.2801, 1.621, 69.08, 162.81),
    "Apophis": (0.9224, 0.1911, 3.339, 203.96, 126.67),
    "Apophis 2029": (1.103, 0.189, 3.339, 203.96, 126.67),
    "Didymos": (1.6427, 0.3839, 3.408, 73.20, 319.32),
    "Torifune": (1.0324, 0.2194, 4.81, 75.63, 179.38),
}


try:
    from .ephemeris import elements as _fetched
    ELEMENTS.update(_fetched())
except (OSError, ValueError):
    pass


def period(a_au):
    return 2 * math.pi * math.sqrt((a_au * AU) ** 3 / MU_SUN)


def synodic_period(a, b):
    """Years per cycle of the two bodies' mean longitudes: a timescale for windows. The best-phase geometry
    doesn't recur with it on eccentric, inclined orbits; when good windows recur needs a dated search."""
    pa, pb = period(ELEMENTS[a][0]), period(ELEMENTS[b][0])
    return 1 / abs(1 / pa - 1 / pb) / YEAR


def perihelion_longitude(name):
    return (ELEMENTS[name][3] + ELEMENTS[name][4]) % 360


def state(elements, nu):
    """Position and velocity (m, m/s) at true anomaly nu (radians, array), in the ecliptic frame."""
    a_au, e, i, node, peri = elements
    a = a_au * AU
    p = a * (1 - e * e)
    nu = np.asarray(nu, dtype=float)
    r = p / (1 + e * np.cos(nu))
    h = math.sqrt(MU_SUN * p)
    # Perifocal frame.
    pos = np.stack([r * np.cos(nu), r * np.sin(nu), np.zeros_like(nu)], axis=-1)
    vel = np.stack([-MU_SUN / h * np.sin(nu), MU_SUN / h * (e + np.cos(nu)), np.zeros_like(nu)], axis=-1)
    rot = _rotation(math.radians(node), math.radians(i), math.radians(peri))
    return pos @ rot.T, vel @ rot.T


def _rotation(node, inc, peri):
    cO, sO, ci, si, cw, sw = math.cos(node), math.sin(node), math.cos(inc), math.sin(inc), math.cos(peri), math.sin(peri)
    return np.array([
        [cO * cw - sO * sw * ci, -cO * sw - sO * cw * ci, sO * si],
        [sO * cw + cO * sw * ci, -sO * sw + cO * cw * ci, -cO * si],
        [sw * si, cw * si, ci],
    ])


def _stumpff(z):
    c = np.empty_like(z)
    s = np.empty_like(z)
    pos, neg, zero = z > 1e-8, z < -1e-8, np.abs(z) <= 1e-8
    sz = np.sqrt(z[pos])
    c[pos] = (1 - np.cos(sz)) / z[pos]
    s[pos] = (sz - np.sin(sz)) / sz ** 3
    sz = np.sqrt(-z[neg])
    c[neg] = (np.cosh(sz) - 1) / -z[neg]
    s[neg] = (np.sinh(sz) - sz) / sz ** 3
    c[zero], s[zero] = 0.5, 1 / 6
    return c, s


def lambert(r1, r2, tof, iterations=80):
    """Prograde zero-revolution Lambert problem (universal variables, bisection on z; vectorised).
    r1, r2: (..., 3) positions in m; tof: (...) seconds. Returns v1, v2 (m/s); NaN where it has no solution."""
    with np.errstate(all="ignore"):
        return _lambert(r1, r2, tof, iterations)


def _lambert(r1, r2, tof, iterations):
    r1, r2 = np.asarray(r1, float), np.asarray(r2, float)
    tof = np.broadcast_to(np.asarray(tof, float), r1.shape[:-1])
    n1, n2 = np.linalg.norm(r1, axis=-1), np.linalg.norm(r2, axis=-1)
    cos_dnu = np.clip(np.sum(r1 * r2, axis=-1) / (n1 * n2), -1, 1)
    # Prograde: the transfer goes the short way when the orbit normal points north (+z).
    cross_z = r1[..., 0] * r2[..., 1] - r1[..., 1] * r2[..., 0]
    dnu = np.where(cross_z >= 0, np.arccos(cos_dnu), 2 * math.pi - np.arccos(cos_dnu))
    A = np.sin(dnu) * np.sqrt(n1 * n2 / (1 - cos_dnu + 1e-300))

    def y_of(z):
        c, s = _stumpff(z)
        return n1 + n2 + A * (z * s - 1) / np.sqrt(c), c, s

    def t_of(z):
        y, c, s = y_of(z)
        ok = y > 0
        x = np.sqrt(np.where(ok, y, 0) / c)
        t = (x ** 3 * s + A * np.sqrt(np.where(ok, y, 0))) / math.sqrt(MU_SUN)
        return np.where(ok, t, -np.inf), y

    lo = np.full(tof.shape, -4 * math.pi ** 2 * 4)
    hi = np.full(tof.shape, 4 * math.pi ** 2 * (1 - 1e-9))
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        t, _ = t_of(mid)
        below = t < tof
        lo = np.where(below, mid, lo)
        hi = np.where(below, hi, mid)
    z = 0.5 * (lo + hi)
    t, y = t_of(z)
    bad = ~np.isfinite(t) | (np.abs(t - tof) > 1e-3 * tof) | (np.abs(A) < 1e-3)
    f = 1 - y / n1
    g = A * np.sqrt(np.maximum(y, 0) / MU_SUN)
    gdot = 1 - y / n2
    v1 = (r2 - f[..., None] * r1) / g[..., None]
    v2 = (gdot[..., None] * r2 - r1) / g[..., None]
    v1[bad] = np.nan
    v2[bad] = np.nan
    return v1, v2


def _delta_v(origin, target, nu1, nu2, tof):
    r1, v1 = state(ELEMENTS[origin], nu1)
    r2, v2 = state(ELEMENTS[target], nu2)
    t1, t2 = lambert(r1, r2, tof)
    dv = np.linalg.norm(t1 - v1, axis=-1) + np.linalg.norm(v2 - t2, axis=-1)
    return np.where(np.isfinite(dv), dv, np.inf)


def best_phase(origin, target, step_deg=10.0, tof_days=np.arange(40, 801, 40)):
    """Lowest two-impulse rendezvous delta-v (m/s) over departure and arrival points and flight time,
    a coarse grid then a pattern search. Returns (delta-v, departure nu deg, arrival nu deg, flight days)."""
    nus = np.radians(np.arange(0, 360, step_deg))
    g1, g2, gt = np.meshgrid(nus, nus, np.asarray(tof_days, float) * DAY, indexing="ij")
    dv = _delta_v(origin, target, g1, g2, gt)
    order = np.argsort(dv, axis=None)[:8]
    best = None
    for flat in order:
        i, j, k = np.unravel_index(flat, dv.shape)
        x = np.array([g1[i, j, k], g2[i, j, k], gt[i, j, k]])
        f = dv[i, j, k]
        steps = np.array([math.radians(step_deg) / 2, math.radians(step_deg) / 2, 20 * DAY])
        while steps[0] > math.radians(0.01):
            moves = np.concatenate([np.diag(steps), -np.diag(steps)])
            trial = x + moves
            trial[:, 2] = np.maximum(trial[:, 2], 5 * DAY)
            fs = _delta_v(origin, target, trial[:, 0], trial[:, 1], trial[:, 2])
            m = int(np.argmin(fs))
            if fs[m] < f:
                x, f = trial[m], fs[m]
            else:
                steps = steps / 2
        if best is None or f < best[0]:
            best = (float(f), math.degrees(x[0]) % 360, math.degrees(x[1]) % 360, x[2] / DAY)
    return best
