"""LeetCode 200. Number of Islands."""

from collections import deque
from typing import List


def num_islands(grid: List[List[str]]) -> int:
    """Count 4-directionally connected components of '1' in a character grid."""
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    # A separate visited set rather than overwriting '1' with '0' in place. The
    # in-place trick is the usual answer and it is genuinely cheaper, but it
    # hands back a grid of all-zeroes: a caller that counts islands and then
    # wants to draw the map has silently lost it.
    seen = [bytearray(cols) for _ in range(rows)]
    islands = 0

    for start_row in range(rows):
        for start_col in range(cols):
            if grid[start_row][start_col] != "1" or seen[start_row][start_col]:
                continue

            islands += 1
            # Iterative flood fill. The textbook version recurses per cell, so a
            # snaking island is one deep call chain — a 200x200 grid filled with
            # a single serpentine island is 40,000 frames and blows Python's
            # recursion limit long before it finishes.
            seen[start_row][start_col] = 1
            queue = deque([(start_row, start_col)])

            while queue:
                row, col = queue.popleft()
                for next_row, next_col in (
                    (row - 1, col),
                    (row + 1, col),
                    (row, col - 1),
                    (row, col + 1),
                ):
                    if not (0 <= next_row < rows and 0 <= next_col < cols):
                        continue
                    # Marking on the way in, not on the way out. Marking at
                    # dequeue time still counts correctly, but every cell gets
                    # enqueued once per neighbour that reaches it, so the queue
                    # grows to several times the island and the fill does four
                    # times the work.
                    if grid[next_row][next_col] == "1" and not seen[next_row][next_col]:
                        seen[next_row][next_col] = 1
                        queue.append((next_row, next_col))

    return islands
