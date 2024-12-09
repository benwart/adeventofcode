#!/usr/bin/env python

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class File:
    id: int
    blocks: int
    moved: int = 0


@dataclass
class Space:
    blocks: int


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_blocks(filepath: Path) -> Iterable[tuple[File, Space]]:
    line: str = next(parse_lines(filepath))

    for i, j in enumerate(range(0, len(line), 2)):
        file: File = File(i, int(line[j]))
        space: int = Space(int(line[j + 1]) if j + 1 < len(line) else 0)
        yield file, space


def backward_files_iter(blocks: list[File | Space]) -> Iterable[int]:
    while len(blocks) > 0:
        block = blocks[-1]
        match block:
            case File():
                for _ in range(block.blocks):
                    block.moved += 1
                    yield block.id

                    # if we exhaust all the values remove from the list
                    if block.moved == block.blocks:
                        blocks.pop()
                        break
            case Space():
                # when we run into space at the end of the list
                # throw is away to compress the output list
                blocks.pop()

    return


def main(filepath: Path):
    blocks: list[File | Space] = []
    file: File
    space: Space
    for file, space in parse_blocks(filepath):
        blocks.append(file)
        if space.blocks > 0:
            blocks.append(space)

    backward: Iterable[int] = backward_files_iter(blocks)

    compacted: list[int] = []
    front: File | Space
    while len(blocks) > 0:
        front = blocks.pop(0)
        match front:
            case File():
                compacted.extend([front.id] * (front.blocks - front.moved))
            case Space():
                compacted.extend([next(backward) for _ in range(front.blocks)])

    # compute checksum

    checksum: int = sum([i * id for i, id in enumerate(compacted)])
    print(checksum)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
