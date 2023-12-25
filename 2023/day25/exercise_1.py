#!/usr/bin/env python

from pathlib import Path
from typing import Iterable

from matplotlib.pyplot import show
from networkx import Graph, draw_spring, connected_components


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_connections(lines: Iterable[str]) -> Graph:
    graph: Graph = Graph()
    nodes: set[str] = set()
    for line in lines:
        a, multi = line.split(": ")
        if a not in nodes:
            nodes.add(a)
            graph.add_node(a)

        for m in multi.split(" "):
            if m not in nodes:
                nodes.add(m)
                graph.add_node(m)

            graph.add_edge(a, m)

    return graph


def main(filepath: Path):
    graph = parse_connections(parse_lines(filepath))

    # draw_spring(graph, with_labels=True)
    # show()

    # remove edges
    graph.remove_edge("ttj", "rpd")
    graph.remove_edge("htp", "vps")
    graph.remove_edge("fqn", "dgc")

    # count nodes in clusters
    a, b = connected_components(graph)

    draw_spring(graph, with_labels=True)
    show()
    print("Part 1:", len(a) * len(b))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
