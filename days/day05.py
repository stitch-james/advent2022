"""Day 5."""

import re
from typing import Iterator

import utils


INPUT_OPTIONS = utils.InputOptions(
    split_groups=True,
)


def part1(data: list[list[str]]) -> str:
    """Day 5, part 1."""
    layout, instructions = data
    stacks = process_layout(layout)

    for count, src, dst in read_instructions(instructions):
        for _ in range(count):
            stacks[dst].append(stacks[src].pop())
    
    return top_crates(stacks)


def part2(data: list[list[str]]) -> str:
    """Day 5, part 2."""
    layout, instructions = data
    stacks = process_layout(layout)

    for count, src, dst in read_instructions(instructions):
        stacks[src], moving = stacks[src][:-count], stacks[src][-count:]
        stacks[dst].extend(moving)

    return top_crates(stacks)


def process_layout(layout: list[str]) -> dict[int, list[str]]:
    """Turn the raw layout strings into a dict of stacks."""
    keys = [int(k) for k in layout[-1].split()]
    stacks: dict[int, list[str]] = {key: [] for key in keys}

    for layer in layout[-2::-1]:
        filled = layer.replace('    ', ' [ ]')
        letters = [l.strip('[]') for l in filled.split('] [')]
        for key, letter in zip(keys, letters):
            if letter.strip():
                stacks[key].append(letter)

    return stacks


def read_instructions(instructions: list[str]) -> Iterator[tuple[int, int, int]]:
    """Read and process each line of the instructions."""
    for instruction in instructions:
        match = re.match(r'move (?P<count>\d+) from (?P<src>\d) to (?P<dst>\d)', instruction)
        if not match:
            raise ValueError('Screwed up the regex')
        count = int(match.group('count'))
        src = int(match.group('src'))
        dst = int(match.group('dst'))
        yield count, src, dst


def top_crates(stacks: dict[int, list[str]]) -> str:
    """Return the top layer of crates."""
    return ''.join(stacks[key][-1] for key in sorted(stacks.keys()))
