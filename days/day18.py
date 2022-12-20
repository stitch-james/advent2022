"""Day 18."""

import utils


INPUT_OPTIONS = utils.InputOptions(
    processor=lambda row: tuple(int(i) for i in row.split(',')),
)


def part1(lava: list[tuple[int, int, int]]) -> int:
    """Day 18, part 1."""
    return count_surfaces(lava)


def part2(lava: list[tuple[int, int, int]]) -> int:
    """Day 18, part 2."""
    ranges = tuple((min(l[i] for l in lava), max(l[i] for l in lava)) for i in range(3))
    # Start at (-1, -1, -1) and grow the exterior to envelope the lava
    exterior = [(ranges[0][0]-1, ranges[1][0]-1, ranges[2][0]-1)]
    to_grow = [*exterior]
    while to_grow:
        source = to_grow.pop()
        for adjacent in [
            (source[0]-1, source[1], source[2]),
            (source[0]+1, source[1], source[2]),
            (source[0], source[1]-1, source[2]),
            (source[0], source[1]+1, source[2]),
            (source[0], source[1], source[2]-1),
            (source[0], source[1], source[2]+1),
        ]:
            if adjacent not in exterior and adjacent not in lava and all(
                ranges[i][0]-1 <= adjacent[i] <= ranges[i][1] + 1
                for i in range(3)
            ):
                exterior.append(adjacent)
                to_grow.append(adjacent)
    filled_lava = [
        (i, j, k)
        for i in range(ranges[0][0], ranges[0][1] + 1)
        for j in range(ranges[1][0], ranges[1][1] + 1)
        for k in range(ranges[2][0], ranges[2][1] + 1)
        if (i, j, k) not in exterior
    ]
    return count_surfaces(filled_lava)


def count_surfaces(lava: list[tuple[int, int, int]]) -> int:
    """Count the surface squares of the lava."""
    n_touching = 0
    for i, lava_i in enumerate(lava):
        x_i, y_i, z_i = lava_i
        for lava_j in lava[i + 1 : ]:
            x_j, y_j, z_j = lava_j
            if abs(x_i - x_j) + abs(y_i - y_j) + abs(z_i - z_j) == 1:
                n_touching += 1
    return 6 * len(lava) - 2 * n_touching
