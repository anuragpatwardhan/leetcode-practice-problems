"""LeetCode 15. 3Sum."""

from typing import List


def three_sum(nums: List[int]) -> List[List[int]]:
    """Return every unique triplet in ``nums`` that sums to zero.

    Triplets are returned with their values in ascending order. The result contains
    no duplicate triplets, regardless of duplicates in the input.
    """
    nums = sorted(nums)
    n = len(nums)
    triplets: List[List[int]] = []

    for i in range(n - 2):
        # All remaining values are positive, so no later triplet can reach zero.
        if nums[i] > 0:
            break
        # Skip repeated anchors, which would only produce duplicate triplets.
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        low, high = i + 1, n - 1
        while low < high:
            total = nums[i] + nums[low] + nums[high]

            if total < 0:
                low += 1
            elif total > 0:
                high -= 1
            else:
                triplets.append([nums[i], nums[low], nums[high]])
                low += 1
                high -= 1
                # Advance past duplicates of the pair we just recorded.
                while low < high and nums[low] == nums[low - 1]:
                    low += 1
                while low < high and nums[high] == nums[high + 1]:
                    high -= 1

    return triplets
