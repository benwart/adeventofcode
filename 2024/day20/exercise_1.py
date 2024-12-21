#!/usr/bin/env python

from math import hypot
from pathlib import Path
from typing import Iterable

from astar import find_path
from tqdm import tqdm


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_map(filepath: Path) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    map: list[list[str]] = []
    start: tuple[int, int]
    end: tuple[int, int]

    for y, line in enumerate(parse_lines(filepath)):
        row: list[str] = []
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
                row.append(".")
            elif c == "E":
                end = (x, y)
                row.append(".")
            else:
                row.append(c)
        map.append(row)

    return map, start, end


def get_cheats(map: list[list[str]]) -> Iterable[list[tuple[int, int, str]]]:
    for y, row in enumerate(map[1:-1], start=1):
        for x, c in enumerate(row[1:-1], start=1):
            if c == "#" and ((map[y][x - 1] == "." and map[y][x + 1] == ".") or (map[y - 1][x] == "." and map[y + 1][x] == ".")):
                yield (x, y)


def get_path(map: list[list[str]], start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    height: int = len(map)
    width: int = len(map[0])

    def neighbors(c: tuple[int, int]) -> Iterable[tuple[int, int]]:
        cx, cy = c
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = cx + dx, cy + dy
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            if map[ny][nx] == "#":
                continue

            yield nx, ny

    def cost_estimate(a: tuple[int, int], b: tuple[int, int]) -> bool:
        ax, ay = a
        bx, by = b
        return hypot((ax - bx), (ay - by))

    find_result = find_path(start, end, neighbors, heuristic_cost_estimate_fnct=cost_estimate)
    if find_result:
        path: list[tuple[int, int]] = [c for c in find_result]

        # print_grid(grid, set(path))
        return path


def main(filepath: Path):
    map, start, end = parse_map(filepath)
    no_cheats: int = len(get_path(map, start, end)) - 1

    cheats: set[tuple[int, int]] = {c for c in get_cheats(map)}

    saving: int = 100
    goal: int = 0
    for cx, cy in tqdm(cheats, unit="cheats"):
        # convert cheat to "."
        map[cy][cx] = "."

        # get shortest path
        with_cheat: int = no_cheats - (len(get_path(map, start, end)) - 1)

        # did we reach our goal
        if with_cheat >= saving:
            goal += 1

        # convert cheat back to "#"
        map[cy][cx] = "#"

    print(f"\n{goal}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1")
