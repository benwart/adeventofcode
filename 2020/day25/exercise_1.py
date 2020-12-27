#!/usr/bin/env python3


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield int(line.rstrip())


def transform(value, subject):
    value *= subject
    value = value % 20201227
    return value


def find_loops(subject, public):
    value = 1
    count = 0
    while value != public and count < 10e7:
        value = transform(value, subject)
        count += 1
    return count


def find_key(public, loops):
    value = 1
    for _ in range(loops):
        value = transform(value, public)
    return value


card_public, door_public = [l for l in parse_lines("./data/full")]

print(card_public, door_public)

card_loops = find_loops(7, card_public)
print(f"card {card_public} == {card_loops} loops")

door_loops = find_loops(7, door_public)
print(f"door {door_public} == {door_loops} loops")

card_key = find_key(door_public, card_loops)
door_key = find_key(card_public, door_loops)

print(f"{card_key} {'==' if card_key == door_key else '!='} {door_key}")