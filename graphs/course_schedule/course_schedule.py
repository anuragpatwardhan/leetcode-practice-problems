"""LeetCode 207. Course Schedule."""

from collections import deque
from typing import List


def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """True when every course can be taken, i.e. the prerequisite graph is acyclic."""
    # prerequisites[i] = [course, needed] means `needed` must come first, so the
    # edge points needed -> course. Reversing this is the classic mistake; the
    # answer is unchanged for symmetric inputs, which is why it survives casual
    # testing and fails on real ones.
    graph: List[List[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses

    for course, needed in prerequisites:
        graph[needed].append(course)
        indegree[course] += 1

    # Kahn's algorithm. Start with everything that has no outstanding
    # prerequisite; taking a course releases the ones waiting on it.
    ready = deque(course for course in range(num_courses) if indegree[course] == 0)
    taken = 0

    while ready:
        course = ready.popleft()
        taken += 1
        for dependent in graph[course]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)

    # Anything left never reached indegree zero, which can only happen if it sits
    # in a cycle — every course in one waits on another in the same cycle. So the
    # count doubles as cycle detection; no separate check is needed.
    return taken == num_courses
