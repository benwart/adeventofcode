from arpeggio import Optional, OneOrMore, EOF
from arpeggio import RegExMatch, StrMatch
from arpeggio import ParserPython


class SuppressStrMatch(StrMatch):
    suppress = True


def number():
    return RegExMatch(r"\d+")


def term():
    return [number, (SuppressStrMatch("("), expression, SuppressStrMatch(")"))]


def operator():
    return ["+", "*"]


def expression():
    return term, OneOrMore(operator, term)


def problem():
    return OneOrMore(expression)


def parse_problems(filepath, debug=False):
    parser = ParserPython(problem, debug=debug)
    with open(filepath) as f:
        for line in f:
            yield parser.parse(line.rstrip())