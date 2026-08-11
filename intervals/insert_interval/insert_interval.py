"""LeetCode 57. Insert Interval."""

from typing import List


def insert(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:
    """Insert an interval into a sorted, non-overlapping list, merging as needed.

    The input is already sorted and disjoint, so no sort is required and the whole
    job is one linear pass.
    """
    result: List[List[int]] = []
    start, end = new_interval
    index, count = 0, len(intervals)

    # Everything ending before the new interval begins is untouched. Strict `<`
    # keeps a merely touching interval for the merge phase, so [1,2] and [2,5]
    # combine rather than being emitted separately.
    while index < count and intervals[index][1] < start:
        result.append(list(intervals[index]))
        index += 1

    # Absorb every interval that overlaps or touches, widening in both directions.
    # The start needs a min because an absorbed interval may begin earlier than
    # the new one, as with [1,5] and an insert of [2,3].
    while index < count and intervals[index][0] <= end:
        start = min(start, intervals[index][0])
        end = max(end, intervals[index][1])
        index += 1
    result.append([start, end])

    # The remainder starts strictly after the merged interval, so it is unchanged.
    while index < count:
        result.append(list(intervals[index]))
        index += 1

    return result
