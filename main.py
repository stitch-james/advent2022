"""Main entrypoint for running each day."""

import importlib
import sys

import utils


def main(day: int) -> None:
    """Import and run the requested day, both parts."""
    print(f'Day {day}:')
    module = importlib.import_module(f'days.day{day:02}')
    data = utils.read_input(day=day, options=module.INPUT_OPTIONS)
    for part in 1, 2:
        if hasattr(module, f'part{part}'):
            result = getattr(module, f'part{part}')(data)
        else:
            result = 'Not found'
        print(f'  Part {part}: {result}')


if __name__ == '__main__':
    main(int(sys.argv[1]))
