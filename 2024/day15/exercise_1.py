#!/usr/bin/env python

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Iterable


class Value(StrEnum):
    EMPTY = "."
    WALL = "#"
    BOX = "O"
    ROBOT = "@"
    INVALID = "*"


class Move(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


@dataclass
class Warehouse:
    grid: list[list[Value]] = field(init=False, default_factory=list)
    robot: tuple[int, int] = field(init=False)

    def add_line(self, line: str) -> None:
        y: int = len(self.grid)
        row: list[Value] = []

        for x, char in enumerate(line):
            value: Value = Value(char)
            if value == Value.ROBOT:
                self.robot = (x, y)
            row.append(value)

        self.grid.append(row)

    def at(self, x: int, y: int) -> Value:
        if 0 > x or x >= len(self.grid[0]):
            return Value.INVALID

        if 0 > y or y >= len(self.grid):
            return Value.INVALID

        return self.grid[y][x]

    def line(self, x: int, y: int, move: Move) -> list[Value]:
        match move:
            case Move.UP:
                return [self.at(x, y - i) for i in range(0, y)]
            case Move.DOWN:
                return [self.at(x, y + i) for i in range(0, len(self.grid) - y)]
            case Move.LEFT:
                return [self.at(x - i, y) for i in range(0, x)]
            case Move.RIGHT:
                return [self.at(x + i, y) for i in range(0, len(self.grid[0]) - x)]

    def update_line(self, x: int, y: int, move: Move, line: list[Value]) -> None:
        v: Value
        match move:
            case Move.UP:
                for iy in range(y, 0, -1):
                    v = line[y - iy]
                    self.grid[iy][x] = v
                    if v == Value.ROBOT:
                        self.robot = (x, iy)
            case Move.DOWN:
                for iy in range(y, len(self.grid)):
                    v = line[iy - y]
                    self.grid[iy][x] = v
                    if v == Value.ROBOT:
                        self.robot = (x, iy)
            case Move.LEFT:
                for ix in range(x, 0, -1):
                    v = line[x - ix]
                    self.grid[y][ix] = v
                    if v == Value.ROBOT:
                        self.robot = (ix, y)
            case Move.RIGHT:
                for ix in range(x, len(self.grid[0])):
                    v = line[ix - x]
                    self.grid[y][ix] = v
                    if v == Value.ROBOT:
                        self.robot = (ix, y)

    def boxes(self) -> Iterable[tuple[int, int]]:
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                if value == Value.BOX:
                    yield (x, y)

    def __str__(self) -> str:
        return "\n".join("".join(value.value for value in row) for row in self.grid)


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_warehouse(line_iter: Iterable[str]) -> Warehouse:
    warehouse = Warehouse()
    for line in line_iter:
        if line == "":
            break
        warehouse.add_line(line)

    return warehouse


def parse_moves(line_iter: Iterable[str]) -> list[Move]:
    moves: list[Move] = []

    for line in line_iter:
        moves.extend([Move(m) for m in line])

    return moves


def parse_input(filepath: Path) -> tuple[Warehouse, list[Move]]:
    line_iter = parse_lines(filepath)
    warehouse = parse_warehouse(line_iter)
    moves = parse_moves(line_iter)

    return warehouse, moves


def move_robot(line: list[Value]) -> list[Value]:
    # walk the line and move if empty spaces found
    empty: list[int] = [i for i, v in enumerate(line[1:], 1) if v == Value.EMPTY]
    if empty:
        # check if we are blocked by a wall before the empty space
        blocking: list[int] = [i for i, v in enumerate(line[1 : empty[0]]) if v == Value.WALL]
        if blocking:
            return line

        # we should be able to move something
        moved: list[Value] = line.copy()
        moved.remove(Value.EMPTY)
        moved.insert(0, Value.EMPTY)

        # we should be all moved now
        return moved

    else:
        # if there are no empty spaces we're blocked
        return line


def apply(warehouse: Warehouse, moves: list[Move]) -> Warehouse:
    for m in moves:
        line: list[Value] = warehouse.line(*warehouse.robot, m)
        moved: list[Value] = move_robot(line)
        warehouse.update_line(*warehouse.robot, m, moved)

    return warehouse


def main(filepath: Path):
    warehouse: Warehouse
    moves: list[Move]
    warehouse, moves = parse_input(filepath)
    warehouse = apply(warehouse, moves)
    print(warehouse)

    # sum of all the box locations in gps coords
    total: int = 0
    for x, y in warehouse.boxes():
        total += (y * 100) + x

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
