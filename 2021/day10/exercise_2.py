#!/usr/bin/env python3

from statistics import median
from collections import deque
from parser import parse_strs

points = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

az = {
    "(": ")",
    "{": "}",
    "[": "]",
    "<": ">",
}

a = set("({[<")
z = set(")}]>")

scores = []

for line in parse_strs("./2021/day10/data/full"):
    try:
        state = deque()
        ssize = 0
        score = 0

        for i in range(0, len(line)):
            c = line[i]
            if c in a:
                state.append(c)
                ssize += 1
            elif c in z:
                if i == 0:
                    raise SyntaxError(c)

                l = state.pop()
                ssize -= 1
                check = az[l]
                if not check == c:
                    raise SyntaxError(c)
        
        # score imcomplete lines
        while ssize > 0:
            l = state.pop()
            ssize -= 1

            score *= 5
            score += points[l]

        
    except SyntaxError:
        # skip invalid lines
        pass
    
    if score:
        scores.append(score)
        print(f"line: {line} score: {score}")

print(f"score = {median(scores)}")
