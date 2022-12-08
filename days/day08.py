"""Day 8."""

import utils


INPUT_OPTIONS = utils.InputOptions(
    processor=lambda row: [int(i) for i in row],
)


def part1(trees: list[list[int]]) -> int:
    """Day 8, part 1."""
    from_left = check_visibility(trees)
    from_top = rotate(check_visibility(rotate(trees, 1)), -1)
    from_right = rotate(check_visibility(rotate(trees, 2)), -2)
    from_bottom = rotate(check_visibility(rotate(trees, 3)), -3)
    visible = [
        [
            l or t or r or b for l, t, r, b in zip(row_l, row_t, row_r, row_b)
        ]
        for (row_l, row_t, row_r, row_b) in zip(from_left, from_top, from_right, from_bottom)
    ]
    return sum(sum(row) for row in visible)


def part2(trees: list[list[int]]) -> int:
    """Day 8, part 2."""
    most_scenic = 0
    for j in range(len(trees)):
        for i in range(len(trees[j])):
            score = calculate_scenic_score(trees, j, i)
            if score > most_scenic:
                most_scenic = score
    return most_scenic


def check_visibility(trees: list[list[int]]) -> list[list[bool]]:
    """Return map of visibility from the left hand side."""
    visible = [[False for _ in row] for row in trees]
    for row_trees, row_visible in zip(trees, visible):
        highest = -1
        for idx, tree in enumerate(row_trees):
            if tree > highest:
                row_visible[idx] = True
                highest = tree
    return visible


def rotate(grid: list[list], quarters: int) -> list[list]:
    """Rotate the grid by a number of quarters."""
    # Do the rotation by 90 degrees at a time
    # Best hope that quarters actually is an int or we'll get an infinite loop
    while quarters != 0:
        x_max = len(grid[0])
        y_max = len(grid)
        if quarters > 0:
            grid = [[grid[i][j] for i in range(y_max)] for j in range(x_max-1, -1, -1)]
            quarters -= 1
        else:
            grid = [[grid[i][j] for i in range(y_max-1, -1, -1)] for j in range(x_max)]
            quarters += 1
    return grid


def calculate_scenic_score(trees: list[list[int]], j: int, i: int) -> int:
    """Calculate the scenic score at one location."""
    result = 1
    # Check each direction in turn, multiplying the results as we go
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        count = 0
        i2 = i + di
        j2 = j + dj
        while 0 <= i2 < len(trees[0]) and 0 <= j2 < len(trees):
            # Count this tree, even if it's the blocker
            count += 1
            if trees[j2][i2] >= trees[j][i]:
                break
            i2 += di
            j2 += dj
        result *= count
    return result
