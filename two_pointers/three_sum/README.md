# 3Sum

**Number:** 15
**Difficulty:** Medium
**Pattern:** Sorting + two pointers
**Problem:** https://leetcode.com/problems/3sum/

## Problem

Find every unique triplet in a list of integers that sums to zero. The hard part is
not finding the triplets — it is returning each distinct triplet exactly once when
the input contains repeated values.

## Approach

Sorting first is what makes everything else work. Once the list is sorted, fixing
one value reduces the problem to 2Sum on a sorted range, which the two-pointer
technique solves in linear time: if the current sum is too small move the left
pointer right, if it is too large move the right pointer left.

So the shape is: for each index `i`, run a two-pointer scan over `nums[i+1:]`
looking for a pair that sums to `-nums[i]`. That is `O(n)` work per anchor, giving
`O(n²)` overall — better than the `O(n³)` brute force.

Deduplication is handled at two levels, and both are necessary:

1. **Anchors.** If `nums[i] == nums[i - 1]`, the previous iteration already found
   every triplet starting with that value, so skip it. The `i > 0` guard matters —
   without it the very first anchor would be compared against `nums[-1]`, the last
   element of the list.
2. **Pairs.** After recording a triplet, advance both pointers past any repeats of
   the values just used. Otherwise input like `[0, 0, 0, 0]` would record `[0,0,0]`
   more than once.

The `nums[i] > 0` early exit is a small but real optimisation: the list is sorted,
so once the anchor is positive every remaining value is positive too and no triplet
can sum to zero.

Sorting also means each returned triplet is already in ascending order, which
matches what the problem asks for.

## Complexity

- **Time:** `O(n²)` — an `O(n log n)` sort, then an `O(n)` two-pointer scan for each
  of the `O(n)` anchors, which dominates.
- **Space:** `O(n)` for the sorted copy of the input. Excluding that copy and the
  returned list, the scan itself uses `O(1)` auxiliary space.
