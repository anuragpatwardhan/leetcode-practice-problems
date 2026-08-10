# Longest Substring Without Repeating Characters

**Number:** 3
**Difficulty:** Medium
**Pattern:** Sliding window
**Problem:** https://leetcode.com/problems/longest-substring-without-repeating-characters/

## Problem

Given a string, find the length of the longest substring that contains no repeated
character. Substrings are contiguous, which is what makes a window the right tool.

## Approach

Maintain a window `s[start..index]` that is always free of duplicates, and slide its
right edge forward one character at a time. The only question is where the left edge
has to move when the new character is already inside the window.

Rather than shrinking the window one step at a time, store the **last index at which
each character was seen**. When the incoming character was last seen at position
`previous`, the window can jump straight to `previous + 1` — every position before
that is guaranteed to still contain the duplicate. That makes each character a
single `O(1)` update instead of a rescan.

The `previous >= start` check is the subtle part, and skipping it is the usual bug.
The map remembers characters that have already fallen out of the window, so a stale
entry can report an index to the left of `start`. Jumping there would move the left
edge *backwards*, re-admitting duplicates and overstating the answer. Guarding on
`previous >= start` keeps the window monotonically forward-moving. `"abba"` is the
smallest input that exposes this: when the final `a` is read, `last_seen["a"]` is
still `0`, but `start` has already advanced to `2`.

Because the answer is recomputed at every position with `index - start + 1`, there
is no need to track where the best window started.

## Complexity

- **Time:** `O(n)` — each character is read once and the left edge only ever moves
  forward, so both pointers traverse the string at most once.
- **Space:** `O(min(n, k))` where `k` is the alphabet size, for the map of last-seen
  indices. The map holds at most one entry per distinct character.
