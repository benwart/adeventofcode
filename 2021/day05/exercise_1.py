#!/usr/bin/env python3

import numpy as np

from parser import parse_vent_lines

# make map of size 1000, 1000
size = 1000
s = (size,size)
map = np.zeros(s, dtype=int)

# read each vent line
for l in parse_vent_lines("./2021/day05/data/full"):

    p1 = l[0]
    p2 = l[1]

    # only deal with non-diagonal lines
    if p1.x == p2.x:
        vents = map[min(p1.y, p2.y):max(p1.y, p2.y)+1, p1.x]
    elif p1.y == p2.y:
        vents = map[p1.y, min(p1.x, p2.x):max(p1.x, p2.x)+1]
    else:
        continue
    
    # update map: increntment all coordinates in vent line
    vents += 1
    # print(vents)

    # print(map)

# compute all locations with at least 2 overlaps
print(map)
print(np.sum(map >= 2))