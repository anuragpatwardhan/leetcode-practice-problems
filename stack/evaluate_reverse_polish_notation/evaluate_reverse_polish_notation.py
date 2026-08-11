"""LeetCode 150. Evaluate Reverse Polish Notation."""

from typing import Callable, Dict, List


def _truncating_div(left: int, right: int) -> int:
    """Integer division that truncates toward zero, as the problem requires.

    Python's ``//`` floors instead, so ``-7 // 2`` is ``-4`` where this problem
    wants ``-3``. Writing ``int(left / right)`` would truncate correctly but goes
    through a float, silently losing precision once the operands exceed 2**53.
    Dividing the magnitudes and reapplying the sign stays exact for any integer.
    """
    quotient = abs(left) // abs(right)
    return quotient if (left < 0) == (right < 0) else -quotient


_OPERATORS: Dict[str, Callable[[int, int], int]] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": _truncating_div,
}


def eval_rpn(tokens: List[str]) -> int:
    """Evaluate an arithmetic expression given in reverse Polish notation."""
    operands: List[int] = []

    for token in tokens:
        # A negative literal such as "-11" is not the "-" operator: an exact
        # dictionary lookup distinguishes them, where a "starts with -" check
        # would not.
        if token in _OPERATORS:
            # The stack yields operands in reverse, so the first pop is the
            # right-hand side. Getting this backwards still passes for + and *
            # and fails only for - and /, which is what makes it easy to miss.
            right = operands.pop()
            left = operands.pop()
            operands.append(_OPERATORS[token](left, right))
        else:
            operands.append(int(token))

    return operands[-1]
