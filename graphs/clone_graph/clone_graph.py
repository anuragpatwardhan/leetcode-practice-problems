"""LeetCode 133. Clone Graph."""

from collections import deque
from typing import Dict, List, Optional


class Node:
    """An undirected graph node, defined here so the problem stays self-contained."""

    def __init__(self, val: int = 0, neighbors: Optional[List["Node"]] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node: Optional[Node]) -> Optional[Node]:
    """Deep copy a connected undirected graph, sharing no node with the original."""
    if node is None:
        return None

    # The map is the whole solution. It answers "have I already made a copy of
    # this node?", which is what stops a cycle from cloning forever, and it is
    # also how two clones end up pointing at the *same* neighbour copy instead of
    # two equal ones.
    clones: Dict[Node, Node] = {node: Node(node.val)}

    # BFS rather than recursion: depth here is the length of the graph, and a
    # 10,000-node chain is a legal input that would exhaust the stack.
    queue = deque([node])

    while queue:
        original = queue.popleft()
        copy = clones[original]

        for neighbor in original.neighbors:
            if neighbor not in clones:
                # Registered before it is queued, not after. Enqueueing first and
                # registering on the way out lets a node already in the queue be
                # discovered again through another edge and cloned twice, which
                # splits the graph into duplicates that never converge.
                clones[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            copy.neighbors.append(clones[neighbor])

    return clones[node]
