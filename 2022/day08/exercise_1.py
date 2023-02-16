#!/usr/bin/env python3


from dataclasses import dataclass
from typing import Iterable


def parse_lines(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_grid(filepath: str) -> list[list[int]]:
    grid: list[list[int]] = []

    for line in parse_lines(filepath):
        grid.append([int(char) for char in line])

    return grid


def print_grid(grid: list[list[int]]):
    for y in grid:
        print(" ".join([str(x) for x in y]))


@dataclass
class Dimensions:
    y: int
    x: int


def is_visible(
    y: int, x: int, height: int, grid: list[list[int]], dims: Dimensions
) -> bool:
    # print(f"{y}, {x}: {height}")

    # check up
    up = len([grid[i][x] for i in range(y - 1, -1, -1) if grid[i][x] >= height]) == 0

    # check down
    down = len([grid[i][x] for i in range(y + 1, dims.y) if grid[i][x] >= height]) == 0

    # check left
    left = len([grid[y][j] for j in range(x - 1, -1, -1) if grid[y][j] >= height]) == 0

    # check right
    right = len([grid[y][j] for j in range(x + 1, dims.x) if grid[y][j] >= height]) == 0

    # print(f"visible: {up} {right} {down} {left}")

    return any([up, down, left, right])


def main():
    grid = parse_grid("2022/day08/data/full")
    dims = Dimensions(len(grid), len(grid[0]))

    # outside edge is always visible, start with those
    count = (dims.y * 2) + ((dims.x - 2) * 2)

    print(f"edge count: {count}")

    for y, row in enumerate(grid[1:-1], 1):
        for x, height in enumerate(row[1:-1], 1):
            if is_visible(y, x, height, grid, dims):
                count += 1

    print(f"visible trees: {count}")


if __name__ == "__main__":
    main()
