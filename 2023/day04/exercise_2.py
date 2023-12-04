#!/usr/bin/env python

from collections import deque
from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class Card:
    id: int
    winners: InitVar[list[int]]
    numbers: InitVar[list[int]]
    count: int = 1
    win: bool = field(init=False)
    win_cards: list[int] = field(init=False)

    def __post_init__(self, winners, numbers):
        wins = len([n for n in numbers if n in winners])
        self.win = wins > 0
        self.win_cards = [self.id + n for n in range(1, wins + 1)] if self.win else []


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_card(filepath: Path) -> Iterable[Card]:
    for line in parse_lines(filepath):
        id = int(line.split(":")[0].strip().split(" ")[-1])
        raw_winners, raw_numbers = line.split(":")[1].split("|")
        yield Card(
            id,
            [int(w.strip()) for w in raw_winners.strip().split(" ") if w.strip() != ""],
            [int(n.strip()) for n in raw_numbers.strip().split(" ") if n.strip() != ""],
        )


def main(filepath: Path):
    total = 0
    cards: dict[int, Card] = {c.id: c for c in parse_card(filepath)}
    queue: deque[Card] = deque([c for c in cards.values() if c.win])

    while len(queue) > 0:
        card = queue.popleft()

        for g in card.win_cards:
            winner = cards[g]
            winner.count += 1
            queue.append(winner)

    total = sum([c.count for c in cards.values()])

    print(f"Total cards: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
