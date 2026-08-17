import random
import re
import string

from design_add_and_search_words import WordDictionary


def build(*words):
    wd = WordDictionary()
    for word in words:
        wd.add_word(word)
    return wd


def test_example():
    wd = build("bad", "dad", "mad")
    assert wd.search("pad") is False
    assert wd.search("bad") is True
    assert wd.search(".ad") is True
    assert wd.search("b..") is True


def test_empty_dictionary_matches_nothing():
    wd = WordDictionary()
    assert wd.search("a") is False
    assert wd.search(".") is False


def test_a_prefix_is_not_a_word():
    wd = build("apple")
    assert wd.search("apple") is True
    # Shorter queries fail on length, wildcard or not — a wildcard stands for
    # exactly one character, never for "the rest of the word".
    assert wd.search("app") is False
    assert wd.search("app.") is False
    # Same length, so the dot legitimately matches the final "e".
    assert wd.search("appl.") is True


def test_all_wildcards_matches_any_word_of_that_length():
    wd = build("cat", "dogs")
    assert wd.search("...") is True
    assert wd.search("....") is True
    assert wd.search(".....") is False


def test_length_must_match_exactly():
    wd = build("cat")
    assert wd.search("ca") is False
    assert wd.search("cats") is False


def test_wildcard_at_each_position():
    wd = build("abc")
    assert wd.search(".bc") is True
    assert wd.search("a.c") is True
    assert wd.search("ab.") is True
    assert wd.search("...") is True


def test_wildcard_that_cannot_be_satisfied():
    wd = build("abc")
    assert wd.search(".bd") is False
    assert wd.search("a.d") is False


def test_branches_are_explored_not_just_the_first():
    # "a.c" must keep looking after the "abx" branch dead-ends.
    wd = build("abx", "adc")
    assert wd.search("a.c") is True


def test_words_of_different_lengths_coexist():
    wd = build("a", "ab", "abc")
    assert wd.search("a") is True
    assert wd.search("ab") is True
    assert wd.search("abc") is True
    assert wd.search("abcd") is False


def test_the_empty_string():
    wd = WordDictionary()
    assert wd.search("") is False
    wd.add_word("")
    assert wd.search("") is True


def test_re_adding_a_word_is_harmless():
    wd = build("same", "same")
    assert wd.search("same") is True


def test_camel_case_alias_adds_the_same_word():
    wd = WordDictionary()
    wd.addWord("alias")
    assert wd.search("alias") is True


def test_matches_a_regex_reference_on_random_input():
    """The wildcard is exactly '.' in a fullmatch, so regex is a clean oracle."""
    rng = random.Random(107)
    alphabet = string.ascii_lowercase[:4]

    for _ in range(200):
        words = [
            "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4)))
            for _ in range(rng.randint(0, 8))
        ]
        wd = build(*words)
        known = set(words)

        for _ in range(20):
            query = "".join(
                rng.choice(alphabet + ".") for _ in range(rng.randint(1, 4))
            )
            expected = any(re.fullmatch(query, w) for w in known)
            assert wd.search(query) == expected, (words, query)
