# Insert Interval

**Number:** 57
**Difficulty:** Medium
**Pattern:** Linear sweep over sorted intervals
**Problem:** https://leetcode.com/problems/insert-interval/

## Problem

Given a list of non-overlapping intervals **already sorted by start**, insert a new
interval, merging where it overlaps, and keep the result sorted and non-overlapping.

## Approach

The precondition is the whole point. Because the input is already sorted and disjoint,
no sort is needed and the answer falls into three consecutive stretches:

1. **Before** — intervals ending strictly before the new one starts. Copied through
   untouched.
2. **Overlapping** — intervals starting at or before the new one's (possibly widened)
   end. These are absorbed, and a single merged interval is emitted.
3. **After** — everything remaining. Since the input was disjoint and sorted, these
   start after the merged interval ends, so they too are copied through.

Each stretch is a `while` loop over the same cursor, so every interval is visited once.

The boundary conditions carry the meaning:

- Phase 1 uses **strict** `<` on the end. An interval that merely touches the new one —
  `[1,2]` with an insert of `[2,5]` — must fall through to phase 2 and merge, not be
  emitted separately.
- Phase 2 needs a `min` on the start, not just a `max` on the end. An absorbed interval
  can begin earlier than the new one: inserting `[2,3]` into `[[1,5]]` must yield
  `[1,5]`, and taking the new interval's start would wrongly give `[2,5]`.

Contrast with [Merge Intervals](../merge_intervals/) (LC 56), which solves the general
case in `O(n log n)`. Sorting the input plus the new interval and re-merging would work
here too, but it throws away the ordering guarantee and costs an unnecessary log factor.
The tests check this solution against exactly that approach on random inputs.

## Complexity

- **Time:** `O(n)` — one pass, no sort.
- **Space:** `O(n)` for the result. Auxiliary space beyond the output is `O(1)`.
