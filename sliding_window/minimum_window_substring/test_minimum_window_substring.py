from collections import Counter
from itertools import product

from minimum_window_substring import min_window


def brute_force(s, t):
    """Shortest containing substring by direct search, leftmost on a tie."""
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            window = s[i : j + 1]
            if not need - Counter(window):
                if not best or len(window) < len(best):
                    best = window
                break  # extending j only makes this start longer
    return best


def test_example():
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"


def test_single_character_match():
    assert min_window("a", "a") == "a"


def test_target_longer_than_source():
    assert min_window("a", "aa") == ""


def test_no_window_exists():
    assert min_window("abc", "d") == ""


def test_empty_source():
    assert min_window("", "a") == ""


def test_empty_target():
    assert min_window("abc", "") == ""


def test_duplicates_in_target_must_all_appear():
    assert min_window("aa", "aa") == "aa"
    assert min_window("bba", "ab") == "ba"


def test_surplus_copies_do_not_satisfy_a_second_requirement():
    # One 'a' is present but two are required, so there is no valid window.
    assert min_window("abcx", "aab") == ""


def test_whole_string_is_the_answer():
    assert min_window("abc", "cba") == "abc"


def test_leading_and_trailing_noise_is_trimmed():
    assert min_window("xxxABCxxx", "ABC") == "ABC"


def test_prefers_the_shorter_of_two_valid_windows():
    assert min_window("ABBBBBBAC", "AC") == "AC"


def test_target_order_is_irrelevant():
    assert min_window("ADOBECODEBANC", "CBA") == "BANC"


def test_case_is_significant():
    assert min_window("aAbB", "AB") == "AbB"


def test_matches_brute_force_on_short_strings():
    for s_len in range(1, 7):
        for s_tup in product("abc", repeat=s_len):
            s = "".join(s_tup)
            for t in ("a", "b", "c", "ab", "bc", "ac", "abc", "aab"):
                assert min_window(s, t) == brute_force(s, t), (s, t)


def test_matches_brute_force_with_heavy_duplication():
    for s_len in range(1, 9):
        for s_tup in product("ab", repeat=s_len):
            s = "".join(s_tup)
            for t in ("a", "b", "ab", "aa", "bb", "aab", "abb", "aabb"):
                assert min_window(s, t) == brute_force(s, t), (s, t)
