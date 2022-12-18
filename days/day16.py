"""Day 16."""

import collections
import operator
import re
from typing import Iterator, Optional

import utils


def process_input(raw: str) -> tuple[str, int, list[str]]:
    """Extract flow rate and connections from an input line."""
    pattern = r'Valve (?P<valve>.+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<connections>.+)'
    match = re.match(pattern, raw)
    if not match:
        raise ValueError('Bad!')
    return (
        match.group('valve'),
        int(match.group('rate')),
        match.group('connections').split(', '),
    )


INPUT_OPTIONS = utils.InputOptions(
    processor=process_input,
)


def part1(valves: list[tuple[str, int, list[str]]]) -> int:
    """Day 16, part 1."""
    time = 30
    useful_valves = {valve: rate for valve, rate, _ in valves if rate > 0}
    distances = {
        src: {
            dst: distance(valves, src, dst)
            for dst in useful_valves
            if src != dst
        }
        for src in useful_valves
    }
    from_aa = {
        dst: distance(valves, 'AA', dst)
        for dst in useful_valves
    }
    best_flow = 0
    for path in available_paths(distances, from_aa, time=time):
        if (total := total_flow(path, useful_valves, distances, from_aa, time=time)) > best_flow:
            best_flow = total
    return best_flow


def part2(valves: list[tuple[str, int, list[str]]]) -> int:
    """Day 16, part 2."""
    time = 26
    useful_valves = {valve: rate for valve, rate, _ in valves if rate > 0}
    distances = {
        src: {
            dst: distance(valves, src, dst)
            for dst in useful_valves
            if src != dst
        }
        for src in useful_valves
    }
    from_aa = {
        dst: distance(valves, 'AA', dst)
        for dst in useful_valves
    }
    paths = {}
    for path in available_paths(distances, from_aa, time=time):
        paths[tuple(path)] = total_flow(path, useful_valves, distances, from_aa, time=time)
    result = 0
    count = 0
    for path_me, flow_me in paths.items():
        count += 1
        for path_el, flow_el in paths.items():
            if len(set(path_me + path_el)) == len(path_me + path_el) and (flow_me + flow_el) > result:
                result = flow_me + flow_el
    return result


def distance(valves: list[tuple[str, int, list[str]]], start: str, finish: str) -> int:
    """Return the minimum distance between two valves."""
    connections = collections.defaultdict(list)
    for src, _, dst_list in valves:
        for dst in dst_list:
            connections[src].append(dst)
            connections[dst].append(src)

    visited = [start]
    location = start
    distances = {start: 0}

    while location != finish:
        for dst in connections[location]:
            if dst not in distances:
                distances[dst] = distances[location] + 1
        location = sorted(
            ((v, d) for (v, d) in distances.items() if v not in visited),
            key=operator.itemgetter(1),
        )[0][0]
        visited.append(location)
    
    return distances[finish]


def available_paths(distances: dict[str, dict[str, int]], from_aa: dict[str, int], time: int,
                    path: Optional[list[str]] = None) -> Iterator[list[str]]:
    """Iterate over the available paths that can be traversed in the time."""
    if path is None:
        path = []
    for next_location in (d for d in from_aa if d not in path):
        time_taken = distances[path[-1]][next_location] if path else from_aa[next_location]
        if time_taken < time:
            yield [*path, next_location]
            yield from available_paths(distances, from_aa, time - time_taken - 1, [*path, next_location])


def joint_paths(distances: dict[str, dict[str, int]], from_aa: dict[str, int], times: tuple[int, int],
                paths: Optional[tuple[list[str], list[str]]] = None) -> Iterator[tuple[list[str], list[str]]]:
    """Iterate over the available paths that can be traversed in the time, with an elephant."""
    if paths is None:
        paths = ([], [])
    for next_location in (d for d in from_aa if d not in paths[0] and d not in paths[1]):
        actor = 0 if times[0] >= times[1] else 1
        time_taken = distances[paths[actor][-1]][next_location] if paths[actor] else from_aa[next_location]
        if time_taken < times[actor]:
            next_paths = (
                ([*paths[0], next_location], paths[1]) if actor == 0
                else (paths[0], [*paths[1], next_location])
            )
            next_times = (
                (times[0] - time_taken - 1, times[1]) if actor == 0
                else (times[0], times[1] - time_taken - 1)
            )
            n_nested = 0
            for result in joint_paths(distances, from_aa, next_times, next_paths):
                yield result
                n_nested += 1
            if n_nested == 0:
                yield next_paths



def total_flow(path: list[str], rates: dict[str, int], distances: dict[str, dict[str, int]], from_aa: dict[str, int],
               time: int = 30) -> int:
    """Return the total flow released from following the path."""
    if not path:
        return 0
    location = path[0]
    time -= from_aa[location]
    time -= 1
    result = rates[location] * time
    for next_valve in path[1:]:
        time -= distances[location][next_valve]
        time -= 1
        location = next_valve
        result += rates[location] * time
    return result
