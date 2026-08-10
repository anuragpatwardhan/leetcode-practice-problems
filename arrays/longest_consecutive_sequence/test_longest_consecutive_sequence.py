from longest_consecutive_sequence import longest_consecutive


def test_example_unordered_run():
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4


def test_longer_example_with_duplicates():
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9


def test_empty_list():
    assert longest_consecutive([]) == 0


def test_single_value():
    assert longest_consecutive([7]) == 1


def test_all_duplicates_count_once():
    assert longest_consecutive([5, 5, 5, 5]) == 1


def test_no_consecutive_values():
    assert longest_consecutive([10, 30, 20, 50]) == 1


def test_negative_and_positive_span_zero():
    assert longest_consecutive([-3, -2, -1, 0, 1]) == 5


def test_two_separate_runs_returns_longer():
    assert longest_consecutive([1, 2, 3, 100, 101]) == 3


def test_run_appears_after_longer_prefix():
    assert longest_consecutive([9, 1, 4, 7, 3, 2, 6, 8, 5]) == 9
