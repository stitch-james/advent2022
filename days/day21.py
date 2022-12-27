"""Day 21."""

import utils


def process_monkey(row: str) -> tuple[str, dict]:
    """Return the details of a monkey."""
    name, operation = row.split(': ')
    for op in '+-*/':
        if op in operation:
            return name, {'operation': op, 'operands': operation.split(f' {op} ')}
    return name, {'operation': 'number', 'number': int(operation)}


INPUT_OPTIONS = utils.InputOptions(
    processor=process_monkey,
)


def part1(monkeys_list: list[tuple[str, dict]]) -> int:
    """Day 21, part 1."""
    monkeys = dict(monkeys_list)
    return calculate_monkey(monkeys, 'root')


def part2(monkeys_list: list[tuple[str, dict]]) -> int:
    """Day 21, part 2."""
    monkeys = dict(monkeys_list)
    monkeys['humn'] = {'operation': 'number'}
    try:
        target = calculate_monkey(monkeys, monkeys['root']['operands'][0])
        name_top = monkeys['root']['operands'][1]
    except KeyError:
        target = calculate_monkey(monkeys, monkeys['root']['operands'][1])
        name_top = monkeys['root']['operands'][0]
    return inverse_calculate(monkeys, name_top, target, 'humn')


def calculate_monkey(monkeys: dict[str, dict], name: str) -> int:
    """Return what the named monkey will shout."""
    monkey = monkeys[name]
    if 'number' in monkey:
        return monkey['number']
    monkey_a, monkey_b = monkey['operands']
    if monkey['operation'] == '+':
        return calculate_monkey(monkeys, monkey_a) + calculate_monkey(monkeys, monkey_b)
    if monkey['operation'] == '-':
        return calculate_monkey(monkeys, monkey_a) - calculate_monkey(monkeys, monkey_b)
    if monkey['operation'] == '*':
        return calculate_monkey(monkeys, monkey_a) * calculate_monkey(monkeys, monkey_b)
    if monkey['operation'] == '/':
        return int(calculate_monkey(monkeys, monkey_a) / calculate_monkey(monkeys, monkey_b))
    raise ValueError('Bad monkey!')


def inverse_calculate(monkeys: dict[str, dict], name_top: str, target: int, name_bottom: str) -> int:
    """Work backwards to find what name_bottom should call out."""
    if name_top == name_bottom:
        return target
    monkey_top = monkeys[name_top]
    try:
        value = calculate_monkey(monkeys, monkey_top['operands'][0])
        if monkey_top['operation'] == '+':
            new_target = target - value
        elif monkey_top['operation'] == '-':
            new_target = value - target
        elif monkey_top['operation'] == '*':
            new_target = int(target / value)
        elif monkey_top['operation'] == '/':
            new_target = int(value / target)
        else:
            raise ValueError('Bad monkey!')
        new_name_top = monkey_top['operands'][1]
    except KeyError:
        value = calculate_monkey(monkeys, monkey_top['operands'][1])
        if monkey_top['operation'] == '+':
            new_target = target - value
        elif monkey_top['operation'] == '-':
            new_target = target + value
        elif monkey_top['operation'] == '*':
            new_target = int(target / value)
        elif monkey_top['operation'] == '/':
            new_target = value * target
        else:
            raise ValueError('Bad monkey!')
        new_name_top = monkey_top['operands'][0]
    return inverse_calculate(monkeys, new_name_top, new_target, name_bottom)
