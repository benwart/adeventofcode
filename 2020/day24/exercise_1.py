#!/usr/bin/env python3

from collections import defaultdict
from parser import parse_input

tiles = defaultdict(lambda: "white")

for direction in parse_input("./data/full"):
    coords = tuple(
        sum(i) for i in zip(*[t for t in map(lambda d: d.transform, direction)])
    )
    tiles[coords] = "black" if tiles[coords] == "white" else "white"

flipped = [side for side in tiles.values() if side == "black"]

print(f"Count of Tiles to Flip: {len(flipped)}")