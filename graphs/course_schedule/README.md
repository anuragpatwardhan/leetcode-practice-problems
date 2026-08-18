# Course Schedule

**Number:** 207
**Difficulty:** Medium
**Pattern:** Topological sort (Kahn's algorithm)
**Problem:** https://leetcode.com/problems/course-schedule/

## Problem

Given `numCourses` and a list of prerequisite pairs, decide whether every course can be
taken.

## Approach

Strip the wording away and the question is: **does this directed graph contain a cycle?**
If course A ultimately requires B and B requires A, neither can ever be started. Anything
acyclic can be ordered.

Kahn's algorithm answers it while building the order rather than searching for the cycle
separately.

Count how many prerequisites each course still has outstanding — its **indegree**. Every
course at zero can be taken now, so queue them. Taking a course releases everything
waiting on it; decrement those, and any that reach zero joins the queue.

**The count is the cycle check.** If the queue drains before every course has been taken,
whatever remains never reached indegree zero — and that can only happen if it sits in a
cycle, since every course in one is waiting on another in the same cycle. No separate
detection pass is needed, which is the neat part of this formulation.

## The trap

`prerequisites[i] = [a, b]` means *to take `a`, first take `b`*. So the edge runs
**b → a**, not a → b.

Reversing it is the classic mistake, and it is nasty because the answer is often
unchanged: reversing every edge of a graph preserves whether a cycle exists. So a
mirrored input still passes, and it survives casual testing. It only fails once the
structure is asymmetric — which is why the tests include an explicitly one-directional
chain rather than only symmetric shapes.

A second subtlety: **duplicate edges must be counted twice.** Indegree has to fall to
exactly zero, so a repeated prerequisite has to be released twice. Deduplicating edges
into a set would be a different algorithm and would break on that input.

## Verification

The reference implementation is an iterative DFS three-colouring — a node currently on
the stack that gets revisited is a back edge, hence a cycle. That is derived straight
from the definition rather than from Kahn's algorithm, so agreement between the two is
meaningful rather than circular. Checked over 500 random graphs, plus 300 constructed to
be acyclic by only ever pointing from a lower index to a higher one.

## Complexity

- **Time:** `O(V + E)` — every course dequeued once, every edge relaxed once.
- **Space:** `O(V + E)` for the adjacency list, indegrees and queue.
