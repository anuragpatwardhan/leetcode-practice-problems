"""LeetCode 236. Lowest Common Ancestor of a Binary Tree."""

from typing import Optional


class TreeNode:
    """Binary tree node, matching LeetCode's definition."""

    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """Return the deepest node that has both p and q as descendants (or is one of them)."""
    # Iterative, for the same reason validate_binary_search_tree is: a
    # recursive postorder search would risk the call-stack limit on a
    # degenerate, list-shaped tree. One pass builds parent pointers, then two
    # short walks up from p and q find where their paths to the root meet.
    parent: dict[TreeNode, Optional[TreeNode]] = {root: None}
    stack = [root]

    # Stop as soon as both targets are known rather than walking the whole
    # tree -- most calls locate both long before the last leaf.
    while p not in parent or q not in parent:
        node = stack.pop()
        if node.left is not None:
            parent[node.left] = node
            stack.append(node.left)
        if node.right is not None:
            parent[node.right] = node
            stack.append(node.right)

    ancestors = set()
    walker: Optional[TreeNode] = p
    while walker is not None:
        ancestors.add(walker)
        walker = parent[walker]

    walker = q
    while walker not in ancestors:
        walker = parent[walker]
    return walker
