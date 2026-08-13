import random

from sort_list import ListNode, sort_list


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
    assert to_list(sort_list(build([4, 2, 1, 3]))) == [1, 2, 3, 4]


def test_example_with_negatives_and_duplicates():
    assert to_list(sort_list(build([-1, 5, 3, 4, 0]))) == [-1, 0, 3, 4, 5]


def test_empty_list():
    assert sort_list(build([])) is None


def test_single_node():
    assert to_list(sort_list(build([7]))) == [7]


def test_two_nodes_already_ordered():
    assert to_list(sort_list(build([1, 2]))) == [1, 2]


def test_two_nodes_reversed():
    # The case that loops forever if the split does not guarantee progress.
    assert to_list(sort_list(build([2, 1]))) == [1, 2]


def test_already_sorted_input():
    assert to_list(sort_list(build([1, 2, 3, 4, 5]))) == [1, 2, 3, 4, 5]


def test_reverse_sorted_input():
    assert to_list(sort_list(build([5, 4, 3, 2, 1]))) == [1, 2, 3, 4, 5]


def test_all_equal_values():
    assert to_list(sort_list(build([3, 3, 3, 3]))) == [3, 3, 3, 3]


def test_duplicates_are_kept_not_collapsed():
    assert to_list(sort_list(build([2, 1, 2, 1]))) == [1, 1, 2, 2]


def test_nodes_are_relinked_not_recreated():
    head = build([4, 2, 1, 3])
    originals = set()
    node = head
    while node is not None:
        originals.add(id(node))
        node = node.next

    node = sort_list(head)
    while node is not None:
        assert id(node) in originals
        node = node.next


def test_every_length_up_to_thirty_against_sorted():
    rng = random.Random(61)
    for length in range(0, 31):
        values = [rng.randint(-20, 20) for _ in range(length)]
        assert to_list(sort_list(build(values))) == sorted(values), values


def test_matches_sorted_on_random_inputs():
    rng = random.Random(67)
    for _ in range(300):
        values = [rng.randint(-50, 50) for _ in range(rng.randint(0, 60))]
        assert to_list(sort_list(build(values))) == sorted(values), values


def test_handles_a_large_list_without_recursion_errors():
    rng = random.Random(71)
    values = [rng.randint(0, 10_000) for _ in range(5_000)]
    assert to_list(sort_list(build(values))) == sorted(values)
