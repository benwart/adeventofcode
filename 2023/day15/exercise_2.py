#!/usr/bin/env python

from enum import StrEnum
from dataclasses import dataclass
from pathlib import Path
from re import compile
from typing import Iterable, Optional


class Operation(StrEnum):
    LENS = "="
    REMOVE = "-"


@dataclass
class Value:
    label: str
    hash: int
    op: Operation
    lens: int

    def __eq__(self, other: "Value") -> bool:
        return self.label == other.label

    def __str__(self) -> str:
        return f"[{self.label} {self.lens if self.lens else '-'}]"

    def __repr__(self) -> str:
        return str(self)


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def hash_string(string: str) -> int:
    acc = 0
    for c in string:
        acc += ord(c)
        acc *= 17
        acc = acc % 256

    return acc


def parse_init_sequence(filepath: Path) -> list[Value]:
    def parese_values(values: str) -> Optional[Value]:
        pattern = compile(r"(?P<label>[^=-]+)(?P<op>[=-])(?P<lens>.*)?")
        for value in values:
            match = pattern.match(value)
            lens = None
            if match:
                groups = match.groupdict()
                label = groups["label"]
                op = Operation(groups["op"])

                if "lens" in groups and groups["lens"] != "":
                    lens = int(groups["lens"])

                yield Value(label, hash_string(label), Operation(op), lens)
            else:
                yield None

    return [v for v in parese_values(next(parse_lines(filepath)).split(",")) if v]


def run_init_sequence(sequence: list[Value]) -> dict[list[Value]]:
    shelf: dict[list[Value]] = {}
    for b in range(256):
        shelf[b] = []

    for value in sequence:
        if value.op == Operation.LENS:
            box: list[Value] = shelf[value.hash]
            if value not in box:
                box.append(value)
            else:
                i = box.index(value)
                box[i].lens = value.lens

        elif value.op == Operation.REMOVE:
            box: list[Value] = shelf[value.hash]
            if value in box:
                box.remove(value)

    # cleanup unused boxes
    return {box: values for box, values in shelf.items() if values}


def focusing_power(shelf: dict[list[Value]]) -> int:
    """One plus the box number of the lens in question.
    The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
    The focal length of the lens."""

    total = 0
    for box, values in shelf.items():
        for i, value in enumerate(values):
            power = (1 + box) * (i + 1) * value.lens
            # print(f"rn: {box+1} (box {box}) * {i+1} (slot) * {value.lens} (focal length) = {power}")
            total += power

    return total


def main(filepath: Path):
    sequence = parse_init_sequence(filepath)
    shelf = run_init_sequence(sequence)

    # for box, values in shelf.items():
    #     print(f"Box {box}: {" ".join([str(v) for v in values])}")

    total = focusing_power(shelf)
    print(f"Total focusing power: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
