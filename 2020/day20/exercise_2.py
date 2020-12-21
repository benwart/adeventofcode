#!/usr/bin/env python3

import numpy as np
from collections import defaultdict
from collections import namedtuple
from math import sqrt
from parser import parse_input

MatchEdge = namedtuple("MatchEdge", "tile edge")
TileMatches = namedtuple("TileMatches", "tile matches")
Coordinates = namedtuple("Coordinates", "y x")


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
    "top": np.fliplr,
    "bottom": np.fliplr,
    "left": np.flipud,
    "right": np.flipud,
}


transforms_sides = {
    "top-top": [np.flipud],
    "top-right": [lambda m: np.rot90(m, k=3), np.fliplr],
    "top-left": [lambda m: np.rot90(m, k=1)],
    "right-top": [lambda m: np.rot90(m, k=1)],
    "right-right": [np.fliplr],
    "right-bottom": [lambda m: np.rot90(m, k=3), np.flipud],
    "bottom-right": [lambda m: np.rot90(m, k=1)],
    "bottom-bottom": [np.flipud],
    "bottom-left": [lambda m: np.rot90(m, k=3), np.fliplr],
    "left-top": [lambda m: np.rot90(m, k=1)],
    "left-bottom": [lambda m: np.rot90(m, k=3), np.flipud],
    "left-left": [np.fliplr],
}


def calculate_transforms(static_side, other_side, reversed):
    transforms = []
    key = f"{static_side}-{other_side}"

    if key in transforms_sides:
        transforms += transforms_sides[key]

    if reversed:
        transforms.append(transform_reverse[static_side])

    return transforms


def transform_first_corner(tile, matches):
    for m in matches:
        edge = tile.get_matching_edge(m.edge)
        side = tile.edge_name[edge]

        debug = [side]
        if side == "top":
            debug.append(" -> bottom")
            tile.apply_transform([np.flipud])
        elif side == "left":
            debug.append(" -> right")
            tile.apply_transform([np.fliplr])

        print("".join(debug))


def find_side_tile(tile_matches, side):
    global remaining

    side_tile = {
        tile_matches.tile.get_matching_side(match.tile): match
        for match in tile_matches.matches
    }

    return side_tile[side] if side in side_tile else None


def place_side_tile(coords, current, side):
    match_side = find_side_tile(current, side)
    if match_side:
        cedge = current.tile.get_matching_edge(match_side.edge)
        oedge = match_side.tile.get_matching_edge(match_side.edge)

        oside = match_side.tile.edge_name[oedge]
        rev = cedge.reversed(oedge)

        transforms = calculate_transforms(side, oside, rev)
        match_side.tile.apply_transform(transforms)

        if side == "right":
            ocoords = Coordinates(y=coords.y, x=coords.x + 1)
        else:
            ocoords = Coordinates(y=coords.y + 1, x=coords.x)

        mosaic_layout[ocoords.y, ocoords.x] = match_side.tile.tile_id
        place_tiles(ocoords, TileMatches(match_side.tile, matches[match_side.tile]))


def place_tiles(coords, current):
    global remaining

    remaining.remove(current.tile)
    # loop through edges starting with down then right...
    # shouldn't need to do top or left in this case
    place_side_tile(coords, current, "right")
    place_side_tile(coords, current, "bottom")


tiles = [t for t in parse_input("./data/example1")]
side_length = int(sqrt(len(tiles)))
matches = match_edges(tiles)

# keep track of tiles that haven't been added to layout
remaining = set(matches.keys())
mosaic_layout = np.zeros((side_length, side_length))

# debugging

# test = [t for t in tiles if t.tile_id == 1171][0]
# ms = matches[test]
# match = TileMatches(test, ms)
# right = find_side_tile(match, "right")
# print(right)
# test.apply_transform([lambda m: np.rot90(m, k=2)])
# right = find_side_tile(match, "right")
# print(right)


# need to find a corner and transform (starting in upper left)
corners = [
    TileMatches(t, matches) for t, matches in matches.items() if len(matches) == 2
]
current = corners[0]
current_coors = Coordinates(0, 0)
transform_first_corner(*current)

# how big is the mosaic...do I care?

mosaic_layout[current_coors.y, current_coors.x] = current.tile.tile_id

place_tiles(Coordinates(0, 0), current)

print(mosaic_layout)

# # generate full mosaic image
