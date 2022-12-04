"""Main entrypoint for running each day."""

import importlib
import sys


def main(day: int) -> None:
    """Import and run the requested day, both parts."""
    print(f'Day {day}:')
    day_module = importlib.import_module(f'days.day{day:02}')
    for part in 1, 2:
        if hasattr(day_module, f'part{part}'):
            result = getattr(day_module, f'part{part}')()
        else:
            result = 'Not found'
        print(f'  Part {part}: {result}')


if __name__ == '__main__':
    main(int(sys.argv[1]))
