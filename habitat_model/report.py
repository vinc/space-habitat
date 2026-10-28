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


def pj(x):
    """Energy in PJ, or 'unknown' when a contribution is unknown."""
    return "unknown" if x is None else f"{num(x / PJ)} PJ"


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
    row("Main section length (10–40 m gaps between tori)",
        lambda n, x: f"{num(x[1]['geometry']['main_length'])}–{num(wide[n]['geometry']['main_length'])} m")
    row("Whole stack with its farm section (10 m gaps)", lambda n, x: f"{num(x[1]['geometry']['stack_length'])} m")
    row("People fed, 1 / 2 / 3 tiers lit", lambda n, x: _tiers(lambda t: num(n * x[t]['food']['people'], 2)))
    row("Constant valley lighting load (sulfur)", lambda n, x: f"{num(n * x[1]['power']['valley_sky'] / MW)} MW")
    row("Farm lighting, per tier lit", lambda n, x: f"{num(n * x[1]['power']['farm_per_tier'] / MW)} MW")
    row("Despun array at 1 AU: valley + per tier lit",
        lambda n, x: f"{num(n * x[1]['power']['array_1au_valley'] / KM2, 2)} + {num(n * x[1]['power']['array_1au_per_tier'] / KM2, 2)} km²")
    row("Heat with three tiers lit: main section (valleys) + farm section",
        lambda n, x: f"{num(x[3]['heat']['main_stack'] / MW)} + {num(x[3]['heat']['farm_stack'] / MW)} MW")
    row(f"Main section: ideal limit of the two open ends (~{p.radiator_temp_k:g} K)",
        lambda n, x: f"{num(x[1]['heat']['capacity'] / GW, 2)} GW")
    row("Passive stability of the whole stack (20% margin): inertia ratio / max tori",
        lambda n, x: f"{num(x[1]['stability']['whole_inertia_ratio'])} / {x[1]['stability']['whole_max_tori']}")
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

def summary(p, d, r, cavity_result=None):
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
        ["Rock jacket / envelope radius (jacket + crawl space)", f"{num(g['jacket'], 2)} m / {num(g['envelope_radius'])} m", ""],
        ["Pitch / clear gap / stack length", f"{num(g['pitch'])} m / {num(g['gap'])} m", f"{num(g['stack_length'])} m"],
        ["Farm section: farm ring radius / crops per tier", f"{num(g['farm_radius'])} m / {num(g['crop_area_per_tier'] / HA)} ha", ""],
        ["Farm section: ring pitch / section length / gap to the main section",
         f"{num(g['farm_pitch'])} m", f"{num(g['farm_length'])} m / {num(g['farm_section_gap'])} m"],
        ["Main section length / whole stack", "", f"{num(g['main_length'])} m / {num(g['stack_length'])} m"],
    ])
    section("Mass", [
        ["Rock shield (after fill credit)", f"{num(m['shield'] / MT)} Mt", f"{num(n * m['shield'] / MT)} Mt"],
        ["Fill (soil + regolith)", f"{num(m['fill'] / MT)} Mt", f"{num(n * m['fill'] / MT)} Mt"],
        ["Hull and frames", f"{num(m['hull_frames'] / MT)} Mt", f"{num(n * m['hull_frames'] / MT)} Mt"],
        ["Cable spokes", f"{num(m['spokes'] / MT)} Mt", f"{num(n * m['spokes'] / MT)} Mt"],
        ["Water needed / N₂ / O₂", f"{num(m['water_needed'] / MT)} Mt / {num(m['n2'] / KT)} kt / {num(m['o2'] / KT)} kt", ""],
        ["**Total** (excl. hub and factory)", f"**{num(m['total'] / MT)} Mt**", f"**{num(n * m['total'] / MT)} Mt**"],
        ["Per m² of floor", f"{num(m['per_floor'] / 1e3)} t", ""],
        ["Farm ring: shell and growing systems / its spokes / its N₂ (at the farm's pressure)",
         f"{num(m['farm_ring'] / KT)} / {num(m['farm_spokes'] / KT, 2)} / {num(m['farm_n2'] / KT, 2)} kt", ""],
        ["Despun array / radiator panels (ideal)", f"{num(pw['array_site_mass'] / KT)} / {num(h['panel_mass'] / KT)} kt", ""],
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
    budget = mat["trace_budget"]
    short = [e for e, b in budget.items() if b["status"] not in ("ok", "no demand")]
    out.append("\nTrace elements (demands mostly guesses from the notes; `--trace` for the table): "
               + ("all budgeted elements covered at their high demand" if not any(budget[e]["status"] != "unbudgeted" for e in short)
                  else "short: " + ", ".join(e for e in short if budget[e]["status"] != "unbudgeted"))
               + "; unbudgeted: " + (", ".join(e for e in short if budget[e]["status"] == "unbudgeted") or "none") + ".")
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
        ["Main section (valleys and other loads)", f"{num(h['main_per_torus'] / MW)} MW", f"{num(h['main_stack'] / MW)} MW"],
        ["Farm section (tiers lit)", f"{num(h['farm_per_ring'] / MW)} MW", f"{num(h['farm_stack'] / MW)} MW"],
        [f"Main section: ideal limit of its two open ends, black bodies at ~{p.radiator_temp_k:g} K", "", f"{num(h['capacity'] / GW)} GW"],
        ["Main section: ideal margin / break-even (upper bounds)", "", f"{num(h['margin'], 2)}× / {num(h['break_even_tori'], 2)} tori"],
        ["Ideal radiating surface, black body, lower bound (two-sided panels: half)", f"{num(h['radiating_surface'] / HA)} ha", f"{num(h['stack'] / h['flux'] / HA)} ha"],
    ])
    if cavity_result:
        main, farm, a = cavity_result
        out.append(f"\nPreliminary radiative exchange (ray tracing, emissivity {p.radiator_emissivity:g}), each section on its own:")
        for name, res in (("main section (drum, ends only)", main),
                          (f"farm section (open, radiators to {num(g['farm_radiator_outer'])} m)", farm)):
            extra = f" ({res['max_vs_ideal']:.0%} of its ideal limit)" if res["max_vs_ideal"] else ""
            out.append(f"- {name}: rejects at most {num(res['max_output'] / GW)} GW{extra}, a margin of "
                       f"{num(res['margin'], 2)}×; "
                       + (f"needs {num(res['needed']['panel_area'] / HA)} ha of panels ({res['needed']['coverage']:.0%} of "
                          f"its radiator annuli), against {num(res['ideal_panel_area'] / HA)} ha ideally."
                          if res["needed"] else "**it can't reject its load.**"))
        out.append(f"- the whole stack, traced together: margins of {num(a['main_margin'], 2)}× (main) and "
                   f"{num(a['farm_margin'], 2)}× (farm) at {_coverage(a)} panel coverage, "
                   + ("so both sections can be cooled." if a["feasible"] else "**so the stack can't be cooled.**"))
    section("Stability (rigid stack)", [
        ["I_axis / I_transverse, tori alone / whole stack", "",
         f"{num(st['inertia_ratio'])} / {num(st['whole_inertia_ratio'])} "
         f"({'stable' if st['whole_stable'] else 'NOT stable'} with a {p.stability_margin:.0%} margin)"],
        ["Max tori at this gap: tori alone, no margin / 10% / 20%; whole stack, 20%", "",
         f"{st['max_tori_no_margin']} / {st['max_tori_10pct']} / {st['max_tori']}; {st['whole_max_tori']}"],
    ])
    dv = rep["delta_v_km_s"]
    section("Processing and replication", [
        ["Crushing S-type / baking C-type", f"{num(rep['crushing'] / PJ)} / {num(rep['baking'] / PJ)} PJ", ""],
        [f"Shipping {num(rep['shipped'] / MT)} Mt of volatiles ({d.c_partner} → {d.site}, "
         + (f"{dv} km/s)" if dv is not None else "no Δv known: pass --dv)"), pj(rep['shipping']), ""],
        ["Energy, processing + shipping", pj(rep['energy_per_torus']), pj(rep['energy_stack'])],
        [f"Generation time at {d.factory_power_gw:g} GW (energy only)", "",
         f"{num(rep['generation_time_yr'], 2)} years" if rep["generation_time_yr"] is not None
         else f"unknown (≥ {num(rep['generation_time_lower_bound_yr'], 2)} years for processing alone)"],
    ])
    return "\n".join(out) + "\n"


# --- Validation and sensitivity ---------------------------------------------

def validation(outcomes):
    bad = [o for o in outcomes if not o.ok]
    unexplained = [o for o in bad if not o.check.known]
    within5 = sum(abs(o.diff) <= 0.05 for o in outcomes)
    relaxed = sum(o.check.tol > 0.05 for o in outcomes)
    out = ["# Validation against the notes", "",
           f"{len(outcomes)} figures from notes.md checked: **{within5} within 5%**; {len(outcomes) - len(bad)} within "
           f"their configured tolerance (5%, or 10–15% for {relaxed} checks of counts and energies quoted as ranges); "
           f"{len(bad) - len(unexplained)} known mismatches, {len(unexplained)} unexplained.", "",
           "This checks that the model reproduces the notes' own figures from the same assumptions; "
           "it does not validate the physical design.", ""]
    out.append("## Mismatches\n")
    known = [o for o in outcomes if o.check.known]
    out.append(table(["§", "Figure", "Notes", "Model", "Diff", "Why"],
                     [[o.check.section, o.check.label, f"{num(o.check.reference)} {o.check.unit}",
                       f"{num(o.model)} {o.check.unit}", f"{o.diff:+.1%}",
                       o.check.known or "**unexplained**"] for o in bad + [o for o in known if o.ok]]))
    out.append("\n## All checks\n")
    out.append(table(["§", "Figure", "Notes", "Model", "Diff", ""],
                     [[o.check.section, o.check.label, f"{num(o.check.reference)} {o.check.unit}",
                       f"{num(o.model)} {o.check.unit}", f"{o.diff:+.1%}",
                       ("✓" if abs(o.diff) <= 0.05 else f"✓ (tolerance {o.check.tol:.0%})") if o.ok else "✗"]
                      for o in outcomes]))
    return "\n".join(out) + "\n"


def tornado(base, rows, assumptions, design, top=None):
    names = [m for m in METRICS if base[m] is not None]
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
             "low / high end. Ranked by the largest swing on any output."
             + ("" if len(names) == len(METRICS) else
                " Left out as unknown for this design: " + ", ".join(METRICS[m][0] for m in METRICS if m not in names) + "."))
    return "\n".join(["# Sensitivity (tornado)", "", intro, "", table(header, [base_row] + body)]) + "\n"


def monte_carlo(stats, n):
    rows = [[METRICS[m][0], METRICS[m][1], num(s["p5"]), num(s["p50"]), num(s["p95"])] for m, s in stats.items()]
    return "\n".join([f"# Monte Carlo ({n} samples)", "",
                      "Each input drawn independently from a triangular distribution (low, value, high). The spread "
                      "shows what the chosen ranges imply; it is not a physical confidence interval.", "",
                      table(["Output", "Unit", "5th percentile", "Median", "95th percentile"], rows)]) + "\n"


def combined_ranking(ranking):
    rows = [[i + 1, f"`{name}`", r["status"], METRICS[r["metric"]][0], f"{r['low']:+.0%} / {r['high']:+.0%}", r["design"]]
            for i, (name, r) in enumerate(ranking)]
    return "\n".join(["# Combined ranking", "",
                      "Each input's largest swing on any output, over representative designs (sizes, host classes "
                      "and sites; `sensitivity.REPRESENTATIVE`), with the output and design where it occurs.", "",
                      table(["Rank", "Assumption", "Status", "Largest effect on", "Low / high", "Design"], rows)]) + "\n"


def trace_table(budget, design):
    def t(x):
        return "—" if x is None else num(x / 1e3, 2)
    rows = [[e, t(b["contained"]), t(b["recoverable"]),
             "—" if b["demand"] is None else f"{num(b['demand'][0] / 1e3, 2)}–{num(b['demand'][1] / 1e3, 2)}",
             t(b["balance"]), b["status"], b["note"]] for e, b in budget.items()]
    size = f"{design.radius_m / 1000:g} km" if design.radius_m >= 1000 else f"{design.radius_m:g} m"
    return "\n".join([f"# Trace-element budget, per {size} torus ({design.host_class} host)", "",
                      "Contained in the torus's S-type and C-type rock, recoverable at the assumed recovery, against "
                      "the demand (tonnes). Most demands and recoveries are guesses taken from the notes; S-type "
                      "abundances are H values for the majors, so nickel and cobalt are overstated for L and LL hosts.", "",
                      table(["Element", "Contained (t)", "Recoverable (t)", "Demand (t)", "Surplus at high demand (t)",
                             "Status", "Basis"], rows)]) + "\n"


STACK_LIMIT_CAP = 40   # cavity.assembled_limit stops searching here


def _coverage(a):
    return f"{a['coverage'][0]:.0%} / {a['coverage'][1]:.0%}"


def thermal_table(rows):
    def needed(c):
        return num(c["needed"]["panel_area"] / HA) if c["needed"] else "**not enough**"

    def limit(n):
        return f"≥ {n}" if n >= STACK_LIMIT_CAP else str(n)

    def margin(x):
        return num(x, 2) if x >= 1 else f"**{num(x, 2)}**"
    body = [[r["label"],
             num(r["main_load"] / MW), num(r["ideal"] / r["main_load"], 2), num(r["main_ends"]["margin"], 2),
             num(r["main_gaps"]["margin"], 2), needed(r["main_ends"]),
             num(r["farm_load"] / MW), num(r["farm"]["margin"], 2), needed(r["farm"]),
             f"{margin(r['assembled']['main_margin'])} / {margin(r['assembled']['farm_margin'])}",
             _coverage(r["assembled"]), limit(r["limit"])] for r in rows]
    return "\n".join([
        "# Heat rejection, per section and assembled: ideal limit and preliminary radiative exchange", "",
        "The **main section** (the tori) rejects the valleys' heat from radiators on the tori's spokes, in the drum "
        "between hub and tori; its ideal limit treats both end openings as black bodies at the radiator temperature. "
        "The **farm section** (one farm ring per torus, on its own spokes) rejects the farm tiers' heat from "
        "radiators on the farm spokes, in an open stack with nothing around it. Each is first ray traced on its own "
        "(`habitat_model/cavity.py`: finite two-sided panels, emissivity and temperature from the assumptions, "
        "insulated hub and rings). Then the **whole stack** is traced as one scene: the drum, the gap and the farm "
        "section with its radiators, with the tori's outer side facing the farm section as an insulated face. The "
        "farm radiators shade the drum's farm end and the main radiators the farm section's near end, so the two "
        "panel coverages are swept together and the assembled margins are those of the best pair (the one with "
        "the best worse-of-the-two margin). Only the assembled check says whether a stack can be cooled; the "
        "**limit** is the most tori (with their farm rings) the assembled stack can cool, the drum through its "
        "ends only. Panel areas are one face of two-sided panels.", "",
        table(["Stack, tiers lit", "Main heat (MW)", "Main, ideal margin", "Main alone, ends only",
               "Main alone, ends + gaps", "Main alone, panels needed (ha)",
               "Farm heat (MW)", "Farm alone", "Farm alone, panels needed (ha)",
               "Assembled margins main / farm", "Assembled coverage main / farm", "Assembled limit (tori)"],
              body)]) + "\n"


def farm_sweep_table(result, assumptions):
    name, rows = result
    a = assumptions[name]
    body = [[r["label"], f"{num(r['value'], 2)}{' (default)' if r['default'] else ''}",
             num(r["farm"]["margin"], 2),
             (num(r["assembled"]["farm_margin"], 2) if r["assembled"]["feasible"]
              else f"**{num(r['assembled']['farm_margin'], 2)}**"),
             (num(r["assembled"]["main_margin"], 2) if r["assembled"]["feasible"]
              else f"**{num(r['assembled']['main_margin'], 2)}**"),
             _coverage(r["assembled"]), "yes" if r["assembled"]["feasible"] else "**no**"] for r in rows]
    return "\n".join([
        f"# Farm radiators' reach: `{name}` across its range", "",
        f"The farm radiators' outer radius ({a.status}, {num(a.low, 2)}–{num(a.high, 2)} of the floor radius) sets "
        "the farm section's panel area and how much of the drum's farm end it shades. The one-at-a-time sweep "
        "and the Monte Carlo can't see it (they use `evaluate`, which ray traces nothing, and their heat metric "
        "is the main drum's ideal margin, which leaves the farm section out), so it is swept here with the "
        "farm section alone and the assembled stack.", "",
        table(["Stack, tiers lit", "Reach (× floor radius)", "Farm alone", "Assembled farm margin",
               "Assembled main margin", "Assembled coverage main / farm", "Cools both?"], body)]) + "\n"


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
            "heat_main_ideal_limit_mw": h["capacity"] / MW, "heat_main_ideal_margin": h["margin"],
            # Stability of the whole stack (tori and farm section); the tori alone under main_*.
            "inertia_ratio": r["stability"]["whole_inertia_ratio"], "max_tori": r["stability"]["whole_max_tori"],
            "inertia_stable": r["stability"]["whole_stable"],
            "main_inertia_ratio": r["stability"]["inertia_ratio"], "main_max_tori": r["stability"]["max_tori"],
            "energy_pj": None if r["replication"]["energy_stack"] is None else r["replication"]["energy_stack"] / PJ,
            "processing_energy_pj": n * r["replication"]["processing"] / PJ,
            "generation_time_yr": r["replication"]["generation_time_yr"],          # null when the delta-v is unknown
            "generation_time_lower_bound_yr": r["replication"]["generation_time_lower_bound_yr"],
        },
    }
