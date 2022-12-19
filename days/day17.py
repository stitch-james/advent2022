"""Day 17."""

import utils


INPUT_OPTIONS = utils.InputOptions(
    single_row=True,
)



SHAPES = [
    [
        '####',
    ],
    [
        '.#.',
        '###',
        '.#.',
    ],
    [
        '..#',
        '..#',
        '###',
    ],
    [
        '#',
        '#',
        '#',
        '#',
    ],
    [
        '##',
        '##',
    ],
]

SHAPES = [shape[::-1] for shape in SHAPES]


def part1(jets: str) -> int:
    """Day 17, part 1."""
    return run_tetris(jets, 2022)


def part2(jets: str) -> int:
    """Day 17, part 2."""
    return run_tetris(jets, 1000000000000)


def run_tetris(jets: str, n_shape: int) -> int:
    """Run the tetris simulation."""
    tower: list[str] = []
    tower_base: int = 0
    i = 0
    j = 0
    history: list[tuple[list[str], int, int]] = []
    count: list[tuple[int, int]] = []
    while i < n_shape:
        state = (tower, i % len(SHAPES), j % len(jets))
        if state in history:
            i_previous, base_previous = count[history.index(state)]
            delta_base = tower_base - base_previous
            delta_i = i - i_previous
            n_skip = int((n_shape - i) / delta_i)
            i += delta_i * n_skip
            tower_base += delta_base * n_skip
        history.append(state)
        count.append((i, tower_base))
        shape = SHAPES[i % len(SHAPES)]
        x, y = place_start(tower)
        stopped = False
        while not stopped:
            x = blow_jet(x, y, jets[j % len(jets)], shape, tower)
            j += 1
            y, stopped = drop(x, y, shape, tower)
        tower = add_to_tower(x, y, shape, tower)
        tower, tower_base = truncate_tower(tower, tower_base)
        i += 1
    return len(tower) + tower_base


def place_start(tower: list[str]) -> tuple[int, int]:
    """Return the starting coordinates of the bottom-left corner of the next shape."""
    return (2, len(tower) + 3)


def blow_jet(x: int, y: int, jet: str, shape: list[str], tower: list[str]) -> int:
    """Return the resulting x coordinate after the jet blows."""
    if (x == 0 and jet == '<') or (x == 7 - len(shape[0]) and jet == '>'):
        return x
    new_x = x - 1 if jet == '<' else x + 1
    if overlap(new_x, y, shape, tower):
        return x
    return new_x


def overlap(x: int, y: int, shape: list[str], tower: list[str]) -> bool:
    """Check if the shape overlaps with the tower."""
    for i, row in enumerate(shape):
        for j, pixel in enumerate(row):
            if i + y < len(tower) and pixel == '#' and tower[i + y][j + x] == '#':
                return True
    return False


def drop(x: int, y: int, shape: list[str], tower: list[str]) -> tuple[int, bool]:
    """Return the resulting y coordinate after the shape drops."""
    if y == 0:
        return y, True
    new_y = y - 1
    if overlap(x, new_y, shape, tower):
        return y, True
    return new_y, False


def add_to_tower(x: int, y: int, shape: list[str], tower: list[str]) -> list[str]:
    """Return the new tower after adding the shape in its current location."""
    return [
        ''.join(
            '#'
            if (i < len(tower) and tower[i][j] == '#')
            or (y <= i < (y + len(shape)) and x <= j < (x + len(shape[0])) and shape[i-y][j-x] == '#')
            else '.'
            for j in range(7)
        )
        for i in range(max(y + len(shape), len(tower)))
    ]


def truncate_tower(tower: list[str], tower_base: int) -> tuple[list[str], int]:
    """Remove unnecessary rows from the bottom of the tower."""
    new_base = 0
    for i, row in enumerate(tower):
        if row == '#' * len(row):
            new_base = i
    return [*tower[new_base:]], new_base + tower_base
