#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def mix(value: int, secret: int) -> int:
    return value ^ secret  # bitwise xor


def prune(secret: int) -> int:
    return secret % 16777216  # modulo


def next_secret(secret: int) -> int:
    value: int = prune(mix(secret * 64, secret))
    value = prune(mix(value // 32, value))
    value = prune(mix(value * 2048, value))
    return value


def nth_secret(secret: int, n: int = 2000) -> int:
    for _ in range(n):
        secret = next_secret(secret)
    return secret


def main(filepath: Path):
    secrets: list[int] = [int(line) for line in parse_lines(filepath)]
    results: list[int] = [nth_secret(s) for s in secrets]
    print(sum(results))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
