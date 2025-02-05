type Literal = str


def negate_literal(literal: Literal) -> Literal:
    if literal[0] == "¬":
        return literal[1:]
    return "¬" + literal
