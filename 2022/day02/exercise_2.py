#!/usr/bin/env python3

from enum import StrEnum, IntEnum


class Opponent(StrEnum):
    ROCK = "A"
    PAPER = "B"
    SCISSORS = "C"


class Player(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(StrEnum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


VALUES = {
    Outcome.LOSE: 0,
    Outcome.DRAW: 3,
    Outcome.WIN: 6,
}

OUTCOMES = {
    (Opponent.ROCK, Outcome.LOSE): Player.SCISSORS,
    (Opponent.ROCK, Outcome.DRAW): Player.ROCK,
    (Opponent.ROCK, Outcome.WIN): Player.PAPER,
    (Opponent.PAPER, Outcome.LOSE): Player.ROCK,
    (Opponent.PAPER, Outcome.DRAW): Player.PAPER,
    (Opponent.PAPER, Outcome.WIN): Player.SCISSORS,
    (Opponent.SCISSORS, Outcome.LOSE): Player.PAPER,
    (Opponent.SCISSORS, Outcome.DRAW): Player.SCISSORS,
    (Opponent.SCISSORS, Outcome.WIN): Player.ROCK,
}


def parse_lines(filepath: str):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_rounds(filepath: str):
    for line in parse_lines(filepath):
        opponent, outcome = line.split(" ")
        yield Opponent(opponent), Outcome(outcome)


def compute_outcome(opponent, outcome) -> int:
    return OUTCOMES[(opponent, outcome)] + VALUES[outcome]


def main():
    total = 0
    for opponent, outcome in parse_rounds("2022/day02/data/full"):
        result = compute_outcome(opponent, outcome)
        print(f"{opponent.name} - {outcome.name} == {result}")
        total += result

    print(f"total: {total}")


if __name__ == "__main__":
    main()
