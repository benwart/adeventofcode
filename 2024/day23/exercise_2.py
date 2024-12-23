#!/usr/bin/env python

from dataclasses import dataclass, field
from functools import cache
from itertools import combinations
from pathlib import Path
from typing import Iterable

from tqdm import tqdm


@dataclass
class Group:
    n: set[str]
    s: str = field(init=False)

    def __post_init__(self) -> None:
        self.s = ",".join(sorted(self.n))

    def __eq__(self, other: "Group") -> bool:
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


def parse_graph(filepath: Path) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for line in parse_lines(filepath):
        [left, right] = line.split("-")
        if left not in graph:
            graph[left] = set()
        graph[left].add(right)

        if right not in graph:
            graph[right] = set()
        graph[right].add(left)
    return graph


def main(filepath: Path):
    graph: dict[str, set[str]] = parse_graph(filepath)

    @cache
    def group_intersection(*args) -> set[str]:
        return graph[args[0]].intersection(*map(graph.get, args[1:]))

    nodes: list[str] = sorted(graph.keys(), key=lambda n: len(graph[n]), reverse=True)
    clusters: dict[Group, int] = {}

    # walk the graph
    # for n in tqdm(nodes):
    for n in nodes:
        ne: set[str] = graph[n]
        sets: dict[set[str]] = {n: ne}
        for nn in ne:
            sets[nn] = graph[nn]

        group_counts: dict[int, int] = {}
        groups: dict[tuple[str, ...], set[str]] = {}
        for r in range(3, len(sets)):
            for tn in combinations(sets.keys(), r=r):
                if tn:
                    combined: set[str] = group_intersection(*tn)
                    lc: int = len(combined)
                    if lc not in group_counts:
                        group_counts[lc] = 1
                    group_counts[lc] += 1
                    groups[tuple(sorted(tn))] = combined

        if group_counts:
            print(max(group_counts.keys()))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
