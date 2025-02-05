from modules import cnf_converter
from modules.literal import Literal
from modules.parser import WFF

type Clause = frozenset[Literal]


def convert_to_clauses(wff: WFF) -> set[Clause]:
    wff_cnf = cnf_converter.convert_to_cnf(wff)
    wff_cleaned = str(wff_cnf).translate(str.maketrans({"(": "", ")": "", " ": ""}))
    string_clauses = wff_cleaned.split("∧")
    return set([frozenset(e.split("∨")) for e in string_clauses])
