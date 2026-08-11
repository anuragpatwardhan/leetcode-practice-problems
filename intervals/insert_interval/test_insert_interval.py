import random

from insert_interval import insert


def merge_from_scratch(intervals):
    """Independent reference: sort everything and merge in one pass."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda pair: pair[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def test_example_simple_overlap():
    assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]


def test_example_spanning_several_intervals():
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]


def test_insert_into_an_empty_list():
    assert insert([], [5, 7]) == [[5, 7]]


def test_insert_before_everything():
    assert insert([[3, 5], [8, 10]], [1, 2]) == [[1, 2], [3, 5], [8, 10]]


def test_insert_after_everything():
    assert insert([[1, 2], [3, 5]], [8, 10]) == [[1, 2], [3, 5], [8, 10]]


def test_insert_into_a_gap():
    assert insert([[1, 2], [8, 10]], [4, 6]) == [[1, 2], [4, 6], [8, 10]]


def test_touching_at_the_left_edge_merges():
    assert insert([[1, 2], [5, 7]], [2, 3]) == [[1, 3], [5, 7]]


def test_touching_at_the_right_edge_merges():
    assert insert([[1, 2], [5, 7]], [3, 5]) == [[1, 2], [3, 7]]


def test_new_interval_swallowed_by_an_existing_one():
    # The min on the start is what keeps this from becoming [2,5].
    assert insert([[1, 5]], [2, 3]) == [[1, 5]]


def test_new_interval_swallows_everything():
    assert insert([[2, 3], [5, 6], [8, 9]], [1, 10]) == [[1, 10]]


def test_degenerate_point_interval():
    assert insert([[1, 5]], [3, 3]) == [[1, 5]]
    assert insert([[1, 2], [6, 7]], [4, 4]) == [[1, 2], [4, 4], [6, 7]]


def test_negative_bounds():
    assert insert([[-8, -5], [1, 3]], [-6, 0]) == [[-8, 0], [1, 3]]


def test_the_input_list_is_not_modified():
    intervals = [[1, 3], [6, 9]]
    snapshot = [list(pair) for pair in intervals]
    insert(intervals, [2, 5])
    assert intervals == snapshot


def test_matches_a_full_merge_on_random_inputs():
    rng = random.Random(13)
    for _ in range(400):
        # Build a sorted, disjoint list the way the problem guarantees.
        intervals = []
        cursor = rng.randint(-20, -10)
        for _ in range(rng.randint(0, 8)):
            start = cursor + rng.randint(1, 4)
            end = start + rng.randint(0, 3)
            intervals.append([start, end])
            cursor = end
        new_start = rng.randint(-25, 25)
        new = [new_start, new_start + rng.randint(0, 8)]

        assert insert(intervals, new) == merge_from_scratch(intervals + [new]), (intervals, new)
