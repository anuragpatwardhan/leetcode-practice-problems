# Serialize and Deserialize Binary Tree

**Number:** 297
**Difficulty:** Hard
**Pattern:** Breadth-first encoding with explicit null markers
**Problem:** https://leetcode.com/problems/serialize-and-deserialize-binary-tree/

## Problem

Design an encoding from a binary tree to a string and back, with no constraint on the
format beyond round-tripping correctly.

## Approach

The common solution is a recursive preorder walk that emits a marker for every missing
child. That is exactly `binary_tree_level_order_traversal` and `lowest_common_ancestor`'s
concern again: recursion depth tracks the tree's height, and a skewed tree can push that
past Python's limit. This solution reuses the same breadth-first shape as the level-order
traversal instead.

`serialize` runs a level-order walk with an explicit queue, same as `level_order`, except
every child gets enqueued — including `None` ones — and a `None` popped off the queue
just emits the marker `"#"` rather than being skipped. That last part matters: skipping
`None` children (as `level_order` does, since it only needs values) would throw away
*where* the gaps are, and a node with only a right child would be indistinguishable from
one with only a left child once decoded.

`deserialize` reverses this with the same queue discipline it was written with: read the
root, then for each dequeued node consume exactly two tokens for its left and right
child, enqueuing whichever ones are not the null marker. Because every level was written
in strict left-to-right, breadth-first order, reading it back in that same order
reconstructs the parent-child relationships without needing to search for anything.

## Complexity

- **Time:** `O(n)` for both directions — each node is enqueued and dequeued once, and
  each token is produced or consumed once.
- **Space:** `O(n)` for the queue and the token list, dominated by the widest level of
  the tree.
