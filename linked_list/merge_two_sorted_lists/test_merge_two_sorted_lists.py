import random

from merge_two_sorted_lists import ListNode, merge_two_lists


def build(values):
    head = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def to_list(head):
    values = []
    seen = set()
    while head is not None:
        assert id(head) not in seen, "cycle in the resulting list"
        seen.add(id(head))
        values.append(head.val)
        head = head.next
    return values


def test_example():
    assert to_list(merge_two_lists(build([1, 2, 4]), build([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]


def test_both_empty():
    assert merge_two_lists(None, None) is None


def test_first_empty_returns_the_second():
    assert to_list(merge_two_lists(None, build([1, 2]))) == [1, 2]


def test_second_empty_returns_the_first():
    assert to_list(merge_two_lists(build([1, 2]), None)) == [1, 2]


def test_disjoint_ranges():
    assert to_list(merge_two_lists(build([1, 2, 3]), build([7, 8]))) == [1, 2, 3, 7, 8]


def test_one_list_exhausts_first():
    # The leftover tail attaches whole rather than being copied node by node.
    assert to_list(merge_two_lists(build([1]), build([2, 3, 4, 5]))) == [1, 2, 3, 4, 5]


def test_all_values_equal():
    assert to_list(merge_two_lists(build([2, 2]), build([2, 2]))) == [2, 2, 2, 2]


def test_negative_values():
    assert to_list(merge_two_lists(build([-5, -1]), build([-3, 0]))) == [-5, -3, -1, 0]


def test_merge_is_stable_on_ties():
    # With equal values the node from the first list must come first. Marking
    # the nodes by identity is the only way to observe it.
    first = build([1])
    second = build([1])
    merged = merge_two_lists(first, second)
    assert merged is first
    assert merged.next is second


def test_nodes_are_spliced_not_recreated():
    a, b = build([1, 3]), build([2, 4])
    originals = set()
    for head in (a, b):
        node = head
        while node is not None:
            originals.add(id(node))
            node = node.next

    node = merge_two_lists(a, b)
    while node is not None:
        assert id(node) in originals
        node = node.next


def test_matches_sorted_on_random_inputs():
    rng = random.Random(211)
    for _ in range(400):
        left = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 12)))
        right = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 12)))
        merged = merge_two_lists(build(left), build(right))
        assert to_list(merged) == sorted(left + right), (left, right)
