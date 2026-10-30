"""Dose behind a shield (plan §3): the transport along rays, the neutrons' diffusion, and the directions.

The reference geometry is the centre of a large spherical shell (as OLTARIS's sphere): every direction
crosses the same shield, outer layer first. For one material the production of slow neutrons per g/cm² of
path doesn't depend on how thick the shield is, so one long ray serves every thickness.
"""

import math
from dataclasses import dataclass

import numpy as np

from . import environment as env, neutrons, physics
from .transport import Knobs, Transport

YEAR = env.SECONDS_PER_YEAR
CAP = 4000.0          # g/cm² of path beyond which production is negligible


@dataclass
class Dose:
    """Dose equivalent rates, mSv/yr, at the centre of the shell."""
    charged: float           # protons and ions straight ahead
    by_species: dict
    neutron_high: float      # neutrons above 20 MeV, straight ahead
    neutron_fast: float      # 0.1–20 MeV, diffused
    neutron_thermal: float
    gray: float              # absorbed dose, mGy/yr

    @property
    def total(self):
        return self.charged + self.neutron_high + self.neutron_fast + self.neutron_thermal

    @property
    def neutron_share(self):
        return (self.neutron_high + self.neutron_fast + self.neutron_thermal) / self.total if self.total else 0.0


class Model:
    def __init__(self, p, step=2.0):
        self.p = p
        self.t = Transport(Knobs.from_params(p))
        self.step = step
        self._spectra = {}
        self._profiles = {}

    def incident(self, source="gcr", phi=None):
        phi = self.p.solar_min_phi_mv if phi is None else phi
        key = (source, phi)
        if key not in self._spectra:
            self._spectra[key] = env.spectrum(self.t.grid.edges, source, phi)
        return self._spectra[key]

    def _dose(self, ray_sv, ray_gy, fast, thermal, per=YEAR):
        """Assemble a Dose from the straight-ahead dose per sr at the centre and the neutron fluence rates."""
        k = 4 * math.pi * per * 1e3
        charged = {s: v * k for s, v in ray_sv.items() if s != "n"}
        fast_sv = fast * self.p.fast_neutron_dose_psv_cm2 * 1e-12 * per * 1e3
        thermal_sv = thermal * physics.NEUTRON_THERMAL_PSV_CM2 * 1e-12 * per * 1e3
        gray = (sum(ray_gy.values()) * k + fast_sv / physics.NEUTRON_Q["fast"]
                + thermal_sv / physics.NEUTRON_Q["thermal"])
        return Dose(sum(charged.values()), charged, ray_sv["n"] * k, fast_sv, thermal_sv, gray)

    def profile(self, mat, depths, source="gcr", phi=None):
        """Dose at the centre of shells of one material, for each areal density in depths (g/cm²)."""
        key = (mat.name, source, phi, tuple(depths))
        if key in self._profiles:
            return self._profiles[key]
        inc = self.incident(source, phi)
        out = self.t.march([(mat, CAP)], inc, step=self.step, record=list(depths))
        xs, prod = out["source"]
        production = lambda path, mu: np.interp(path, xs, prod, right=0.0)
        src = neutrons.slab_source(production)
        per = YEAR if source == "gcr" else 1.0
        doses = []
        for t in depths:
            i = int(np.argmin(np.abs(out["depths"] - t)))
            sv, gy = out["dose"][i], out["gray"][i]
            fast, thermal, _ = neutrons.fluence([(mat, t)], src) if t > 0 else (0.0, 0.0, None)
            doses.append(self._dose(sv, gy, fast, thermal, per))
        self._profiles[key] = doses
        return doses

    def layered(self, layers, source="gcr", phi=None, mu_points=8):
        """Dose at the centre of a shell of layers [(Material, g/cm²)], outer first. Slow neutrons from rays at
        every slant through the layers (one march per direction)."""
        inc = self.incident(source, phi)
        total = sum(t for _, t in layers)
        normal = self.t.march(layers, inc, step=self.step)
        mu, w = np.polynomial.legendre.leggauss(mu_points)
        mu = 0.5 * (mu + 1)
        tables = {}
        for m in mu:
            scaled, left = [], CAP
            for mat, t in layers:
                if left <= 0:
                    break
                scaled.append((mat, min(t / m, left)))
                left -= t / m
            xs, prod = self.t.march(scaled, inc, step=self.step)["source"]
            tables[m] = (xs, prod)
        production = lambda path, m: np.interp(path, *tables[m], right=0.0)
        src = neutrons.slab_source(production, mu_points=mu_points)
        fast, thermal, _ = neutrons.fluence(layers, src) if total > 0 else (0.0, 0.0, None)
        per = YEAR if source == "gcr" else 1.0
        sv, gy = self.t.dose(normal["state"])
        return self._dose(sv, gy, fast, thermal, per)
