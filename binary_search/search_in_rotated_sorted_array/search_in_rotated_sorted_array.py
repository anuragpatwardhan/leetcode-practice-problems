"""LeetCode 33. Search in Rotated Sorted Array."""

from typing import List


def search(nums: List[int], target: int) -> int:
    """Return the index of ``target`` in a rotated sorted array, or ``-1``.

    ``nums`` holds distinct values and was sorted ascending before being rotated
    at some unknown pivot.
    """
    low, high = 0, len(nums) - 1

    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid

        # A rotation leaves at least one side of mid still sorted. Only a sorted
        # side can be range-checked, so identify it first and then decide whether
        # the target falls inside it.
        if nums[low] <= nums[mid]:
            # Left side is sorted. The <= is required: when two elements remain,
            # mid == low, and a strict < would misread that side as unsorted.
            if nums[low] <= target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            # Right side is sorted.
            if nums[mid] < target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1

    return -1
