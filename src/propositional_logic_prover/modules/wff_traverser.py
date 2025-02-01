from typing import List

from modules.parser import WFF, Atom, Negation


def build_traversal_post_order(wff: WFF) -> List[WFF]:
    traversal: List[WFF] = []
    stack: List[WFF] = []
    current = wff
    lastVisited: WFF | None = None
    while len(stack) > 0 or current != None:
        if current != None:
            stack.append(current)
            current = match_case_next(current)
        else:
            peeked = stack[-1]
            if lastVisited != None and match_case_not_visited(peeked, lastVisited):
                current = match_case_next(peeked, left_direction=False)
            else:
                traversal.append(peeked)
                lastVisited = stack.pop()
    return traversal


def match_case_not_visited(peeked: WFF, lastVisited: WFF) -> bool:
    match peeked.__class__.__name__:
        case Atom.__name__:
            return False
        case Negation.__name__:
            return not (peeked.wff is lastVisited)  # type: ignore
        case _:
            return not (peeked.rhs is lastVisited)  # type: ignore


def match_case_next(wff: WFF, left_direction: bool = True) -> WFF | None:
    match wff.__class__.__name__:
        case Atom.__name__:
            return None
        case Negation.__name__:
            return wff.wff  # type: ignore
        case _:
            if left_direction:
                return wff.lhs  # type: ignore
            else:
                return wff.rhs  # type: ignore
