#!/usr/bin/env python3

from parser import parse_instructions

x = 0
d = 0
a = 0

print(f"horizontal: {x}, depth: {d}")
for line in parse_instructions("./2021/day02/data/full"):
    op = line["op"]
    value = line["value"]

    if op == "forward":
        x += value
        d += a * value
    if op == "up":
        a -= value
    if op == "down":
        a += value

    print(f"horizontal: {x}, depth: {d}")

print(f"answer: {x * d}")