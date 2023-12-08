#!/usr/bin/env python

from collections import defaultdict
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Iterable


class HandQuality(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class CardValue(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


char_to_card = {
    "2": CardValue.TWO,
    "3": CardValue.THREE,
    "4": CardValue.FOUR,
    "5": CardValue.FIVE,
    "6": CardValue.SIX,
    "7": CardValue.SEVEN,
    "8": CardValue.EIGHT,
    "9": CardValue.NINE,
    "T": CardValue.TEN,
    "J": CardValue.JACK,
    "Q": CardValue.QUEEN,
    "K": CardValue.KING,
    "A": CardValue.ACE,
}


def calculate_hand_quality(cards: list[CardValue]) -> HandQuality:
    grouped_cards = defaultdict(int)
    for c in cards:
        grouped_cards[c] += 1

    if len(grouped_cards) == 1:
        return HandQuality.FIVE_OF_A_KIND

    if len(grouped_cards) == 2:
        if 4 in grouped_cards.values():
            return HandQuality.FOUR_OF_A_KIND
        return HandQuality.FULL_HOUSE

    if 3 in grouped_cards.values():
        return HandQuality.THREE_OF_A_KIND

    if len(grouped_cards) == 3:
        return HandQuality.TWO_PAIR

    if len(grouped_cards) == 4:
        return HandQuality.ONE_PAIR

    return HandQuality.HIGH_CARD


@dataclass
class Hand:
    cards: list[str]
    bid: int
    quality: HandQuality = field(init=False)

    def __post_init__(self):
        self.quality = calculate_hand_quality(self.cards)

    def __gt__(self, other: "Hand"):
        if self.quality != other.quality:
            return self.quality > other.quality

        else:
            for i in range(len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return self.cards[i] > other.cards[i]


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_hands(filepath: Path) -> Iterable[Hand]:
    for line in parse_lines(filepath):
        cards, bid = line.split(" ")
        yield Hand([char_to_card[c] for c in cards], int(bid))


def main(filepath: Path):
    hands = list(parse_hands(filepath))
    ranked = sorted(hands)
    total = sum((index + 1) * hand.bid for index, hand in enumerate(ranked))

    print(f"Sum of winnings: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
