"""Local, read-only HTTP interface to the repository's system model."""
import argparse
from dataclasses import asdict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import math
from pathlib import Path
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from habitat_model.assumptions import load, params
from habitat_model.design import Design, SITES
from habitat_model.model import evaluate

# Deliberately bounded UI domain, not a claim of physical validation.
DESIGN_RANGES = {
    'radius_m': (200, 2500), 'n_tori': (1, 32), 'tiers_lit': (0, 3),
    'gap_m': (0, 100), 'g': (0.1, 1.2), 'factory_power_gw': (0.1, 20),
}
OVERRIDE_RANGES = {
    'width_ratio': (8, 32), 'shield_areal_t_m2': (5, 20),
    'fill_depth_m': (0, 5), 'pressure_kpa': (40, 101.3),
    'farm_radiator_outer_frac': (0.45, 0.9),
}


def bounded(value, bounds, name, integer=False):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    if not bounds[0] <= value <= bounds[1] or (integer and int(value) != value):
        raise ValueError(f'{name} must be {"an integer " if integer else ""}in {bounds}')
    return value


def calculate(payload):
    if not isinstance(payload, dict) or set(payload) - {'design', 'overrides'}:
        raise ValueError('expected design and overrides objects')
    design = payload.get('design', {})
    overrides = payload.get('overrides', {})
    if not isinstance(design, dict) or not isinstance(overrides, dict):
        raise ValueError('design and overrides must be objects')
    allowed = set(DESIGN_RANGES) | {'host_class', 'site', 'c_partner', 'seasonal_sky', 'water_spinup', 'delta_v_km_s'}
    if set(design) - allowed or set(overrides) - set(OVERRIDE_RANGES):
        raise ValueError('unsupported parameter')
    for name, bounds in DESIGN_RANGES.items():
        if name in design:
            bounded(design[name], bounds, name, name in ('n_tori', 'tiers_lit'))
    for name in ('seasonal_sky', 'water_spinup'):
        if name in design and not isinstance(design[name], bool):
            raise ValueError(f'{name} must be boolean')
    if design.get('delta_v_km_s') is not None:
        bounded(design['delta_v_km_s'], (0, 30), 'delta_v_km_s')
    for name, value in overrides.items():
        bounded(value, OVERRIDE_RANGES[name], name)
    d = Design(**design)
    assumptions = load()
    p = params(assumptions, **overrides)
    result = evaluate(p, d)
    return {'design': asdict(d), 'overrides': overrides, 'results': result,
            'assumptions': {k: asdict(v) | {'value': getattr(p, k)} for k, v in assumptions.items()}}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def reply(self, status, data):
        body = json.dumps(data, allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlsplit(self.path).path == '/api/config':
            self.reply(200, {'design': asdict(Design(n_tori=6, tiers_lit=2, site='Eros', host_class='LL')),
                             'sites': list(SITES), 'partners': [k for k, v in SITES.items() if v.kind == 'C'],
                             'ranges': DESIGN_RANGES, 'override_ranges': OVERRIDE_RANGES,
                             'assumptions': {k: asdict(v) for k, v in load().items()}})
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != '/api/evaluate':
            self.reply(404, {'error': 'unknown endpoint'})
            return
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 16384:
                raise ValueError('request must be between 1 and 16384 bytes')
            data = calculate(json.loads(self.rfile.read(size)))
            self.reply(200, data)
        except (ValueError, TypeError, KeyError, OverflowError) as exc:
            self.reply(400, {'error': str(exc)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--strictPort', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    print(f'Habitat explorer: http://{args.host}:{args.port}', flush=True)
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == '__main__':
    main()
