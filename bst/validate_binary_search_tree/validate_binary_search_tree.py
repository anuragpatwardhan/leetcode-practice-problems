"""LeetCode 98. Validate Binary Search Tree."""

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


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """True when every node lies strictly between its permitted bounds."""
    # Iterative to avoid a recursion limit on a degenerate, list-shaped tree.
    # Each frame carries the open interval the subtree must fall inside.
    stack: list[tuple[Optional[TreeNode], float, float]] = [(root, float("-inf"), float("inf"))]

    while stack:
        node, low, high = stack.pop()
        if node is None:
            continue

        # Strict comparisons: a BST here holds no duplicates, so a value equal to
        # an ancestor's is invalid.
        if not (low < node.val < high):
            return False

        # The bound tightens rather than resetting. Going left caps everything
        # below by this node's value, so a deep left descendant still cannot
        # exceed an ancestor further up -- which is what a parent-only check
        # misses in trees like [5, 1, 4, None, None, 3, 6].
        stack.append((node.left, low, node.val))
        stack.append((node.right, node.val, high))

    return True
