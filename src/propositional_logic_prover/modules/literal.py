import re

type Literal = str


def is_literal(literal: Literal) -> bool:
    pattern_literal = re.compile(r"¬?[^\d\W]\w*\b")
    return pattern_literal.fullmatch(literal) != None


def negate_literal(literal: Literal) -> Literal:
    if literal[0] == "¬":
        return literal[1:]
    return "¬" + literal
