"""Day 12."""

from typing import Iterator

import utils


INPUT_OPTIONS = utils.InputOptions()


def part1(raw: list[str]) -> int:
    """Day 12, part 1."""
    elevation, start, end = process_map(raw)
    n_x = len(raw[0])
    n_y = len(raw)
    distance = {start: 0}
    updating = [start]
    while updating:
        location = updating.pop(0)
        for next_location in adjacent(location, n_x, n_y):
            if elevation[next_location] - elevation[location] <= 1 and (
                next_location not in distance or distance[next_location] > (distance[location] + 1)
            ):
                distance[next_location] = distance[location] + 1
                if next_location not in updating:
                    updating.append(next_location)
    return distance[end]


def part2(raw: list[str]) -> int:
    """Day 12, part 2."""
    elevation, _, end = process_map(raw)
    n_x = len(raw[0])
    n_y = len(raw)
    distance = {end: 0}
    updating = [end]
    while updating:
        location = updating.pop(0)
        for next_location in adjacent(location, n_x, n_y):
            if elevation[location] - elevation[next_location] <= 1 and (
                next_location not in distance or distance[next_location] > (distance[location] + 1)
            ):
                distance[next_location] = distance[location] + 1
                if next_location not in updating:
                    updating.append(next_location)
    return min(dist for coords, dist in distance.items() if elevation[coords] == 0)


def process_map(raw: list[str]) -> tuple[dict[tuple[int, int], int], tuple[int, int], tuple[int, int]]:
    """Turn the raw map into elevation, and start and end points."""
    elevation: dict[tuple[int, int], int] = {}
    start = (-1, -1)
    end = (-1, -1)
    for i in range(len(raw)):
        for j in range(len(raw[0])):
            if raw[i][j] == 'S':
                elevation[(j, i)] = 0
                start = (j, i)
            elif raw[i][j] == 'E':
                elevation[(j, i)] = 25
                end = (j, i)
            else:
                elevation[(j, i)] = ord(raw[i][j]) - ord('a')
    assert min(start) >= 0
    assert min(end) >= 0
    assert min(min(row) for row in elevation) >= 0
    return elevation, start, end


def adjacent(location: tuple[int, int], n_x: int, n_y: int) -> Iterator[tuple[int, int]]:
    """Yield adjacent coordinates, if they are in the grid."""
    if location[0] > 0:
        yield (location[0] - 1, location[1])
    if location[0] < (n_x - 1):
        yield (location[0] + 1, location[1])
    if location[1] > 0:
        yield (location[0], location[1] - 1)
    if location[1] < (n_y - 1):
        yield (location[0], location[1] + 1)
