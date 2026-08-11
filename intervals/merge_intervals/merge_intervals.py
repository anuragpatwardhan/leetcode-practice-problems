"""LeetCode 56. Merge Intervals."""

from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    """Collapse overlapping intervals into the smallest covering set."""
    if not intervals:
        return []

    # Sorting by start is what makes a single pass sufficient: once the intervals
    # arrive in start order, anything that overlaps the group being built must
    # overlap it at its right edge, so only the last kept interval matters.
    ordered = sorted(intervals, key=lambda interval: interval[0])

    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        current = merged[-1]
        if start <= current[1]:
            # Touching counts as overlapping: [1,4] and [4,5] become [1,5].
            # max is required because the previous interval may already extend
            # past this one, as with [1,10] followed by [2,3].
            current[1] = max(current[1], end)
        else:
            merged.append([start, end])

    return merged
