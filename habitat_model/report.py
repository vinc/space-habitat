"""Markdown and JSON output: the notes' §0 tables, a design summary, validation and sensitivity (plan §1.5)."""

import math

from .design import SITES, Design
from .materials import tori_supported
from .model import METRICS, evaluate

KM2, HA, MT, KT, MW, GW, PJ = 1e6, 1e4, 1e9, 1e6, 1e6, 1e9, 1e15
SIZES = ((900, "900 m / 60 s"), (1600, "1.6 km / 80 s"), (2500, "2.5 km / 100 s"))


def num(x, sig=3):
    """Round to `sig` significant figures, with thousands separators."""
    if x is None:
        return "—"
    if x == 0:
        return "0"
    digits = sig - 1 - math.floor(math.log10(abs(x)))
    rounded = round(x, digits)
    if digits <= 0:
        return f"{int(rounded):,}"
    return f"{rounded:,.{digits}f}"


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def _tiers(fn):
    return " / ".join(fn(t) for t in (1, 2, 3))


# --- The notes' §0 tables ---------------------------------------------------

def key_numbers(p):
    """§0 "Key numbers, per torus", regenerated."""
    res = {r: {t: evaluate(p, Design(radius_m=r, n_tori=1, tiers_lit=t, host_class="H")) for t in (0, 1, 2, 3)}
           for r, _ in SIZES}
    s_type = {r: {c: evaluate(p, Design(radius_m=r, n_tori=1, host_class=c))["materials"]["s_type"] / MT
                  for c in ("H", "L", "LL")} for r, _ in SIZES}
    rows = []

    def row(label, fn):
        rows.append([label] + [fn(r, res[r]) for r, _ in SIZES])

    row("rpm / rim speed", lambda r, x: f"{num(x[1]['geometry']['rpm'], 2)} / {num(x[1]['geometry']['rim_speed'])} m/s")
    row("Tube width / floor area", lambda r, x: f"{num(x[1]['geometry']['width'])} m / {num(x[1]['geometry']['floor_area'] / HA)} ha")
    row("Rock shield (after fill credit)", lambda r, x: f"{num(x[1]['mass']['shield'] / MT)} Mt")
    row("Steel (spokes + hull + frames, excl. hub and factory)", lambda r, x: f"{num(x[1]['mass']['steel'] / MT)} Mt")
    row("Fill (soil + regolith)", lambda r, x: f"{num(x[1]['mass']['fill'] / MT, 2)} Mt")
    row("Water (soil, O₂, lakes)", lambda r, x: f"{num(x[1]['mass']['water_needed'] / MT, 2)} Mt")
    row("N₂", lambda r, x: f"{num(x[1]['mass']['n2'] / KT, 2)} kt")
    row("**Total**", lambda r, x: f"**{num(x[1]['mass']['total'] / MT)} Mt**")
    row("Mass per m² of floor", lambda r, x: f"{num(x[1]['mass']['per_floor'] / 1e3)} t")
    row("S-type mined per torus, H / L / LL host", lambda r, x: " / ".join(f"{num(s_type[r][c], 2)}" for c in ("H", "L", "LL")) + " Mt")
    row("C-type per torus (sized by nitrogen)", lambda r, x: f"{num(x[1]['materials']['c_type'] / MT, 2)} Mt")
    row("Valley lighting, daily average (sulfur)", lambda r, x: f"{num(x[1]['power']['valley_sky'] / MW)} MW")
    row("Farm ring at ~0.4 r: crops per tier", lambda r, x: f"{num(x[1]['geometry']['crop_area_per_tier'] / HA, 2)} ha")
    row("People fed, 1 / 2 / 3 tiers lit", lambda r, x: _tiers(lambda t: num(x[t]['food']['people'], 2)))
    row("Floor per person, 1 / 2 / 3 tiers lit", lambda r, x: _tiers(lambda t: num(x[t]['food']['floor_per_person'])) + " m²")
    row("Farm lighting, per tier lit", lambda r, x: f"{num(x[1]['power']['farm_per_tier'] / MW)} MW")
    row("Solar needed: valley + other loads, + per tier lit",
        lambda r, x: f"{num(x[1]['power']['valley'] / MW)} + {num(x[1]['power']['farm_per_tier'] / MW)} MW")
    row("Plain rim solar, for comparison", lambda r, x: f"{num(x[1]['power']['plain_rim_pv'] / MW)} MW")
    row("Despun array at 1 AU (survival sizing): valley + per tier lit",
        lambda r, x: f"{num(x[1]['power']['array_1au_valley'] / KM2, 2)} + {num(x[1]['power']['array_1au_per_tier'] / KM2, 2)} km²")
    row("Despun array with three tiers lit", lambda r, x: f"{num(x[3]['power']['array_1au'] / KM2, 2)} km²")
    return table(["Key numbers, per torus"] + [name for _, name in SIZES], rows)


def stack_numbers(p, radius_m=900):
    """§0 stack table (pair and six-stack), regenerated."""
    stacks = (("Pair (A B)", 2), ("Six (A A B B C C)", 6))
    res = {n: {t: evaluate(p, Design(radius_m=radius_m, n_tori=n, tiers_lit=t, host_class="H")) for t in (1, 2, 3)}
           for _, n in stacks}
    wide = {n: evaluate(p, Design(radius_m=radius_m, n_tori=n, gap_m=40, host_class="H")) for _, n in stacks}
    rows = []

    def row(label, fn):
        rows.append([label] + [fn(n, res[n]) for _, n in stacks])

    row("Floor area", lambda n, x: f"{num(n * x[1]['geometry']['floor_area'] / HA)} ha")
    row("Mass (excl. shared hub and factory)", lambda n, x: f"{num(n * x[1]['mass']['total'] / MT)} Mt")
    row("Material mined (H-like host)", lambda n, x: f"{num(n * x[1]['materials']['mined'] / MT)} Mt")
    row("Stack length (10–40 m gaps)",
        lambda n, x: f"{num(x[1]['geometry']['stack_length'])}–{num(wide[n]['geometry']['stack_length'])} m")
    row("People fed, 1 / 2 / 3 tiers lit", lambda n, x: _tiers(lambda t: num(n * x[t]['food']['people'], 2)))
    row("Constant valley lighting load (sulfur)", lambda n, x: f"{num(n * x[1]['power']['valley_sky'] / MW)} MW")
    row("Farm lighting, per tier lit", lambda n, x: f"{num(n * x[1]['power']['farm_per_tier'] / MW)} MW")
    row("Despun array at 1 AU: valley + per tier lit",
        lambda n, x: f"{num(n * x[1]['power']['array_1au_valley'] / KM2, 2)} + {num(n * x[1]['power']['array_1au_per_tier'] / KM2, 2)} km²")
    row("Heat to reject with three tiers lit", lambda n, x: f"{num(x[3]['heat']['stack'] / MW)} MW")
    row(f"Radiator capacity of the two open ends (~{p.radiator_temp_k:g} K)",
        lambda n, x: f"{num(x[1]['heat']['capacity'] / GW, 2)} GW")
    row("Passive stability (20% margin): inertia ratio / max tori",
        lambda n, x: f"{num(x[1]['stability']['inertia_ratio'])} / {x[1]['stability']['max_tori']}")
    size = f"{radius_m / 1000:g} km" if radius_m >= 1000 else f"{radius_m:g} m"
    return table([f"Stack of {size} tori"] + [name for name, _ in stacks], rows)


def key_tables(p):
    return "\n\n".join([
        "# Key tables (regenerated from the model)",
        "Regenerates the tables of notes.md §0 from `habitat_model/assumptions.toml`. "
        "Mass and mining figures assume an H-like host, as in the notes' sizing tables; "
        "the S-type row also gives L and LL hosts.",
        key_numbers(p),
        stack_numbers(p, 900),
        stack_numbers(p, 1600),
    ]) + "\n"


# --- One design -------------------------------------------------------------

def summary(p, d, r):
    g, m, mat, f, pw, h, st, rep = (r[k] for k in
                                     ("geometry", "mass", "materials", "food", "power", "heat", "stability", "replication"))
    n = d.n_tori
    site = SITES[d.site]
    size = f"{d.radius_m / 1000:g} km" if d.radius_m >= 1000 else f"{d.radius_m:g} m"
    out = [f"# {n} × {size} tori, {d.tiers_lit} farm tier{'s' if d.tiers_lit != 1 else ''} lit, "
           f"{d.host_class} host, site {d.site}, C-type {d.c_partner}"]

    def section(title, rows):
        out.append(f"\n## {title}\n")
        out.append(table(["", "Per torus", f"Stack of {n}"], rows))

    section("Geometry", [
        ["Period / rpm / rim speed", f"{num(g['period'])} s / {num(g['rpm'], 2)} / {num(g['rim_speed'])} m/s", ""],
        ["Spin gravity", f"{num(d.g * 1.006, 2)} g at the floor, {num(g['hub_gravity'], 2)} g at the hub rim", ""],
        ["Tube width / hub radius", f"{num(g['width'])} m / {num(g['hub_radius'])} m", ""],
        ["Floor area", f"{num(g['floor_area'] / HA)} ha", f"{num(n * g['floor_area'] / HA)} ha"],
        ["Air volume", f"{num(g['volume'] / 1e6)} million m³", f"{num(n * g['volume'] / 1e6)} million m³"],
        ["Pitch / stack length", f"{num(g['pitch'])} m", f"{num(g['stack_length'])} m"],
        ["Farm ring: radius / crops per tier", f"{num(g['farm_radius'])} m / {num(g['crop_area_per_tier'] / HA)} ha", ""],
    ])
    section("Mass", [
        ["Rock shield (after fill credit)", f"{num(m['shield'] / MT)} Mt", f"{num(n * m['shield'] / MT)} Mt"],
        ["Fill (soil + regolith)", f"{num(m['fill'] / MT)} Mt", f"{num(n * m['fill'] / MT)} Mt"],
        ["Hull and frames", f"{num(m['hull_frames'] / MT)} Mt", f"{num(n * m['hull_frames'] / MT)} Mt"],
        ["Cable spokes", f"{num(m['spokes'] / MT)} Mt", f"{num(n * m['spokes'] / MT)} Mt"],
        ["Water needed / N₂ / O₂", f"{num(m['water_needed'] / MT)} Mt / {num(m['n2'] / KT)} kt / {num(m['o2'] / KT)} kt", ""],
        ["**Total** (excl. hub and factory)", f"**{num(m['total'] / MT)} Mt**", f"**{num(n * m['total'] / MT)} Mt**"],
        ["Per m² of floor", f"{num(m['per_floor'] / 1e3)} t", ""],
        ["Farm ring / array / radiator panels", f"{num(m['farm_ring'] / KT)} / {num(pw['array_site_mass'] / KT)} / {num(h['panel_mass'] / KT)} kt", ""],
        ["Spin-up propellant (water, if used)", f"{num(m['spinup_propellant'] / MT)} Mt", ""],
    ])
    trace = mat["trace"]
    section("Materials and mining", [
        ["Metal needed (with hub, dock, factory)", f"{num(mat['metal_needed'] / MT)} Mt", f"{num(n * mat['metal_needed'] / MT)} Mt"],
        [f"S-type ({d.host_class} host), sized by {mat['s_sized_by']}", f"{num(mat['s_type'] / MT)} Mt (~{num(mat['s_diameter'])} m)", f"{num(n * mat['s_type'] / MT)} Mt"],
        ["Spare tailings", f"{num(mat['spare_tailings'] / MT)} Mt", ""],
        [f"C-type, sized by {mat['c_sized_by']}", f"{num(mat['c_type'] / MT)} Mt (~{num(mat['c_diameter'])} m)", f"{num(n * mat['c_type'] / MT)} Mt"],
        ["Water / carbon in the C-type", f"{num(mat['c_water_contained'] / MT)} / {num(mat['c_carbon_contained'] / MT)} Mt", ""],
        ["**Mined**", f"**{num(mat['mined'] / MT)} Mt**", f"**{num(n * mat['mined'] / MT)} Mt**"],
        ["Copper contained (S + C)", f"{num(trace['Cu']['s_type'] / 1e6)} + {num(trace['Cu']['c_type'] / 1e6)} kt", ""],
    ])
    if site.kind == "S":
        tori = tori_supported(p, site, m, mat)
        out.append(f"\n{d.site} ({site.host_class}-like, ~{num(site.mass_mt)} Mt) supplies ~{num(tori, 2)} tori of this size by free metal; "
                   f"{d.c_partner} (~{num(SITES[d.c_partner].mass_mt)} Mt) ~{num(tori_supported(p, SITES[d.c_partner], m, mat), 2)} by nitrogen.")
    section("Power and light", [
        ["Valley sky + other loads", f"{num(pw['valley_sky'] / MW)} + {num(pw['other_loads'] / MW)} MW", f"{num(n * pw['valley'] / MW)} MW"],
        ["Farm lighting per tier lit", f"{num(pw['farm_per_tier'] / MW)} MW", f"{num(n * pw['farm_per_tier'] / MW)} MW"],
        ["**Total electricity**", f"**{num(pw['total'] / MW)} MW**", f"**{num(n * pw['total'] / MW)} MW**"],
        ["Despun array at 1 AU, constant sky", f"{num(pw['array_1au'] / KM2)} km²", f"{num(n * pw['array_1au'] / KM2)} km²"],
        [f"Despun array at {d.site} ({num(pw['site_aphelion_sunlight'], 2)}× sunlight at aphelion, "
         f"{'seasonal' if d.seasonal_sky else 'constant'} sky)", f"{num(pw['array_site'] / KM2)} km²", f"{num(n * pw['array_site'] / KM2)} km²"],
    ])
    section("Food", [
        ["Light on the crops per person", f"{num(f['mol_per_person'])} mol/day", ""],
        ["Crop area / electricity per person", f"{num(f['crop_area_per_person'])} m² / {num(f['power_per_person'] / 1e3)} kW", ""],
        ["People per tier lit", f"{num(f['people_per_tier'])}", f"{num(n * f['people_per_tier'])}"],
        ["**People fed**", f"**{num(f['people'])}**", f"**{num(n * f['people'])}**"],
        ["Floor per person", f"{num(f['floor_per_person'])} m²" if f["floor_per_person"] else "—", ""],
    ])
    section("Heat", [
        ["Heat to reject", f"{num(h['per_torus'] / MW)} MW", f"{num(h['stack'] / MW)} MW"],
        [f"Capacity of the two open ends (~{p.radiator_temp_k:g} K)", "", f"{num(h['capacity'] / GW)} GW"],
        ["Margin / break-even", "", f"{num(h['margin'], 2)}× / {num(h['break_even_tori'], 2)} tori"],
        ["Radiating surface (two-sided panels: half)", f"{num(h['radiating_surface'] / HA)} ha", f"{num(h['stack'] / h['flux'] / HA)} ha"],
    ])
    section("Stability (rigid stack)", [
        ["I_axis / I_transverse", "", f"{num(st['inertia_ratio'])} ({'stable' if st['stable'] else 'NOT stable'} with a {p.stability_margin:.0%} margin)"],
        ["Max tori at this gap: no margin / 10% / 20%", "", f"{st['max_tori_no_margin']} / {st['max_tori_10pct']} / {st['max_tori']}"],
    ])
    dv = rep["delta_v_km_s"]
    section("Processing and replication", [
        ["Crushing S-type / baking C-type", f"{num(rep['crushing'] / PJ)} / {num(rep['baking'] / PJ)} PJ", ""],
        [f"Shipping {num(rep['shipped'] / MT)} Mt of volatiles ({d.c_partner} → {d.site}, "
         + (f"{dv} km/s)" if dv is not None else "no Δv known: pass --dv)"), f"{num(rep['shipping'] / PJ)} PJ", ""],
        ["Energy", f"{num(rep['energy_per_torus'] / PJ)} PJ", f"{num(rep['energy_stack'] / PJ)} PJ"],
        [f"Generation time at {d.factory_power_gw:g} GW (energy only)", "", f"{num(rep['generation_time_yr'], 2)} years"],
    ])
    return "\n".join(out) + "\n"


# --- Validation and sensitivity ---------------------------------------------

def validation(outcomes):
    bad = [o for o in outcomes if not o.ok]
    unexplained = [o for o in bad if not o.check.known]
    out = ["# Validation against the notes", "",
           f"{len(outcomes)} figures from notes.md checked; {len(outcomes) - len(bad)} within tolerance (5% unless noted), "
           f"{len(bad) - len(unexplained)} known mismatches, {len(unexplained)} unexplained.", ""]
    out.append("## Mismatches\n")
    known = [o for o in outcomes if o.check.known]
    out.append(table(["§", "Figure", "Notes", "Model", "Diff", "Why"],
                     [[o.check.section, o.check.label, f"{num(o.check.reference)} {o.check.unit}",
                       f"{num(o.model)} {o.check.unit}", f"{o.diff:+.1%}",
                       o.check.known or "**unexplained**"] for o in bad + [o for o in known if o.ok]]))
    out.append("\n## All checks\n")
    out.append(table(["§", "Figure", "Notes", "Model", "Diff", ""],
                     [[o.check.section, o.check.label, f"{num(o.check.reference)} {o.check.unit}",
                       f"{num(o.model)} {o.check.unit}", f"{o.diff:+.1%}", "✓" if o.ok else "✗"] for o in outcomes]))
    return "\n".join(out) + "\n"


def tornado(base, rows, assumptions, design, top=None):
    names = list(METRICS)
    header = ["Rank", "Assumption", "Status", "Range"] + [f"{METRICS[m][0]} ({METRICS[m][1]})" if METRICS[m][1] else METRICS[m][0]
                                                       for m in names]
    base_row = ["", "**Baseline**", "", ""] + [f"**{num(base[m])}**" for m in names]

    def cell(lo, hi):
        if abs(lo) < 0.005 and abs(hi) < 0.005:
            return ""
        return f"{lo:+.0%} / {hi:+.0%}"

    body = [[i + 1, f"`{r.name}`", r.status,
             f"{num(r.low)}–{num(r.high)} {assumptions[r.name].unit}"] + [cell(*r.effects[m]) for m in names]
            for i, r in enumerate(rows[:top] if top else rows)]
    size = f"{design.radius_m / 1000:g} km" if design.radius_m >= 1000 else f"{design.radius_m:g} m"
    intro = (f"One-at-a-time sweep for {design.n_tori} × {size}, {design.tiers_lit} tier(s) lit, "
             f"{design.host_class} host at {design.site}. Each cell: change of the output with the input at its "
             "low / high end. Ranked by the largest swing on any output.")
    return "\n".join(["# Sensitivity (tornado)", "", intro, "", table(header, [base_row] + body)]) + "\n"


def monte_carlo(stats, n):
    rows = [[METRICS[m][0], METRICS[m][1], num(s["p5"]), num(s["p50"]), num(s["p95"])] for m, s in stats.items()]
    return "\n".join([f"# Monte Carlo ({n} samples, triangular over every range)", "",
                      table(["Output", "Unit", "5th percentile", "Median", "95th percentile"], rows)]) + "\n"


def assumptions_table(assumptions):
    rows = [[f"`{a.name}`", num(a.value, 4), a.unit, f"{num(a.low, 4)}–{num(a.high, 4)}" if a.varies else "fixed",
             a.status, a.source] for a in assumptions.values()]
    return "\n".join(["# Assumptions", "", table(["Name", "Value", "Unit", "Range", "Status", "Source"], rows)]) + "\n"


# --- JSON for the 3D model's stats panel ------------------------------------

def stats_json(p, d, r):
    """Headline numbers per torus and per stack, in display units."""
    g, m, mat, f, pw, h = (r[k] for k in ("geometry", "mass", "materials", "food", "power", "heat"))
    n = d.n_tori
    return {
        "design": {"radius_m": d.radius_m, "period_s": g["period"], "n_tori": n, "tiers_lit": d.tiers_lit,
                   "host_class": d.host_class, "site": d.site, "c_partner": d.c_partner, "gap_m": d.gap_m, "g": d.g},
        "per_torus": {
            "rpm": g["rpm"], "rim_speed_m_s": g["rim_speed"], "width_m": g["width"], "floor_ha": g["floor_area"] / HA,
            "mass_mt": m["total"] / MT, "mass_per_floor_t_m2": m["per_floor"] / 1e3, "shield_mt": m["shield"] / MT,
            "steel_mt": m["steel"] / MT, "n2_kt": m["n2"] / KT, "water_mt": m["water_needed"] / MT,
            "s_type_mt": mat["s_type"] / MT, "c_type_mt": mat["c_type"] / MT,
            "people": f["people"], "people_per_tier": f["people_per_tier"],
            "power_mw": pw["total"] / MW, "valley_mw": pw["valley"] / MW, "farm_per_tier_mw": pw["farm_per_tier"] / MW,
            "array_1au_km2": pw["array_1au"] / KM2, "array_site_km2": pw["array_site"] / KM2,
            "heat_mw": h["per_torus"] / MW,
        },
        "stack": {
            "floor_ha": n * g["floor_area"] / HA, "mass_mt": n * m["total"] / MT, "mined_mt": n * mat["mined"] / MT,
            "length_m": g["stack_length"], "people": n * f["people"], "power_mw": n * pw["total"] / MW,
            "array_site_km2": n * pw["array_site"] / KM2, "heat_mw": h["stack"] / MW,
            "heat_capacity_mw": h["capacity"] / MW, "heat_margin": h["margin"],
            "inertia_ratio": r["stability"]["inertia_ratio"], "max_tori": r["stability"]["max_tori"],
            "generation_time_yr": r["replication"]["generation_time_yr"],
        },
    }
