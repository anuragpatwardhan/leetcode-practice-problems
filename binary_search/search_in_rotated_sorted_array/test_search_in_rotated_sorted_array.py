from search_in_rotated_sorted_array import search


def rotations(values):
    """Every rotation of ``values``, including the unrotated original."""
    return [values[i:] + values[:i] for i in range(len(values))]


def test_example_target_present():
    assert search([4, 5, 6, 7, 0, 1, 2], 0) == 4


def test_example_target_absent():
    assert search([4, 5, 6, 7, 0, 1, 2], 3) == -1


def test_empty_array():
    assert search([], 5) == -1


def test_single_element_found():
    assert search([1], 1) == 0


def test_single_element_missing():
    assert search([1], 0) == -1


def test_two_elements_rotated():
    # mid == low here, which is why the sorted-side check uses <= rather than <.
    assert search([3, 1], 1) == 1
    assert search([3, 1], 3) == 0


def test_unrotated_array_still_works():
    assert search([1, 2, 3, 4, 5], 4) == 3


def test_pivot_element_is_found():
    # The smallest value sits at the rotation point, the easiest index to skip.
    assert search([4, 5, 6, 7, 0, 1, 2], 4) == 0
    assert search([4, 5, 6, 7, 0, 1, 2], 2) == 6


def test_target_between_the_two_sorted_runs_is_absent():
    # 3 is larger than every value in the right run and smaller than every value
    # in the left run, so a naive range check on the wrong side would find it.
    assert search([5, 6, 7, 1, 2, 3], 4) == -1


def test_negative_values():
    assert search([1, 2, -3, -2, -1], -3) == 2


def test_every_rotation_and_target_matches_a_linear_scan():
    values = list(range(9))
    for rotated in rotations(values):
        for target in values:
            expected = rotated.index(target)
            assert search(rotated, target) == expected, (rotated, target)


def test_every_rotation_reports_absent_targets():
    values = [n * 2 for n in range(8)]  # even numbers only
    for rotated in rotations(values):
        for target in (-1, 1, 7, 15, 100):
            assert search(rotated, target) == -1, (rotated, target)


def test_all_lengths_up_to_ten():
    for size in range(1, 11):
        values = list(range(size))
        for rotated in rotations(values):
            for target in values:
                assert search(rotated, target) == rotated.index(target)
