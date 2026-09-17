"""LeetCode 973. K Closest Points to Origin."""

import heapq
from typing import List


def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """The k points nearest the origin, in no particular order."""
    if k <= 0:
        return []
    if k >= len(points):
        # Everything qualifies. Returning a copy rather than the caller's list
        # so the result cannot be a handle on their data.
        return [point[:] for point in points]

    # A bounded max-heap of the best k seen so far: the worst of them sits on
    # top, so each new point is one comparison away from being rejected.
    # heapq is a min-heap, so distances go in negated to invert the ordering.
    heap: List[tuple] = []

    for x, y in points:
        # Squared distance throughout: sqrt is monotonic, so it cannot change
        # which points are closer, and skipping it keeps the comparison in
        # exact integers. Within this problem's bounds sqrt would not actually
        # give a wrong answer — the gap between adjacent distances stays far
        # wider than float spacing — so this is about doing n fewer transcendental
        # operations and keeping the ordering exact by construction.
        distance = x * x + y * y

        if len(heap) < k:
            heapq.heappush(heap, (-distance, x, y))
        elif -heap[0][0] > distance:
            # Strictly greater: on a tie the incumbent stays. Either choice is
            # a correct answer, and not swapping avoids pointless heap churn on
            # inputs where many points share a distance.
            heapq.heapreplace(heap, (-distance, x, y))

    return [[x, y] for _, x, y in heap]
