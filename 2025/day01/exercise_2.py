#!/usr/bin/env python

from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[tuple[str, int]]:
    with open(filepath, "r") as f:
        for line in f:
            clean: str = line.strip()
            yield clean[0], int(clean[1:])


def main(filepath: Path):
    output: int = 0
    value: int = 50
    for direction, steps in parse_lines(filepath):

        # calculate ratations and final position
        q, r = divmod(steps, 100)

        # if we have multiple loops we passed over 0
        output += q

        # adjust value
        temp: int = value - r if direction == "L" else value + r
        dest: int = temp % 100

        # if temp and dest are not the same we crossed 0
        if value != 0 and (temp <= 0 or temp >= 100):
            output += 1

        # set value
        value = dest

    print(output)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
