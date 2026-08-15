# Construct Binary Tree from Preorder and Inorder Traversal

**Number:** 105
**Difficulty:** Medium
**Pattern:** Traversal reconstruction with an explicit stack
**Problem:** https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

## Problem

Given a tree's preorder and inorder traversals (no duplicate values), rebuild the tree.

## Approach

The textbook solution reads the root off the front of preorder, finds it in inorder to
split the remaining values into a left slice and a right slice, and recurses on each.
That is correct but expensive in two ways: it recurses to the tree's height, which
`lowest_common_ancestor` already flagged as unsafe on a skewed input, and each call
slices two arrays, turning O(n) nodes into O(n^2) work overall.

The iterative version processes preorder left to right with a stack, using inorder only
to know *when a subtree closes*, never to slice anything.

Preorder visits a node, then its whole left subtree, then its whole right subtree. So as
long as the next preorder value is still inside the current stack top's left subtree,
it becomes that node's left child and gets pushed. The stack at any point is exactly the
current root-to-node path.

The signal that a left subtree has finished is inorder catching up to the stack top: once
`inorder[inorder_index]` equals `stack[-1].val`, that node (and, if this keeps holding
after popping it, one or more of its ancestors) has had its entire left side visited and
is itself done. Popping while the tops keep matching finds the *lowest* ancestor whose
right side is still open — that is the true parent for the next preorder value, which
becomes its right child.

Each preorder value is pushed once and popped at most once, so the whole reconstruction
is O(n) rather than the recursive solution's O(n^2).

## Complexity

- **Time:** `O(n)` — every value is pushed once and popped at most once; the
  `inorder_index` walk across the whole method also advances at most `n` times.
- **Space:** `O(n)` for the stack, which in the worst case (a fully skewed tree) holds
  every node at once.
