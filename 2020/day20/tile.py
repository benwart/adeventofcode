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

        # set of edges will never change as this is used to
        # determine matches with other images
        self.edges = set([self.right, self.top, self.left, self.bottom])

    @property
    def right(self):
        return Edge(self.tile_id, self.image[:, -1])

    @property
    def top(self):
        return Edge(self.tile_id, self.image[0])

    @property
    def left(self):
        return Edge(self.tile_id, self.image[:, 0])

    @property
    def bottom(self):
        return Edge(self.tile_id, self.image[-1])

    @property
    def cropped(self):
        return self.image[1:-1, 1:-1]

    def __repr__(self):
        return f"{self.tile_id}"

    def __hash__(self):
        return self.tile_id

    def print(self):
        print_array(self.image)

    def match_edges(self, other):
        return self.edges.intersection(other.edges)

    def get_matching_edge(self, other):
        return {
            self.right: self.right,
            self.top: self.top,
            self.left: self.left,
            self.bottom: self.bottom,
        }[other]

    def get_matching_side(self, other):
        return {
            self.right: "right",
            self.top: "top",
            self.left: "left",
            self.bottom: "bottom",
        }[other]

    def apply_transform(self, transforms):
        for t in transforms:
            self.image = t(self.image)


if __name__ == "__main__":
    from parser import parse_input

    tiles = [t for t in parse_input("./data/example1")]
