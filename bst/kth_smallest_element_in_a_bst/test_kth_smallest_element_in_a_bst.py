import random

import pytest

from kth_smallest_element_in_a_bst import TreeNode, kth_smallest


def insert(root, value):
    """Build a real BST by insertion, so the invariant is never assumed."""
    if root is None:
        return TreeNode(value)
    node = root
    while True:
        if value < node.val:
            if node.left is None:
                node.left = TreeNode(value)
                return root
            node = node.left
        else:
            if node.right is None:
                node.right = TreeNode(value)
                return root
            node = node.right


def build(values):
    root = None
    for value in values:
        root = insert(root, value)
    return root


def test_example():
    assert kth_smallest(build([3, 1, 4, 2]), 1) == 1


def test_example_deeper():
    assert kth_smallest(build([5, 3, 6, 2, 4, 1]), 3) == 3


def test_single_node():
    assert kth_smallest(build([7]), 1) == 7


def test_k_of_one_is_the_minimum():
    assert kth_smallest(build([8, 3, 10, 1, 6, 14]), 1) == 1


def test_k_equal_to_size_is_the_maximum():
    values = [8, 3, 10, 1, 6, 14]
    assert kth_smallest(build(values), len(values)) == 14


def test_left_leaning_chain():
    # Inserting descending values produces a pure left spine.
    assert kth_smallest(build([5, 4, 3, 2, 1]), 2) == 2


def test_right_leaning_chain():
    assert kth_smallest(build([1, 2, 3, 4, 5]), 4) == 4


def test_negative_values():
    assert kth_smallest(build([0, -5, 5, -10]), 2) == -5


def test_k_beyond_the_tree_size_raises():
    with pytest.raises(ValueError):
        kth_smallest(build([2, 1, 3]), 4)


def test_empty_tree_raises():
    with pytest.raises(ValueError):
        kth_smallest(None, 1)


def test_every_k_matches_the_sorted_order():
    values = [50, 30, 70, 20, 40, 60, 80, 35, 65]
    tree = build(values)
    ordered = sorted(values)
    for k in range(1, len(values) + 1):
        assert kth_smallest(tree, k) == ordered[k - 1], k


def test_matches_sorted_on_random_trees():
    rng = random.Random(103)
    for _ in range(300):
        values = rng.sample(range(-100, 100), rng.randint(1, 30))
        tree = build(values)
        ordered = sorted(values)
        k = rng.randint(1, len(values))
        assert kth_smallest(tree, k) == ordered[k - 1], (values, k)


def test_handles_a_degenerate_chain_without_recursing():
    # 5,000 ascending inserts give a pure right spine; a recursive in-order walk
    # would exceed Python's stack limit here.
    tree = build(list(range(5_000)))
    assert kth_smallest(tree, 4_999) == 4_998
