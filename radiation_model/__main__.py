"""Radiation transport through the shield (plan §3): dose against areal density for the shield materials,
the neutrons' share, a hydrogen-rich inner layer, a solar particle event, the tube's geometry, and what the
dose means for the jacket's thickness.

python -m radiation_model [--set name=value ...]
"""

import argparse
import math
import sys

import numpy as np

from habitat_model import Design, evaluate, load, params
from habitat_model.__main__ import parse_override
from habitat_model.report import num, table

from . import environment as env, physics, shield, tube

ROCK = "Tailings (L/LL chondrite, metal removed)"
MATERIALS = (ROCK, "CI-like clays (C-type)", "Water", "Polyethylene")
AREALS = (0, 1, 2, 3, 5, 7, 9, 11, 13, 15, 20)            # t/m²
STEP = 50.0                                               # g/cm² between recorded depths for the sweeps
SWEPT = ("solar_min_phi_mv", "leading_nucleon_z", "cascade_nucleons_coeff", "cascade_nucleon_mev",
         "evaporation_neutrons_coeff", "knockout_alphas_coeff", "fast_neutron_dose_psv_cm2")


def needed(depths, doses, limit):
    """Areal density (t/m²) where the dose falls to the limit, by log interpolation."""
    tot = np.array([d.total for d in doses])
    if tot[-1] > limit:
        return None
    return float(np.interp(-math.log(limit), -np.log(np.maximum(tot, 1e-30)), depths)) / 100


def depth_grid(top=2000.0):
    return [float(x) for x in np.arange(0.0, top + 1e-9, STEP)]


def check_section(m, p):
    w = physics.material("Water")
    rt = physics.RangeTable(w)
    air = physics.Material("Air", {"N": 0.755, "O": 0.232, "C": 0.0003}, 0.0012)
    lam_air = _nucleon_attenuation(m, air)
    free = m.profile(physics.material(ROCK), [5.0])[0]
    rows = [
        ["Proton range in water, 100 MeV", f"{num(float(rt.range(100.0)), 3)} g/cm²", "7.72 g/cm² (NIST PSTAR)"],
        ["… 1 GeV", f"{num(float(rt.range(1000.0)), 3)} g/cm²", "~324 g/cm² (PSTAR)"],
        ["Inelastic cross section, p + O", f"{num(physics.sigma_inelastic(1, 16))} mb", "~300 mb (measured)"],
        ["… C + C", f"{num(physics.sigma_inelastic(12, 12))} mb", "~850–900 mb (measured)"],
        ["Nucleons above 1 GeV in air, attenuation length", f"{num(lam_air)} g/cm²",
         "~120 g/cm² (Gaisser; this air's interaction length is ~7% short)"],
        ["Free space behind 5 g/cm², solar minimum", f"{num(free.total / 1e3, 2)} Sv/yr, {num(free.gray / 1e3, 2)} Gy/yr",
         "~1 Sv/yr, ~0.2–0.3 Gy/yr (recalled): the model runs ~1.5× high here, from its heavy ions"],
    ]
    return [
        "## Checks",
        "Against figures the model should reproduce (all but PSTAR's recalled, not looked up):",
        table(["", "Model", "Reference"], rows),
    ]


def _nucleon_attenuation(m, mat):
    t = m.t
    g = t.grid
    inc = {s: np.zeros(g.n) for s in env.SPECIES}
    inc["p"] = (g.edges[:-1] ** -1.7 - g.edges[1:] ** -1.7) * (g.centres > 10)
    vals = []
    for d in (400.0, 800.0):
        st = t.march([(mat, d)], inc)["state"]
        mask = g.centres > 1000
        vals.append(float(st["p"][mask].sum() + st["n"][mask].sum()))
    return 400 / math.log(vals[0] / vals[1])


def materials_section(m, p):
    depths = depth_grid()
    profiles = {name: m.profile(physics.material(name), depths) for name in MATERIALS}
    rows = []
    for a in AREALS:
        i = depths.index(a * 100.0)
        row = [f"{a:g} t/m²" + (" (unshielded)" if a == 0 else "")]
        for name in MATERIALS:
            d = profiles[name][i]
            row.append(f"{num(d.total, 2)}" + (f" ({d.neutron_share:.0%})" if a else ""))
        rows.append(row)
    need = [num(needed(depths, profiles[n], p.dose_limit_msv_yr), 2) + " t/m²" for n in MATERIALS]
    rows.append([f"**{p.dose_limit_msv_yr:g} mSv/yr reached at**"] + [f"**{x}**" for x in need])
    return profiles, [
        "## Dose against areal density",
        "Dose equivalent (mSv/yr, ICRP 60 quality factors, at a point with no body around it) at the centre "
        "of a large spherical shell, every direction crossing the same shield (as OLTARIS's sphere), galactic "
        f"cosmic rays at a deep solar minimum (φ = {p.solar_min_phi_mv:g} MV); in brackets, the share from "
        "neutrons (above 20 MeV straight ahead, and the slow ones diffusing from the walls).",
        table(["Shield", "Tailings (L/LL, metal removed)", "CI-like clays", "Water", "Polyethylene"], rows),
        "Per tonne, hydrogen shields best: it makes no neutrons of its own and slows the others. The "
        "tailings, rich in iron and magnesium, are the worst of the four; the clays' bound water helps a "
        "little. Behind a few t/m² the dose is mostly secondaries: neutrons (two thirds of it, deep in rock), "
        "pions and the protons and light ions the cascade knocks out, regenerated all the way through; the "
        "heavy ions are gone by ~1 t/m².",
        f"**For water, {need[2]} for {p.dose_limit_msv_yr:g} mSv/yr: OLTARIS (Globus & Strout 2017) gives ~7 "
        f"t/m², so the model agrees where a check exists.** For rock it gives {need[0]} against their ~11 for "
        "regolith (which the notes use as a rock/water equivalence).",
    ]


def layer_section(m, p, base_areal):
    rock, water, pe = (physics.material(n) for n in (ROCK, "Water", "Polyethylene"))
    base = m.layered([(rock, base_areal)])
    rows = []
    for x in (25.0, 50.0, 100.0, 200.0):
        more_rock = m.layered([(rock, base_areal + x)])
        w = m.layered([(rock, base_areal), (water, x)])
        poly = m.layered([(rock, base_areal), (pe, x)])
        rows.append([f"{x / 100:g} t/m²", num(more_rock.total, 2), num(w.total, 2), num(poly.total, 2),
                     num(more_rock.total - w.total, 2)])
    return [
        "## A hydrogen-rich inner layer",
        f"{num(base_areal / 100, 2)} t/m² of tailings (sphere centre: {num(base.total, 2)} mSv/yr, "
        f"{num(base.neutron_fast + base.neutron_thermal, 2)} of it from slow neutrons), then an inner layer: "
        "more tailings, water (moist soil, ponds, tanks) or polyethylene. The slow neutrons are traced at "
        "every slant through the layers.",
        table(["Inner layer", "More tailings", "Water", "Polyethylene", "Water saves, against tailings"],
              rows),
        "A water layer stops the neutrons that diffuse out of the dry rock (a few cm of it already) and shields "
        "the high-energy particles about as well as rock per tonne; the floor's moist fill, the cliff "
        "dwellings' soil and any tanks against the walls do this already.",
    ]


def event_section(m, p):
    rock, water = physics.material(ROCK), physics.material("Water")
    depths = [1.0, 5.0, 10.0, 20.0, 50.0, 100.0]
    r = m.profile(rock, depths, source="spe")
    w = m.profile(water, depths, source="spe")
    rows = [[f"{d:g} g/cm²", num(a.total / 1e3, 2), num(b.total / 1e3, 2)] for d, a, b in zip(depths, r, w)]
    return [
        "## A solar particle event",
        "The August 1972 event's protons (King 1974), taken as isotropic over the event: dose equivalent (Sv) "
        "for the whole event at the centre of the shell.",
        table(["Shield", "Tailings", "Water"], rows),
        "Lethal in a light spacecraft, nothing behind the jacket: the event's protons are spent within a few "
        "tens of g/cm², and what reaches ~1 t/m² is a trickle of neutrons. Crews outside the jacket (the hub, "
        "the farm, the factory) need a storm shelter of ~20–50 g/cm², as the notes have it.",
    ]


def tube_section(m, p, rock_profile):
    depths = depth_grid(shield.CAP)
    hi = np.array([d.charged + d.neutron_high for d in rock_profile]) / (4 * math.pi)
    log_hi = np.log(np.maximum(hi, 1e-30))
    ray = lambda length: np.exp(np.interp(length, depths, log_hi, right=-70.0))
    rows = []
    floor_doses = {}
    for areal in (7, 9, 11, 13):
        q = params(load(), **{**vars(p), "shield_areal_t_m2": areal})
        geo = evaluate(q, Design(radius_m=900, n_tori=6, tiers_lit=3))["geometry"]
        lay = tube.layout(geo, q)
        sph = rock_profile[depths.index(areal * 100.0)]
        slow = sph.neutron_fast + sph.neutron_thermal
        a = lay["a"]
        cliff_angle = math.radians(70)
        cliff = (a * math.sin(cliff_angle) * 0.97, -a * math.cos(cliff_angle) * 0.97)
        inward = (-math.sin(cliff_angle), math.cos(cliff_angle))
        pts = [tube.dose_at(lay, (0, -a + lay["fill"] + 1.5), ray, slow)[0],
               tube.dose_at(lay, (0, 0), ray, slow)[0],
               tube.dose_at(lay, (0, a - 2), ray, slow)[0],
               tube.dose_at(lay, cliff, ray, slow, cover=(2 * p.soil_density * 100, inward))[0]]
        floor_doses[areal] = pts
        rows.append([f"{areal} t/m² ({num(lay['jacket'], 2)} m; {num(lay['jacket_under_fill'], 2)} m under the fill)",
                     num(sph.total, 2)] + [num(x, 2) for x in pts])
    return floor_doses, [
        "## Inside the tube",
        "The 900 m torus's cross-section (`radiation_model/tube.py`): the tube (radius 28 m), the jacket "
        "(thinner under the fill by its credit, as the system model has it), the 1 m fill over the lower half. "
        "Rays to every direction, their path through rock and fill counted as tailings, the tube taken as "
        "straight (its radius is 1/32 of the torus's); slow neutrons as from the slab. Neighbouring tori, the "
        "hub and the farm section, which hide some of the sky in a stack, are left out.",
        table(["Jacket", "Sphere centre", "On the floor (1.5 m up)", "Tube's centre", "Under the ceiling",
               "Cliff dwelling behind 2 m of soil"], rows),
        "A long tube shields better than a sphere of the same wall: a ray leaving at an angle ψ to its axis "
        "crosses 1/sin ψ times the wall, so only the directions across the tube see the jacket's thickness. "
        "On the floor and against the walls the dose is about a quarter of the sphere's; on the tube's axis "
        "about half.",
    ]


def sensitivity_section(p):
    rows = []
    depths = depth_grid(1600.0)
    i11 = depths.index(1100.0)
    for name in SWEPT:
        a = load()[name]
        cells = []
        for v in (a.low, a.high):
            m = shield.Model(params(load(), **{**vars(p), name: v}))
            prof = m.profile(physics.material(ROCK), depths)
            cells.append((prof[i11].total, needed(depths, prof, p.dose_limit_msv_yr)))
        rows.append([f"`{name}`", f"{num(a.low, 3)} – {num(a.high, 3)}", a.status,
                     f"{num(cells[0][0], 2)} – {num(cells[1][0], 2)}",
                     f"{num(cells[0][1], 2)} – {num(cells[1][1], 2)} t/m²"])
    return [
        "## What moves it",
        "Each input at its low and high, the rest as configured: the tailings at the sphere's centre.",
        table(["Input", "Range", "Status", "Dose at 11 t/m², mSv/yr", f"For {p.dose_limit_msv_yr:g} mSv/yr"], rows),
        "The cascade's guessed inputs move the dose behind 11 t/m² by about −40% / +60%, but the thickness "
        "for the limit by only ±0.6 t/m²: deep in the shield the dose falls e-fold every ~1.7 t/m².",
    ]


def impact_section(p, proposed):
    rows = []
    for radius, name in ((900, "900 m"), (1600, "1.6 km")):
        des = Design(radius_m=radius, n_tori=6, tiers_lit=3, host_class="LL", site="Eros", c_partner="Ryugu")
        before = evaluate(p, des)
        after = evaluate(params(load(), **{**vars(p), "shield_areal_t_m2": proposed}), des)
        for label, get, unit, scale in (
            ("Rock shield per torus", lambda r: r["mass"]["shield"], "Mt", 1e9),
            ("Mass per torus", lambda r: r["mass"]["total"], "Mt", 1e9),
            ("Mass per m² of floor", lambda r: r["mass"]["total"] / r["geometry"]["floor_area"], "t", 1e3),
            ("S-type mined per torus", lambda r: r["materials"]["s_type"], "Mt", 1e9),
            ("Generation time, six-stack", lambda r: r["replication"]["generation_time_yr"], "yr", 1),
        ):
            x, y = get(before), get(after)
            rows.append([name, label, f"{num(x / scale)} {unit}", f"{num(y / scale)} {unit}", f"{(y / x - 1) * 100:+.0f}%"])
    return [
        "## What it would mean",
        f"The system model with a {proposed:g} t/m² jacket in place of {p.shield_areal_t_m2:g} t/m²: a "
        "six-stack at Eros (LL host, Ryugu as the C-type), three tiers lit.",
        table(["Torus", "", f"{p.shield_areal_t_m2:g} t/m²", f"{proposed:g} t/m²", "Change"], rows),
    ]


def report(p):
    m = shield.Model(p)
    proposed = 9.0
    profiles, materials = materials_section(m, p)
    rock_profile = m.profile(physics.material(ROCK), depth_grid(shield.CAP))
    floor_doses, tube_part = tube_section(m, p, rock_profile)
    need_rock = needed(depth_grid(), profiles[ROCK], p.dose_limit_msv_yr)
    at11 = profiles[ROCK][depth_grid().index(1100.0)]
    parts = [
        "# Radiation transport: how much shield",
        "Plan §3 (`radiation_model/`). Galactic cosmic rays carried through the shield by a one-dimensional "
        "straight-ahead transport along each ray (`transport.py`, as HZETRN does in its classic form): "
        "protons, neutrons, helium and three heavier groups, and the charged pions they make, slowing down "
        "and colliding (leading nucleons, cascade nucleons, evaporation neutrons, knocked-out light ions, "
        "fragments); the slow neutrons followed by two-group diffusion across the shield (`neutrons.py`); "
        "then the directions, at a sphere's centre or inside the torus's tube (`tube.py`). Geant4 and "
        "OLTARIS can't run here; this is a stand-in, with its cascade's inputs guessed and checked against "
        "the few figures below. Left out: the neutral pions' showers, muons, elastic scattering, and the "
        "fragments that recoil in the body's own tissue, all of which would add to the dose at depth.",
        *check_section(m, p),
        *materials,
        *tube_part,
        *layer_section(m, p, 900.0),
        *event_section(m, p),
        *sensitivity_section(p),
        "## The jacket's thickness",
        f"At the configured {p.shield_areal_t_m2:g} t/m² the model gives ~{num(at11.total, 2)} mSv/yr at a "
        f"sphere's centre and ~{num(floor_doses[11][0], 2)} on the tube's floor, against the "
        f"{p.dose_limit_msv_yr:g} mSv/yr the jacket was sized for: the notes' ~11 t/m² (Globus & Strout's "
        f"regolith figure, for a sphere) is conservative. A sphere needs ~{num(need_rock, 2)} t/m² of tailings; "
        f"inside the tube ~{proposed:g} t/m² gives ~{num(floor_doses[9][0], 2)} mSv/yr on the floor and "
        f"~{num(floor_doses[9][1], 2)} at the tube's centre, leaving a factor ~2 or more for what the transport "
        f"leaves out. **Proposed: a {proposed:g} t/m² jacket**, kept at {p.shield_areal_t_m2:g} t/m² in the "
        "system model until a full transport code (OLTARIS, Geant4) confirms the curve for rock.",
        *impact_section(p, proposed),
        "Not modelled: the stack's neighbouring tori, hub and farm section shading the sky (less dose), "
        "the hub-facing side's services and train tube, the body's self-shielding (effective dose is lower "
        "than the point dose here), solar maximum (the dose behind the jacket barely changes), capture "
        "gamma rays from the slow neutrons, and seasonal or long-term changes of the heliosphere.",
    ]
    return "\n\n".join(parts) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m radiation_model", description=__doc__)
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE")
    args = ap.parse_args(argv)
    print(report(params(load(), **dict(args.set))), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
