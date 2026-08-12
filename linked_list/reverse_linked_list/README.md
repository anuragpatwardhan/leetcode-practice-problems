# Reverse Linked List

**Number:** 206
**Difficulty:** Easy
**Pattern:** In-place pointer manipulation
**Problem:** https://leetcode.com/problems/reverse-linked-list/

## Problem

Reverse a singly linked list and return the new head.

## Approach

Walk the list once, flipping each `next` pointer to face backwards. Three pointers are
enough: the node being processed, the one before it, and a temporary hold on the one
after.

**Saving the next node first is the whole problem.** Overwriting `current.next` destroys
the only reference to the remainder of the list, so capturing it beforehand is what
makes the loop able to advance at all. Everything else follows mechanically: point
`current` back at `previous`, then shift both forward.

`previous` starts at `None`, which is what turns the original head into the new tail
without a special case. The loop exits when `current` reaches `None`, at which point
`previous` holds the last node visited — the original tail, and the new head. Returning
`current` there is the classic off-by-one; it is always `None`.

This is the building block for the harder list problems. [Reverse Nodes in
k-Group](../reverse_nodes_in_k_group/) (LC 25) runs this same loop on bounded slices,
seeding `previous` with the node *after* the group instead of `None` so each reversed
chunk reconnects as it goes.

The tests assert the returned list reuses the original node objects, since rebuilding
the list from values would pass a values-only check while ignoring the point of the
exercise. They also check that reversing twice restores the input.

## Complexity

- **Time:** `O(n)` — each node is visited once.
- **Space:** `O(1)` — three pointers, no recursion. A recursive version reads more
  neatly but costs `O(n)` stack frames.
