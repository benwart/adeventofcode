#!/usr/bin/env python
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Iterable

from tqdm import tqdm


@dataclass(frozen=True)
class PriceDelta:
    price: int
    delta: int


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


def price_deltas(secret: int, n: int = 2000) -> list[PriceDelta]:
    prices: list[tuple[int, int | None]] = []
    price: int = secret % 10
    for _ in range(n):
        ns: int = next_secret(secret)
        np: int = ns % 10
        d: int = np - price

        prices.append(PriceDelta(np, d))

        price = np
        secret = ns
    return prices


def price_by_deltas(secret_deltas: list[PriceDelta]) -> dict[tuple[int, ...], int]:
    output: dict[tuple[int, ...], int] = {}

    j: int = 3
    for j in range(j, len(secret_deltas)):
        deltas = (
            secret_deltas[j - 3].delta,
            secret_deltas[j - 2].delta,
            secret_deltas[j - 1].delta,
            secret_deltas[j].delta,
        )

        # only care about the first instance of deltas
        if deltas not in output:
            output[deltas] = secret_deltas[j].price

    return output


def main(filepath: Path):
    secrets: list[int] = [int(line) for line in parse_lines(filepath)]
    secret_deltas: list[list[PriceDelta]] = [price_deltas(s, 2000) for s in secrets]
    secret_price_by_deltas: list[dict[tuple[int, ...], int]] = [price_by_deltas(sd) for sd in secret_deltas]

    iterations: int = 1
    for groups in secret_price_by_deltas:
        iterations *= len(groups)

    groups_seen: set[tuple[int, ...]] = set()
    most_bananas: int = 0

    for i, spd in enumerate(secret_price_by_deltas):
        for deltas, price in tqdm(spd.items()):
            if deltas in groups_seen:
                continue

            total: int = price
            for j, spd in enumerate(secret_price_by_deltas):
                if i == j:
                    continue

                total += spd.get(deltas, 0)

            if total > most_bananas:
                most_bananas = total

            groups_seen.add(deltas)

    print(most_bananas, len(groups_seen))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
