"""Torus geometry: the 1 g family, floor, tube, hub, stack and farm ring (§1, §2, §3a, §12, §13)."""

import math

# The "1 g" family r = (T/2)^2 gives a = pi^2 m/s^2 (1.006 g); the notes use it throughout.
ONE_G = math.pi ** 2


def radius_for_period(period_s):
    """Radius of the 1 g family for a rotation period: r = (T/2)^2."""
    return (period_s / 2) ** 2


def compute(p, d):
    """Boundaries, from the axis of the tube outward: the pressurised tube (radius a = w/2,
    the valley with its fill inside), the rock jacket (thickness t), the empty crawl space,
    then the thin bumper. The envelope is everything out to the bumper; gaps are clear
    space between neighbouring envelopes.
    """
    r = d.radius_m
    accel = d.g * ONE_G
    omega = math.sqrt(accel / r)
    w = r / p.width_ratio
    a = w / 2                      # tube radius
    centre = r - a                 # tube centre line
    jacket = p.shield_areal_t_m2 / p.rock_density
    envelope = a + jacket + p.crawl_space_m
    hub = p.hub_radius_per_width * w
    if d.gap_m < 0:
        raise ValueError("neighbouring tori would intersect: the gap between envelopes must be >= 0")
    drum = centre - envelope       # inner edge of the envelopes: outer radius of the drum's end openings
    if drum <= hub:
        raise ValueError("the tube's envelope reaches the hub")
    pitch = 2 * envelope + d.gap_m
    farm_radius = p.farm_ring_radius_frac * r
    farm_width = p.farm_ring_width_frac * w
    farm_ring_area = 2 * math.pi * farm_radius * farm_width
    return {
        "radius": r,
        "accel": accel,
        "omega": omega,
        "period": 2 * math.pi / omega,
        "rpm": omega * 60 / (2 * math.pi),
        "rim_speed": omega * r,
        "width": w,
        "tube_radius": a,
        "jacket": jacket,
        "envelope_radius": envelope,
        "envelope_outer": centre + envelope,
        "drum_radius": drum,
        "gap": d.gap_m,
        "floor_area": 2 * math.pi * r * w,
        "volume": 2 * math.pi ** 2 * centre * a ** 2,
        "hull_area": 4 * math.pi ** 2 * centre * a,
        "hub_radius": hub,
        "hub_gravity": d.g * hub / r,
        "pitch": pitch,
        "stack_length": d.n_tori * pitch,
        "farm_radius": farm_radius,
        "farm_width": farm_width,
        "farm_height": p.farm_ring_height_m,
        "farm_gravity": d.g * p.farm_ring_radius_frac,
        "farm_ring_area": farm_ring_area,                        # per tier
        "crop_area_per_tier": p.farm_planted_frac * farm_ring_area,
        "farm_shell_area": 2 * math.pi * farm_radius * 2 * (farm_width + p.farm_ring_height_m),
        # Each open end of the drum: from the hub out to the envelopes' inner edge.
        "end_opening": math.pi * (drum ** 2 - hub ** 2),
    }
