# Course Schedule II

**Number:** 210
**Difficulty:** Medium
**Pattern:** Topological sort (Kahn's algorithm)
**Problem:** https://leetcode.com/problems/course-schedule-ii/

## Problem

Given `numCourses` and a list of prerequisite pairs, return an order in which every course
can be taken, or an empty list if no such order exists.

## Approach

This is [Course Schedule](../course_schedule/) asking for the work rather than the verdict.
LeetCode 207 answers "is this graph acyclic?"; this one answers "and what is the order?" —
and Kahn's algorithm was already computing the order to decide the first question. The only
change is to keep it.

Count each course's outstanding prerequisites — its **indegree**. Everything at zero can be
taken now, so queue it. Taking a course releases what waits on it; decrement those, and any
reaching zero joins the queue. Append each course to the answer as it is taken.

The cycle check is still free. If the queue drains before every course has been taken,
whatever remains never reached indegree zero, which can only happen inside a cycle.

## Why this problem is stricter than 207

**A reversed graph gives a plausible wrong answer.** `prerequisites[i] = [a, b]` means *to
take `a`, first take `b`*, so the edge runs **b → a**. Getting this backwards is the classic
mistake, and in LeetCode 207 it is nearly invisible: reversing every edge preserves whether
a cycle exists, so the boolean is unchanged. Here the mistake survives just as quietly but
produces an order that is exactly backwards — still a permutation, still looks like a
schedule. Only an asymmetric chain distinguishes them, so the tests include one.

**A partial order must not be returned.** When a cycle blocks part of the graph, the courses
outside it still come out of the queue in a perfectly valid order. Returning that is the
dangerous failure: it looks like a schedule and silently omits the courses that deadlocked.
The length check at the end is what turns it into a refusal.

## The trap

**Empty means two different things, and only one of them is a refusal.**

`[]` is the failure signal, but it is also the correct answer for `numCourses = 0`. A guard
that short-circuits on an empty order earlier in the function returns the right value by
the wrong reasoning, and the distinction matters the moment anything is layered on top. The
length comparison handles both: with no courses, `0 == 0` and the empty order is returned
as a success.

The other subtlety carried over from 207: **duplicate prerequisites must be counted twice.**
Indegree has to fall to exactly zero, so a repeated edge must be released twice.
De-duplicating into a set would leave the course stuck and report a cycle that is not there.

## Verification

Two independent checks, because many orders are correct and comparing against one
particular answer would be wrong.

- **Validity** is checked by a validator, not a second sort: the result must be a
  permutation of `0..n-1`, and for every pair, the prerequisite must appear earlier.
- **Feasibility** is cross-checked against an iterative DFS three-colouring, derived from
  the definition of a cycle rather than from Kahn's algorithm, so it can genuinely disagree
  about whether an order should exist at all.

Run over 500 random graphs, plus 300 constructed acyclic by only ever pointing from a lower
index to a higher one, where an order must always exist.

## Complexity

- **Time:** `O(V + E)` — every course dequeued once, every edge relaxed once.
- **Space:** `O(V + E)` for the adjacency list, indegrees and queue.
