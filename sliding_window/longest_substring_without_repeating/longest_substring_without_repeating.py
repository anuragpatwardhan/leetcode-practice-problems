"""LeetCode 3. Longest Substring Without Repeating Characters."""


def length_of_longest_substring(s: str) -> int:
    """Return the length of the longest substring of ``s`` with no repeated character."""
    last_seen: dict[str, int] = {}
    longest = 0
    start = 0

    for index, char in enumerate(s):
        previous = last_seen.get(char)
        # Only move the window forward; an earlier duplicate is already outside it.
        if previous is not None and previous >= start:
            start = previous + 1

        last_seen[char] = index
        longest = max(longest, index - start + 1)

    return longest
