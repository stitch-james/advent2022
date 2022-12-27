"""Day 20."""

import utils


INPUT_OPTIONS = utils.InputOptions(
    processor=int,
)


def part1(numbers: list[int]) -> int:
    """Day 20, part 1."""
    return grove(mix(numbers, 1))


def part2(numbers: list[int]) -> int:
    """Day 20, part 2."""
    numbers = [n * 811589153 for n in numbers]
    return grove(mix(numbers, 10))


def mix(numbers: list[int], n_mix: int) -> list[int]:
    """Return a mixed list."""
    numbers = [*numbers]
    order = list(range(len(numbers)))
    for _ in range(n_mix):
        for index_original in range(len(numbers)):
            index_mixed = order.index(index_original)
            index_new = (index_mixed + numbers[index_mixed]) % (len(numbers) - 1)
            numbers.insert(index_new, numbers.pop(index_mixed))
            order.insert(index_new, order.pop(index_mixed))
    return numbers


def grove(numbers: list[int]) -> int:
    """Return the sum of the grove coordinates."""
    zero_index = numbers.index(0)
    return sum(numbers[(zero_index + i) % len(numbers)] for i in (1000, 2000, 3000))
