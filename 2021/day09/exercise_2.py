#!/usr/bin/env python3

import math
import numpy as np

from collections import deque
from parser import parse_table

def get_neighbors(x, y, data):
    # top
    if y > 0:
        yield (x, y-1,), data[y-1, x]
    
    # left
    if x > 0:
        yield (x-1, y,), data[y, x-1]

    # bottom
    if y < data.shape[0]-1:
        yield (x, y+1,), data[y+1, x]

    # right
    if x < data.shape[1]-1:
        yield (x+1, y,), data[y, x+1]


def scan_basin(start_x, start_y, data):
    pos = (start_x, start_y,)
    basin = set([pos])
    queue = deque([pos])
    qsize = 1

    # scan neighbors and add to list until we run out
    while qsize > 0:
        cx, cy = queue.popleft()
        qsize -= 1
        for (nx, ny), value in get_neighbors(cx, cy, data):
            pos = (nx, ny,)
            if value < 9 and pos not in basin:
                basin.add(pos)
                queue.append(pos)
                qsize += 1
    
    # count basin elements as size
    return len(basin)


data:np.array = parse_table("./2021/day09/data/full")

basin_sizes = []

for (y,x), value in np.ndenumerate(data):
    if all(map(lambda n: n[1] > value, get_neighbors(x, y, data))):
        size = scan_basin(x, y, data)
        basin_sizes.append(size)
        print(f"({x},{y}) = size: {size}")

# sort basin sizes
basin_sizes.sort(reverse=True)

# multiply the top three
print(f"top 3 product: {math.prod(basin_sizes[0:3])}")
