"""LeetCode 994. Rotting Oranges."""

from collections import deque
from typing import List

EMPTY, FRESH, ROTTEN = 0, 1, 2


def oranges_rotting(grid: List[List[int]]) -> int:
    """Minutes until no fresh orange remains, or -1 if one can never be reached."""
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])

    # Every rotten orange starts the clock at the same instant, so all of them go
    # into the queue before the first step. Running a separate BFS per source and
    # taking the minimum would give the same answer far more slowly; running them
    # one after another would give a wrong one.
    queue = deque(
        (row, col, 0)
        for row in range(rows)
        for col in range(cols)
        if grid[row][col] == ROTTEN
    )
    fresh = sum(row.count(FRESH) for row in grid)

    # No fresh oranges means zero minutes, whether or not anything is rotten.
    if fresh == 0:
        return 0

    rotted = [bytearray(cols) for _ in range(rows)]
    for row, col, _ in queue:
        rotted[row][col] = 1

    minutes = 0
    while queue:
        row, col, elapsed = queue.popleft()
        minutes = elapsed
        for next_row, next_col in (
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ):
            if not (0 <= next_row < rows and 0 <= next_col < cols):
                continue
            if grid[next_row][next_col] != FRESH or rotted[next_row][next_col]:
                continue
            # Marked on the way in, so a cell reached by two neighbours in the
            # same minute is only counted, and only enqueued, once.
            rotted[next_row][next_col] = 1
            fresh -= 1
            queue.append((next_row, next_col, elapsed + 1))

    # Anything still fresh was unreachable — walled off by empty cells, or in a
    # grid with no rotten orange at all.
    return minutes if fresh == 0 else -1
