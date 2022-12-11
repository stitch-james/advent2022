"""Day 10."""

import utils


INPUT_OPTIONS = utils.InputOptions()


BZPAJELK = [
    '###..####.###...##....##.####.#....#..#.',
    '#..#....#.#..#.#..#....#.#....#....#.#..',
    '###....#..#..#.#..#....#.###..#....##...',
    '#..#..#...###..####....#.#....#....#.#..',
    '#..#.#....#....#..#.#..#.#....#....#.#..',
    '###..####.#....#..#..##..####.####.#..#.'
]


def part1(instructions: list[str]) -> int:
    """Day 10, part 1."""
    breakpoints = (20, 60, 100, 140, 180, 220)
    x = 1
    cycle = 0

    result = 0

    for instruction in instructions:
        if instruction == 'noop':
            result, cycle = step1(result, cycle, x, breakpoints)
        elif instruction.startswith('addx '):
            result, cycle = step1(result, cycle, x, breakpoints)
            result, cycle = step1(result, cycle, x, breakpoints)
            x += int(instruction.removeprefix('addx '))
    
    return result


def step1(result: int, cycle: int, x: int, breakpoints: tuple[int, ...]) -> tuple[int, int]:
    """Step forwards one cycle, adding to the result if necessary."""
    cycle += 1
    if cycle in breakpoints:
        result += cycle * x
    return result, cycle


def part2(instructions: list[str]) -> str:
    """Day 10, part 2."""
    output: list[str] = []

    x = 1
    cycle = 0

    for instruction in instructions:
        if instruction == 'noop':
            cycle, output = step2(cycle, x, output)
        elif instruction.startswith('addx '):
            cycle, output = step2(cycle, x, output)
            cycle, output = step2(cycle, x, output)
            x += int(instruction.removeprefix('addx '))

    if output == BZPAJELK:
        return 'BZPAJELK'
    else:
        for row in output:
            print(row)
        raise ValueError('Unrecognised output!')


def step2(cycle: int, x: int, output: list[str], width: int = 40) -> tuple[int, list[str]]:
    """Increment the cycle and update the output."""
    cycle += 1
    pixel = (cycle - 1) % width

    if pixel == 0:
        output.append('')

    if x - 1 <= pixel <= x + 1:
        value = '#'
    else:
        value = '.'
    
    output[-1] += value

    return cycle, output
