"""The viewer must preserve model results and reject malformed public inputs."""
import importlib.util
import math
from pathlib import Path
import unittest

from habitat_model.design import Design
from habitat_model.model import evaluate_default

spec = importlib.util.spec_from_file_location('explorer_server', Path(__file__).parents[1] / 'explorer/server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class ExplorerTests(unittest.TestCase):
    def test_complete_default_design_roundtrip(self):
        from dataclasses import asdict
        response = server.calculate({'design': asdict(Design())})
        self.assertEqual(response['results'], evaluate_default(Design()))

    def test_passes_design_and_assumptions_to_model(self):
        payload = {'design': {'radius_m': 1600, 'n_tori': 6, 'tiers_lit': 3, 'site': 'Eros', 'host_class': 'LL'},
                   'overrides': {'width_ratio': 20, 'shield_areal_t_m2': 10}}
        response = server.calculate(payload)
        expected = evaluate_default(Design(**payload['design']), **payload['overrides'])
        self.assertEqual(response['results'], expected)
        self.assertEqual(response['assumptions']['width_ratio']['value'], 20)
        self.assertIn('source', response['assumptions']['width_ratio'])

    def test_unknown_route_and_zero_tiers_remain_unknown(self):
        r = server.calculate({'design': {'site': '1 AU', 'tiers_lit': 0}})['results']
        self.assertIsNone(r['replication']['shipping'])
        self.assertIsNone(r['replication']['generation_time_yr'])
        self.assertEqual(r['food']['people'], 0)
        self.assertIsNone(r['food']['floor_per_person'])

    def test_rejects_invalid_inputs(self):
        cases = [None, [], {'oops': 1}, {'design': []}, {'overrides': []},
                 {'design': {'n_tori': 1.5}}, {'design': {'tiers_lit': True}},
                 {'design': {'radius_m': math.nan}}, {'design': {'radius_m': math.inf}},
                 {'design': {'radius_m': 0}}, {'design': {'g': -1}},
                 {'design': {'seasonal_sky': 'false'}}, {'design': {'site': 'unknown'}},
                 {'design': {'c_partner': 'Eros'}}, {'overrides': {'width_ratio': 0}},
                 {'overrides': {'not_a_parameter': 1}}]
        for payload in cases:
            with self.subTest(payload=payload), self.assertRaises((ValueError, TypeError)):
                server.calculate(payload)

    def test_exploration_bounds_are_evaluable(self):
        for radius in [200, 900, 2500]:
            for gravity in [.1, 1.2]:
                response = server.calculate({'design': {'radius_m': radius, 'g': gravity, 'n_tori': 32},
                                             'overrides': {'width_ratio': 8, 'fill_depth_m': 0}})
                self.assertGreater(response['results']['mass']['total'], 0)


if __name__ == '__main__':
    unittest.main()
