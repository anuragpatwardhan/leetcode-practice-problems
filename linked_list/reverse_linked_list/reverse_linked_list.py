"""LeetCode 206. Reverse Linked List."""

from typing import Optional


class ListNode:
    """Singly linked list node, matching LeetCode's definition."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse the list in place and return the new head."""
    previous: Optional[ListNode] = None
    current = head

    while current is not None:
        # Save the next node before overwriting the pointer, otherwise the rest
        # of the list becomes unreachable and the loop cannot advance.
        following = current.next
        current.next = previous
        previous = current
        current = following

    # The loop ends with current at None, so previous holds the last node
    # visited, which is the original tail and the new head.
    return previous
