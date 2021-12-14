#!/usr/bin/env python3

from collections import defaultdict
from llist import dllist
from parser import parse_data


def iteration(step, insertions, state):
    for node in state.iternodes():
        if node.prev is not None:
            search = "".join([node.prev.value, node.value])
            insert = insertions[search]
            state.insertbefore(insert, node)

    if step % 10 == 0:
        print(".")
    else:
        print(".", end="")


def main():
    template, insertions = parse_data("./2021/day14/data/example_1")

    steps = 30
    state = dllist(template)

    print(f"Template: {template}")

    for step in range(1, steps+1):
        iteration(step, insertions, state)

    # count min and max values
    counts = defaultdict(lambda: 0)

    for value in state.itervalues():
        counts[value] += 1

    min_element = min(counts.items(), key=lambda t: t[1])
    max_element = max(counts.items(), key=lambda t: t[1])

    print(f"min: {min_element}")
    print(f"max: {max_element}")
    print(f"delta: {max_element[1] - min_element[1]}")


if __name__ == "__main__":
    main()

    # TODO switch to counting the pairs rather than growing the string