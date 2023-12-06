#!/usr/bin/env python

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from tqdm import tqdm as progressbar


@dataclass
class MappingRange:
    source: int
    dest: int
    length: int

    def __contains__(self, value: int) -> bool:
        return self.source <= value and self.source + self.length > value

    def transform(self, value: int) -> int:
        if value not in self:
            return value

        offset = value - self.source
        output = self.dest + offset
        # print(f"  - {value} -> {output}")
        return output


@dataclass
class Mapping:
    source: str
    destination: str
    ranges: Iterable[MappingRange]
    prev: Optional["Mapping"] = None
    next: Optional["Mapping"] = None

    def tranform(self, seed: int) -> int:
        for r in self.ranges:
            if seed in r:
                return r.transform(seed)

        return seed


@dataclass
class Almanac:
    seeds: Iterable[int]
    mappings: dict[Mapping]


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def create_mapping(lines: list[str]) -> Mapping:
    source_name, _, destination_name = lines[0].split(" ")[0].split("-")
    ranges = []
    for r in lines[1:]:
        destination, source, length = [int(n) for n in r.split(" ")]
        ranges.append(MappingRange(source, destination, length))

    return Mapping(source_name, destination_name, ranges)
    ...


def parse_almanac(filepath: Path) -> Almanac:
    seeds = []
    mappings = {}
    mapping = []
    for line in parse_lines(filepath):
        if line.startswith("seeds:"):
            seeds = [int(s) for s in line.split(":")[1].strip().split(" ")]
            continue

        if line.endswith("map:") or line:
            mapping.append(line)
            continue

        if line == "" and mapping:
            lookup = create_mapping(mapping)
            mappings[lookup.source] = lookup
            mapping = []

    # handle last mapping
    if mapping:
        lookup = create_mapping(mapping)
        mappings[lookup.source] = lookup
        mapping = []

    # setup linked list
    for mapping in mappings.values():
        n = mappings.get(mapping.destination, None)
        mapping.next = n

        if n:
            n.prev = mapping

    return Almanac(seeds=seeds, mappings=mappings)


def main(filepath: Path):
    almanac = parse_almanac(filepath)
    smallest = (2**64) + 1

    for seed in almanac.seeds:
        print(".", end="")

        mapping = almanac.mappings["seed"]
        value = seed

        while mapping:
            current = value
            value = mapping.tranform(current)
            # print(f"  {mapping.source} {current} -> {mapping.destination} {value}")
            mapping = mapping.next

        smallest = min(smallest, value)

    print(f"\nSmallest: {smallest}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
