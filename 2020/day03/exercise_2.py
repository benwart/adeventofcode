#!/usr/bin/env python3

from math import prod

with open("./data") as f:
    map = [line.rstrip() for line in f]

width = len(map[0])


def hit_tree(row, col):
    # print(map[row][col % width], end="")
    return map[row][col % width] == "#"


def compute_slope(right, down):
    col = 0
    trees = 0
    for row in range(0, len(map), down):
        if hit_tree(row, col):
            trees += 1
        col += right
    return trees


inputs = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
outputs = []

for i in inputs:
    trees = compute_slope(*i)
    outputs.append(trees)

print(outputs)
print(prod(outputs))
