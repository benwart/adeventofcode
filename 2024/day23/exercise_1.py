#!/usr/bin/env python

from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Iterable


@dataclass
class Triplet:
    a: str
    b: str
    c: str
    s: str = field(init=False)

    def __post_init__(self) -> None:
        self.s = ",".join(sorted([self.a, self.b, self.c]))

    def __eq__(self, other: "Triplet") -> bool:
        return self.s == other.s

    def __hash__(self) -> int:
        return hash(self.s)

    def starts_with(self, value: str) -> bool:
        for v in [self.a, self.b, self.c]:
            if v.startswith(value):
                return True
        return False


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    graph: dict[str, set[str]] = {}
    for line in parse_lines(filepath):
        [left, right] = line.split("-")
        if left not in graph:
            graph[left] = set()
        graph[left].add(right)

        if right not in graph:
            graph[right] = set()
        graph[right].add(left)

    triplets: dict[Triplet, int] = {}

    # walk the graph
    for node, edges in graph.items():
        if len(edges) >= 2:
            for e1, e2 in combinations(edges, r=2):
                if e1 == e2:
                    continue

                t: Triplet = Triplet(node, e1, e2)
                if t not in triplets:
                    triplets[t] = 1
                    continue
                else:
                    triplets[t] += 1

    count: int = 0
    for t, i in triplets.items():
        if i == 3 and t.starts_with("t"):
            print(t, i)
            count += 1

    print(count)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
