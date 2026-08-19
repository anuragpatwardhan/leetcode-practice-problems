"""LeetCode 704. Binary Search."""

from typing import List


def search(nums: List[int], target: int) -> int:
    """Return the index of ``target`` in a sorted ascending array, or ``-1``."""
    low, high = 0, len(nums) - 1

    # Inclusive bounds on both ends, so `low == high` still holds one unchecked
    # candidate and the loop must run. Using `low < high` here would skip it and
    # miss any single-element search.
    while low <= high:
        # Equivalent to (low + high) // 2 for Python, whose ints never overflow,
        # but written the way it must be in a fixed-width language — where
        # low + high can exceed the type on a large array.
        mid = low + (high - low) // 2

        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            # mid is ruled out, so move past it. Assigning low = mid instead
            # would leave the range unchanged when high == low + 1 and spin
            # forever.
            low = mid + 1
        else:
            high = mid - 1

    return -1
