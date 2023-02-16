#!/usr/bin/env python3


from typing import Iterable
from dataclasses import dataclass, field, InitVar

from networkx import DiGraph, shortest_path, NetworkXNoPath


def parse_lines(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.strip()


@dataclass
class Point:
    y: int
    x: int
    value: InitVar[str]
    start: bool = field(init=False, default=False)
    end: bool = field(init=False, default=False)
    height: int = field(init=False)

    def __post_init__(self, value: str):
        if value == "S":
            value = "a"
            self.start = True

        if value == "E":
            value = "z"
            self.end = True

        self.height = ord(value) - ord("a")

    def coordinates(self) -> tuple[int, int]:
        return self.y, self.x

    def neighbors(self) -> list[tuple[int, int]]:
        return [
            (self.y + 1, self.x),
            (self.y, self.x + 1),
            (self.y - 1, self.x),
            (self.y, self.x - 1),
        ]

    def __hash__(self) -> int:
        return hash(self.coordinates())


def parse_points(filepath: str) -> Iterable[Point]:
    for y, line in enumerate(parse_lines(filepath)):
        for x, char in enumerate(line):
            yield Point(y, x, char)


def main():
    points = {}
    graph = DiGraph()
    s = None
    e = None

    # parse and add all points into graph and lookup dictionary
    for point in parse_points("2022/day12/data/full"):
        points[point.coordinates()] = point
        graph.add_node(point)

        if point.start:
            s = point

        if point.end:
            e = point

    # for each point lookup neighbors and add all possible edges
    for point in points.values():

        # make sure the neighbor exists and is <= 1 step higher
        neighbors = [n for n in point.neighbors()]

        # add all the valid neighbors
        for n in neighbors:
            if n not in points:
                continue

            neighbor = points[n]
            if neighbor.height <= point.height + 1:
                graph.add_edge(point, neighbor)

    # get list of starting locations
    lowest_points = [p for p in points.values() if p.height == 0]

    shortest_path_length = float("inf")
    for p in lowest_points:
        try:
            # traverse the graph and find the shortest path
            shortest = shortest_path(graph, p, e)
            shortest_path_length = int(min(len(shortest), shortest_path_length))
        except NetworkXNoPath as ex:
            pass

    # print(",".join([str(s.coordinates()) for s in shortest]))
    print(f"shortest path length = {shortest_path_length-1}")


if __name__ == "__main__":
    main()
