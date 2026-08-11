# Merge Intervals

**Number:** 56
**Difficulty:** Medium
**Pattern:** Sort by start, then sweep
**Problem:** https://leetcode.com/problems/merge-intervals/

## Problem

Given a collection of intervals, merge all overlapping ones and return the smallest set
of non-overlapping intervals covering exactly the same points.

## Approach

Unsorted, an interval can overlap any other, so deciding what merges with what is a
pairwise question. **Sorting by start point turns it into a local one.**

Once the intervals arrive in start order, any interval that overlaps the group being
built must overlap it at its right edge — its start cannot precede anything already
absorbed. So only the most recently kept interval needs to be compared against, and one
pass suffices.

For each interval in order: if it starts at or before the current group's end, extend
that group; otherwise the group is finished and a new one begins.

Two details:

- **Touching counts as overlapping.** `start <= current_end` rather than `<`, so
  `[1,4]` and `[4,5]` become `[1,5]`. Whether that is right depends on whether the
  bounds are closed, which this problem treats as so.
- **The end must be a `max`, not an assignment.** A later interval can be entirely
  contained in the current group — `[1,10]` followed by `[2,3]` — and blindly assigning
  would truncate the result to `[1,3]`, dropping covered points.

The solution sorts a copy and builds new lists rather than mutating the caller's
intervals, since the merging step writes to the end value in place.

## Complexity

- **Time:** `O(n log n)`, dominated entirely by the sort; the sweep is `O(n)`.
- **Space:** `O(n)` for the sorted copy. Python's sort also needs `O(n)` of its own, so
  this cannot be reduced to `O(1)` auxiliary space without sorting in place.
