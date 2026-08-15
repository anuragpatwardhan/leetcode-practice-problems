import random
import string

from implement_trie import Trie


def test_example():
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.starts_with("app") is True
    trie.insert("app")
    assert trie.search("app") is True


def test_empty_trie_finds_nothing():
    trie = Trie()
    assert trie.search("anything") is False
    assert trie.starts_with("a") is False


def test_a_prefix_is_not_a_word_until_inserted():
    # The whole reason nodes carry an is_word flag.
    trie = Trie()
    trie.insert("apple")
    for prefix in ("a", "ap", "app", "appl"):
        assert trie.search(prefix) is False
        assert trie.starts_with(prefix) is True


def test_a_word_is_its_own_prefix():
    trie = Trie()
    trie.insert("cat")
    assert trie.starts_with("cat") is True


def test_longer_query_than_any_word():
    trie = Trie()
    trie.insert("cat")
    assert trie.search("cats") is False
    assert trie.starts_with("cats") is False


def test_the_empty_string():
    trie = Trie()
    # Every trie has a root, so the empty prefix always matches.
    assert trie.starts_with("") is True
    assert trie.search("") is False
    trie.insert("")
    assert trie.search("") is True


def test_words_sharing_a_prefix_are_independent():
    trie = Trie()
    for word in ("car", "card", "care", "careful"):
        trie.insert(word)
    for word in ("car", "card", "care", "careful"):
        assert trie.search(word) is True
    assert trie.search("ca") is False
    assert trie.search("cards") is False


def test_diverging_branches_do_not_leak():
    trie = Trie()
    trie.insert("abc")
    trie.insert("abd")
    assert trie.search("abc") is True
    assert trie.search("abd") is True
    assert trie.search("abe") is False


def test_reinserting_a_word_is_harmless():
    trie = Trie()
    trie.insert("repeat")
    trie.insert("repeat")
    assert trie.search("repeat") is True


def test_single_character_words():
    trie = Trie()
    trie.insert("a")
    assert trie.search("a") is True
    assert trie.search("b") is False
    assert trie.starts_with("a") is True


def test_non_letter_characters():
    trie = Trie()
    trie.insert("a1!")
    assert trie.search("a1!") is True
    assert trie.starts_with("a1") is True


def test_camel_case_alias_matches_the_snake_case_method():
    trie = Trie()
    trie.insert("alias")
    assert trie.startsWith("ali") == trie.starts_with("ali")


def test_matches_a_plain_set_on_random_words():
    """A trie must agree with a set for search, and with any() for prefixes."""
    rng = random.Random(83)
    alphabet = string.ascii_lowercase[:5]

    for _ in range(150):
        words = [
            "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 6)))
            for _ in range(rng.randint(0, 12))
        ]
        trie = Trie()
        for word in words:
            trie.insert(word)
        known = set(words)

        for _ in range(20):
            query = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 6)))
            assert trie.search(query) == (query in known), (words, query)
            expected_prefix = any(w.startswith(query) for w in known)
            assert trie.starts_with(query) == expected_prefix, (words, query)
