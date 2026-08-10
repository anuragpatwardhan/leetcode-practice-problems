from itertools import combinations

from subarray_sum_equals_k import subarray_sum


def brute_force(nums, k):
    """Quadratic reference implementation used to cross-check the fast one."""
    return sum(
        1
        for start, end in combinations(range(len(nums) + 1), 2)
        if sum(nums[start:end]) == k
    )


def test_example_repeated_ones():
    assert subarray_sum([1, 1, 1], 2) == 2


def test_example_distinct_values():
    assert subarray_sum([1, 2, 3], 3) == 2


def test_subarray_starting_at_index_zero_is_counted():
    # Fails if the prefix map is not seeded with {0: 1}.
    assert subarray_sum([3, 4], 3) == 1


def test_negative_values_defeat_a_sliding_window():
    assert subarray_sum([1, -1, 0], 0) == 3


def test_repeated_prefix_sums_are_counted_separately():
    # Fails if prefix sums are stored as a set rather than a counter.
    assert subarray_sum([0, 0, 0], 0) == 6


def test_no_matching_subarray():
    assert subarray_sum([1, 2, 3], 100) == 0


def test_empty_array():
    assert subarray_sum([], 0) == 0


def test_single_element_match():
    assert subarray_sum([5], 5) == 1


def test_single_element_no_match():
    assert subarray_sum([5], 4) == 0


def test_whole_array_is_the_only_match():
    assert subarray_sum([2, 2, 2], 6) == 1


def test_mixed_signs():
    assert subarray_sum([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4


def test_matches_brute_force_on_varied_inputs():
    cases = [
        ([1, 2, 3, 4, 5], 5),
        ([-1, -1, 1], 0),
        ([1, -1, 1, -1], 0),
        ([0, 1, 0, 1], 1),
        ([5, -5, 5, -5, 5], 5),
        ([2, -1, 3, -2, 4], 4),
    ]
    for nums, k in cases:
        assert subarray_sum(nums, k) == brute_force(nums, k), (nums, k)
