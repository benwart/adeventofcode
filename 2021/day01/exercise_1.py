#!/usr/bin/env python3


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield int(line.rstrip())


last = None
deeper = 0
for depth in parse_lines("./2021/day01/data/full"):
    if last is None:
        last = depth
        continue

    if last < depth:
        deeper += 1

    last = depth


print(f"Deeper Count: {deeper}")
