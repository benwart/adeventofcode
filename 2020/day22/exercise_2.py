#!/usr/bin/env python3

from collections import deque
from parser import parse_input


def play_game(cards0, cards1):
    rounds = set()
    while len(cards0) > 0 and len(cards1) > 0:
        if (calculate_score(cards0), calculate_score(cards1)) in rounds:
            return 0, cards0

        rounds.add((calculate_score(cards0), calculate_score(cards1)))

        c0, c1 = cards0.pop(), cards1.pop()
        if len(cards0) >= c0 and len(cards1) >= c1:
            winner, _ = play_game(deque(list(cards0)[-c0:]), deque(list(cards1)[-c1:]))
        else:
            winner = (1, 0)[c0 > c1]
        if winner == 0:
            cards0.appendleft(c0)
            cards0.appendleft(c1)
        else:
            cards1.appendleft(c1)
            cards1.appendleft(c0)

        winner = 0 if len(cards1) == 0 else 1

    return winner, cards0 if winner == 0 else cards1


def calculate_score(cards):
    return sum([(i + 1) * card for i, card in enumerate(cards)])


players = parse_input("./data/full")
cards0, cards1 = players[0]["cards"], players[1]["cards"]

winner, cards = play_game(cards0, cards1)
score = calculate_score(cards)

print(f"Winner is Player {winner + 1} (Score: {score})")
