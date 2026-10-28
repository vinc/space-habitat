"""One-at-a-time sweep (tornado) and Monte Carlo over the assumption ranges (plan §1.4)."""

from dataclasses import dataclass

import numpy as np

from .assumptions import params
from .model import METRICS, evaluate, metrics


@dataclass
class Row:
    name: str
    status: str
    low: float
    high: float
    effects: dict      # metric -> (relative change at low, at high)

    @property
    def score(self):
        """Largest relative swing on any output."""
        return max(abs(hi - lo) for lo, hi in self.effects.values())


def _relative(value, base):
    return value / base - 1 if base else 0.0


def tornado(assumptions, design, overrides=None):
    """Each varying input at its low and high, the rest at their values; rows ranked by impact."""
    overrides = overrides or {}
    base = metrics(evaluate(params(assumptions, **overrides), design))
    rows = []
    for a in assumptions.values():
        if not a.varies or a.name in overrides:
            continue
        lo = metrics(evaluate(params(assumptions, **{**overrides, a.name: a.low}), design))
        hi = metrics(evaluate(params(assumptions, **{**overrides, a.name: a.high}), design))
        effects = {m: (_relative(lo[m], base[m]), _relative(hi[m], base[m])) for m in METRICS}
        row = Row(a.name, a.status, a.low, a.high, effects)
        if row.score > 1e-9:
            rows.append(row)
    rows.sort(key=lambda r: r.score, reverse=True)
    return base, rows


def monte_carlo(assumptions, design, n=1000, seed=0, overrides=None):
    """Triangular sampling (low, value, high) of every varying input; percentiles of each output."""
    overrides = overrides or {}
    rng = np.random.default_rng(seed)
    varying = [a for a in assumptions.values() if a.varies and a.name not in overrides]
    samples = {m: np.empty(n) for m in METRICS}
    for i in range(n):
        draw = {a.name: rng.triangular(a.low, a.value, a.high) for a in varying}
        result = metrics(evaluate(params(assumptions, **overrides, **draw), design))
        for m, v in result.items():
            samples[m][i] = v
    return {m: dict(zip(("p5", "p50", "p95"), np.percentile(v, [5, 50, 95]))) for m, v in samples.items()}
