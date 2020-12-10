"""
--- Part Two ---
Now find one that starts with six zeroes.
"""
import sys
from hashlib import md5

inputs = {
    "full": {"in": "bgvyzdsv", "solution": None},
}

value = 0
input = inputs["full"]
leading_zeros = "000000"

while True:
    value += 1

    digest = md5(f"{input['in']}{value}".encode("utf-8")).hexdigest()
    if digest.startswith(leading_zeros):
        if input["solution"] == value:
            print(f"\nAssert == TRUE", end="")
        print(f"\nFound {value}")
        break

    if value % 10 ** 4 == 0:
        sys.stdout.write(".")
        sys.stdout.flush()

    if input["solution"] and value >= input["solution"]:
        print(f"\nAssert == FALSE")
        break
