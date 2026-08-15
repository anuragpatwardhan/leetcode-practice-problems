from serialize_and_deserialize_binary_tree import TreeNode, deserialize, serialize


def level_values(root):
    """Iterative level-order walk (values only, gaps skipped) for shape checks."""
    if root is None:
        return []
    values = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        values.append(node.val)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return values


def test_round_trips_the_leetcode_example():
    root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
    rebuilt = deserialize(serialize(root))
    assert level_values(rebuilt) == [1, 2, 3, 4, 5]
    assert rebuilt.left.left is None and rebuilt.left.right is None
    assert rebuilt.right.left.val == 4
    assert rebuilt.right.right.val == 5


def test_empty_tree():
    assert serialize(None) == ""
    assert deserialize("") is None


def test_single_node():
    root = TreeNode(42)
    rebuilt = deserialize(serialize(root))
    assert rebuilt.val == 42
    assert rebuilt.left is None
    assert rebuilt.right is None


def test_negative_values_round_trip():
    root = TreeNode(-5, TreeNode(-10), TreeNode(0))
    rebuilt = deserialize(serialize(root))
    assert rebuilt.val == -5
    assert rebuilt.left.val == -10
    assert rebuilt.right.val == 0


def test_left_skewed_chain_round_trips():
    root = TreeNode(3, TreeNode(2, TreeNode(1)))
    rebuilt = deserialize(serialize(root))
    assert rebuilt.val == 3
    assert rebuilt.right is None
    assert rebuilt.left.val == 2
    assert rebuilt.left.right is None
    assert rebuilt.left.left.val == 1


def test_serialization_marks_every_missing_child_not_just_a_trailing_gap():
    # A right-only node: the gap is in the middle of the level, not at the
    # end, so a scheme that only marked trailing nulls would misplace 3 as
    # node 2's left child instead of its right child on deserialize.
    root = TreeNode(1, None, TreeNode(2, TreeNode(3), None))
    encoded = serialize(root)
    assert encoded == "1,#,2,3,#,#,#"
    rebuilt = deserialize(encoded)
    assert rebuilt.left is None
    assert rebuilt.right.left.val == 3
    assert rebuilt.right.right is None


def test_deep_skewed_chain_round_trips_without_hitting_the_recursion_limit():
    # A recursive preorder-with-markers implementation would recurse to
    # depth n on this chain and raise RecursionError.
    depth = 5000
    root = TreeNode(0)
    node = root
    for i in range(1, depth):
        node.left = TreeNode(i)
        node = node.left

    rebuilt = deserialize(serialize(root))

    node = rebuilt
    count = 0
    while node is not None:
        assert node.val == count
        assert node.right is None
        count += 1
        node = node.left
    assert count == depth
