# Clone Graph

**Number:** 133
**Difficulty:** Medium
**Pattern:** Graph traversal with a memo map (BFS)
**Problem:** https://leetcode.com/problems/clone-graph/

## Problem

Given a reference to a node in a connected undirected graph, return a deep copy of the
whole graph — same structure, no node shared with the original.

## Approach

Copying a tree is easy because you can never arrive back where you started. A graph has
cycles, so the naive copy follows `1 → 2 → 1 → 2` forever.

One map fixes it: **original node → its copy**. Before following any edge, ask whether that
neighbour has already been copied. If it has, reuse the copy; if it has not, make one now.
Traversal then visits each node once, and the recursion that would have run forever
terminates on the second sighting.

The map does two jobs at once, and it is worth separating them:

1. **It is the visited set**, which is what stops the cycle.
2. **It is the identity map**, which is what makes the copy correct. Two nodes that both
   point at node 4 must end up pointing at the *same* copy of 4. Cloning 4 twice gives a
   graph with the right values and the wrong shape — the diamond quietly becomes a tree.

The traversal is BFS with an explicit queue rather than recursion, because depth here is
the length of the graph and a 10,000-node chain is a legal input that would exhaust the
stack. Same rule the tree problems in this repo follow.

## The trap

**Put the copy in the map at the moment the node is discovered, not when it is processed.**

If discovery only enqueues, and the copy is created when the node is dequeued, then a node
sitting in the queue is not yet in the map. Another edge reaching it finds nothing there
and makes a second copy. Both copies are populated, both look right in isolation, and the
result is a graph that has silently split in two.

**And key the map by node identity, not by `val`.** LeetCode guarantees unique values, so
a `val`-keyed map passes every official test case. It is still the wrong key: nothing in
the *problem* says values are unique, and two distinct nodes sharing a value would be
merged into one. The Python default — hashing objects by identity — is exactly what is
wanted here, which is why `Node` deliberately defines no `__eq__` or `__hash__`.

## Verification

There is no independent reference implementation here, because a second traversal would be
the same algorithm again. Instead the tests check the two properties that define a correct
answer, which are easier to state than to compute:

- **The structure matches.** Each graph is fingerprinted by numbering its nodes in BFS
  discovery order and recording each node's neighbours as indices. That compares shape
  without comparing object identity, and it keeps neighbour order, which is observable.
- **Nothing is shared.** Every node object reachable from the copy is checked against the
  set of node objects reachable from the original. A shallow copy satisfies the structural
  check perfectly and fails this one immediately.

Checked over 300 random graphs, each built as a spanning tree with extra edges layered on
so it is connected and genuinely cyclic, plus a complete graph on 40 nodes where the map
hits far more often than it misses.

## Complexity

- **Time:** `O(V + E)` — each node dequeued once, each edge walked once from each end.
- **Space:** `O(V)` for the map and the queue, plus the `O(V + E)` of the returned graph.
