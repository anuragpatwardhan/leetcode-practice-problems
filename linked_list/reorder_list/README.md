# Reorder List

**Number:** 143
**Difficulty:** Medium
**Pattern:** Fast/slow pointers, reversal, merge
**Problem:** https://leetcode.com/problems/reorder-list/

## Problem

Reorder a singly linked list from `L0 → L1 → … → Ln` into
`L0 → Ln → L1 → Ln-1 → …`, in place and without changing any values.

## Approach

The reorder wants the back half read backwards — but a singly linked list cannot be
walked backwards, and copying into an array is the obvious cheat the follow-up rules
out. Three standard passes get there in `O(1)` space, each one a smaller problem
already solved elsewhere in this repo:

1. **Find the middle** with fast/slow pointers.
2. **Reverse the second half** — exactly [Reverse Linked List](../reverse_linked_list/)
   (LC 206).
3. **Weave the two halves**, alternating one node from each.

Three details decide whether it works.

**Where the middle lands.** Advancing `fast` by two only while both `fast.next` and
`fast.next.next` exist leaves `slow` on the last node of the *first* half. On an
odd-length list the extra node stays on the left, which is what puts the middle element
last in the final weave — `[1,2,3]` becomes `[1,3,2]`. The other common loop condition
(`fast && fast.next`) overshoots and produces a longer second half, which breaks the
alternation.

**Cutting the list before reversing.** Setting `slow.next = None` matters. Without it,
the reversed second half still points back into the first, and the weave walks in a
circle rather than terminating. The test helper asserts no cycle exists precisely
because that failure produces an infinite loop rather than a wrong answer.

**Which half runs out first.** After the split, the reversed half is never longer than
the first, so exhausting it ends the loop and no length bookkeeping is needed.

Returning `None` is part of the contract — the reorder happens in place, and a test
asserts nothing is returned.

## Complexity

- **Time:** `O(n)` — three passes, each linear.
- **Space:** `O(1)` — pointers only; no array copy and no recursion.
