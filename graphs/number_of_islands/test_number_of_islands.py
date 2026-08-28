import random
import sys

from number_of_islands import num_islands


def reference(grid):
    """Independent check: union-find over adjacent land cells.

    Counting disjoint sets is a different formulation from flood fill — it never
    traverses a component at all — so agreement between the two is meaningful
    rather than the same idea written twice.
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                parent[(r, c)] = (r, c)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            for nr, nc in ((r + 1, c), (r, c + 1)):
                if nr < rows and nc < cols and grid[nr][nc] == "1":
                    union((r, c), (nr, nc))

    return len({find(cell) for cell in parent})


def make_grid(rows):
    """Build a grid from a list of strings, so the cases stay readable."""
    return [list(row) for row in rows]


def test_single_island():
    assert num_islands(make_grid(["11110", "11010", "11000", "00000"])) == 1


def test_several_islands():
    assert num_islands(make_grid(["11000", "11000", "00100", "00011"])) == 3


def test_all_water():
    assert num_islands(make_grid(["000", "000"])) == 0


def test_all_land_is_one_island():
    assert num_islands(make_grid(["111", "111", "111"])) == 1


def test_single_cell_island():
    assert num_islands(make_grid(["1"])) == 1


def test_single_cell_water():
    assert num_islands(make_grid(["0"])) == 0


def test_empty_grid():
    assert num_islands([]) == 0


def test_grid_of_empty_rows():
    # A row with no columns is not the same as no rows, and indexing grid[0][0]
    # to probe the width would raise on it.
    assert num_islands([[], []]) == 0


def test_every_cell_its_own_island():
    # A checkerboard: no two land cells touch orthogonally.
    grid = make_grid(["101", "010", "101"])
    assert num_islands(grid) == 5


def test_diagonals_do_not_connect():
    # The single most common wrong answer is including the four diagonals, which
    # would merge these two corners into one island.
    assert num_islands(make_grid(["10", "01"])) == 2


def test_land_touching_every_edge():
    # Guards the bounds check: each of the four directions must be rejected at
    # the border rather than wrapping to the opposite side.
    assert num_islands(make_grid(["111", "101", "111"])) == 1


def test_wrapping_would_merge_these():
    # Two islands hugging opposite edges of the same row. A missing bounds check
    # that wraps column -1 to the last column would fuse them.
    assert num_islands(make_grid(["1001", "0000", "1001"])) == 4


def test_single_row():
    assert num_islands(make_grid(["10101"])) == 3


def test_single_column():
    assert num_islands([["1"], ["0"], ["1"], ["1"]]) == 2


def test_u_shape_is_one_island():
    # Connected only by going around, so a fill that stops at the first dead end
    # would report two.
    assert num_islands(make_grid(["101", "101", "111"])) == 1


def test_does_not_modify_the_grid():
    # The in-place variant sinks each island as it counts it. That is a valid
    # solution to the puzzle and a bad function to hand someone.
    grid = make_grid(["110", "010", "001"])
    before = [row[:] for row in grid]
    num_islands(grid)
    assert grid == before


def test_counting_twice_gives_the_same_answer():
    # Follows from the above, and is what a caller would actually notice.
    grid = make_grid(["110", "010", "001"])
    assert num_islands(grid) == num_islands(grid)


def test_long_snake_does_not_hit_the_recursion_limit():
    # One serpentine island threading a 120x120 grid: about 7,200 cells in a
    # single chain. Recursive flood fill needs a frame per cell and dies here;
    # Python's default limit is 1,000.
    size = 120
    grid = [["0"] * size for _ in range(size)]
    for r in range(0, size, 2):
        for c in range(size):
            grid[r][c] = "1"
        # Join this row to the next filled one at alternating ends.
        if r + 2 < size:
            grid[r + 1][size - 1 if (r // 2) % 2 == 0 else 0] = "1"

    assert sys.getrecursionlimit() < size * size // 2
    assert num_islands(grid) == 1


def test_large_grid_of_separate_islands():
    # Every other cell in both directions, so 50x50 land cells none of which
    # touch. Exercises the outer scan finding many components.
    grid = [["0"] * 100 for _ in range(100)]
    for r in range(0, 100, 2):
        for c in range(0, 100, 2):
            grid[r][c] = "1"
    assert num_islands(grid) == 2500


def test_matches_union_find_on_random_grids():
    rng = random.Random(200)
    for _ in range(400):
        rows = rng.randint(1, 8)
        cols = rng.randint(1, 8)
        # Vary the density so the runs cover sparse, balanced and dense grids;
        # a fixed 50% would rarely produce a single large component.
        density = rng.choice((0.2, 0.5, 0.8))
        grid = [
            ["1" if rng.random() < density else "0" for _ in range(cols)]
            for _ in range(rows)
        ]
        expected = reference([row[:] for row in grid])
        assert num_islands(grid) == expected, grid


def test_matches_union_find_on_tall_and_wide_grids():
    # Random square-ish grids rarely produce a 1xN or Nx1 shape, where an
    # off-by-one in the bounds check is easiest to hide.
    rng = random.Random(201)
    for _ in range(200):
        if rng.random() < 0.5:
            rows, cols = rng.randint(1, 20), 1
        else:
            rows, cols = 1, rng.randint(1, 20)
        grid = [["1" if rng.random() < 0.5 else "0" for _ in range(cols)] for _ in range(rows)]
        assert num_islands(grid) == reference([row[:] for row in grid]), grid
