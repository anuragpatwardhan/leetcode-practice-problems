"""LeetCode 128. Longest Consecutive Sequence."""

from typing import List


def longest_consecutive(nums: List[int]) -> int:
    """Return the length of the longest run of consecutive integers in ``nums``.

    The values do not need to be adjacent in the list, and duplicates are ignored.
    """
    unique = set(nums)
    longest = 0

    for value in unique:
        # Only walk a run from its smallest member, so each run is scanned once.
        if value - 1 in unique:
            continue

        length = 1
        while value + length in unique:
            length += 1

        longest = max(longest, length)

    return longest
