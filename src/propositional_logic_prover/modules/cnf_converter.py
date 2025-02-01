from modules.parser import (
    wff_from_str,
    WFF,
    Atom,
    Negation,
    Conjunction,
    Disjunction,
    Implication,
    Equivalence,
)


def convert_to_cnf(wff: WFF) -> WFF:
    wff_nnf = convert_to_nnf(wff)
    return push_disjunction_inwards(wff_nnf)


def push_disjunction_inwards(wff: WFF) -> WFF:
    match wff.__class__.__name__:
        case Atom.__name__:
            return Atom(None, wff.id)
        case Negation.__name__:
            if not isinstance(wff.wff, Atom):
                raise ValueError(f"wff must be in negative normal form (nnf).")
            return Negation(None, Atom(None, wff.wff.id))
        case Conjunction.__name__:
            lhs = push_disjunction_inwards(wff.lhs)
            rhs = push_disjunction_inwards(wff.rhs)
            return Conjunction(None, lhs, rhs)
        case Disjunction.__name__:
            lhs = push_disjunction_inwards(wff.lhs)
            rhs = push_disjunction_inwards(wff.rhs)
            if isinstance(lhs, Conjunction):
                lhs_disj = Disjunction(None, lhs.lhs, rhs)
                rhs_disj = Disjunction(None, lhs.rhs, rhs)
            elif isinstance(rhs, Conjunction):
                lhs_disj = Disjunction(None, lhs, rhs.lhs)
                rhs_disj = Disjunction(None, lhs, rhs.rhs)
            else:
                return Disjunction(None, lhs, rhs)
            lhs_disj = push_disjunction_inwards(lhs_disj)
            rhs_disj = push_disjunction_inwards(rhs_disj)
            return Conjunction(None, lhs_disj, rhs_disj)
    raise ValueError(f"wff must be in negative normal form (nnf).")


def convert_to_nnf(wff: WFF) -> WFF:
    wff_replaced = replace_implications_and_equivalences(wff)
    return push_negation_inwards(wff_replaced)


def push_negation_inwards(wff: WFF) -> WFF:
    match wff.__class__.__name__:
        case Atom.__name__:
            return Atom(None, wff.id)
        case Negation.__name__:
            child = wff.wff
            if isinstance(child, Atom):
                atom = Atom(None, child.id)
                return Negation(None, atom)
            elif isinstance(child, Negation):
                wff_new = child.wff
            else:
                wff_new = apply_de_morgans_law(child)
            return push_negation_inwards(wff_new)
        case Conjunction.__name__:
            lhs = push_negation_inwards(wff.lhs)
            rhs = push_negation_inwards(wff.rhs)
            return Conjunction(None, lhs, rhs)
        case Disjunction.__name__:
            lhs = push_negation_inwards(wff.lhs)
            rhs = push_negation_inwards(wff.rhs)
            return Disjunction(None, lhs, rhs)
    raise ValueError(f"Not implemented for {wff.__class__.__name__}")


def apply_de_morgans_law(wff: WFF) -> WFF:
    match wff.__class__.__name__:
        case Conjunction.__name__:
            neg_lhs = Negation(None, wff.lhs)
            neg_rhs = Negation(None, wff.rhs)
            return Disjunction(None, neg_lhs, neg_rhs)
        case Disjunction.__name__:
            neg_lhs = Negation(None, wff.lhs)
            neg_rhs = Negation(None, wff.rhs)
            return Conjunction(None, neg_lhs, neg_rhs)
    raise ValueError(f"Not implemented for {wff.__class__.__name__}")


def replace_implications_and_equivalences(wff: WFF) -> WFF:
    match wff.__class__.__name__:
        case Atom.__name__:
            return Atom(None, wff.id)
        case Negation.__name__:
            replaced = replace_implications_and_equivalences(wff.wff)
            return Negation(None, replaced)
        case Conjunction.__name__:
            lhs = replace_implications_and_equivalences(wff.lhs)
            rhs = replace_implications_and_equivalences(wff.rhs)
            return Conjunction(None, lhs, rhs)
        case Disjunction.__name__:
            lhs = replace_implications_and_equivalences(wff.lhs)
            rhs = replace_implications_and_equivalences(wff.rhs)
            return Disjunction(None, lhs, rhs)
        case Implication.__name__:
            lhs = replace_implications_and_equivalences(wff.lhs)
            rhs = replace_implications_and_equivalences(wff.rhs)
            neg_lhs = Negation(None, lhs)
            return Disjunction(None, neg_lhs, rhs)
        case Equivalence.__name__:
            lhs = replace_implications_and_equivalences(wff.lhs)
            rhs = replace_implications_and_equivalences(wff.rhs)
            neg_lhs = Negation(None, lhs)
            neg_rhs = Negation(None, rhs)
            lhs_disj = Disjunction(None, neg_lhs, rhs)
            rhs_disj = Disjunction(None, neg_rhs, lhs)
            return Conjunction(None, lhs_disj, rhs_disj)
