#!/usr/bin/env python3

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
        history[i] = turn

    last_said = i
    turn += 1

for i in range(turn, stop + 1):
    saying = ((i - 1) - history[last_said]) if last_said in history else 0
    history[last_said] = i - 1
    last_said = saying

    if i == stop:
        if input["answer"]:
            print(f"{('FAIL', 'PASS')[input['answer']==last_said]}")
        print(last_said)
