"""LeetCode 76. Minimum Window Substring."""

from collections import Counter


def min_window(s: str, t: str) -> str:
    """Shortest substring of ``s`` containing every character of ``t``.

    Multiplicity counts: if ``t`` holds two of a character, the window must too.
    Returns ``""`` when no such substring exists.
    """
    if not s or not t or len(t) > len(s):
        return ""

    # Positive values are characters still owed; zero or negative means the
    # window holds enough of that character, with negatives tracking the surplus.
    remaining = Counter(t)
    missing = len(t)  # total characters still owed, counting duplicates

    best_length = len(s) + 1
    best_start = 0
    left = 0

    for right, char in enumerate(s):
        # Only decrement the debt when this character is actually still owed.
        # A surplus copy pushes the count negative without touching `missing`.
        if remaining[char] > 0:
            missing -= 1
        remaining[char] -= 1

        while missing == 0:
            if right - left + 1 < best_length:
                best_length = right - left + 1
                best_start = left

            # Give back the leftmost character. It only re-enters the debt if it
            # was needed rather than surplus, which is what the > 0 test catches.
            remaining[s[left]] += 1
            if remaining[s[left]] > 0:
                missing += 1
            left += 1

    if best_length > len(s):
        return ""
    return s[best_start : best_start + best_length]
