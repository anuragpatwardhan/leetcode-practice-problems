# Search in Rotated Sorted Array

**Number:** 33
**Difficulty:** Medium
**Pattern:** Modified binary search
**Problem:** https://leetcode.com/problems/search-in-rotated-sorted-array/

## Problem

An ascending array of distinct integers has been rotated at some unknown pivot, so
`[0,1,2,4,5,6,7]` might arrive as `[4,5,6,7,0,1,2]`. Find the index of a target value,
or `-1` if it is not there. The search has to run in `O(log n)`, which rules out
scanning the array.

## Approach

The array is no longer sorted, so the usual "is the target above or below the middle"
comparison is not enough — `nums[mid] < target` no longer implies the target lies to
the right.

The property that survives rotation is this: **a rotation can only break the ordering
at one point, so at least one side of `mid` is always still sorted.** That gives a way
forward. Identify which side is sorted, and it becomes possible to ask a question that
does have a reliable answer: does the target fall within that side's range?

- If `nums[low] <= nums[mid]`, the left side is sorted. The target is on the left only
  if `nums[low] <= target < nums[mid]`. Otherwise discard the left.
- Otherwise the right side is sorted. The target is on the right only if
  `nums[mid] < target <= nums[high]`. Otherwise discard the right.

Either way half the array is eliminated per iteration, so the logarithmic bound holds.

Checking the range on the *sorted* side is what makes this correct. A range check on
the unsorted side is meaningless — it spans the discontinuity, so a value can sit
inside its numeric bounds while being absent. `[5,6,7,1,2,3]` searching for `4`
demonstrates it: `4` lies between `nums[low]=5`'s run and `nums[high]=3`'s run and
appears in neither.

The comparison `nums[low] <= nums[mid]` needs its equality. Once two elements remain,
integer division puts `mid` on `low`, and a strict `<` would read that side as
unsorted and follow the wrong branch — `[3,1]` searching for `1` is the smallest case
that exposes it.

## Complexity

- **Time:** `O(log n)` — each iteration discards half the remaining range, exactly as
  in an ordinary binary search. The rotation only changes *which* half is discarded.
- **Space:** `O(1)` — two indices, no auxiliary structure, no recursion.
