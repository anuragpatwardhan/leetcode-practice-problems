"""LeetCode 684. Redundant Connection."""

from typing import List


class DisjointSet:
    """Union-find over 1..n with path compression and union by size."""

    def __init__(self, size: int):
        self.parent = list(range(size + 1))
        self.size = [1] * (size + 1)

    def find(self, node: int) -> int:
        # Path compression, written iteratively. The recursive one-liner is
        # shorter, but its depth is the height of the tree, and the height is
        # only small *because* of this compression — an adversarial union order
        # before compression kicks in can still make it deep.
        root = node
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[node] != root:
            self.parent[node], node = root, self.parent[node]
        return root

    def union(self, a: int, b: int) -> bool:
        """Merge the two sets. False if they were already the same set."""
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        # Union by size keeps trees shallow. Without it, unioning in a chain
        # builds a linked list and find degrades to linear.
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        return True


def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """The edge that can be removed to leave a tree — the last one closing a cycle."""
    disjoint = DisjointSet(len(edges))
    redundant: List[int] = []

    for a, b in edges:
        # Both endpoints already connected means this edge closes a cycle: there
        # was a path between them before it existed.
        if not disjoint.union(a, b):
            redundant = [a, b]

    # "Last in input order" comes out for free. Any earlier edge of the cycle
    # was still joining two separate components when it was processed, so it
    # succeeded; only the edge that completes the cycle can fail. No tie-break
    # is needed. The loop runs to the end rather than returning early so that an
    # input with more than one extra edge still yields the last one.
    return redundant
