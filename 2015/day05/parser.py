def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()