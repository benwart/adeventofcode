import re


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


# 456 -> y
LITERAL_REGEX = re.compile(r"(?P<literal>\d+)\s+->\s+(?P<output>[a-z]{1,2})")

# lx -> a
JUNCTION_REGEX = re.compile(r"(?P<input>[a-z]{1,2})\s+->\s+(?P<output>[a-z]{1,2})")

# x AND y -> d
AND_REGEX = re.compile(
    r"(?P<a>[a-z]{1,2}|\d+)\s+AND\s+(?P<b>[a-z]{1,2}|\d+)\s+->\s+(?P<output>[a-z]{1,2})"
)

# x OR y -> e
OR_REGEX = re.compile(
    r"(?P<a>[a-z]{1,2}|\d+)\s+OR\s+(?P<b>[a-z]{1,2}|\d+)\s+->\s+(?P<output>[a-z]{1,2})"
)

# NOT x -> h
NOT_REGEX = re.compile(r"NOT\s+(?P<a>[a-z]{1,2}|\d+)\s+->\s+(?P<output>[a-z]{1,2})")

# y RSHIFT 2 -> g
RSHIFT_REGEX = re.compile(
    r"(?P<a>[a-z]{1,2}|\d+)\s+RSHIFT\s+(?P<shift>[a-z]{1,2}|\d+)\s+->\s+(?P<output>[a-z]{1,2})"
)

# x LSHIFT 2 -> f
LSHIFT_REGEX = re.compile(
    r"(?P<a>[a-z]{1,2}|\d+)\s+LSHIFT\s+(?P<shift>[a-z]{1,2}|\d+)\s+->\s+(?P<output>[a-z]{1,2})"
)

searches = {
    "literal": LITERAL_REGEX,
    "junction": JUNCTION_REGEX,
    "and": AND_REGEX,
    "or": OR_REGEX,
    "not": NOT_REGEX,
    "rshift": RSHIFT_REGEX,
    "lshift": LSHIFT_REGEX,
}


def parse_config(line):
    for k, search in searches.items():
        m = search.match(line)
        if m:
            return (k, m.groupdict())
    raise ValueError(f"'{line}' does not contian valid config.")


def parse_input(filepath):
    for line in parse_lines(filepath):
        yield parse_config(line)