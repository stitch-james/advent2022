"""Day 3."""

import utils


def split_row(row: str) -> tuple[set[str], set[str]]:
    """Split the row into the two compartments."""
    half = int(len(row) / 2)
    return set(row[:half]), set(row[half:])


INPUT_OPTIONS = utils.InputOptions(
    processor=split_row,
)


def part1(contents_split: list[tuple[set[str], set[str]]]) -> int:
    """Day 3, part 1."""
    result = 0
    for first, second in contents_split:
        overlap = (first & second).pop()
        result += priority(overlap)
    return result


def part2(contents_split: list[tuple[set[str], set[str]]]) -> int:
    """Day 3, part 2."""
    contents = [first | second for first, second in contents_split]
    result = 0
    for idx in range(0, len(contents), 3):
        first, second, third = contents[idx : idx + 3]
        overlap = (first & second & third).pop()
        result += priority(overlap)
    return result


def priority(item: str) -> int:
    """Return the priority value of the item."""
    if len(item) != 1:
        raise ValueError('Only one item please!')
    if item.lower() == item:
        # Lower case letters have priority 1-26
        return ord(item) - ord('a') + 1
    # Upper case letters have priority 27-52
    return ord(item) - ord('A') + 27
