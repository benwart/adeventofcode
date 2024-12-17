#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


def execute(registers: dict[str, int], program: list[int]) -> str:
    pointer: int = 0
    output: list[str] = []

    def combo(operand: int) -> int:
        match operand:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return registers["A"]
            case 5:
                return registers["B"]
            case 6:
                return registers["C"]

    while True:
        if pointer >= len(program):
            break

        opcode: int = program[pointer]
        operand: int = program[pointer + 1]
        coperand: int = combo(operand)

        match opcode:
            case 0:
                # adv
                value = registers["A"] // 2**coperand
                registers["A"] = value
                pointer += 2
            case 1:
                # bxl
                value = registers["B"] ^ operand
                registers["B"] = value
                pointer += 2
            case 2:
                # bst
                value = coperand % 8
                registers["B"] = value
                pointer += 2
            case 3:
                # jnz
                if registers["A"] != 0:
                    pointer = operand
                else:
                    pointer += 2
            case 4:
                # bxc
                value = registers["B"] ^ registers["C"]
                registers["B"] = value
                pointer += 2
            case 5:
                # out
                output.append(f"{coperand % 8}")
                pointer += 2
            case 6:
                # bdv
                value = registers["A"] // 2**coperand
                registers["B"] = value
                pointer += 2
            case 7:
                # cdv
                value = registers["A"] // 2**coperand
                registers["C"] = value
                pointer += 2

    return ",".join(output)


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    registers: dict[str, int] = {}
    program: list[int] = []

    for line in parse_lines(filepath):
        if line.startswith("Register"):
            register_split: list[str] = line.split(":")
            key: str = register_split[0].split(" ")[1]
            value: int = int(register_split[1].strip())
            registers[key] = value

        elif line.startswith("Program"):
            program = list(map(int, line.split(":")[1].strip().split(",")))

    output: str = execute(registers, program)
    print(output)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
