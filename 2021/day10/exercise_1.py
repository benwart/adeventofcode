#!/usr/bin/env python3

from collections import deque
from parser import parse_strs

points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

az = {
    "(": ")",
    "{": "}",
    "[": "]",
    "<": ">",
}

a = set("({[<")
z = set(")}]>")
state = deque()
score = 0

for line in parse_strs("./2021/day10/data/full"):
    for i in range(0, len(line)):
        c = line[i]
        if c in a:
            state.append(c)
        elif c in z:
            if i == 0:
                score += points[c]
                break

            l = state.pop()
            check = az[l]
            if not check == c:
                score += points[c]
                break

print(f"score = {score}")
