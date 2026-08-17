"""LeetCode 124. Binary Tree Maximum Path Sum."""

from typing import Dict, List, Optional, Tuple


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


def max_path_sum(root: Optional[TreeNode]) -> int:
    """Largest sum along any path; a path need not pass through the root."""
    if root is None:
        raise ValueError("the tree must contain at least one node")

    best = float("-inf")
    # Downward gain for each node: the best sum obtainable by starting at that
    # node and descending, which is what a parent can actually reuse.
    gain: Dict[TreeNode, int] = {}

    # Post-order, iteratively: both children must be resolved before their
    # parent. A recursive version is shorter but a degenerate tree is a chain,
    # and its depth would exceed Python's recursion limit.
    stack: List[Tuple[Optional[TreeNode], bool]] = [(root, False)]

    while stack:
        node, resolved = stack.pop()
        if node is None:
            continue

        if not resolved:
            stack.append((node, True))
            stack.append((node.left, False))
            stack.append((node.right, False))
            continue

        # Clamping at zero is the heart of it: a subtree that sums negative is
        # simply not taken. That is why a missing child and a harmful child are
        # worth the same — nothing.
        left = max(gain.get(node.left, 0), 0)
        right = max(gain.get(node.right, 0), 0)

        # The answer may *split* here, using both children. This path turns at
        # this node, so it can never be extended upward.
        best = max(best, node.val + left + right)

        # What the parent may reuse is only a straight descent, so at most one
        # child. Returning the split sum instead is the classic bug: it would
        # let a path fork twice and stop being a path.
        gain[node] = node.val + max(left, right)

    return int(best)
