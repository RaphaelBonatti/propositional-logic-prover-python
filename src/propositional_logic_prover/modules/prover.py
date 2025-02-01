from itertools import combinations

from modules.clause import Clause, convert_to_clauses
from modules.literal import negate_literal
from modules.parser import WFF, Negation


class Prover:
    def __init__(self) -> None:
        self.initial_clauses: set[Clause] = set()
        self.derivation_map: dict[Clause, tuple[Clause, Clause]] = dict()
        self.resolved: set[tuple[Clause, Clause]] = set()

    def add_to_derivation(
        self, resolvent: Clause, clause_tuple: tuple[Clause, Clause]
    ) -> None:
        # Check to avoid self derivation loops
        if resolvent in self.derivation_map.keys():
            return

        # Check to avoid derivation of initial clauses
        if resolvent in self.initial_clauses:
            return

        self.derivation_map[resolvent] = clause_tuple

    def resolve(self, clause1: Clause, clause2: Clause) -> set[Clause]:
        resolvents: set[Clause] = set()
        for literal in clause1:
            neg_literal = negate_literal(literal)
            if neg_literal in clause2:
                clause_diff1 = clause1.difference({literal})
                clause_diff2 = clause2.difference({neg_literal})
                resolvent = clause_diff1.union(clause_diff2)
                resolvents.add(resolvent)
                self.add_to_derivation(resolvent, (clause1, clause2))
        return resolvents

    def resolve_all(self, clauses: set[Clause]) -> set[Clause]:
        resolvents: set[Clause] = set()
        for clause_tuple in combinations(clauses, 2):
            if clause_tuple in self.resolved:
                continue
            self.resolved.add(clause_tuple)
            resolvents = resolvents.union(self.resolve(*clause_tuple))
            if frozenset() in resolvents:
                break
        return resolvents

    def search_refutation(self, clauses: set[Clause]) -> bool:
        length = 0
        while length != len(clauses):
            if frozenset() in clauses:
                return True

            length = len(clauses)
            clauses = clauses.union(self.resolve_all(clauses))
        return False

    def prove_by_refutation(self, kb: WFF, query: WFF) -> bool:
        clauses = convert_to_clauses(kb)
        is_kb_unsatisfiable = self.search_refutation(clauses)
        if is_kb_unsatisfiable:
            raise ValueError("Knowledge base must be consistent")

        query_negated = Negation(None, query)
        clauses_query = convert_to_clauses(query_negated)
        self.initial_clauses = clauses.union(clauses_query)
        return self.search_refutation(self.initial_clauses)
