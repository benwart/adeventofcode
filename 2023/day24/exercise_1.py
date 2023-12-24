#!/usr/bin/env python

from pathlib import Path
from typing import Iterable

from euclid import Point2, Ray2, Vector2


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_rays(lines: Iterable[str]) -> Iterable[Ray2]:
    for line in lines:
        point, vector = line.split(" @ ")
        p = Point2(*tuple(map(int, point.split(",")[0:2])))
        v = Vector2(*tuple(map(int, vector.split(",")[0:2])))
        yield Ray2(p, v)


def intersections_between(
    rays: list[Ray2],
) -> Iterable[Point2]:
    for i, n in enumerate(rays[:-1]):
        for m in rays[i + 1 :]:
            intersection = n.intersect(m)
            if intersection:
                yield intersection


def main(filepath: Path):
    bound_min = 200000000000000
    bound_max = 400000000000000

    total = 0
    rays = list(parse_rays(parse_lines(filepath)))
    for intersection in intersections_between(rays):
        if bound_min <= intersection.x <= bound_max and bound_min <= intersection.y <= bound_max:
            total += 1

    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
