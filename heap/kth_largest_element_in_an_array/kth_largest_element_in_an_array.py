"""LeetCode 215. Kth Largest Element in an Array."""

import heapq
from typing import List


def find_kth_largest(nums: List[int], k: int) -> int:
    """Return the kth largest value, counting duplicates as separate ranks."""
    # A MIN-heap holding the k largest values seen so far. The inversion is the
    # whole trick: the smallest of the k best sits at the top, so it is the one
    # cheap to evict when something better arrives.
    largest: List[int] = []

    for value in nums:
        heapq.heappush(largest, value)
        # Once the heap is over size, the root is by definition the weakest
        # candidate and cannot be the answer.
        if len(largest) > k:
            heapq.heappop(largest)

    # What remains are the k largest values; their minimum is the kth largest.
    return largest[0]
