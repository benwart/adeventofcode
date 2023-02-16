#!/usr/bin/env python3

import math


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield int(line.rstrip())


depths = list(parse_lines("./2021/day01/data/full"))

last = None
deeper = 0
for i in range(2, len(depths)):

    total = sum(depths[i - 2 : i + 1])
    print(f"sum = {total}")

    if last is not None and last < total:
        deeper += 1

    last = total

print(f"Deeper Count: {deeper}")
