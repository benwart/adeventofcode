#!/usr/bin/env python

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from operator import lt, gt, le, ge
from pathlib import Path
from re import match
from typing import Callable, Deque, Iterable

from colorama import Style, Fore


def parse_sections(filepath: Path) -> tuple[str, str]:
    with open(filepath, "r") as f:
        workflows, parts = f.read().split("\n\n")
        return workflows, parts


@dataclass
class Rule:
    operation: str
    has_check: bool = field(init=False, default=False)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{Style.BRIGHT}{Fore.GREEN}{self.operation}{Style.RESET_ALL}"

    def inverted(self) -> "Rule":
        return Rule(self.operation)


comparison_map: dict[str, Callable[[int, int], bool]] = {
    ">": gt,
    "<": lt,
    ">=": ge,
    "<=": le,
}

invert_comparison_map: dict[str, str] = {
    ">": "<=",
    "<": ">=",
}


@dataclass
class RuleCondition(Rule):
    prop: str
    comparison: str
    value: int

    def __post_init__(self):
        self.has_check = True

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{Style.DIM}{self.prop} {self.comparison} {self.value}:{Style.RESET_ALL} {Style.BRIGHT}{Fore.BLUE}{self.operation}{Style.RESET_ALL}"

    def inverted(self) -> "RuleCondition":
        return RuleCondition(self.operation, self.prop, invert_comparison_map[self.comparison], self.value)


@dataclass
class Workflow:
    id: str
    rules: list[Rule]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{Style.BRIGHT}{Fore.CYAN}{self.id}{Style.RESET_ALL}: {', '.join(map(str, self.rules))}"


class Result(Enum):
    PASS = 0
    FAIL = 1


@dataclass
class FlowNode:
    workflow: Workflow
    index: int
    result: Result

    def rule(self) -> Rule:
        return self.workflow.rules[self.index]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"({self.workflow.id}, {self.index}) {str(self.workflow.rules[self.index] if self.result == Result.PASS else str(self.workflow.rules[self.index].inverted()))}"


WORKFLOW_ID_RULES_REGEX = r"(?P<id>[^\{}]+)\{(?P<rules>.+)\}"
WORKFLOW_RULE_CONDITION_REGEX = r"(?P<prop>[a-z])(?P<comparison>[><])(?P<value>\d+):(?P<operation>[a-zA-Z]+)"
WORKFLOW_RULE_ACCECPT_REJECT_REGEX = r"[AR]"
WORKFLOW_RULE_NEXT_WORKFLOW_REGEX = r"[a-z]+"


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


def accepting_flows(workflows: dict[str, Workflow]) -> Iterable[list[Rule]]:
    flows: Deque[list[FlowNode]] = deque()

    start: Workflow = workflows["in"]
    flows.append([FlowNode(start, 0, Result.PASS)])
    flows.append([FlowNode(start, 0, Result.FAIL)])

    while len(flows) > 0:
        flow = flows.popleft()
        current = flow[-1]
        rule = current.rule()

        # if the rule is only an operation, we skip fail flows
        if not rule.has_check:
            if current.result == Result.FAIL:
                continue

            # are we done?
            if rule.operation == "A":
                yield flow
                continue

            elif rule.operation == "R":
                continue

            # add the next workflow to the flow and push to the queue
            else:
                pass_flow = flow.copy() + [FlowNode(workflows[rule.operation], 0, Result.PASS)]
                fail_flow = flow.copy() + [FlowNode(workflows[rule.operation], 0, Result.FAIL)]
                flows.extend([pass_flow, fail_flow])
                continue

        else:
            if current.result == Result.PASS:
                # are we done?
                if rule.operation == "A":
                    yield flow
                    continue

                elif rule.operation == "R":
                    continue

                pass_flow = flow.copy() + [FlowNode(workflows[rule.operation], 0, Result.FAIL)]
                fail_flow = flow.copy() + [FlowNode(workflows[rule.operation], 0, Result.PASS)]
                flows.extend([pass_flow, fail_flow])
                continue

            else:
                pass_flow = flow.copy() + [FlowNode(current.workflow, current.index + 1, Result.PASS)]
                fail_flow = flow.copy() + [FlowNode(current.workflow, current.index + 1, Result.FAIL)]
                flows.extend([pass_flow, fail_flow])
                continue


def main(filepath: Path):
    workflows_section, _ = parse_sections(filepath)
    workflows = parse_workflows(workflows_section)

    for flow in accepting_flows(workflows):
        print(flow)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1")
