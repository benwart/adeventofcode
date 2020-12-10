"""
--- Day 4: The Ideal Stocking Stuffer ---
Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least five zeroes. The input to the MD5 hash is some secret key (your puzzle input, given below) followed by a number in decimal. To mine AdventCoins, you must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.

For example:

If your secret key is abcdef, the answer is 609043, because the MD5 hash of abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest such number to do so.
If your secret key is pqrstuv, the lowest number it combines with to make an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of pqrstuv1048970 looks like 000006136ef....

Your puzzle input is bgvyzdsv.
"""
import sys
from hashlib import md5

inputs = {
    "example1": {"in": "abcdef", "solution": 609043},
    "example2": {"in": "pqrstuv", "solution": 1048970},
    "full": {"in": "bgvyzdsv", "solution": None},
}

value = 0
input = inputs["full"]
leading_zeros = "00000"

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
