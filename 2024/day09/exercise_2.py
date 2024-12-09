#!/usr/bin/env python

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class File:
    id: int
    blocks: int


@dataclass
class Space:
    id: int
    blocks: int


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_blocks(filepath: Path) -> Iterable[tuple[File, Space]]:
    line: str = next(parse_lines(filepath))

    for i, j in enumerate(range(0, len(line), 2)):
        file: File = File(i, int(line[j]))
        space: int = Space(i, int(line[j + 1]) if j + 1 < len(line) else 0)
        yield file, space


def print_blocks(blocks: list[File | Space]) -> str:
    output: list[str] = []
    for block in blocks:
        match block:
            case File():
                output.append(f"{block.id}" * block.blocks)
            case Space():
                output.append("." * block.blocks)

    return "".join(output)


def render_blocks(blocks: list[File | Space]) -> list[int]:
    output: list[int] = []
    for block in blocks:
        match block:
            case File():
                output.extend([block.id] * block.blocks)
            case Space():
                output.extend([-1] * block.blocks)

    return output


def main(filepath: Path):
    blocks: list[File | Space] = []
    file: File
    space: Space
    for file, space in parse_blocks(filepath):
        blocks.extend([file, space])

    # print(print_blocks(blocks))

    files_reversed: list[File] = [b for b in reversed(blocks) if isinstance(b, File)]
    spaces: list[Space] = [b for b in blocks if isinstance(b, Space)]

    file: File
    for file in files_reversed:
        # can we move the file to a lower position
        for space in spaces:
            if space.id >= file.id:
                break

            if space.blocks >= file.blocks:
                s: int = blocks.index(space)
                f: int = blocks.index(file)

                # replace the file by extending the space after the file
                file_block: File = blocks.pop(f)

                # if there is no space after the just popped file
                if isinstance(blocks[f], Space):
                    blocks[f].blocks += file.blocks
                else:
                    # add a new space
                    blocks.insert(f, Space(file.id, file.blocks))

                # move the file before the open space and resize the space
                blocks.insert(s, file_block)
                space.blocks -= file.blocks
                break

    # print(print_blocks(blocks))

    # compute checksum
    checksum: int = sum([i * id for i, id in enumerate(render_blocks(blocks)) if id >= 0])
    print(checksum)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
