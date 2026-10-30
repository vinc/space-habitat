"""Straight-ahead transport of cosmic rays through a layered shield (plan §3).

Along one ray, as HZETRN does in its classic form: every particle keeps its direction; charged ones slow
down continuously (CSDA, `physics.RangeTable`) and all are removed by inelastic nuclear collisions
(`physics.interaction_length`), whose products carry on along the ray:

- **Nucleons** (protons, and neutrons above 20 MeV) leave a leading nucleon with a share x of the energy,
  distributed as (a + 1) x^a, a set so that the spectrum-weighted moment Z_NN = ∫ x^(γ−1) dN/dx for a
  γ = 2.7 power law is `leading_z` (~0.3: the nucleon attenuation length λ / (1 − Z_NN) ≈ 120 g/cm² in air,
  Gaisser's textbook value). It stays a proton or neutron with probability 0.7.
- **Every collision** also knocks out cascade nucleons from the target, `cascade_coeff` × A^(1/3) of them
  (fewer below ~500 MeV), with an exponential spectrum of mean `cascade_t_mev`, half protons, half
  neutrons; and evaporates `evaporation_coeff` × A^0.6 neutrons of a few MeV.
- **Every collision stays within its energy:** the leading particle first, then the target's products
  (cascade nucleons, light ions, evaporation neutrons), scaled down where they would take more than it
  leaves.
- **Charged pions**, above the production threshold (~290 MeV), take two thirds of what is left, rest
  masses included (the rest, neutral pions, goes into electromagnetic
  showers, left out), their total energies spread as (1 − y)^b / y from m_π / E up, with b = 4. In dense rock they
  interact long before they decay, so they carry the cascade on like nucleons (interaction length
  `PION_LAMBDA` × the nucleons'), making nucleons and pions again; they ionise like protons of their speed.
- **Light ions** are knocked out of the struck nuclei too: `alpha_coeff` × A^(1/3) helium nuclei (standing
  for d, t, ³He and α) of ~30 MeV per nucleon, exponentially distributed.
- **Ions** fragment at the same energy per nucleon: helium into two protons and two neutrons; heavier groups
  into lighter groups (`FRAGMENTS`), the nucleons left over as helium (30% of them), protons and neutrons.
- **Neutrons below 20 MeV** leave the ray: they are counted as a source per g/cm² of path for the diffusion
  model (`neutrons.py`), which follows them (isotropic, slowing down) through the shield.

Left out: neutral pions' electromagnetic showers, muons (charged pions in rock interact before they decay),
elastic scattering of the high-energy particles, and nuclear fragments recoiling in the body's own tissue.
They would add to the dose at depth, so the transport errs low there.
"""

import math
from dataclasses import dataclass

import numpy as np

from . import physics
from .environment import PION_A, SPECIES

NAMES = list(SPECIES)
IDX = {s: i for i, s in enumerate(NAMES)}
CHARGED = [s for s in NAMES if SPECIES[s][1] > 0]
N_LOW_MEV = 20.0
# Fragmentation of the heavy groups at the same energy per nucleon: {group: {lighter group: probability}}.
FRAGMENTS = {
    "Z21-28": {"Z21-28": 0.25, "Z11-20": 0.30, "Z3-10": 0.20},
    "Z11-20": {"Z11-20": 0.25, "Z3-10": 0.40},
    "Z3-10": {"Z3-10": 0.30},
}
ALPHA_SHARE = 0.3          # of the left-over nucleons
CHARGE_EXCHANGE = 0.3
PION_LAMBDA = 1.15         # pions' interaction length over the nucleons'
PION_B = 4.0
M_PION = 139.57            # MeV
PION_THRESHOLD_MEV = 290.0 # nucleon kinetic energy for single-pion production on a nucleon
ALPHA_T_MEV = 30.0
EVAPORATION_MEV = 2.0      # mean kinetic energy of an evaporation neutron
SUBSTEPS = 4


@dataclass
class Knobs:
    leading_z: float = 0.30
    cascade_coeff: float = 0.5
    cascade_t_mev: float = 100.0
    evaporation_coeff: float = 0.2
    alpha_coeff: float = 0.1

    @classmethod
    def from_params(cls, p):
        return cls(p.leading_nucleon_z, p.cascade_nucleons_coeff, p.cascade_nucleon_mev, p.evaporation_neutrons_coeff,
                   p.knockout_alphas_coeff)


class Grid:
    def __init__(self, e_min=1.0, e_max=1e5, n=120):
        self.edges = np.geomspace(e_min, e_max, n + 1)
        self.centres = np.sqrt(self.edges[1:] * self.edges[:-1])
        self.n = n
        self.low_neutron = self.centres < N_LOW_MEV


class MaterialData:
    """Everything the march needs for one material."""

    def __init__(self, mat, grid, knobs):
        self.mat = mat
        self.ranges = physics.RangeTable(mat)
        self.lam = {s: physics.interaction_length(mat, SPECIES[s][0]) for s in NAMES if s != "pi"}
        self.lam["pi"] = PION_LAMBDA * self.lam["p"]
        _, shares = physics.mean_target_mass(mat)
        a13 = sum(w * physics.ELEMENTS[e][1] ** (1 / 3) for e, w in shares.items())
        a06 = sum(w * physics.ELEMENTS[e][1] ** 0.6 for e, w in shares.items())
        e, c = grid.edges, grid.centres
        # Leading nucleon: P(x in bin) for an incident nucleon at each bin centre.
        a = (knobs.leading_z * 2.7 - 1) / (1 - knobs.leading_z)
        x_lo = np.clip(e[None, :-1] / c[:, None], 0, 1)
        x_hi = np.clip(e[None, 1:] / c[:, None], 0, 1)
        self.lead = x_hi ** (a + 1) - x_lo ** (a + 1)                     # [incident j, product i]
        # Cascade nucleons from the target: ν(E) exponential spectrum truncated at E.
        nu = knobs.cascade_coeff * a13 * np.minimum(1.0, c / 500.0)
        t = knobs.cascade_t_mev
        cdf = lambda x, top: (1 - np.exp(-np.minimum(x, top) / t)) / (1 - np.exp(-top / t))
        self.casc = nu[:, None] * (cdf(e[None, 1:], c[:, None]) - cdf(e[None, :-1], c[:, None]))
        # Below the grid's bottom (1 MeV): neutrons from the cascade's low end, counted with the evaporation.
        self.casc_below = nu * cdf(e[0], c)
        self.evap = knobs.evaporation_coeff * a06 * np.minimum(1.0, c / 50.0)
        # Knocked-out light ions (as helium), per collision, in energy per nucleon: [incident j, bin i].
        nu_a = knobs.alpha_coeff * a13
        ca = lambda x: 1 - np.exp(-x / ALPHA_T_MEV)
        self.alphas = (nu_a * np.minimum(1.0, c / 200.0))[:, None] * (ca(e[1:]) - ca(e[:-1]))[None, :]
        # The collision's energy: the leading particle first; the target's products (cascade nucleons, light
        # ions, evaporation neutrons) scaled down where they would take more than it leaves; then charged
        # pions, rest masses included, two thirds of whatever remains (the neutral third is not followed).
        lead_energy = np.maximum((a + 1) / (a + 2) * c, self.lead @ c)          # as filed on the grid, too
        target = target_energy(self.casc, self.casc_below, self.alphas, self.evap, c)
        scale = np.where(target > 0, np.clip((c - lead_energy) / np.maximum(target, 1e-30), 0, 1), 1.0)
        self.casc = self.casc * scale[:, None]
        self.casc_below = self.casc_below * scale
        self.alphas = self.alphas * scale[:, None]
        self.evap = self.evap * scale
        left = np.clip(c - lead_energy - target * scale, 0, None)
        # A pion's total energy y E (y ≥ m_π / E) is spread as A (1 − y)^b / y, with ∫ y dN = f, so the
        # pions' total energy, masses and all, is f E; filed on the pion grid by kinetic energy y E − m_π.
        self.pion_budget = np.where(c >= PION_THRESHOLD_MEV, 2 / 3 * left, 0.0)
        self.pions = pion_kernel(self.pion_budget, c, e)                             # [incident j, pion bin i]
        # Pions as projectiles: the bin's kinetic energy is c × PION_A; same shapes at that energy.
        self.pion_energy = c * PION_A
        self._shift = {}

    def shift(self, species, dx, grid):
        """Edge energies after dx g/cm² of slowing down (0 where stopped)."""
        key = (species, round(dx, 9))
        if key not in self._shift:
            a, z = SPECIES[species]
            r = self.ranges.range(grid.edges, z, a)
            self._shift[key] = self.ranges.energy(r - dx, z, a)
        return self._shift[key]


def target_energy(casc, casc_below, alphas, evap, c):
    """Kinetic energy (MeV) the target's products take per collision at each incident energy c: cascade
    nucleons, those below the grid (~half an MeV each), light ions (four nucleons each) and evaporation
    neutrons (`EVAPORATION_MEV` each)."""
    return casc @ c + 0.5 * casc_below + alphas @ (4 * c) + evap * EVAPORATION_MEV


def pion_kernel(budget, c, edges, b=PION_B):
    """Pions per collision, [incident bin, pion bin], for total-energy fractions y = (T + m_π) / E spread as
    A (1 − y)^b / y on [m_π / E, 1] with ∫ y dN = budget / E."""
    ys = np.linspace(0.0, 1.0, 20001)[1:]
    shape = (1 - ys) ** b / ys
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (shape[1:] + shape[:-1]) * np.diff(ys))])
    ys = ys
    out = np.zeros((len(c), len(edges) - 1))
    for j, energy in enumerate(c):
        if budget[j] <= 0 or energy <= M_PION:
            continue
        y_min = M_PION / energy
        amp = budget[j] / energy * (b + 1) / (1 - y_min) ** (b + 1)              # from ∫ (1 − y)^b dy
        y = np.clip((edges * PION_A + M_PION) / energy, y_min, 1.0)
        out[j] = amp * np.diff(np.interp(y, ys, cum))
    return out


def _rebin(counts, energies, grid):
    """Counts at the given energies (one per bin) filed into the grid's bins by energy."""
    out = np.zeros(grid.n)
    idx = np.searchsorted(grid.edges, energies, side="right") - 1
    ok = (idx >= 0) & (idx < grid.n)
    np.add.at(out, idx[ok], counts[ok])
    return out


def _slow(counts, new_edges, grid):
    """Rebin counts whose bin edges moved to new_edges (monotone, 0 where stopped)."""
    cum = np.concatenate([np.cumsum(counts[::-1])[::-1], [0.0]])      # particles above each old edge
    ok = new_edges > 0
    if not ok.any():
        return np.zeros_like(counts)
    le = np.log(new_edges[ok])
    cv = cum[ok]
    new_cum = np.interp(np.log(grid.edges), le, cv, left=cv[0], right=0.0)
    return np.maximum(new_cum[:-1] - new_cum[1:], 0.0)


class Transport:
    def __init__(self, knobs=None, grid=None):
        self.knobs = knobs or Knobs()
        self.grid = grid or Grid()
        self._mats = {}
        g = self.grid
        self.sv = {}
        self.gy = {}
        for s in NAMES:
            a, z = SPECIES[s]
            if z > 0:
                gy, sv = physics.charged_dose_per_fluence(g.centres, z, a)
            else:
                sv = np.where(g.low_neutron, 0.0, physics.NEUTRON_HIGH_PSV_CM2 * 1e-12)
                gy = sv / physics.NEUTRON_Q["high"]
            self.sv[s], self.gy[s] = sv, gy

    def data(self, mat):
        key = (mat.name, tuple(sorted(mat.fractions.items())))
        if key not in self._mats:
            self._mats[key] = MaterialData(mat, self.grid, self.knobs)
        return self._mats[key]

    def dose(self, state):
        """Dose equivalent and absorbed dose rates per sr, by species, for a state {species: counts}."""
        return ({s: float(state[s] @ self.sv[s]) for s in NAMES}, {s: float(state[s] @ self.gy[s]) for s in NAMES})

    def march(self, layers, incident, step=2.0, first_steps=0.25, record=None, fine=0.2, tail=6.0):
        """Carry the incident intensities {species: per bin} along a ray through layers [(Material, g/cm²)].
        Returns the depths recorded (g/cm² of path; every step, or the first step reaching each depth in
        record), the dose equivalent and absorbed dose there by species (per sr), the low-energy neutron
        source per g/cm² of path, and the final state. Steps are `fine` over the last `tail` g/cm² before each
        recorded depth and the end, where the short-ranged particles must come to their equilibrium (coarse
        steps there misplace them), `first_steps` over the first 10 g/cm², `step` elsewhere."""
        g = self.grid
        state = {s: np.asarray(incident.get(s, np.zeros(g.n)), float).copy() for s in NAMES}
        targets = sorted(record) if record is not None else None
        k = 0
        depth, depths, doses, grays, source = 0.0, [], [], [], []

        def keep():
            sv, gy = self.dose(state)
            depths.append(depth)
            doses.append(sv)
            grays.append(gy)

        while targets is not None and k < len(targets) and targets[k] <= 1e-12:
            k += 1
        keep()
        end = sum(t for _, t in layers)
        for mat, thickness in layers:
            d = self.data(mat)
            done = 0.0
            while done < thickness - 1e-12:
                ahead = end - depth if targets is None or k >= len(targets) else min(targets[k], end) - depth
                size = fine if ahead <= tail + 1e-9 else (step if depth >= 10 else first_steps)
                dx = min(size, thickness - done, max(ahead - tail, fine) if ahead > tail + 1e-9 else size)
                low = self._step(state, d, dx)
                done += dx
                depth += dx
                source.append((depth - dx / 2, low / dx))
                if targets is None:
                    keep()
                elif k < len(targets) and depth >= targets[k] - 1e-9:
                    keep()
                    while k < len(targets) and depth >= targets[k] - 1e-9:
                        k += 1
        return {"depths": np.array(depths), "dose": doses, "gray": grays,
                "source": (np.array([x for x, _ in source]), np.array([v for _, v in source])), "state": state}

    def _step(self, st, d, dx):
        g = self.grid
        ints = {}
        for s in NAMES:
            f = -math.expm1(-dx / d.lam[s])
            ints[s] = st[s] * f
            st[s] = st[s] - ints[s]
        add = {s: np.zeros(g.n) for s in NAMES}
        # Leading nucleons, and the charged pions nucleons make.
        for s, other in (("n", "p"), ("p", "n")):
            lead = ints[s] @ d.lead
            add[s] += (1 - CHARGE_EXCHANGE) * lead
            add[other] += CHARGE_EXCHANGE * lead
            add["pi"] += ints[s] @ d.pions
        # Pions: re-file by kinetic energy on the nucleon grid, then a leading pion and more pions.
        pion_as_nucleon = _rebin(ints["pi"], d.pion_energy, g)
        add["pi"] += _rebin(pion_as_nucleon @ d.lead, g.centres / PION_A, g) + pion_as_nucleon @ d.pions
        # The target's response to every collision, by the projectile's energy per nucleon.
        total = sum(v for k, v in ints.items() if k != "pi") + pion_as_nucleon
        add["He"] += total @ d.alphas
        casc = total @ d.casc
        add["p"] += 0.5 * casc
        add["n"] += 0.5 * casc
        low = float(total @ d.evap) + 0.5 * float(total @ d.casc_below)
        # Ions break up at the same energy per nucleon.
        add["p"] += 2 * ints["He"]
        add["n"] += 2 * ints["He"]
        for grp, prods in FRAGMENTS.items():
            a = SPECIES[grp][0]
            left = a - sum(pr * SPECIES[h][0] for h, pr in prods.items())
            for h, pr in prods.items():
                add[h] += pr * ints[grp]
            add["He"] += ALPHA_SHARE * left / 4 * ints[grp]
            add["p"] += (1 - ALPHA_SHARE) * left / 2 * ints[grp]
            add["n"] += (1 - ALPHA_SHARE) * left / 2 * ints[grp]
        # Slowing down: what was there crosses the whole step; what was made in it, on average half of it
        # (made evenly along the step, so slowed by a share spread over (0, dx), in SUBSTEPS parts).
        for s in CHARGED:
            st[s] = _slow(st[s], d.shift(s, dx, g), g)
            if add[s].any():
                made = np.zeros(g.n)
                for k in range(SUBSTEPS):
                    made += _slow(add[s], d.shift(s, dx * (k + 0.5) / SUBSTEPS, g), g)
                add[s] = made / SUBSTEPS
        for s in NAMES:
            st[s] = st[s] + add[s]
        # Neutrons below 20 MeV leave the ray for the diffusion model.
        low += float(st["n"][g.low_neutron].sum())
        st["n"][g.low_neutron] = 0.0
        return low
