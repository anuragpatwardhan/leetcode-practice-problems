import random
from itertools import product

from largest_rectangle_in_histogram import largest_rectangle_area


def brute_force(heights):
    """Every start/end pair, tracking the limiting height."""
    best = 0
    for i in range(len(heights)):
        limit = heights[i]
        for j in range(i, len(heights)):
            limit = min(limit, heights[j])
            best = max(best, limit * (j - i + 1))
    return best


def test_example():
    assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10


def test_two_bars():
    assert largest_rectangle_area([2, 4]) == 4


def test_empty_histogram():
    assert largest_rectangle_area([]) == 0


def test_single_bar():
    assert largest_rectangle_area([7]) == 7


def test_uniform_bars_span_the_whole_width():
    assert largest_rectangle_area([3, 3, 3, 3]) == 12


def test_zero_height_bars_split_the_histogram():
    assert largest_rectangle_area([4, 0, 4]) == 4


def test_all_zero_heights():
    assert largest_rectangle_area([0, 0, 0]) == 0


def test_increasing_bars():
    # Best is the full width at the shortest height, or a suffix at a taller one.
    assert largest_rectangle_area([1, 2, 3, 4, 5]) == 9


def test_decreasing_bars():
    assert largest_rectangle_area([5, 4, 3, 2, 1]) == 9


def test_a_valley_between_two_towers():
    # The widest rectangle has to reach back across the popped taller bar.
    assert largest_rectangle_area([6, 1, 6]) == 6


def test_tall_bar_alone_beats_a_wide_short_one():
    assert largest_rectangle_area([1, 1, 100]) == 100


def test_matches_brute_force_on_every_short_small_valued_histogram():
    for length in range(1, 8):
        for heights in product(range(4), repeat=length):
            assert largest_rectangle_area(list(heights)) == brute_force(list(heights)), heights


def test_matches_brute_force_on_random_histograms():
    rng = random.Random(3)
    for _ in range(300):
        heights = [rng.randint(0, 50) for _ in range(rng.randint(1, 40))]
        assert largest_rectangle_area(heights) == brute_force(heights), heights
