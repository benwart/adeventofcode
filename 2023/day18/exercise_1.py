#!/usr/bin/env python

from dataclasses import dataclass, field, InitVar
from enum import StrEnum
from pathlib import Path
from re import compile
from typing import Iterable

from shapely import Point, LinearRing, Polygon

INSTSTRUCTION_REGEX = compile(r"(?P<direction>[UDLR]) (?P<steps>\d+) \(#(?P<color>[a-f0-9]{6})\)")


class Direction(StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Instruction:
    direction: Direction = field(init=False)
    steps: int = field(init=False)
    line: InitVar[str]

    def __post_init__(self, line: str):
        match = INSTSTRUCTION_REGEX.match(line)
        if match is None:
            raise ValueError(f"Invalid instruction: {line}")

        self.direction = Direction(match.group("direction"))
        self.steps = int(match.group("steps"))

    def __repr__(self) -> str:
        return f"Instruction[{str(self)}]"

    def __str__(self) -> str:
        return f"{self.direction} {self.steps} ({self.color})"


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    instructions = [Instruction(line) for line in parse_lines(filepath)]

    # Create a polygon from the instructions
    points: list[Point] = []
    current_point = Point(0, 0)
    for i in instructions:
        if i.direction == Direction.UP:
            new_point = Point(current_point.x, current_point.y + i.steps)
        elif i.direction == Direction.DOWN:
            new_point = Point(current_point.x, current_point.y - i.steps)
        elif i.direction == Direction.LEFT:
            new_point = Point(current_point.x - i.steps, current_point.y)
        elif i.direction == Direction.RIGHT:
            new_point = Point(current_point.x + i.steps, current_point.y)
        else:
            raise ValueError(f"Invalid direction: {i.direction}")

        points.append(new_point)
        current_point = new_point

    edge = LinearRing(points)
    pit = Polygon(edge).buffer(0.5, cap_style="square", join_style="mitre")
    print(int(pit.area))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
