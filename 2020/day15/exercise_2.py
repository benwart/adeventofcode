#!/usr/bin/env python3

import numpy as np

inputs = [
    {"numbers": [0, 3, 6], "answer": 175594},
    {"numbers": [1, 3, 2], "answer": 2578},
    {"numbers": [2, 1, 3], "answer": 3544142},
    {"numbers": [1, 2, 3], "answer": 261214},
    {"numbers": [2, 3, 1], "answer": 6895259},
    {"numbers": [3, 2, 1], "answer": 18},
    {"numbers": [3, 1, 2], "answer": 362},
    {"numbers": [12, 1, 16, 3, 11, 0], "answer": None},
]

input = inputs[-1]
stop = 30000000

history = np.zeros(stop, dtype=int)
last_said = None

for turn, number in enumerate(input["numbers"]):
    history[last_said], last_said = turn, number

for turn in range(len(input["numbers"]), stop):
    history[last_said], last_said = turn, turn - history[last_said]

if input["answer"]:
    print(f"{('FAIL', 'PASS')[input['answer']==last_said]}")
print(last_said)
