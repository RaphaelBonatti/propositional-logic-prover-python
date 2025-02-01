from modules import parser
from modules.prover import Prover


def test_query_is_valid() -> None:
    kb = parser.wff_from_str("A")
    query = parser.wff_from_str("A")

    is_valid = Prover().prove_by_refutation(kb, query)

    assert is_valid


def test_query_not_valid() -> None:
    kb = parser.wff_from_str("A")
    query = parser.wff_from_str("B")

    is_valid = Prover().prove_by_refutation(kb, query)

    assert not is_valid


def test_a_does_not_entails_not_a() -> None:
    kb = parser.wff_from_str("A")
    query = parser.wff_from_str("~A")

    is_valid = Prover().prove_by_refutation(kb, query)

    assert not is_valid


def test_a_or_b_does_not_entails_a() -> None:
    kb = parser.wff_from_str("(A|B)")
    query = parser.wff_from_str("A")

    is_valid = Prover().prove_by_refutation(kb, query)

    assert not is_valid


def test_study_and_practice_implies_graduate_is_valid() -> None:
    kb = parser.wff_from_str("(((STUDY&PRACTICE)=>PASS)&(PASS=>GRADUATE))")
    query = parser.wff_from_str("((STUDY&PRACTICE)=>GRADUATE)")

    is_valid = Prover().prove_by_refutation(kb, query)

    assert is_valid
