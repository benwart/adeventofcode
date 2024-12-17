#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from networkx import DiGraph


TURNS_MAP: dict[tuple[str, str], int] = {
    # prior right
    (">", ">"): 0,
    (">", "^"): 1,
    (">", "<"): 2,
    (">", "v"): 1,
    # prior up
    ("^", "^"): 0,
    ("^", "<"): 1,
    ("^", "v"): 2,
    ("^", ">"): 1,
    # prior left
    ("<", "<"): 0,
    ("<", "v"): 1,
    ("<", ">"): 2,
    ("<", "^"): 1,
    # prior down
    ("v", "v"): 0,
    ("v", ">"): 1,
    ("v", "^"): 2,
    ("v", "<"): 1,
}


@dataclass
class Node:
    x: int
    y: int
    direction: str

    def tuple(self) -> tuple[int, int, str]:
        return (self.x, self.y, self.direction)

    def __eq__(self, other: "Node") -> bool:
        self.x == other.x and self.y == other.y and self.direction == other.direction

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.direction))

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.direction}"


@dataclass
class Edge:
    start: Node
    end: Node
    score: int


@dataclass
class Maze:
    start: Node = field(init=False)
    end: tuple[int, int] = field(init=False)
    grid: list[str] = field(init=False, default_factory=list)

    def add_line(self, line: str) -> None:
        y: int = len(self.grid)
        for x, c in enumerate(line):
            if c == "S":
                self.start = Node(x, y, ">")
            elif c == "E":
                self.end = (x, y)

        self.grid.append(line)

    def at(self, l: Node) -> str:
        return self.grid[l.y][l.x]

    def print(self) -> str:
        return "\n".join(self.grid)


# def get_neighbors(maze: Maze, cur: Node) -> Iterable[Location]:
#     neighbors: list[Location] = [
#         Location(cur.l.x - 1, cur.l.y, "<"),
#         Location(cur.l.x + 1, cur.l.y, ">"),
#         Location(cur.l.x, cur.l.y - 1, "^"),
#         Location(cur.l.x, cur.l.y + 1, "v"),
#     ]

#     for n in neighbors:
#         # if this isn't the start skip backtracks
#         if cur.parent is not None:
#             if (cur.l.direction, n.direction) in NEIGHBOR_SKIP:
#                 continue

#         # if the new location is a wall skip
#         if maze.at(n) == "#":
#             continue

#         yield n


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    maze: Maze = Maze()
    for line in parse_lines(filepath):
        maze.add_line(line)

    # create graph of entire maze with all possible moves
    graph: DiGraph = DiGraph()
    nodes: dict[tuple[int, int, str], Node] = {}
    node: Node

    # add nodes for all locations
    for y, row in enumerate(maze.grid):
        for x, c in enumerate(row):
            if c == "#":
                continue

            # make a node for all directions
            for d in ["<", ">", "^", "v"]:
                node = Node(x, y, d)
                nodes[node.tuple()] = node
                graph.add_node(node)

    # add edges for all locations with weight
    for i, node in nodes.items():
        for neighbor in [(node.x - 1, node.y, "<"), (node.x + 1, node.y, ">"), (node.x, node.y - 1, "^"), (node.x, node.y + 1, "v")]:
            if maze.at(Node(*neighbor)) == "#":
                continue

            other: Node = nodes[neighbor]
            weight: int = (TURNS_MAP[(node.direction, other.direction)] * 1000) + 1
            graph.add_edge(node, other, weight=weight)

    print(graph)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1")
