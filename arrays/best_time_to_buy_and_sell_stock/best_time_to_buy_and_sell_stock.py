"""LeetCode 121. Best Time to Buy and Sell Stock."""

from typing import List


def max_profit(prices: List[int]) -> int:
    """Best profit from one buy and one later sell, or ``0`` if none is possible."""
    best = 0
    cheapest_so_far = float("inf")

    for price in prices:
        # Selling today is only ever best against the cheapest earlier day, so a
        # single running minimum replaces the inner loop of the brute force.
        # Updating it before measuring is safe: buying and selling on the same
        # day yields 0, which never beats an existing profit.
        cheapest_so_far = min(cheapest_so_far, price)
        best = max(best, price - cheapest_so_far)

    return best
