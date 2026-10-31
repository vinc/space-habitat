"""The valley's light box and a farm tier, traced across the pipes (plan §7, notes §13).

Light box (one pipe's width of ceiling, repeating): the magnesium-oxide top, the pipe hung just below it,
the diffuser `diffuser_gap_m` below the pipe, and the valley's floor far below. What the floor absorbs,
over its absorptance, is the light delivered (what, falling once on the floor, would be absorbed the same).

Farm tier (one bed and one aisle, repeating): the crop canopy as a block `canopy_height_m` tall over the
bed, the aisle's floor beside it, the pipes `farm_pipe_gap_m` above the canopy and the white underside of
the tier above. Delivered: what the canopy absorbs, top and sides, over its absorptance.

Both are per unit of light leaving the pipes; the pipes' own efficiency (`pipe.py`) and the lamps'
coupling into them come on top (`delivery`).
"""

import math

import numpy as np

from . import pipe
from habitat_model.power import farm_efficacy

from .trace import Scene, emit_from_circle, trace

DAY = 86400.0


def valley_peak_w_m2(p):
    """Electricity for the sky per m² of floor while it is lit (W/m²), at the configured delivery."""
    return p.valley_light_mol / (p.valley_day_h * 3600) / (p.lamp_efficacy_umol_j * 1e-6) / p.ceiling_delivery


def farm_peak_w_m2(p):
    """Electricity per m² of bed while it is lit (W/m²), at the configured delivery."""
    return p.crop_light_mol / (p.farm_photoperiod_h * 3600) / (farm_efficacy(p) * 1e-6) / p.farm_delivery


def valley_pitch(p):
    """Pipe spacing across the ceiling (m) for the sky's peak power at the pipes' loading."""
    return p.pipe_w_per_m / valley_peak_w_m2(p)


def farm_pipes_per_bed(p):
    """Pipes over each bed: enough for the bed's peak power at no more than the pipes' loading."""
    return max(1, math.ceil(p.bed_width_m * farm_peak_w_m2(p) / p.pipe_w_per_m - 1e-9))


def light_box(p, pitch=None, gap=None, n=200_000, seed=2, bins=24, **over):
    """Trace the light box. Returns the shares of the pipes' light the floor gets (delivered, over its
    absorptance) and each surface absorbs, and the diffuser's glow across one pitch (max / min)."""
    q = {**vars(p), **over}
    pitch = valley_pitch(p) if pitch is None else pitch
    gap = q["diffuser_gap_m"] if gap is None else gap
    r = q["pipe_diameter_m"] / 2
    if pitch < 2 * r:
        raise ValueError("pipes wider than their spacing")
    top_gap = 0.05
    y_pipe = -(top_gap + r)
    y_diff = y_pipe - r - gap
    y_floor = y_diff - 1.0
    td = q["diffuser_transmittance"]
    rd = 1 - td - q["diffuser_absorptance"]
    s = Scene(pitch)
    s.add("top", "segment", (pitch, 0.0), (0.0, 0.0), front=(q["mgo_reflectance"], 0.0))
    s.add("pipe", "circle", (pitch / 2, y_pipe), r, front=(q["pipe_albedo"], 0.0))
    s.add("diffuser", "segment", (0.0, y_diff), (pitch, y_diff), front=(rd, td), back=(rd, td))
    s.add("floor", "segment", (0.0, y_floor), (pitch, y_floor), front=(q["floor_albedo"], 0.0))
    rng = np.random.default_rng(seed)
    o, d = emit_from_circle((pitch / 2, y_pipe), r, n, rng, q["pipe_emit_arc_deg"])
    out = trace(s, o, d, rng)
    shares = {k: v.size / n for k, v in out["absorbed"].items()}
    delivered = shares["floor"] / (1 - q["floor_albedo"])
    glow = np.histogram(out["down"]["diffuser"], bins=bins, range=(0, pitch))[0]
    return {"delivered": delivered, "absorbed": shares, "glow_ratio": glow.max() / max(glow.min(), 1),
            "glow_spread": (glow.max() - glow.min()) / glow.mean(), "pitch": pitch, "gap": gap,
            "lost": out["lost"] / n}


def farm_tier(p, pipe_gap=None, pipes=None, n=200_000, seed=3, bins=24, **over):
    """Trace a farm tier. Returns the share of the pipes' light the crops get (delivered), what each surface
    absorbs, and the light on the canopy's top across the bed (lowest / mean)."""
    q = {**vars(p), **over}
    gap = q["farm_pipe_gap_m"] if pipe_gap is None else pipe_gap
    pipes = farm_pipes_per_bed(p) if pipes is None else pipes
    r = q["pipe_diameter_m"] / 2
    bed, aisle, c = q["bed_width_m"], q["aisle_width_m"], q["canopy_height_m"]
    period = bed + aisle
    x0, x1 = aisle / 2, aisle / 2 + bed
    y_ceiling = q["tier_clear_m"] - c                    # the canopy's top at y = 0, the floor at y = -c
    y_pipe = gap + r
    if y_pipe + r > y_ceiling:
        raise ValueError("pipes above the ceiling")
    rc, ra = q["canopy_reflectance"], q["aisle_reflectance"]
    s = Scene(period)
    s.add("ceiling", "segment", (period, y_ceiling), (0.0, y_ceiling), front=(q["mgo_reflectance"], 0.0))
    centres = [(x0 + bed * (i + 0.5) / pipes, y_pipe) for i in range(pipes)]
    for ctr in centres:
        s.add("pipe", "circle", ctr, r, front=(q["pipe_albedo"], 0.0))
    s.add("canopy top", "segment", (x0, 0.0), (x1, 0.0), front=(rc, 0.0))
    s.add("canopy side", "segment", (x0, -c), (x0, 0.0), front=(rc, 0.0))
    s.add("canopy side", "segment", (x1, 0.0), (x1, -c), front=(rc, 0.0))
    s.add("aisle", "segment", (0.0, -c), (x0, -c), front=(ra, 0.0))
    s.add("aisle", "segment", (x1, -c), (period, -c), front=(ra, 0.0))
    rng = np.random.default_rng(seed)
    parts = [emit_from_circle(ctr, r, n // pipes, rng, q["pipe_emit_arc_deg"]) for ctr in centres]
    o = np.concatenate([a for a, _ in parts])
    d = np.concatenate([b for _, b in parts])
    total = len(o)
    out = trace(s, o, d, rng)
    shares = {k: v.size / total for k, v in out["absorbed"].items()}
    delivered = (shares["canopy top"] + shares["canopy side"]) / (1 - rc)
    light = np.histogram(out["absorbed"]["canopy top"], bins=bins, range=(x0, x1))[0]
    return {"delivered": delivered, "absorbed": shares, "uniformity": light.min() / light.mean(),
            "peak": light.max() / light.mean(), "pipes": pipes, "pipe_pitch": bed / pipes, "gap": gap,
            "lost": out["lost"] / total}


def delivery(p, n=200_000, pipe_result=None, box=None, tier=None, pitch=None, pipes=None):
    """The whole chain for the valley and the farm: lamp into pipe, pipe out, light box or tier. The layout
    is sized from p's deliveries unless pitch (valley) and pipes (per bed) are given."""
    pr = pipe.efficiency(p) if pipe_result is None else pipe_result
    box = light_box(p, pitch=pitch, n=n) if box is None else box
    tier = farm_tier(p, pipes=pipes, n=n) if tier is None else tier
    chain = p.pipe_coupling * pr["efficiency"]
    return {"pipe": pr, "box": box, "tier": tier, "lamp_to_pipe_out": chain,
            "valley": chain * box["delivered"], "farm": chain * tier["delivered"]}


def with_delivery(p, d):
    """p with its deliveries replaced by a traced chain's."""
    return type(p)(**{**vars(p), "ceiling_delivery": d["valley"], "farm_delivery": d["farm"]})


def converged(p, n=200_000, pipe_result=None, tol=0.002, max_iter=12):
    """The layout and the delivery that agree: the pipes spaced for the power the traced delivery needs at
    their loading, traced again, until the delivery settles. A denser layout takes back more of the light.
    Returns the chain, with `params`: p carrying the converged deliveries, which size the layout."""
    pr = pipe.efficiency(p) if pipe_result is None else pipe_result
    q = p
    d = delivery(q, n, pr)
    for _ in range(max_iter):
        q = with_delivery(p, d)
        nxt = delivery(q, n, pr)
        done = abs(nxt["valley"] - d["valley"]) < tol and nxt["tier"]["pipes"] == d["tier"]["pipes"]
        d = nxt
        if done:
            break
    else:
        raise RuntimeError("the layout and the delivery did not settle")
    # The layout was sized from q's deliveries; d is what it delivers. Size it once more from d's own.
    return {**d, "params": with_delivery(p, d), "sized_from": q}
