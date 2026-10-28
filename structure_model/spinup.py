"""Building a ring in the tangent-chord net: partial arcs hung in opposite pairs (notes §12, plan §2).

A chord from rim angle phi lands at phi + pi -/+ 2 theta (one per handedness), not
exactly opposite. So for two opposite arcs [a, b] and [a + pi, b + pi]:
  - an anchor near the start of an arc (within 2 theta of it) has only one chord whose far
    end lands on the other arc, and likewise near the end: these end zones are single-laced;
  - an anchor with only one chord gets a pull along the rim of tan(theta) times its radial
    load; the two end zones of an arc pull outward along the rim, so the arc carries a
    tension along its length, which the segment joints must take until the ring closes;
  - every anchor has at least one chord only if the arc spans more than 4 theta.
"""

import math


def partial_arc(radius, theta, rim_line_mass, omega, plate_stress_pa=500e6):
    load = rim_line_mass * omega ** 2 * radius            # radial pull per metre of rim, N/m
    end_zone = 2 * theta * radius                           # single-laced length at each end of an arc
    tension = load * end_zone * math.tan(theta)             # along the arc, from each end zone
    hoop_full_ring = rim_line_mass * (omega * radius) ** 2  # a self-supporting ring's hoop force, for scale
    return {
        "end_zone": end_zone,
        "min_arc": 2 * end_zone,
        "joint_tension": tension,
        "joint_tension_vs_hoop": tension / hoop_full_ring,
        "joint_steel_area": tension / plate_stress_pa,
        "hoop_full_ring": hoop_full_ring,
    }


def imbalance_offset(mismatch_kg, radius, total_mass_kg):
    """A free spinning body turns about its centre of mass: a mismatch between paired arcs
    shifts the rim's centre (and the hub) off the spin axis by this much."""
    return mismatch_kg * radius / total_mass_kg
