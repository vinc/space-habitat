"""The farm radiators' layout and reach, and how long a stack the radiators can cool (plan §6).

Everything here is the assembled stack traced as one scene (`habitat_model.cavity`): the drum with the
valleys' radiators, the gap, and the farm section with its own. The farm's radiators can sit outboard of the
farm rings (out to farm_radiator_outer, pumped loops: their heat flows against spin gravity) or inboard,
between the hub and the rings (passive thermosiphons).
"""

from dataclasses import replace

from habitat_model import cavity
from habitat_model.assumptions import params
from habitat_model.design import Design
from habitat_model.model import evaluate


def _check(p, d, layout, n_rays, grid=cavity.GRID):
    r = evaluate(p, d)
    return cavity.check_assembled(p, d, r["geometry"], r["heat"], n_rays=n_rays, grid=grid, layout=layout)


def smallest(points, target):
    """The grid point with the least panel area (both sections, one face) whose worse margin meets target."""
    ok = [q for q in points if q["margin"] >= target]
    return min(ok, key=lambda q: sum(q["panel_area"])) if ok else None


def compare(p, cases, target=1.5, n_rays=4000, grid=cavity.GRID):
    """Both layouts for each (label, radius, tori, tiers): best margins, and the least panel area for target."""
    rows = []
    for label, radius, n, tiers in cases:
        d = Design(radius_m=radius, n_tori=n, tiers_lit=tiers)
        for layout in cavity.FARM_LAYOUTS:
            a = _check(p, d, layout, n_rays, grid)
            rows.append({"label": label, "layout": layout, "tiers": tiers, "main": a["main_margin"],
                         "farm": a["farm_margin"], "coverage": a["coverage"], "loads": a["loads"],
                         "least": smallest(a["points"], target)})
    return rows


def passive_tiers(row, per_tier):
    """Farm tiers the inboard (passive) radiators alone can carry: their best output over one tier's heat."""
    return row["farm"] * row["loads"][1] / per_tier


def reach_needed(assumptions, d, target, low=0.45, high=1.4, n_rays=4000, steps=8, name="farm_radiator_outer_frac"):
    """Least outboard reach (× floor radius) at which the assembled stack meets target in both sections."""
    def margin(v):
        return _check(params(assumptions, **{name: v}), d, "outboard", n_rays)["margin"]

    if margin(high) < target:
        return None
    if margin(low) >= target:
        return low
    for _ in range(steps):
        mid = (low + high) / 2
        low, high = (mid, high) if margin(mid) < target else (low, mid)
    return high


def capacity(p, radius, tiers, n_rays=3000, max_tori=40):
    """Most tori (with their farm rings) the assembled stack can cool, farm radiators outboard."""
    return cavity.assembled_limit(p, replace(Design(radius_m=radius, n_tori=1), tiers_lit=tiers),
                                  n_rays=n_rays, max_tori=max_tori)
