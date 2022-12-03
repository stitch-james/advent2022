"""IO and utils functions."""

from pathlib import Path
from typing import Callable, Optional


def read_input(day: int, processor: Optional[Callable] = int, split_groups: bool = False) -> list:
    """Read from file and process input."""
    if processor is None:
        processor = lambda row: row
    raw = (Path(__file__).parent / 'data' / f'day{day:02}.txt').read_text().strip()
    if split_groups:
        return [[processor(item) for item in group.split('\n')] for group in raw.split('\n\n')]
    else:
        return [processor(item) for item in raw.split('\n')]
