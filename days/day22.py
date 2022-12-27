"""Day 22."""

from typing import Union

import utils


INPUT_OPTIONS = utils.InputOptions(
    process_as_group=True,
)


FACINGS = ['^', '>', 'v', '<']

FACING_VALUES = {
    # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
    '>': 0,
    'v': 1,
    '<': 2,
    '^': 3,
}


def part1(inputs: list[str]) -> int:
    """Day 22, part 1."""
    board_str, instructions_str = inputs
    board = process_board(board_str)
    instructions = process_instructions(instructions_str)
    row = 0
    column = board[0].index('.')
    facing = '>'

    connections = mirror_connections({
        (0, c, '^'): (149, c, '^') for c in range(50, 100)
    } | {
        (0, c, '^'): (49, c, '^') for c in range(100, 150)
    } | {
        (100, c, '^'): (199, c, '^') for c in range(0, 50)
    } | {
        (r, 50, '<'): (r, 149, '<') for r in range(0, 50)
    } | {
        (r, 50, '<'): (r, 99, '<') for r in range(50, 100)
    } | {
        (r, 0, '<'): (r, 99, '<') for r in range(100, 150)
    } | {
        (r, 0, '<'): (r, 49, '<') for r in range(150, 200)
    })

    for instruction in instructions:
        row, column, facing = step(row, column, facing, board, connections, instruction)
    return password(row, column, facing)


def part2(inputs: list[str]) -> int:
    """Day 22, part 2."""
    board_str, instructions_str = inputs
    board = process_board(board_str)
    instructions = process_instructions(instructions_str)
    row = 0
    column = board[0].index('.')
    facing = '>'

    connections = mirror_connections({
        (0, c, '^'): (150 + c - 50, 0, '>') for c in range(50, 100)
    } | {
        (0, c, '^'): (199, c - 100, '^') for c in range(100, 150)
    } | {
        (100, c, '^'): (50 + c, 50, '>') for c in range(0, 50)
    } | {
        (r, 50, '<'): (149 - r, 0, '>') for r in range(0, 50)
    } | {
        (r, 149, '>'): (149 - r, 99, '<') for r in range(0, 50)
    } | {
        (49, c, 'v'): (50 + c - 100, 99, '<') for c in range(100, 150)
    } | {
        (149, c, 'v'): (150 + c - 50, 49, '<') for c in range(50, 100)
    })

    for instruction in instructions:
        row, column, facing = step(row, column, facing, board, connections, instruction)
    return password(row, column, facing)


def process_board(board_str: str) -> list[str]:
    """Turn a raw board string into a rectangular board."""
    board = board_str.strip('\n').split('\n')
    width = max(len(b) for b in board)
    board = [b + ' ' * (width - len(b)) for b in board]
    return board


def process_instructions(instructions_str: str) -> list[Union[str, int]]:
    """Turn a raw instructions string into a list of instructions."""
    instructions_str = instructions_str.strip()
    result: list[Union[str, int]] = []
    index = 0
    while index < len(instructions_str):
        if instructions_str[index] in 'LR':
            result.append(instructions_str[index])
            index += 1
        else:
            for end in range(index, len(instructions_str) + 1):
                if end < len(instructions_str) and instructions_str[end] in 'LR':
                    break
            result.append(int(instructions_str[index:end]))
            index = end
    return result


def mirror_connections(connections: dict[tuple[int, int, str], tuple[int, int, str]],
                       ) -> dict[tuple[int, int, str], tuple[int, int, str]]:
    """Fill in the connections in the other direction."""
    return connections | {
        (r1, c1, FACINGS[(FACINGS.index(f1) + 2) % len(FACINGS)]): (
            r0, c0, FACINGS[(FACINGS.index(f0) + 2) % len(FACINGS)]
        )
        for (r0, c0, f0), (r1, c1, f1) in connections.items()
    }


def step(row: int, column: int, facing: str, board: list[str],
         connections: dict[tuple[int, int, str], tuple[int, int, str]], instruction: Union[str, int],
         ) -> tuple[int, int, str]:
    """Update the position based on the instruction."""
    if instruction == 'L':
        return row, column, FACINGS[(FACINGS.index(facing) - 1) % len(FACINGS)]
    if instruction == 'R':
        return row, column, FACINGS[(FACINGS.index(facing) + 1) % len(FACINGS)]
    if not isinstance(instruction, int):
        raise ValueError('That was weird')
    for _ in range(instruction):
        new_row = row
        new_column = column
        new_facing = facing
        if (row, column, facing) in connections:
            new_row, new_column, new_facing = connections[row, column, facing]
        elif facing == '>':
            new_column = column + 1
        elif facing == 'v':
            new_row = row + 1
        elif facing == '<':
            new_column = column - 1
        elif facing == '^':
            new_row = row - 1
        if board[new_row][new_column] == '#':
            break
        row = new_row
        column = new_column
        facing = new_facing
    return row, column, facing


def password(row: int, column: int, facing: str) -> int:
    """Calculate password value."""
    return 1000 * (row + 1) + 4 * (column + 1) + FACING_VALUES[facing]
