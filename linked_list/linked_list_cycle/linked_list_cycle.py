"""LeetCode 141. Linked List Cycle."""

from typing import Optional


class ListNode:
    """Singly linked list node, matching LeetCode's definition."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def has_cycle(head: Optional[ListNode]) -> bool:
    """True when following ``next`` from ``head`` never reaches the end."""
    # Floyd's tortoise and hare. Both start at the head; slow advances one node
    # per step and fast two, so the gap between them grows by exactly one each
    # step. Inside a cycle of length L that gap is taken modulo L, which means it
    # eventually hits zero — so if a cycle exists the two *must* land on the same
    # node rather than merely stepping past each other.
    slow = fast = head

    # fast is the one that runs off the end, so both it and its next must be
    # checked before dereferencing twice.
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True

    # fast reached the end, so the list is finite and has no cycle.
    return False
