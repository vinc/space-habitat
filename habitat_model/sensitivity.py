"""One-at-a-time sweep (tornado) and Monte Carlo over the assumption ranges (plan §1.4).

Outputs that are unknown for a design (e.g. shipping energy without a known delta-v)
are left out of its sweep rather than counted as zero.
"""

from dataclasses import dataclass

import numpy as np

from .assumptions import params
from .design import Design
from .model import METRICS, evaluate, metrics

# Representative designs for the combined ranking: sizes, host classes and sites.
REPRESENTATIVE = {
    "900 m six-stack, L host, Eros": Design(radius_m=900, n_tori=6, tiers_lit=2, host_class="L", site="Eros"),
    "1.6 km six-stack, LL host, Eros": Design(radius_m=1600, n_tori=6, tiers_lit=2, host_class="LL", site="Eros"),
    "900 m pair, L host, Torifune": Design(radius_m=900, n_tori=2, tiers_lit=1, host_class="L", site="Torifune"),
    "400 m pair, LL host, Itokawa": Design(radius_m=400, n_tori=2, tiers_lit=1, host_class="LL", site="Itokawa"),
    "2.5 km pair, H host, Eros": Design(radius_m=2500, n_tori=2, tiers_lit=1, host_class="H", site="Eros"),
}


@dataclass
class Row:
    name: str
    status: str
    low: float
    high: float
    effects: dict      # metric -> (relative change at low, at high); only known metrics

    @property
    def score(self):
        """Largest relative swing on any output."""
        return max((abs(hi - lo) for lo, hi in self.effects.values()), default=0.0)


def _relative(value, base):
    return value / base - 1 if base else 0.0


def tornado(assumptions, design, overrides=None):
    """Each varying input at its low and high, the rest at their values; rows ranked by impact."""
    overrides = overrides or {}
    base = metrics(evaluate(params(assumptions, **overrides), design))
    known = [m for m in METRICS if base[m] is not None]
    rows = []
    for a in assumptions.values():
        if not a.varies or a.name in overrides:
            continue
        lo = metrics(evaluate(params(assumptions, **{**overrides, a.name: a.low}), design))
        hi = metrics(evaluate(params(assumptions, **{**overrides, a.name: a.high}), design))
        effects = {m: (_relative(lo[m], base[m]), _relative(hi[m], base[m])) for m in known}
        row = Row(a.name, a.status, a.low, a.high, effects)
        if row.score > 1e-9:
            rows.append(row)
    rows.sort(key=lambda r: r.score, reverse=True)
    return base, rows


def combined_ranking(assumptions, designs=REPRESENTATIVE, overrides=None):
    """For each input, its largest swing on any output across the designs, and where it occurs.
    Overridden inputs are held at their override in every design and left out of the sweep."""
    best = {}
    for label, design in designs.items():
        _, rows = tornado(assumptions, design, overrides)
        for row in rows:
            metric, (lo, hi) = max(row.effects.items(), key=lambda kv: abs(kv[1][1] - kv[1][0]))
            if row.name not in best or row.score > best[row.name]["score"]:
                best[row.name] = {"score": row.score, "design": label, "metric": metric, "low": lo, "high": hi,
                                  "status": row.status}
    return sorted(best.items(), key=lambda kv: kv[1]["score"], reverse=True)


def monte_carlo(assumptions, design, n=1000, seed=0, overrides=None):
    """Independent triangular sampling (low, value, high) of every varying input; percentiles of each
    known output. The spread is conditional on the chosen ranges and on treating the inputs as
    independent; it is not a physical confidence interval."""
    overrides = overrides or {}
    rng = np.random.default_rng(seed)
    varying = [a for a in assumptions.values() if a.varies and a.name not in overrides]
    known = [m for m, v in metrics(evaluate(params(assumptions, **overrides), design)).items() if v is not None]
    samples = {m: np.empty(n) for m in known}
    for i in range(n):
        draw = {a.name: rng.triangular(a.low, a.value, a.high) for a in varying}
        result = metrics(evaluate(params(assumptions, **overrides, **draw), design))
        for m in known:
            samples[m][i] = result[m]
    return {m: dict(zip(("p5", "p50", "p95"), np.percentile(v, [5, 50, 95]))) for m, v in samples.items()}
