import random

from validate_binary_search_tree import TreeNode, is_valid_bst


def build(values):
    """Build a tree from a LeetCode-style level-order list, None for a gap."""
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


def in_order(node):
    values = []
    stack = []
    while node is not None or stack:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        values.append(node.val)
        node = node.right
    return values


def reference(root):
    """A valid BST is exactly one whose in-order walk strictly increases."""
    values = in_order(root)
    return all(a < b for a, b in zip(values, values[1:]))


def test_example_valid():
    assert is_valid_bst(build([2, 1, 3])) is True


def test_example_invalid():
    assert is_valid_bst(build([5, 1, 4, None, None, 3, 6])) is False


def test_empty_tree_is_valid():
    assert is_valid_bst(None) is True


def test_single_node_is_valid():
    assert is_valid_bst(build([1])) is True


def test_a_descendant_violating_an_ancestor_bound():
    # 6 is a legitimate right child of 2, so comparing only against its parent
    # passes. But it sits in 5's left subtree, where every value must stay below
    # 5, and 6 does not. Only a bound inherited from the ancestor catches it.
    root = TreeNode(5, TreeNode(2, TreeNode(1), TreeNode(6)), TreeNode(8))
    assert is_valid_bst(root) is False


def test_equal_values_are_rejected():
    assert is_valid_bst(build([2, 2, 3])) is False
    assert is_valid_bst(build([2, 1, 2])) is False


def test_left_leaning_chain_is_valid():
    root = TreeNode(3, TreeNode(2, TreeNode(1)))
    assert is_valid_bst(root) is True


def test_right_leaning_chain_is_valid():
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    assert is_valid_bst(root) is True


def test_extreme_values_are_allowed():
    # Sentinels must not be real values a node could hold.
    biggest, smallest = 2**63, -(2**63)
    assert is_valid_bst(TreeNode(smallest)) is True
    assert is_valid_bst(TreeNode(biggest)) is True
    assert is_valid_bst(TreeNode(0, TreeNode(smallest), TreeNode(biggest))) is True


def test_negative_values():
    assert is_valid_bst(build([-10, -20, -5])) is True
    assert is_valid_bst(build([-10, -5, -20])) is False


def test_a_deep_chain_does_not_recurse():
    root = TreeNode(0)
    node = root
    for depth in range(1, 5_000):
        node.right = TreeNode(depth)
        node = node.right
    assert is_valid_bst(root) is True


def test_matches_the_in_order_reference_on_random_trees():
    rng = random.Random(73)
    for _ in range(500):
        size = rng.randint(1, 12)
        values = [rng.choice([None] + list(range(1, 15))) for _ in range(size)]
        values[0] = rng.randint(1, 15)
        tree = build(values)
        assert is_valid_bst(tree) == reference(tree), values


def test_accepts_every_genuinely_sorted_tree_it_is_given():
    """Build real BSTs by insertion, so they must all validate."""
    rng = random.Random(79)
    for _ in range(200):
        root = None
        for value in rng.sample(range(200), rng.randint(1, 30)):
            if root is None:
                root = TreeNode(value)
                continue
            node = root
            while True:
                if value < node.val:
                    if node.left is None:
                        node.left = TreeNode(value)
                        break
                    node = node.left
                else:
                    if node.right is None:
                        node.right = TreeNode(value)
                        break
                    node = node.right
        assert is_valid_bst(root) is True
