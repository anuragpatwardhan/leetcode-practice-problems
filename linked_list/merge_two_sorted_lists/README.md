# Merge Two Sorted Lists

**Number:** 21
**Difficulty:** Easy
**Pattern:** Two-pointer splice with a dummy head
**Problem:** https://leetcode.com/problems/merge-two-sorted-lists/

## Problem

Splice two sorted linked lists into one sorted list, reusing the existing nodes.

## Approach

Walk both lists at once, always taking the smaller head. Because each list is already
sorted, whichever head is smaller is the smallest node remaining anywhere — so a single
pass suffices with no lookahead.

Two details carry the weight.

**The dummy head removes a branch.** Without it, the first node is a special case:
there is no tail to append to yet, so the loop needs an "is this the first one?" check on
every iteration. A throwaway node in front means every node is appended identically and
the answer is `dummy.next`.

**The leftover attaches whole.** When one list runs out the other is already sorted, so
one pointer assignment finishes the job. Walking it node by node would work and be
strictly slower for no benefit.

The comparison is `<=` rather than `<`, which makes the merge **stable** — on a tie the
node from the first list is emitted first. That changes no value in the output, so the
only way to observe it is by node identity, which is what the test does.

## Why this one is here

This is the `_merge` helper inside [Sort List](../sort_list/) (LC 148), lifted out and
tested on its own. Merge sort on a linked list is exactly this routine plus a split, and
having it verified independently is what makes the harder problem's correctness easy to
believe.

It is also the reason the list version of merge sort beats the array version on space:
merging arrays needs a scratch buffer, while merging lists is pure pointer relinking.

## Complexity

- **Time:** `O(n + m)` — every node is visited once.
- **Space:** `O(1)` — nodes are spliced, never copied. Only the dummy is allocated.
