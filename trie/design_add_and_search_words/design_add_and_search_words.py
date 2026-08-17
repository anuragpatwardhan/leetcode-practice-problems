"""LeetCode 211. Design Add and Search Words Data Structure."""

from typing import Dict, List


class TrieNode:
    """One character position. Children are keyed by the next character."""

    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_word = False


class WordDictionary:
    """A trie where search accepts '.' as a single-character wildcard."""

    def __init__(self) -> None:
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        """True if any stored word matches, treating '.' as any one character."""
        # A wildcard turns the walk into a search over several possible paths at
        # once, so this needs a frontier of candidate nodes rather than the
        # single pointer a plain trie lookup uses.
        #
        # Iterative rather than recursive: a query of all dots against a deep
        # trie would otherwise recurse once per character.
        frontier: List[TrieNode] = [self.root]

        for char in word:
            next_frontier: List[TrieNode] = []
            for node in frontier:
                if char == ".":
                    # Every child is a possible continuation.
                    next_frontier.extend(node.children.values())
                else:
                    child = node.children.get(char)
                    if child is not None:
                        next_frontier.append(child)
            if not next_frontier:
                # No candidate survived, so no stored word can match.
                return False
            frontier = next_frontier

        # Reaching the end is not enough — at least one candidate has to be the
        # end of a real word, or "app" would match after only "apple" was added.
        return any(node.is_word for node in frontier)

    # LeetCode's signature is camelCase; the alias keeps this pasteable there
    # while the rest of the repo stays snake_case.
    addWord = add_word
