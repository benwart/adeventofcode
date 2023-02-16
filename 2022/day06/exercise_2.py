#!/usr/bin/env python3


from collections import deque


def parse_characters(filepath: str):
    with open(filepath) as f:
        for line in f:
            for char in line.rstrip():
                yield char


def main():
    marker = 14
    buffer = deque(maxlen=marker)

    for index, char in enumerate(parse_characters("2022/day06/data/full")):
        buffer.append(char)

        if index >= marker:
            buffer_set = set(buffer)
            if len(buffer_set) == marker:
                print(f"index: {index + 1} with buffer {''.join(buffer)}")
                break


if __name__ == "__main__":
    main()
