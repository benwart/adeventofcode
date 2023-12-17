#!/usr/bin/env python

from collections import deque
from dataclasses import InitVar, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Iterable


class Direction(StrEnum):
    LEFT = "←"
    RIGHT = "→"
    UP = "↑"
    DOWN = "↓"


class Space(StrEnum):
    HORIZONTAL = "-"
    VERTICAL = "|"
    SLASH = "/"
    BACKSLASH = "\\"
    EMPTY = "."
    HEATED = "#"


@dataclass
class Line:
    grid: "Grid"
    spaces: list[Space]
    len: int = field(init=False)
    index: int

    def __post_init__(self) -> None:
        self.len = len(self.spaces)

    def __repr__(self) -> str:
        return f"Line({str(self)})"

    def __str__(self) -> str:
        return "".join([space.value for space in self.spaces])

    def to_string(self, index: int) -> str:
        return "".join(["*" if i == index else s for i, s in enumerate(self.spaces)])


@dataclass
class Lookup:
    x: int
    y: int
    row: Line
    column: Line

    def space(self) -> Space:
        return self.row.spaces[self.x]


@dataclass
class Grid:
    lines: InitVar[Iterable[Line]]
    rows: list[Line] = field(default_factory=list)
    columns: list[Line] = field(default_factory=list)
    index: dict[tuple[int, int], Space] = field(default_factory=dict)

    def __post_init__(self, lines: Iterable[Line]) -> None:
        self.rows = [Line(self, [Space(c) for c in line], r) for r, line in enumerate(lines)]

        columns = [[] for _ in range(self.rows[0].len)]
        for row in self.rows:
            for c in range(row.len):
                columns[c].append(Space(row.spaces[c]))

        self.columns = [Line(self, column, c) for c, column in enumerate(columns)]

        # index all the spaces
        for y, line in enumerate(self.rows):
            for x in range(line.len):
                self.index[(y, x)] = Lookup(x, y, self.rows[y], self.columns[x])

    def __str__(self) -> str:
        return "\n".join([str(row) for row in self.rows])

    def __getitem__(self, key: tuple[int, int]) -> Lookup:
        return self.index[key]


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


@dataclass
class Ray:
    grid: InitVar[Grid]
    y: InitVar[int]
    x: InitVar[int]
    direction: Direction
    point: Lookup = field(init=False)

    def __post_init__(self, grid: Grid, y: int, x: int) -> None:
        self.point = grid[(y, x)]

    def __hash__(self) -> int:
        return hash((self.point.y, self.point.x, self.direction))

    def __repr__(self) -> str:
        return f"Ray({str(self)})"

    def __str__(self) -> str:
        return f"[{self.point.y},{self.point.x}] {self.direction}"


def coords_from_offset(y: int, x: int, direction: Direction, offset: int) -> tuple[int, int]:
    match (direction):
        case Direction.LEFT:
            return (y, x - offset)
        case Direction.RIGHT:
            return (y, x + offset)
        case Direction.UP:
            return (y - offset, x)
        case Direction.DOWN:
            return (y + offset, x)


mirror_turns = {
    Direction.LEFT: {
        Space.SLASH: Direction.DOWN,
        Space.BACKSLASH: Direction.UP,
    },
    Direction.RIGHT: {
        Space.SLASH: Direction.UP,
        Space.BACKSLASH: Direction.DOWN,
    },
    Direction.UP: {
        Space.SLASH: Direction.RIGHT,
        Space.BACKSLASH: Direction.LEFT,
    },
    Direction.DOWN: {
        Space.SLASH: Direction.LEFT,
        Space.BACKSLASH: Direction.RIGHT,
    },
}


def render_heated(grid: Grid, heated: dict[tuple[int, int], Space]) -> str:
    lines = []
    for y, line in enumerate(grid.rows):
        chars = []
        for x in range(line.len):
            chars.append(heated.get((y, x), Space.EMPTY))
        lines.append("".join(chars))
    return "\n".join(lines)


def energize_grid(grid: Grid, start: Ray) -> int:
    rays = deque()
    coords = (start.point.y, start.point.x)

    heated: dict[tuple[int, int], Space] = {}
    heated[coords] = Space.HEATED

    # make sure we do the right thing since we are starting off the grid
    # skip empty spaces

    space = grid[coords].space()

    if (
        space == Space.EMPTY
        or space == Space.HORIZONTAL
        and start.direction in (Direction.LEFT, Direction.RIGHT)
        or space == Space.VERTICAL
        and start.direction in (Direction.UP, Direction.DOWN)
    ):
        rays.append(start)

    elif space == Space.HORIZONTAL and start.direction in (Direction.UP, Direction.DOWN):
        rays.append(Ray(grid, *coords, Direction.LEFT))
        rays.append(Ray(grid, *coords, Direction.RIGHT))

    elif space == Space.VERTICAL and start.direction in (Direction.LEFT, Direction.RIGHT):
        rays.append(Ray(grid, *coords, Direction.UP))
        rays.append(Ray(grid, *coords, Direction.DOWN))

    elif space in [Space.BACKSLASH, Space.SLASH]:
        turn = mirror_turns[start.direction][space]
        rays.append(Ray(grid, *coords, turn))

    # store history of rays casts so we don't repeat ourselves
    casts: set[rays] = set()

    # cast rays until we run out
    while len(rays):
        ray = rays.popleft()

        # check if we've already cast this ray
        if ray in casts:
            continue

        # add this ray to the set of casts
        casts.add(ray)

        # get current position
        y, x = ray.point.y, ray.point.x

        # get appropriate line, starting point on line, and step size (direction)
        match (ray.direction):
            case Direction.LEFT | Direction.RIGHT:
                line = ray.point.row
                index = x
                reverse = ray.direction == Direction.LEFT
            case Direction.UP | Direction.DOWN:
                line = ray.point.column
                index = y
                reverse = ray.direction == Direction.UP

        # print(f"{line.to_string(index)} starting at {index} ({y},{x}) moving {'reverse' if reverse else 'forward'} ({ray.direction})")

        ray_range = range(index, -1, -1) if reverse else range(index, line.len)
        for i in ray_range:
            if i == index:
                continue

            space: Space = line.spaces[i]
            coords = coords_from_offset(y, x, ray.direction, abs(index - i))

            # add to heat map
            heated[coords] = Space.HEATED

            # skip empty spaces
            if space == Space.EMPTY:
                continue

            # horizontal rays go through horizontal spaces
            if space == Space.HORIZONTAL and ray.direction in (Direction.LEFT, Direction.RIGHT):
                continue

            # vertical rays go through vertical spaces
            if space == Space.VERTICAL and ray.direction in (Direction.UP, Direction.DOWN):
                continue

            # vertical rays get split into two rays at horizontal spaces
            if space == Space.HORIZONTAL and ray.direction in (Direction.UP, Direction.DOWN):
                rays.append(Ray(grid, *coords, Direction.LEFT))
                rays.append(Ray(grid, *coords, Direction.RIGHT))
                # print("split horizontal")
                break

            # horizontal rays get split into two rays at vertical spaces
            if space == Space.VERTICAL and ray.direction in (Direction.LEFT, Direction.RIGHT):
                rays.append(Ray(grid, *coords, Direction.UP))
                rays.append(Ray(grid, *coords, Direction.DOWN))
                # print("split vertical")
                break

            # turn 90 degrees at mirrors
            if space in [Space.BACKSLASH, Space.SLASH]:
                turn = mirror_turns[ray.direction][space]
                rays.append(Ray(grid, *coords, turn))
                # print(f"turn {turn}")
                break

    # performed the following casts
    # print(casts)

    # show heated map
    # print(render_heated(grid, heated))

    return len(heated)


def start_positions(grid: Grid) -> Iterable[Ray]:
    """Generate all possible edge starting positions from outside in."""
    # top edge
    for x in range(grid.rows[0].len):
        yield Ray(grid, 0, x, Direction.DOWN)

    # right edge
    for y in range(grid.rows[0].len):
        yield Ray(grid, y, grid.rows[0].len - 1, Direction.LEFT)

    # bottom edge
    for x in range(grid.rows[0].len):
        yield Ray(grid, grid.rows[0].len - 1, x, Direction.UP)

    # left edge
    for y in range(grid.rows[0].len):
        yield Ray(grid, y, 0, Direction.RIGHT)


def main(filepath: Path):
    grid = Grid(parse_lines(filepath))

    # generate all the posible start positions
    max_energy = 0
    for start in start_positions(grid):
        energy = energize_grid(grid, start)
        max_energy = max(max_energy, energy)

    print(f"max energy: {max_energy}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
