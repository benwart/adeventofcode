def parse(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_ints(filepath):
    for line in parse(filepath):
        yield int(line)
