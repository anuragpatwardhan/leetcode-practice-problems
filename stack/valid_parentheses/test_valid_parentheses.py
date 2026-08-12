import random

from valid_parentheses import is_valid


def test_example_simple_pair():
    assert is_valid("()") is True


def test_example_all_three_types():
    assert is_valid("()[]{}") is True


def test_example_mismatched_pair():
    assert is_valid("(]") is False


def test_empty_string_is_valid():
    assert is_valid("") is True


def test_nested_brackets():
    assert is_valid("([{}])") is True


def test_crossed_brackets_are_invalid():
    # Correct counts of each type, but the nesting order is wrong.
    assert is_valid("([)]") is False


def test_unclosed_opener_is_invalid():
    assert is_valid("(((") is False


def test_closer_with_nothing_open_is_invalid():
    assert is_valid(")") is False


def test_closer_arriving_before_its_opener():
    assert is_valid("()]") is False


def test_long_valid_nesting():
    assert is_valid("(" * 500 + ")" * 500) is True


def test_long_nesting_with_one_wrong_closer():
    assert is_valid("(" * 500 + ")" * 499 + "]") is False


def test_matches_a_reference_on_random_bracket_strings():
    def reference(text):
        """Independent check via repeated removal of adjacent pairs."""
        previous = None
        while previous != text:
            previous = text
            for pair in ("()", "[]", "{}"):
                text = text.replace(pair, "")
        return text == ""

    rng = random.Random(41)
    for _ in range(600):
        text = "".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 12)))
        assert is_valid(text) == reference(text), text
