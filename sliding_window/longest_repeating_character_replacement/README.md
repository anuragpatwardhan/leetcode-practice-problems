# Longest Repeating Character Replacement

**Number:** 424
**Difficulty:** Medium
**Pattern:** Sliding window with a character count
**Problem:** https://leetcode.com/problems/longest-repeating-character-replacement/

## Problem

Given an uppercase string and a budget `k`, you may replace up to `k` characters with
any other character. Return the length of the longest run of one repeated character
obtainable this way.

## Approach

The useful reframing: rather than deciding *which* characters to replace, ask whether a
given window **could** be made uniform. For a window of width `w` whose most common
character appears `m` times, every other character has to be replaced, so the cost is
`w - m`. The window is achievable exactly when `w - m <= k`.

That makes it a sliding window. Extend the right edge one character at a time, keeping
a count of each character. Whenever the window becomes unachievable, move the left edge
forward by one.

Two details carry the weight.

**The window never shrinks.** The left edge advances by at most one per step, and only
in lockstep with the right edge, so the window's width is non-decreasing. This is why
the answer is `len(s) - left` — the final width — instead of a maximum tracked along
the way. Once a width is known to be achievable, the window only needs to find out
whether a *wider* one is, and it never has to give ground to do so.

**The most-common count is never lowered.** `best_count` only ever rises, so after the
window slides past the run that set it, the value can be stale — higher than any count
actually inside the current window. That looks like a bug and is not one. A stale
`best_count` makes the cost check too generous, so the window can drift along carrying
a width it has not re-earned; but the width only *grows* when some character truly
reaches a new highest count, and growth is all that gets reported. Recomputing the
maximum on every iteration would also be correct, at the cost of a scan over the
alphabet each step.

Because the second point is subtle, the tests check the result against a brute-force
scan of every substring for every binary string up to length 10 and every three-letter
string up to length 7.

## Complexity

- **Time:** `O(n)` — each edge advances at most `n` times, and updating a count is
  `O(1)`.
- **Space:** `O(a)` where `a` is the alphabet size — 26 for this problem, so `O(1)` in
  practice.
