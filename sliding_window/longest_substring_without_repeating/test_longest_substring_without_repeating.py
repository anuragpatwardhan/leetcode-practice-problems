from longest_substring_without_repeating import length_of_longest_substring


def test_example_abcabcbb():
    assert length_of_longest_substring("abcabcbb") == 3


def test_all_same_character():
    assert length_of_longest_substring("bbbbb") == 1


def test_window_must_not_move_backwards():
    # "abba": when the final 'a' is read, its last-seen index is 0 but the window
    # already starts at 2. Moving back would wrongly return 3.
    assert length_of_longest_substring("abba") == 2


def test_example_pwwkew():
    assert length_of_longest_substring("pwwkew") == 3


def test_empty_string():
    assert length_of_longest_substring("") == 0


def test_single_character():
    assert length_of_longest_substring("a") == 1


def test_all_distinct_characters():
    assert length_of_longest_substring("abcdef") == 6


def test_longest_window_is_at_the_end():
    assert length_of_longest_substring("aabcdefg") == 7


def test_spaces_and_symbols_are_ordinary_characters():
    assert length_of_longest_substring("a b!c b") == 5


def test_repeated_pair_pattern():
    assert length_of_longest_substring("abcbadef") == 6
