#!/usr/bin/env python

from collections import deque
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Iterable


class Value(StrEnum):
    EMPTY = "."
    WALL = "#"
    BOX = "O"
    ROBOT = "@"


class ExpValue(StrEnum):
    EMPTY = "."
    WALL = "#"
    BOX_L = "["
    BOX_R = "]"
    ROBOT = "@"


class Move(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


EXPAND_MAP = {
    Value.EMPTY: (ExpValue.EMPTY, ExpValue.EMPTY),
    Value.WALL: (ExpValue.WALL, ExpValue.WALL),
    Value.BOX: (ExpValue.BOX_L, ExpValue.BOX_R),
    Value.ROBOT: (ExpValue.ROBOT, ExpValue.EMPTY),
}


@dataclass
class Line:
    x: int
    y: int
    i: int
    m: Move
    line: list[ExpValue]

    def __eq__(self, other: "Line") -> bool:
        return other.x == self.x and other.y == self.y and other.m == self.m and other.line == self.line

    def __hash__(self) -> str:
        return hash((self.x, self.y, self.m))


@dataclass
class Swath:
    x: int
    y: int
    m: Move
    lines: list[Line] = field(default_factory=list)

    def contains(self, x: int, y: int, move: Move) -> bool:
        return all([l.eq(x, y, move) for l in self.lines])


@dataclass
class Warehouse:
    grid: list[list[ExpValue]] = field(init=False, default_factory=list)
    robot: tuple[int, int] = field(init=False)

    def add_line(self, line: str) -> None:
        y: int = len(self.grid)
        row: list[ExpValue] = []

        for x, char in enumerate(line):
            value: Value = Value(char)
            if value == Value.ROBOT:
                self.robot = (x * 2, y)
            row.extend(EXPAND_MAP[value])

        self.grid.append(row)

    def at(self, x: int, y: int) -> ExpValue:
        return self.grid[y][x]

    def line(self, x: int, y: int, move: Move) -> Line:
        match move:
            case Move.UP:
                return Line(x, y, move, [self.at(x, y - i) for i in range(0, y)])
            case Move.DOWN:
                return Line(x, y, move, [self.at(x, y + i) for i in range(0, len(self.grid) - y)])
            case Move.LEFT:
                return Line(x, y, move, [self.at(x - i, y) for i in range(0, x)])
            case Move.RIGHT:
                return Line(x, y, move, [self.at(x + i, y) for i in range(0, len(self.grid[0]) - x)])

    def swath(self, x: int, y: int, move: Move) -> Swath:
        lines: list[Line] = []

        # short circuit for LEFT and RIGHT movements that only need 1 line
        if move in [Move.LEFT, Move.RIGHT]:
            lines.append(self.line(x, y, move))
            return Swath(x, y, move, lines)

        # handle UP and DOWN movements that may need more than 1 line
        search: deque[tuple[int, Line]] = deque([(0, self.line(x, y, move))])
        seen: set[Line] = set([self.line(x, y, move)])
        current: tuple[int, int, int] = (x, y)

        while search:
            # search the line to see if more lines are needed
            start: int
            line: Line
            start, line = search.popleft()
            for i in range(start, len(line.line)):
                v: ExpValue = line.line[i]
                if v in [ExpValue.BOX_L, ExpValue.BOX_R]:
                    match v:
                        case ExpValue.BOX_L:
                            new_x: int = (1 if move == Move.UP else -1) + current[0]
                            new_line: Line = self.line(new_x, y, move)
                        case ExpValue.BOX_R:
                            new_x: int = (-1 if move == Move.UP else 1) + current[0]
                            new_line: Line = self.line(new_x, y, move)

                    if new_line not in seen:
                        search.append((i, new_line))
                        seen.add(new_line)

        s: Swath = Swath(x, y, move, list(seen))
        return s

    def update_line(self, line: Line) -> None:
        x: int = line.x
        y: int = line.y
        move: Move = line.m
        l: list[ExpValue] = line.line

        v: Value
        match move:
            case Move.UP:
                for iy in range(y, 0, -1):
                    v = l[y - iy]
                    self.grid[iy][x] = v
                    if v == Value.ROBOT:
                        self.robot = (x, iy)
            case Move.DOWN:
                for iy in range(y, len(self.grid)):
                    v = l[iy - y]
                    self.grid[iy][x] = v
                    if v == Value.ROBOT:
                        self.robot = (x, iy)
            case Move.LEFT:
                for ix in range(x, 0, -1):
                    v = l[x - ix]
                    self.grid[y][ix] = v
                    if v == Value.ROBOT:
                        self.robot = (ix, y)
            case Move.RIGHT:
                for ix in range(x, len(self.grid[0])):
                    v = l[ix - x]
                    self.grid[y][ix] = v
                    if v == Value.ROBOT:
                        self.robot = (ix, y)

    def update_swath(self, swath: Swath) -> None:
        for line in swath.lines:
            self.update_line(line)

    def boxes(self) -> Iterable[tuple[int, int]]:
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                if value == ExpValue.BOX_L:
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


def move_robot(swath: Swath) -> Swath:
    # TODO: update to move swaths of lines not just a single line

    # walk the line and move if empty spaces found
    # empty: list[int] = [i for i, v in enumerate(line[1:], 1) if v == Value.EMPTY]
    # if empty:
    #     # check if we are blocked by a wall before the empty space
    #     blocking: list[int] = [i for i, v in enumerate(line[1 : empty[0]]) if v == Value.WALL]
    #     if blocking:
    #         return line

    #     # we should be able to move something
    #     moved: list[Value] = line.copy()
    #     moved.remove(Value.EMPTY)
    #     moved.insert(0, Value.EMPTY)

    #     # we should be all moved now
    #     return moved

    # else:
    #     # if there are no empty spaces we're blocked
    #     return line

    return swath


def apply(warehouse: Warehouse, moves: list[Move]) -> Warehouse:
    for m in moves:
        swath: Swath = warehouse.swath(*warehouse.robot, m)
        moved: Swath = move_robot(swath)
        warehouse.update_swath(moved)

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
    main(Path(__file__).parent / "data" / "example_3")
