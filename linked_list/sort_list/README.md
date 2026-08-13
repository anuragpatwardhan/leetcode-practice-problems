# Sort List

**Number:** 148
**Difficulty:** Medium
**Pattern:** Merge sort on a linked list
**Problem:** https://leetcode.com/problems/sort-list/

## Problem

Sort a linked list in ascending order, in `O(n log n)` time and without copying values
into another structure.

## Approach

Merge sort is the natural fit, and for once the linked list is an *advantage*. On an
array, merging needs a scratch buffer of the same size. On a list, merging is pure
pointer relinking — the extra space arrays pay for disappears.

Quicksort would be the other `O(n log n)` candidate, but it depends on random access to
pick and swap around a pivot, which a singly linked list does not offer.

Three steps: split at the middle, sort each half recursively, merge the sorted halves.

**Starting `fast` one node ahead is what makes it terminate.** The split biases so the
left half is never longer than the right, guaranteeing both are strictly shorter than
the input. With `fast = head`, a two-node list puts *both* nodes on the left, the
recursion never shrinks, and it loops forever. This is the single most important line,
and it fails only on inputs of exactly two elements — easy to miss by testing on longer
lists.

**The merge is stable** because ties emit the left node first (`<=`, not `<`). Stability
does not change the answer when sorting plain integers, but it is the property that lets
the same routine sort records by a secondary key later, so it is worth preserving for
free.

Attaching the leftover tail whole, rather than walking it node by node, matters: the
remaining side is already sorted, so one pointer assignment finishes it.

## Complexity

- **Time:** `O(n log n)` — `log n` levels of splitting, each level merging `n` nodes.
- **Space:** `O(log n)` for the recursion stack. This is the top-down formulation; a
  bottom-up merge sort reaches `O(1)` by iterating over run widths instead of recursing,
  at the cost of noticeably fiddlier splicing.

The tests include a 5,000-node list, which would overflow the stack under a naive
recursive scheme but is comfortable at `log n` depth.
