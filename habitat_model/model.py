"""Chain the modules into one evaluation of a design. All results are in SI units (m, kg, W, J)."""

from . import food, geometry, heat, mass, materials, power, replication, stability
from .assumptions import load, params


def evaluate(p, d):
    geo = geometry.compute(p, d)
    m = mass.compute(p, d, geo)
    mat = materials.compute(p, d, geo, m)
    f = food.compute(p, d, geo)
    pw = power.compute(p, d, geo)
    return {
        "geometry": geo,
        "mass": m,
        "materials": mat,
        "food": f,
        "power": pw,
        "heat": heat.compute(p, d, geo, pw),
        "stability": stability.compute(p, d, geo),
        "replication": replication.compute(p, d, geo, m, mat),
    }


def evaluate_default(d, **overrides):
    """Evaluate with the default assumptions file, plus overrides."""
    return evaluate(params(load(), **overrides), d)


# Outputs ranked by the sensitivity sweep (plan §1.4).
METRICS = {
    "mass_per_floor": ("Mass per m² of floor", "t/m²", lambda r: r["mass"]["per_floor"] / 1e3),
    "s_type_mined": ("Rock mined per torus (S-type)", "Mt", lambda r: r["materials"]["s_type"] / 1e9),
    "c_type": ("C-type per torus", "Mt", lambda r: r["materials"]["c_type"] / 1e9),
    "array_area": ("Despun array at the site", "km²", lambda r: r["power"]["array_site"] / 1e6),
    "people": ("People per torus", "", lambda r: r["food"]["people"]),
    "heat_margin": ("Heat margin (capacity / stack heat)", "×", lambda r: r["heat"]["margin"]),
    "processing_energy": ("Processing energy per torus", "PJ", lambda r: r["replication"]["processing"] / 1e15),
}


def metrics(results):
    return {key: fn(results) for key, (_, _, fn) in METRICS.items()}
