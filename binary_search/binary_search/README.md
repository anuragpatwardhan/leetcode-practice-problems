# Binary Search

**Number:** 704
**Difficulty:** Easy
**Pattern:** Binary search
**Problem:** https://leetcode.com/problems/binary-search/

## Problem

Return the index of a target in a sorted ascending array of distinct values, or `-1`.

## Approach

Keep an inclusive range `[low, high]`. Compare the midpoint and discard the half that
cannot contain the target. Every step halves the search space, so the array is exhausted
in logarithmic time.

The algorithm is four lines. What makes it worth writing down is that **all three of its
classic bugs are silent or fatal rather than merely wrong**.

**`while low <= high`, not `<`.** With inclusive bounds, `low == high` still leaves one
unchecked candidate. An exclusive condition skips it, so every single-element search
returns `-1` — and that failure only shows up on the smallest possible input, which is
exactly the case a quick manual test tends to skip.

**`low = mid + 1`, not `low = mid`.** The midpoint has already been compared and ruled
out, so the range must move past it. Assigning `low = mid` leaves the range unchanged
when `high == low + 1`, and the loop spins forever. That is a hang, not a wrong answer —
which is why the tests include a two-million-element array whose real purpose is proving
termination.

**`low + (high - low) // 2`, not `(low + high) // 2`.** In Python these are identical,
since integers never overflow. The habit is written in anyway because in a fixed-width
language `low + high` can exceed the type on a large array, and the version above cannot.
It costs nothing here and is the form worth having in muscle memory.

## Why this one is here

Three harder problems in this repo already rest on it —
[Search in Rotated Sorted Array](../search_in_rotated_sorted_array/) (LC 33),
[Find Minimum in Rotated Sorted Array](../find_minimum_in_rotated_sorted_array/) (LC 153)
and [Median of Two Sorted Arrays](../median_of_two_sorted_arrays/) (LC 4).

Each of those changes what the comparison means — LC 33 asks which half is sorted, LC 153
compares against the right end, LC 4 searches over a partition rather than over values —
but every one of them keeps this loop's invariant and termination argument. Having the
plain case written down makes the variations legible as variations.

## Complexity

- **Time:** `O(log n)`.
- **Space:** `O(1)` — iterative, so no call stack.
