"""Torus geometry: the 1 g family, floor, tube, hub, stack and farm ring (§1, §2, §3a, §12, §13)."""

import math

# The "1 g" family r = (T/2)^2 gives a = pi^2 m/s^2 (1.006 g); the notes use it throughout.
ONE_G = math.pi ** 2


def radius_for_period(period_s):
    """Radius of the 1 g family for a rotation period: r = (T/2)^2."""
    return (period_s / 2) ** 2


def compute(p, d):
    r = d.radius_m
    accel = d.g * ONE_G
    omega = math.sqrt(accel / r)
    w = r / p.width_ratio
    a = w / 2                      # tube radius
    centre = r - a                 # tube centre line
    hub = p.hub_radius_per_width * w
    pitch = w + d.gap_m
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
        "floor_area": 2 * math.pi * r * w,
        "volume": 2 * math.pi ** 2 * centre * a ** 2,
        "hull_area": 4 * math.pi ** 2 * centre * a,
        "hub_radius": hub,
        "hub_gravity": d.g * hub / r,
        "pitch": pitch,
        "stack_length": d.n_tori * pitch,
        "farm_radius": farm_radius,
        "farm_width": farm_width,
        "farm_gravity": d.g * p.farm_ring_radius_frac,
        "farm_ring_area": farm_ring_area,                        # per tier
        "crop_area_per_tier": p.farm_planted_frac * farm_ring_area,
        "farm_shell_area": 2 * math.pi * farm_radius * 2 * (farm_width + p.farm_ring_height_m),
        # Each open end of the drum: from the hub out to the tubes' inner edge.
        "end_opening": math.pi * ((r - w) ** 2 - hub ** 2),
    }
