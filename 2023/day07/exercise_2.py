#!/usr/bin/env python

from collections import defaultdict
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Iterable


class HandQuality(IntEnum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


class CardValue(IntEnum):
    JOKER = 0
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
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
    "J": CardValue.JOKER,
    "Q": CardValue.QUEEN,
    "K": CardValue.KING,
    "A": CardValue.ACE,
}


def calculate_hand_quality(cards: list[CardValue]) -> HandQuality:
    no_jokers = [c for c in cards if c != CardValue.JOKER]
    jokers = len(cards) - len(no_jokers)

    grouped_cards = defaultdict(int)
    for c in no_jokers:
        grouped_cards[c] += 1

    # handle 5 jokers
    if jokers == 5:
        return HandQuality.FIVE_OF_A_KIND

    # add joker(s) to the group with the most cards
    largest_group = max(grouped_cards, key=grouped_cards.get)
    grouped_cards[largest_group] += jokers

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
    cards: list[CardValue]
    bid: int
    quality: HandQuality = field(init=False)

    def __post_init__(self):
        self.quality = calculate_hand_quality(self.cards)

    def __gt__(self, other: "Hand"):
        if self.quality != other.quality:
            return self.quality < other.quality

        else:
            for i in range(len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return self.cards[i] > other.cards[i]


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_hands(filepath: Path) -> Iterable[str]:
    for line in parse_lines(filepath):
        cards, bid = line.split(" ")
        yield Hand([char_to_card[c] for c in cards], int(bid))


def main(filepath: Path):
    hands = list(parse_hands(filepath))
    ranked = sorted(hands)

    for hand in ranked:
        print(f"{hand.cards} {hand.bid} {hand.quality.name}")

    total = sum((index + 1) * hand.bid for index, hand in enumerate(ranked))

    print(f"Sum of winnings: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
