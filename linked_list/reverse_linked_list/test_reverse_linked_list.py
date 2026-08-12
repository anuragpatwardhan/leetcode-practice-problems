from reverse_linked_list import ListNode, reverse_list


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


def test_helpers_round_trip():
    assert to_list(build([1, 2, 3])) == [1, 2, 3]


def test_example():
    assert to_list(reverse_list(build([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]


def test_two_nodes():
    assert to_list(reverse_list(build([1, 2]))) == [2, 1]


def test_single_node():
    assert to_list(reverse_list(build([1]))) == [1]


def test_empty_list():
    assert reverse_list(build([])) is None


def test_duplicate_values():
    assert to_list(reverse_list(build([1, 1, 2, 1]))) == [1, 2, 1, 1]


def test_the_original_head_becomes_the_tail():
    head = build([1, 2, 3])
    reversed_head = reverse_list(head)
    assert head.next is None
    assert reversed_head.val == 3


def test_nodes_are_relinked_not_recreated():
    head = build([1, 2, 3, 4])
    originals = set()
    node = head
    while node is not None:
        originals.add(id(node))
        node = node.next

    node = reverse_list(head)
    while node is not None:
        assert id(node) in originals
        node = node.next


def test_reversing_twice_restores_the_original_order():
    values = [1, 2, 3, 4, 5]
    assert to_list(reverse_list(reverse_list(build(values)))) == values


def test_every_length_up_to_twenty():
    for length in range(0, 21):
        values = list(range(length))
        assert to_list(reverse_list(build(values))) == values[::-1], length
