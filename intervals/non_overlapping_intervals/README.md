# Non-overlapping Intervals

**Number:** 435
**Difficulty:** Medium
**Pattern:** Greedy, sort by end
**Problem:** https://leetcode.com/problems/non-overlapping-intervals/

## Problem

Return the minimum number of intervals to remove so that none of the remaining ones
overlap. Touching endpoints do not count as overlapping.

## Approach

Removing the fewest is the same as **keeping the most**, which turns this into interval
scheduling — the classic activity-selection problem.

The greedy rule: when two intervals conflict, keep whichever **finishes first**. An
interval that ends earlier constrains everything after it no more than one ending later
does, so keeping it is never worse. That makes the end point the sort key.

Walk the sorted list holding the end of the last interval kept. If the next one starts
before that end, it conflicts — drop it and count. Otherwise keep it and advance.

**Sorting by start is the trap.** It looks equally reasonable and is wrong:
`[[1,100],[2,3],[4,5]]` puts `[1,100]` first, which then conflicts with both short
intervals, reporting 2 removals. Sorting by end finds the real answer of 1.

Note the contrast with [Merge Intervals](../merge_intervals/) (LC 56), which sorts by
**start**. The key follows the question: merging asks what runs together, so starts
matter; scheduling asks what fits next, so ends do.

Touching is allowed here, so the conflict test is `start < kept_end`, strictly. Using
`<=` would wrongly discard `[2,3]` next to `[3,4]`.

## A subtlety the random tests exposed

LeetCode guarantees `start < end`, so every interval has positive length. My random test
generator did not, and produced zero-length intervals — where a **tie on the end point
starts to matter**. Given `[3,3]` and `[2,3]`, both can be kept, since they only touch.
But if `[3,3]` is processed first, `[2,3]` starts before the kept end of `3` and gets
discarded, over-counting by one.

Breaking ties by earlier start fixes it. It is unreachable under the problem's stated
constraints, but it costs nothing and makes the function correct for any input rather
than only the ones LeetCode promises.

## Complexity

- **Time:** `O(n log n)`, dominated by the sort; the sweep is `O(n)`.
- **Space:** `O(n)` for the sorted copy, so the caller's list is left untouched.
