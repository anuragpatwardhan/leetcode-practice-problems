import random

from word_search import exist


def reference(board, word):
    """Independent check: enumerate every self-avoiding walk and read it off.

    Builds the paths themselves rather than pruning a search, which is the
    definition of the problem rather than a second copy of the algorithm. It is
    exponential, so it is only ever run on tiny boards.
    """
    rows, cols = len(board), len(board[0]) if board else 0
    if not word:
        return True

    def walk(row, col, index, path):
        if board[row][col] != word[index]:
            return False
        if index == len(word) - 1:
            return True
        path.add((row, col))
        for nr, nc in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in path:
                if walk(nr, nc, index + 1, path):
                    path.discard((row, col))
                    return True
        path.discard((row, col))
        return False

    return any(walk(r, c, 0, set()) for r in range(rows) for c in range(cols))


BOARD = [
    ["A", "B", "C", "E"],
    ["S", "F", "C", "S"],
    ["A", "D", "E", "E"],
]


def grid(rows):
    return [list(row) for row in rows]


def test_example_found():
    assert exist(BOARD, "ABCCED") is True


def test_example_short_word_found():
    assert exist(BOARD, "SEE") is True


def test_example_not_found():
    assert exist(BOARD, "ABCB") is False


def test_a_cell_cannot_be_reused():
    # "ABCB" fails only because the B would have to be visited twice. Without
    # the visited check this returns True, and it is the single most common bug.
    assert exist([["A", "B"]], "ABA") is False


def test_single_letter_present():
    assert exist([["A"]], "A") is True


def test_single_letter_absent():
    assert exist([["A"]], "B") is False


def test_word_longer_than_the_board():
    assert exist([["A", "B"]], "ABAB") is False


def test_empty_board():
    assert exist([], "A") is False


def test_board_of_empty_rows():
    assert exist([[], []], "A") is False


def test_diagonals_are_not_steps():
    # B sits diagonally from A, so there is no path.
    assert exist(grid(["AX", "XB"]), "AB") is False


def test_word_wrapping_around_a_corner():
    assert exist(grid(["ABC", "XXD", "GFE"]), "ABCDEFG") is True


def test_a_cell_abandoned_by_one_route_is_free_for_another():
    # This is the backtracking half of backtracking: the search commits to a
    # partial route, fails, and the cells it gave up have to become available to
    # the route that does work. Dropping the unmark on the way out of a frame —
    # keeping only the mark on the way in — makes this exact board return False.
    # It was found by comparing against the exhaustive walk, not by inspection,
    # which is a fair measure of how invisible the bug is.
    assert exist(grid(["BBBB", "ABAA"]), "BBBABA") is True


def test_second_start_succeeds_after_the_first_fails():
    # The A at (0,0) leads nowhere; the one at (1,0) spells the word. A visited
    # set left dirty by the failed attempt would block the second.
    assert exist(grid(["AX", "AB"]), "AB") is True


def test_all_identical_letters():
    assert exist([["A"] * 4 for _ in range(4)], "AAAAAAAA") is True


def test_all_identical_letters_with_one_missing():
    # The pathological case: every path is viable until the final letter, which
    # is nowhere on the board. The letter-count precheck ends it immediately.
    assert exist([["A"] * 8 for _ in range(8)], "A" * 20 + "B") is False


def test_word_needing_more_of_a_letter_than_exists():
    assert exist(grid(["AB", "CD"]), "AABB") is False


def test_snake_through_a_single_row():
    assert exist([list("ABCDEFGHIJ")], "ABCDEFGHIJ") is True


def test_single_column():
    assert exist([["A"], ["B"], ["C"]], "ABC") is True


def test_reversed_word_is_also_findable():
    # A path read backwards is still a path, so both directions must succeed.
    # The solution reverses the word internally when the last letter is rarer,
    # and this is what pins that transformation down.
    assert exist(BOARD, "ABCCED") is True
    assert exist(BOARD, "DECCBA") is True


def test_does_not_modify_the_board():
    # The classic in-place trick overwrites each visited cell with a sentinel and
    # restores it on the way out. It works, but a bug in the restore leaves the
    # caller's board corrupted, so this solution never writes to it.
    board = [row[:] for row in BOARD]
    exist(board, "ABCCED")
    assert board == BOARD


def test_searching_twice_gives_the_same_answer():
    board = [row[:] for row in BOARD]
    assert exist(board, "SEE") == exist(board, "SEE")


def test_matches_exhaustive_search_on_random_boards():
    rng = random.Random(79)
    for _ in range(300):
        rows, cols = rng.randint(1, 4), rng.randint(1, 4)
        # Two letters, so words collide often and both answers actually occur.
        board = [[rng.choice("AB") for _ in range(cols)] for _ in range(rows)]
        word = "".join(rng.choice("AB") for _ in range(rng.randint(1, 6)))
        assert exist(board, word) == reference(board, word), (board, word)


def test_matches_exhaustive_search_with_a_wider_alphabet():
    # Three letters makes matches rarer, exercising the rejection paths that the
    # two-letter boards mostly skip past.
    rng = random.Random(80)
    for _ in range(300):
        rows, cols = rng.randint(1, 4), rng.randint(1, 4)
        board = [[rng.choice("ABC") for _ in range(cols)] for _ in range(rows)]
        word = "".join(rng.choice("ABC") for _ in range(rng.randint(1, 5)))
        assert exist(board, word) == reference(board, word), (board, word)


def test_finds_words_that_are_actually_on_the_board():
    # Generated by walking a random path, so the answer is known to be True and
    # a solution that rejects everything cannot pass.
    rng = random.Random(81)
    for _ in range(200):
        rows, cols = rng.randint(2, 5), rng.randint(2, 5)
        board = [[rng.choice("ABCDE") for _ in range(cols)] for _ in range(rows)]

        row, col = rng.randrange(rows), rng.randrange(cols)
        path = [(row, col)]
        for _ in range(rng.randint(0, 6)):
            options = [
                (nr, nc)
                for nr, nc in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1))
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in path
            ]
            if not options:
                break
            row, col = rng.choice(options)
            path.append((row, col))

        word = "".join(board[r][c] for r, c in path)
        assert exist(board, word) is True, (board, word, path)
