# Rotting Oranges

**Number:** 994
**Difficulty:** Medium
**Pattern:** Multi-source BFS on a grid
**Problem:** https://leetcode.com/problems/rotting-oranges/

## Problem

In a grid of empty cells, fresh oranges and rotten ones, rot spreads each minute to
orthogonally adjacent fresh oranges. Return the minutes until none are fresh, or `-1` if
some orange can never rot.

## Approach

The answer is the time the **last** orange rots, and each orange rots at its shortest
distance from *any* rotten one. So this is a shortest-path problem, and the answer is the
largest of those distances.

BFS computes shortest distances on an unweighted graph. The twist is that there is not one
starting point but many, which is what makes this a different problem from
[Number of Islands](../number_of_islands/) rather than the same flood fill again.

**Every rotten orange goes into the queue before the first step**, all at distance zero.
BFS then expands them together, one shared frontier moving outward, and the first time it
reaches a cell is that cell's distance to the nearest source. Nothing about the algorithm
changes — a multi-source BFS is just a BFS whose queue starts with more than one entry.

This works because BFS's correctness rests on the queue holding distances in non-decreasing
order. Seeding it with several zeroes preserves that.

## The trap

**Do not run one BFS per rotten orange.**

Two wrong versions look reasonable. Taking the minimum over a separate BFS from each source
gives the right answer, slowly — `O(sources × cells)` where the multi-source version is
`O(cells)`. Worse is running them one after another over a shared grid, which makes the
second source start from the first one's finishing time and so *adds* the durations
instead of overlapping them. A row with rot at both ends catches it: the answer halves when
the clocks run together.

Two smaller traps:

- **Zero and `-1` both describe grids with no work to do, and they are not the same.** A
  grid with no fresh oranges takes zero minutes, whether it is full of rotten ones or
  entirely empty. A grid with a fresh orange and no rotten one is `-1`. The distinction is
  the count of fresh oranges, not whether the queue was empty.
- **Mark cells on the way into the queue**, so an orange reached by two neighbours in the
  same minute is counted once. Decrementing the fresh count at dequeue time makes it drop
  below zero on those cells.

The grid is not modified, for the same reason as in Number of Islands: rotting it in place
is the shortest solution and hands the caller back a destroyed input.

## Verification

The reference implementation is a **literal round-by-round simulation** — sweep the whole
grid each minute, rot whatever touches something already rotten, count rounds until nothing
changes. That is the problem restated rather than a shortest-path computation, so agreement
with the BFS is meaningful. It costs a full pass per minute, which is fine for a test and
useless for a solution.

Checked over 400 random grids, weighted so rotten cells stay rare — an even split finishes
almost every grid in one or two minutes and tests nothing — plus 200 single-row and
single-column grids where a bounds off-by-one hides.

## Complexity

- **Time:** `O(rows × cols)` — each cell enqueued at most once, each with four neighbour
  checks.
- **Space:** `O(rows × cols)` for the visited grid and, in the worst case, the queue.
