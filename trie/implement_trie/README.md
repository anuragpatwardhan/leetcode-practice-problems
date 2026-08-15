# Implement Trie (Prefix Tree)

**Number:** 208
**Difficulty:** Medium
**Pattern:** Trie / prefix tree
**Problem:** https://leetcode.com/problems/implement-trie-prefix-tree/

## Problem

Build a prefix tree supporting `insert(word)`, `search(word)` for an exact match, and
`startsWith(prefix)` for any word beginning with that prefix.

## Approach

A hash set answers `search` in O(1) and `startsWith` not at all — checking a prefix
against a set means scanning every key. The trie trades that: it stores words by
*shared path*, so a prefix query is just a walk.

Each node holds a map from the next character to a child. Inserting walks the word one
character at a time, creating nodes only where the path does not already exist, so
`car`, `card` and `care` share four nodes rather than storing eleven characters.

**The `is_word` flag is the part that is easy to leave out.** Without it, inserting
`apple` would make `search("app")` return true, because those nodes exist on the way.
Existence of a path proves only that some word runs through here, not that the path
itself was ever inserted. That flag is exactly the difference between `search` and
`startsWith` — both walk identically, and only `search` checks it afterwards.

Both operations share one private `_walk`, which returns the node the path ends at or
`None` if it breaks. `search` then asks "and is it a word?"; `startsWith` just asks "did
we get there?".

Two smaller decisions:

- **`__slots__` on the node.** A trie over a real dictionary allocates one node per
  distinct prefix. Dropping the per-instance `__dict__` cuts the footprint of every one
  of them, which is the difference between a trie being practical and being a memory
  hog.
- **`setdefault` rather than a membership test.** It creates the child only when
  missing, in one lookup instead of two.

The empty string behaves consistently and is worth knowing: `startsWith("")` is always
true because every trie has a root, while `search("")` is false until you insert it.

`startsWith` is aliased to the snake_case `starts_with` so the file stays pasteable into
LeetCode without breaking the repo's naming.

## Complexity

With `m` the length of the queried word:

- **Insert / search / startsWith:** `O(m)` — independent of how many words are stored.
- **Space:** `O(total characters inserted)` in the worst case of no shared prefixes;
  far less in practice, since sharing is the point.
