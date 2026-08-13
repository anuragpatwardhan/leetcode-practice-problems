from binary_tree_level_order_traversal import TreeNode, level_order


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


def test_example():
    assert level_order(build([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]


def test_single_node():
    assert level_order(build([1])) == [[1]]


def test_empty_tree():
    assert level_order(None) == []


def test_left_leaning_chain():
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert level_order(root) == [[1], [2], [3]]


def test_right_leaning_chain():
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    assert level_order(root) == [[1], [2], [3]]


def test_rows_read_left_to_right():
    assert level_order(build([1, 2, 3, 4, 5, 6, 7])) == [[1], [2, 3], [4, 5, 6, 7]]


def test_a_gap_does_not_shift_the_remaining_nodes():
    # 4 is a left child and 7 a right child two levels down; both belong on the
    # same row without any placeholder between them.
    assert level_order(build([1, 2, 3, 4, None, None, 7])) == [[1], [2, 3], [4, 7]]


def test_duplicate_values_are_all_reported():
    assert level_order(build([1, 1, 1])) == [[1], [1, 1]]


def test_negative_values():
    assert level_order(build([-1, -2, -3])) == [[-1], [-2, -3]]


def test_row_widths_match_the_tree_shape():
    tree = build([1, 2, 3, 4, 5, None, 8])
    assert [len(row) for row in level_order(tree)] == [1, 2, 3]


def test_every_node_appears_exactly_once():
    values = list(range(1, 32))  # a full tree of depth 5
    rows = level_order(build(values))
    assert sorted(value for row in rows for value in row) == values


def test_a_deep_chain_does_not_recurse():
    # 5,000 levels: an implementation using recursion would hit the limit.
    root = TreeNode(0)
    node = root
    for depth in range(1, 5_000):
        node.left = TreeNode(depth)
        node = node.left
    assert len(level_order(root)) == 5_000
