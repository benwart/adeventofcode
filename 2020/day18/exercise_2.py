#!/usr/bin/env python3

from collections import namedtuple
from parser_2 import parse_problems

"""
https://github.com/eliben/code-for-blog/blob/master/2012/rd_infix_precedence.py
"""


def compute_atom(tokenizer):
    tok = tokenizer.cur_token
    if tok.name == "LEFTPAREN":
        tokenizer.get_next_token()
        val = compute_expr(tokenizer, 1)
        if tokenizer.cur_token.name != "RIGHTPAREN":
            raise Exception('unmatched "("')
        tokenizer.get_next_token()
        return val
    elif tok is None:
        raise Exception("source ended unexpectedly")
    elif tok.name == "BINOP":
        raise Exception(f"expected an atom, not an operator '{tok.value}'")
    else:
        assert tok.name == "NUMBER"
        tokenizer.get_next_token()
        return int(tok.value)


# For each operator, a (precedence, associativity) pair.
OpInfo = namedtuple("OpInfo", "prec assoc")

OPINFO_MAP = {
    "+": OpInfo(2, "LEFT"),
    "*": OpInfo(1, "LEFT"),
}


def compute_op(op, lhs, rhs):
    lhs = int(lhs)
    rhs = int(rhs)
    if op == "+":
        return lhs + rhs
    elif op == "-":
        return lhs - rhs
    elif op == "*":
        return lhs * rhs
    elif op == "/":
        return lhs / rhs
    elif op == "^":
        return lhs ** rhs
    else:
        raise Exception(f"unknown operator '{op}'")


def compute_expr(tokenizer, min_prec):
    atom_lhs = compute_atom(tokenizer)

    while True:
        cur = tokenizer.cur_token
        if cur is None or cur.name != "BINOP" or OPINFO_MAP[cur.value].prec < min_prec:
            break

        # Inside this loop the current token is a binary operator
        assert cur.name == "BINOP"

        # Get the operator's precedence and associativity, and compute a
        # minimal precedence for the recursive call
        op = cur.value
        prec, assoc = OPINFO_MAP[op]
        next_min_prec = prec + 1 if assoc == "LEFT" else prec

        # Consume the current token and prepare the next one for the
        # recursive call
        tokenizer.get_next_token()
        atom_rhs = compute_expr(tokenizer, next_min_prec)

        # Update lhs with the new value
        atom_lhs = compute_op(op, atom_lhs, atom_rhs)

    return atom_lhs


total = 0
for t in parse_problems("./data/full"):
    result = compute_expr(t, 1)
    total += result
    print(result)

print(f"Total: {total}")