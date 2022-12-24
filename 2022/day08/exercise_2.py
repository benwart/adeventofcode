#!/usr/bin/env python3


from dataclasses import dataclass
from functools import reduce
from typing import Iterable
from operator import mul


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


def scenic_score(
    y: int, x: int, height: int, grid: list[list[int]], dims: Dimensions
) -> int:
    # print(f"{y}, {x}: {height}")

    up = [grid[i][x] for i in range(y - 1, -1, -1)]
    down = [grid[i][x] for i in range(y + 1, dims.y)]
    left = [grid[y][j] for j in range(x - 1, -1, -1)]
    right = [grid[y][j] for j in range(x + 1, dims.x)]

    scenic_score = 1
    for check in [up, right, down, left]:
        stopped = False
        for n, value in enumerate(check, 1):
            if value >= height:
                stopped = True
                scenic_score *= n
                break

        if not stopped:
            scenic_score *= n

    return scenic_score


def main():
    grid = parse_grid("2022/day08/data/full")
    dims = Dimensions(len(grid), len(grid[0]))

    scenic_scores = []

    for y, row in enumerate(grid[1:-1], 1):
        for x, height in enumerate(row[1:-1], 1):
            scenic_scores.append(scenic_score(y, x, height, grid, dims))

    print(f"scenic scores: {scenic_scores}")
    print(f"max: {max(scenic_scores)}")


if __name__ == "__main__":
    main()
