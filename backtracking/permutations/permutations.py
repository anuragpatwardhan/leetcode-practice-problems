"""LeetCode 46. Permutations."""

from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    """Every ordering of `nums`, built by choosing one unused element at a time."""
    n = len(nums)
    if n == 0:
        # One permutation of nothing: the empty one. Returning [] instead would
        # claim there are none, which breaks anything counting results.
        return [[]]

    results: List[List[int]] = []
    used = [False] * n
    path: List[int] = []

    # Explicit stack rather than recursion, per this repo's rule. Each frame is
    # [chosen index, iterator over candidates]: the iterator is what lets a
    # frame resume where it left off instead of rescanning from the start, and
    # the chosen index is what tells it which choice to undo when it resumes.
    NOTHING = -1
    stack: List[list] = [[NOTHING, iter(range(n))]]

    while stack:
        frame = stack[-1]

        # Reached only when a child frame has finished, so the choice this frame
        # made on its way down is still standing and has to come back off. Doing
        # the undo here, at the single point where a frame regains control, is
        # what keeps it from being forgotten on one of the several exit paths.
        if frame[0] != NOTHING:
            used[frame[0]] = False
            path.pop()
            frame[0] = NOTHING

        advanced = False
        for index in frame[1]:
            if used[index]:
                continue

            used[index] = True
            path.append(nums[index])

            if len(path) == n:
                # A complete ordering. Copy it — `path` is about to be mutated,
                # and storing the live list would leave every result aliasing
                # the same object, which ends up empty.
                results.append(path.copy())
                used[index] = False
                path.pop()
                continue

            frame[0] = index
            stack.append([NOTHING, iter(range(n))])
            advanced = True
            break

        if not advanced:
            stack.pop()

    return results
