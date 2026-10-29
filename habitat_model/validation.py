"""The notes' key figures, and the model's value for each (plan §1.3).

Each check names the section it comes from. A check with `known` set is a
mismatch that has been looked at; the text says why the model differs.
"""

from dataclasses import dataclass, field
from functools import lru_cache
from typing import Callable, Optional

from .design import SITES, Design
from .materials import tori_supported
from .model import evaluate
from .replication import GW_YR, shipping_energy_per_kg
from .stability import max_tori

KM2, HA, MT, KT, MW, GW = 1e6, 1e4, 1e9, 1e6, 1e6, 1e9


@dataclass(frozen=True)
class Check:
    section: str
    label: str
    design: dict
    value: Callable
    reference: float
    unit: str = ""
    tol: float = 0.05
    known: Optional[str] = None


@dataclass
class Outcome:
    check: Check
    model: float

    @property
    def diff(self):
        return self.model / self.check.reference - 1

    @property
    def ok(self):
        return abs(self.diff) <= self.check.tol


def _d(r, **kw):
    return {"radius_m": r, "n_tori": 1, **kw}


def _sizes(section, label, unit, fn, refs, **kw):
    """One check per radius, for figures quoted at several sizes."""
    known = kw.pop("known", {})
    tol = kw.pop("tol", 0.05)
    return [Check(section, f"{label}, {r / 1000:g} km" if r >= 1000 else f"{label}, {r:g} m",
                  _d(r, **kw), fn, ref, unit, tol, known.get(r))
            for r, ref in refs.items()]


CHECKS = [
    # §1, §2: rotation and floor
    *_sizes("§1", "Rotation", "rpm", lambda r: r["geometry"]["rpm"], {900: 1.0, 1600: 0.75, 2500: 0.6}),
    *_sizes("§1", "Rim speed", "m/s", lambda r: r["geometry"]["rim_speed"], {900: 94, 1600: 126, 2500: 157}),
    *_sizes("§2b", "Floor", "ha", lambda r: r["geometry"]["floor_area"] / HA,
            {400: 6.3, 900: 32, 1600: 100, 2500: 245}),
    *_sizes("§3a", "Torus volume", "m³", lambda r: r["geometry"]["volume"],
            {400: 1.20e6, 900: 1.36e7, 1600: 7.65e7, 2500: 2.92e8}),
    *_sizes("§12", "Hub radius", "m", lambda r: r["geometry"]["hub_radius"], {900: 60, 1600: 110, 2500: 170}),
    # §3c, §4: atmosphere
    *_sizes("§4", "N₂", "kt", lambda r: r["mass"]["n2"] / KT, {900: 7.9, 1600: 44.5, 2500: 170}),
    *_sizes("§4", "O₂", "kt", lambda r: r["mass"]["o2"] / KT, {900: 3.7, 1600: 20.7, 2500: 80}),
    # §5c mass model
    *_sizes("§5c", "Rock shield after fill credit", "Mt", lambda r: r["mass"]["shield"] / MT,
            {400: 2.4, 900: 11.0, 1600: 33.5, 2500: 80, 3600: 165}),
    *_sizes("§5c", "Fill", "Mt", lambda r: r["mass"]["fill"] / MT,
            {400: 0.11, 900: 0.54, 1600: 1.7, 2500: 4.2, 3600: 8.6}),
    *_sizes("§5c", "Hull and frames", "Mt", lambda r: r["mass"]["hull_frames"] / MT,
            {400: 0.05, 900: 0.30, 1600: 1.1, 2500: 3.1, 3600: 7.0},
            known={400: "the notes round 0.047 Mt to 0.05"}),
    *_sizes("§5c", "Spokes", "Mt", lambda r: r["mass"]["spokes"] / MT,
            {400: 0.08, 900: 0.87, 1600: 4.9, 2500: 19.1, 3600: 60}),
    *_sizes("§5c", "Total per torus", "Mt", lambda r: r["mass"]["total"] / MT,
            {400: 2.7, 900: 12.8, 1600: 41.5, 2500: 108, 3600: 243}),
    *_sizes("§5c", "Mass per m² of floor", "t", lambda r: r["mass"]["per_floor"] / 1e3,
            {400: 42, 900: 40, 1600: 41, 2500: 44, 3600: 48}),
    *_sizes("§8", "Steel per torus", "Mt", lambda r: r["mass"]["steel"] / MT, {900: 1.2, 1600: 6.0, 2500: 22}),
    # §9 reduced gravity
    *_sizes("§9", "Steel at 0.3 g", "Mt", lambda r: r["mass"]["steel"] / MT, {900: 0.34, 1600: 1.7, 2500: 6.1}, g=0.3),
    *_sizes("§9", "Total at 0.3 g", "Mt", lambda r: r["mass"]["total"] / MT, {900: 12.0, 1600: 37.2, 2500: 91.5}, g=0.3),
    *_sizes("§9", "Period at 0.3 g", "s", lambda r: r["geometry"]["period"], {900: 110, 1600: 146, 2500: 183}, g=0.3),
    # §7, §10 water, volatiles, metal
    *_sizes("§7", "Water needed (soil, lakes, O₂, ballast, vegetation)", "Mt",
            lambda r: r["mass"]["water_needed"] / MT, {900: 0.12, 1600: 0.38, 2500: 0.96}),
    *_sizes("§7", "Spin-up propellant (water, 3 km/s)", "Mt", lambda r: r["mass"]["spinup_propellant"] / MT,
            {900: 0.40, 1600: 1.7, 2500: 5.6}),
    *_sizes("§7", "C-type sized by nitrogen", "Mt", lambda r: r["materials"]["c_type"] / MT,
            {900: 5, 1600: 27, 2500: 100}),
    Check("§7", "C-type with water spin-up, 900 m", _d(900, water_spinup=True),
          lambda r: r["materials"]["c_type"] / MT, 8, "Mt"),
    *_sizes("§10", "C-type water contained", "Mt", lambda r: r["materials"]["c_water_contained"] / MT,
            {900: 0.32, 1600: 1.7, 2500: 6.5}),
    *_sizes("§10", "C-type diameter", "m", lambda r: r["materials"]["c_diameter"],
            {900: 200, 1600: 350, 2500: 540}),
    *_sizes("§10", "Total metal (with hub, dock, factory)", "Mt", lambda r: r["materials"]["metal_needed"] / MT,
            {900: 1.5, 1600: 7.5, 2500: 28}),
    *_sizes("§10", "Regolith (0.5 m)", "Mt", lambda r: r["mass"]["regolith"] / MT, {900: 0.29, 1600: 0.9, 2500: 2.2}),
    *_sizes("§10", "Soil (0.5 m)", "Mt", lambda r: r["mass"]["soil"] / MT, {900: 0.25, 1600: 0.8, 2500: 2.0}),
    *_sizes("§10", "S-type, H host", "Mt", lambda r: r["materials"]["s_type"] / MT,
            {900: 14, 1600: 44, 2500: 165}, host_class="H"),
    *_sizes("§10", "S-type, LL host", "Mt", lambda r: r["materials"]["s_type"] / MT,
            {900: 32, 1600: 165, 2500: 620}, host_class="LL"),
    Check("§10", "S-type, L host, 900 m", _d(900, host_class="L"), lambda r: r["materials"]["s_type"] / MT, 16, "Mt"),
    Check("§10", "S-type diameter, H host, 900 m", _d(900, host_class="H"),
          lambda r: r["materials"]["s_diameter"], 235, "m"),
    # §13 power, food
    *_sizes("§13", "Valley lighting", "MW", lambda r: r["power"]["valley_sky"] / MW, {900: 53, 1600: 166, 2500: 410}),
    *_sizes("§13", "Valley + other loads", "MW", lambda r: r["power"]["valley"] / MW, {900: 57, 1600: 180, 2500: 440}),
    *_sizes("§13", "Farm lighting per tier", "MW", lambda r: r["power"]["farm_per_tier"] / MW,
            {400: 6.3, 900: 32, 1600: 102, 2500: 247}),
    *_sizes("§13", "Plain rim solar", "MW", lambda r: r["power"]["plain_rim_pv"] / MW, {900: 34, 1600: 110, 2500: 270}),
    *_sizes("§13", "Array at 1 AU, valley", "km²", lambda r: r["power"]["array_1au_valley"] / KM2,
            {900: 0.27, 1600: 0.85, 2500: 2.1}),
    *_sizes("§13", "Array at 1 AU, per tier", "km²", lambda r: r["power"]["array_1au_per_tier"] / KM2,
            {900: 0.15, 1600: 0.48, 2500: 1.16}),
    *_sizes("§13", "Array at 1 AU, three tiers", "km²", lambda r: r["power"]["array_1au"] / KM2,
            {900: 0.71, 1600: 2.3, 2500: 5.6}, tiers_lit=3),
    *_sizes("§8", "Farm ring area per tier", "ha", lambda r: r["geometry"]["farm_ring_area"] / HA,
            {900: 11, 1600: 36, 2500: 88}),
    *_sizes("§13", "Crops per tier", "ha", lambda r: r["geometry"]["crop_area_per_tier"] / HA,
            {400: 1.8, 900: 9.0, 1600: 29, 2500: 70}),
    Check("§13", "Light per person", _d(900), lambda r: r["food"]["mol_per_person"], 3200, "mol/day"),
    Check("§13", "Crop area per person", _d(900), lambda r: r["food"]["crop_area_per_person"], 89, "m²"),
    Check("§13", "Food per m² of crops", _d(900), lambda r: r["food"]["kcal_per_m2"], 26, "kcal/day"),
    Check("§13", "Electricity per person", _d(900), lambda r: r["food"]["power_per_person"] / 1e3, 31, "kW"),
    *_sizes("§13", "People per tier lit", "", lambda r: r["food"]["people_per_tier"],
            {400: 200, 900: 1000, 1600: 3250, 2500: 7900}),
    *_sizes("§13", "People, three tiers lit", "", lambda r: r["food"]["people"],
            {900: 3050, 1600: 9750, 2500: 23700}, tiers_lit=3),
    *_sizes("§13", "Floor per person, one tier", "m²", lambda r: r["food"]["floor_per_person"],
            {900: 310, 1600: 310, 2500: 310}),
    *_sizes("§13", "Farm ring mass", "kt", lambda r: r["mass"]["farm_ring"] / KT, {900: 50, 1600: 150}),
    # §13 heat
    *_sizes("§13", "Radiating surface, valley", "ha", lambda r: r["heat"]["radiating_surface_valley"] / HA,
            {900: 16, 1600: 48, 2500: 117}),
    *_sizes("§13", "Radiating surface per tier", "ha", lambda r: r["heat"]["radiating_surface_per_tier"] / HA,
            {900: 8.5, 1600: 27, 2500: 66}),
    *_sizes("§13", "End openings (both)", "km²", lambda r: r["heat"]["openings"] / KM2, {900: 4.4, 1600: 14}),
    *_sizes("§13", "Capacity of the end openings", "GW", lambda r: r["heat"]["capacity"] / GW, {900: 1.6, 1600: 5.3}),
    Check("§13", "Break-even, 900 m, no farm lit", _d(900, tiers_lit=0),
          lambda r: r["heat"]["break_even_tori"], 29, "tori", tol=0.1),
    Check("§13", "Break-even, 1.6 km, no farm lit", _d(1600, tiers_lit=0),
          lambda r: r["heat"]["break_even_tori"], 29, "tori", tol=0.1),
    Check("§13", "Heat, 900 m pair, three tiers lit", {"radius_m": 900, "n_tori": 2, "tiers_lit": 3},
          lambda r: r["heat"]["stack"] / MW, 310, "MW"),
    Check("§13", "Heat, 900 m six-stack, three tiers lit", {"radius_m": 900, "n_tori": 6, "tiers_lit": 3},
          lambda r: r["heat"]["stack"] / MW, 930, "MW"),
    Check("§13", "Array mass, 900 m, valley", _d(900, tiers_lit=0, seasonal_sky=False),
          lambda r: r["power"]["array_site_mass"] / KT, 0.8, "kt"),
    Check("§13", "Radiator panel mass, 900 m, three tiers", _d(900, tiers_lit=3),
          lambda r: r["heat"]["panel_mass"] / KT, 1.0, "kt"),
    # §11 stability (closed form; also checked against the inertia sums in the tests)
    *[Check("§11", f"Max tori, {r / 1000:g} km, {gap} m gaps, {int(m * 100)}% margin", _d(r, gap_m=gap),
            lambda res, m=m: max_tori(res["geometry"]["radius"], res["geometry"]["pitch"], m), ref, "tori")
      for r, gap, m, ref in ((900, 10, 0.0, 27), (900, 10, 0.1, 24), (900, 10, 0.2, 22),
                             (1600, 10, 0.0, 31), (1600, 10, 0.1, 28), (1600, 10, 0.2, 25), (900, 40, 0.2, 16))],
    Check("§11", "Stack length at the limit, 900 m", _d(900), lambda r: r["stability"]["stack_length_at_limit"],
          1800, "m"),
    Check("§0", "Six-stack main section length, 10 m gaps", {"radius_m": 900, "n_tori": 6},
          lambda r: r["geometry"]["main_length"], 480, "m"),
    Check("§0", "Six-stack main section length, 40 m gaps", {"radius_m": 900, "n_tori": 6, "gap_m": 40},
          lambda r: r["geometry"]["main_length"], 660, "m"),
    # §15 seasonal sizing at the sites
    *[Check("§15", f"Array, 900 m valley, constant sky, {site}", _d(900, site=site, seasonal_sky=False, tiers_lit=0),
            lambda r: r["power"]["array_site"] / KM2, ref, "km²")
      for site, ref in (("Itokawa", 0.76), ("Eros", 0.84), ("Torifune", 0.42), ("Apophis", 0.32))],
    *[Check("§15", f"Array, 900 m valley, seasonal sky, {site}", _d(900, site=site, tiers_lit=0),
            lambda r: r["power"]["array_site"] / KM2, ref, "km²")
      for site, ref in (("1 AU", 0.14), ("Itokawa", 0.41), ("Eros", 0.46), ("Torifune", 0.23))],
    *[Check("§15", f"Array, 900 m, per tier, {site}", _d(900, site=site),
            lambda r: r["power"]["array_site_per_tier"] / KM2, ref, "km²")
      for site, ref in (("Itokawa", 0.42), ("Eros", 0.47), ("Torifune", 0.23), ("Apophis 2029", 0.26))],
    Check("§15", "Array, 1.6 km valley, seasonal sky, Eros", _d(1600, site="Eros", tiers_lit=0),
          lambda r: r["power"]["array_site"] / KM2, 1.45, "km²"),
    Check("§15", "Array, 1.6 km, per tier, Eros", _d(1600, site="Eros"),
          lambda r: r["power"]["array_site_per_tier"] / KM2, 1.51, "km²"),
    # §15 tori supported by the candidate bodies
    *[Check("§15", f"900 m tori supported by {name}", _d(900),
            lambda r, name=name: r["_tori"][name], ref, "tori", tol=0.15)
      for name, ref in (("Itokawa", 1), ("Didymos", 30), ("Torifune", 6), ("Ryugu", 90), ("Bennu", 15))],
    Check("§15", "1.6 km tori supported by Ryugu", _d(1600), lambda r: r["_tori"]["Ryugu"], 17, "tori"),
    # §13, §15 processing and shipping
    Check("§15", "Processing energy, 900 m", _d(900, host_class="H"),
          lambda r: r["replication"]["processing"] / GW_YR, 0.3, "GW·yr", tol=0.15),
    *[Check("§15", f"Shipping energy at {dv} km/s", _d(900), lambda r, dv=dv: r["_ship"](dv), ref, "J/kg")
      for dv, ref in ((4.5, 1.2e8), (6.3, 1.75e8), (8.5, 2.5e8))],
]


@lru_cache(maxsize=None)
def _evaluate(p_items, design_items):
    from types import SimpleNamespace
    p = SimpleNamespace(**dict(p_items))
    d = Design(**dict(design_items))
    r = evaluate(p, d)
    r["_tori"] = {name: tori_supported(p, body, r["mass"], r["materials"])
                  for name, body in SITES.items() if body.kind}
    r["_ship"] = lambda dv: shipping_energy_per_kg(p, dv)
    return r


def run(p, checks=CHECKS):
    p_items = tuple(sorted(vars(p).items()))
    return [Outcome(c, c.value(_evaluate(p_items, tuple(sorted(c.design.items()))))) for c in checks]
