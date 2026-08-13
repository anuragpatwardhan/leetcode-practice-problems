# Validate Binary Search Tree

**Number:** 98
**Difficulty:** Medium
**Pattern:** Bounds propagation
**Problem:** https://leetcode.com/problems/validate-binary-search-tree/

## Problem

Decide whether a binary tree is a valid binary search tree: every value in a node's left
subtree is strictly smaller, every value in its right subtree strictly larger, and both
subtrees are themselves valid.

## Approach

The tempting check — each node sits between its own two children — is **wrong**, and
wrong in a way that passes the obvious examples. The BST property is about entire
subtrees, not parent/child pairs.

Consider `TreeNode(5, TreeNode(2, TreeNode(1), TreeNode(6)), TreeNode(8))`. The node `6`
is a perfectly legitimate right child of `2`. But it lives in `5`'s left subtree, where
every value must stay below `5` — and it does not. A parent-only check accepts this tree.

The fix is to carry down the **open interval** each subtree must fall inside. The root
starts unbounded. Descending left replaces the upper bound with the current node's
value; descending right replaces the lower bound. Crucially the bound **tightens and is
never reset**, so a constraint from far up the tree still applies many levels down — the
exact thing the naive version loses.

Comparisons are strict on both sides, since duplicates are not permitted here.

The traversal is **iterative**, pushing `(node, low, high)` onto an explicit stack. A
recursive version is shorter, but a BST built from sorted insertions degenerates into a
list, and Python's recursion limit would give up around a thousand levels. The tests
include a 5,000-node chain.

`float("-inf")` and `float("inf")` are safe sentinels precisely because no integer can
equal them — the tests check `±2**63` to confirm that extreme real values still pass.

## Verification

The tests check against an independent property: **a tree is a valid BST exactly when
its in-order traversal is strictly increasing.** That reference is derived a completely
different way, and it is compared on 500 random trees. A second test builds genuine BSTs
by repeated insertion and asserts every one validates, which catches the opposite failure
of a checker that is simply too strict.

## Complexity

- **Time:** `O(n)` — each node is visited once.
- **Space:** `O(h)` for the explicit stack, where `h` is the height: `O(log n)` balanced,
  `O(n)` for a degenerate chain.
