#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


BAD_MOVES: dict[tuple[str, str], str] = {
    ("A", "1"): "<<^",
    ("A", "4"): "<<^^",
    ("A", "7"): "<<^^^",
    ("0", "1"): "<^",
    ("0", "4"): "<^^",
    ("0", "7"): "<^^^",
    ("1", "0"): "v>",
    ("1", "A"): "v>>",
    ("4", "0"): "vv>",
    ("4", "A"): "vv>>",
    ("7", "0"): "vvv>",
    ("7", "A"): "vvv>>",
}

LOOKUP: dict[tuple[str, str], set[str]] = {
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+
    ("A", "0"): set("<"),
    ("A", "1"): set("^<<"),
    ("A", "2"): set("^<"),
    ("A", "3"): set("^"),
    ("A", "4"): set("^^<<"),
    ("A", "5"): set("^^<"),
    ("A", "6"): set("^^"),
    ("A", "7"): set("^^^<<"),
    ("A", "8"): set("^^^<"),
    ("A", "9"): set("^^^"),
    ("A", "A"): set(""),
    ("0", "0"): set(""),
    ("0", "1"): set("^<"),
    ("0", "2"): set("^"),
    ("0", "3"): set("^>"),
    ("0", "4"): set("^^<"),
    ("0", "5"): set("^^"),
    ("0", "6"): set("^^>"),
    ("0", "7"): set("^^^<"),
    ("0", "8"): set("^^^"),
    ("0", "9"): set("^^^>"),
    ("0", "A"): set(">"),
    ("1", "0"): set(">v"),
    ("1", "1"): set(""),
    ("1", "2"): set(">"),
    ("1", "3"): set(">>"),
    ("1", "4"): set("^"),
    ("1", "5"): set("^>"),
    ("1", "6"): set("^>>"),
    ("1", "7"): set("^^"),
    ("1", "8"): set("^^>"),
    ("1", "9"): set("^^>>"),
    ("1", "A"): set(">>v"),
    ("2", "0"): set("v"),
    ("2", "1"): set("<"),
    ("2", "2"): set(""),
    ("2", "3"): set(">"),
    ("2", "4"): set("^<"),
    ("2", "5"): set("^"),
    ("2", "6"): set("^>"),
    ("2", "7"): set("^^<"),
    ("2", "8"): set("^^"),
    ("2", "9"): set(">^^"),
    ("2", "A"): set(">v"),
    ("3", "0"): set("v<"),
    ("3", "1"): set("<<"),
    ("3", "2"): set("<"),
    ("3", "3"): set(""),
    ("3", "4"): set("^<<"),
    ("3", "5"): set("^<"),
    ("3", "6"): set("^"),
    ("3", "7"): set("^^<<"),
    ("3", "8"): set("^^<"),
    ("3", "9"): set("^^"),
    ("3", "A"): set("v"),
    ("4", "0"): set(">vv"),
    ("4", "1"): set("v"),
    ("4", "2"): set("v>"),
    ("4", "3"): set("v>>"),
    ("4", "4"): set(""),
    ("4", "5"): set(">"),
    ("4", "6"): set(">>"),
    ("4", "7"): set("^"),
    ("4", "8"): set("^>"),
    ("4", "9"): set("^>>"),
    ("4", "A"): set(">>vv"),
    ("5", "0"): set("vv"),
    ("5", "1"): set("v<"),
    ("5", "2"): set("v"),
    ("5", "3"): set("v>"),
    ("5", "4"): set("<"),
    ("5", "5"): set(""),
    ("5", "6"): set(">"),
    ("5", "7"): set("^<"),
    ("5", "8"): set("^"),
    ("5", "9"): set("^>"),
    ("5", "A"): set(">vv"),
    ("6", "0"): set("vv<"),
    ("6", "1"): set("v<<"),
    ("6", "2"): set("v<"),
    ("6", "3"): set("v"),
    ("6", "4"): set("<<"),
    ("6", "5"): set("<"),
    ("6", "6"): set(""),
    ("6", "7"): set("^<<"),
    ("6", "8"): set("^<"),
    ("6", "9"): set("^"),
    ("6", "A"): set("vv"),
    ("7", "0"): set(">vvv"),
    ("7", "1"): set("vv"),
    ("7", "2"): set("vv>"),
    ("7", "3"): set(">>vv"),
    ("7", "4"): set("v"),
    ("7", "5"): set(">v"),
    ("7", "6"): set(">>v"),
    ("7", "7"): set(""),
    ("7", "8"): set(">"),
    ("7", "9"): set(">>"),
    ("7", "A"): set(">>vvv"),
    ("8", "0"): set("vvv"),
    ("8", "1"): set("vv<"),
    ("8", "2"): set("vv"),
    ("8", "3"): set("vv>"),
    ("8", "4"): set("v<"),
    ("8", "5"): set("v"),
    ("8", "6"): set("v>"),
    ("8", "7"): set("<"),
    ("8", "8"): set(""),
    ("8", "9"): set(">"),
    ("8", "A"): set(">vvv"),
    ("9", "0"): set("<vvv"),
    ("9", "1"): set("<<vv"),
    ("9", "2"): set("<vv"),
    ("9", "3"): set("vv"),
    ("9", "4"): set("<<v"),
    ("9", "5"): set("<v"),
    ("9", "6"): set("v"),
    ("9", "7"): set("<<"),
    ("9", "8"): set("<"),
    ("9", "9"): set(""),
    ("9", "A"): set("vvv"),
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    ("A", "^"): set("<"),
    ("A", ">"): set("v"),
    ("A", "v"): set("<v"),
    ("A", "<"): set("v<<"),
    ("A", "A"): set(""),
    ("<", "^"): set(">^"),
    ("<", ">"): set(">>"),
    ("<", "v"): set(">"),
    ("<", "<"): set(""),
    ("<", "A"): set(">>^"),
    ("^", "^"): set(""),
    ("^", ">"): set(">v"),
    ("^", "v"): set("v"),
    ("^", "<"): set("v<"),
    ("^", "A"): set(">"),
    (">", "^"): set("<^"),
    (">", ">"): set(""),
    (">", "v"): set("<"),
    (">", "<"): set("<<"),
    (">", "A"): set("^"),
    ("v", "^"): set("^"),
    ("v", ">"): set(">"),
    ("v", "v"): set(""),
    ("v", "<"): set("<"),
    ("v", "A"): set(">^"),
}

DIRECTION_PAD_REVERT: dict[set[str], tuple[str, str]] = {v: k for k, v in LOOKUP.items()}


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def transform(code: str, lookup: dict[tuple[str, str], str]) -> str:
    with_start: str = f"A{code}"
    return "".join([lookup[(c, with_start[i + 1])] for i, c in enumerate(with_start[:-1])])


def shortest_transforms(code: str, lookup: dict[tuple[str, str], set[str]]) -> list[str]:
    with_start: str = f"A{code}"
    shortest: int = len(with_start) * 10

    return "".join([lookup[(c, with_start[i + 1])] for i, c in enumerate(with_start[:-1])])


def main(filepath: Path):
    codes: list[str] = [line for line in parse_lines(filepath)]
    total: int = 0

    for code in codes:
        # robot 1 = code -> number pad
        r1: str = transform(code, LOOKUP, BAD_MOVES)

        # robot 2 = number pad -> direction pad
        r2: str = transform(r1, LOOKUP, BAD_MOVES)

        # robot 3 = direction pag -> direction pad
        r3: str = transform(r2, LOOKUP, BAD_MOVES)

        value: int = int("".join([c for c in code if c != "A"]))
        print(f"{code} ({len(r3)} * {value}): {r3}")

        total += value * len(r3)

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1")
