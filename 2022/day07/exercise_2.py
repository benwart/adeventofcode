#!/usr/bin/env python3

from functools import cache
from dataclasses import dataclass, field
from typing import Iterable
from pathlib import Path
from enum import StrEnum
from collections import deque


def parse_lines(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


class CommandType(StrEnum):
    CD = "cd"
    LS = "ls"


def parse_command(line: str) -> tuple[CommandType, str | None]:
    args = line.split(" ")
    return CommandType(args[1]), args[2] if len(args) > 2 else None


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    path: Path
    subdirs: list["Directory"] = field(default_factory=list)
    files: list[File] = field(default_factory=list)
    listed: bool = False

    def __hash__(self) -> int:
        return hash(self.path)

    @cache
    def size(self) -> int:
        total = 0
        for dir in walk_directory(self):
            total += sum([file.size for file in dir.files])

        return total


def parse_output(line: str, cwd: Path) -> File | Directory:
    args = line.split(" ")

    if args[0] == "dir":
        dirname = args[1]
        return Directory(cwd / dirname)
    else:
        filesize = int(args[0])
        filename = args[1]
        return File(filename, filesize)


def walk_directory(dir: Directory) -> Iterable[Directory]:
    dirs = deque([dir])
    while dirs:
        cwd = dirs.popleft()
        yield cwd

        for subdir in cwd.subdirs:
            dirs.append(subdir)


def print_dir_tree(root: Directory):
    for dir in walk_directory(root):
        print(f"{dir.path} (size: {dir.size()})")

        # for f in dir.files:
        #     print(f" - {f.name}")


def parse_console(filepath: str):
    cwd = Path("/")
    parent = None
    directories: dict[Path, Directory] = {}

    for line in parse_lines(filepath):
        if line.startswith("$"):
            cmd_type, cmd_arg = parse_command(line)

            match cmd_type:
                case CommandType.CD:
                    match cmd_arg:
                        case "..":
                            cwd = cwd.parent
                        case "/":
                            cwd = Path("/")
                        case _:
                            cwd /= cmd_arg

                    # add this to the map of directories if it isn't already there
                    if cwd not in directories:
                        directories[cwd] = Directory(cwd)

                    # set the parent for use when handling output
                    parent = directories[cwd]

                case CommandType.LS:
                    directories[cwd].listed = True

            # print(f"{cwd} - {cmd_type} with {cmd_arg}")

        else:
            output = parse_output(line, cwd)

            match output:
                case Directory():
                    parent.subdirs.append(output)

                    if output.path not in directories:
                        directories[output.path] = output

                case File():
                    parent.files.append(output)

    return directories


def main():
    directories = parse_console("2022/day07/data/full")
    root = directories[Path("/")]

    # print_dir_tree(root)

    total_device_size = 70000000
    upgrade_space_size = 30000000
    delta_to_upgrade_size = upgrade_space_size - (total_device_size - root.size())

    print(f"total used space = {root.size()}")
    print(f"total device space = {total_device_size}")
    print(f"upgrade space needed = {upgrade_space_size}")
    print(f"delta to be able to upgrade = {delta_to_upgrade_size}")

    large_dirs = [
        dir for dir in directories.values() if dir.size() >= delta_to_upgrade_size
    ]
    large_dirs.sort(key=lambda d: d.size())
    # for dir in large_dirs:
    #     print(f"{dir.path}: {dir.size()} (delta: {dir.size() - delta_to_upgrade_size})")

    dir = large_dirs[0]
    print(f"{dir.path}: {dir.size()} (delta: {dir.size() - delta_to_upgrade_size})")


if __name__ == "__main__":
    main()
