import random

import pytest

from binary_tree_maximum_path_sum import TreeNode, max_path_sum


def build(values):
    """Build from a LeetCode-style level-order list, None for a gap."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    index = 1
    while queue and index < len(values):
        node = queue.pop(0)
        if index < len(values):
            value = values[index]
            index += 1
            if value is not None:
                node.left = TreeNode(value)
                queue.append(node.left)
        if index < len(values):
            value = values[index]
            index += 1
            if value is not None:
                node.right = TreeNode(value)
                queue.append(node.right)
    return root


def brute_force(root):
    """Every path, checked directly.

    A path is any simple route through the tree; it turns at exactly one node.
    So enumerating, for every node, the best downward run on each side and
    combining them covers all of them.
    """
    nodes = []

    def collect(n):
        if n is None:
            return
        nodes.append(n)
        collect(n.left)
        collect(n.right)

    collect(root)

    def best_down(n):
        """Best sum starting at n and descending, taking at least n."""
        if n is None:
            return float("-inf")
        return n.val + max(0, best_down(n.left), best_down(n.right))

    return max(
        n.val + max(0, best_down(n.left)) + max(0, best_down(n.right)) for n in nodes
    )


def test_example_simple():
    assert max_path_sum(build([1, 2, 3])) == 6


def test_example_with_negative_root():
    assert max_path_sum(build([-10, 9, 20, None, None, 15, 7])) == 42


def test_single_node():
    assert max_path_sum(build([5])) == 5


def test_single_negative_node():
    # The path must contain at least one node, so the answer can be negative.
    assert max_path_sum(build([-3])) == -3


def test_empty_tree_raises():
    with pytest.raises(ValueError):
        max_path_sum(None)


def test_all_negative_values_picks_the_least_bad():
    assert max_path_sum(build([-2, -1, -3])) == -1


def test_a_negative_child_is_skipped_rather_than_taken():
    # Adding -50 would only hurt, so the best path is 10 + 20.
    assert max_path_sum(build([10, -50, 20])) == 30


def test_the_best_path_need_not_include_the_root():
    # 15 + 20 + 7 sits entirely in the right subtree.
    assert max_path_sum(build([-100, 1, 20, None, None, 15, 7])) == 42


def test_a_path_turns_at_only_one_node():
    # Returning the split sum upward would let this fork twice and overcount.
    tree = build([2, 1, 3, 4, 5, 6, 7])
    assert max_path_sum(tree) == brute_force(tree)


def test_left_leaning_chain():
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert max_path_sum(root) == 6


def test_zeros_do_not_break_the_clamp():
    assert max_path_sum(build([0, 0, 0])) == 0


def test_matches_brute_force_on_random_trees():
    rng = random.Random(109)
    for _ in range(400):
        size = rng.randint(1, 12)
        values = [rng.choice([None] + list(range(-9, 10))) for _ in range(size)]
        values[0] = rng.randint(-9, 9)
        tree = build(values)
        assert max_path_sum(tree) == brute_force(tree), values


def test_matches_brute_force_on_all_negative_trees():
    rng = random.Random(113)
    for _ in range(300):
        size = rng.randint(1, 10)
        values = [rng.choice([None] + list(range(-9, 0))) for _ in range(size)]
        values[0] = rng.randint(-9, -1)
        tree = build(values)
        assert max_path_sum(tree) == brute_force(tree), values


def test_handles_a_deep_chain_without_recursing():
    root = TreeNode(1)
    node = root
    for _ in range(5_000):
        node.left = TreeNode(1)
        node = node.left
    assert max_path_sum(root) == 5_001
