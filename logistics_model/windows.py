"""Dated launch windows between the candidate bodies (plan §5), on JPL Horizons' ephemerides.

For each departure date (every `STEP` days) and flight time (`TOF_DAYS`), a two-impulse rendezvous on a
prograde zero-revolution Lambert arc (`transfers.lambert`): Δv = |v_transfer(t1) − v_origin(t1)| +
|v_target(t2) − v_transfer(t2)|. The best flight time for each departure gives a curve against the calendar;
each dip below a threshold is a window, refined by a pattern search on departure and flight time.
"""

import math

import numpy as np

from . import transfers
from .ephemeris import DAY, Ephemeris, calendar, jd_of

STEP = 5.0                                   # days between departures on the coarse grid
TOF_DAYS = np.arange(60.0, 901.0, 10.0)


def delta_v(eph, origin, target, t1, tof):
    """Rendezvous Δv (m/s) departing at JD t1 with flight time tof (days); inf where Lambert fails."""
    t1 = np.asarray(t1, float)
    tof = np.asarray(tof, float)
    r1, v1 = eph.state(origin, t1)
    r2, v2 = eph.state(target, t1 + tof)
    a1, a2 = transfers.lambert(r1, r2, tof * DAY)
    dv = np.linalg.norm(a1 - v1, axis=-1) + np.linalg.norm(v2 - a2, axis=-1)
    return np.where(np.isfinite(dv), dv, np.inf)


def curve(eph, origin, target, start_jd, end_jd, step=STEP, tofs=TOF_DAYS):
    """Best Δv over flight time for each departure date: (departure JDs, Δv m/s, best flight days)."""
    last = eph.span()[1]
    t1 = np.arange(start_jd, end_jd, step)
    g1, gt = np.meshgrid(t1, tofs, indexing="ij")
    ok = g1 + gt <= last
    dv = np.full(g1.shape, np.inf)
    dv[ok] = delta_v(eph, origin, target, g1[ok], gt[ok])
    k = np.argmin(dv, axis=1)
    return t1, dv[np.arange(len(t1)), k], tofs[k]


def refine(eph, origin, target, t1, tof, start_jd=None, end_jd=None):
    """Pattern search on (departure JD, flight days) from a grid point, the departure kept within
    [start_jd, end_jd] and the arrival within the ephemeris."""
    first, last = eph.span()
    lo = first if start_jd is None else start_jd
    hi = last if end_jd is None else min(end_jd, last)
    x = np.array([np.clip(t1, lo, hi), tof], float)
    f = float(delta_v(eph, origin, target, x[0], x[1])) if x[0] + x[1] <= last else np.inf
    steps = np.array([STEP / 2, 5.0])
    while steps[0] > 0.01:
        trial = x + np.concatenate([np.diag(steps), -np.diag(steps)])
        trial[:, 0] = np.clip(trial[:, 0], lo, hi)
        trial[:, 1] = np.clip(trial[:, 1], 20.0, None)
        valid = trial[:, 0] + trial[:, 1] <= last
        fs = np.full(len(trial), np.inf)
        fs[valid] = delta_v(eph, origin, target, trial[valid, 0], trial[valid, 1])
        m = int(np.argmin(fs))
        if fs[m] < f:
            x, f = trial[m], fs[m]
        else:
            steps = steps / 2
    return float(f), float(x[0]), float(x[1])


def local_minima(dv, half_width):
    """Indices of the departure curve's minima: points no higher than any other within half_width samples
    (one per basin; a plateau keeps its first point)."""
    n = len(dv)
    out = []
    for i in range(n):
        if not np.isfinite(dv[i]):
            continue
        lo, hi = max(0, i - half_width), min(n, i + half_width + 1)
        window = dv[lo:hi]
        if dv[i] <= window.min() and int(np.argmin(window)) + lo == i:
            out.append(i)
    return out


def deduplicate(found, separation):
    """The best of every group of windows departing within `separation` days of each other, by date."""
    kept = []
    for w in sorted(found, key=lambda w: w[0]):
        if all(abs(w[1] - k[1]) >= separation for k in kept):
            kept.append(w)
    return sorted(kept, key=lambda w: w[1])


def windows(eph, origin, target, start_jd, end_jd, margin=1000.0, separation=120.0):
    """Windows: the minima of the best-flight curve (one per basin, `separation` days wide) within `margin`
    (m/s) of its lowest value, each refined within the span, then deduplicated so no two depart within
    `separation` days (the better kept). Returns [(Δv m/s, departure JD, flight days)], by date, and the
    curve."""
    t1, dv, tof = curve(eph, origin, target, start_jd, end_jd)
    best = float(np.min(dv))
    half = max(1, int(round(separation / 2 / STEP)))
    picks = [i for i in local_minima(dv, half) if dv[i] <= best + margin]
    refined = [refine(eph, origin, target, t1[i], tof[i], start_jd, end_jd) for i in picks]
    refined = [w for w in refined if np.isfinite(w[0])]
    out = deduplicate(refined, separation)
    return out, (t1, dv, tof)


def summary(eph, origin, target, start_jd, end_jd, within=500.0):
    """The best window in the span, the windows within `within` m/s of it, and the gaps between them
    (years): mean and longest, which sets the stock a shipping schedule must buffer."""
    found, curve_ = windows(eph, origin, target, start_jd, end_jd, margin=max(within, 1000.0))
    best = min(found, key=lambda w: w[0])
    good = [w for w in found if w[0] <= best[0] + within]
    gaps = np.diff([w[1] for w in good]) / 365.25 if len(good) > 1 else np.array([])
    return {"best": best, "good": good, "all": found, "gaps_yr": gaps, "curve": curve_,
            "mean_gap": float(np.mean(gaps)) if len(gaps) else None,
            "max_gap": float(np.max(gaps)) if len(gaps) else None}


def date_str(jd):
    y, m, d = calendar(jd)
    return f"{y}-{m:02d}-{d:02d}"


__all__ = ["delta_v", "curve", "refine", "windows", "summary", "date_str", "jd_of", "Ephemeris"]
