import importlib
import unittest


EXPECTED = {
    1: {1: 70698},
}


class TestAll(unittest.TestCase):

    def test_all_days(self):
        for day in range(1, 26):
            for part in range(1, 3):
                with self.subTest(day=f'{day:02}', part=part):
                    module = importlib.import_module(f'days.day{day:02}')
                    func = getattr(module, f'part{part}')
                    result = func()
                    self.assertIsNot(result, None)
                    self.assertEqual(result, EXPECTED.get(day, {}).get(part))
