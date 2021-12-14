#!/usr/bin/env python3

from collections import defaultdict
from llist import dllist
from parser import parse_data


if __name__ == "__main__":
    template, insertions = parse_data("./2021/day14/data/full")

    steps = 10
    state = dllist(template)

    print(f"Template: {template}")

    for step in range(1, steps+1):
        for node in state.iternodes():
            if node.prev is not None:
                search = "".join([node.prev.value, node.value])
                insert = insertions[search]
                state.insertbefore(insert, node)

        # print(f"After step {step}: {''.join(state.itervalues())}")

    # count min and max values
    counts = defaultdict(lambda: 0)

    for value in state.itervalues():
        counts[value] += 1

    min_element = min(counts.items(), key=lambda t: t[1])
    max_element = max(counts.items(), key=lambda t: t[1])

    print(f"min: {min_element}")
    print(f"max: {max_element}")
    print(f"delta: {max_element[1] - min_element[1]}")