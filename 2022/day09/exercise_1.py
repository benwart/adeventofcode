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


def main():
    head = Coordinates(0, 0)
    tail = Coordinates(0, 0)
    tail_visited = {tail}

    for motion in parse_motions("2022/day09/data/full"):
        print(motion)

        for _ in range(motion.count):

            # move head
            head = move_head(head, motion.direction)

            # move tail based on relative location
            tail = move_tail(tail, head)

            # add tail visited location
            tail_visited.add(tail)

    print(f"tail positions: {len(tail_visited)}")


if __name__ == "__main__":
    main()
