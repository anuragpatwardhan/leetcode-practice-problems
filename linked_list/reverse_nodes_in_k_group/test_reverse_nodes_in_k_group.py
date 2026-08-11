from reverse_nodes_in_k_group import ListNode, reverse_k_group


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


def expected(values, k):
    """Reverse each full chunk of k, leaving a short final chunk alone."""
    if k <= 1:
        return list(values)
    result = []
    for start in range(0, len(values), k):
        chunk = values[start : start + k]
        result += chunk[::-1] if len(chunk) == k else chunk
    return result


def test_helpers_round_trip():
    assert to_list(build([1, 2, 3])) == [1, 2, 3]
    assert to_list(build([])) == []


def test_example_k_two():
    assert to_list(reverse_k_group(build([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]


def test_example_k_three():
    assert to_list(reverse_k_group(build([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]


def test_empty_list():
    assert reverse_k_group(build([]), 3) is None


def test_k_of_one_leaves_the_list_untouched():
    assert to_list(reverse_k_group(build([1, 2, 3]), 1)) == [1, 2, 3]


def test_k_equal_to_the_length_reverses_everything():
    assert to_list(reverse_k_group(build([1, 2, 3, 4]), 4)) == [4, 3, 2, 1]


def test_k_larger_than_the_list_changes_nothing():
    # A group shorter than k keeps its original order.
    assert to_list(reverse_k_group(build([1, 2, 3]), 5)) == [1, 2, 3]


def test_trailing_partial_group_is_left_in_order():
    assert to_list(reverse_k_group(build([1, 2, 3, 4, 5, 6, 7]), 3)) == [3, 2, 1, 6, 5, 4, 7]


def test_exact_multiple_has_no_leftover():
    assert to_list(reverse_k_group(build([1, 2, 3, 4, 5, 6]), 3)) == [3, 2, 1, 6, 5, 4]


def test_single_node():
    assert to_list(reverse_k_group(build([1]), 2)) == [1]


def test_nodes_are_relinked_not_recreated():
    # Reversal must move pointers rather than copy values into fresh nodes.
    head = build([1, 2, 3, 4])
    originals = set()
    node = head
    while node is not None:
        originals.add(id(node))
        node = node.next

    result = reverse_k_group(head, 2)
    node = result
    while node is not None:
        assert id(node) in originals
        node = node.next


def test_matches_the_reference_for_every_length_and_k():
    for length in range(0, 13):
        values = list(range(1, length + 1))
        for k in range(1, length + 3):
            assert to_list(reverse_k_group(build(values), k)) == expected(values, k), (length, k)
