from modules import cnf_converter, wff_traverser
from modules.literal import Literal, is_literal
from modules.parser import WFF, Disjunction, Negation

type Clause = frozenset[Literal]


def convert_to_clauses(wff: WFF) -> set[Clause]:
    wff_cnf = cnf_converter.convert_to_cnf(wff)
    traversal = wff_traverser.build_traversal_post_order(wff_cnf)
    stack: list[Clause] = []
    for current in traversal:
        if isinstance(current, Disjunction):
            clause1 = stack.pop()
            clause2 = stack.pop()
            stack.append(clause1.union(clause2))
        if isinstance(current, Negation):
            _ = stack.pop()
        if is_literal(str(current)):
            stack.append(frozenset({str(current)}))
    return set(stack)
