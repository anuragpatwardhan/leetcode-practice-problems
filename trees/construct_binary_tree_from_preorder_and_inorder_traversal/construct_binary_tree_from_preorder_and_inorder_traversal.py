"""LeetCode 105. Construct Binary Tree from Preorder and Inorder Traversal."""

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


def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """Rebuild the tree that produced these two traversals."""
    if not preorder:
        return None

    # Iterative, matching the rest of trees/ -- a purely left- or right-leaning
    # input makes the recursive textbook solution (slice preorder/inorder around
    # the root's inorder index) recurse to the tree's height and slice the same
    # arrays over and over, O(n) work per node for O(n^2) overall.
    root = TreeNode(preorder[0])
    stack = [root]
    inorder_index = 0

    for i in range(1, len(preorder)):
        node = stack[-1]
        value = preorder[i]

        if node.val != inorder[inorder_index]:
            # The stack top has not been closed off by inorder yet, so the next
            # preorder value is still descending into its left subtree.
            node.left = TreeNode(value)
            stack.append(node.left)
        else:
            # The stack top (and possibly several ancestors above it) has just
            # been visited in inorder, meaning its whole left subtree -- and it
            # itself -- is done. Pop back to the last node whose right side is
            # still open; that is the true parent of the next value.
            while stack and stack[-1].val == inorder[inorder_index]:
                node = stack.pop()
                inorder_index += 1
            node.right = TreeNode(value)
            stack.append(node.right)

    return root
