"""Radiator wings on the elevator shafts, and the chord nets' shading (notes §12, §13).

Each torus and each farm ring has four elevator shafts in its mid-plane, one per quadrant, each carrying a
radiator wing on both sides (cavity.Wings): the same layout in both sections. Traced with the assembled
inboard scene (`habitat_model/cavity.py`), against the evenly spread panels the coverage sweeps assume:
the wings aligned in every ring or turned ring to ring, the least farm coverage for the 1.5x target with
staggered wings, and the tori's tangent-chord nets (cable_net) as shading in their side planes.
"""

import math

from habitat_model import Design, evaluate
from habitat_model import cavity, wing_geometry
from habitat_model.heat import radiator_flux
from structure_model import cable_net

TARGET = 1.5
MAIN_COVER = 0.05
FARM_GRID = (0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80, 0.90)
SEEDS = (0, 1)
N_RAYS = 20000


def scene_of(p, radius, n_tori, tiers):
    res = evaluate(p, Design(radius_m=radius, n_tori=n_tori, tiers_lit=tiers))
    geo, heat = res["geometry"], res["heat"]
    return res, cavity.assembled_scene(geo, n_tori, layout="inboard"), (heat["main_stack"], heat["farm_stack"])


def nets(p, res, n_tori, anchor_spacing):
    """The tori's two side nets per torus at this anchor spacing, each holding half the rim."""
    g, m = res["geometry"], res["mass"]
    net = cable_net.compute(g["radius"], m["rim"], g["omega"], g["hub_radius"], p.wire_stress_mpa * 1e6,
                            p.steel_density, anchor_spacing=anchor_spacing)
    diameter = 2 * math.sqrt(net["wire_area_uniform"] / 2 / math.pi)
    return cavity.nets_of(g, n_tori, net["n_chords"], diameter, net["tangent_radius"]), net, diameter


def margins(p, radius, n_tori, tiers, cover, wings=None, net_spacing=None, n_rays=N_RAYS, seeds=SEEDS):
    """Margins (main, farm) at panel coverages cover = (main, farm), averaged over seeds."""
    res, scene, loads = scene_of(p, radius, n_tori, tiers)
    flux, eps = radiator_flux(p.radiator_temp_k), p.radiator_emissivity
    net = nets(p, res, n_tori, net_spacing)[0] if net_spacing else None
    out = []
    for group in (0, 1):
        annulus = scene.annulus(group)
        e = sum(cavity.escape_probability(scene, cover, eps, n_rays, s, source=group, wings=wings, nets=net)["escape"]
                for s in seeds) / len(seeds)
        out.append(eps * flux * 2 * cover[group] * annulus * e / loads[group])
    return tuple(out), scene, res


def least_farm(p, radius, n_tori, tiers, wings=None, net_spacing=None, main=MAIN_COVER, grid=FARM_GRID):
    """Least farm coverage meeting the target with the main section at `main`, or the best reached."""
    res, scene, _ = scene_of(p, radius, n_tori, tiers)
    top = wing_geometry.max_coverage(*scene.bands[-1])          # the farm band: wings can't cover it all
    grid = sorted({min(f, top) for f in grid})
    best = None
    for f in grid:
        m, scene, _ = margins(p, radius, n_tori, tiers, (main, f), wings, net_spacing)
        area = f * scene.annulus(1) / n_tori
        if m[1] >= TARGET:
            return {"coverage": f, "margins": m, "area_per_ring": area, "met": True}
        if best is None or m[1] > best["margins"][1]:
            best = {"coverage": f, "margins": m, "area_per_ring": area, "met": False}
    return best
