"""Drawing layout of the structure, for the explorer and renders (notes §12, §13).

Counts and positions only, from the same rules as the detailed models, so that a picture shows the real
number of parts without reimplementing formulas in JavaScript:

- the tangent-chord nets (structure_model.cable_net, net_statics): an anchor every cell_size_m of rim,
  on the tube's centre line in each of the two side planes, each anchor joined to the one m steps
  ahead (so it carries one chord of each handedness), the chords tangent near 1.1 x the hub radius; one
  stabilising line per chord, from the hub to the chord's closest point;
- the rim lattice (dynamics_model.links): X-braced bays as wide as the gap, at the tube's centre line;
- the farm spokes: two planes per farm ring, one spoke every cell_size_m of the ring's inner face
  (the count is not sized by a model; the spacing follows the nets), ~10% crossed between the planes;
- the elevator shafts and their radiator wings (habitat_model.cavity.Wings): four shafts per torus and
  per farm ring in its mid-plane, each ring's shafts turned 90°/N from its neighbour's, a wing on both
  sides of each shaft over the radiator band, sized to the coverage of reports/heat_rejection.md.
"""

import math

TANGENT_MARGIN = 1.1          # chords tangent at this multiple of the hub radius (cable_net)
SHAFTS = 4                    # elevator shafts per torus and per farm ring, one per quadrant
SHAFT_WIDTH_M = 8.0           # placeholder truss width, not sized (cavity.Wings: edge = width / 2 + 1 m)
FARM_CROSSED = 0.10           # share of the farm spokes crossed between their planes (notes §11)
# Least wing coverage for 1.5x with staggered wings (reports/heat_rejection.md, wings section). The
# valleys: 5% of the drum's band at every size. The farm, by tiers lit 1 / 2 / 3, for a pair and a
# six-stack (other stack lengths take the nearer); a six-stack with three tiers lit never reaches
# 1.5x, so it is drawn at the best-reached coverage. Larger tori need slightly more with two tiers.
MAIN_COVER = 0.05
FARM_COVER = {"pair": (0.10, 0.20, 0.25), "six": (0.10, 0.35, 0.90)}
FARM_COVER_SIX_TWO_TIERS_LARGE = 0.40      # 1.6 and 2.5 km six-stacks with two tiers lit


def farm_cover(n_tori, tiers, radius):
    if tiers <= 0:
        return 0.0
    if n_tori <= 3:
        return FARM_COVER["pair"][tiers - 1]
    if tiers == 2 and radius > 1000:
        return FARM_COVER_SIX_TWO_TIERS_LARGE
    return FARM_COVER["six"][tiers - 1]


def wing_angle(cover, r0, r1, edge, shafts=SHAFTS):
    """Angle beta (rad) of each wing: an annular sector r0..r1 from the shaft's edge (a straight line
    `edge` off its centre line) out to beta, so that 2 x shafts wings cover `cover` of the band."""
    if cover <= 0:
        return 0.0
    f = lambda q: q * q / 2 * math.asin(edge / q) + edge / 2 * math.sqrt(q * q - edge * edge)
    return (cover * math.pi * (r1 * r1 - r0 * r0) / (2 * shafts) + f(r1) - f(r0)) * 2 / (r1 * r1 - r0 * r0)


def compute(p, d, geo):
    r, a, hub = geo["radius"], geo["tube_radius"], geo["hub_radius"]
    centre = r - a
    cell = p.cell_size_m
    n_anchors = round(2 * math.pi * r / cell)
    step = 2 * math.pi / n_anchors
    m = round((math.pi - 2 * math.asin(TANGENT_MARGIN * hub / centre)) / step)
    tangent = centre * math.cos(m * step / 2)
    gap = geo["gap"]
    ring_inner = geo["farm_radius"] - geo["farm_height"] / 2
    farm_spokes = round(2 * math.pi * ring_inner / cell)
    shaft = SHAFT_WIDTH_M
    edge = shaft / 2 + 1.0
    main_band = (geo["radiator_inner"], geo["drum_radius"])              # cavity.main_scene
    farm_band = (hub + 1.0, ring_inner)                                  # cavity._farm_band, inboard
    main_cover = MAIN_COVER
    farm = farm_cover(d.n_tori, d.tiers_lit, r)
    return {
        "net": {"planes_offset": a + geo["jacket"], "anchor_radius": centre, "anchors": n_anchors,
                "chord_steps": m, "tangent_radius": tangent, "lines_per_torus": 2 * n_anchors},
        "lattice": {"radius": centre, "bays": max(3, round(2 * math.pi * centre / max(gap, 1.0))) if gap > 0 else 0},
        "farm_spokes": {"per_plane": farm_spokes, "crossed_every": round(1 / FARM_CROSSED),
                        "inner": hub, "outer": ring_inner},
        "shafts": {"count": SHAFTS, "width": shaft, "stagger": 2 * math.pi / SHAFTS / max(1, d.n_tori),
                   "main_top": centre - a, "farm_top": geo["farm_radius"] + geo["farm_height"] / 2},
        "wings": {
            "edge": edge,
            "main": {"band": main_band, "coverage": main_cover,
                     "angle": wing_angle(main_cover, *main_band, edge),
                     "area_per_torus": main_cover * math.pi * (main_band[1] ** 2 - main_band[0] ** 2)},
            "farm": {"band": farm_band, "coverage": farm,
                     "angle": wing_angle(farm, *farm_band, edge),
                     "area_per_ring": farm * math.pi * (farm_band[1] ** 2 - farm_band[0] ** 2)},
        },
    }
