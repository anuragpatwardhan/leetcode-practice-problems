from reorder_list import ListNode, reorder_list


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


def expected(values):
    """Take from the front and back alternately."""
    out = []
    left, right = 0, len(values) - 1
    while left < right:
        out.append(values[left])
        out.append(values[right])
        left += 1
        right -= 1
    if left == right:
        out.append(values[left])
    return out


def test_helpers_agree_on_small_cases():
    assert expected([1, 2, 3, 4]) == [1, 4, 2, 3]
    assert expected([1, 2, 3, 4, 5]) == [1, 5, 2, 4, 3]


def test_example_even_length():
    head = build([1, 2, 3, 4])
    reorder_list(head)
    assert to_list(head) == [1, 4, 2, 3]


def test_example_odd_length():
    head = build([1, 2, 3, 4, 5])
    reorder_list(head)
    assert to_list(head) == [1, 5, 2, 4, 3]


def test_empty_list_is_left_alone():
    assert reorder_list(build([])) is None


def test_single_node():
    head = build([1])
    reorder_list(head)
    assert to_list(head) == [1]


def test_two_nodes_are_unchanged():
    head = build([1, 2])
    reorder_list(head)
    assert to_list(head) == [1, 2]


def test_three_nodes_put_the_middle_last():
    head = build([1, 2, 3])
    reorder_list(head)
    assert to_list(head) == [1, 3, 2]


def test_returns_none_rather_than_the_head():
    # The problem reorders in place; returning a head would be the wrong shape.
    assert reorder_list(build([1, 2, 3, 4])) is None


def test_duplicate_values():
    head = build([1, 1, 2, 2])
    reorder_list(head)
    assert to_list(head) == [1, 2, 1, 2]


def test_nodes_are_relinked_not_recreated():
    head = build([1, 2, 3, 4, 5])
    originals = set()
    node = head
    while node is not None:
        originals.add(id(node))
        node = node.next

    reorder_list(head)

    node = head
    while node is not None:
        assert id(node) in originals
        node = node.next


def test_no_node_is_lost_or_duplicated():
    for length in range(1, 25):
        values = list(range(length))
        head = build(values)
        reorder_list(head)
        assert sorted(to_list(head)) == values, length


def test_every_length_up_to_twenty_five():
    for length in range(0, 26):
        values = list(range(1, length + 1))
        head = build(values)
        reorder_list(head)
        assert to_list(head) == expected(values), length
