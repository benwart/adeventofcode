#!/usr/bin/env python3

with open("./data") as f:
    map = [line.rstrip() for line in f]

width = len(map[0])


def hit_tree(row, col):
    print(map[row][col % width], end="")
    return map[row][col % width] == "#"


col = 0
trees = 0
for row in range(0, len(map), 1):
    if hit_tree(row, col):
        trees += 1
    col += 3

print(f"\nTrees Hit: {trees}")
