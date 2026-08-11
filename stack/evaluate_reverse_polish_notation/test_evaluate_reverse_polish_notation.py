import random

import pytest

from evaluate_reverse_polish_notation import eval_rpn


def test_example_simple():
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9


def test_example_with_division():
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6


def test_example_long_expression():
    tokens = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
    assert eval_rpn(tokens) == 22


def test_single_operand():
    assert eval_rpn(["42"]) == 42


def test_single_negative_operand():
    assert eval_rpn(["-42"]) == -42


def test_subtraction_respects_operand_order():
    # 5 - 3, not 3 - 5. The case that catches a swapped pop.
    assert eval_rpn(["5", "3", "-"]) == 2


def test_division_respects_operand_order():
    assert eval_rpn(["6", "3", "/"]) == 2


def test_division_truncates_toward_zero_not_down():
    # Python's // would give -4 here; the problem wants -3.
    assert eval_rpn(["-7", "2", "/"]) == -3
    assert eval_rpn(["7", "-2", "/"]) == -3


def test_positive_division_still_truncates():
    assert eval_rpn(["7", "2", "/"]) == 3


def test_division_of_both_negatives_is_positive():
    assert eval_rpn(["-7", "-2", "/"]) == 3


def test_negative_literals_are_not_mistaken_for_operators():
    assert eval_rpn(["-11", "-2", "*"]) == 22


def test_division_stays_exact_beyond_float_precision():
    # int(a / b) via float would round these operands; exact arithmetic must not.
    big = 2**53 + 1
    assert eval_rpn([str(big), "1", "/"]) == big
    assert eval_rpn([str(-big), "1", "/"]) == -big


def test_multiplication_and_addition_chain():
    assert eval_rpn(["3", "4", "*", "5", "6", "*", "+"]) == 42


def test_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        eval_rpn(["1", "0", "/"])


def test_matches_python_evaluation_on_random_expressions():
    """Build random expression trees, then compare against direct evaluation."""
    rng = random.Random(17)

    def build(depth):
        """Return (rpn_tokens, value)."""
        if depth == 0 or rng.random() < 0.3:
            value = rng.randint(-20, 20)
            return [str(value)], value

        left_tokens, left = build(depth - 1)
        right_tokens, right = build(depth - 1)
        op = rng.choice("+-*/")
        if op == "/" and right == 0:
            op = "+"

        if op == "+":
            value = left + right
        elif op == "-":
            value = left - right
        elif op == "*":
            value = left * right
        else:
            quotient = abs(left) // abs(right)
            value = quotient if (left < 0) == (right < 0) else -quotient

        return left_tokens + right_tokens + [op], value

    for _ in range(400):
        tokens, expected = build(rng.randint(1, 5))
        assert eval_rpn(tokens) == expected, tokens
