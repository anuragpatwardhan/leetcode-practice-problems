import random
from itertools import permutations as itertools_permutations
from math import factorial

from permutations import permute


def canonical(result):
    """Order-insensitive view, since the problem accepts any ordering of results."""
    return sorted(tuple(p) for p in result)


def reference(nums):
    """Independent check: the standard library's own permutation generator.

    A different implementation entirely — itertools generates in lexicographic
    order of input positions without any backtracking — so agreement is
    meaningful rather than the same idea retyped.
    """
    return [list(p) for p in itertools_permutations(nums)]


def test_single_element():
    assert permute([1]) == [[1]]


def test_two_elements():
    assert canonical(permute([1, 2])) == [(1, 2), (2, 1)]


def test_three_elements():
    assert canonical(permute([1, 2, 3])) == [
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 1, 2),
        (3, 2, 1),
    ]


def test_empty_input_has_one_permutation():
    # The empty ordering, not zero orderings. 0! is 1, and anything counting
    # results downstream depends on that.
    assert permute([]) == [[]]


def test_count_is_n_factorial():
    for n in range(1, 7):
        assert len(permute(list(range(n)))) == factorial(n)


def test_every_result_is_a_full_length_ordering():
    nums = [4, 7, 1, 9]
    for candidate in permute(nums):
        assert len(candidate) == len(nums)


def test_every_result_uses_each_element_exactly_once():
    # The property the used-flag bookkeeping exists to guarantee. A missed undo
    # shows up here as a short or repeated ordering.
    nums = [4, 7, 1, 9]
    for candidate in permute(nums):
        assert sorted(candidate) == sorted(nums)


def test_results_are_distinct():
    nums = [1, 2, 3, 4]
    results = permute(nums)
    assert len({tuple(p) for p in results}) == len(results)


def test_results_are_separate_lists():
    # Appending the live path instead of a copy makes every entry the same
    # object, so they all read as the last state the path was in.
    results = permute([1, 2, 3])
    results[0][0] = 99
    assert results[1][0] != 99


def test_does_not_modify_the_input():
    nums = [3, 1, 2]
    before = nums.copy()
    permute(nums)
    assert nums == before


def test_negative_and_zero_values():
    assert canonical(permute([0, -1])) == [(-1, 0), (0, -1)]


def test_calling_twice_gives_the_same_answer():
    # Shared mutable state left dirty between calls would show up here.
    nums = [1, 2, 3]
    assert canonical(permute(nums)) == canonical(permute(nums))


def test_matches_itertools_on_small_inputs():
    for n in range(0, 7):
        nums = list(range(n))
        assert canonical(permute(nums)) == canonical(reference(nums))


def test_matches_itertools_on_random_inputs():
    rng = random.Random(46)
    for _ in range(200):
        # LeetCode guarantees distinct values, so the inputs sampled here are
        # distinct too — duplicates are LeetCode 47, a different problem.
        size = rng.randint(1, 6)
        nums = rng.sample(range(-20, 20), size)
        assert canonical(permute(nums)) == canonical(reference(nums))


def test_deepest_input_within_a_second():
    # 8! is 40,320 orderings, which is the largest size that keeps this suite
    # near a second. The recursion-depth argument is about the shape, not the
    # size: depth is len(nums), so it is small here by construction — but the
    # iterative frame handling is what this exercises hardest, since every
    # frame is entered, resumed and popped many times over.
    nums = list(range(8))
    results = permute(nums)
    assert len(results) == factorial(8)
    assert len({tuple(p) for p in results}) == factorial(8)
