"""Day 1."""

import utils


INPUT_OPTIONS = utils.InputOptions(
    processor=int,
    split_groups=True,
)


def part1(all_calories: list[list[int]]) -> int:
    """Day 1, part 1."""
    per_elf = [sum(calories) for calories in all_calories]
    return max(per_elf)


def part2(all_calories: list[list[int]]) -> int:
    """Day 1, part 2."""
    per_elf = [sum(calories) for calories in all_calories]
    return sum(sorted(per_elf)[-3:])
