"""Day 25."""

import utils


INPUT_OPTIONS = utils.InputOptions()


def part1(snafus: list[str]) -> str:
    """Day 25, part 1."""
    return int_to_snafu(sum(snafu_to_int(snafu) for snafu in snafus))


def snafu_to_int(snafu: str) -> int:
    """Convert a SNAFU number to a python int."""
    return sum(
        5**i * (
            -2 if character == '='
            else -1 if character == '-'
            else int(character)
        )
        for i, character in enumerate(snafu[::-1])
    )


def int_to_snafu(value: int) -> str:
    """Convert a python int to a SNAFU number."""
    result = ''
    while value:
        digit = ((value + 2) % 5) - 2
        value = int((value - digit) / 5)
        result = ('=' if digit == -2 else '-' if digit == -1 else str(digit)) + result
    return result
