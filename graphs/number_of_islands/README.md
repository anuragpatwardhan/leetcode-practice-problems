# Number of Islands

**Number:** 200
**Difficulty:** Medium
**Pattern:** Grid traversal / connected components (BFS flood fill)
**Problem:** https://leetcode.com/problems/number-of-islands/

## Problem

Given a grid of `'1'` (land) and `'0'` (water), count the islands. Land connects
horizontally and vertically, not diagonally.

## Approach

The grid is a graph in disguise. Each land cell is a vertex, each orthogonal pair of land
cells an edge, and an island is a **connected component**. Counting islands is counting
components, which is the same scan used on any graph: walk every vertex, and each time one
turns up unvisited, start a traversal from it and count one.

The only thing the grid changes is that adjacency is implicit — no adjacency list to
build, just four offsets and a bounds check.

Scan row by row. On an unvisited land cell, increment the count and flood fill outward
from it, marking everything reachable. The next unvisited land cell must therefore belong
to a different island, because if it were reachable the fill would already have claimed it.

## Two decisions that go the other way from the usual answer

**The grid is not modified.** The standard trick sinks each island as it counts it,
overwriting `'1'` with `'0'`, which makes the visited set free. It is genuinely cheaper.
But it hands the caller back a grid of all-zeroes — count the islands and then try to draw
the map and it is gone. The extra `O(rows × cols)` of visited bits buys a function that can
be called twice, and the tests assert both properties.

**The fill is iterative.** Recursive DFS is shorter, but its depth is the size of the
island, not the depth of anything balanced. A single serpentine island threading a 120×120
grid is a chain of about 7,200 cells; Python's default recursion limit is 1,000. This is
the same rule the tree problems here follow, and the test builds exactly that snake.

## The trap

**Mark cells visited when they go into the queue, not when they come out.**

Marking at dequeue time still produces the right count, which is what makes it hard to
notice. But a cell with three land neighbours gets pushed three times before any of them
is processed, so the queue holds several copies of most of the island and the fill does
roughly four times the work. On a dense grid that is the difference between linear and
something visibly worse.

The other classic error is including the four diagonals in the neighbour list. The problem
says orthogonal only, and a checkerboard tells the two apart immediately: five islands the
right way, one the wrong way.

## Verification

The reference implementation is **union-find** over adjacent land cells, counting distinct
roots at the end. It never traverses a component — it merges pairs and counts sets — so it
is a genuinely different formulation rather than the same flood fill written twice.

Checked over 400 random grids at three densities, since a fixed 50% rarely produces a
single large component, plus 200 more constrained to a single row or single column, where
an off-by-one in the bounds check is easiest to hide.

## Complexity

- **Time:** `O(rows × cols)` — every cell is examined by the outer scan once and enqueued
  at most once.
- **Space:** `O(rows × cols)` for the visited grid, and the same in the worst case for the
  queue, which on an all-land grid holds a full diagonal frontier.
