"""Parametric system model of the torus habitat (plan.md §1).

Recomputes the design notes' numbers from one set of assumptions
(assumptions.toml) and ranks the assumptions by how much they matter.
"""

from .assumptions import load, params
from .design import Design
from .model import METRICS, evaluate, metrics

__all__ = ["Design", "METRICS", "evaluate", "load", "metrics", "params"]
