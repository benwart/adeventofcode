#!/usr/bin/env python

from collections import deque
from dataclasses import InitVar, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Iterable, Optional

from colorama import Style, Fore


@dataclass
class Point:
    y: int
    x: int

    def coords(self) -> tuple[int, int]:
        return self.y, self.x

    def __eq__(self, other: "Point") -> bool:
        if not isinstance(other, Point):
            return NotImplemented

        return self.coords() == other.coords()

    def __hash__(self) -> int:
        return hash(self.coords())

    def __repr__(self) -> str:
        return f"Point{str(self)}"

    def __str__(self) -> str:
        return f"({self.y},{self.x})"


class Direction(StrEnum):
    LEFT = "←"
    RIGHT = "→"
    UP = "↑"
    DOWN = "↓"


@dataclass
class Node:
    coords: Point
    loss: int
    parent: Optional["Node"]

    f: int = 0  # total_cost
    g: int = 0  # distance_to_start
    h: int = 0  # heuristic_to_goal

    def __post_init__(self):
        self.g = self.loss
        self.f = self.g + self.h

    def consecutive(self) -> int:
        if self.parent is None:
            return 0

        # compute for direction to check for consecutive steps that match
        current = self
        parent = current.parent
        direction = parent.direction(current)

        count = 1
        while True:
            # check the parent of the current node
            current = parent
            parent = current.parent

            # break if there is no parent
            if parent is None:
                break

            d = parent.direction(current)

            # break if the direction changes
            if direction != d:
                break

            # increment the count if we are still going in the same direction
            count += 1

        # return the count
        return count

    def direction(self, other: "Node") -> Direction:
        if self.coords.y == other.coords.y:
            if self.coords.x < other.coords.x:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        else:
            if self.coords.y < other.coords.y:
                return Direction.DOWN
            else:
                return Direction.UP

    def __eq__(self, other: "Node") -> bool:
        if not isinstance(other, Node):
            return NotImplemented

        return self.coords == other.coords

    def __hash__(self) -> int:
        return hash(self.coords)

    def __repr__(self) -> str:
        return f"{str(self.coords)} @ {self.loss} = {self.f})"

    def __str__(self) -> str:
        return str(self.loss)


@dataclass
class Map:
    data: list[list[Node]] = field(init=False)
    map: InitVar[list[str]]

    def __post_init__(self, map: list[str]):
        self.data = []
        for y, line in enumerate(map):
            self.data.append([])
            for x, value in enumerate(line):
                point = Point(y, x)
                self.data[y].append(Node(point, int(value), None))

    def __str__(self) -> str:
        return "\n".join("".join(str(node.loss) for node in line) for line in self.data)

    def render_path(self, path: list[Node]) -> str:
        """Returns a string representation of the map with the given path rendered"""

        return "\n".join(
            "".join(
                f"{Style.DIM}{Fore.BLACK}{str(node.loss)}{Style.RESET_ALL}"
                if node not in path
                else f"{Style.BRIGHT}{Fore.CYAN}{str(node.loss)}{Style.RESET_ALL}"
                for node in line
            )
            for line in self.data
        )

    def __getitem__(self, key: tuple[int, int]) -> Node:
        y, x = key
        return self.data[y][x]

    def neighbors(self, node: Node) -> Iterable[Node]:
        coords = node.coords

        point_direction = [
            (coords.y - 1, coords.x),
            (coords.y + 1, coords.x),
            (coords.y, coords.x - 1),
            (coords.y, coords.x + 1),
        ]

        # only return neighbors that are in bounds
        in_bounds = []
        for y, x in point_direction:
            if 0 <= y < len(self.data) and 0 <= x < len(self.data[y]):
                base = self[(y, x)]
                in_bounds.append(Node(base.coords, base.loss, node))

        # make sure the neighbor are not consecutive for too many blocks
        max_consecutive = 2
        for neighbor in in_bounds:
            if neighbor.consecutive() > max_consecutive:
                continue
            yield neighbor


def best_path(map: Map, start_coords: tuple[int, int] = (0, 0), goal_coords: tuple[int, int] = (-1, -1)) -> list[Node]:
    """Returns a list of tuples as a path from the given start to the given end in the given map

    make an openlist containing only the starting node
    make an empty closed list
    while (the destination node has not been reached):
        consider the node with the lowest f score in the open list
        if (this node is our destination node):
            we are finished

        if not:
            put the current node in the closed list and look at all of its neighbors
            for (each neighbor of the current node):
                if (neighbor has lower g value than current and is in the closed list):
                    replace the neighbor with the new, lower, g value
                    current node is now the neighbor's parent

                else if (current g value is lower and this neighbor is in the open list):
                    replace the neighbor with the new, lower, g value
                    change the neighbor's parent to our current node

                else if this neighbor is not in both lists:
                    add it to the open list and set its g
    """

    # Create start and end node
    start = map[start_coords]
    goal = map[goal_coords]

    # Initialize both open and closed list
    open_list: deque[Node] = deque()
    closed_list: set[Node] = set()

    # Add the start node
    open_list.append(start)

    # Loop until you find the end
    while len(open_list) > 0:
        # get the lowest f score (account for loss if f score is tied)
        open_list = deque(sorted(open_list, key=lambda n: (n.f, n.loss)))
        current: Node = open_list.popleft()

        # Pop current off open list, add to closed list
        closed_list.add(current)

        # Found the goal
        if current == goal:
            shortest_path = []
            while current is not None:
                shortest_path.append(current)
                current = current.parent
            return list(reversed(shortest_path))

        # Generate children
        children: Iterable[Node] = map.neighbors(current)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current.g + child.loss
            child.h = abs(child.coords.y - goal.coords.y) + abs(child.coords.x - goal.coords.x)
            child.f = child.g + child.h  # + (30 * child.loss)

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def heat_loss(path: list[Node]) -> int:
    return sum(node.loss for node in path)


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    map = Map(parse_lines(filepath))
    # print(map)
    best = best_path(map)
    print(map.render_path(best))
    print(str(heat_loss(best)))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1")
