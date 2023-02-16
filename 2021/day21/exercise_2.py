#!/usr/bin/env python3

# from: https://www.reddit.com/r/adventofcode/comments/rl6p8y/comment/hpe6bgn/?utm_source=share&utm_medium=web2x&context=3

from functools import cache

@cache
def getpossibilities(curplayerscore, otherscore, curplayerpos, otherplayerpos):
    if otherscore >= 21:
        return 0, 1
    wins, losses = 0, 0
    ROLLS = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    for roll, freq in ROLLS.items():
        newpos = (curplayerpos + roll - 1) % 10 + 1
        newlosses, newwins = getpossibilities(otherscore, curplayerscore + newpos, otherplayerpos, newpos) 
        wins += newwins * freq
        losses += newlosses * freq
    return wins, losses

print(getpossibilities(0, 0, 7, 8))