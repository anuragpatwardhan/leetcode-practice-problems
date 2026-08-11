"""LeetCode 25. Reverse Nodes in k-Group."""

from typing import Optional


class ListNode:
    """Singly linked list node, matching LeetCode's definition."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """Reverse every consecutive group of ``k`` nodes, leaving any short tail as is.

    Relinks in place using constant extra space; no values are copied.
    """
    if head is None or k <= 1:
        return head

    # A dummy in front removes the special case for the very first group, which
    # is the only one that would otherwise change the caller's head pointer.
    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        # Walk k nodes ahead before touching anything. A group shorter than k is
        # left in its original order, so it must not be partially reversed.
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next

        group_next = kth.next

        # Reverse the group by pointing each node at its predecessor. Seeding
        # `prev` with group_next rather than None joins the group's new tail to
        # the rest of the list in the same sweep.
        prev, current = group_next, group_prev.next
        while current is not group_next:
            following = current.next
            current.next = prev
            prev = current
            current = following

        # group_prev.next still refers to the node that led the group and now
        # trails it, so it becomes the anchor for the next group.
        new_group_prev = group_prev.next
        group_prev.next = kth
        group_prev = new_group_prev
