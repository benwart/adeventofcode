#!/usr/bin/env python3


from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


def parse_lines(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


class Command(Enum):
    ADDX = "addx"
    NOOP = "noop"


@dataclass
class Instruction:
    cmd: Command
    arg: int | None = field(default=None)


def parse_instructions(filepath: str) -> Iterable[Instruction]:
    for line in parse_lines(filepath):
        tokens = line.split(" ")
        yield Instruction(
            Command(tokens[0]), int(tokens[1]) if len(tokens) > 1 else None
        )


instruction_cycles = {
    Command.ADDX: 2,
    Command.NOOP: 1,
}


def compute_value_at_cycle(filepath: str) -> list[int]:
    cycle = 0
    value_at_cycle = [1]

    for i in parse_instructions(filepath):
        # working cycles
        for _ in range(instruction_cycles[i.cmd]):
            cycle += 1

            if len(value_at_cycle) <= cycle:
                value_at_cycle.append(value_at_cycle[cycle - 1])

        # updating cycle
        if i.arg:
            value_at_cycle.append(value_at_cycle[cycle] + i.arg)
        else:
            value_at_cycle.append(value_at_cycle[cycle])

    return value_at_cycle


def pixel_in_sprint(pixel, value) -> bool:
    sprite_location = [value - 1, value, value + 1]
    return pixel in sprite_location


def main():

    value_at_cycle = compute_value_at_cycle("2022/day10/data/full")

    # render the sprite position at each cycle
    row_indices = [
        (1, 40),
        (41, 80),
        (81, 120),
        (121, 160),
        (161, 200),
        (201, 240),
    ]

    display: list[list[str]] = []
    for s, e in row_indices:
        row = ["." for _ in range(40)]
        display.append(row)
        for x, value in enumerate(value_at_cycle[s:e]):
            row[x] = "." if not pixel_in_sprint(x, value) else "#"

    for row in display:
        print("".join(row))


if __name__ == "__main__":
    main()
