"""Day 11."""

import math
from typing import Callable, Iterator, Optional

import utils


class Monkey:
    """A monkey doing monkey business."""
    def __init__(self, description: str) -> None:
        """Initialise the monkey."""
        _, start_row, operation_row, test_row, true_row, false_row = description.split('\n')
        self.items = [
            int(item) for item in start_row.removeprefix('  Starting items: ').split(', ')
        ]
        self.increaser = get_increaser(operation_row)
        self.divider = int(test_row.split()[-1])
        self.if_true = int(true_row.split()[-1])
        self.if_false = int(false_row.split()[-1])
        self.n_inspected = 0
    
    def take_turn(self, manage_worry: bool, common_divider: Optional[int] = None) -> Iterator[tuple[int, int]]:
        """Take its turn, yielding thrown items."""
        for item in self.items:
            self.n_inspected += 1
            item = self.increaser(item)
            if manage_worry:
                item = int(item / 3)
            if common_divider is not None:
                item = item % common_divider
            if item % self.divider == 0:
                yield self.if_true, item
            else:
                yield self.if_false, item
        self.items = []


INPUT_OPTIONS = utils.InputOptions(
    processor=Monkey,
    process_as_group=True,
)


def get_increaser(operation_row: str) -> Callable[[int], int]:
    """Get the function to increase the worry level."""
    operator = operation_row.removeprefix('  Operation: new = old ')[0]
    if operator == '*':
        func = lambda x, y: math.prod([x, y])
    elif operator == '+':
        func = lambda x, y: sum([x, y])
    else:
        raise ValueError(f'Unrecognised operator: {operator}')

    operand = operation_row.split()[-1]
    if operand == 'old':
        increaser = lambda worry: func(worry, worry)
    else:
        operand_int = int(operand)
        increaser = lambda worry: func(worry, operand_int)

    return increaser


def part1(monkeys: list[Monkey]) -> int:
    """Day 11, part 1."""
    for _ in range(20):
        for monkey in monkeys:
            for target, item in monkey.take_turn(manage_worry=True):
                monkeys[target].items.append(item)

    return math.prod(sorted(monkey.n_inspected for monkey in monkeys)[-2:])


def part2(monkeys: list[Monkey]) -> int:
    """Day 11, part 2."""
    common_divider = math.prod(monkey.divider for monkey in monkeys)
    for _ in range(10000):
        for monkey in monkeys:
            for target, item in monkey.take_turn(manage_worry=False, common_divider=common_divider):
                monkeys[target].items.append(item)

    return math.prod(sorted(monkey.n_inspected for monkey in monkeys)[-2:])
