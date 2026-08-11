"""LeetCode 84. Largest Rectangle in Histogram."""

from typing import List, Tuple


def largest_rectangle_area(heights: List[int]) -> int:
    """Area of the largest rectangle fitting under a histogram of unit-width bars."""
    best = 0
    # (start_index, height) for bars that can still grow to the right. Heights are
    # strictly increasing from the bottom of the stack upward.
    stack: List[Tuple[int, int]] = []

    for index, height in enumerate(heights):
        # This bar caps every taller pending bar, so each one's rectangle ends here.
        start = index
        while stack and stack[-1][1] > height:
            popped_start, popped_height = stack.pop()
            best = max(best, popped_height * (index - popped_start))
            # The current bar can extend back to where the taller bar began: every
            # bar in between was at least that tall, so it is at least this tall.
            start = popped_start
        stack.append((start, height))

    # Whatever survives was never capped on the right, so it runs to the end.
    for start, height in stack:
        best = max(best, height * (len(heights) - start))

    return best
