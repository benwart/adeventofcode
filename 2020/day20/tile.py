import numpy as np
from collections import namedtuple
from functools import cache


class Edge:
    def __init__(self, tile_id, edge):
        self.tile_id = tile_id
        self.edge = edge
        self.value = int("".join([str(c) for c in self.edge]))
        self.rvalue = int("".join([str(c) for c in reversed(self.edge)]))
        self.min = min(self.value, self.rvalue)

    def __repr__(self):
        return "".join([str(c) for c in self.edge])

    def __hash__(self):
        return self.min

    def __eq__(self, other):
        return hash(self) == hash(other)

    def print(self):
        print_array(self.edge)

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
        "left": Edge(tile_id, image[:, 0]),
        "right": Edge(tile_id, image[:, -1]),
    }
    return name_edge


print_mapping = {0: ".", 1: "#"}
print_keys = {"int": lambda n: print_mapping[n]}


def print_array(arr, end="\n"):
    np.set_printoptions(formatter=print_keys)
    print(arr, end=end)
    np.set_printoptions()


class Tile:
    def __init__(self, tile_id, image):
        self.tile_id = int(tile_id)
        self.raw = np.array(image)
        self.image = self.raw[:]
        self.cropped = self.image[1:-1, 1:-1]

        # initial edges, will change with transforms
        self.update_edges()

        # set of edges will never change as this is used to
        # determine matches with other images
        self.edges = set(self.edge_name.keys())

    def __repr__(self):
        return f"{self.tile_id}"

    def __hash__(self):
        return self.tile_id

    def print(self):
        print_array(self.image)

    def update_edges(self):
        self.name_edge = get_edges(self.tile_id, self.image)
        self.edge_name = swap_key_value(self.name_edge)

    def match_edges(self, other):
        return self.edges.intersection(other.edges)

    def get_matching_edge(self, other):
        matches = [e for e in self.edges if e == other]
        assert len(matches) > 0
        return matches[0]

    def get_matching_side(self, other):
        match = [self.get_matching_edge(e) for e in self.match_edges(other)][0]
        return self.edge_name[match]

    def apply_transform(self, transforms):
        for t in transforms:
            self.image = t(self.image)

        self.update_edges()