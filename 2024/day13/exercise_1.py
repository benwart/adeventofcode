#!/usr/bin/env python

from pathlib import Path

Co = tuple[int, int]


def determinant(a: Co, b: Co) -> int:
    return a[0] * b[1] - a[1] * b[0]


def corrected(a: Co, b: Co, c: Co) -> tuple[Co, Co, Co]:
    return a, b, (int(c[0] + 1e13), int(c[1] + 1e13))


def solve(a: Co, b: Co, c: Co) -> int:
    det = determinant(a, b)
    ta = (determinant(c, b) * 3) / det
    tb = determinant(a, c) / det

    return int(ta + tb) if ta.is_integer() and tb.is_integer() else 0


def main(filepath: Path) -> None:
    input_text = filepath.read_text("utf-8").replace("=", "+").split("\n\n")
    data = [
        [(int(f[0].split("+")[1]), int(f[1].split("+")[1])) for f in [data.split(",") for data in [line.split(":")[1] for line in item.splitlines()]]]
        for item in input_text
    ]

    print("Part 1:", sum(solve(*i) for i in data))
    print("Part 2:", sum(solve(*corrected(*i)) for i in data))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
