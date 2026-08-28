import random

from course_schedule_ii import find_order


def is_acyclic(num_courses, prerequisites):
    """Independent feasibility check: iterative DFS three-colouring.

    Derived from the definition of a cycle rather than from Kahn's algorithm, so
    it can disagree with the solution about whether an order should exist.
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
                    return False
                if state[child] == UNVISITED:
                    state[child] = IN_PROGRESS
                    stack.append((child, iter(graph[child])))
                    advanced = True
                    break
            if not advanced:
                state[node] = DONE
                stack.pop()
    return True


def assert_valid_order(order, num_courses, prerequisites):
    """Validate an answer rather than recompute it.

    Many orders are correct, so comparing against one particular answer would be
    wrong. What matters is that this one is a permutation of the courses and
    respects every prerequisite.
    """
    assert sorted(order) == list(range(num_courses)), order
    position = {course: i for i, course in enumerate(order)}
    for course, needed in prerequisites:
        assert position[needed] < position[course], (order, course, needed)


def test_example_two_courses():
    assert find_order(2, [[1, 0]]) == [0, 1]


def test_example_four_courses():
    order = find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert_valid_order(order, 4, [[1, 0], [2, 0], [3, 1], [3, 2]])


def test_no_prerequisites_gives_every_course():
    order = find_order(3, [])
    assert sorted(order) == [0, 1, 2]


def test_impossible_returns_empty():
    assert find_order(2, [[1, 0], [0, 1]]) == []


def test_self_dependency_is_impossible():
    assert find_order(1, [[0, 0]]) == []


def test_zero_courses():
    # The one input where [] is the correct answer rather than a refusal. Both
    # readings agree on the value, but a guard that special-cases "empty means
    # impossible" earlier in the function would get here by the wrong route.
    assert find_order(0, []) == []


def test_single_course():
    assert find_order(1, []) == [0]


def test_a_cycle_off_to_one_side_still_blocks_everything():
    # Courses 0 and 1 are perfectly schedulable; 2 and 3 deadlock. There is no
    # order for *all* four, so the answer is empty rather than the two that work.
    assert find_order(4, [[1, 0], [3, 2], [2, 3]]) == []


def test_partial_order_is_not_returned_on_failure():
    # The dangerous failure mode: an order that looks fine and is missing the
    # courses trapped in the cycle.
    assert find_order(5, [[1, 0], [2, 1], [4, 3], [3, 4]]) == []


def test_long_chain_is_forced_into_one_order():
    # Each course needs the previous one, so exactly one order is valid.
    prerequisites = [[i, i - 1] for i in range(1, 50)]
    assert find_order(50, prerequisites) == list(range(50))


def test_duplicate_prerequisites_are_counted_twice():
    # Indegree must fall to exactly zero, so a repeated edge has to be released
    # twice. De-duplicating into a set is a different algorithm that would leave
    # course 1 at indegree 1 forever and wrongly report a cycle.
    order = find_order(2, [[1, 0], [1, 0]])
    assert order == [0, 1]


def test_disconnected_components_all_appear():
    order = find_order(6, [[1, 0], [3, 2], [5, 4]])
    assert_valid_order(order, 6, [[1, 0], [3, 2], [5, 4]])


def test_direction_is_not_reversed():
    # A reversed graph is still acyclic, so LeetCode 207's answer is unchanged by
    # this bug. Here it produces a valid-looking order that is exactly backwards,
    # which only an asymmetric chain exposes.
    assert find_order(3, [[1, 0], [2, 1]]) == [0, 1, 2]


def test_matches_feasibility_on_random_graphs():
    rng = random.Random(210)
    for _ in range(500):
        num_courses = rng.randint(1, 8)
        prerequisites = [
            [rng.randrange(num_courses), rng.randrange(num_courses)]
            for _ in range(rng.randint(0, 12))
        ]
        order = find_order(num_courses, prerequisites)
        if is_acyclic(num_courses, prerequisites):
            assert_valid_order(order, num_courses, prerequisites)
        else:
            assert order == [], (num_courses, prerequisites)


def test_valid_on_random_acyclic_graphs():
    # Edges only ever point from a lower index to a higher one, so these are
    # acyclic by construction and an order must always exist.
    rng = random.Random(211)
    for _ in range(300):
        num_courses = rng.randint(2, 10)
        prerequisites = []
        for course in range(num_courses):
            for needed in range(course):
                if rng.random() < 0.3:
                    prerequisites.append([course, needed])
        order = find_order(num_courses, prerequisites)
        assert_valid_order(order, num_courses, prerequisites)
