# Binary Tree Maximum Path Sum

**Number:** 124
**Difficulty:** Hard
**Pattern:** Post-order with a split/extend distinction
**Problem:** https://leetcode.com/problems/binary-tree-maximum-path-sum/

## Problem

Return the largest sum along any path. A path is any sequence of connected nodes, it
need not touch the root, and it must contain at least one node.

## Approach

The difficulty is that **two different quantities live at every node**, and conflating
them is the bug this problem is built to catch.

1. **The best path that turns here** — `node.val + left + right`. It comes up one
   subtree and back down the other. This is a candidate for the answer.
2. **The best path a parent can extend** — `node.val + max(left, right)`. A parent joins
   through this node, so the path must arrive and continue in a straight line, using at
   most one child.

Return the first from the recursion and the answer is wrong: a path would fork at two
different nodes and stop being a path at all. So the split value updates a running
maximum, and only the extend value is passed upward.

**Clamping at zero is the other half.** `max(gain, 0)` means a subtree that sums negative
is simply not taken — the path stops rather than paying to continue. That is also why a
missing child and a harmful child are worth the same: nothing.

The running maximum starts at negative infinity, not zero. Every path must contain at
least one node, so an all-negative tree has a negative answer — `[-3]` is `-3`, not `0`.
Seeding at zero silently breaks exactly that case, which is why the tests include a
random all-negative sweep.

The traversal is **post-order and iterative**: both children must be resolved before
their parent, and a degenerate tree is a chain, so recursion would exceed Python's limit
on the 5,000-node case the tests include. Gains are kept in a dict keyed by node, and
absent children read as `0` through the same clamp.

## Verification

The brute force enumerates, for every node, the best downward run on each side and
combines them. That works as an independent oracle because **a path turns at exactly one
node** — so iterating over all possible turning points covers every path. It is derived
from the definition rather than from the algorithm, which is what makes the agreement
meaningful. Checked over 400 random trees plus 300 all-negative ones.

## Complexity

- **Time:** `O(n)` — each node is pushed twice and resolved once.
- **Space:** `O(n)` for the explicit stack and the gain map; `O(h)` of that is the stack,
  which is `O(n)` for a chain.
