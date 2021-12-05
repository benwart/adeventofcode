#!/usr/bin/env python3
#!/usr/bin/env python3

import numpy as np

from parser import parse_vent_lines

def print_array(arr):
    # print_mapping = {0: ".", 1: "#"}
    print_keys = {"int": lambda n: "." if n == 0 else str(n)}
    np.set_printoptions(formatter=print_keys)
    print(arr, end="\n\n")
    np.set_printoptions(formatter=None)


# make map
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
        vents += 1
    elif p1.y == p2.y:
        vents = map[p1.y, min(p1.x, p2.x):max(p1.x, p2.x)+1]
        vents += 1
    else:
        # get rect sub array that contains diagonal
        top = min(p1.y, p2.y)
        bottom = max(p1.y, p2.y)+1
        left = min(p1.x, p2.x)
        right = max(p1.x, p2.x)+1

        sub = map[top:bottom, left:right]

        dx = p2.x - p1.x
        dy = p2.y - p1.y

        # pick the right diagonal by rotating view
        if (dx < 0 and dy > 0) or \
           (dx > 0 and dy < 0):
            sub = np.fliplr(sub)

        # update the diagonal
        vents = sub.diagonal().copy()
        vents += 1
        np.fill_diagonal(sub, vents)

    # print(f"{p1} -> {p2}")
    # print_array(map)
    # print()

# compute all locations with at least 2 overlaps
print_array(map)
print(np.sum(map >= 2))