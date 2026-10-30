"""Materials, stopping powers, nuclear cross sections and dose (plan §3).

Standard physics, with data recalled from the usual tables rather than looked up (unsourced unless noted):
mean excitation energies, thermal and fast neutron cross sections, the Bethe formula, the Letaw and Sihver
cross-section fits, ICRP 60's quality factor and ICRP 74's neutron fluence-to-dose coefficients.
"""

import math
from dataclasses import dataclass

import numpy as np

N_A = 6.02214e23
M_P = 938.272            # MeV, nucleon mass (proton)
M_E = 0.510999           # MeV
K_BETHE = 0.307075       # MeV cm²/mol
MEV_PER_G_TO_GY = 1.602177e-10    # 1 MeV/g = 1.602e-10 Gy
BARN = 1e-24

# Element: Z, A (g/mol), mean excitation energy I (eV); neutrons around 1–2 MeV: elastic σ (b), inelastic σ (b);
# thermal: absorption σ_a and scattering σ_s (b, 2,200 m/s).
ELEMENTS = {
    "H": (1, 1.008, 19.2, 3.0, 0.0, 0.332, 30.0),
    "B": (5, 10.81, 76.0, 2.0, 0.1, 767.0, 4.3),
    "C": (6, 12.011, 78.0, 2.0, 0.05, 0.0035, 4.7),
    "N": (7, 14.007, 82.0, 2.0, 0.1, 1.9, 10.0),
    "O": (8, 15.999, 95.0, 2.5, 0.05, 0.0002, 3.8),
    "Na": (11, 22.99, 149.0, 2.5, 0.4, 0.53, 3.3),
    "Mg": (12, 24.305, 156.0, 2.5, 0.4, 0.063, 3.4),
    "Al": (13, 26.982, 166.0, 2.5, 0.4, 0.231, 1.5),
    "Si": (14, 28.086, 173.0, 2.5, 0.4, 0.171, 2.2),
    "S": (16, 32.06, 180.0, 2.0, 0.3, 0.53, 1.0),
    "Ca": (20, 40.078, 191.0, 2.5, 0.3, 0.43, 3.0),
    "Cr": (24, 51.996, 257.0, 3.0, 0.8, 3.1, 3.4),
    "Fe": (26, 55.845, 286.0, 3.0, 0.8, 2.56, 11.6),
    "Ni": (28, 58.693, 311.0, 3.0, 0.8, 4.49, 18.0),
}

# Shield and habitat materials, mass fractions and bulk density (t/m³). The tailings are an L/LL ordinary
# chondrite less its free metal (the iron left is in silicates and troilite); the clays a CI-like C-type with
# its bound water and organics; the steel a plain carbon steel taken as iron.
COMPOSITIONS = {
    "Tailings (L/LL chondrite, metal removed)": ({"O": 0.405, "Si": 0.200, "Mg": 0.155, "Fe": 0.150, "S": 0.023,
                                                  "Ca": 0.014, "Al": 0.012, "Na": 0.007, "Ni": 0.003,
                                                  "Cr": 0.004}, 2.0),
    "CI-like clays (C-type)": ({"O": 0.46, "Si": 0.107, "Mg": 0.097, "Fe": 0.185, "S": 0.054, "C": 0.035,
                                "H": 0.020, "Ca": 0.009, "Al": 0.009, "Na": 0.005, "Ni": 0.011, "N": 0.002,
                                "Cr": 0.003}, 1.8),
    "Lunar regolith (OLTARIS's)": ({"O": 0.43, "Si": 0.21, "Al": 0.08, "Ca": 0.08, "Fe": 0.11, "Mg": 0.06,
                                   "Na": 0.004}, 1.8),
    "Water": ({"H": 0.1119, "O": 0.8881}, 1.0),
    "Polyethylene": ({"H": 0.1437, "C": 0.8563}, 0.94),
    "Moist soil": ({"O": 0.52, "Si": 0.22, "Mg": 0.08, "Fe": 0.10, "H": 0.022, "C": 0.03, "Ca": 0.01,
                    "Al": 0.012, "S": 0.006}, 1.6),
    "Steel": ({"Fe": 1.0}, 7.9),
    "Tissue (water)": ({"H": 0.1119, "O": 0.8881}, 1.0),
}


# Measured mean excitation energies of compounds, where Bragg additivity of the elements is poor (eV).
I_COMPOUND = {"Water": 75.0, "Tissue (water)": 75.0, "Polyethylene": 57.4}


@dataclass
class Material:
    name: str
    fractions: dict
    density: float = 1.0
    i_ev: float = None

    def __post_init__(self):
        total = sum(self.fractions.values())
        self.fractions = {k: v / total for k, v in self.fractions.items()}

    @property
    def z_over_a(self):
        return sum(w * ELEMENTS[e][0] / ELEMENTS[e][1] for e, w in self.fractions.items())

    @property
    def mean_excitation_mev(self):
        """Bragg additivity in ln I, weighted by electrons (or the measured value where given)."""
        if self.i_ev:
            return self.i_ev * 1e-6
        za = self.z_over_a
        ln_i = sum(w * ELEMENTS[e][0] / ELEMENTS[e][1] * math.log(ELEMENTS[e][2]) for e, w in self.fractions.items())
        return math.exp(ln_i / za) * 1e-6

    def atoms_per_gram(self):
        """{element: atoms per g}."""
        return {e: w * N_A / ELEMENTS[e][1] for e, w in self.fractions.items()}

    def hydrogen(self):
        return self.fractions.get("H", 0.0)


def material(name):
    frac, rho = COMPOSITIONS[name]
    return Material(name, dict(frac), rho, I_COMPOUND.get(name))


def mix(name, parts):
    """A mixture by mass of materials: parts = [(Material, mass share)]."""
    out = {}
    total = sum(s for _, s in parts)
    for m, s in parts:
        for e, w in m.fractions.items():
            out[e] = out.get(e, 0.0) + w * s / total
    rho = total / sum(s / m.density for m, s in parts)
    return Material(name, out, rho)


# --- Charged particles ---------------------------------------------------------------------------------------

def stopping_power(mat, t_per_n, z=1, a=1.0):
    """Electronic stopping power (MeV cm²/g) of an ion of charge z and mass number a at kinetic energy
    t_per_n (MeV per nucleon): the Bethe formula without shell, density or Barkas corrections (fine above
    ~10 MeV/n, a little high at GeV energies where the density effect starts)."""
    t = np.asarray(t_per_n, float)
    gamma = 1 + t / M_P
    beta2 = 1 - 1 / gamma ** 2
    mass = a * M_P
    tmax = 2 * M_E * beta2 * gamma ** 2 / (1 + 2 * gamma * M_E / mass + (M_E / mass) ** 2)
    i = mat.mean_excitation_mev
    arg = 2 * M_E * beta2 * gamma ** 2 * tmax / i ** 2
    s = K_BETHE * z ** 2 * mat.z_over_a / beta2 * (0.5 * np.log(np.maximum(arg, 1.0001)) - beta2)
    return np.maximum(s, 1e-6)


class RangeTable:
    """CSDA range of a proton-like nucleon in a material, R(T) in g/cm², and its inverse; ions scale as
    R_ion(T/n) = (a / z²) R_p(T/n). The Bethe formula is integrated from 1 MeV up; below, where it fails for
    heavy materials, the range follows R ∝ T^1.75."""

    def __init__(self, mat, t_join=1.0, t_max=2e5, n=4000):
        t = np.geomspace(t_join, t_max, n)
        s = stopping_power(mat, t)
        r0 = t[0] / s[0] / 1.75
        inv = 1 / s
        r = r0 + np.concatenate([[0.0], np.cumsum(0.5 * (inv[1:] + inv[:-1]) * np.diff(t))])
        low = np.geomspace(1e-3, t_join, 40)[:-1]
        self.t = np.concatenate([low, t])
        self.r = np.concatenate([r0 * (low / t_join) ** 1.75, r])
        self.log_t, self.log_r = np.log(self.t), np.log(self.r)

    def range(self, t, z=1, a=1.0):
        return a / z ** 2 * np.exp(np.interp(np.log(np.maximum(t, self.t[0])), self.log_t, self.log_r))

    def energy(self, r, z=1, a=1.0):
        """Kinetic energy per nucleon with range r (0 below the table)."""
        rp = np.asarray(r, float) * z ** 2 / a
        out = np.exp(np.interp(np.log(np.maximum(rp, 1e-30)), self.log_r, self.log_t))
        return np.where(rp <= self.r[0], 0.0, out)


# --- Nuclear interactions ------------------------------------------------------------------------------------

def sigma_inelastic(a_proj, a_targ):
    """High-energy inelastic (absorption) cross section, mb. Nucleons: Letaw et al. (1983), 45 A^0.7 with its
    small oscillation (p + p: ~30 mb above the pion threshold). Nuclei: Sihver et al. (1993)."""
    def letaw(a):
        return 45.0 * a ** 0.7 * (1 + 0.016 * math.sin(5.3 - 2.63 * math.log(a)))

    if a_proj <= 1.5 and a_targ <= 1.5:
        return 30.0
    if a_proj <= 1.5:
        return letaw(a_targ)
    if a_targ <= 1.5:
        return letaw(a_proj)
    x = a_proj ** (-1 / 3) + a_targ ** (-1 / 3)
    b0 = 1.581 - 0.876 * x
    r0 = 1.36
    return 10 * math.pi * r0 ** 2 * (a_proj ** (1 / 3) + a_targ ** (1 / 3) - b0 * x) ** 2


def interaction_length(mat, a_proj):
    """Mean free path for inelastic nuclear interactions, g/cm²."""
    n = sum(atoms * sigma_inelastic(a_proj, ELEMENTS[e][1]) * 1e-27 for e, atoms in mat.atoms_per_gram().items())
    return 1 / n


def mean_target_mass(mat, a_proj=1.0):
    """Target mass number averaged over interactions (weighted by each element's share of them)."""
    w = {e: atoms * sigma_inelastic(a_proj, ELEMENTS[e][1]) for e, atoms in mat.atoms_per_gram().items()}
    total = sum(w.values())
    return sum(ELEMENTS[e][1] * v for e, v in w.items()) / total, {e: v / total for e, v in w.items()}


# --- Neutrons below 20 MeV: two groups -----------------------------------------------------------------------

def neutron_groups(mat, lethargy=3.0):
    """Macroscopic constants per g/cm² for fast (~0.1–20 MeV) and thermal neutrons: transport and removal
    from the fast group (elastic slowing over `lethargy`, half of inelastic scatters), thermal absorption and
    transport. Returns (fast: (Σ_tr, Σ_r), thermal: (Σ_tr, Σ_a)), in cm²/g."""
    tr_f = rem = tr_t = ab = 0.0
    for e, atoms in mat.atoms_per_gram().items():
        z, a, _, el, inel, sa, ss = ELEMENTS[e]
        mu = 2 / (3 * a)
        xi = 1.0 if a < 1.5 else 1 + (a - 1) ** 2 / (2 * a) * math.log((a - 1) / (a + 1))
        tr_f += atoms * (el * (1 - mu) + inel) * BARN
        rem += atoms * (el * xi / lethargy + 0.5 * inel) * BARN
        tr_t += atoms * (ss * (1 - mu) + sa) * BARN
        ab += atoms * sa * BARN
    return (tr_f, rem), (tr_t, ab)


# --- Dose ----------------------------------------------------------------------------------------------------

def quality_factor(let_kev_um):
    """ICRP 60 Q(L), L in keV/µm in water."""
    l = np.asarray(let_kev_um, float)
    return np.where(l < 10, 1.0, np.where(l <= 100, 0.32 * l - 2.2, 300 / np.sqrt(np.maximum(l, 1e-9))))


TISSUE = material("Tissue (water)")


def charged_dose_per_fluence(t_per_n, z, a):
    """Absorbed dose (Gy) and dose equivalent (Sv) per particle/cm² in tissue for an ion at t_per_n."""
    s = stopping_power(TISSUE, t_per_n, z, a)              # MeV cm²/g
    gy = s * MEV_PER_G_TO_GY
    let = s * 0.1                                          # MeV cm²/g × 1 g/cm³ → keV/µm: × 0.1
    return gy, gy * quality_factor(let)


# Neutrons: fluence to ambient dose equivalent, pSv cm² (ICRP 74, recalled; above 20 MeV extended values).
NEUTRON_HIGH_PSV_CM2 = 400.0      # 20 MeV – GeV, roughly flat
NEUTRON_THERMAL_PSV_CM2 = 10.6
# Absorbed dose per neutron fluence, pGy cm², for the shares of absorbed dose (quality ~10 for 1 MeV, ~3 at
# high energy, ~2 thermal, all rough).
NEUTRON_Q = {"high": 3.0, "fast": 10.0, "thermal": 2.0}
