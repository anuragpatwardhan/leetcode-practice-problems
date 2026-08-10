# Longest Consecutive Sequence

**Number:** 128
**Difficulty:** Medium
**Pattern:** Hash set
**Problem:** https://leetcode.com/problems/longest-consecutive-sequence/

## Problem

Given an unsorted list of integers, find how long the longest run of consecutive
values is. The values do not have to appear next to each other in the list, and the
solution has to run in linear time — which is what rules out the obvious approach.

## Approach

Sorting solves this immediately but costs `O(n log n)`, so it fails the time
requirement. The linear approach is to put every value in a hash set and then count
runs by walking upward from each value.

The trick is to avoid re-walking the same run. If `value - 1` is also in the set,
then `value` is somewhere in the middle of a run and some smaller element will cover
it — so we skip it entirely. We only start counting when `value - 1` is absent,
meaning `value` is the smallest member of its run.

That guard is what keeps the algorithm linear. Without it, an input like
`[1, 2, 3, ..., n]` would walk a run of length `n` from every starting point and
degrade to `O(n²)`. With it, every value is visited at most twice overall: once by
the outer loop and once by the inner `while` of the run it belongs to.

Building the set also handles duplicates for free — `[1, 1, 2]` collapses to
`{1, 2}` and correctly returns `2`.

## Complexity

- **Time:** `O(n)` — the set is built in one pass, and across all iterations the
  inner loop advances a total of `O(n)` steps because each run is walked exactly once.
- **Space:** `O(n)` for the set of distinct values.
