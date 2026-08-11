from itertools import combinations

import pytest

from median_of_two_sorted_arrays import find_median_sorted_arrays


def reference(a, b):
    """Median by merging outright."""
    merged = sorted(a + b)
    mid = len(merged) // 2
    if len(merged) % 2:
        return float(merged[mid])
    return (merged[mid - 1] + merged[mid]) / 2


def test_example_odd_total():
    assert find_median_sorted_arrays([1, 3], [2]) == 2.0


def test_example_even_total():
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5


def test_first_array_empty():
    assert find_median_sorted_arrays([], [1, 2, 3]) == 2.0


def test_second_array_empty():
    assert find_median_sorted_arrays([1, 2, 3, 4], []) == 2.5


def test_single_elements():
    assert find_median_sorted_arrays([1], [2]) == 1.5


def test_both_arrays_empty_is_an_error():
    with pytest.raises(ValueError):
        find_median_sorted_arrays([], [])


def test_arrays_do_not_overlap():
    assert find_median_sorted_arrays([1, 2, 3], [7, 8, 9]) == 5.0


def test_longer_array_given_first():
    # The implementation swaps internally; the answer must not depend on order.
    assert find_median_sorted_arrays([1, 2, 3, 4, 5], [6]) == 3.5
    assert find_median_sorted_arrays([6], [1, 2, 3, 4, 5]) == 3.5


def test_all_values_identical():
    assert find_median_sorted_arrays([2, 2, 2], [2, 2]) == 2.0


def test_duplicates_across_both_arrays():
    assert find_median_sorted_arrays([1, 1, 3], [1, 1, 3]) == 1.0


def test_negative_values():
    assert find_median_sorted_arrays([-5, -3], [-4, -1]) == -3.5


def test_result_is_a_float_even_when_whole():
    result = find_median_sorted_arrays([1, 3], [2])
    assert isinstance(result, float)


def test_matches_a_full_merge_on_every_small_split():
    # Split each sorted set every possible way between the two arrays.
    for size in range(1, 11):
        values = list(range(size))
        for take in range(size + 1):
            for left_idx in combinations(range(size), take):
                a = [values[i] for i in left_idx]
                b = [values[i] for i in range(size) if i not in left_idx]
                assert find_median_sorted_arrays(a, b) == reference(a, b), (a, b)


def test_matches_a_full_merge_with_repeated_values():
    for size in range(1, 9):
        values = sorted([v // 2 for v in range(size)])
        for take in range(size + 1):
            for left_idx in combinations(range(size), take):
                a = [values[i] for i in left_idx]
                b = [values[i] for i in range(size) if i not in left_idx]
                assert find_median_sorted_arrays(a, b) == reference(a, b), (a, b)
