# Linked List Cycle

**Number:** 141
**Difficulty:** Easy
**Pattern:** Floyd's tortoise and hare
**Problem:** https://leetcode.com/problems/linked-list-cycle/

## Problem

Return whether following `next` from the head ever revisits a node instead of reaching
the end.

## Approach

The obvious solution is a set of visited nodes — correct, `O(n)` time, and `O(n)` space.
The tests use exactly that as an independent oracle. Floyd's algorithm gets the same
answer in `O(1)` space.

Two pointers start at the head. `slow` advances one node per step, `fast` two. If the
list ends, `fast` falls off it and there is no cycle. If there is a cycle, both pointers
eventually enter it and **`fast` catches `slow` exactly**.

## Why they must actually meet

The part worth understanding is why `fast` cannot simply leap over `slow` forever.

Each step, `fast` gains exactly one node on `slow` — it moves two, `slow` moves one, so
the gap grows by one. Once both are inside a cycle of length `L`, that gap is measured
around the loop, so it is taken modulo `L`. A quantity that increases by one each step
and wraps at `L` must pass through every residue, including **zero**. Gap zero is the two
pointers on the same node.

That is also why the step sizes matter. With `fast` moving *three*, the gap grows by two
per step, and modulo an even `L` it would only ever hit even residues — it could skip
zero entirely and loop forever. One and two is the pair that guarantees a meeting.

**The loop guard is `fast` and `fast.next`.** `fast` is the pointer that runs off the
end, and it dereferences twice per step, so both must be non-null before advancing.
Checking only `fast` raises on the last node of an odd-length list.

Identity comparison (`slow is fast`) rather than value comparison is essential — a list
of fifty identical values is still finite. There's a test for exactly that.

## Why this one is here

Fast/slow pointers are already load-bearing in this repo. [Reorder List](../reorder_list/)
(LC 143) and [Sort List](../sort_list/) (LC 148) both use the same two-speed walk to find
the middle of a list, and getting the loop condition wrong there changes where the split
lands rather than crashing.

There's also a direct connection to the test suites: every linked-list problem here has a
`to_list` helper that asserts no cycle exists in its result, because a bad relink produces
an infinite loop rather than a wrong answer. This problem is that safety check written out
as the algorithm.

## Complexity

- **Time:** `O(n)`. Before the cycle, `fast` covers the tail in `O(n)`; inside it, the gap
  closes in at most `L` more steps.
- **Space:** `O(1)` — two pointers, against `O(n)` for the visited-set version.
