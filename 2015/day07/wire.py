import numpy as np


def to_uint16(value):
    return np.array([value], dtype="uint16")[0]


class Literal:
    def __init__(self, value):
        self._value = to_uint16(value)

    def __repr__(self):
        return f"Literal({self.value})"

    @property
    def value(self):
        return self._value


class Wire:
    def __init__(self, id: str):
        self.id = id
        self._input = None
        self._outputs = []
        self._value = None

    def __repr__(self):
        return f"Wire({self.id})"

    def __iadd__(self, output):
        self.outputs.append(output)

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, input):
        self._input = input

    @property
    def outputs(self):
        return self._outputs

    @property
    def value(self):
        if self._value == None:
            self._value = to_uint16(self.input.value)
        return self._value
