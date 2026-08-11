# Reverse Nodes in k-Group

**Number:** 25
**Difficulty:** Hard
**Pattern:** In-place linked list surgery with a dummy head
**Problem:** https://leetcode.com/problems/reverse-nodes-in-k-group/

## Problem

Reverse every consecutive group of `k` nodes in a singly linked list. A trailing group
of fewer than `k` nodes stays in its original order. Node values may not be changed —
only the links.

## Approach

Reversing a whole list is routine; the difficulty here is doing it in slices while
keeping the boundaries joined, and knowing when *not* to reverse.

**Check before reversing.** A group shorter than `k` must be left alone, and once nodes
have been relinked, undoing that costs another pass. So walk `k` nodes ahead first. If
the walk runs off the end, the remaining tail is already correct and the work is done.

**Reverse against the following node, not `None`.** The usual reversal seeds `prev`
with `None`, which would terminate the list at the end of each group. Seeding it with
`group_next` — the node just past the group — means the group's new tail is connected
to the rest of the list as part of the same sweep, with no repair step afterwards.

**Reconnect using the node that led the group.** After reversal, `group_prev.next` still
points at the node that used to be first and is now last. That node is exactly the
anchor the next group needs, so it is saved before `group_prev.next` is repointed at
`kth`, the group's new head. Getting these two assignments in the wrong order loses the
reference and corrupts the list.

**The dummy head removes the only special case.** The first group is the sole one whose
reversal changes which node the caller should hold. Placing a throwaway node in front
means every group has a real predecessor, so one code path handles all of them, and the
answer is `dummy.next`.

The result is one pass with constant extra space. A recursive version reads more
cleanly but costs `O(n/k)` stack frames.

The tests check every list length up to 12 against every `k` up to `length + 2`, and
separately assert that the returned list contains the original node objects, since
copying values into new nodes would satisfy the values-only checks while violating the
problem's constraint.

## Complexity

- **Time:** `O(n)` — every node is visited once to check the group's length and once to
  be reversed.
- **Space:** `O(1)` — a fixed number of pointers, no recursion.
