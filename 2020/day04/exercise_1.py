#!/usr/bin/env python3

with open("./data/example") as f:
    data = [line.rstrip() for line in f]

print(f"Row of Data: {len(data)}")
