#!/usr/bin/env python3

import math
import numpy as np

from collections import deque, namedtuple
from parser import parse_table

Point = namedtuple("Point", "x y")


def get_neighbors(p: Point, data: np.array):
    x,y = p

    # top-right
    if y > 0 and x < data.shape[1]-1:
        yield Point(x+1, y-1,), data[y-1, x+1]

    # top
    if y > 0:
        yield Point(x, y-1,), data[y-1, x]

    # top-left
    if y > 0 and x > 0:
        yield Point(x-1, y-1,), data[y-1, x-1]
    
    # left
    if x > 0:
        yield Point(x-1, y,), data[y, x-1]

    # bottom-left
    if y < data.shape[0]-1 and x > 0:
        yield Point(x-1, y+1,), data[y+1, x-1]

    # bottom
    if y < data.shape[0]-1:
        yield Point(x, y+1,), data[y+1, x]

    # bottom-right
    if y < data.shape[0]-1 and x < data.shape[1]-1:
        yield Point(x+1, y+1,), data[y+1, x+1]

    # right
    if x < data.shape[1]-1:
        yield Point(x+1, y,), data[y, x+1]


def flash_neighbors(p: Point, data: np.array):
    # update neighbors blindly
    for n, _ in get_neighbors(p, data):
        data[n.y, n.x] += 1


def new_flashes(data: np.array, flashes: set):


    return False


data:np.array = parse_table("./2021/day11/data/full")

print(f"Before any steps:")
print(data)

total_flashes = 0

for iteration in range(0,1000):
    flashes = set()

    # increase all cells by 1
    data += 1

    # continue until no more flashes
    while True:

        # iterate all cells larger than 9
        positions = np.nonzero(data > 9)

        # convert to Point namedtuple
        points = set()
        y, x = positions
        for i in range(0,x.shape[0]):
            points.add(Point(x[i], y[i]))

        # flash if not already flashed this iteration
        new_flashes = points - flashes

        for p in new_flashes:
            flashes.add(p)
            flash_neighbors(p, data)

        if len(new_flashes) == 0:
            break

        # capture count of new flashes
        total_flashes += len(new_flashes)

    # reset to zero any that flashed
    data[data > 9] = 0

    # check if they are all 0
    len_data = data.size
    count_zeros = np.count_nonzero(data == 0)
    not_zero = len_data - count_zeros
    if not_zero == 0:
        print(f"Found all zeros at iteration: {iteration+1}")
        print(data)
        break

    # print(f"\nAfter step {iteration+1}:")
    # print(data)

# print(f"total flashes: {total_flashes}")
