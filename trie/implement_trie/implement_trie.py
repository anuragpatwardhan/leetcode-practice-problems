"""LeetCode 208. Implement Trie (Prefix Tree)."""

from typing import Dict, Optional


class TrieNode:
    """One character position. Children are keyed by the next character."""

    # __slots__ matters here: a trie over a large dictionary allocates one node
    # per distinct prefix, and dropping the per-instance __dict__ cuts the
    # footprint of every one of them.
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        # Marks the end of an inserted word. Without it "app" would appear to be
        # present merely because "apple" was inserted through those nodes.
        self.is_word = False


class Trie:
    """A prefix tree supporting insert, exact search and prefix search."""

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Add a word. Re-inserting an existing word is a no-op."""
        node = self.root
        for char in word:
            # setdefault creates the child only when the path does not exist, so
            # shared prefixes are walked rather than duplicated.
            node = node.children.setdefault(char, TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        """True only if the exact word was inserted."""
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        """True if any inserted word begins with this prefix."""
        return self._walk(prefix) is not None

    # LeetCode's signature is camelCase; the alias keeps the solution pasteable
    # there while the rest of the repo stays snake_case.
    startsWith = starts_with

    def _walk(self, text: str) -> Optional[TrieNode]:
        """Follow `text` from the root, or return None if the path breaks."""
        node = self.root
        for char in text:
            child = node.children.get(char)
            if child is None:
                return None
            node = child
        return node
