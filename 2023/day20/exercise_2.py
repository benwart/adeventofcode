#!/usr/bin/env python

from collections import deque
from dataclasses import dataclass, field, InitVar
from enum import StrEnum
from pathlib import Path
from typing import Deque, Iterable, override

from colorama import Fore, Style


class ModuleType(StrEnum):
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    BROADCASTER = "BROADCASTER"
    BUTTON = "BUTTON"
    TEST = "TEST"


module_types = {
    "%": ModuleType.FLIP_FLOP,
    "&": ModuleType.CONJUNCTION,
    "broadcaster": ModuleType.BROADCASTER,
    "button": ModuleType.BUTTON,
    "test": ModuleType.TEST,
}


class PulseType(StrEnum):
    HIGH = "H"
    LOW = "L"


@dataclass
class Pulse:
    source: "Module"
    type: PulseType
    destination: "Module"

    def __str__(self) -> str:
        return f"{self.source.id} -{self.type.name.lower()}-> {self.destination.id}"


@dataclass
class Processor:
    module: "Module"

    def init(self, modules: dict[str, "Module"]) -> None:
        ...

    def process(self, source: "Module", pulse: PulseType, modules: dict[str, "Module"]) -> list[Pulse]:
        ...


@dataclass
class Test(Processor):
    """
    Test module that does nothing.
    """

    @override
    def process(self, source: "Module", pulse: PulseType, modules: dict[str, "Module"]) -> list[Pulse]:
        if self.module.id == "rx" and pulse == PulseType.LOW:
            print(f"{Fore.YELLOW}{Style.BRIGHT}{self.module.id} -{pulse.name.lower()}-> {source.id}{Style.RESET_ALL}")

        return []


class FlipFlopState(StrEnum):
    ON = "ON"
    OFF = "OFF"


flipflop_toggle = {
    FlipFlopState.ON: FlipFlopState.OFF,
    FlipFlopState.OFF: FlipFlopState.ON,
}


@dataclass
class FlipFlop(Processor):
    """
    Flip-flop modules (prefix %) are either on or off; they are initially off.
    If a flip-flop module receives a high pulse, it is ignored and nothing happens.
    However, if a flip-flop module receives a low pulse, it flips between on and off.
    If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
    """

    state: FlipFlopState = FlipFlopState.OFF

    @override
    def process(self, source: "Module", pulse: PulseType, modules: dict[str, "Module"]) -> list[Pulse]:
        if pulse == PulseType.HIGH:
            return []

        self.state = flipflop_toggle[self.state]
        pulse_type: PulseType = PulseType.HIGH if self.state == FlipFlopState.ON else PulseType.LOW
        return [Pulse(self.module, pulse_type, modules[c]) for c in self.module.connections]


@dataclass
class Conjunction(Processor):
    """
    Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules;
    they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first
    updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends
    a high pulse.
    """

    memory: dict[str, PulseType] = field(default_factory=dict)

    @override
    def init(self, modules: dict[str, "Module"]) -> None:
        for module in modules.values():
            if module.id == self.module.id:
                continue

            for c in module.connections:
                if c == self.module.id:
                    self.memory[module.id] = PulseType.LOW

    @override
    def process(self, source: "Module", pulse: PulseType, modules: dict[str, "Module"]) -> list[Pulse]:
        self.memory[source.id] = pulse
        pulse_type = PulseType.LOW if all([v == PulseType.HIGH for v in self.memory.values()]) else PulseType.HIGH

        # add in any test modules that are not already in modules
        for c in self.module.connections:
            if c not in modules:
                modules[c] = Module(c, "")

        return [Pulse(self.module, pulse_type, modules[c]) for c in self.module.connections]


@dataclass
class Broadcaster(Processor):
    """
    There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.
    """

    @override
    def process(self, source: "Module", pulse: PulseType, modules: dict[str, "Module"]) -> list[Pulse]:
        return [Pulse(self.module, pulse, modules[c]) for c in self.module.connections]


@dataclass
class Button(Processor):
    """
    Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly, the button module. When you push the button,
    a single low pulse is sent directly to the broadcaster module.

    After pushing the button, you must wait until all pulses have been delivered and fully handled before pushing it again. Never push the button
    if modules are still processing pulses.
    """

    @override
    def process(self, source: "Module", pulse: PulseType, modules: dict[str, "Module"]) -> list[Pulse]:
        return [Pulse(self.module, PulseType.LOW, modules[self.module.connections[0]])]


processor_types = {
    ModuleType.FLIP_FLOP: FlipFlop,
    ModuleType.CONJUNCTION: Conjunction,
    ModuleType.BROADCASTER: Broadcaster,
    ModuleType.BUTTON: Button,
    ModuleType.TEST: Test,
}


@dataclass
class Module:
    module_str: InitVar[str]
    connections_str: InitVar[str]

    id: str = field(init=False)
    type: ModuleType = field(init=False)
    processor: Processor = field(init=False, repr=False)
    connections: Iterable[str] = field(init=False)

    def __post_init__(self, module_str: str, connections_str: str) -> None:
        self.type = ModuleType.TEST
        for k, v in module_types.items():
            if module_str.startswith(k):
                self.type = v
                break

        self.id = module_str[1:]
        if self.type in [ModuleType.BROADCASTER, ModuleType.BUTTON, ModuleType.TEST]:
            self.id = module_str

        self.processor = processor_types[self.type](self)
        self.connections = [c.strip() for c in connections_str.split(",")]

    def __str__(self) -> str:
        id = f"{Fore.GREEN}{Style.BRIGHT}{self.id}{Style.RESET_ALL}"
        type = f"{Style.DIM}{self.type.name}{Style.RESET_ALL}"
        connections = f"{Fore.BLUE}{', '.join(self.connections)}{Style.RESET_ALL}"
        return f"{id} ({type}) -> {connections}"

    def pulse(self, source: "Module", pulse: PulseType, modules: dict[str, "Module"]) -> list[Pulse]:
        return self.processor.process(source, pulse, modules)


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_modules(lines: Iterable[str]) -> Iterable[str]:
    for line in lines:
        module, connections = line.split(" -> ")
        m = Module(module.strip(), connections)
        yield m

        if m.type == ModuleType.BROADCASTER:
            yield Module("button", "broadcaster")


def push_button(modules: dict[str, Module]) -> None:
    queue: Deque[Pulse] = deque([Pulse(modules["button"], PulseType.LOW, modules["broadcaster"])])
    high_pulses: list[Pulse] = []
    low_pulses: list[Pulse] = []

    while len(queue) > 0:
        current = queue.popleft()  # get next pulse

        if current.type == PulseType.HIGH:
            high_pulses.append(current)
        else:
            low_pulses.append(current)

        # print(current)

        # process pulse and add new pulses to queue
        queue.extend(current.destination.pulse(current.source, current.type, modules))

    return len(high_pulses), len(low_pulses)


def main(filepath: Path):
    modules: dict[str, Module] = {m.id: m for m in parse_modules(parse_lines(filepath))}

    # initialize modules
    for module in modules.values():
        module.processor.init(modules)

    high_total: int = 0
    low_total: int = 0

    # push the button
    for _ in range(10000):
        high_pulses, low_pulses = push_button(modules)
        high_total += high_pulses
        low_total += low_pulses

    # compute the results
    result = high_total * low_total
    print(f"Result: {result}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
