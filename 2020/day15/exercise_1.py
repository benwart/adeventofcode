#!/usr/bin/env python3

from collections import deque

inputs = [
    {"numbers": [0, 3, 6], "answer": 436},
    {"numbers": [1, 3, 2], "answer": 1},
    {"numbers": [2, 1, 3], "answer": 10},
    {"numbers": [1, 2, 3], "answer": 27},
    {"numbers": [2, 3, 1], "answer": 78},
    {"numbers": [3, 2, 1], "answer": 438},
    {"numbers": [3, 1, 2], "answer": 1836},
    {"numbers": [12, 1, 16, 3, 11, 0], "answer": None},
]

input = inputs[-1]
stop = 2020

history = {}
last_said = None

turn = 1
for i in input["numbers"]:
    if i not in history:
        history[i] = deque([turn], maxlen=2)
    else:
        history[i].append(turn)

    last_said = i
    turn += 1

for i in range(turn, stop + 1):
    h = history[last_said]
    if len(h) == 1:
        last_said = 0
    else:
        last_said = h[1] - h[0]

    if last_said not in history:
        history[last_said] = deque([i], maxlen=2)
    else:
        history[last_said].append(i)

    if i == stop:
        if input["answer"]:
            print(f"{('FAIL', 'PASS')[input['answer']==last_said]}")
        print(last_said)
