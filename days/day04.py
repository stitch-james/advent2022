"""Day 4."""

import utils


def process_ranges(row: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """Turn the ranges string into the min/max section IDs for each elf."""
    return tuple(tuple(int(value) for value in elf.split('-')) for elf in row.split(','))


INPUT_OPTIONS = utils.InputOptions(
    processor=process_ranges,
)


def part1(ranges: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    """Day 4, part 1."""
    return sum(
        (min_a <= min_b <= max_b <= max_a)
        or (min_b <= min_a <= max_a <= max_b)
        for (min_a, max_a), (min_b, max_b) in ranges
    )


def part2(ranges: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    return sum(
        max_a >= min_b and max_b >= min_a
        for (min_a, max_a), (min_b, max_b) in ranges
    )
