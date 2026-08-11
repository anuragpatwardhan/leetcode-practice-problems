"""LeetCode 4. Median of Two Sorted Arrays."""

from typing import List

INF = float("inf")


def find_median_sorted_arrays(nums1: List[int], nums2: List[int]) -> float:
    """Median of two sorted arrays in ``O(log min(m, n))``."""
    # Always binary search the shorter array: the search range is its length, and
    # it also guarantees the partner index stays inside the longer array.
    a, b = (nums1, nums2) if len(nums1) <= len(nums2) else (nums2, nums1)
    m, n = len(a), len(b)

    if m == 0 and n == 0:
        raise ValueError("median of two empty arrays is undefined")

    total = m + n
    # Size of the combined left half. The +1 puts the extra element on the left
    # when the total is odd, so the median is then the largest value on the left.
    half = (total + 1) // 2

    low, high = 0, m

    while low <= high:
        i = (low + high) // 2  # take i values from a
        j = half - i           # the rest must come from b

        # Sentinels stand in past either edge, so an empty side never needs a
        # special case: -inf never blocks a partition, +inf never gets chosen.
        a_left = a[i - 1] if i > 0 else -INF
        a_right = a[i] if i < m else INF
        b_left = b[j - 1] if j > 0 else -INF
        b_right = b[j] if j < n else INF

        if a_left <= b_right and b_left <= a_right:
            # Correct split: everything left of the cut is <= everything right.
            if total % 2:
                return float(max(a_left, b_left))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2

        if a_left > b_right:
            high = i - 1  # took too many from a
        else:
            low = i + 1   # took too few from a

    raise ValueError("inputs are not sorted ascending")
