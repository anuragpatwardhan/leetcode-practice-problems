import random

from k_closest_points_to_origin import k_closest


def squared(point):
    x, y = point
    return x * x + y * y


def reference(points, k):
    """Independent check: sort everything by distance and take the first k.

    A full sort rather than a bounded heap — the thing the heap exists to avoid —
    so agreement is meaningful rather than the same idea retyped.
    """
    return sorted(points, key=squared)[: max(k, 0)]


def assert_valid(result, points, k):
    """Validate the answer rather than compare to one.

    Ties make the answer non-unique: with four points all at distance 2 and
    k = 2, any pair is correct. What must hold is that the returned points came
    from the input and that their distances are exactly the k smallest.
    """
    expected = max(0, min(k, len(points)))
    assert len(result) == expected, (result, points, k)

    remaining = [list(p) for p in points]
    for point in result:
        assert list(point) in remaining, (point, points)
        remaining.remove(list(point))

    assert sorted(squared(p) for p in result) == sorted(
        squared(p) for p in reference(points, k)
    ), (result, points, k)


def test_example_one():
    assert_valid(k_closest([[1, 3], [-2, 2]], 1), [[1, 3], [-2, 2]], 1)
    assert k_closest([[1, 3], [-2, 2]], 1) == [[-2, 2]]


def test_example_two():
    points = [[3, 3], [5, -1], [-2, 4]]
    assert_valid(k_closest(points, 2), points, 2)


def test_single_point():
    assert k_closest([[1, 1]], 1) == [[1, 1]]


def test_k_equal_to_the_number_of_points():
    points = [[1, 1], [2, 2], [3, 3]]
    assert sorted(k_closest(points, 3)) == sorted(points)


def test_k_larger_than_the_number_of_points():
    # Not an error: everything qualifies.
    points = [[1, 1], [2, 2]]
    assert sorted(k_closest(points, 10)) == sorted(points)


def test_k_of_zero_returns_nothing():
    assert k_closest([[1, 1], [2, 2]], 0) == []


def test_negative_k_returns_nothing():
    assert k_closest([[1, 1]], -3) == []


def test_no_points():
    assert k_closest([], 3) == []


def test_the_origin_itself_is_closest():
    points = [[5, 5], [0, 0], [1, 1]]
    assert k_closest(points, 1) == [[0, 0]]


def test_negative_coordinates_are_measured_by_magnitude():
    # (-1, -1) is as close as (1, 1); a solution comparing raw coordinates
    # rather than squared distance would rank it first or last.
    points = [[-1, -1], [3, 0]]
    assert k_closest(points, 1) == [[-1, -1]]


def test_all_points_the_same_distance():
    # Every answer is correct here, so only the count and the distances can be
    # asserted.
    points = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    assert_valid(k_closest(points, 2), points, 2)


def test_duplicate_points():
    points = [[1, 1], [1, 1], [9, 9]]
    assert_valid(k_closest(points, 2), points, 2)


def test_ties_across_different_coordinates():
    # (0, 5) and (3, 4) are both at distance 25 from the origin.
    points = [[0, 5], [3, 4], [1, 0]]
    result = k_closest(points, 2)
    assert_valid(result, points, 2)
    assert [1, 0] in [list(p) for p in result]


def test_does_not_modify_the_input():
    points = [[3, 3], [5, -1], [-2, 4]]
    before = [p[:] for p in points]
    k_closest(points, 2)
    assert points == before


def test_result_does_not_alias_the_input_rows():
    # When k covers everything the shortcut could hand back the caller's own
    # lists, so mutating the result would reach into their data.
    points = [[1, 1], [2, 2]]
    result = k_closest(points, 5)
    result[0][0] = 99
    assert points == [[1, 1], [2, 2]]


def test_calling_twice_gives_the_same_answer():
    points = [[3, 3], [5, -1], [-2, 4], [0, 1]]
    assert k_closest(points, 2) == k_closest(points, 2)


def test_points_on_the_axes():
    points = [[0, 4], [3, 0], [0, -1]]
    assert k_closest(points, 1) == [[0, -1]]


def test_large_input_with_small_k():
    # 200,000 points for k = 5. This is what the bounded heap buys: the heap
    # never exceeds 5 entries, so the work is O(n log k) rather than a full
    # O(n log n) sort of the whole input.
    rng = random.Random(973)
    points = [[rng.randint(-10_000, 10_000), rng.randint(-10_000, 10_000)] for _ in range(200_000)]
    points[12_345] = [0, 0]
    result = k_closest(points, 5)
    assert len(result) == 5
    assert [0, 0] in [list(p) for p in result]


def test_matches_a_full_sort_on_random_inputs():
    rng = random.Random(974)
    for _ in range(400):
        size = rng.randint(1, 12)
        points = [[rng.randint(-8, 8), rng.randint(-8, 8)] for _ in range(size)]
        k = rng.randint(0, size + 2)
        assert_valid(k_closest(points, k), points, k)


def test_matches_a_full_sort_when_distances_collide():
    # A small coordinate range so ties are common, which is where validating
    # the property instead of comparing to one answer actually matters.
    rng = random.Random(975)
    for _ in range(400):
        size = rng.randint(1, 10)
        points = [[rng.randint(-2, 2), rng.randint(-2, 2)] for _ in range(size)]
        k = rng.randint(1, size)
        assert_valid(k_closest(points, k), points, k)


def test_every_k_over_one_input():
    # Walks k from 0 past the end on a fixed input, so an off-by-one at either
    # boundary has nowhere to hide.
    points = [[2, 2], [0, 1], [-3, 0], [1, 1], [5, 5]]
    for k in range(0, len(points) + 3):
        assert_valid(k_closest(points, k), points, k)
