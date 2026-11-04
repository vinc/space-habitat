"""Radiator wings on elevator shafts: exact area, angle for a coverage, attainable maximum (notes §12, §13).

In a ring's plane, `shafts` shafts at equal angles each carry a wing on both sides. A wing is the set of
points of the radiator band r0 <= rho <= r1 whose angle from its shaft's centre line is at most beta and
whose distance from that line is at least `edge` (the shaft's half-width plus a clearance). Near the axis
a narrow wing doesn't reach past the shaft: it starts at rho_a = max(r0, edge / sin(beta)).

Pure Python (no numpy), so that the browser build of the model can use it too.
"""

import math

SHAFTS = 4
EDGE = 5.0          # m: an 8 m shaft's half-width plus 1 m


def _f(q, edge):
    """Antiderivative of rho * asin(edge / rho)."""
    return q * q / 2 * math.asin(edge / q) + edge / 2 * math.sqrt(q * q - edge * edge)


def area(beta, r0, r1, edge=EDGE, shafts=SHAFTS):
    """Total area (one face) of the 2 x shafts wings of half-angle beta in the band r0..r1."""
    if beta <= 0:
        return 0.0
    beta = min(beta, math.pi / shafts)
    start = max(r0, edge / math.sin(beta))
    if start >= r1:
        return 0.0
    one = beta * (r1 * r1 - start * start) / 2 - (_f(r1, edge) - _f(start, edge))
    return 2 * shafts * one


def max_coverage(r0, r1, edge=EDGE, shafts=SHAFTS):
    """The most of the band the wings can cover: neighbouring wings meet halfway between shafts."""
    return area(math.pi / shafts, r0, r1, edge, shafts) / (math.pi * (r1 * r1 - r0 * r0))


def angle(coverage, r0, r1, edge=EDGE, shafts=SHAFTS):
    """Half-angle beta giving the wings `coverage` of the band; 0 for no wings. Raises ValueError above
    the attainable maximum."""
    if coverage <= 0:
        return 0.0
    target = coverage * math.pi * (r1 * r1 - r0 * r0)
    lo, hi = 0.0, math.pi / shafts
    if area(hi, r0, r1, edge, shafts) < target * (1 - 1e-12):
        raise ValueError(f"wing coverage {coverage:.0%} exceeds the attainable "
                         f"{max_coverage(r0, r1, edge, shafts):.1%} of this band")
    for _ in range(100):                     # area grows monotonically with beta
        mid = (lo + hi) / 2
        if area(mid, r0, r1, edge, shafts) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
