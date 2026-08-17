# Kth Smallest Element in a BST

**Number:** 230
**Difficulty:** Medium
**Pattern:** In-order traversal with early exit
**Problem:** https://leetcode.com/problems/kth-smallest-element-in-a-bst/

## Problem

Return the kth smallest value (1-indexed) in a binary search tree.

## Approach

The BST invariant already encodes the answer: **an in-order walk of a BST emits values
in ascending order.** So the kth value it produces is the kth smallest — no sorting, and
no need to gather the values first.

Descend as far left as possible, pushing each node onto a stack. The deepest left node
is the smallest value not yet visited. Pop it, count it, then move to its right subtree
and repeat.

**The early exit is the point.** Returning the moment the counter reaches zero means the
right subtree and every remaining ancestor go untouched. Collecting the whole traversal
into a list and indexing gives the same answer but always costs `O(n)`; stopping early
costs only what it takes to reach the kth node.

The traversal is **iterative**. This matters more here than on a balanced tree problem:
a BST built from sorted inserts degenerates into a linked list, so its height is `O(n)`,
and a recursive in-order walk would exceed Python's recursion limit around a thousand
nodes. The tests build a 5,000-node chain specifically to cover that.

`k` beyond the tree's size raises rather than returning a silent wrong answer — the loop
simply runs out of nodes, and there is no sensible value to return.

## Complexity

- **Time:** `O(h + k)` — `h` to reach the leftmost node, then `k` pops. That is
  `O(log n + k)` on a balanced tree and `O(n)` worst case on a degenerate one.
- **Space:** `O(h)` for the stack.

If the tree were modified often and this query were hot, the standard follow-up is to
store a subtree-size count on each node, which turns the lookup into `O(h)` by letting
you skip whole subtrees rather than counting through them.
