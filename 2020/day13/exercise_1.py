#!/usr/bin/env python3

from parser import parse_scedule_exercise1

earliest, bus_ids = parse_scedule_exercise1("./data/full")

print(earliest, bus_ids)

offsets = [id for id in map(lambda id: id - (earliest % id), bus_ids)]
minimum = min(offsets)
id = bus_ids[offsets.index(minimum)]

print(f"Bus ID: {id}, Offset: {minimum}, Answer: {id * minimum}")
