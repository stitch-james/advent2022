"""Day 23."""

import itertools

import utils


def read_grove(raw: str) -> set[tuple[int, int]]:
    """Read a raw grove string into coordinates."""
    return set(
        (i_row, i_col)
        for i_row, row in enumerate(raw.split('\n'))
        for i_col, character in enumerate(row)
        if character == '#'
    )


INPUT_OPTIONS = utils.InputOptions(
    processor=read_grove,
    single_row=True,
)


def part1(elves: set[tuple[int, int]]) -> int:
    """Day 23, part 1."""
    order = ['N', 'S', 'W', 'E']
    for _ in range(10):
        elves = move_elves(elves, order)
        order = order[1:] + [order[0]]
    return empty_spaces(elves)


def part2(elves: set[tuple[int, int]]) -> int:
    """Day 23, part 2."""
    order = ['N', 'S', 'W', 'E']
    for i in itertools.count(1):
        new_elves = move_elves(elves, order)
        if elves == new_elves:
            return i
        elves = new_elves
        order = order[1:] + [order[0]]
    raise RuntimeError('Really, no')


def move_elves(elves: set[tuple[int, int]], order: list[str]) -> set[tuple[int, int]]:
    """Propose, check and move to new spaces."""
    proposal_with_fallback = []
    for elf in elves:
        if clear_all_around(elves, elf):
            proposal_with_fallback.append((elf, elf))
        else:
            for direction in order:
                if looks_clear(elves, elf, direction):
                    proposal_with_fallback.append((move_elf(elf, direction), elf))
                    break
            else:
                proposal_with_fallback.append((elf, elf))
    proposal = [p for p, f in proposal_with_fallback]
    return set(p if proposal.count(p) == 1 else f for p, f in proposal_with_fallback)


def clear_all_around(elves: set[tuple[int, int]], elf: tuple[int, int]) -> bool:
    """Return whether or not the elf is sitting on their own."""
    return all(
        i == j == 0 or (elf[0] + i, elf[1] + j) not in elves
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
    )

def looks_clear(elves: set[tuple[int, int]], elf: tuple[int, int], direction: str) -> bool:
    """Return whether or not it looks clear in the given direction."""
    if direction == 'N':
        deltas = [(-1, -1), (-1, 0), (-1, 1)]
    elif direction == 'S':
        deltas = [(1, -1), (1, 0), (1, 1)]
    elif direction == 'W':
        deltas = [(-1, -1), (0, -1), (1, -1)]
    elif direction == 'E':
        deltas = [(-1, 1), (0, 1), (1, 1)]
    else:
        raise ValueError('I will not go there!')
    return not any((elf[0] + i, elf[1] + j) in elves for i, j in deltas)

def move_elf(elf: tuple[int, int], direction: str) -> tuple[int, int]:
    """Return the elf's new position after moving."""
    if direction == 'N':
        return (elf[0] - 1, elf[1])
    if direction == 'S':
        return (elf[0] + 1, elf[1])
    if direction == 'W':
        return (elf[0], elf[1] - 1)
    if direction == 'E':
        return (elf[0], elf[1] + 1)
    raise ValueError('I will not go there!')

def empty_spaces(elves: set[tuple[int, int]]) -> int:
    """Count the empty spaces between the elves."""
    min_x = min(j for i, j in elves)
    max_x = max(j for i, j in elves)
    min_y = min(i for i, j in elves)
    max_y = max(i for i, j in elves)
    return (max_x + 1 - min_x) * (max_y + 1 - min_y) - len(elves)
