"""LeetCode 210. Course Schedule II."""

from collections import deque
from typing import List


def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    """An order in which every course can be taken, or [] if no such order exists."""
    # prerequisites[i] = [course, needed] means `needed` comes first, so the edge
    # points needed -> course. Reversing it still detects cycles correctly, which
    # is why LeetCode 207 survives the mistake — but here the *order* is the
    # answer, and a reversed graph produces a perfectly plausible reversed one.
    graph: List[List[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses

    for course, needed in prerequisites:
        graph[needed].append(course)
        indegree[course] += 1

    ready = deque(course for course in range(num_courses) if indegree[course] == 0)
    order: List[int] = []

    while ready:
        course = ready.popleft()
        order.append(course)
        for dependent in graph[course]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)

    # A short order means something never reached indegree zero, which can only
    # happen inside a cycle. Returning the partial order would be worse than
    # returning nothing: it looks like a schedule and silently omits courses.
    return order if len(order) == num_courses else []
