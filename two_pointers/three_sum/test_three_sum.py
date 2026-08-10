from three_sum import three_sum


def normalise(triplets):
    """Order-independent comparison helper for the returned triplets."""
    return sorted(tuple(triplet) for triplet in triplets)


def test_example_with_two_triplets():
    assert normalise(three_sum([-1, 0, 1, 2, -1, -4])) == normalise(
        [[-1, -1, 2], [-1, 0, 1]]
    )


def test_no_triplet_sums_to_zero():
    assert three_sum([0, 1, 1]) == []


def test_all_zeros_returns_single_triplet():
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]


def test_many_zeros_still_returns_single_triplet():
    assert three_sum([0, 0, 0, 0, 0]) == [[0, 0, 0]]


def test_fewer_than_three_values():
    assert three_sum([]) == []
    assert three_sum([1]) == []
    assert three_sum([1, -1]) == []


def test_all_positive_values():
    assert three_sum([1, 2, 3, 4]) == []


def test_all_negative_values():
    assert three_sum([-1, -2, -3, -4]) == []


def test_duplicate_heavy_input_is_deduplicated():
    assert three_sum([-2, 0, 0, 2, 2, -2]) == [[-2, 0, 2]]


def test_returned_triplets_are_sorted_ascending():
    for triplet in three_sum([-4, 2, -2, 1, 3, -1, 0]):
        assert triplet == sorted(triplet)


def test_result_contains_no_duplicates():
    result = three_sum([-1, 0, 1, 2, -1, -4, -1, 0, 1])
    assert len(result) == len({tuple(triplet) for triplet in result})
