#!/usr/bin/env python3

import numpy as np
from collections import defaultdict
from collections import namedtuple
from parser import parse_input

MatchEdge = namedtuple("MatchEdge", "tile edge")

tiles = [t for t in parse_input("./data/example1")]


def match_edges(tiles):
    matches = defaultdict(list)

    for i in range(0, len(tiles) - 1):
        t = tiles[i]
        for j in range(i + 1, len(tiles)):
            o = tiles[j]
            edges = t.match_edges(o)
            for edge in edges:
                matches[t].append(MatchEdge(o, o.get_matching_edge(edge)))
                matches[o].append(MatchEdge(t, t.get_matching_edge(edge)))

    return matches


transform_reverse = {
    "top": np.fliplf,
    "bottom": np.fliplf,
    "left": np.flipud,
    "right": np.flipud,
}


transforms_sides = {
    "top-top": np.flipud,
    "top-right": lambda m: np.rot90(m, k=3),
    "top-left": lambda m: np.rot90(m, k=1),
    "right-top": lambda m: np.rot90(m, k=1),
    "right-right": np.fliplr,
    "right-bottom": lambda m: np.rot90(m, k=3),
    "bottom-right": lambda m: np.rot90(m, k=1),
    "bottom-bottom": np.flipud,
    "bottom-left": lambda m: np.rot90(m, k=3),
    "left-top": lambda m: np.rot90(m, k=1),
    "left-bottom": lambda m: np.rot90(m, k=3),
    "left-left": np.fliplr,
}


def calculate_transforms(static_side, other_side, reversed):
    transforms = []
    key = f"{static_side}-{other_side}"

    if key in transforms_sides:
        transforms.append(transforms_sides[key])

    if reversed:
        transforms.append(transform_reverse[static_side])

    return transforms


matches = match_edges(tiles)
for t, matches in matches.items():
    print(t)
    for m in matches:
        tedge = t.get_matching_edge(m.edge)
        oedge = m.tile.get_matching_edge(m.edge)

        tside = t.edge_name[tedge]
        oside = m.tile.edge_name[oedge]

        rev = t.get_matching_edge(m.edge).reversed(m.tile.get_matching_edge(m.edge))
        print(f" - {tside} {m.tile} {oside} reversed: {rev}")
