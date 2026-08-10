# Subarray Sum Equals K

**Number:** 560
**Difficulty:** Medium
**Pattern:** Prefix sum + hash map
**Problem:** https://leetcode.com/problems/subarray-sum-equals-k/

## Problem

Count the contiguous subarrays whose values sum to `k`. The array can contain
negative numbers and zero, which is the detail that decides the whole approach.

## Approach

The obvious `O(n²)` solution fixes a start index and extends the end. The obvious
*wrong* improvement is a sliding window: windows only work when growing the window
grows the sum monotonically, and with negative values it does not. Adding an element
can shrink the total, so there is no rule for when to advance the left edge. This is
the trap in the problem.

What does work is prefix sums. If `P(i)` is the sum of the first `i` elements, the
sum of the subarray `(j, i]` is `P(i) - P(j)`. So a subarray ending at `i` sums to
`k` exactly when some earlier prefix satisfies `P(j) = P(i) - k`.

That turns the question into a lookup. Walk the array once keeping the running
prefix sum, and keep a map from prefix value to **how many times it has occurred**.
At each step, the number of subarrays ending here is however many times
`running - k` has already been seen.

Two details carry the correctness:

1. **Seed the map with `{0: 1}`.** The empty prefix sums to zero. Without it, a
   subarray that starts at index 0 and sums to `k` is never counted — `[1, 1, 1]`
   with `k = 2` would return 1 instead of 2.
2. **Count occurrences, not existence.** The same prefix sum can be reached by
   several different indices, and each one is a distinct subarray. Storing a set
   rather than a counter undercounts on input like `[0, 0, 0]` with `k = 0`, which
   has six valid subarrays.

Recording the current prefix *after* the lookup also matters. Doing it first would
let a subarray of length zero match whenever `k == 0`.

## Complexity

- **Time:** `O(n)` — one pass, with `O(1)` expected map operations per element.
- **Space:** `O(n)` for the prefix-count map, which in the worst case holds one entry
  per distinct prefix sum.
