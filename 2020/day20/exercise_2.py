#!/usr/bin/env python3

import numpy as np
from collections import defaultdict
from collections import namedtuple
from math import prod, sqrt
from parser import parse_input
from tile import print_array

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
    "top-top": [lambda m: np.rot90(m, k=2)],
    "top-right": [lambda m: np.rot90(m, k=3)],
    "top-left": [lambda m: np.rot90(m, k=1)],
    "right-top": [lambda m: np.rot90(m, k=1)],
    "right-right": [lambda m: np.rot90(m, k=2)],
    "right-bottom": [lambda m: np.rot90(m, k=3)],
    "bottom-right": [lambda m: np.rot90(m, k=1)],
    "bottom-bottom": [lambda m: np.rot90(m, k=2)],
    "bottom-left": [lambda m: np.rot90(m, k=3)],
    "left-top": [lambda m: np.rot90(m, k=1)],
    "left-bottom": [lambda m: np.rot90(m, k=3)],
    "left-left": [lambda m: np.rot90(m, k=2)],
}


def calculate_transforms(static_side, other_side):
    transforms = []
    key = f"{static_side}-{other_side}"

    if key in transforms_sides:
        transforms += transforms_sides[key]

    return transforms


def transform_first_corner(tile, matches):
    for m in matches:
        edge = tile.get_matching_edge(m.edge)
        side = tile.get_matching_side(edge)

        debug = [side]
        if side == "top":
            debug.append(" -> bottom")
            tile.apply_transform([np.flipud])
        elif side == "left":
            debug.append(" -> right")
            tile.apply_transform([np.fliplr])

        # print("".join(debug))


def find_side_tile(tile_matches, side):
    tile, matches = tile_matches
    side_tile = {tile.get_matching_side(match.edge): match for match in matches}

    # print(f"{tile}: {side_tile}")

    return side_tile[side] if side in side_tile else None


def place_side_tile(coords, current, side):
    global matches
    global remaining

    match_side = find_side_tile(current, side)
    if match_side and match_side.tile in remaining:
        tile, edge = match_side
        cedge = current.tile.get_matching_edge(edge)
        oside = tile.get_matching_side(edge)

        transforms = calculate_transforms(side, oside)
        tile.apply_transform(transforms)

        oside = tile.get_matching_side(edge)

        # check for reversed edge

        if side == "right":
            oedge = tile.left
            ocoords = Coordinates(y=coords.y, x=coords.x + 1)
        else:
            oedge = tile.top
            ocoords = Coordinates(y=coords.y + 1, x=coords.x)

        # now that we have the sides matched up reverse the new side if needed
        rev = oedge.reversed(cedge)
        if rev:
            tile.apply_transform([transform_reverse[side]])

        mosaic_layout[ocoords.y, ocoords.x] = tile.tile_id

        # print(mosaic_layout)

        place_tiles(ocoords, TileMatches(tile, matches[tile]))


def place_tiles(coords, current):
    global remaining

    remaining.remove(current.tile)
    # loop through edges starting with down then right...
    # shouldn't need to do top or left in this case
    place_side_tile(coords, current, "right")
    place_side_tile(coords, current, "bottom")


def count_waves_not_monsters(mosaic):
    monster = np.array(
        (
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        ),
        dtype=np.int,
    )
    monster_pos = {(y, x) for y, x in zip(*np.where(monster == 1))}
    monster_shape = Coordinates(*monster.shape)
    image_shape = Coordinates(*mosaic.shape)

    monster_found = False
    for i in range(8):
        all_rough_water_pos = {(y, x) for y, x in zip(*np.where(mosaic == 1))}
        for y in range(image_shape.y - monster_shape.y):
            for x in range(image_shape.x - monster_shape.x):
                cropped = mosaic[y : y + monster_shape.y, x : x + monster_shape.x]
                rough_water_pos = set()
                for cy, row in enumerate(cropped):
                    for cx, char in enumerate(row):
                        if char == 1:
                            rough_water_pos.add((cy, cx))
                if monster_pos.issubset(rough_water_pos):
                    monster_found = True
                    for y_, x_ in monster_pos & rough_water_pos:
                        pos = (y + y_, x + x_)
                        all_rough_water_pos.remove(pos)
        if monster_found:
            break
        mosaic = np.rot90(mosaic)
        if i == 4:
            mosaic = np.flip(mosaic, 1)
    return len(all_rough_water_pos)


tiles = {t.tile_id: t for t in parse_input("./data/full")}

side_length = int(sqrt(len(tiles)))
matches = match_edges(list(tiles.values()))

# keep track of tiles that haven't been added to layout
remaining = set(matches.keys())
mosaic_layout = np.zeros((side_length, side_length))

# need to find a corner and transform (starting in upper left)
corners = [
    TileMatches(t, matches) for t, matches in matches.items() if len(matches) == 2
]
current = corners[0]
current_coords = Coordinates(0, 0)
transform_first_corner(*current)

mosaic_layout[current_coords.y, current_coords.x] = current.tile.tile_id

place_tiles(Coordinates(0, 0), current)

print(mosaic_layout, "\n")

# generate full mosaic image

# all the tiles should be transformed to final layout orientations
cropped_shape = Coordinates(*list(tiles.values())[0].cropped.shape)
mosaic_layout_shape = Coordinates(*mosaic_layout.shape)

dims = [
    cropped_shape,
    mosaic_layout_shape,
]

mosaic_shape = Coordinates(*(prod(i) for i in zip(*(d for d in dims))))

print(mosaic_shape, "\n")
mosaic = np.zeros(mosaic_shape, dtype=np.int)

for y, row in enumerate(mosaic_layout):
    y_start = y * cropped_shape.y
    y_end = y_start + cropped_shape.y

    for x, col in enumerate(row):
        x_start = x * cropped_shape.x
        x_end = x_start + cropped_shape.x

        window = mosaic[y_start:y_end, x_start:x_end]
        window[: cropped_shape.y, : cropped_shape.x] = tiles[
            mosaic_layout[y, x]
        ].cropped


wave_count = count_waves_not_monsters(mosaic)

print(wave_count)
