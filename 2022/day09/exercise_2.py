#!/usr/bin/env python3


from dataclasses import dataclass
from enum import Enum
from typing import Iterable


def parse_lines(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


class Direction(Enum):
    LEFT = "L"
    UP = "U"
    RIGHT = "R"
    DOWN = "D"


@dataclass
class Motion:
    direction: Direction
    count: int


def parse_motions(filepath: str) -> Iterable[Motion]:
    for line in parse_lines(filepath):
        args = line.split(" ")
        yield Motion(Direction(args[0]), int(args[1]))


@dataclass
class Coordinates:
    y: int
    x: int

    def __hash__(self) -> int:
        return hash(f"{self.y},{self.x}")

    def delta(self, other: "Coordinates") -> "Coordinates":
        return Coordinates(self.y - other.y, self.x - other.x)


def move_head(head: Coordinates, direction: Direction) -> Coordinates:
    y = head.y
    x = head.x

    match direction:
        case Direction.UP:
            y += 1
        case Direction.RIGHT:
            x += 1
        case Direction.DOWN:
            y -= 1
        case Direction.LEFT:
            x -= 1

    return Coordinates(y, x)


def move_tail(tail: Coordinates, head: Coordinates) -> Coordinates:
    y = tail.y
    x = tail.x

    delta = head.delta(tail)

    # if the delta has no value greater than 1 then no movement
    if (-2 < delta.y < 2) and (-2 < delta.x < 2):
        return tail

    if delta.y > 0:
        y += 1
    elif delta.y < 0:
        y -= 1

    if delta.x > 0:
        x += 1
    elif delta.x < 0:
        x -= 1

    return Coordinates(y, x)


def print_grid_with_rope(segments: list[Coordinates]):
    # new segment with one set to 0,0 every time
    segments_with_start = [s for s in segments]
    segments_with_start.append(Coordinates(0, 0))

    # find min/max y and min/max x
    minimum = Coordinates(
        min([s.y for s in segments_with_start]), min([s.x for s in segments_with_start])
    )
    maximum = Coordinates(
        max([s.y for s in segments_with_start]), max([s.x for s in segments_with_start])
    )

    height = (maximum.y - minimum.y) + 1
    width = (maximum.x - minimum.x) + 1

    # set grid coordinates
    grid = [["." for x in range(width)] for y in range(height)]

    # add segments from tail to head
    for index, segment in reversed([(i, v) for i, v in enumerate(segments_with_start)]):
        grid[maximum.y - segment.y][segment.x - minimum.x] = (
            str(index) if index < 10 else "s"
        )

    # print the grid
    for row in grid:
        print(" ".join(row))


def main():
    segments = [Coordinates(0, 0) for _ in range(10)]
    tail_visited = {segments[9]}

    for motion in parse_motions("2022/day09/data/full"):
        # print_grid_with_rope(segments)

        print(motion)

        for _ in range(motion.count):
            # move the actual head
            segments[0] = move_head(segments[0], motion.direction)

            # iterate through the segments util we get to the tail
            for i, _ in enumerate(segments[1:], 1):

                # move tail based on relative location
                segments[i] = move_tail(segments[i], segments[i - 1])

            # add tail visited location
            tail_visited.add(segments[9])

    print(f"tail positions: {len(tail_visited)}")


if __name__ == "__main__":
    main()
