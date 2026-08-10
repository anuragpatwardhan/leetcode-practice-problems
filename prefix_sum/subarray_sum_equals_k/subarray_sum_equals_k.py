"""LeetCode 560. Subarray Sum Equals K."""

from typing import Dict, List


def subarray_sum(nums: List[int], k: int) -> int:
    """Return how many contiguous subarrays of ``nums`` sum to ``k``."""
    # Number of prefixes seen so far for each running total. The empty prefix
    # sums to 0, which is what lets a subarray starting at index 0 be counted.
    seen: Dict[int, int] = {0: 1}
    running = 0
    count = 0

    for value in nums:
        running += value
        # Any earlier prefix equal to running - k closes a subarray summing to k.
        count += seen.get(running - k, 0)
        seen[running] = seen.get(running, 0) + 1

    return count
