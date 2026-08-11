# Sliding Window Maximum

**Number:** 239
**Difficulty:** Hard
**Pattern:** Monotonic deque
**Problem:** https://leetcode.com/problems/sliding-window-maximum/

## Problem

Given an array and a window size `k`, return the maximum of every contiguous window as
the window slides one position at a time.

## Approach

Recomputing `max` per window is `O(n·k)`. A heap gets to `O(n log k)` but needs lazy
deletion, since the element leaving the window is rarely the one at the top. The linear
solution comes from asking which elements could *ever* be a future maximum.

**If a later element is at least as large as an earlier one, the earlier one is finished.**
It is smaller (or equal) *and* expires sooner, so there is no window in which it wins.
Discard it immediately.

What survives is a sequence of indices whose values strictly decrease. Keeping only
those, the front is always the current window's maximum — no search required.

Two operations are needed each step, at opposite ends:

- **Back:** pop everything the incoming value dominates, then append it.
- **Front:** drop the front if it has slid out of the window.

Needing both ends is exactly why this is a deque and not a stack. Only one index can
expire per step, since the window advances by one, so the front check is a single `if`.

Results are recorded from index `k-1` onward, the first point at which a full window
exists.

The `while` loop looks like it could make a step expensive, but each index is appended
once and removed once across the whole run, so total work is linear — the same amortised
argument as [Daily Temperatures](../../monotonic_stack/daily_temperatures/) (LC 739).
The difference is the front eviction: there, candidates only ever leave by being
resolved; here they also leave by aging out.

The pop condition is `<=` rather than `<`, so an equal newer value evicts the older one.
Either is correct for the reported maximum, but `<=` keeps the deque shorter on inputs
with many duplicates. The tests cover a 0–2 value range specifically to exercise that.

## Complexity

- **Time:** `O(n)` — amortised; every index enters and leaves the deque at most once.
- **Space:** `O(k)` — the deque never holds more than one window's worth of indices.
