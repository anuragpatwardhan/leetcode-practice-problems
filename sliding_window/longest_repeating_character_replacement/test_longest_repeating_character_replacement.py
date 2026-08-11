from collections import Counter
from itertools import product

from longest_repeating_character_replacement import character_replacement


def brute_force(s, k):
    """Check every substring directly. Only viable for short inputs."""
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            window = s[i : j + 1]
            replacements = len(window) - max(Counter(window).values())
            if replacements <= k:
                best = max(best, len(window))
    return best


def test_example_one():
    assert character_replacement("ABAB", 2) == 4


def test_example_two():
    assert character_replacement("AABABBA", 1) == 4


def test_empty_string():
    assert character_replacement("", 2) == 0


def test_single_character():
    assert character_replacement("A", 0) == 1


def test_already_uniform_needs_no_replacements():
    assert character_replacement("AAAA", 0) == 4


def test_no_replacements_allowed_finds_the_longest_existing_run():
    assert character_replacement("ABBBCC", 0) == 3


def test_budget_larger_than_the_string_takes_everything():
    assert character_replacement("ABCDE", 10) == 5


def test_budget_exactly_covers_the_string():
    assert character_replacement("ABCDE", 4) == 5


def test_the_best_window_is_not_the_last_one():
    # The winning run sits at the start, so a solution that reported the final
    # window position rather than its width would get this wrong.
    assert character_replacement("AABAABBBBBBBB", 0) == 8


def test_lowercase_and_mixed_case_are_distinct():
    assert character_replacement("aAaA", 0) == 1
    assert character_replacement("aAaA", 2) == 4


def test_matches_brute_force_on_every_short_binary_string():
    for length in range(1, 11):
        for tup in product("AB", repeat=length):
            s = "".join(tup)
            for k in range(0, 4):
                assert character_replacement(s, k) == brute_force(s, k), (s, k)


def test_matches_brute_force_on_three_letter_alphabets():
    for length in range(1, 8):
        for tup in product("ABC", repeat=length):
            s = "".join(tup)
            for k in (0, 1, 2):
                assert character_replacement(s, k) == brute_force(s, k), (s, k)
