"""Regression test."""

import importlib
from pathlib import Path
import unittest

import utils


EXPECTED = {
    1: {1: 70698, 2: 206643},
    2: {1: 10310, 2: 14859},
    3: {1: 7701, 2: 2644},
    4: {1: 576, 2: 905},
    5: {1: 'FWNSHLDNZ', 2: 'RNRGDNFQG'},
    6: {1: 1896, 2: 3452},
    7: {1: 1886043, 2: 3842121},
    8: {1: 1719, 2: 590824},
    9: {1: 6057, 2: 2514},
    10: {1: 11220, 2: 'BZPAJELK'},
    11: {1: 50616, 2: 11309046332},
    12: {1: 468, 2: 459},
    13: {1: 5330, 2: 27648},
    14: {1: 892, 2: 27155},
    15: {1: 4873353, 2: 11600823139120},
    16: {1: 1741, 2: 2316},
    17: {1: 3184, 2: 1577077363915},
    18: {1: 4364, 2: 2508},
    19: {1: 1382, 2: 31740},
}


class TestAll(unittest.TestCase):

    def test_all_days(self):
        for day in range(1, 26):
            module = importlib.import_module(f'days.day{day:02}')
            path = Path(__file__).parent / 'data' / f'day{day:02}.txt'
            for part in 1, 2:
                with self.subTest(day=f'{day:02}', part=part):
                    func = getattr(module, f'part{part}')
                    data = utils.read_input(path=path, options=module.INPUT_OPTIONS)
                    result = func(data)
                    self.assertIsNot(result, None)
                    self.assertEqual(result, EXPECTED.get(day, {}).get(part))
