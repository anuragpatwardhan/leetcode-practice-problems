"""LeetCode 21. Merge Two Sorted Lists."""

from typing import Optional


class ListNode:
    """Singly linked list node, matching LeetCode's definition."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def merge_two_lists(
    list1: Optional[ListNode], list2: Optional[ListNode]
) -> Optional[ListNode]:
    """Splice two sorted lists into one sorted list, reusing the nodes."""
    # A dummy head removes the "is this the first node?" branch from the loop:
    # every node is appended the same way, and the answer is dummy.next.
    dummy = ListNode()
    tail = dummy

    while list1 is not None and list2 is not None:
        # <= rather than < keeps the merge stable — on a tie the node from the
        # first list is emitted first, preserving the original relative order.
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    # Exactly one list can still have nodes, and it is already sorted, so it
    # attaches whole rather than being walked node by node.
    tail.next = list1 if list1 is not None else list2

    return dummy.next
