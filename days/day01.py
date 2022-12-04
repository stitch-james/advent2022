"""Day 1."""

import utils


def part1() -> int:
    """Day 1, part 1."""
    all_calories = utils.read_input(day=1, processor=int, split_groups=True)
    per_elf = [sum(calories) for calories in all_calories]
    return max(per_elf)


def part2() -> int:
    """Day 1, part 2."""
    all_calories = utils.read_input(day=1, processor=int, split_groups=True)
    per_elf = [sum(calories) for calories in all_calories]
    return sum(sorted(per_elf)[-3:])
