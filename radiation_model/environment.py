"""The radiation environment in deep space near 1 AU (plan §3): galactic cosmic rays and solar particle events.

Galactic cosmic rays: the local interstellar proton spectrum of Usoskin et al. (2005, after Burger et al.
2000), modulated by the force-field approximation with potential φ (MV): ~300 MV at a deep solar minimum
(2009–2010, the highest cosmic-ray flux of the space age), ~1,000 MV at solar maximum. Heavier ions take
the same spectrum per nucleon, scaled by their abundance and modulated with their charge-to-mass ratio, in
four groups: helium, light (Z 3–10, as nitrogen), medium (Z 11–20, as magnesium) and iron (Z 21–28).

Solar particle events: the August 1972 event's proton fluence, King's (1974) fit J(>E) = 7.9 × 10⁹
exp((30 − E) / 26.5) per cm², the classic worst case for design.
"""

import math

import numpy as np

from .physics import M_P

# Species carried by the transport: name: (mass number, charge). Neutrons have charge 0.
# Charged pions ("pi") are made in the shield; for them the energy variable is kinetic energy over 0.1488
# (their mass in nucleon masses), so that it sets their speed as energy per nucleon does for the rest.
PION_A = 0.1488
SPECIES = {"n": (1, 0), "p": (1, 1), "He": (4, 2), "Z3-10": (14, 7), "Z11-20": (24, 12), "Z21-28": (56, 26),
           "pi": (PION_A, 1)}
# Abundance relative to protons at the same energy per nucleon in interstellar space (rough, ~1 GeV/n,
# recalled): helium ~0.13 of protons, C–O ~0.03 of helium, Ne–Ca about half of oxygen, iron ~0.12 of oxygen.
# Together they give ~0.25 Gy and ~1.3 Sv a year in free space at a deep solar minimum (`report`).
ABUNDANCE = {"p": 1.0, "He": 0.13, "Z3-10": 0.007, "Z11-20": 0.0018, "Z21-28": 0.0005}

SECONDS_PER_YEAR = 3.15576e7


def lis_proton(t_mev):
    """Interstellar proton intensity, per (cm² s sr MeV), at kinetic energy t (MeV)."""
    t = np.asarray(t_mev, float) / 1e3                       # GeV
    p = np.sqrt(t * (t + 2 * M_P / 1e3))                     # GV for protons
    j = 1.9e4 * p ** -2.78 / (1 + 0.4866 * p ** -2.51)       # per (m² s sr GeV)
    return j * 1e-7


def gcr(t_per_n, phi_mv, species):
    """Modulated galactic cosmic-ray intensity of a species, per (cm² s sr MeV/n), at t_per_n (MeV/n)."""
    a, z = SPECIES[species]
    t = np.asarray(t_per_n, float)
    big_phi = z / a * phi_mv                                   # MeV per nucleon lost to the heliosphere
    tl = t + big_phi
    return ABUNDANCE[species] * lis_proton(tl) * t * (t + 2 * M_P) / (tl * (tl + 2 * M_P))


def spe_aug1972(t_mev):
    """August 1972 proton fluence per (cm² MeV) over the event, King (1974)."""
    t = np.asarray(t_mev, float)
    return 7.9e9 / 26.5 * np.exp((30 - t) / 26.5)


def spectrum(edges, source="gcr", phi_mv=300.0):
    """Incident intensity per bin, per (cm² sr) and per second (GCR) or per event (SPE, taken isotropic over
    the event), for every species: {species: array over bins}."""
    lo, hi = edges[:-1], edges[1:]
    out = {s: np.zeros(len(lo)) for s in SPECIES}
    # Integrate each bin with a few points in log energy.
    x = np.linspace(0, 1, 9)
    pts = lo[:, None] * (hi / lo)[:, None] ** x[None, :]
    for s in SPECIES:
        if source == "gcr" and s not in ("n", "pi"):
            f = gcr(pts, phi_mv, s)
        elif source == "spe" and s == "p":
            f = spe_aug1972(pts) / (4 * math.pi)
        else:
            continue
        out[s] = np.trapezoid(f, pts, axis=1)
    return out
