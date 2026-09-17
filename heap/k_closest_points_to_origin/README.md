# K Closest Points to Origin

**Number:** 973
**Difficulty:** Medium
**Pattern:** Bounded max-heap (top-k selection)
**Problem:** https://leetcode.com/problems/k-closest-points-to-origin/

## Problem

Given a list of points on a plane and an integer `k`, return the `k` points closest to the
origin. Any order, and any valid answer when distances tie.

## Approach

Sorting everything by distance and slicing works and is `O(n log n)`. But the question only
asks for `k` points, and `k` is usually far smaller than `n` — so most of that sorting is
spent ordering points that will be thrown away.

Keep a **max-heap of the best `k` seen so far**. The worst of the current best sits on top,
so each new point costs one comparison to reject. Only a point that beats the incumbent
worst causes any heap work at all. That is `O(n log k)`: for 200,000 points and `k = 5`, the
heap never holds more than five entries.

Python's `heapq` is a min-heap, so distances go in **negated** to invert the ordering. This
is the same structure as [Kth Largest Element](../kth_largest_element_in_an_array/), turned
around — that one keeps a min-heap of the largest `k`, this keeps a max-heap of the
smallest.

## Two decisions

**Squared distance throughout, never `sqrt`.** Square root is monotonic, so it cannot change
which point is closer, and skipping it keeps every comparison in exact integers.

Worth being precise about why: it is *not* that `sqrt` would give a wrong answer here. With
coordinates bounded by 10⁴, the smallest gap between two adjacent distances after `sqrt` is
about `3.5e-5`, while float spacing at that magnitude is about `1.8e-12` — seven orders of
magnitude of headroom, so no two distinct distances could ever collide. The reason is
simply that it is `n` transcendental operations bought nothing, and integers are exact by
construction rather than by an argument about bounds.

**Ties keep the incumbent.** The replace is gated on a strict `>`, so an equally distant
newcomer does not displace what is already there. Either answer is correct, and not swapping
avoids pointless heap churn on inputs where many points share a distance.

## The trap

**Getting the heap direction backwards keeps the `k` furthest points.** It produces exactly
`k` points from the input, in a plausible order, and on a small example where you eyeball the
output it can even look right. Two mutations of this were checked — inverting the comparison
and dropping the negation — and both are caught, because the tests compare distances rather
than counting results.

Smaller one: when `k` covers every point, the shortcut must not hand back the caller's own
row lists. Mutating the result would then reach into their data.

## Verification

The reference is a **full sort by distance**, which is the very thing the bounded heap exists
to avoid — a different formulation, so agreement is meaningful.

Because ties make the answer non-unique, the tests *validate the property* rather than
compare to one answer: the returned points must all come from the input, each consumed once,
and their multiset of distances must equal the `k` smallest distances. Run over 400 random
inputs, plus 400 more confined to coordinates in `[-2, 2]` so distances collide constantly,
plus a sweep of every `k` from 0 past the end of one fixed input.

## Complexity

- **Time:** `O(n log k)` — one comparison per point, and a `log k` heap operation only when
  it beats the incumbent worst.
- **Space:** `O(k)` for the heap, excluding the returned list.
