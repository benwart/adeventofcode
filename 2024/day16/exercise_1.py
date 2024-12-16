#!/usr/bin/env python

from dataclasses import InitVar, dataclass, field
from heapq import heappop, heappush
from pathlib import Path
from typing import Iterable


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
class Location:
    x: int
    y: int
    direction: str


@dataclass
class Node:
    finish: InitVar[tuple[int, int]]

    l: Location
    parent: "Node" = None

    score: int = field(init=False, default=0)
    turns: int = field(init=False, default=0)

    g: int = field(init=False, default=0)
    h: int = field(init=False, default=0)
    f: int = field(init=False, default=0)

    def __post_init__(self, finish: tuple[int, int]) -> None:
        # handle the start using defaults...everyone else gets updated
        if self.parent is not None:
            self.turns = TURNS_MAP[(self.parent.l.direction, self.l.direction)]
            self.score = self.parent.score + (self.turns * 1000) + 1

            fx, fy = finish

            self.g = self.score
            self.h = (self.l.x - fx) ** 2 + (self.l.y - fy) ** 2
            self.f = self.g + self.h

    def __eq__(self, other: "Node") -> bool:
        return self.l.x == other.l.x and self.l.y == other.l.y and self.l.direction == other.l.direction

    def __lt__(self, other: "Node"):
        return self.f < other.f


@dataclass
class Maze:
    start: Location = field(init=False)
    end: tuple[int, int] = field(init=False)
    grid: list[str] = field(init=False, default_factory=list)

    def add_line(self, line: str) -> None:
        y: int = len(self.grid)
        for x, c in enumerate(line):
            if c == "S":
                self.start = Location(x, y, ">")
            elif c == "E":
                self.end = (x, y)

        self.grid.append(line)

    def at(self, l: Location) -> str:
        return self.grid[l.y][l.x]

    def print(self) -> str:
        return "\n".join(self.grid)


NEIGHBOR_SKIP: set[tuple[str, str]] = set(
    [
        (">", "<"),
        ("<", ">"),
        ("^", "v"),
        ("v", "^"),
    ]
)


def get_neighbors(maze: Maze, cur: Node) -> Iterable[Location]:
    neighbors: list[Location] = [
        Location(cur.l.x - 1, cur.l.y, "<"),
        Location(cur.l.x + 1, cur.l.y, ">"),
        Location(cur.l.x, cur.l.y - 1, "^"),
        Location(cur.l.x, cur.l.y + 1, "v"),
    ]

    for n in neighbors:
        # if this isn't the start skip backtracks
        if cur.parent is not None:
            if (cur.l.direction, n.direction) in NEIGHBOR_SKIP:
                continue

        # if the new location is a wall skip
        if maze.at(n) == "#":
            continue

        yield n


def astar(maze: Maze) -> int | None:
    open: list[Node] = []
    closed: list[Node] = []

    start: Node = Node(maze.end, maze.start)
    heappush(open, start)

    while len(open) > 0:
        # Get the current node
        cur: Node = heappop(open)

        # add to closed list
        closed.append(cur)

        # Check if we have reached the goal
        if cur.l.x == maze.end[0] and cur.l.y == maze.end[1]:
            return cur.score

        # Loop through children
        for n in get_neighbors(maze, cur):
            neigh: Node = Node(maze.end, n, cur)

            # Child is on the closed list
            if neigh in closed:
                continue

            # Child is already in the open list
            if neigh in closed:
                continue

            # Add the child to the open list
            heappush(open, neigh)

    return None


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    maze: Maze = Maze()
    for line in parse_lines(filepath):
        maze.add_line(line)

    lowest: int | None = astar(maze)
    print(lowest)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
