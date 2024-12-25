#!/usr/bin/env python

from collections import deque
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Iterable, Optional


@dataclass
class Wire:
    name: str
    value: int = -1

    start: Optional["Gate"] = None

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Gate:
    a: "Wire"
    b: "Wire"
    o: "Wire"

    def __post_init__(self) -> None:
        # self.a.end.append(self)
        # self.b.end.append(self)
        self.o.start = self

    def op(self, a, b) -> int:
        raise NotImplementedError()


@dataclass
class AND(Gate):
    def op(self, a, b) -> int:
        return a & b


@dataclass
class OR(Gate):
    def op(self, a, b) -> int:
        return a | b


@dataclass
class XOR(Gate):
    def op(self, a, b) -> int:
        return a ^ b


@dataclass
class Device:
    wires: dict[str, Wire] = field(init=False, default_factory=dict)
    gates: list[Gate] = field(init=False, default_factory=list)

    # circuit is the ends of the "z" wires
    circuit: dict[str, Wire] = field(init=False, default_factory=dict)

    def __str__(self) -> str:
        return "\n".join(f"{name}: {wire.value}" for name, wire in sorted(self.circuit.items(), key=lambda x: x[0]))


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_device(filepath: Path) -> Device:
    input_iter = parse_lines(filepath)
    device: Device = Device()
    wires: dict[str, Wire] = device.wires
    gates: list[Gate] = device.gates
    circuit: dict[str, Wire] = device.circuit

    # parse the wires
    for line in input_iter:
        if line == "":
            break
        name, value = line.strip().split(":")
        wires[name] = Wire(name, int(value.strip()))

    # parse the gates
    for line in input_iter:
        input_op, output = line.strip().split("->")
        o = output.strip()
        a, op, b = input_op.strip().split(" ")

        # handle inputs/output wires
        if a not in wires:
            wires[a] = Wire(a)

        if b not in wires:
            wires[b] = Wire(b)

        if o not in wires:
            wires[o] = Wire(o)

        # create the gate and wire up
        g: Gate
        match op:
            case "AND":
                g = AND(wires[a], wires[b], wires[o])
            case "OR":
                g = OR(wires[a], wires[b], wires[o])
            case "XOR":
                g = XOR(wires[a], wires[b], wires[o])
        gates.append(g)

    # setup circuit
    for name, w in wires.items():
        if name.startswith("z"):
            circuit[w.name] = w

    return device


@cache
def execute_wire(wire: Wire) -> int:
    if wire.value != -1:
        return wire.value

    g: Gate = wire.start
    return g.op(execute_wire(g.a), execute_wire(g.b))


def execute(device: Device) -> int:
    c: list[int] = [execute_wire(w) for _, w in sorted(device.circuit.items(), key=lambda x: x[0], reverse=True)]
    return int("".join(map(str, c)), 2)


def main(filepath: Path):
    device: Device = parse_device(filepath)
    result: int = execute(device)
    print(result)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
