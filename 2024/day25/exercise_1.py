#!/usr/bin/env python

from dataclasses import InitVar, dataclass, field
from itertools import product
from pathlib import Path
from typing import Iterable


@dataclass
class Key:
    lines: InitVar[list[str]]
    opens: list[int] = field(init=False, default_factory=list)
    bumps: list[int] = field(init=False, default_factory=list)

    def __post_init__(self, lines: list[str]) -> None:
        for x in range(len(lines[0])):
            open: int = -1
            bump: int = -1
            for y in range(len(lines)):
                match lines[y][x]:
                    case "#":
                        bump += 1
                    case ".":
                        open += 1

            self.opens.append(open)
            self.bumps.append(bump)

    def __str__(self) -> str:
        return ",".join(map(str, self.bumps))


@dataclass
class Lock:
    lines: InitVar[list[str]]
    tumblers: list[int] = field(init=False, default_factory=list)
    slots: list[int] = field(init=False, default_factory=list)

    def __post_init__(self, lines: list[str]) -> None:
        for x in range(len(lines[0])):
            tumbler: int = -1
            slot: int = -1
            for y in range(len(lines)):
                match lines[y][x]:
                    case "#":
                        tumbler += 1
                    case ".":
                        slot += 1

            self.tumblers.append(tumbler)
            self.slots.append(slot)

    def __str__(self) -> str:
        return ",".join(map(str, self.tumblers))

    def unlock(self, key: "Key") -> bool:
        for i, bump in enumerate(key.bumps):
            if self.slots[i] < bump:
                return False

        return True


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_schematic(filepath: Path) -> tuple[list[Lock], list[Key]]:
    locks: list[Lock] = []
    keys: list[Key] = []

    lines: list[str] = []
    for line in parse_lines(filepath):
        if line == "":
            if lines[0][0] == "#":
                locks.append(Lock(lines))
            else:
                keys.append(Key(lines))
            lines = []

        else:
            lines.append(line)

    if lines[0][0] == "#":
        locks.append(Lock(lines))
    else:
        keys.append(Key(lines))
    lines = []

    return locks, keys


def main(filepath: Path):
    locks: list[Lock]
    keys: list[Key]
    locks, keys = parse_schematic(filepath)

    count: int = 0
    for key, lock in product(*(keys, locks)):
        if lock.unlock(key):
            count += 1
            # print(f"Lock {lock} and Key {key}: all columns fit!")
        # else:
        # print(f"Lock {lock} and Key {key}: overlap")

    print(count)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
