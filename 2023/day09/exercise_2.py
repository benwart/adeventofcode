#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class Layer:
    values: list[int]
    done: bool = field(init=False)

    def __post_init__(self):
        self.done = all([n == 0 for n in self.values])


def predict_next_layer(layer: Layer) -> Layer:
    values = []
    for i, n in enumerate(layer.values[:-1]):
        m = layer.values[i + 1]
        values.append(m - n)

    return Layer(values)


def predict_next_value(upper: Layer, lower: Layer) -> int:
    return lower.values[-1] + upper.values[-1]


@dataclass
class Report:
    values: Layer

    def prediction(self) -> int:
        layer = self.values
        layers: list[Layer] = []
        layers.append(layer)
        not_done = not layer.done

        while not_done:
            layer = predict_next_layer(layer)
            layers.append(layer)
            not_done = not layer.done

        layers = list(reversed(layers))

        for i, lower in enumerate(layers[:-1]):
            upper = layers[i + 1]
            upper.values.append(predict_next_value(upper, lower))

        return layers[-1].values[-1]


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_reports(filepath: Path) -> Iterable[Report]:
    for line in parse_lines(filepath):
        values = list(reversed([int(value) for value in line.split(" ")]))
        yield Report(Layer(values))


def main(filepath: Path):
    total = 0
    for report in parse_reports(filepath):
        print(report)
        value = report.prediction()
        total += value

    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
