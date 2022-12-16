"""Day 15."""

import operator
import re

import utils


def process_input(raw: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """Extract sensor and beacon coordinates from an input line."""
    pattern = r'Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)'
    match = re.match(pattern, raw)
    if not match:
        raise ValueError('Bad!')
    return (
        (int(match.group('sx')), int(match.group('sy'))),
        (int(match.group('bx')), int(match.group('by'))),
    )


INPUT_OPTIONS = utils.InputOptions(
    processor=process_input,
)


def part1(coords: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    """Day 15, part 1."""
    target_y = 2000000
    cannot_contain = find_cannot_contain(coords, target_y)
    beacons = set(b for s, b in coords if b[1] == target_y)
    return sum(1 + x1 - x0 for x0, x1 in cannot_contain) - len(beacons)


def part2(coords: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    """Day 15, part 2."""
    max_coords = 4000000
    for target_y in range(max_coords + 1):
        cannot_contain = find_cannot_contain(coords, target_y)
        cannot_contain = [
            (max(x0, 0), min(x1, max_coords))
            for x0, x1 in cannot_contain
            if x1 >= 0 and x0 <= max_coords
        ]
        if cannot_contain[0][0] == 1:
            beacon = (0, target_y)
            break
        if cannot_contain[0][1] == max_coords - 1:
            beacon = (max_coords, target_y)
            break
        if len(cannot_contain) == 2:
            beacon = (cannot_contain[0][1] + 1, target_y)
            break
    else:
        raise ValueError('Hmmmmm')
    return beacon[0] * max_coords + beacon[1]


def find_cannot_contain(coords: list[tuple[tuple[int, int], tuple[int, int]]], target_y: int) -> list[tuple[int, int]]:
    """Return the ranges of coordinates that cannot contain a beacon."""
    cannot_contain: list[tuple[int, int]] = []
    for (sx, sy), (bx, by) in coords:
        radius = manhattan((sx, sy), (bx, by))
        dy = abs(target_y - sy)
        if dy <= radius:
            x0 = sx - (radius - dy)
            x1 = sx + (radius - dy)
            cannot_contain.append((x0, x1))
    return consolidate(cannot_contain)


def manhattan(coords_0: tuple[int, int], coords_1: tuple[int, int]) -> int:
    """Calculate the Manhattan distance between two sets of coordinates."""
    x_0, y_0 = coords_0
    x_1, y_1 = coords_1
    return abs(x_0 - x_1) + abs(y_0 - y_1)


def consolidate(cannot_contain: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Consolidate excluded coordinate ranges."""
    result: list[tuple[int, int]] = []
    for x0, x1 in sorted(cannot_contain, key=operator.itemgetter(0)):
        if result and x1 <= result[-1][1]:
            # The new range is completely within the previous one
            pass
        elif result and x0 <= result[-1][1]:
            # The new range overlaps with the old one, so combine them
            result[-1] = result[-1][0], x1
        else:
            # New non-overlapping range
            result.append((x0, x1))
    return result
