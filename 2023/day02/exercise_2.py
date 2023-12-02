#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class Draw:
    red: int
    blue: int
    green: int
    total: int = field(init=False)

    def __post_init__(self):
        self.total = self.red + self.blue + self.green


@dataclass
class Game:
    raw: str
    number: int
    draws: Iterable[Draw]

    def max_red(self) -> int:
        return max([d.red for d in self.draws])

    def max_blue(self) -> int:
        return max([d.blue for d in self.draws])

    def max_green(self) -> int:
        return max([d.green for d in self.draws])

    def max_total(self) -> int:
        return max([d.total for d in self.draws])

    def power(self) -> int:
        return self.max_red() * self.max_blue() * self.max_green()

    def valid_game(self, red: int, blue: int, green: int) -> bool:
        if self.max_red() > red or self.max_blue() > blue or self.max_green() > green:
            return False

        if self.max_total() > red + blue + green:
            return False

        return True


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_draws(draws: str) -> Iterable[Draw]:
    for draw in (d.strip() for d in draws.split(";")):
        red = 0
        blue = 0
        green = 0

        cubes = [c.strip().split(" ") for c in draw.split(",")]

        for cube in cubes:
            if cube[1] == "red":
                red = int(cube[0])
            elif cube[1] == "blue":
                blue = int(cube[0])
            elif cube[1] == "green":
                green = int(cube[0])

        yield Draw(red, blue, green)


def parse_games(filepath: Path) -> Iterable[Game]:
    for line in parse_lines(filepath):
        raw_game, raw_draws = [p.strip() for p in line.split(":")]

        game_number = int(raw_game.split(" ")[1])
        draws = list(parse_draws(raw_draws))

        yield Game(line, game_number, draws)


if __name__ == "__main__":
    total = 0
    for game in parse_games(Path("2023/day02/data/full")):
        total += game.power()

    print(f"Sum of game powers: {total}")
