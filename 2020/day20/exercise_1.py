#!/usr/bin/env python3

from collections import defaultdict
from math import prod
from parser import parse_input

tiles = [t for t in parse_input("./data/full")]

matches = defaultdict(lambda: 0)

for i in range(0, len(tiles) - 1):
    t = tiles[i]
    for j in range(i + 1, len(tiles)):
        o = tiles[j]
        check = t.matched_edges(o)
        matches[t.tile_id] += check
        matches[o.tile_id] += check

        # if check:
        #     print(f"{t.tile_id} == {o.tile_id}")


corners = [m for m, c in matches.items() if c == 2]
print(prod(corners))