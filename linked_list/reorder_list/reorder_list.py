"""LeetCode 143. Reorder List."""

from typing import Optional


class ListNode:
    """Singly linked list node, matching LeetCode's definition."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def reorder_list(head: Optional[ListNode]) -> None:
    """Weave the list into L0 → Ln → L1 → Ln-1 → … in place.

    Reorders by relinking nodes; no values are copied and nothing is returned.
    """
    if head is None or head.next is None:
        return

    # 1. Find the end of the first half. Advancing fast by two only while both
    #    fast.next and fast.next.next exist leaves slow on the last node of the
    #    first half, so an odd-length list keeps the extra node on the left --
    #    which is what puts the middle element last in the final weave.
    slow, fast = head, head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next

    # 2. Detach and reverse the second half. Cutting the link first is what stops
    #    the merge below from running back into the first half and cycling.
    second = slow.next
    slow.next = None

    previous: Optional[ListNode] = None
    while second is not None:
        following = second.next
        second.next = previous
        previous = second
        second = following

    # 3. Weave the two halves. The reversed half is never longer than the first,
    #    so it runs out first and its exhaustion ends the loop.
    first, second = head, previous
    while second is not None:
        first_next, second_next = first.next, second.next
        first.next = second
        second.next = first_next
        first, second = first_next, second_next
