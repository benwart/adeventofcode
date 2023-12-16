#!/usr/bin/env python

from collections import defaultdict, deque
from pathlib import Path
from typing import Deque, Iterable, DefaultDict


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def rotate_panel(panel: tuple[str]) -> tuple[str]:
    columns: DefaultDict[int, deque[str]] = defaultdict(deque)
    for line in panel:
        width = len(line)
        for i, c in enumerate(line):
            columns[(width - 1) - i].appendleft(c)

    return tuple(["".join(chars) for _, chars in columns.items()])


def panel_weight(panel: tuple[str]) -> int:
    total = 0
    for r, row in enumerate(reversed(panel)):
        for c in row:
            if c == "O":
                total += r + 1

    return total


def transpose_panel(panel: tuple[str]) -> tuple[str]:
    columns: Deque[list[str]] = deque(maxlen=len(panel))
    for row in panel:
        for i, c in enumerate(row):
            if len(columns) <= i:
                columns.append([c])
            else:
                columns[i].append(c)

    return tuple(["".join(chars) for chars in columns])


def shift_rocks(panel: tuple[str]) -> tuple[str]:
    # transpose the panel
    transposed = transpose_panel(panel)

    # roll the rocks
    shifted = []
    for column in transposed:
        # split the column into sections
        sections = "".join(column).split("#")
        shifted_sections = []
        for section in sections:
            # shift 'O' to the right
            length = len(section)
            rocks = section.count("O")
            shifted_sections.append(f"{'O' * rocks}{'.' * (length - rocks)}")

        # rejoin the sections
        rejoined = "#".join(shifted_sections)
        shifted.append(rejoined)

    # transpose the panel back
    rows = transpose_panel(tuple(shifted))

    # join the lists in each row
    return tuple(["".join(r) for r in rows])


def cycle(panel: tuple[str], cycles: int) -> tuple[str]:
    working = panel
    for _ in range(cycles):
        for _ in range(4):
            working = rotate_panel(working)
            working = shift_rocks(working)

    return working


def find_cycle(panel: tuple[str]) -> int:
    cycles = 1000000000 * 4
    cached: set[tuple] = set()
    working = panel

    # add initial state
    cached.add(working)

    for i in range(cycles):
        working = cycle(working, 1)

        # add to cache
        if working not in cached:
            cached.add(working)
        else:
            print(f"Found a pattern after {i} cycles!")
            break

    return i


def main(filepath: Path):
    panel = tuple(parse_lines(filepath))
    cycles = 1000000000 * 4
    cycle_length = find_cycle(panel)

    # calculate how many more rotations
    q, r = divmod(cycles, cycle_length)
    print(f"Cycle length: {cycle_length}")
    print(f"Remaining rotations: {r}")
    print(f"Total cycles: {q * cycle_length + r}")

    # perform the left over cycles
    panel = cycle(panel, r)

    # calculate the total
    total = panel_weight(panel)
    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_2")
