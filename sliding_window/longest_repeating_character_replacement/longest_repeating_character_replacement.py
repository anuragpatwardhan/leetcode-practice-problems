"""LeetCode 424. Longest Repeating Character Replacement."""

from collections import defaultdict


def character_replacement(s: str, k: int) -> int:
    """Length of the longest run achievable by replacing at most ``k`` characters."""
    counts: defaultdict[str, int] = defaultdict(int)
    best_count = 0  # highest single-character count seen in any window so far
    left = 0

    for right, char in enumerate(s):
        counts[char] += 1
        best_count = max(best_count, counts[char])

        # Characters that would have to be replaced to make the window uniform.
        if (right - left + 1) - best_count > k:
            # Slide rather than shrink: advance both ends by one so the window
            # keeps its width. A window this size is no longer achievable, but a
            # wider one might still be found further along.
            counts[s[left]] -= 1
            left += 1

    # best_count is deliberately never lowered, so the test above can be too
    # optimistic once the window moves past the run that set it. That cannot
    # inflate the answer: the window only ever widens when some character
    # genuinely reaches a new highest count, and its final width is what is
    # returned.
    return len(s) - left
