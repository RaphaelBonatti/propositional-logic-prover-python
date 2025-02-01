from modules import parser, cnf_converter


def test_atom():
    wff = parser.wff_from_str("A")

    output = cnf_converter.convert_to_cnf(wff)

    assert str(output) == "A"


def test_negated_atom():
    wff = parser.wff_from_str("~A")

    output = cnf_converter.convert_to_cnf(wff)

    assert str(output) == "¬A"


def test_disjunctive_wff():
    wff = parser.wff_from_str("(A|B)")

    output = cnf_converter.convert_to_cnf(wff)

    assert str(output) == "(A ∨ B)"


def test_conjunctive_wff():
    wff = parser.wff_from_str("(A&B)")

    output = cnf_converter.convert_to_cnf(wff)

    assert str(output) == "(A ∧ B)"


def test_implicative_wff():
    wff = parser.wff_from_str("(A=>B)")

    output = cnf_converter.convert_to_cnf(wff)

    assert str(output) == "(¬A ∨ B)"


def test_implicative_2_wff():
    wff = parser.wff_from_str("((A=>B)=>C)")

    output = cnf_converter.convert_to_cnf(wff)

    assert str(output) == "((A ∨ C) ∧ (¬B ∨ C))"
