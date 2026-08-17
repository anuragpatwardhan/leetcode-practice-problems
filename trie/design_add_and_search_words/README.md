# Design Add and Search Words Data Structure

**Number:** 211
**Difficulty:** Medium
**Pattern:** Trie with wildcard search
**Problem:** https://leetcode.com/problems/design-add-and-search-words-data-structure/

## Problem

Support `addWord(word)` and `search(word)`, where the query may contain `.` as a
wildcard matching any single character.

## Approach

Adding is exactly [Implement Trie](../implement_trie/) (LC 208) — walk the characters,
creating nodes only where the path does not exist, and flag the end.

Search is where it diverges. A plain trie lookup keeps **one pointer** and follows it. A
wildcard can match any child, so from that position the search is suddenly in several
places at once. The fix is to carry a **frontier of candidate nodes** instead of a single
pointer.

For each character of the query:

- A literal narrows every candidate to the one matching child, dropping candidates that
  do not have it.
- A `.` expands every candidate into all of its children.

If the frontier ever empties, no stored word can match and the search stops early rather
than walking the rest of the query.

Two things that are easy to get wrong:

**The final `is_word` check still applies.** Arriving at a set of nodes only proves paths
of the right length exist. Without checking the flag, `search("app")` would return true
after only `apple` was added.

**A wildcard is exactly one character, never "the rest".** `app.` does not match `apple`,
because the query is four characters and the word is five. Length always has to match,
wildcards or not. My first draft of the tests asserted `appl.` should *fail* against
`apple` — it should pass, since the dot legitimately matches the final `e`. The
implementation was right and the test was wrong.

The frontier is walked **iteratively**. The natural formulation is recursive, but a query
of all dots against a deep trie recurses once per character and branches at every step;
the loop keeps the stack flat.

## Verification

Because a `.` here means precisely what it means in a regular expression, `re.fullmatch`
is a clean independent oracle. The random test builds small dictionaries over a
four-letter alphabet, fires wildcard-heavy queries at both, and requires they agree —
which caught the test bug above rather than letting it through.

## Complexity

With `m` the query length and `k` the alphabet size:

- **Add:** `O(m)`.
- **Search:** `O(m)` with no wildcards. Each `.` can multiply the frontier by up to `k`,
  so the worst case is `O(k^d · m)` for `d` wildcards — an all-dots query genuinely does
  visit every node at that depth. Bounded by the number of nodes in the trie.
- **Space:** `O(total characters added)`, plus the frontier during a search.
