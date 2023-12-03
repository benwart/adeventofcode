#!/usr/bin/env python

from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    print(filepath)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1")
