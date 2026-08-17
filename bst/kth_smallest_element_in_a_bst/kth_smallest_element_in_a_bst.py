"""LeetCode 230. Kth Smallest Element in a BST."""

from typing import List, Optional


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


def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """Return the kth smallest value (1-indexed) in a binary search tree."""
    # An in-order walk of a BST yields values in ascending order, so the kth
    # value it emits is the answer — no sorting and no full traversal needed.
    # Iterative rather than recursive: a BST built from sorted inserts is a
    # list in disguise, and its height can exceed Python's recursion limit.
    stack: List[TreeNode] = []
    node = root

    while node is not None or stack:
        # Descend as far left as possible; the deepest left node is the
        # smallest value not yet visited.
        while node is not None:
            stack.append(node)
            node = node.left

        node = stack.pop()
        k -= 1
        if k == 0:
            # Stop the moment the count is reached. The right subtree and every
            # remaining ancestor are never touched, which is what keeps this
            # cheaper than a full traversal.
            return node.val

        node = node.right

    raise ValueError(f"k is larger than the number of nodes in the tree")
