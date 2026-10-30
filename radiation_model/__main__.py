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

from . import environment as env, physics, reference, shield, tube

ROCK = "Tailings (L/LL chondrite, metal removed)"
LUNAR = "Lunar regolith (OLTARIS's)"
PROPOSED = 10.0                                           # t/m²
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
        "These are the model's own figures; against OLTARIS (next) they fall too fast with depth in rock.",
    ]


def oltaris_section(m, p):
    rows = []
    mats = (LUNAR, "Water", "Polyethylene")
    prof = {n: m.profile(physics.material(n), [100.0 * t for t in reference.TONNES]) for n in mats}
    for i, t in enumerate(reference.TONNES):
        row = [f"{t:g} t/m²"]
        for n in mats:
            ref = reference.TABLE2[n]
            row.append(f"{num(prof[n][i].total, 2)} / {num(ref[i], 3)}" if i < len(ref) else "—")
        rows.append(row)
    model_need = [needed([100.0 * t for t in reference.TONNES], prof[n], p.dose_limit_msv_yr) for n in mats]
    olt_need = [reference.needed(n, p.dose_limit_msv_yr) for n in mats]
    rows.append([f"**{p.dose_limit_msv_yr:g} mSv/yr**"] + [f"**{num(a, 2)} / {num(b, 3)} t/m²**" for a, b in
                                                         zip(model_need, olt_need)])
    tail = m.profile(physics.material(ROCK), [900.0, 1100.0])
    lun = m.profile(physics.material(LUNAR), [900.0, 1100.0])
    ratio = tail[1].total / lun[1].total
    return ratio, [
        "## Against OLTARIS",
        "OLTARIS (NASA's HZETRN, with its neutrons' angular spread) for the same sphere, from Globus & Strout "
        "(2017, Table 2: the 1977–78 solar minimum, effective dose on a female body model). Model / OLTARIS, "
        "mSv/yr:",
        table(["Shield", "Lunar regolith", "Water", "Polyethylene"], rows),
        "Two differences, both expected: shallow, the model's point dose runs ~2× OLTARIS's dose averaged "
        "over a body, which shields its own organs from the heavy ions; deep, the model falls too fast, e-fold "
        "every ~1.7 t/m² of rock against OLTARIS's ~2.3, so behind 9–11 t/m² of regolith it is 2–3× low. "
        "For water the two cross near the limit and agree on the thickness; for rock the model's ~8.8 t/m² "
        f"is too thin, and OLTARIS's ~{num(olt_need[0], 3)} t/m² (the notes' ~11) stands. Two cascade inputs "
        "can't match all three materials at once (fitting rock's slope puts water ~2.5× high), so the model "
        "is kept for what it compares, and the sizing below rests on OLTARIS's curve.",
        f"Its comparison of rock types holds better than its depth: the tailings, richer in iron and "
        f"magnesium than lunar regolith, come out within ~{abs(ratio - 1):.0%} of it at 9–11 t/m² "
        "(about as much neutron-making per tonne), so OLTARIS's regolith curve stands for the tailings.",
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
        "OLTARIS agrees on the direction (Janhunen 2020): 8.68 t/m² of dry regolith with 0.18 t/m² of water and "
        "1 kg/m² of boron-10 inside it (and 0.18 t/m² of iron outside) gives 20 mSv/yr at a sphere's centre, "
        f"~{num(sum(reference.JANHUNEN['layers_t_m2'].values()), 3)} t/m² in all against "
        f"~{num(reference.needed(LUNAR, 20), 3)} t/m² of bare regolith.",
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
        "## Inside the tube, straight ahead",
        "The 900 m torus's cross-section (`radiation_model/tube.py`): the tube (radius 28 m), the jacket "
        "(thinner under the fill by its credit, as the system model has it), the 1 m fill over the lower half. "
        "Rays to every direction, their path through rock and fill counted as tailings, the tube taken as "
        "straight (its radius is 1/32 of the torus's); slow neutrons as from the slab. Neighbouring tori, the "
        "hub and the farm section, which hide some of the sky in a stack, are left out.",
        table(["Jacket", "Sphere centre", "On the floor (1.5 m up)", "Tube's centre", "Under the ceiling",
               "Cliff dwelling behind 2 m of soil"], rows),
        "Straight ahead, a long tube shields better than a sphere of the same wall: a ray leaving at an angle "
        "ψ to its axis crosses 1/sin ψ times the wall, so the model puts the floor and the walls at ~¼ of the "
        "sphere's dose and the axis at ~½. That overstates it: in OLTARIS a point at the wall of a slab gets "
        f"~{reference.WALL_FACTOR:.0%} of the sphere's centre (Janhunen 2020), because deep in the shield the "
        "dose comes from particles spread in angle (neutrons above all), which slant paths don't stop as well. "
        "The sizing takes OLTARIS's ½ near the walls.",
    ]


def jacket_section(p, ratio):
    rows = []
    for t in (8.0, 9.0, 10.0, 11.0, 12.0):
        sphere = float(reference.table2(LUNAR, t)) * ratio
        rows.append([f"{t:g} t/m²" + (" (configured)" if t == p.shield_areal_t_m2 else "")
                     + (" (proposed)" if t == PROPOSED else ""), num(sphere, 2),
                     num(sphere * reference.WALL_FACTOR, 2), num(sphere * reference.JANHUNEN["solar_max_centre"]
                                                                 / reference.JANHUNEN["sphere_centre"], 2)])
    limit = p.dose_limit_msv_yr
    centre_need = reference.needed(LUNAR, limit, ratio)
    wall_need = reference.needed(LUNAR, limit, ratio * reference.WALL_FACTOR)
    thick = lambda x, sig: f"~{num(x, sig)} t/m²" if x is not None else "more than 30 t/m² (beyond the curve)"
    return [
        "## The jacket's thickness",
        "OLTARIS's lunar regolith curve (Globus & Strout, Table 2, extended past 11 t/m² at its last slope), "
        "scaled to the tailings by the model, for a sphere's centre, which bounds the tube's middle; near the "
        f"walls (the floor, the cliff dwellings, under the ceiling) OLTARIS's slab factor, "
        f"~{reference.WALL_FACTOR:.2f}. Solar maximum: 25% less (Janhunen). mSv/yr:",
        table(["Jacket", "Sphere's centre (the tube's middle, at most)", "Near the walls, where people live",
               "Sphere's centre, solar maximum"], rows),
        f"**{limit:g} mSv/yr is met at a sphere's centre with {thick(centre_need, 3)} and near the walls with "
        f"{thick(wall_need, 2)}.** The configured {p.shield_areal_t_m2:g} t/m² gives "
        f"~{num(float(reference.table2(LUNAR, p.shield_areal_t_m2)) * ratio, 2)} mSv/yr at a sphere's centre and "
        f"~{num(float(reference.table2(LUNAR, p.shield_areal_t_m2)) * ratio * reference.WALL_FACTOR, 2)} near the "
        "walls. **Proposed: "
        f"{PROPOSED:g} t/m²** (~5 m of rock): ~{num(float(reference.table2(LUNAR, PROPOSED)) * ratio * reference.WALL_FACTOR, 2)} "
        f"mSv/yr where people live, and ~{num(float(reference.table2(LUNAR, PROPOSED)) * ratio, 2)} at worst in "
        "the middle of the tube, where nobody lives (less still with the stack's shading and the body's own). "
        f"The system model keeps {p.shield_areal_t_m2:g} t/m² until a run in the tube's own geometry (OLTARIS "
        "or Geant4) confirms the factor near the walls.",
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
        "The cascade's guessed inputs move the model's dose behind 11 t/m² by about −40% / +60%, its thickness "
        "for the limit by ±0.7 t/m²; none of them closes the gap to OLTARIS at depth on its own.",
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
    _, materials = materials_section(m, p)
    ratio, oltaris = oltaris_section(m, p)
    rock_profile = m.profile(physics.material(ROCK), depth_grid(shield.CAP))
    _, tube_part = tube_section(m, p, rock_profile)
    parts = [
        "# Radiation transport: how much shield",
        "Plan §3 (`radiation_model/`). Galactic cosmic rays carried through the shield by a one-dimensional "
        "straight-ahead transport along each ray (`transport.py`, as HZETRN does in its classic form): "
        "protons, neutrons, helium and three heavier groups, and the charged pions they make, slowing down "
        "and colliding (leading nucleons, cascade nucleons, evaporation neutrons, knocked-out light ions, "
        "fragments); the slow neutrons followed by two-group diffusion across the shield (`neutrons.py`); "
        "then the directions, at a sphere's centre or inside the torus's tube (`tube.py`). Geant4 and "
        "OLTARIS can't run here; this is a stand-in, with its cascade's inputs guessed, checked against the "
        "figures below and against OLTARIS's published results (`reference.py`), which in the end size the "
        "jacket. Left out: the neutral pions' showers, muons, elastic scattering, angular spread, and the "
        "fragments that recoil in the body's own tissue.",
        *check_section(m, p),
        *materials,
        *oltaris,
        *tube_part,
        *layer_section(m, p, 900.0),
        *event_section(m, p),
        *sensitivity_section(p),
        *jacket_section(p, ratio),
        *impact_section(p, PROPOSED),
        "Not modelled: the stack's neighbouring tori, hub and farm section shading the sky (less dose), "
        "the hub-facing side's services and train tube, the body's self-shielding in the model's own figures "
        "(OLTARIS's include it), capture gamma rays from the slow neutrons, and seasonal or long-term changes "
        "of the heliosphere (OLTARIS's 1977–78 minimum is milder than 2009–10's).",
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
