"""LeetCode 153. Find Minimum in Rotated Sorted Array."""

from typing import List


def find_min(nums: List[int]) -> int:
    """Return the smallest value in a rotated sorted array of distinct values."""
    low, high = 0, len(nums) - 1

    while low < high:
        mid = (low + high) // 2
        # Compare against the right end, never the left. nums[mid] > nums[high]
        # can only happen when the rotation point lies to the right of mid, so
        # the minimum is in (mid, high]. Otherwise mid itself may be the minimum
        # and everything past it is larger, so the answer is in [low, mid].
        #
        # Comparing against nums[low] instead would be ambiguous: on an
        # unrotated array nums[mid] >= nums[low] holds while the minimum is
        # still to the left, which sends the search the wrong way.
        if nums[mid] > nums[high]:
            low = mid + 1
        else:
            high = mid

    return nums[low]
