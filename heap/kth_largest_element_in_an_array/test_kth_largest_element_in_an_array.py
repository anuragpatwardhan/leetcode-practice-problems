import random

from kth_largest_element_in_an_array import find_kth_largest


def reference(nums, k):
    """Sort descending and index — obvious, and O(n log n)."""
    return sorted(nums, reverse=True)[k - 1]


def test_example():
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5


def test_example_with_duplicates():
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4


def test_k_of_one_is_the_maximum():
    assert find_kth_largest([7, 2, 9, 4], 1) == 9


def test_k_equal_to_length_is_the_minimum():
    assert find_kth_largest([7, 2, 9, 4], 4) == 2


def test_single_element():
    assert find_kth_largest([5], 1) == 5


def test_all_equal_values():
    assert find_kth_largest([4, 4, 4, 4], 3) == 4


def test_duplicates_occupy_separate_ranks():
    # The 1st and 2nd largest are both 9; the 3rd is 5. Deduplicating first
    # would wrongly return 5 for k=2.
    assert find_kth_largest([9, 9, 5, 1], 1) == 9
    assert find_kth_largest([9, 9, 5, 1], 2) == 9
    assert find_kth_largest([9, 9, 5, 1], 3) == 5


def test_negative_values():
    assert find_kth_largest([-1, -5, -3], 2) == -3


def test_mixed_signs():
    assert find_kth_largest([-2, 0, 5, -7, 3], 2) == 3


def test_already_sorted_ascending():
    assert find_kth_largest([1, 2, 3, 4, 5], 2) == 4


def test_already_sorted_descending():
    assert find_kth_largest([5, 4, 3, 2, 1], 2) == 4


def test_the_input_list_is_not_modified():
    nums = [3, 2, 1, 5, 6, 4]
    snapshot = list(nums)
    find_kth_largest(nums, 3)
    assert nums == snapshot


def test_every_k_on_a_fixed_array():
    nums = [12, 3, 7, 7, 1, 20, -4]
    for k in range(1, len(nums) + 1):
        assert find_kth_largest(nums, k) == reference(nums, k), k


def test_matches_the_reference_on_random_inputs():
    rng = random.Random(89)
    for _ in range(400):
        size = rng.randint(1, 40)
        nums = [rng.randint(-50, 50) for _ in range(size)]
        k = rng.randint(1, size)
        assert find_kth_largest(nums, k) == reference(nums, k), (nums, k)


def test_matches_the_reference_with_heavy_duplication():
    rng = random.Random(97)
    for _ in range(400):
        size = rng.randint(1, 25)
        nums = [rng.randint(0, 3) for _ in range(size)]
        k = rng.randint(1, size)
        assert find_kth_largest(nums, k) == reference(nums, k), (nums, k)


def test_handles_a_large_input():
    rng = random.Random(101)
    nums = [rng.randint(0, 1_000_000) for _ in range(50_000)]
    assert find_kth_largest(nums, 500) == reference(nums, 500)
