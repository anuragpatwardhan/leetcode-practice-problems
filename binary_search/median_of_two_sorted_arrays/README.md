# Median of Two Sorted Arrays

**Number:** 4
**Difficulty:** Hard
**Pattern:** Binary search on a partition
**Problem:** https://leetcode.com/problems/median-of-two-sorted-arrays/

## Problem

Given two sorted arrays, return the median of their combined contents in
`O(log(m + n))`. The bound rules out merging them, which would be `O(m + n)`.

## Approach

The median does not require the merged array — only the boundary between its lower and
upper halves. So search for that boundary directly.

Cut each array into a left and a right part such that:

1. the two left parts together hold exactly half the elements, and
2. every value on the left is `<=` every value on the right.

Once such a cut exists, the median follows immediately: for an odd total it is the
largest value on the left, and for an even total it is the average of the largest on
the left and the smallest on the right.

Condition 1 makes this a one-dimensional search. Choosing `i` elements from the first
array forces `j = half - i` from the second, so there is only one variable, and binary
search over `i` applies. `half` is `(m + n + 1) // 2`, where the `+1` places the odd
element on the left so the odd case reads off the left side.

Condition 2 reduces to two comparisons across the cut. With each array already sorted,
the only pairs that can violate it are `a_left > b_right` and `b_left > a_right`:

- `a_left > b_right` — too many taken from `a`, so search lower.
- `b_left > a_right` — too few taken from `a`, so search higher.
- Neither — the cut is correct.

**Binary searching the shorter array is not just an optimisation.** It keeps
`j = half - i` inside the bounds of the longer array; searching the longer one could
drive `j` negative or past the end.

The `±inf` sentinels for the four boundary values remove every edge case. When a cut
sits at the very start of an array there is nothing on its left, and `-inf` never
triggers a violation; at the very end, `+inf` is never selected as a minimum. An empty
input array is then handled by the same code path as any other, with no special
branch — which is why `[]` paired with `[1,2,3]` needs no separate handling.

The loop cannot fall through on valid input. Reaching the end means no partition
satisfied the ordering, which is only possible if an input was not sorted ascending, so
that case raises rather than returning a wrong number silently.

## Complexity

- **Time:** `O(log min(m, n))` — binary search over the shorter array's length, with
  `O(1)` work per step.
- **Space:** `O(1)` — a few indices and boundary values.
