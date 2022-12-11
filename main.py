"""Main entrypoint for running each day."""

import importlib
from pathlib import Path
import sys
from typing import Optional

import utils


def main(day: int, path: Optional[Path] = None) -> None:
    """Import and run the requested day, both parts."""
    print(f'Day {day}:')
    module = importlib.import_module(f'days.day{day:02}')
    if not path:
        path = Path(__file__).parent / 'data' / f'day{day:02}.txt'
    for part in 1, 2:
        if hasattr(module, f'part{part}'):
            data = utils.read_input(path=path, options=module.INPUT_OPTIONS)
            result = getattr(module, f'part{part}')(data)
        else:
            result = 'Not found'
        print(f'  Part {part}: {result}')


if __name__ == '__main__':
    day = int(sys.argv[1])
    path: Optional[Path]
    if len(sys.argv) > 2:
        path = Path(sys.argv[2])
    else:
        path = None
    main(day, path)
