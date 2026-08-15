# Kth Largest Element in an Array

**Number:** 215
**Difficulty:** Medium
**Pattern:** Bounded min-heap
**Problem:** https://leetcode.com/problems/kth-largest-element-in-an-array/

## Problem

Return the kth largest element, where duplicates occupy separate ranks — in
`[9, 9, 5, 1]` the 1st and 2nd largest are both `9`, and the 3rd is `5`.

## Approach

Sorting and indexing is one line and `O(n log n)`. It is a perfectly good answer, and
it is what the tests check against. But it does more work than the question asks: the
order of the other `n - k` elements is irrelevant.

Keep a **min-heap holding only the k largest values seen so far**.

The inversion is the entire idea and reads backwards at first. To track the *largest*
values you keep a *min*-heap, because the useful operation is eviction: when the heap
grows past `k`, its root is by definition the weakest of the candidates, so it is the
one that can no longer be the answer. A max-heap would put the strongest candidate at
the top, which is precisely the element you never want to remove.

Push every value; whenever the size exceeds `k`, pop. What survives is the k largest
values, and their minimum — the root — is the kth largest.

That gives `O(n log k)` time and `O(k)` space. When `k` is small against `n` this is a
real win, and the space bound matters more than the time: it means the array never has
to be held in memory at all, so the same loop works over a stream.

**Duplicates need no special handling.** They are pushed like any other value and
occupy their own slots, which is what makes ranks work the way the problem specifies.
Deduplicating first would return `5` for `k=2` on `[9, 9, 5, 1]` instead of `9`, and the
tests pin that case.

The input list is never modified, unlike an in-place sort or a quickselect partition.

## Alternatives

**Quickselect** reaches `O(n)` average time by partitioning around a pivot and recursing
into only the side that can contain the answer. It is the better answer when `k` is
close to `n`, but it degrades to `O(n^2)` on adversarial input without randomised pivots,
and it reorders the caller's array. The heap is more predictable for the cost of a log
factor.

## Complexity

- **Time:** `O(n log k)` — one push and at most one pop per element.
- **Space:** `O(k)` for the heap.
