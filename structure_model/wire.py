"""Drawn pearlitic steel wire: strength classes, working stress, relaxation (plan §2).

The numbers are collected in structure_model/README.md with their sources.
"""

import math

E_STEEL = 200e9  # Pa, Young's modulus of drawn wire (standard value)

# Guaranteed ultimate tensile strength classes of suspension-bridge wire, MPa
# (Tokyo Rope catalogue: 1570-1770, 1770-1960, 1960-2160 MPa classes; the
# 0.2% proof stress must reach 75% of the guaranteed strength).
BRIDGE_CLASSES = (1570, 1770, 1960)
PROOF_RATIO = 0.75

# Safety factors on the guaranteed strength. Only the 2.15 action level and the
# 2.4 of an in-service cable were found in sources; 2.5 and 2.2 are the commonly
# quoted design values for new cables, not verified here (NCHRP 534 was unreachable).
SAFETY_FACTORS = {
    "new bridge cables (commonly quoted, unverified)": 2.5,
    "long spans such as Akashi (commonly quoted, unverified)": 2.2,
    "NCHRP 534 action level for existing cables": 2.15,
    "static, well-known spin load (proposed here)": 2.0,
}


def working_stress(guaranteed_mpa, safety_factor):
    return guaranteed_mpa / safety_factor


def thin_wire_strength(diameter_mm):
    """Strength above which wire counts as 'high strength', R = 2250 - 1130 log10(d) MPa (Bekaert patent).

    A rough guide to how strength rises as wire gets thinner, not a guarantee.
    """
    return 2250 - 1130 * math.log10(diameter_mm)


def relaxation_1000h(stress_ratio):
    """Stress loss (fraction) after 1,000 h for cold-drawn wire held at fixed length.

    Empirical r% = 30 f0/fpt - 10 for cold-drawn wire (Hungarian design paper); zero
    below f0/fpt = 1/3.
    """
    return max(0.0, 0.30 * stress_ratio - 0.10)


def final_relaxation(stress_ratio):
    """Long-term relaxation, taken as twice the 1,000 h value (same source's rule of thumb)."""
    return 2 * relaxation_1000h(stress_ratio)


def creep_elongation(stress_pa, ultimate_pa, length_m):
    """Long-term extra stretch of a wire held at constant load, from its relaxation.

    Relaxation at fixed length and creep at fixed load are the same flow: a stress loss
    of fraction x at fixed length corresponds to an extra strain of x times the elastic strain.
    """
    elastic = stress_pa / E_STEEL
    return final_relaxation(stress_pa / ultimate_pa) * elastic * length_m
