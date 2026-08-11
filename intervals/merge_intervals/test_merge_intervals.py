import random

from merge_intervals import merge


def covered_points(intervals):
    """Every integer point covered, as a set. Order-independent ground truth."""
    points = set()
    for start, end in intervals:
        points.update(range(start, end + 1))
    return points


def test_example():
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]


def test_touching_intervals_merge():
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]


def test_empty_input():
    assert merge([]) == []


def test_single_interval():
    assert merge([[1, 4]]) == [[1, 4]]


def test_disjoint_intervals_are_left_alone():
    assert merge([[1, 2], [5, 6]]) == [[1, 2], [5, 6]]


def test_unsorted_input_is_ordered_first():
    assert merge([[8, 10], [1, 3], [15, 18], [2, 6]]) == [[1, 6], [8, 10], [15, 18]]


def test_a_fully_contained_interval_does_not_shrink_the_result():
    # The max on the end is what prevents [1,10] being truncated to [1,3].
    assert merge([[1, 10], [2, 3]]) == [[1, 10]]


def test_chain_of_overlaps_collapses_to_one():
    assert merge([[1, 4], [3, 6], [5, 8], [7, 10]]) == [[1, 10]]


def test_identical_intervals_collapse():
    assert merge([[1, 4], [1, 4], [1, 4]]) == [[1, 4]]


def test_degenerate_point_intervals():
    assert merge([[1, 1], [2, 2]]) == [[1, 1], [2, 2]]
    assert merge([[1, 1], [1, 1]]) == [[1, 1]]


def test_same_start_different_ends():
    assert merge([[1, 3], [1, 7], [1, 5]]) == [[1, 7]]


def test_negative_bounds():
    assert merge([[-5, -3], [-4, 0]]) == [[-5, 0]]


def test_the_input_list_is_not_modified():
    intervals = [[1, 3], [2, 6]]
    snapshot = [list(pair) for pair in intervals]
    merge(intervals)
    assert intervals == snapshot


def test_output_is_sorted_and_non_overlapping():
    rng = random.Random(5)
    for _ in range(300):
        intervals = []
        for _ in range(rng.randint(1, 12)):
            start = rng.randint(-15, 15)
            intervals.append([start, start + rng.randint(0, 6)])
        result = merge(intervals)
        assert result == sorted(result)
        for earlier, later in zip(result, result[1:]):
            assert earlier[1] < later[0]


def test_merging_preserves_exactly_the_covered_points():
    rng = random.Random(9)
    for _ in range(300):
        intervals = []
        for _ in range(rng.randint(1, 12)):
            start = rng.randint(-15, 15)
            intervals.append([start, start + rng.randint(0, 6)])
        assert covered_points(merge(intervals)) == covered_points(intervals), intervals
