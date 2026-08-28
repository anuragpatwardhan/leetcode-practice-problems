import random

from redundant_connection import DisjointSet, find_redundant_connection


def leaves_a_tree(edges, removed):
    """Would removing `removed` leave a single acyclic connected component?

    Independent check: builds the graph without that edge and walks it with BFS,
    which is the definition of a tree spelled out rather than a second
    union-find. A tree on n nodes has n-1 edges and reaches every node.
    """
    from collections import deque

    remaining = [e for e in edges if e is not removed]
    nodes = {n for edge in edges for n in edge}
    if len(remaining) != len(nodes) - 1:
        return False

    adjacency = {n: [] for n in nodes}
    for a, b in remaining:
        adjacency[a].append(b)
        adjacency[b].append(a)

    start = next(iter(nodes))
    seen = {start}
    queue = deque([start])
    while queue:
        for neighbor in adjacency[queue.popleft()]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == len(nodes)


def make_tree_plus_one(rng, size):
    """A random tree on 1..size with one extra edge, shuffled into the list.

    Needs at least three nodes: on two, the only edge that could be added is the
    one the tree already has, and the problem states edges are not repeated.
    """
    assert size >= 3
    edges = []
    for node in range(2, size + 1):
        edges.append([rng.randint(1, node - 1), node])

    existing = {frozenset(e) for e in edges}
    while True:
        a, b = rng.randint(1, size), rng.randint(1, size)
        if a != b and frozenset((a, b)) not in existing:
            edges.append([a, b])
            break

    rng.shuffle(edges)
    return edges


def test_example_triangle():
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]


def test_example_larger():
    assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]


def test_the_extra_edge_is_the_last_one():
    assert find_redundant_connection([[1, 2], [2, 3], [1, 3]]) == [1, 3]


def test_the_extra_edge_is_in_the_middle():
    # The redundant edge is not simply the last edge in the list; the answer is
    # the last one that *closes a cycle*.
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3], [3, 4], [4, 5]]) == [2, 3]


def test_smallest_case():
    # Two nodes joined twice: the second edge is redundant.
    assert find_redundant_connection([[1, 2], [1, 2]]) == [1, 2]


def test_endpoints_are_reported_in_input_order():
    # [2, 3] and [3, 2] describe the same undirected edge, but the answer has to
    # match the input, so the pair cannot be normalised or sorted.
    assert find_redundant_connection([[1, 2], [1, 3], [3, 2]]) == [3, 2]


def test_a_long_chain_closed_at_the_ends():
    edges = [[i, i + 1] for i in range(1, 50)] + [[1, 50]]
    assert find_redundant_connection(edges) == [1, 50]


def test_star_with_one_extra_spoke_joined():
    # Every node hangs off node 1, then two leaves are joined to each other.
    edges = [[1, i] for i in range(2, 8)] + [[3, 6]]
    assert find_redundant_connection(edges) == [3, 6]


def test_result_actually_leaves_a_tree():
    edges = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
    answer = find_redundant_connection(edges)
    assert leaves_a_tree(edges, next(e for e in edges if e == answer))


def test_does_not_modify_the_input():
    edges = [[1, 2], [1, 3], [2, 3]]
    before = [e[:] for e in edges]
    find_redundant_connection(edges)
    assert edges == before


def test_matches_a_tree_check_on_random_graphs():
    rng = random.Random(684)
    for _ in range(400):
        size = rng.randint(3, 12)
        edges = make_tree_plus_one(rng, size)
        answer = find_redundant_connection(edges)

        # The answer must be one of the input edges, and removing it must leave
        # a tree. Which edge is "the" answer is not unique in general, so this
        # validates the property rather than comparing to a fixed edge.
        candidates = [e for e in edges if e == answer]
        assert candidates, (edges, answer)
        assert any(leaves_a_tree(edges, e) for e in candidates), (edges, answer)


def test_returns_the_last_valid_removal_in_input_order():
    rng = random.Random(685)
    for _ in range(200):
        size = rng.randint(3, 10)
        edges = make_tree_plus_one(rng, size)
        answer = find_redundant_connection(edges)

        valid = [i for i, e in enumerate(edges) if leaves_a_tree(edges, e)]
        last = edges[valid[-1]]
        assert answer == last, (edges, answer, last)


class TestDisjointSet:
    """The union-find itself, since it is the reusable part."""

    def test_starts_with_every_node_separate(self):
        ds = DisjointSet(3)
        assert ds.find(1) != ds.find(2)

    def test_union_joins_two_sets(self):
        ds = DisjointSet(3)
        assert ds.union(1, 2) is True
        assert ds.find(1) == ds.find(2)

    def test_union_of_an_existing_pair_reports_false(self):
        ds = DisjointSet(3)
        ds.union(1, 2)
        assert ds.union(1, 2) is False

    def test_transitivity(self):
        ds = DisjointSet(4)
        ds.union(1, 2)
        ds.union(2, 3)
        assert ds.find(1) == ds.find(3)
        assert ds.union(1, 3) is False

    def test_separate_components_stay_separate(self):
        ds = DisjointSet(4)
        ds.union(1, 2)
        ds.union(3, 4)
        assert ds.find(1) != ds.find(3)

    def test_a_node_is_its_own_root(self):
        assert DisjointSet(1).find(1) == 1

    def test_deep_chain_stays_fast_and_correct(self):
        # Unioning in strict order is the shape that degrades an implementation
        # without union by size into a linked list; find would then be linear
        # and the iterative walk is what keeps it from also being a deep
        # recursion.
        size = 50_000
        ds = DisjointSet(size)
        for node in range(1, size):
            ds.union(node, node + 1)
        assert ds.find(1) == ds.find(size)

    def test_path_compression_flattens_the_tree(self):
        size = 1_000
        ds = DisjointSet(size)
        for node in range(1, size):
            ds.union(node, node + 1)
        root = ds.find(size)
        # After one find from the deepest node, everything on that path points
        # straight at the root.
        ds.find(1)
        assert ds.parent[1] == root
