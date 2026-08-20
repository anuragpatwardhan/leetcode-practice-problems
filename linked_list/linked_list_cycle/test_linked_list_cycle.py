import random

from linked_list_cycle import ListNode, has_cycle


def build(values, cycle_at=None):
    """Build a list, optionally linking the tail back to index ``cycle_at``."""
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if cycle_at is not None:
        nodes[-1].next = nodes[cycle_at]
    return nodes[0]


def reference(head):
    """Independent oracle: remember every node seen, by identity."""
    seen = set()
    node = head
    while node is not None:
        if id(node) in seen:
            return True
        seen.add(id(node))
        node = node.next
    return False


def test_example_with_cycle():
    assert has_cycle(build([3, 2, 0, -4], cycle_at=1)) is True


def test_example_two_node_cycle():
    assert has_cycle(build([1, 2], cycle_at=0)) is True


def test_example_single_node_no_cycle():
    assert has_cycle(build([1])) is False


def test_empty_list():
    assert has_cycle(None) is False


def test_single_node_pointing_at_itself():
    # The tightest possible cycle, and the case where slow and fast start equal.
    assert has_cycle(build([1], cycle_at=0)) is True


def test_two_nodes_no_cycle():
    assert has_cycle(build([1, 2])) is False


def test_long_list_no_cycle():
    assert has_cycle(build(list(range(1000)))) is False


def test_cycle_back_to_the_head():
    assert has_cycle(build(list(range(10)), cycle_at=0)) is True


def test_cycle_that_is_only_the_final_node():
    # A one-node loop at the tail: fast has to enter it and lap slow.
    assert has_cycle(build(list(range(10)), cycle_at=9)) is True


def test_long_tail_before_a_short_cycle():
    assert has_cycle(build(list(range(500)), cycle_at=498)) is True


def test_duplicate_values_are_not_a_cycle():
    # Detection must be by node identity, not by value. Every value here is the
    # same, and the list is still finite.
    assert has_cycle(build([7] * 50)) is False


def test_matches_the_reference_on_random_lists():
    rng = random.Random(229)
    for _ in range(500):
        size = rng.randint(0, 30)
        values = [rng.randint(-9, 9) for _ in range(size)]
        cycle_at = rng.choice([None] + list(range(size))) if size else None
        head = build(values, cycle_at)
        assert has_cycle(head) == reference(head), (values, cycle_at)


def test_every_cycle_position_is_found():
    for size in range(1, 15):
        for cycle_at in range(size):
            assert has_cycle(build(list(range(size)), cycle_at)) is True, (size, cycle_at)


def test_no_cycle_at_every_length():
    for size in range(0, 15):
        assert has_cycle(build(list(range(size)))) is False, size
