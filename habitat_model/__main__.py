"""Command line: python -m habitat_model --size 900 --stack six --tiers 2 --host L --site Eros"""

import argparse
import json
import sys
from pathlib import Path

from . import cavity, report, sensitivity, validation
from .assumptions import DEFAULT_PATH, load, params
from .design import SITES, Design
from .geometry import radius_for_period
from .model import evaluate


def parse_size(text):
    """Floor radius: '900', '900m', '1.6km' or '2500'."""
    t = text.strip().lower()
    if t.endswith("km"):
        return float(t[:-2]) * 1000
    return float(t.removesuffix("m"))


def parse_stack(text):
    return {"single": 1, "pair": 2, "six": 6}.get(text.lower()) or int(text)


def parse_override(text):
    name, _, value = text.partition("=")
    if not value:
        raise argparse.ArgumentTypeError(f"expected NAME=VALUE, got {text!r}")
    return name.strip(), float(value)


def build_parser():
    ap = argparse.ArgumentParser(prog="python -m habitat_model", description=__doc__)
    size = ap.add_mutually_exclusive_group()
    size.add_argument("--size", type=parse_size, default=900.0, help="floor radius: 400, 900, 1.6km, 2.5km… (default 900)")
    size.add_argument("--period", type=float, help="rotation period in s; radius = (T/2)^2")
    ap.add_argument("--stack", type=parse_stack, default=2, help="single, pair, six or a number of tori (default pair)")
    ap.add_argument("--tiers", type=int, default=1, choices=range(4), help="farm tiers lit (default 1)")
    ap.add_argument("--host", default="L", choices=("H", "L", "LL"), help="S-type host class (default L)")
    ap.add_argument("--site", default="1 AU", choices=list(SITES), help="orbit for the solar sizing (default 1 AU)")
    ap.add_argument("--partner", default="Ryugu", choices=[n for n, b in SITES.items() if b.kind == "C"])
    ap.add_argument("--gap", type=float, default=10.0, help="gap between tori in m (default 10)")
    ap.add_argument("--g", type=float, default=1.0, help="spin gravity, fraction of 1 g (default 1)")
    ap.add_argument("--water-spinup", action="store_true", help="spin up with water thrusters")
    ap.add_argument("--constant-sky", action="store_true", help="size the array for a constant sky, not a seasonal one")
    ap.add_argument("--factory-power", type=float, default=1.0, help="factory power in GW (default 1)")
    ap.add_argument("--dv", type=float, help="C-type -> site delta-v in km/s (default: the notes' value if known)")
    ap.add_argument("--assumptions", type=Path, default=DEFAULT_PATH, help="assumptions file")
    ap.add_argument("--set", type=parse_override, action="append", default=[], metavar="NAME=VALUE",
                    help="override one assumption (repeatable)")

    out = ap.add_argument_group("outputs (default: a summary of the design)")
    out.add_argument("--key-tables", action="store_true", help="regenerate the notes' §0 tables")
    out.add_argument("--validate", action="store_true", help="compare with the notes' figures")
    out.add_argument("--sensitivity", action="store_true", help="one-at-a-time sweep, ranked")
    out.add_argument("--ranking", action="store_true", help="combined ranking over representative designs")
    out.add_argument("--monte-carlo", type=int, metavar="N", help="Monte Carlo with N samples")
    out.add_argument("--thermal", action="store_true", help="ideal limit vs preliminary radiative exchange, by stack")
    out.add_argument("--trace", action="store_true", help="trace-element budget of the design")
    out.add_argument("--assumptions-table", action="store_true", help="list the assumptions")
    out.add_argument("--json", type=Path, metavar="FILE", help="write the stats panel JSON ('-' for stdout)")
    out.add_argument("--write-reports", type=Path, metavar="DIR", help="write every report into DIR")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    assumptions = load(args.assumptions)
    overrides = dict(args.set)
    p = params(assumptions, **overrides)
    d = Design(
        radius_m=radius_for_period(args.period) if args.period else args.size,
        n_tori=args.stack, tiers_lit=args.tiers, host_class=args.host, site=args.site, c_partner=args.partner,
        gap_m=args.gap, g=args.g, water_spinup=args.water_spinup, seasonal_sky=not args.constant_sky,
        factory_power_gw=args.factory_power, delta_v_km_s=args.dv,
    )
    results = evaluate(p, d)

    if args.write_reports:
        write_reports(args.write_reports, assumptions, overrides, p, d, results)
        return 0

    chosen = False
    if args.key_tables:
        print(report.key_tables(p)); chosen = True
    if args.validate:
        print(report.validation(validation.run(p))); chosen = True
    if args.sensitivity:
        base, rows = sensitivity.tornado(assumptions, d, overrides)
        print(report.tornado(base, rows, assumptions, d)); chosen = True
    if args.ranking:
        print(report.combined_ranking(sensitivity.combined_ranking(assumptions, overrides=overrides))); chosen = True
    if args.thermal:
        print(report.thermal_table(cavity.study(p)) + "\n"
              + report.farm_sweep_table(cavity.farm_sweep(assumptions, overrides), assumptions)); chosen = True
    if args.trace:
        print(report.trace_table(results["materials"]["trace_budget"], d)); chosen = True
    if args.monte_carlo:
        print(report.monte_carlo(sensitivity.monte_carlo(assumptions, d, args.monte_carlo, overrides=overrides),
                                 args.monte_carlo)); chosen = True
    if args.assumptions_table:
        print(report.assumptions_table(assumptions)); chosen = True
    if args.json:
        text = json.dumps(report.stats_json(p, d, results), indent=2)
        if str(args.json) == "-":
            print(text)
        else:
            args.json.write_text(text + "\n")
        chosen = True
    if not chosen:
        print(report.summary(p, d, results, design_cavity(p, d, results)))
    return 0


def design_cavity(p, d, results):
    g, h = results["geometry"], results["heat"]
    return (cavity.check_main(p, d, g, h, side_gaps=False), cavity.check_farm(p, d, g, h),
            cavity.check_assembled(p, d, g, h))


def write_reports(folder, assumptions, overrides, p, d, results):
    folder.mkdir(parents=True, exist_ok=True)
    base, rows = sensitivity.tornado(assumptions, d, overrides)
    n_mc = 2000
    farm_sweep = report.farm_sweep_table(cavity.farm_sweep(assumptions, overrides), assumptions)
    files = {
        "key_tables.md": report.key_tables(p),
        "design.md": report.summary(p, d, results, design_cavity(p, d, results)),
        "thermal.md": report.thermal_table(cavity.study(p)) + "\n" + farm_sweep,
        "trace.md": report.trace_table(results["materials"]["trace_budget"], d),
        "validation.md": report.validation(validation.run(p)),
        "sensitivity.md": report.tornado(base, rows, assumptions, d) + "\n"
                          + report.combined_ranking(sensitivity.combined_ranking(assumptions, overrides=overrides)) + "\n"
                          + report.monte_carlo(sensitivity.monte_carlo(assumptions, d, n_mc, overrides=overrides), n_mc)
                          + "\n" + farm_sweep,
        "assumptions.md": report.assumptions_table(assumptions),
        "stats.json": json.dumps(report.stats_json(p, d, results), indent=2) + "\n",
    }
    for name, text in files.items():
        (folder / name).write_text(text)
        print(f"wrote {folder / name}")


if __name__ == "__main__":
    sys.exit(main())
