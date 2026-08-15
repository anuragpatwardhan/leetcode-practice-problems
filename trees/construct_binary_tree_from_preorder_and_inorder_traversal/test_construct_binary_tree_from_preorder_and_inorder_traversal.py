from construct_binary_tree_from_preorder_and_inorder_traversal import TreeNode, build_tree


def preorder_values(root):
    """Iterative preorder walk, used only to check the rebuilt shape."""
    values = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        values.append(node.val)
        stack.append(node.right)
        stack.append(node.left)
    return values


def inorder_values(root):
    """Iterative inorder walk, used only to check the rebuilt shape."""
    values = []
    stack = []
    node = root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        values.append(node.val)
        node = node.right
    return values


def test_example_from_leetcode():
    root = build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    assert root.val == 3
    assert root.left.val == 9
    assert root.left.left is None and root.left.right is None
    assert root.right.val == 20
    assert root.right.left.val == 15
    assert root.right.right.val == 7


def test_single_node():
    root = build_tree([1], [1])
    assert root.val == 1
    assert root.left is None
    assert root.right is None


def test_empty_traversals_yield_no_tree():
    assert build_tree([], []) is None


def test_left_skewed_chain():
    root = build_tree([3, 2, 1], [1, 2, 3])
    assert root.val == 3
    assert root.right is None
    assert root.left.val == 2
    assert root.left.right is None
    assert root.left.left.val == 1


def test_right_skewed_chain():
    root = build_tree([1, 2, 3], [1, 2, 3])
    assert root.val == 1
    assert root.left is None
    assert root.right.val == 2
    assert root.right.left is None
    assert root.right.right.val == 3


def test_negative_and_repeated_magnitude_values():
    # -2 and 2 share a magnitude, which would confuse an equality check that
    # normalised sign, so the tree is walked and the exact values asserted.
    root = build_tree([0, -2, 2], [-2, 0, 2])
    assert root.val == 0
    assert root.left.val == -2
    assert root.right.val == 2


def test_traversals_round_trip_through_a_wider_tree():
    preorder = [8, 4, 2, 1, 3, 6, 5, 7, 12, 10, 9, 11, 14, 13, 15]
    inorder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    root = build_tree(preorder, inorder)
    assert preorder_values(root) == preorder
    assert inorder_values(root) == inorder


def test_deep_left_skewed_chain_does_not_hit_the_recursion_limit():
    # Preorder and inorder for a chain purely descending through left
    # children -- the shape that would make a recursive slice-and-recurse
    # solution recurse to depth n.
    depth = 5000
    preorder = list(range(depth, 0, -1))
    inorder = list(range(1, depth + 1))

    root = build_tree(preorder, inorder)

    node = root
    count = 0
    while node is not None:
        assert node.right is None
        count += 1
        node = node.left
    assert count == depth
