"""LeetCode 739. Daily Temperatures."""

from typing import List


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """For each day, how many days until a strictly warmer one, else ``0``."""
    answer = [0] * len(temperatures)
    # Indices of days still waiting for a warmer day. Their temperatures are
    # non-increasing from the bottom of the stack upward: a day can only still be
    # waiting if every day after it so far was no warmer.
    waiting: List[int] = []

    for day, temp in enumerate(temperatures):
        # Today resolves every pending day it beats. Each such day is popped once
        # and never reconsidered, which is what keeps the whole pass linear.
        while waiting and temperatures[waiting[-1]] < temp:
            earlier = waiting.pop()
            answer[earlier] = day - earlier
        waiting.append(day)

    # Anything left never found a warmer day, and those entries are already 0.
    return answer
