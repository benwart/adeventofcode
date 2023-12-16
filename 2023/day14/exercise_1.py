#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path
from typing import Iterable, DefaultDict


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_columns(filepath: Path) -> Iterable[str]:
    columns: DefaultDict[int, list[str]] = defaultdict(list)
    for line in parse_lines(filepath):
        for i, c in enumerate(line.strip()):
            columns[i].append(c)

    for i, chars in columns.items():
        yield "".join(reversed(chars))

def weight(column: str) -> int:
    total = 0
    for i, c in enumerate(column):
        if c == "O":
            total += i + 1

    return total

def main(filepath: Path):
    total = 0
    for column in parse_columns(filepath):
        sections = column.split("#")
        shifted = []
        for section in sections:
            # shift 'O' to the right
            length = len(section)
            rocks = section.count("O")
            shifted.append(f"{"." * (length - rocks)}{"O" * rocks}")

        # rejoin the sections
        joined = "#".join(shifted)
        w = weight(joined)
        print(f"{joined} = {w}")

        total += w

    print(f"Total: {total}")
        

if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
