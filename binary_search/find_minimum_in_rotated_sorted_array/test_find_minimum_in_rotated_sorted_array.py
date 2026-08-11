from find_minimum_in_rotated_sorted_array import find_min


def rotations(values):
    """Every rotation of ``values``, including the unrotated original."""
    return [values[i:] + values[:i] for i in range(len(values))]


def test_example():
    assert find_min([3, 4, 5, 1, 2]) == 1


def test_example_with_larger_rotation():
    assert find_min([4, 5, 6, 7, 0, 1, 2]) == 0


def test_single_element():
    assert find_min([1]) == 1


def test_two_elements_rotated():
    assert find_min([2, 1]) == 1


def test_two_elements_unrotated():
    assert find_min([1, 2]) == 1


def test_unrotated_array_returns_its_first_element():
    # The case that breaks a version comparing nums[mid] against nums[low].
    assert find_min([1, 2, 3, 4, 5]) == 1


def test_rotated_by_one():
    assert find_min([2, 3, 4, 5, 1]) == 1


def test_minimum_sits_at_the_midpoint():
    assert find_min([4, 5, 1, 2, 3]) == 1


def test_negative_values():
    assert find_min([2, 3, -4, -3, -2]) == -4


def test_every_rotation_of_every_length_up_to_twelve():
    for size in range(1, 13):
        values = list(range(size))
        for rotated in rotations(values):
            assert find_min(rotated) == 0, rotated


def test_matches_builtin_min_on_non_contiguous_values():
    values = [n * 3 - 7 for n in range(11)]
    for rotated in rotations(values):
        assert find_min(rotated) == min(values), rotated
