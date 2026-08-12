"""LeetCode 20. Valid Parentheses."""

_CLOSERS = {")": "(", "]": "[", "}": "{"}


def is_valid(s: str) -> bool:
    """True when every bracket is closed by the right type in the right order."""
    open_brackets: list[str] = []

    for char in s:
        if char in _CLOSERS:
            # A closer must match the most recent unclosed opener. Popping an
            # empty stack means a closer arrived first, as in "()]".
            if not open_brackets or open_brackets.pop() != _CLOSERS[char]:
                return False
        else:
            open_brackets.append(char)

    # Anything still open was never closed, so "(((" is invalid even though no
    # mismatch was ever found.
    return not open_brackets
