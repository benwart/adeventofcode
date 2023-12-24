#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from shapely import Polygon, Point, box


@dataclass
class Brick:
    corners: list[Point]
    box: Polygon = field(init=False)
    top: int = field(init=False)
    bottom: int = field(init=False)

    def __post_init__(self):
        self.top = int(max([p.z for p in self.corners])) + 1
        self.bottom = int(min([p.z for p in self.corners]))
        max_x = max([p.x for p in self.corners]) + 1
        min_x = min([p.x for p in self.corners])
        max_y = max([p.y for p in self.corners]) + 1
        min_y = min([p.y for p in self.corners])
        self.box = box(min_x, min_y, max_x, max_y)

    def __str__(self) -> str:
        return f"{"~".join([str(corner) for corner in self.corners])} - {self.box}, {self.top}, {self.bottom}"
    

    def overlap(self, other: "Brick") -> bool:
        return self.box.intersects(other.box)   


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_bricks(filepath: Path) -> Iterable[Brick]:
    for line in parse_lines(filepath):
        points = line.strip().split("~")
        yield Brick([Point(p.strip().split(",")) for p in points])

def condense(bricks: list[Brick]) -> list[Brick]:
    done = False
    loops = 0
    while not done:
        movement = False
        loops += 1
        for i, brick in enumerate(bricks[:-1]):
            shifted = False
            for below in bricks[i+1:]:
                if brick.overlap(below):
                    # print(f"{brick} overlaps {below}")
                    shift = brick.bottom - below.top
                    brick.bottom -= shift
                    brick.top -= shift
                    shifted = True
                    movement = movement or shift > 0
                    break
            
            if not shifted:
                # no overlapping bricks found
                shift = brick.bottom - brick.bottom
                brick.bottom -= shift
                brick.top -= shift
                movement = movement or shift > 0

        done = not movement

    return bricks
            

def main(filepath: Path):
    bricks = sorted(parse_bricks(filepath), reverse=True, key=lambda b: b.bottom)
    bricks = condense(bricks)
    for brick in bricks:
        print(brick)
    

if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
