"""LeetCode 148. Sort List."""

from typing import Optional


class ListNode:
    """Singly linked list node, matching LeetCode's definition."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Sort a linked list ascending in O(n log n) time, relinking nodes in place."""
    if head is None or head.next is None:
        return head

    # Split at the middle. Starting fast one node ahead biases the split so the
    # left half is never longer than the right, which guarantees both halves are
    # strictly shorter than the input. With fast starting at head, a two-node
    # list would put both nodes on the left and recurse forever.
    slow, fast = head, head.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

    middle = slow.next
    slow.next = None

    return _merge(sort_list(head), sort_list(middle))


def _merge(left: Optional[ListNode], right: Optional[ListNode]) -> Optional[ListNode]:
    """Merge two sorted lists, preserving the order of equal values."""
    dummy = ListNode()
    tail = dummy

    while left is not None and right is not None:
        # <= rather than < keeps the merge stable: when values tie, the node from
        # the left half is emitted first, matching its original relative order.
        if left.val <= right.val:
            tail.next = left
            left = left.next
        else:
            tail.next = right
            right = right.next
        tail = tail.next

    # At most one side remains, and it is already sorted, so it attaches whole.
    tail.next = left if left is not None else right
    return dummy.next
