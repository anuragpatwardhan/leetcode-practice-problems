# Lowest Common Ancestor of a Binary Tree

**Number:** 236
**Difficulty:** Medium
**Pattern:** Parent-pointer ancestor tracking
**Problem:** https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

## Problem

Given a binary tree and two of its nodes, return the deepest node that has both as
descendants (a node counts as its own descendant).

## Approach

The textbook solution is a recursive postorder search: a subtree "contains" a target if
either child does or the root itself is one, and the first node where both children
report a hit is the answer. That is elegant but recurses to the tree's depth, and
`validate_binary_search_tree` already established the house rule for this repo — a
degenerate, list-shaped input can be deeper than Python's recursion limit, so anything
touching arbitrary tree shapes goes iterative.

The iterative version trades the clever postorder check for a simpler two-pass idea:

1. Walk the tree once with an explicit stack, recording each node's parent in a dict as
   it is discovered. The walk stops the moment both targets have parents recorded —
   most calls find both long before reaching the last leaf, so this is rarely a full
   traversal.
2. Walk up from `p` via the parent pointers to the root, collecting every node on that
   path into a set. This is `p`'s full ancestor chain, root included.
3. Walk up from `q` the same way, stopping at the first node already in that set. That
   first shared node is the answer — it is the point where the two paths to the root
   merge.

Root is deliberately seeded into the parent map with a `None` parent before the walk
starts, so a call where `p` or `q` **is** the root is not a special case: the ancestor
walk from either one just terminates immediately.

## Complexity

- **Time:** `O(n)` — building parent pointers visits each node at most once, and each
  ancestor walk is at most the tree's height.
- **Space:** `O(n)` for the parent map and the stack, plus `O(h)` for the ancestor set,
  where `h` is the height — dominated by the `O(n)` parent map.
