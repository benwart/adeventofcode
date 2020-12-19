import re

RULE_REF_REGEX = re.compile(
    r"(?P<id>\d+):\s+((?P<refs>[0-9 |]+)|\"(?P<literal>[a-z]+)\")"
)


def parse_line(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_rule(rule):
    m = RULE_REF_REGEX.match(rule)
    if m:
        captures = m.groupdict()
        return int(captures["id"]), {
            "refs": captures["refs"],
            "literal": captures["literal"],
        }


def parse_data(filepath):
    rules = {}
    messages = []

    for line in parse_line(filepath):
        if ":" in line:
            id, refs = parse_rule(line)
            rules[id] = refs
        elif len(line) > 0:
            messages.append(line)

    return rules, messages
