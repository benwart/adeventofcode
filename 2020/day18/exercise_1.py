#!/usr/bin/env python3

from arpeggio import PTNodeVisitor, visit_parse_tree
from parser_1 import parse_problems


class ProblemVisitor(PTNodeVisitor):
    def visit_number(self, node, children):
        """
        Converts node value to int.
        """
        return int(node.value)

    def visit_expression(self, node, children):
        """
        Adds or mutiplies terms.
        """
        if self.debug:
            print("Expression {}".format(children))
        expr = children[0]
        for i in range(2, len(children), 2):
            if i and children[i - 1] == "*":
                expr *= children[i]
            else:
                expr += children[i]
        if self.debug:
            print("Expression = {}".format(expr))
        return expr


total = 0
for parse_tree in parse_problems("./data/full"):
    print(parse_tree)
    result = visit_parse_tree(parse_tree, ProblemVisitor(debug=False))
    total += result
    print(result)

print(f"Sum of Results: {total}")