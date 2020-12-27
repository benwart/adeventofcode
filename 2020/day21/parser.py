import re


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


RECIPE_REGEX = re.compile(
    r"^(?P<ingredients>[a-z ]+\s)+\(contains\s(?P<allergens>[^)]+)?\)$"
)


def parse_food(line):
    m = RECIPE_REGEX.match(line)
    d = m.groupdict()

    return {
        "ingredients": d["ingredients"].strip().split(" "),
        "allergens": re.split(", ", d["allergens"].strip()),
    }


def parse_foods(filepath):
    for line in parse_lines(filepath):
        yield parse_food(line)