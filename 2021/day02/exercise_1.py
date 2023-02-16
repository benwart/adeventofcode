#!/usr/bin/env python3

from parser import parse_instructions

x = 0
d = 0

print(f"horizontal: {x}, depth: {d}")
for line in parse_instructions("./2021/day02/data/full"):
    op = line["op"]
    value = line["value"]

    if op == "forward":
        x += value
    if op == "up":
        d -= value
    if op == "down":
        d += value

    print(f"horizontal: {x}, depth: {d}")

print(f"answer: {x * d}")