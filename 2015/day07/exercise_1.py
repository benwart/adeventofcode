import re
from parser import parse_input
from wire import Literal, Wire
from gate import AND, OR, NOT, RSHIFT, LSHIFT

is_letter = re.compile(r"[a-z]{1,2}")
is_number = re.compile(r"\d+")


def get_literal_or_wire(a):
    global wires

    l = is_letter.match(a)
    n = is_number.match(a)

    if l:
        if a not in wires:
            wires[a] = Wire(id=a)

        return wires[a]

    if n:
        return Literal(value=a)

    raise ValueError(f"'{a}' is not a number of letters.")


def literal(literal, output):
    l = get_literal_or_wire(literal)
    w = get_literal_or_wire(output)

    w.input = l


def junction(input, output):
    i = get_literal_or_wire(input)
    w = get_literal_or_wire(output)

    w.input = i


def and_gate(a, b, output):
    AND(get_literal_or_wire(a), get_literal_or_wire(b), get_literal_or_wire(output))


def or_gate(a, b, output):
    OR(get_literal_or_wire(a), get_literal_or_wire(b), get_literal_or_wire(output))


def not_gate(a, output):
    NOT(get_literal_or_wire(a), get_literal_or_wire(output))


def rshift_gate(a, shift, output):
    RSHIFT(get_literal_or_wire(a), shift, get_literal_or_wire(output))


def lshift_gate(a, shift, output):
    LSHIFT(get_literal_or_wire(a), shift, get_literal_or_wire(output))


setup = {
    "literal": literal,
    "junction": junction,
    "and": and_gate,
    "or": or_gate,
    "not": not_gate,
    "rshift": rshift_gate,
    "lshift": lshift_gate,
}

wires = {}

import numpy as np


def to_uint16(value):
    return np.array([value], dtype="uint16")[0]


for k, m in parse_input("./data/full"):
    # print(k, m)
    setup[k](**m)

for k in sorted(wires):
    w = wires[k]
    print(f"{k}: {to_uint16(w.value)}")

# print(f"Input to 'f': {wires['f'].value}")
# print(f"123 << 2 = {123 << 2}")

print(f"Input to 'a': {wires['a'].value}")
