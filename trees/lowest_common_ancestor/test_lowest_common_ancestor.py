from lowest_common_ancestor import TreeNode, lowest_common_ancestor


def build_example():
    """The tree from LeetCode's own example: [3,5,1,6,2,0,8,None,None,7,4]."""
    seven = TreeNode(7)
    four = TreeNode(4)
    two = TreeNode(2, seven, four)
    six = TreeNode(6)
    five = TreeNode(5, six, two)
    zero = TreeNode(0)
    eight = TreeNode(8)
    one = TreeNode(1, zero, eight)
    root = TreeNode(3, five, one)
    return root, five, one, six, two, zero, eight, seven, four


def test_targets_in_different_subtrees():
    root, five, one, *_ = build_example()
    assert lowest_common_ancestor(root, five, one) is root


def test_one_target_is_ancestor_of_the_other():
    root, five, _one, _six, two, _zero, _eight, _seven, four = build_example()
    assert lowest_common_ancestor(root, five, four) is five


def test_both_targets_share_a_grandparent():
    root, _five, _one, _six, two, _zero, _eight, seven, four = build_example()
    assert lowest_common_ancestor(root, seven, four) is two


def test_root_is_one_of_the_targets():
    root, five, *_ = build_example()
    assert lowest_common_ancestor(root, root, five) is root


def test_single_node_tree_with_p_equal_to_q():
    root = TreeNode(1)
    assert lowest_common_ancestor(root, root, root) is root


def test_sibling_leaves_share_their_direct_parent():
    root, _five, one, _six, _two, zero, eight, *_ = build_example()
    assert lowest_common_ancestor(root, zero, eight) is one


def test_deep_skewed_chain_does_not_hit_the_recursion_limit():
    # A left-leaning chain far past Python's default recursion limit, so a
    # recursive postorder search over it would raise RecursionError.
    depth = 5000
    root = TreeNode(0)
    node = root
    nodes = [root]
    for i in range(1, depth):
        node.left = TreeNode(i)
        node = node.left
        nodes.append(node)

    shallow, deep = nodes[10], nodes[-1]
    assert lowest_common_ancestor(root, shallow, deep) is shallow
