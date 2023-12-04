#!/usr/bin/env python

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Game:
    id: int
    winners: list[int]
    numbers: list[int]

    def points(self) -> int:
        wins = len([n for n in self.numbers if n in self.winners])
        return pow(2, wins - 1) if wins > 0 else 0


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_game(filepath: Path) -> Iterable[Game]:
    for line in parse_lines(filepath):
        id = line[line.index(":") - 1]
        raw_winners, raw_numbers = line.split(":")[1].split("|")
        yield Game(
            id,
            [int(w.strip()) for w in raw_winners.strip().split(" ") if w.strip() != ""],
            [int(n.strip()) for n in raw_numbers.strip().split(" ") if n.strip() != ""],
        )


def main(filepath: Path):
    total = 0
    for game in parse_game(filepath):
        print(f"Game {game.id} points: {game.points()}")
        total += game.points()

    print(f"Total points: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
