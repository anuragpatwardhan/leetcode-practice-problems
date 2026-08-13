"""LeetCode 102. Binary Tree Level Order Traversal."""

from collections import deque
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


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """Return node values level by level, left to right."""
    if root is None:
        return []

    levels: List[List[int]] = []
    frontier = deque([root])

    while frontier:
        # Snapshot the width before draining. Children are appended during the
        # loop, so without this the queue would grow underneath the iteration
        # and two levels would merge into one row.
        width = len(frontier)
        row: List[int] = []

        for _ in range(width):
            node = frontier.popleft()
            row.append(node.val)
            # Enqueue in left-then-right order so each row reads left to right.
            if node.left is not None:
                frontier.append(node.left)
            if node.right is not None:
                frontier.append(node.right)

        levels.append(row)

    return levels
