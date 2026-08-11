# Minimum Window Substring

**Number:** 76
**Difficulty:** Hard
**Pattern:** Variable-size sliding window with a character debt
**Problem:** https://leetcode.com/problems/minimum-window-substring/

## Problem

Given strings `s` and `t`, return the shortest substring of `s` that contains every
character of `t`, respecting multiplicity — if `t` holds two of a character, the window
must hold at least two. Return `""` if no such substring exists.

## Approach

A window that already contains everything needed stays valid when it grows, and can
only become invalid when it shrinks. That monotonicity is what makes one pass enough:
extend the right edge until the window is valid, then pull the left edge in as far as
it will go while it stays valid, recording the width each time. Every position is
visited at most twice.

The whole difficulty is answering **"is this window valid?"** in `O(1)`. Rescanning the
window's counts on each step would make it quadratic.

The trick is to track a single integer, `missing` — how many characters are still owed
in total, duplicates counted separately — alongside a per-character count that is
allowed to go **negative**. `remaining[c]` starts at the number of copies of `c` that
`t` requires:

- Positive: still owed that many.
- Zero: exactly satisfied.
- Negative: that many surplus copies are sitting in the window.

Adding a character always decrements its count, but only decrements `missing` when the
count was still **positive** — that is, when the character was genuinely needed.
Removing a character always increments its count, but only increments `missing` when
the count comes back **above zero**, meaning a surplus copy has been used up and a
truly needed one has now left.

The window is valid exactly when `missing == 0`, so validity is one comparison.

Letting counts go negative is what makes surplus copies free. Clamping them at zero
would lose the distinction between "this window has one spare `a`" and "this window has
exactly the `a` it needs", and the left edge would stop advancing too early — the
window could not slide past a redundant copy without believing it had broken itself.

`"abcx"` with target `"aab"` shows the multiplicity requirement: an `a` and a `b` are
both present, but only one `a`, so the correct answer is `""` rather than `"ab"`.

## Complexity

- **Time:** `O(n + m)` for `n = len(s)`, `m = len(t)`. Building the initial counts is
  `O(m)`; each edge crosses each index at most once.
- **Space:** `O(a)` for the count map, bounded by the alphabet size — `O(1)` for a
  fixed alphabet.
