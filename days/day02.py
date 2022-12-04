"""Day 2."""

import enum

import utils


class Options(enum.Enum):
    ROCK = enum.auto()
    PAPER = enum.auto()
    SCISSORS = enum.auto()


class Outcomes(enum.Enum):
    WIN = enum.auto()
    DRAW = enum.auto()
    LOSE = enum.auto()


letters_p1 = {
    'A': Options.ROCK,
    'B': Options.PAPER,
    'C': Options.SCISSORS,
    'X': Options.ROCK,
    'Y': Options.PAPER,
    'Z': Options.SCISSORS,
}

letters_p2 = {
    **letters_p1,
    'X': Outcomes.LOSE,
    'Y': Outcomes.DRAW,
    'Z': Outcomes.WIN,
}

beats = {
    Options.ROCK: Options.SCISSORS,
    Options.SCISSORS: Options.PAPER,
    Options.PAPER: Options.ROCK,
}

scores_options = {
    Options.ROCK: 1,
    Options.PAPER: 2,
    Options.SCISSORS: 3,
}

scores_outcomes = {
    Outcomes.WIN: 6,
    Outcomes.DRAW: 3,
    Outcomes.LOSE: 0,
}


def part1() -> int:
    """Day 2, part 1."""
    strategy = utils.read_input(day=2, processor=lambda row: [letters_p1[char] for char in row.split()])
    return sum(score(theirs, mine) for theirs, mine in strategy)


def part2() -> int:
    """Day 2, part 2."""
    strategy = utils.read_input(day=2, processor=lambda row: [letters_p2[char] for char in row.split()])
    return sum(score(theirs, select_option(theirs, desired)) for theirs, desired in strategy)


def score(theirs: Options, mine: Options) -> int:
    """Calculate the score for a single round."""
    outcome = Outcomes.WIN if beats[mine] == theirs else Outcomes.DRAW if mine == theirs else Outcomes.LOSE
    return scores_outcomes[outcome] + scores_options[mine]


def select_option(theirs: Options, desired: Outcomes) -> Options:
    """Select the option that produces the desired outcome."""
    for option in Options:
        if beats[option] == theirs and desired == Outcomes.WIN:
            return option
        if option == theirs and desired == Outcomes.DRAW:
            return option
        if beats[theirs] == option and desired == Outcomes.LOSE:
            return option
    raise RuntimeError('Uh-oh')
