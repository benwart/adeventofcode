#!/usr/bin/env python

from pathlib import Path
from typing import Iterable

from networkx import DiGraph
from networkx.algorithms.simple_paths import all_simple_paths


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_row(line: str) -> tuple[str, list[str]]:
    name, outputs = line.split(": ")
    return name, outputs.split(" ")


def main(filepath: Path):
    nodes: set[str] = set()
    edges: list[tuple[str, list[str]]] = []
    for line in parse_lines(filepath):
        name, outputs = parse_row(line)
        nodes.add(name)
        nodes |= {o for o in outputs}
        edges.append(
            (
                name,
                outputs,
            )
        )

    graph: DiGraph = DiGraph()
    for node in nodes:
        graph.add_node(node)

    for src, outputs in edges:
        for dst in outputs:
            graph.add_edge(src, dst)

    total: int = 0
    for path in all_simple_paths(graph, "svr", "out"):
        if "fft" in path and "dac" in path:
            print(path)
            total += 1

    print("\n", total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
