import re
from collections import namedtuple

"""
https://github.com/eliben/code-for-blog/blob/master/2012/rd_infix_precedence.py
"""

Tok = namedtuple("Tok", "name value")


class Tokenizer(object):
    """Simple tokenizer object. The cur_token attribute holds the current
    token (Tok). Call get_next_token() to advance to the
    next token. cur_token is None before the first token is
    taken and after the source ends.
    """

    TOKPATTERN = re.compile(r"\s*(?:(\d+)|(.))")

    def __init__(self, source):
        self._tokgen = self._gen_tokens(source)
        self.cur_token = None

    def get_next_token(self):
        """Advance to the next token, and return it."""
        try:
            self.cur_token = next(self._tokgen)
        except StopIteration:
            self.cur_token = None
        return self.cur_token

    def _gen_tokens(self, source):
        for number, operator in self.TOKPATTERN.findall(source):
            if number:
                yield Tok("NUMBER", number)
            elif operator == "(":
                yield Tok("LEFTPAREN", "(")
            elif operator == ")":
                yield Tok("RIGHTPAREN", ")")
            else:
                yield Tok("BINOP", operator)


def parse_problems(filepath):
    with open(filepath) as f:
        for line in f:
            t = Tokenizer(line.rstrip())
            t.get_next_token()
            yield t