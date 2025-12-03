#!/usr/bin/env python

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Segment:
    left: str
    right: str
    start: int
    stop: int


def parse_segments(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            for segment in line.split(","):
                yield segment.strip()


def parse_segment(segment: str) -> Segment:
    split: list[str] = segment.split("-")
    result: Segment = Segment(split[0], split[1], int(split[0]), int(split[1]))
    return result


def invalid_check(n: int) -> bool:
    # check for odd number of digits
    s: str = f"{n}"
    ls: int = len(s)
    half: int = ls // 2

    valid = False

    for size in range(1, half + 1):
        valid = True
        # ensure pattern size evenly fits string
        if ls % size != 0:
            valid = False
            continue

        # get the pattern
        pattern: int = int(s[0:size])

        # compare against repeats
        for j in range(size, ls, size):
            repeat: int = int(s[j : j + size])

            # if we fail to match no need to continue
            if pattern != repeat:
                valid = False
                break

        # if we are still valid
        if valid:
            break

    return valid


def main(filepath: Path):
    invalid: int = 0
    for segment in parse_segments(filepath):
        s: Segment = parse_segment(segment)
        for n in range(s.start, s.stop + 1):
            if invalid_check(n):
                invalid += n
                print(n)

    print(invalid)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
