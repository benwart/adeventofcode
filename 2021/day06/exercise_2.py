#!/usr/bin/env python3

from collections import deque

from parser import parse_strs

full = map(int, next(parse_strs("./2021/day06/data/full")).split(","))
d = deque([0] * 9)

# store the sum of the ages (histogram style)
for i in full:
    d[i] += 1


for _ in range(256):
    # for each day rotate d (0 -> 8)
    d.append(d.popleft())

    # add all the 8s to the 6s
    d[6] += d[-1]

print(sum(d))

