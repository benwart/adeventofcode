#!/usr/bin/env python3

from collections import defaultdict
from parser import parse_input


def exercise_1(filepath):
    tiles = defaultdict(lambda: "white")

    for direction in parse_input(filepath):
        coords = tuple(
            sum(i) for i in zip(*[t for t in map(lambda d: d.transform, direction)])
        )
        tiles[coords] = "black" if tiles[coords] == "white" else "white"

    return {coords: side for coords, side in tiles.items() if side == "black"}


if __name__ == "__main__":
    flipped = exercise_1("./data/full")
    print(f"Count of Tiles to Flip: {len(flipped)}")