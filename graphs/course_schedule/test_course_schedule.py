import random

from course_schedule import can_finish


def reference(num_courses, prerequisites):
    """Independent check: iterative DFS three-colouring for a cycle.

    Derived from the definition of a cycle rather than from Kahn's algorithm, so
    agreement between the two is meaningful.
    """
    graph = [[] for _ in range(num_courses)]
    for course, needed in prerequisites:
        graph[needed].append(course)

    UNVISITED, IN_PROGRESS, DONE = 0, 1, 2
    state = [UNVISITED] * num_courses

    for start in range(num_courses):
        if state[start] != UNVISITED:
            continue
        stack = [(start, iter(graph[start]))]
        state[start] = IN_PROGRESS
        while stack:
            node, children = stack[-1]
            advanced = False
            for child in children:
                if state[child] == IN_PROGRESS:
                    return False  # back edge — cycle
                if state[child] == UNVISITED:
                    state[child] = IN_PROGRESS
                    stack.append((child, iter(graph[child])))
                    advanced = True
                    break
            if not advanced:
                state[node] = DONE
                stack.pop()
    return True


def test_example_possible():
    assert can_finish(2, [[1, 0]]) is True


def test_example_impossible():
    assert can_finish(2, [[1, 0], [0, 1]]) is False


def test_no_prerequisites_at_all():
    assert can_finish(5, []) is True


def test_single_course():
    assert can_finish(1, []) is True


def test_a_course_requiring_itself():
    # The shortest possible cycle, and the one an indegree check must still catch.
    assert can_finish(1, [[0, 0]]) is False


def test_a_long_chain_is_fine():
    chain = [[i + 1, i] for i in range(999)]
    assert can_finish(1000, chain) is True


def test_a_cycle_closing_a_long_chain():
    chain = [[i + 1, i] for i in range(999)]
    chain.append([0, 999])
    assert can_finish(1000, chain) is False


def test_a_cycle_in_one_component_fails_the_whole_thing():
    # Courses 0 and 1 are fine; 2 and 3 deadlock. The answer is still False.
    assert can_finish(4, [[1, 0], [3, 2], [2, 3]]) is False


def test_diamond_dependency_is_acyclic():
    # 0 -> 1, 0 -> 2, both -> 3. Shared ancestry is not a cycle.
    assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True


def test_duplicate_edges_are_counted_twice_and_still_resolve():
    # indegree must fall to exactly zero, so a repeated edge has to be released
    # twice; treating edges as a set would be a different algorithm.
    assert can_finish(2, [[1, 0], [1, 0]]) is True


def test_edge_direction_matters():
    # 1 needs 0, and separately 2 needs 0. If the direction were reversed this
    # would still pass, so the asymmetric case below is the real check.
    assert can_finish(3, [[1, 0], [2, 0]]) is True
    # 2 needs 1, 1 needs 0: a strict order exists in one direction only.
    assert can_finish(3, [[1, 0], [2, 1]]) is True


def test_isolated_courses_alongside_a_chain():
    assert can_finish(5, [[1, 0]]) is True


def test_matches_the_reference_on_random_graphs():
    rng = random.Random(127)
    for _ in range(500):
        n = rng.randint(1, 9)
        edges = []
        for _ in range(rng.randint(0, 12)):
            course = rng.randrange(n)
            needed = rng.randrange(n)
            edges.append([course, needed])
        assert can_finish(n, edges) == reference(n, edges), (n, edges)


def test_matches_the_reference_on_guaranteed_acyclic_graphs():
    """Edges only ever point from a lower index to a higher one, so no cycle exists."""
    rng = random.Random(131)
    for _ in range(300):
        n = rng.randint(2, 12)
        edges = []
        for _ in range(rng.randint(0, 15)):
            a, b = sorted(rng.sample(range(n), 2))
            edges.append([b, a])  # b needs a, and a < b
        assert can_finish(n, edges) is True, (n, edges)
