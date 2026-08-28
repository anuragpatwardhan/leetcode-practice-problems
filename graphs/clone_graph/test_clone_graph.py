import random
import sys
from collections import deque

from clone_graph import Node, clone_graph


def build(adjacency):
    """Build a graph from {val: [neighbour vals]}, returning {val: Node}."""
    nodes = {val: Node(val) for val in adjacency}
    for val, neighbors in adjacency.items():
        nodes[val].neighbors = [nodes[n] for n in neighbors]
    return nodes


def collect(node):
    """Every node object reachable from `node`, in discovery order."""
    if node is None:
        return []
    seen, order, queue = {id(node)}, [node], deque([node])
    while queue:
        current = queue.popleft()
        for neighbor in current.neighbors:
            if id(neighbor) not in seen:
                seen.add(id(neighbor))
                order.append(neighbor)
                queue.append(neighbor)
    return order


def signature(node):
    """A structural fingerprint that ignores object identity.

    Nodes are numbered by BFS discovery order, so two graphs match only if they
    have the same shape reached the same way — not merely the same values.
    Neighbour order is preserved rather than sorted, since it is observable.
    """
    order = collect(node)
    index = {id(n): i for i, n in enumerate(order)}
    return [(n.val, [index[id(x)] for x in n.neighbors]) for n in order]


def test_returns_none_for_none():
    assert clone_graph(None) is None


def test_single_node_with_no_neighbours():
    original = Node(1)
    copy = clone_graph(original)
    assert copy.val == 1
    assert copy.neighbors == []
    assert copy is not original


def test_two_connected_nodes():
    nodes = build({1: [2], 2: [1]})
    copy = clone_graph(nodes[1])
    assert signature(copy) == signature(nodes[1])


def test_the_square_from_the_problem():
    nodes = build({1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]})
    copy = clone_graph(nodes[1])
    assert signature(copy) == signature(nodes[1])


def test_shares_no_node_with_the_original():
    # The point of the exercise. A shallow copy passes every structural check
    # above while leaving the caller's graph wired into the result.
    nodes = build({1: [2, 3], 2: [1], 3: [1]})
    originals = {id(n) for n in collect(nodes[1])}
    for node in collect(clone_graph(nodes[1])):
        assert id(node) not in originals


def test_leaves_the_original_untouched():
    nodes = build({1: [2, 3], 2: [1], 3: [1]})
    before = signature(nodes[1])
    clone_graph(nodes[1])
    assert signature(nodes[1]) == before


def test_original_neighbour_lists_are_not_appended_to():
    # Writing into `original.neighbors` instead of `copy.neighbors` is a one
    # character slip that still returns a plausible-looking graph.
    nodes = build({1: [2], 2: [1]})
    clone_graph(nodes[1])
    assert len(nodes[1].neighbors) == 1
    assert len(nodes[2].neighbors) == 1


def test_a_cycle_terminates():
    # Without the "have I cloned this already?" map, following 1 -> 2 -> 1 never
    # ends. This test hangs rather than fails if that map is missing.
    nodes = build({1: [2], 2: [3], 3: [1]})
    assert signature(clone_graph(nodes[1])) == signature(nodes[1])


def test_self_loop():
    node = Node(1)
    node.neighbors = [node]
    copy = clone_graph(node)
    # The clone must loop to itself, not back to the original.
    assert copy.neighbors == [copy]


def test_shared_neighbour_is_cloned_once():
    # A diamond: 2 and 3 both point at 4. If 4 is cloned twice the copies never
    # converge and the graph quietly becomes a tree.
    nodes = build({1: [2, 3], 2: [1, 4], 3: [1, 4], 4: [2, 3]})
    copy = clone_graph(nodes[1])
    assert len(collect(copy)) == 4
    from_two, from_three = copy.neighbors[0].neighbors[1], copy.neighbors[1].neighbors[1]
    assert from_two is from_three


def test_neighbour_order_is_preserved():
    # Order is part of the returned structure; a set-based implementation loses
    # it and the signature check catches that here.
    nodes = build({1: [2, 3, 4], 2: [1], 3: [1], 4: [1]})
    copy = clone_graph(nodes[1])
    assert [n.val for n in copy.neighbors] == [2, 3, 4]


def test_duplicate_edges_are_kept():
    # Two edges between the same pair is not the same graph as one, and
    # de-duplicating through the clone map would silently collapse them.
    nodes = build({1: [2, 2], 2: [1, 1]})
    copy = clone_graph(nodes[1])
    assert len(copy.neighbors) == 2
    assert copy.neighbors[0] is copy.neighbors[1]


def test_repeated_values_are_treated_as_distinct_nodes():
    # LeetCode guarantees unique values, so keying the clone map by `val` passes
    # every official case. It is still the wrong key: identity is what matters.
    a, b = Node(7), Node(7)
    a.neighbors = [b]
    b.neighbors = [a]
    copy = clone_graph(a)
    assert len(collect(copy)) == 2
    assert copy.neighbors[0] is not copy


def test_long_chain_does_not_hit_the_recursion_limit():
    # 10,000 nodes in a line. Recursive cloning needs a frame per node; the
    # default limit is 1,000.
    size = 10_000
    nodes = [Node(i) for i in range(size)]
    for i in range(size - 1):
        nodes[i].neighbors.append(nodes[i + 1])
        nodes[i + 1].neighbors.append(nodes[i])

    assert sys.getrecursionlimit() < size
    copy = clone_graph(nodes[0])
    assert len(collect(copy)) == size


def test_dense_graph():
    # Complete graph on 40 nodes: every node reaches every other, so the map is
    # hit far more often than it misses.
    size = 40
    nodes = [Node(i) for i in range(size)]
    for i in range(size):
        nodes[i].neighbors = [nodes[j] for j in range(size) if j != i]
    copy = clone_graph(nodes[0])
    assert len(collect(copy)) == size
    assert all(len(n.neighbors) == size - 1 for n in collect(copy))


def test_matches_the_original_on_random_connected_graphs():
    rng = random.Random(133)
    for _ in range(300):
        size = rng.randint(1, 10)
        nodes = [Node(i) for i in range(size)]
        # Build a spanning tree first so the graph is connected — an unconnected
        # one is outside the problem, and the clone could not reach it anyway.
        for i in range(1, size):
            parent = nodes[rng.randrange(i)]
            parent.neighbors.append(nodes[i])
            nodes[i].neighbors.append(parent)
        # Then sprinkle extra edges to create cycles.
        for _ in range(rng.randint(0, size)):
            a, b = rng.randrange(size), rng.randrange(size)
            if a != b:
                nodes[a].neighbors.append(nodes[b])
                nodes[b].neighbors.append(nodes[a])

        copy = clone_graph(nodes[0])
        assert signature(copy) == signature(nodes[0])

        originals = {id(n) for n in collect(nodes[0])}
        assert not any(id(n) in originals for n in collect(copy))
