"""LeetCode 239. Sliding Window Maximum."""

from collections import deque
from typing import Deque, List


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """Return the maximum of every contiguous window of size ``k``."""
    if not nums or k <= 0:
        return []

    maxima: List[int] = []
    # Indices of candidates, held so their values strictly decrease from front to
    # back. The front is therefore always the maximum of the current window.
    candidates: Deque[int] = deque()

    for index, value in enumerate(nums):
        # Anything no larger than the incoming value can never be a maximum again:
        # the new element is at least as big and stays in the window longer. Pop
        # from the back, which is why this needs a deque rather than a stack.
        while candidates and nums[candidates[-1]] <= value:
            candidates.pop()
        candidates.append(index)

        # Drop the front once it falls out of the window. Only one index can
        # expire per step, since the window advances by one.
        if candidates[0] <= index - k:
            candidates.popleft()

        # Windows are only complete from the (k-1)th element onward.
        if index >= k - 1:
            maxima.append(nums[candidates[0]])

    return maxima
