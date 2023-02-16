#!/usr/bin/env python3

from functools import cache
from parser import parse_edges


class Node(object):
    def __init__(self, name: str):
        self.name = name
        self.edges = set()

    def add_edge(self, e: "Edge"):
        self.edges.add(e)

    @cache
    def is_limited(self) -> bool:
        return all(map(str.islower, self.name))

    def __eq__(self, other: "Node") -> bool:
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Node({str(self)})"

    def __str__(self):
        return self.name


class Edge(object):
    def __init__(self, n1:Node, n2:Node):
        self.nodes = { n1.name: n1, n2.name: n2 }
        n1.add_edge(self)
        n2.add_edge(self)

    def other_node(self, n: Node):
        n1, n2 = self.nodes.values()
        return n1 if n == n2 else n2

    def __hash__(self):
        n1, n2 = self.nodes
        return hash(f"{n1}-{n2}")

    def __repr__(self):
        return f"Edge({str(self)})"

    def __str__(self):
        n1, n2 = self.nodes
        return f"{n1}-{n2}"


class Path(object):
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes
        self.limited_visits = set([n for n in nodes if n.is_limited()])

    @property
    def head(self):
        return self.nodes[0]

    @property
    def tail(self):
        return self.nodes[-1]

    def add_node(self, n: Node):
        return Path(self.nodes + [n])

    def __eq__(self, __o: "Path") -> bool:
        return hash(self) == hash(__o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return f"Path({str(self)})"

    def __str__(self):
        return f"{','.join(map(str, self.nodes))}"


def load_data(filepath: str):
    nodes = dict()

    for edge in parse_edges(filepath):
        n1_name, n2_name = edge

        if n1_name not in nodes:
            nodes[n1_name] = Node(n1_name)

        if n2_name not in nodes:
            nodes[n2_name] = Node(n2_name)

        n1 = nodes[n1_name]
        n2 = nodes[n2_name]

        # assume no edges are duplicated

        e = Edge(n1, n2)

    return nodes


def follow_paths(p: Path, end: Node):
    # we found the end
    if p.tail == end:
        return set([p])
    
    # search other edges
    paths = set()
    for e in p.tail.edges:
        n = e.other_node(p.tail)

        if n not in p.limited_visits:
            # find longer paths
            paths |= follow_paths(p.add_node(n), end)
            # print(paths)

    # we've found all the paths
    return paths


if __name__ == "__main__":
    nodes = load_data("./2021/day12/data/full")
    paths = set()
        
    start = nodes["start"]
    end = nodes["end"]

    paths = follow_paths(Path([start]), end)

    print("\n".join(map(str, paths)))
    print(f"count: {len(paths)}")
