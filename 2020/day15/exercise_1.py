#!/usr/bin/env python3

from collections import defaultdict

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

history = defaultdict(lambda: turn)
last_said = None

for turn, number in enumerate(input["numbers"]):
    history[last_said], last_said = turn, number

for turn in range(len(input["numbers"]), stop):
    history[last_said], last_said = turn, turn - history[last_said]

if input["answer"]:
    print(f"{('FAIL', 'PASS')[input['answer']==last_said]}")
print(last_said)
