#!/usr/bin/env python3

import numpy as np
from parser import parse_table

def get_neighbors(x, y, data):
    # top
    if y > 0:
        yield data[y-1, x]
    
    # left
    if x > 0:
        yield data[y, x-1]

    # bottom
    if y < data.shape[0]-1:
        yield data[y+1, x]

    # right
    if x < data.shape[1]-1:
        yield data[y, x+1]


data:np.array = parse_table("./2021/day09/data/full")

risk = 0
for (y,x), value in np.ndenumerate(data):
    if all(map(lambda n: n > value, get_neighbors(x, y, data))):
        risk += value+1
        print(f"({x},{y}) = {value} (risk: {value+1})")

print(f"total risk: {risk}")