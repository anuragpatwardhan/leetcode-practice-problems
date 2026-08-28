import random

from rotting_oranges import oranges_rotting


def reference(grid):
    """Independent check: literal round-by-round simulation.

    Sweeps the whole grid each minute and rots what is adjacent to something
    already rotten, counting rounds until nothing changes. That is the problem
    restated rather than a shortest-path computation, so agreement with the
    multi-source BFS is meaningful. It is O(rows * cols) per round, which is why
    it is only fit for a test.
    """
    grid = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0]) if grid else 0
    minutes = 0
    while True:
        newly = [
            (r, c)
            for r in range(rows)
            for c in range(cols)
            if grid[r][c] == 1
            and any(
                0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 2
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
            )
        ]
        if not newly:
            break
        for r, c in newly:
            grid[r][c] = 2
        minutes += 1
    return -1 if any(1 in row for row in grid) else minutes


def test_example_all_rot():
    assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4


def test_example_one_is_unreachable():
    # The lone orange at the bottom left is cut off by empty cells.
    assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1


def test_no_fresh_oranges_takes_no_time():
    assert oranges_rotting([[0, 2]]) == 0


def test_completely_empty_grid_takes_no_time():
    # Nothing to rot, so zero minutes — not -1, which would mean impossible.
    assert oranges_rotting([[0, 0, 0]]) == 0


def test_all_already_rotten():
    assert oranges_rotting([[2, 2], [2, 2]]) == 0


def test_a_fresh_orange_with_no_rotten_anywhere():
    # The clock never starts, so it can never rot.
    assert oranges_rotting([[1, 1], [1, 1]]) == -1


def test_single_fresh_next_to_single_rotten():
    assert oranges_rotting([[2, 1]]) == 1


def test_empty_grid():
    assert oranges_rotting([]) == 0


def test_grid_of_empty_rows():
    assert oranges_rotting([[], []]) == 0


def test_diagonals_do_not_spread_rot():
    # Rot travels orthogonally only; a diagonal neighbour is unreachable.
    assert oranges_rotting([[2, 0], [0, 1]]) == -1


def test_straight_line_takes_one_minute_per_cell():
    assert oranges_rotting([[2, 1, 1, 1, 1]]) == 4


def test_two_sources_meet_in_the_middle():
    # Nine cells with rot starting at both ends. A single-source BFS would say 8;
    # starting both clocks together halves it.
    assert oranges_rotting([[2, 1, 1, 1, 1, 1, 1, 1, 2]]) == 4


def test_sources_are_not_run_one_after_another():
    # Both rotten oranges act in the same minute. Processing one source to
    # completion and then the next would add their times instead of overlapping
    # them, and this grid makes the difference large.
    grid = [[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]]
    assert oranges_rotting(grid) == 5


def test_rot_spreads_around_a_wall():
    # A wall of empty cells splits the grid, so the far corner is reached the
    # long way round: down the left edge, across the bottom, back up the right.
    # Six minutes, against a straight-line distance of two.
    grid = [
        [2, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    assert oranges_rotting(grid) == 6


def test_does_not_modify_the_grid():
    # Rotting the caller's grid in place is the shortest solution and destroys
    # the input, exactly as with the flood fill in LeetCode 200.
    grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    before = [row[:] for row in grid]
    oranges_rotting(grid)
    assert grid == before


def test_counting_twice_gives_the_same_answer():
    grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    assert oranges_rotting(grid) == oranges_rotting(grid)


def test_large_grid_of_all_fresh_with_one_source():
    # A 60x60 grid rotting from one corner: the far corner is 118 steps away by
    # the Manhattan path, and every cell is reachable.
    size = 60
    grid = [[1] * size for _ in range(size)]
    grid[0][0] = 2
    assert oranges_rotting(grid) == (size - 1) * 2


def test_matches_simulation_on_random_grids():
    rng = random.Random(994)
    for _ in range(400):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        # Weighted so rotten cells stay rare; an even split would make almost
        # every grid finish in one or two minutes.
        grid = [
            [rng.choices((0, 1, 2), weights=(2, 5, 1))[0] for _ in range(cols)]
            for _ in range(rows)
        ]
        assert oranges_rotting(grid) == reference(grid), grid


def test_matches_simulation_on_narrow_grids():
    # Single rows and columns, where an off-by-one in the bounds check hides.
    rng = random.Random(995)
    for _ in range(200):
        length = rng.randint(1, 15)
        line = [rng.choices((0, 1, 2), weights=(2, 5, 1))[0] for _ in range(length)]
        for grid in ([line], [[cell] for cell in line]):
            assert oranges_rotting(grid) == reference(grid), grid
