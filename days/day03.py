"""Day 3."""

import utils


def part1() -> int:
    """Day 3, part 1."""
    contents = utils.read_input(day=3, processor=split_row)
    result = 0
    for first, second in contents:
        for item in first:
            if item in second:
                result += priority(item)
                break  # Exactly one mistake per row
    return result


def part2() -> int:
    """Day 3, part 2."""
    contents = utils.read_input(day=3, processor=None)
    available = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = 0
    for idx in range(0, len(contents), 3):
        rows = contents[idx : idx + 3]
        for item in available:
            if all(item in row for row in rows):
                result += priority(item)
                available.replace(item, '')
                break
    return result


def split_row(row: str) -> tuple[str, str]:
    """Split the row into the two compartments."""
    half = int(len(row) / 2)
    return row[:half], row[half:]


def priority(item: str) -> int:
    """Return the priority value of the item."""
    if len(item) != 1:
        raise ValueError('Only one item please!')
    if item.lower() == item:
        # Lower case letters have priority 1-26
        return ord(item) - ord('a') + 1
    # Upper case letters have priority 27-52
    return ord(item) - ord('A') + 27


if __name__ == '__main__':
    print(part1())
    print(part2())
