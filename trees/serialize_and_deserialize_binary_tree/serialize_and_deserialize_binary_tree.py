"""LeetCode 297. Serialize and Deserialize Binary Tree."""

from collections import deque
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


_NULL_MARKER = "#"


def serialize(root: Optional[TreeNode]) -> str:
    """Encode a tree as a comma-separated, level-order string, gaps included."""
    if root is None:
        return ""

    # Breadth-first, like binary_tree_level_order_traversal, rather than the
    # usual recursive preorder-with-markers solution -- that recurses to the
    # tree's height, which a skewed input can push past Python's recursion
    # limit. BFS needs an explicit marker for every missing child (not just a
    # trailing gap) so deserialize can tell which parent each value belongs to.
    tokens = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            tokens.append(_NULL_MARKER)
            continue
        tokens.append(str(node.val))
        queue.append(node.left)
        queue.append(node.right)

    return ",".join(tokens)


def deserialize(data: str) -> Optional[TreeNode]:
    """Rebuild the tree that `serialize` encoded."""
    if not data:
        return None

    tokens = data.split(",")
    root = TreeNode(int(tokens[0]))
    queue = deque([root])
    index = 1

    while queue:
        node = queue.popleft()
        if tokens[index] != _NULL_MARKER:
            node.left = TreeNode(int(tokens[index]))
            queue.append(node.left)
        index += 1

        if tokens[index] != _NULL_MARKER:
            node.right = TreeNode(int(tokens[index]))
            queue.append(node.right)
        index += 1

    return root
