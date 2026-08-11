# Find Minimum in Rotated Sorted Array

**Number:** 153
**Difficulty:** Medium
**Pattern:** Modified binary search
**Problem:** https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

## Problem

An ascending array of distinct integers has been rotated at some unknown pivot. Return
its smallest value in `O(log n)`.

## Approach

The minimum is the single point where the ascending order breaks — the element that is
smaller than the one before it. So this is really a search for the rotation point.

The whole problem reduces to one decision: **is the rotation point left or right of
`mid`?** The comparison that answers it is `nums[mid]` against `nums[high]`.

- `nums[mid] > nums[high]` — a value in the middle outranks the last value, which can
  only happen if the order breaks somewhere after `mid`. The minimum is in
  `(mid, high]`, so `low = mid + 1`.
- Otherwise the run from `mid` to `high` is intact, so nothing after `mid` can beat it.
  The minimum is in `[low, mid]`, so `high = mid` — note `mid` is kept, since `mid`
  itself may be the answer.

The loop runs while `low < high` rather than `low <= high`. The range only ever shrinks
toward a single surviving index, and that index is the answer; testing equality would
loop forever on the `high = mid` branch.

**Comparing against `nums[high]` rather than `nums[low]` is the part that matters.**
The right end is a reliable reference because the minimum is always somewhere at or
before it. The left end is not: on an unrotated array such as `[1,2,3,4,5]`,
`nums[mid] >= nums[low]` holds while the minimum sits at `low`, so a left-hand
comparison discards the very element being looked for.

There is no separate check for "not rotated at all". That case falls out naturally —
`nums[mid] <= nums[high]` every time, so `high` walks down to index `0`.

## Complexity

- **Time:** `O(log n)` — one comparison halves the search range.
- **Space:** `O(1)` — two indices.
