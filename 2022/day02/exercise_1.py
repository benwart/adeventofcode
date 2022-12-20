#!/usr/bin/env python3

from enum import StrEnum, IntEnum


class Opponent(StrEnum):
    ROCK = "A"
    PAPER = "B"
    SCISSORS = "C"


class Player(StrEnum):
    ROCK = "X"
    PAPER = "Y"
    SCISSORS = "Z"


class Outcomes(IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6


VALUES = {
    Player.ROCK: 1,
    Player.PAPER: 2,
    Player.SCISSORS: 3,
}

OUTCOMES = {
    (Opponent.ROCK, Player.ROCK): Outcomes.DRAW,
    (Opponent.ROCK, Player.PAPER): Outcomes.WIN,
    (Opponent.ROCK, Player.SCISSORS): Outcomes.LOSE,
    (Opponent.PAPER, Player.ROCK): Outcomes.LOSE,
    (Opponent.PAPER, Player.PAPER): Outcomes.DRAW,
    (Opponent.PAPER, Player.SCISSORS): Outcomes.WIN,
    (Opponent.SCISSORS, Player.ROCK): Outcomes.WIN,
    (Opponent.SCISSORS, Player.PAPER): Outcomes.LOSE,
    (Opponent.SCISSORS, Player.SCISSORS): Outcomes.DRAW,
}


def parse_lines(filepath: str):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_rounds(filepath: str):
    for line in parse_lines(filepath):
        opponent, player = line.split(" ")
        yield Opponent(opponent), Player(player)


def compute_outcome(opponent, player) -> int:
    return OUTCOMES[(opponent, player)] + VALUES[player]


def main():
    total = 0
    for opponent, player in parse_rounds("2022/day02/data/full"):
        outcome = compute_outcome(opponent, player)
        print(f"{opponent.name} - {player.name} == {outcome}")
        total += outcome

    print(f"total: {total}")


if __name__ == "__main__":
    main()
