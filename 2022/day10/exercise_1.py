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


def main():
    cycle = 0
    value_at_cycle = [1]
    for i in parse_instructions("2022/day10/data/full"):
        print(i)

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

    print(value_at_cycle)

    check_values = [20, 60, 100, 140, 180, 220]
    total = 0
    for i in check_values:
        signal_strength = i * value_at_cycle[i]
        total += signal_strength
        print(f"{i} - {value_at_cycle[i] = }, {signal_strength = }")

    print(f"{total = }")


if __name__ == "__main__":
    main()
