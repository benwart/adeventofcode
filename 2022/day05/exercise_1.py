#!/usr/bin/env python3

from collections import deque, defaultdict
from dataclasses import dataclass
from re import compile

MOVE_REGEX = compile(
    r"move (?P<count>\d+) from (?P<source>\d+) to (?P<destination>\d+)"
)


def parse_lines(filepath: str):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_stacks(filepath: str):
    stack_lines = []
    for line in parse_lines(filepath):
        if line:
            stack_lines.append(line)
        else:
            break

    # stacks has the format of a bunch of stacks divided into columns.
    # the stack number is located at the bottom so start there.
    last_row = stack_lines[-1]
    column_indices = [
        index for index, value in enumerate(last_row) if value.isnumeric()
    ]

    stacks = defaultdict(deque)

    # since we're using deques we can just do lpush to make sure the top is on the right and bottom is to the left
    for line in stack_lines[0:-1]:
        for index, column in enumerate(column_indices):
            stack_value = line[column]
            if stack_value.isalpha():
                stacks[index + 1].appendleft(stack_value)

    return stacks


@dataclass
class Move:
    count: int
    source: int
    destination: int


def parse_moves(filepath: str):
    moves = []

    for line in parse_lines(filepath):
        m = MOVE_REGEX.match(line)
        if m:
            groups = m.groupdict()
            moves.append(
                Move(
                    int(groups["count"]),
                    int(groups["source"]),
                    int(groups["destination"]),
                )
            )

    return moves


def apply_move(stacks, move: Move):
    """This function will modify the stacks in place."""

    for _ in range(move.count):
        stacks[move.destination].append(stacks[move.source].pop())


def main():
    filepath = "2022/day05/data/full"
    stacks = parse_stacks(filepath)
    moves = parse_moves(filepath)

    for move in moves:
        apply_move(stacks, move)

    sorted_keys = sorted(stacks.keys())
    top_of_stacks = []

    for key in sorted_keys:
        stack = stacks[key]
        top = stack.pop()
        top_of_stacks.append(top)
        print(f"{key}: {top}")

    print("".join(top_of_stacks))


if __name__ == "__main__":
    main()
