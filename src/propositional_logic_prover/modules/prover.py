from itertools import combinations

from modules.clause import Clause, convert_to_clauses
from modules.literal import negate_literal
from modules.parser import WFF, Negation


def prove_by_refutation(
    kb: WFF, query: WFF
) -> tuple[bool, dict[Clause, tuple[Clause, Clause]]]:
    clauses = convert_to_clauses(kb)
    query_negated = Negation(None, query)
    clauses_query = convert_to_clauses(query_negated)
    initial_clauses = clauses.union(clauses_query)
    derivation = search_refutation(initial_clauses)
    return frozenset() in derivation.keys(), derivation


def verify_knowledge_base_consistency(kb: WFF) -> bool:
    clauses = convert_to_clauses(kb)
    derivation = search_refutation(clauses)
    return not frozenset() in derivation.keys()


def search_refutation(
    initial_clauses: set[Clause],
) -> dict[Clause, tuple[Clause, Clause]]:
    clauses = initial_clauses
    resolved: set[tuple[Clause, Clause]] = set()
    derivation: dict[Clause, tuple[Clause, Clause]] = dict()
    length = 0
    while length != len(clauses):
        if frozenset() in clauses:
            break

        length = len(clauses)
        pairs = [
            pair for pair in combinations(clauses, 2) if pair not in resolved
        ]
        resolved = resolved.union(pairs)
        pairs_resolvents = resolve_clause_pairs(pairs)
        derivation.update(
            map_resolvent_to_parent(pairs_resolvents, pairs, clauses)
        )
        clauses = clauses.union(*pairs_resolvents)
    return derivation


def map_resolvent_to_parent(
    pairs_resolvents: list[set[Clause]],
    pairs: list[tuple[Clause, Clause]],
    clauses_to_filter: set[Clause],
) -> dict[Clause, tuple[Clause, Clause]]:
    return {
        resolvent: pair
        for resolvents, pair in zip(pairs_resolvents, pairs)
        for resolvent in resolvents
        if not resolvent in clauses_to_filter
    }


def resolve_clause_pairs(
    pairs: list[tuple[Clause, Clause]]
) -> list[set[Clause]]:
    resolvents_list: list[set[Clause]] = []
    for pair in pairs:
        resolvents = resolve(*pair)
        resolvents_list.append(resolvents)
        if frozenset() in resolvents:
            break
    return resolvents_list


def resolve(clause1: Clause, clause2: Clause) -> set[Clause]:
    resolvents: set[Clause] = set()
    for literal in clause1:
        neg_literal = negate_literal(literal)
        if neg_literal in clause2:
            clause_diff1 = clause1.difference({literal})
            clause_diff2 = clause2.difference({neg_literal})
            resolvent = clause_diff1.union(clause_diff2)
            resolvents.add(resolvent)
    return resolvents
