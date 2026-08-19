import random

from binary_search import search


def test_example_found():
    assert search([-1, 0, 3, 5, 9, 12], 9) == 4


def test_example_absent():
    assert search([-1, 0, 3, 5, 9, 12], 2) == -1


def test_empty_array():
    assert search([], 1) == -1


def test_single_element_found():
    # The case an exclusive `low < high` loop silently skips.
    assert search([5], 5) == 0


def test_single_element_absent():
    assert search([5], 3) == -1


def test_two_elements():
    assert search([1, 2], 1) == 0
    assert search([1, 2], 2) == 1
    assert search([1, 2], 3) == -1


def test_first_and_last_positions():
    nums = [1, 3, 5, 7, 9]
    assert search(nums, 1) == 0
    assert search(nums, 9) == 4


def test_target_below_and_above_the_range():
    nums = [10, 20, 30]
    assert search(nums, 5) == -1
    assert search(nums, 35) == -1


def test_negative_values():
    assert search([-9, -5, -1], -5) == 1


def test_every_index_of_a_fixed_array():
    nums = [2, 4, 6, 8, 10, 12, 14]
    for index, value in enumerate(nums):
        assert search(nums, value) == index


def test_absent_targets_between_every_pair():
    nums = [2, 4, 6, 8]
    for gap in (1, 3, 5, 7, 9):
        assert search(nums, gap) == -1


def test_matches_list_index_on_random_arrays():
    rng = random.Random(223)
    for _ in range(500):
        # Distinct values, since the problem guarantees uniqueness and index
        # equality would otherwise be ambiguous.
        nums = sorted(rng.sample(range(-200, 200), rng.randint(0, 40)))
        for target in nums:
            assert search(nums, target) == nums.index(target), (nums, target)


def test_reports_absent_targets_on_random_arrays():
    rng = random.Random(227)
    for _ in range(500):
        nums = sorted(rng.sample(range(0, 400, 2), rng.randint(0, 40)))  # evens only
        for target in (-1, 1, 401):
            assert search(nums, target) == -1, (nums, target)


def test_terminates_on_a_large_array():
    # A range-update bug shows up as a hang rather than a wrong answer, so this
    # is really a termination check.
    nums = list(range(0, 2_000_000, 2))
    assert search(nums, 1_999_998) == len(nums) - 1
    assert search(nums, 999_999) == -1
