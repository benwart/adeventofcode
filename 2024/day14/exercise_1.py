#!/usr/bin/env python

from dataclasses import dataclass
from pathlib import Path
from re import Pattern, compile
from typing import Iterable


ROBOT_INPUT: Pattern = compile(r"p=(?P<x>(-)?\d+),(?P<y>(-)?\d+) v=(?P<dx>(-)?\d+),(?P<dy>(-)?\d+)")


@dataclass
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_robots(filepath: Path) -> Iterable[Robot]:
    for line in parse_lines(filepath):
        m = ROBOT_INPUT.match(line)
        if m:
            yield Robot(
                position=(int(m.group("x")), int(m.group("y"))),
                velocity=(int(m.group("dx")), int(m.group("dy"))),
            )


def move(grid: tuple[int, int], robot: Robot, seconds: int) -> tuple[int, int]:
    gx, gy = grid
    x, y = robot.position
    dx, dy = robot.velocity

    px = (x + (dx * seconds)) % gx
    py = (y + (dy * seconds)) % gy

    return px, py


def main(filepath: Path):
    grid: tuple[int, int] = (101, 103)
    robot: Robot
    endings: dict[tuple[int, int], int] = {}
    p: tuple[int, int]
    for robot in parse_robots(filepath):
        p = move(grid, robot, 100)
        if p not in endings:
            endings[p] = 0
        endings[p] += 1

    # find middle of grid to ignore
    gx, gy = grid
    mx, my = gx // 2, gy // 2

    quadrants: list[int] = [0] * 4
    for (x, y), count in endings.items():
        if x == mx or y == my:
            continue

        if x < mx and y < my:
            quadrants[0] += count
        elif x > mx and y < my:
            quadrants[1] += count
        elif x < mx and y > my:
            quadrants[2] += count
        elif x > mx and y > my:
            quadrants[3] += count

    total: int = 1
    for count in quadrants:
        total *= count

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
