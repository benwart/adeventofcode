#!/usr/bin/env python3

from parser import parse_input


def play_round(player1, player2):
    p1 = player1.pop()
    p2 = player2.pop()

    if p1 > p2:
        player1.appendleft(p1)
        player1.appendleft(p2)
    else:
        player2.appendleft(p2)
        player2.appendleft(p1)


def game_over(player1, player2):
    if len(player1) == 0:
        return 1
    elif len(player2) == 0:
        return 0
    else:
        return -1


def calculate_score(cards):
    return sum([(i + 1) * card for i, card in enumerate(cards)])


players = parse_input("./data/full")
cards0 = players[0]["cards"]
cards1 = players[1]["cards"]

winner = -1
while winner == -1:
    play_round(cards0, cards1)
    winner = game_over(cards0, cards1)

score = calculate_score(players[winner]["cards"])

print(f"Winner is Player {winner + 1} (Score: {score})")
