"""IO and utils functions."""

import dataclasses
from pathlib import Path
from typing import Callable


def noop(row: str) -> str:
    """Do nothing."""
    return row


@dataclasses.dataclass
class InputOptions:
    processor: Callable = noop
    split_groups: bool = False
    single_row: bool = False


def read_input(day: int, options: InputOptions) -> list:
    """Read from file and process input."""
    raw = (Path(__file__).parent / 'data' / f'day{day:02}.txt').read_text().strip()
    if options.split_groups:
        return [[options.processor(item) for item in group.split('\n')] for group in raw.split('\n\n')]
    elif options.single_row:
        return options.processor(raw.strip())
    else:
        return [options.processor(item) for item in raw.split('\n')]
