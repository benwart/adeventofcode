#!/usr/bin/env python

from dataclasses import dataclass
from math import inf
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


def no_overlap(robots: list[Robot]) -> bool:
    seen: set[tuple[int, int]] = set()

    for robot in robots:
        if robot.position in seen:
            return False

        else:
            seen.add(robot.position)

    return True


def print_grid(grid: tuple[int, int], robots: list[Robot]) -> None:
    gx, gy = grid
    for y in range(gy):
        for x in range(gx):
            for robot in robots:
                if robot.position == (x, y):
                    print("#", end="")
                    break
            else:
                print(".", end="")
        print()


def main(filepath: Path):
    grid: tuple[int, int] = (101, 103)
    robots: list[Robot] = [r for r in parse_robots(filepath)]

    gx, gy = grid

    for seconds in range(1, gx * gy):
        robot: Robot
        for robot in robots:
            robot.position = move(grid, robot, 1)

        if no_overlap(robots):
            print_grid(grid, robots)
            print(seconds)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
