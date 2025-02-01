from abc import ABC
from typing import Any

from textx import metamodel_from_str  # type: ignore

type TruthValue = bool
type Variable = str
type Formula = str

grammar = """
Model: wff=WFF;
WFF: Atom | Negation | Conjunction | Disjunction | Implication | Equivalence;
Equivalence: '(' lhs=WFF '<=>' rhs=WFF ')';
Implication: '(' lhs=WFF '=>' rhs=WFF ')';
Disjunction: '(' lhs=WFF '|' rhs=WFF ')';
Conjunction: '(' lhs=WFF '&' rhs=WFF ')';
Negation: '~' wff=WFF;
Atom: id=ID;
"""


class WFF(ABC):
    formula: Formula = ""

    def __str__(self) -> Formula:
        return self.formula


class Equivalence(WFF):
    def __init__(self, parent: Any, lhs: WFF, rhs: WFF):
        self.parent = parent
        self.lhs = lhs
        self.rhs = rhs
        self.formula = f"({str(self.lhs)} ↔ {str(self.rhs)})"

    @staticmethod
    def evaluate(lhs: TruthValue, rhs: TruthValue) -> TruthValue:
        return lhs == rhs


class Implication(WFF):
    def __init__(self, parent: Any, lhs: WFF, rhs: WFF):
        self.parent = parent
        self.lhs = lhs
        self.rhs = rhs
        self.formula = f"({str(self.lhs)} → {str(self.rhs)})"

    @staticmethod
    def evaluate(rhs: TruthValue, lhs: TruthValue) -> TruthValue:
        return (not lhs) or rhs


class Disjunction(WFF):
    def __init__(self, parent: Any, lhs: WFF, rhs: WFF):
        self.parent = parent
        self.lhs = lhs
        self.rhs = rhs
        self.formula = f"({str(self.lhs)} ∨ {str(self.rhs)})"

    @staticmethod
    def evaluate(lhs: TruthValue, rhs: TruthValue) -> TruthValue:
        return lhs or rhs


class Conjunction(WFF):
    def __init__(self, parent: Any, lhs: WFF, rhs: WFF):
        self.parent = parent
        self.lhs = lhs
        self.rhs = rhs
        self.formula = f"({str(self.lhs)} ∧ {str(self.rhs)})"

    @staticmethod
    def evaluate(lhs: TruthValue, rhs: TruthValue) -> TruthValue:
        return lhs and rhs


class Negation(WFF):
    def __init__(self, parent: Any, wff: WFF):
        self.parent = parent
        self.wff = wff
        self.formula = f"¬{str(self.wff)}"

    @staticmethod
    def evaluate(value: TruthValue) -> TruthValue:
        return not value


class Atom(WFF):
    def __init__(self, parent: Any, id: Variable):
        self.parent = parent
        self.id = id
        self.formula = id

    @staticmethod
    def evaluate() -> None:
        return None


def wff_from_str(wff_str: str) -> WFF:
    return (
        metamodel_from_str(
            grammar,
            classes=[
                Atom,
                Negation,
                Conjunction,
                Disjunction,
                Implication,
                Equivalence,
            ],
        )
        .model_from_str(wff_str)  # type: ignore
        .wff
    )
