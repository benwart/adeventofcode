import re


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def replace(m):
    value = m.group(1)
    if value == "\\\\":
        return "\\"

    if value == '\\"':
        return '"'

    if value.startswith("\\x"):
        i = int(value[2:], 16)
        if i < ord(" ") or i > ord("z"):
            print(i, value, chr(i))
        return chr(i)


def encode(m):
    value = m.group(1)
    if value == "\\":
        return "\\\\"

    if value == '"':
        return '\\"'


def parse_line(line):
    trimmed = line[1:-1]
    value = re.sub(r"(\\x[0-9a-f]{2}|\\\"|\\\\)", replace, trimmed)
    encoded = re.sub(r"(\\|\")", encode, line)
    encoded = f'"{encoded}"'

    print(f"{line} - {len(line)}")
    print(f" {value} - {len(value)}")
    print(f"{encoded} - {len(encoded)}")

    return {
        "code": len(line),
        "stored": len(value),
        "encoded": len(encoded),
        "value": value,
    }


def parse_input(filepath):
    for line in parse_lines(filepath):
        yield parse_line(line)
