import numpy as np
from collections import namedtuple

str_to_value = {
    ".": "0",
    "#": "1",
}


class Edge:
    def __init__(self, tile_id, edge):
        self.tile_id = tile_id
        self.edge = edge
        self.value = int("".join([str_to_value[n] for n in edge]))
        self.rvalue = int("".join([str_to_value[n] for n in reversed(edge)]))

    def __repr__(self):
        return self.edge

    def __hash__(self):
        return min(self.value, self.rvalue)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def reversed(self, other):
        assert self == other
        return self.rvalue == other.value


Edges = namedtuple("Edges", "top bottom left right")


def swap_key_value(d):
    return {v: k for k, v in d.items()}


def get_edges(tile_id, image):
    name_edge = {
        "top": Edge(tile_id, image[0]),
        "bottom": Edge(tile_id, image[-1]),
        "left": Edge(tile_id, "".join([row[0] for row in image])),
        "right": Edge(tile_id, "".join([row[-1] for row in image])),
    }
    return name_edge, swap_key_value(name_edge)


class Tile:
    def __init__(self, tile_id, image):
        self.tile_id = int(tile_id)
        self.image = np.array(image)
        self.name_edge, self.edge_name = get_edges(tile_id, image)
        self.edges = set(self.edge_name.keys())

    def match_edges(self, other):
        return self.edges.intersection(other.edges)

    def get_matching_edge(self, other):
        return [e for e in self.edge_name.keys() if e == other][0]

    def __repr__(self):
        return f"{self.tile_id}"