#!/usr/bin/env python3


from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
from math import floor
from typing import Iterable, Callable
from operator import add, mul


def parse_lines(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.strip()


op_loookup = {
    "+": add,
    "*": mul,
}


@dataclass
class Operation:
    a: str
    b: str
    operator: Callable[[int, int], int]

    def operate(self, old: int) -> int:
        a = old if self.a == "old" else int(self.a)
        b = old if self.b == "old" else int(self.b)
        return self.operator(a, b)


@dataclass
class Test:
    divisible: int
    if_true: int
    if_false: int


MOD_CONSTANT = 1


@dataclass
class Monkey:
    id: int
    items: deque[int]
    op: Operation
    test: Test
    inspections: int = field(default=0)

    def inspect_item(self, item: int) -> int:
        self.inspections += 1
        return (self.op.operate(old=item)) % MOD_CONSTANT

    def test_item(self, item: int, monkeys: list["Monkey"]):
        if item % self.test.divisible == 0:
            monkeys[self.test.if_true].items.append(item)
        else:
            monkeys[self.test.if_false].items.append(item)


def parse_monkey(lines: list[str]) -> Monkey:
    global MOD_CONSTANT
    no_headers = [l.split(":")[1].lstrip() for l in lines[1:]]

    id = int(lines[0].split(" ")[1].rstrip().replace(":", ""))
    items = deque([int(i) for i in no_headers[0].split(", ")])
    operation = no_headers[1].split("=")[1].strip().split(" ")
    divisible = int(no_headers[2].split(" ")[2])
    if_true = int(no_headers[3].split(" ")[3])
    if_false = int(no_headers[4].split(" ")[3])

    # this is used to reduce the size of the worry but not change the results
    MOD_CONSTANT *= divisible

    return Monkey(
        id,
        items,
        Operation(operation[0], operation[2], op_loookup[operation[1]]),
        Test(divisible, if_true, if_false),
    )


def parse_monkeys(filepath: str) -> Iterable[Monkey]:
    lines = []

    # accumulate until we have 6 lines
    for line in parse_lines(filepath):
        if line:
            lines.append(line)

        if len(lines) == 6:
            yield parse_monkey(lines)
            lines = []


def relief_adjustment(item: int) -> int:
    return int(floor(item / 3.0))


def main():
    monkeys = [m for m in parse_monkeys("2022/day11/data/full")]
    print(monkeys)

    rounds = 10000

    check_rounds = {1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000}

    for round in range(rounds):
        # print(round)

        for monkey in monkeys:

            while monkey.items:
                item = monkey.items.popleft()

                # inspect = apply operation
                item = monkey.inspect_item(item)

                # test and throw item = check divisible by value then throw if true/false
                monkey.test_item(item, monkeys)

        if round + 1 in check_rounds:
            print(f"== After round {round + 1} ==")
            for monkey in monkeys:
                print(
                    f"Monkey {monkey.id} inspected items {str(monkey.inspections)} times."
                )

            print("")

    top_monkeys = sorted([m.inspections for m in monkeys], reverse=True)[:2]

    print(f"\nmonkey business: {reduce(mul, top_monkeys)}")


if __name__ == "__main__":
    main()
