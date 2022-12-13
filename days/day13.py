"""Day 13."""

import enum
import functools
import json
from typing import Union

import utils


Packet = Union[int, list['Packet']]


INPUT_OPTIONS = utils.InputOptions(
    processor=json.loads,
    split_groups=True,
)


def part1(packets: list[list[Packet]]) -> int:
    """Day 13, part 1."""
    return sum(idx + 1 for idx, (left, right) in enumerate(packets) if order(left, right) < 0)


def part2(packets: list[list[Packet]]) -> int:
    """Day 13, part 1."""
    init: list[Packet] = []
    flat = sum(packets, init)
    dividers: tuple[Packet, Packet] = ([[2]], [[6]])
    flat.extend(dividers)

    packets_sorted = sorted(flat, key=functools.cmp_to_key(order))

    return (packets_sorted.index(dividers[0]) + 1) * (packets_sorted.index(dividers[1]) + 1)


def order(left: Packet, right: Packet) -> int:
    """Return which comes first out of left or right."""
    if isinstance(left, int) and isinstance(right, int):
        return -1 if left < right else 1 if right < left else 0

    if isinstance(left, int) and isinstance(right, list):
        return order([left], right)
    
    if isinstance(left, list) and isinstance(right, int):
        return order(left, [right])
    
    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            o = order(l, r)
            if o != 0:
                return o
        return order(len(left), len(right))

    raise TypeError('No thank you')
