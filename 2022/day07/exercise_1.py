#!/usr/bin/env python3


def parse_lines(filepath: str):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def main():
    pass


if __name__ == "__main__":
    main()
