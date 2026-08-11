import random

from sliding_window_maximum import max_sliding_window


def brute_force(nums, k):
    return [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]


def test_example():
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]


def test_single_element_window_returns_the_input():
    assert max_sliding_window([1, 3, -1], 1) == [1, 3, -1]


def test_window_spanning_the_whole_array():
    assert max_sliding_window([4, 2, 12, 3], 4) == [12]


def test_empty_input():
    assert max_sliding_window([], 3) == []


def test_single_element():
    assert max_sliding_window([9], 1) == [9]


def test_increasing_input():
    assert max_sliding_window([1, 2, 3, 4, 5], 3) == [3, 4, 5]


def test_decreasing_input():
    # The maximum expires every step, exercising the front eviction.
    assert max_sliding_window([5, 4, 3, 2, 1], 3) == [5, 4, 3]


def test_all_equal_values():
    assert max_sliding_window([7, 7, 7, 7], 2) == [7, 7, 7]


def test_duplicate_maxima_inside_a_window():
    # The <= when popping means an equal newer value replaces the older one; the
    # reported maximum must be unaffected either way.
    assert max_sliding_window([2, 5, 5, 1], 2) == [5, 5, 5]


def test_all_negative_values():
    assert max_sliding_window([-4, -2, -8, -1], 2) == [-2, -2, -1]


def test_maximum_leaves_the_window_and_a_smaller_one_takes_over():
    assert max_sliding_window([10, 1, 2, 3], 2) == [10, 2, 3]


def test_output_length_is_always_n_minus_k_plus_one():
    for size in range(1, 20):
        nums = list(range(size))
        for k in range(1, size + 1):
            assert len(max_sliding_window(nums, k)) == size - k + 1, (size, k)


def test_matches_brute_force_on_random_inputs():
    rng = random.Random(23)
    for _ in range(400):
        size = rng.randint(1, 40)
        nums = [rng.randint(-30, 30) for _ in range(size)]
        k = rng.randint(1, size)
        assert max_sliding_window(nums, k) == brute_force(nums, k), (nums, k)


def test_matches_brute_force_with_heavy_duplication():
    rng = random.Random(29)
    for _ in range(400):
        size = rng.randint(1, 25)
        nums = [rng.randint(0, 2) for _ in range(size)]
        k = rng.randint(1, size)
        assert max_sliding_window(nums, k) == brute_force(nums, k), (nums, k)
