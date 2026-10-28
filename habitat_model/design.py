"""Design choices (what is being built, and where) and the candidate bodies."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Design:
    radius_m: float = 900.0      # floor (outer rim) radius
    n_tori: int = 2              # tori in the co-rotating stack
    tiers_lit: int = 1           # farm tiers lit, 0-3
    host_class: str = "L"        # S-type host's ordinary-chondrite class: H, L or LL
    site: str = "1 AU"           # orbit, for the solar sizing (see SITES)
    c_partner: str = "Ryugu"     # C-type supplying the volatiles
    gap_m: float = 10.0          # gap between neighbouring tori
    g: float = 1.0               # spin gravity, in units of the 1 g family (pi^2 m/s^2)
    water_spinup: bool = False   # spin-up with water thrusters (else rock in a mass driver)
    seasonal_sky: bool = True    # valley sky follows the host's seasons (§15)
    factory_power_gw: float = 1.0
    delta_v_km_s: Optional[float] = None  # C-type -> site; looked up in DELTA_V_KM_S if None

    def __post_init__(self):
        if self.host_class not in ("H", "L", "LL"):
            raise ValueError(f"host class must be H, L or LL, not {self.host_class!r}")
        if self.site not in SITES:
            raise ValueError(f"unknown site {self.site!r}; known: {', '.join(SITES)}")
        if self.c_partner not in SITES or SITES[self.c_partner].kind != "C":
            raise ValueError(f"{self.c_partner!r} is not a known C-type")
        if not 0 <= self.tiers_lit <= 3:
            raise ValueError("tiers lit must be 0-3")
        if self.n_tori < 1:
            raise ValueError("a stack needs at least one torus")


@dataclass(frozen=True)
class Body:
    name: str
    kind: str                  # "S", "C" or "" for a plain orbit
    host_class: Optional[str]  # ordinary-chondrite class for S-types (conservative where uncertain)
    a_au: float
    e: float
    mass_mt: Optional[float]
    note: str = ""

    @property
    def aphelion_sunlight(self):
        return 1.0 / (self.a_au * (1 + self.e)) ** 2

    @property
    def perihelion_sunlight(self):
        return 1.0 / (self.a_au * (1 - self.e)) ** 2


# §15, candidate bodies (masses are central estimates).
SITES = {
    "1 AU": Body("1 AU", "", None, 1.0, 0.0, None, "reference circular orbit"),
    "Itokawa": Body("Itokawa", "S", "LL", 1.32, 0.28, 35, "LL-like samples"),
    "Apophis": Body("Apophis", "S", "LL", 0.92, 0.19, 50, "today's orbit; ~40-60 Mt"),
    "Apophis 2029": Body("Apophis 2029", "S", "LL", 1.103, 0.189, 50, "orbit after the 2029 flyby (approx.)"),
    "Eros": Body("Eros", "S", "LL", 1.46, 0.22, 6.7e6, "L- or LL-like; LL taken"),
    "Didymos": Body("Didymos", "S", "L", 1.64, 0.38, 500, "L-like spectra"),
    "Torifune": Body("Torifune", "S", "L", 1.03, 0.22, 100, "L-like spectra; ~40 Mt at the smallest size"),
    "Bennu": Body("Bennu", "C", None, 1.13, 0.20, 73),
    "Ryugu": Body("Ryugu", "C", None, 1.19, 0.19, 450),
}

# §15, rendezvous delta-v from C-type to S-type site, km/s (dated where the notes give it).
DELTA_V_KM_S = {
    ("Ryugu", "Eros"): 4.7,
    ("Ryugu", "Itokawa"): 6.3,
    ("Ryugu", "Apophis 2029"): 5.5,
    ("Ryugu", "Torifune"): 7.6,
    ("Bennu", "Eros"): 6.2,
    ("Bennu", "Itokawa"): 8.5,
    ("Bennu", "Apophis"): 9.2,
    ("Bennu", "Apophis 2029"): 7.4,
    ("Bennu", "Torifune"): 8.4,
}
