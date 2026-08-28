"""LeetCode 79. Word Search."""

from typing import List


def exist(board: List[List[str]], word: str) -> bool:
    """True when `word` can be spelled by walking orthogonally without reusing a cell."""
    if not word:
        return True
    if not board or not board[0]:
        return False

    rows, cols = len(board), len(board[0])
    if rows * cols < len(word):
        return False

    # A word needing more of some letter than the board holds can be rejected
    # before any searching. Cheap, and it turns the pathological "board of all
    # A's, word of all A's plus a B" case from exponential into a single pass.
    needed: dict = {}
    for letter in word:
        needed[letter] = needed.get(letter, 0) + 1
    available: dict = {}
    for row in board:
        for letter in row:
            available[letter] = available.get(letter, 0) + 1
    if any(available.get(letter, 0) < count for letter, count in needed.items()):
        return False

    # Searching from the rarer end. The number of starting cells is the branching
    # factor of the whole search, so if the last letter occurs less often than
    # the first, spelling the word backwards explores far fewer paths.
    if available.get(word[-1], 0) < available.get(word[0], 0):
        word = word[::-1]

    # Explicit stack rather than recursion. Depth is the length of the word, and
    # while LeetCode caps that at 15, nothing in the algorithm does — the repo's
    # rule is that anything whose depth tracks input size goes iterative.
    #
    # Each frame carries the cell it is standing on and an iterator over the four
    # directions, so resuming a frame continues where it left off instead of
    # restarting the neighbour scan.
    for start_row in range(rows):
        for start_col in range(cols):
            if board[start_row][start_col] != word[0]:
                continue

            on_path = {(start_row, start_col)}
            stack = [(start_row, start_col, iter(_neighbors(start_row, start_col)))]

            while stack:
                row, col, directions = stack[-1]
                depth = len(stack)

                if depth == len(word):
                    return True

                advanced = False
                for next_row, next_col in directions:
                    if not (0 <= next_row < rows and 0 <= next_col < cols):
                        continue
                    if (next_row, next_col) in on_path:
                        continue
                    if board[next_row][next_col] != word[depth]:
                        continue
                    on_path.add((next_row, next_col))
                    stack.append((next_row, next_col, iter(_neighbors(next_row, next_col))))
                    advanced = True
                    break

                if not advanced:
                    # The undo. Without it the cell stays marked for every other
                    # path, and a word that has to cross its own earlier route
                    # is wrongly rejected.
                    on_path.discard((row, col))
                    stack.pop()

    return False


def _neighbors(row: int, col: int):
    """The four orthogonal neighbours, unbounded — the caller checks the edges."""
    return ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
