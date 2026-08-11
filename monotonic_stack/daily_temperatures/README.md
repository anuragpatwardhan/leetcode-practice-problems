# Daily Temperatures

**Number:** 739
**Difficulty:** Medium
**Pattern:** Monotonic stack
**Problem:** https://leetcode.com/problems/daily-temperatures/

## Problem

Given a list of daily temperatures, return for each day how many days you would wait
for a strictly warmer one, or `0` if none ever comes.

## Approach

This is the "next greater element" problem. The brute force scans forward from every
day, which is `O(n^2)` on a long warm-to-cold run.

The observation that removes the rescanning: if day `j` comes after day `i` and is at
least as warm, then **day `i` is irrelevant to everything after `j`**. Any later day
warm enough to resolve `i` would have resolved `j` first. So only days forming a
strictly decreasing run need to be remembered — everything else has already been ruled
out.

That set is exactly a stack. Push each day's index; before pushing, pop every pending
day this one is warmer than, recording the gap. The stack stays non-increasing in
temperature from bottom to top, which is what makes the top the only candidate worth
testing.

Each index is pushed once and popped at most once, so the total work is linear even
though the inner loop is unbounded — the classic amortised-cost argument. Days still on
the stack at the end never warmed up, and their answers are already `0` from
initialisation.

The comparison is strict. `<` means an equal temperature does not resolve a pending
day, which matches "strictly warmer"; using `<=` would wrongly resolve `[30, 30]` as a
one-day wait.

## Complexity

- **Time:** `O(n)` — amortised, since each index enters and leaves the stack once.
- **Space:** `O(n)` for the stack, which holds every index in the worst case of a
  strictly decreasing sequence. The output array is excluded by the convention in the
  root README.
