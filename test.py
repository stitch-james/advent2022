import importlib
import unittest

import utils


EXPECTED = {
    1: {1: 70698, 2: 206643},
    2: {1: 10310, 2: 14859},
    3: {1: 7701, 2: 2644},
    4: {1: 576, 2: 905},
}


class TestAll(unittest.TestCase):

    def test_all_days(self):
        for day in range(1, 26):
            module = importlib.import_module(f'days.day{day:02}')
            data = utils.read_input(day=day, options=module.INPUT_OPTIONS)
            for part in 1, 2:
                with self.subTest(day=f'{day:02}', part=part):
                    func = getattr(module, f'part{part}')
                    result = func(data)
                    self.assertIsNot(result, None)
                    self.assertEqual(result, EXPECTED.get(day, {}).get(part))
