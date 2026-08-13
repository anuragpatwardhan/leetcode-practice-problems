# Binary Tree Level Order Traversal

**Number:** 102
**Difficulty:** Medium
**Pattern:** Breadth-first search
**Problem:** https://leetcode.com/problems/binary-tree-level-order-traversal/

## Problem

Return the node values level by level, top to bottom, each level read left to right.

## Approach

Depth-first traversal reaches every node but visits them in the wrong order — it dives
to a leaf before touching the sibling next door. Levels demand breadth-first: a queue
holding the current frontier, expanded one row at a time.

Plain BFS would yield a flat sequence. The output needs the rows kept apart, and the
trick is **capturing the queue's length before draining it**.

At the top of each iteration the queue holds exactly one level. Recording that width
first, then popping exactly that many nodes, processes one row precisely — even though
children are being appended to the same queue while the loop runs. Without the snapshot,
the loop would keep consuming into the next level and the rows would merge into one.

Children are enqueued left before right, which is what makes each row read left to
right; FIFO order preserves it down the whole tree.

Gaps need no placeholders. Skipping `None` children means a row contains only real
nodes, so a tree missing an inner node still produces a compact row rather than one
padded with holes.

The traversal is **iterative**, so depth costs nothing on the call stack — the tests
include a 5,000-level chain that a recursive version would not survive.

## Complexity

- **Time:** `O(n)` — every node is enqueued once and dequeued once.
- **Space:** `O(w)` where `w` is the widest level. For a balanced tree that is about
  `n/2` at the bottom row, so `O(n)` in the worst case; for a degenerate chain it is
  `O(1)`.
