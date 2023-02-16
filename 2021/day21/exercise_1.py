#!/usr/bin/env python3

def roll_die(sides: int=100):
    last: int = 0
    while True:
        if last == 100:
            last = 0
        
        last += 1
        yield last


winner = None
rolls = 0
die = roll_die(sides=100)
players = {
    1: {
        "location": 7,
        "score": 0,
    },
    2: {
        "location": 8,
        "score": 0,
    },
}

while not winner:
    for i in players.keys():
        turn = 0
        for r in range(0, 3):
            rolls += 1
            turn += next(die)
        players[i]["location"] += turn
        players[i]["location"] %= 10
        if players[i]["location"] == 0:
            players[i]["location"] = 10

        players[i]["score"] += players[i]["location"]

        if players[i]["score"] >= 1000:
            winner = i
            break

losing_score = min(players.values(), key=lambda p: p['score'])["score"]

print(f"rolls: {rolls}")
print(f"losing score: {losing_score}")
print(f"output: {rolls * losing_score}")
