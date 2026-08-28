# Redundant Connection

**Number:** 684
**Difficulty:** Medium
**Pattern:** Union-find (disjoint set union)
**Problem:** https://leetcode.com/problems/redundant-connection/

## Problem

A tree had one extra edge added to it. Given the resulting edge list, return the edge that
can be removed to leave a tree. If several qualify, return the one appearing last in the
input.

## Approach

A tree is a connected graph with no cycles, and adding one edge to it creates exactly one
cycle. So the question is: **which edge closes the cycle?**

Union-find answers it while building the graph, without ever traversing it. Start with
every node in its own set and process edges in order. Each edge asks whether its two
endpoints are already in the same set:

- **Different sets** — this edge is joining two pieces that were separate. It is part of
  the tree. Merge them.
- **Same set** — there was already a path between these two nodes, so this edge closes a
  cycle. This is the answer.

That is the whole algorithm. No adjacency list, no traversal, no visited set.

This is the first problem here where union-find is the *solution* rather than a test
reference — it appears in [Number of Islands](../number_of_islands/) only as the
independent check.

## Why "last in input order" is free

The tie-break looks like it needs handling and does not. Any earlier edge of the cycle was
still joining two separate components at the moment it was processed, so it merged
successfully. Only the edge that completes the cycle can be the one that fails. Sorting or
comparing indices would be solving a problem that does not exist.

## The two optimisations are not optional here

**Union by size.** Attaching the smaller tree under the larger one keeps depth
logarithmic. Without it, unioning `1-2, 2-3, 3-4, …` in order builds a linked list, and
`find` degrades to a linear walk — turning the whole solution quadratic on exactly the
chain input the tests use.

**Path compression, written iteratively.** After finding a root, point every node on the
path straight at it. The recursive version is three lines shorter, but its depth is the
height of the tree — and the height is only small *because* of compression, so on the first
deep find it can still overrun the stack. The test unions a 50,000-node chain, which the
recursive form does not survive.

## The trap

**The answer must be returned as it appeared in the input.** `[2, 3]` and `[3, 2]` are the
same undirected edge, and it is tempting to normalise the pair while storing it. The
expected output is the original ordering, so the edge has to be carried through unchanged.

## Verification

The reference is a **BFS tree check** — remove a candidate edge, then confirm what is left
has `n - 1` edges and reaches every node from any starting point. That is the definition of
a tree spelled out, not a second union-find, so it cannot share a bug with the solution.

Two properties are checked over random trees-plus-one-edge: that removing the returned edge
really does leave a tree, and separately that the returned edge is the *last* edge in the
input for which that is true. The second is the part a single example would not pin down,
since several edges of the cycle are usually valid removals.

The union-find is tested directly as well, since it is the reusable piece.

## Complexity

- **Time:** `O(n α(n))` — effectively linear; `α` is the inverse Ackermann function, below
  5 for any input that fits in memory.
- **Space:** `O(n)` for the parent and size arrays.
