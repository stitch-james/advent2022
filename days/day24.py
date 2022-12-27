"""Day 24."""

import itertools

import utils


def read_valley(raw_map: str) -> tuple[tuple[int, int], list[tuple[int, int, str]]]:
    """Process the map and return its size and the blizzard setup."""
    rows = raw_map.split('\n')
    blizzards = [
        (i, j, character)
        for i, row in enumerate(rows[1 : len(rows) - 1])
        for j, character in enumerate(row[1 : len(row) - 1])
        if character in '^>v<'
    ]
    return (len(rows) - 2, len(rows[0]) - 2), blizzards


INPUT_OPTIONS = utils.InputOptions(
    processor=read_valley,
    single_row=True,
)


def part1(valley: tuple[tuple[int, int], list[tuple[int, int, str]]]) -> int:
    """Day 24, part 1."""
    size, blizzards = valley
    options = set([(-1, 0)])
    target = (size[0], size[1] - 1)
    for t in itertools.count(1):
        blizzards = move_blizzards(size, blizzards)
        options = next_options(size, blizzards, options)
        if target in options:
            return t
    raise RuntimeError('Definitely not')


def part2(valley: tuple[tuple[int, int], list[tuple[int, int, str]]]) -> int:
    """Day 24, part 2."""
    size, blizzards = valley
    options = set([(-1, 0)])
    target = (size[0], size[1] - 1)
    with_snacks = False
    for t in itertools.count(1):
        blizzards = move_blizzards(size, blizzards)
        options = next_options(size, blizzards, options)
        if target in options:
            options = set([target])
            if target == (size[0], size[1] - 1) and not with_snacks:
                target = (-1, 0)
            elif target == (-1, 0):
                target = (size[0], size[1] - 1)
                with_snacks = True
            else:
                return t
    raise RuntimeError('Definitely not')


def next_options(size: tuple[int, int], blizzards: list[tuple[int, int, str]], options: set[tuple[int, int]],
                 ) -> set[tuple[int, int]]:
    """Return the next set of options, given the blizzard positions."""
    blizzards_positions = set((i, j) for (i, j, _) in blizzards)
    return set(o for option in options for o in options_to_move(size, blizzards_positions, option))


def move_blizzards(size: tuple[int, int], blizzards: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    """Move the blizzards to the next position"""
    n_i, n_j = size
    return [
        ((i - 1) % n_i, j, f) if f == '^'
        else ((i + 1) % n_i, j, f) if f == 'v'
        else (i, (j - 1) % n_j, f) if f == '<'
        else (i, (j + 1) % n_j, f)
        for i, j, f in blizzards
    ]


def options_to_move(size: tuple[int, int], blizzards: set[tuple[int, int]], position: tuple[int, int],
                    ) -> list[tuple[int, int]]:
    """Return the list of options the expedition can move to."""
    result = [position]

    if (
        (position[0] == (size[0] - 1) and position[1] == (size[1] - 1))
        or (position[0] < (size[0] - 1))
    ):
        result.append((position[0] + 1, position[1]))

    if position[1] < (size[1] - 1) and position[0] >= 0:
        result.append((position[0], position[1] + 1))

    if (
        (position[0] == 0 and position[1] == 0)
        or (position[0] > 0)
    ):
        result.append((position[0] - 1, position[1]))

    if position[1] > 0 and position[0] < size[0]:
        result.append((position[0], position[1] - 1))

    return [option for option in result if option not in blizzards]
