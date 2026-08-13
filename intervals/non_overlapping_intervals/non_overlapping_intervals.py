"""LeetCode 435. Non-overlapping Intervals."""

from typing import List


def erase_overlap_intervals(intervals: List[List[int]]) -> int:
    """Fewest intervals to remove so that none of the rest overlap."""
    if not intervals:
        return 0

    # Sort by END, not start. Removing the fewest intervals is the same as
    # keeping the most, and when two intervals collide the one to keep is
    # whichever finishes first -- it leaves the most room for everything after.
    # Sorting by start instead would keep a long interval that swallows several
    # short ones, as in [[1,100],[2,3],[4,5]].
    #
    # Ties on the end break by earlier start. LeetCode guarantees start < end, so
    # this cannot matter there, but it does for zero-length intervals: [2,3] and
    # [3,3] merely touch and can both be kept, which only works if [2,3] is seen
    # first. Taking [3,3] first would reject [2,3] and over-count by one.
    ordered = sorted(intervals, key=lambda interval: (interval[1], interval[0]))

    kept_end = ordered[0][1]
    removals = 0

    for start, end in ordered[1:]:
        if start < kept_end:
            # Overlaps the interval already kept. Dropping this one is never
            # worse: the kept interval ends no later, so it rules out no more
            # of what follows.
            removals += 1
        else:
            kept_end = end

    return removals
