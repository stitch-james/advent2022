"""Day 6."""

import utils


INPUT_OPTIONS = utils.InputOptions(
    single_row=True,
)


def part1(stream: str) -> int:
    """Day 6, part 1."""
    return find_unique(stream, 4)


def part2(stream: str) -> int:
    """Day 6, part 2."""
    return find_unique(stream, 14)


def find_unique(stream: str, marker_size: int) -> int:
    """Return the length at the marker of unique characters."""
    for start in range(len(stream)):
        if len(set(stream[start : start + marker_size])) == marker_size:
            return len(stream[: start + marker_size])
    raise RuntimeError('Missed the answer!')
