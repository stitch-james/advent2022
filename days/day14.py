"""Day 14."""

import utils


INPUT_OPTIONS = utils.InputOptions(
    processor=lambda row: [(int(coords.split(',')[0]), int(coords.split(',')[1])) for coords in row.split(' -> ')],
)


def part1(rock_corners: list[list[tuple[int, int]]]) -> int:
    """Day 14, part 1."""
    return simulate(rock_corners, with_floor=False)


def part2(rock_corners: list[list[tuple[int, int]]]) -> int:
    """Day 14, part 2."""
    return simulate(rock_corners, with_floor=True)


def simulate(rock_corners: list[list[tuple[int, int]]], with_floor: bool) -> int:
    """Simulate sand falling and return the amount that fits."""
    rock = process_corners(rock_corners)
    cave_floor = max(r[1] for r in rock) + 2  # Positive is downwards
    sand = set()
    full = False
    start = (500, 0)
    while not full:
        falling = start
        while True:
            options = [
                (falling[0], falling[1] + 1),
                (falling[0] - 1, falling[1] + 1),
                (falling[0] + 1, falling[1] + 1),
            ]
            for next_coords in options:
                if next_coords not in sand and next_coords not in rock:
                    falling = next_coords
                    # Cut the for loop short, we've found the best next location
                    break
            else:
                # We have not found a new place for the sand to fall to
                sand.add(falling)
                if falling == start:
                    # The sand couldn't fall anywhere, so we're done
                    full = True
                # Jump out of the inner while loop and move onto the next piece of sand
                break
            if falling[1] == (cave_floor - 1):
                if with_floor:
                    # The sand has reached the floor
                    sand.add(falling)
                else:
                    # The sand is falling out the bottom, so we're done
                    full = True
                break
    return len(sand)


def process_corners(rock_corners: list[list[tuple[int, int]]]) -> set[tuple[int, int]]:
    """Create the set of all coordinates that contain rock."""
    rock = set()
    for rock_line in rock_corners:
        position = rock_line[0]
        rock.add(position)
        for next_corner in rock_line[1:]:
            dx = 1 if next_corner[0] > position[0] else -1 if next_corner[0] < position[0] else 0
            dy = 1 if next_corner[1] > position[1] else -1 if next_corner[1] < position[1] else 0
            while position != next_corner:
                position = (position[0] + dx, position[1] + dy)
                rock.add(position)
    return rock