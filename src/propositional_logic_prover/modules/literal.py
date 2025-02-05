def negate_literal(literal: str) -> str:
    if literal[0] == "¬":
        return literal[1:]
    return "¬" + literal
