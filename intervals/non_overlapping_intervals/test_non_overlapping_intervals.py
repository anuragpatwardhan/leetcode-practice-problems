import random
from itertools import combinations

from non_overlapping_intervals import erase_overlap_intervals


def brute_force(intervals):
    """Smallest number of removals, found by trying every subset to keep."""

    def disjoint(chosen):
        # Sort by start *and* end. Start alone is not enough: [8,8] and [8,11]
        # are compatible, but comparing them in the other order reads as an
        # overlap and would understate how many can be kept.
        ordered = sorted(chosen, key=lambda pair: (pair[0], pair[1]))
        return all(a[1] <= b[0] for a, b in zip(ordered, ordered[1:]))

    total = len(intervals)
    for keep in range(total, -1, -1):
        if any(disjoint(subset) for subset in combinations(intervals, keep)):
            return total - keep
    return total


def test_example_one_overlap():
    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1


def test_example_duplicates():
    assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2


def test_example_already_disjoint():
    assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0


def test_empty_input():
    assert erase_overlap_intervals([]) == 0


def test_single_interval():
    assert erase_overlap_intervals([[1, 5]]) == 0


def test_touching_intervals_do_not_count_as_overlapping():
    # Unlike Merge Intervals, [1,2] and [2,3] coexist here.
    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4]]) == 0


def test_one_long_interval_beats_keeping_many_short_ones():
    # Sorting by start would keep [1,100] and drop both short intervals.
    assert erase_overlap_intervals([[1, 100], [2, 3], [4, 5]]) == 1


def test_fully_nested_intervals():
    assert erase_overlap_intervals([[1, 10], [2, 9], [3, 8]]) == 2


def test_unsorted_input():
    assert erase_overlap_intervals([[3, 4], [1, 3], [1, 2], [2, 3]]) == 1


def test_negative_bounds():
    assert erase_overlap_intervals([[-5, -2], [-3, 0], [1, 2]]) == 1


def test_degenerate_point_intervals_never_overlap():
    assert erase_overlap_intervals([[1, 1], [1, 1], [2, 2]]) == 0


def test_the_input_list_is_not_modified():
    intervals = [[1, 3], [2, 4], [3, 5]]
    snapshot = [list(pair) for pair in intervals]
    erase_overlap_intervals(intervals)
    assert intervals == snapshot


def test_matches_brute_force_on_small_random_inputs():
    rng = random.Random(53)
    for _ in range(200):
        intervals = []
        for _ in range(rng.randint(1, 7)):
            start = rng.randint(0, 8)
            intervals.append([start, start + rng.randint(0, 4)])
        assert erase_overlap_intervals(intervals) == brute_force(intervals), intervals


def test_matches_brute_force_on_heavily_overlapping_inputs():
    rng = random.Random(59)
    for _ in range(200):
        intervals = []
        for _ in range(rng.randint(1, 6)):
            start = rng.randint(0, 3)
            intervals.append([start, start + rng.randint(1, 5)])
        assert erase_overlap_intervals(intervals) == brute_force(intervals), intervals
