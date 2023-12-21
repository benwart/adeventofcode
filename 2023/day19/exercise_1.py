#!/usr/bin/env python

from colorama import Style
from dataclasses import dataclass, field
from pathlib import Path
from re import match
from typing import Iterable, override


def parse_sections(filepath: Path) -> tuple[str, str]:
    with open(filepath, "r") as f:
        workflows, parts = f.read().split("\n\n")
        return workflows, parts


WORKFLOW_ID_RULES_REGEX = r"(?P<id>[^\{}]+)\{(?P<rules>.+)\}"
WORKFLOW_RULE_CONDITION_REGEX = r"(?P<prop>[a-z])(?P<comparison>[><])(?P<value>\d+):(?P<operation>[a-zA-Z]+)"
WORKFLOW_RULE_ACCECPT_REJECT_REGEX = r"[AR]"
WORKFLOW_RULE_NEXT_WORKFLOW_REGEX = r"[a-z]+"


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int
    flow: list[str] = field(default_factory=list)
    total: int = field(init=False)

    def __post_init__(self):
        self.total = self.x + self.m + self.a + self.s

    def __repr__(self):
        return f"{{x={self.x}, m={self.m}, a={self.a}, s={self.s}}}"

    def __str__(self):
        return f"{repr(self)}: {Style.DIM}{' -> '.join(self.flow[:-1])} -> {Style.RESET_ALL}{Style.BRIGHT}{self.flow[-1]}{Style.RESET_ALL}"

    def accepted(self) -> bool:
        if len(self.flow) == 0:
            return False

        return self.flow[-1] == "A"


@dataclass
class Rule:
    operation: str

    def check(self, _: Part) -> bool:
        return True


comparison_map = {
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
}


@dataclass
class RuleCondition(Rule):
    prop: str
    comparison: str
    value: int

    @override
    def check(self, part: Part) -> bool:
        return comparison_map[self.comparison](getattr(part, self.prop), self.value)


@dataclass
class Workflow:
    id: str
    rules: list[Rule]


def parse_workflows(section: str) -> dict[str, Workflow]:
    workflows = {}
    for line in section.splitlines():
        groups = match(WORKFLOW_ID_RULES_REGEX, line).groupdict()
        id = groups["id"]

        rules = []
        for rule in groups["rules"].split(","):
            m = match(WORKFLOW_RULE_CONDITION_REGEX, rule)
            if m:
                g = m.groupdict()
                rules.append(RuleCondition(g["operation"], g["prop"], g["comparison"], int(g["value"])))
                continue

            m = match(WORKFLOW_RULE_ACCECPT_REJECT_REGEX, rule)
            if m:
                rules.append(Rule(m.string))
                continue

            m = match(WORKFLOW_RULE_NEXT_WORKFLOW_REGEX, rule)
            if m:
                rules.append(Rule(m.string))
                continue

            print(f"Could not parse rule: {rule}")

        workflows[groups["id"]] = Workflow(id, rules)

    return workflows


def parse_parts(section: str) -> Iterable[Part]:
    for line in section.splitlines():
        props = line.strip("{}").split(",")

        args = {}
        for prop in props:
            k, v = prop.split("=")
            args[k] = int(v)

        yield Part(args["x"], args["m"], args["a"], args["s"])


def part_flow(part: Part, workflows: dict[str, Workflow]) -> Part:
    current: Workflow = workflows["in"]
    part.flow.append(current.id)

    while True:
        for rule in current.rules:
            if rule.check(part):
                if rule.operation in ["A", "R"]:
                    part.flow.append(rule.operation)
                    return part

                else:
                    part.flow.append(rule.operation)
                    current = workflows[rule.operation]
                    break


def main(filepath: Path):
    workflows_section, parts_section = parse_sections(filepath)
    workflows = parse_workflows(workflows_section)
    parts: list[Part] = [part_flow(p, workflows) for p in parse_parts(parts_section)]

    total = 0
    for part in parts:
        if part.accepted():
            print(part)
            total += part.total

    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
