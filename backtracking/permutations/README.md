# Permutations

**Number:** 46
**Difficulty:** Medium
**Pattern:** Backtracking (enumeration)
**Problem:** https://leetcode.com/problems/permutations/

## Problem

Given an array of distinct integers, return every possible ordering of them.

## Approach

Build an ordering one position at a time. At each position, try every element not already
placed; when the ordering is full, record it and step back to try the next candidate.

This is the other half of backtracking from [Word Search](../word_search/). There the
search was looking for *one* answer and could stop the moment it found it. Here every leaf
of the search tree is a result, so the search always runs to completion and the interesting
question is not "does a path exist" but "is the bookkeeping exact" — every ordering must be
full length, use each element once, and appear once.

The tree has `n` choices at the root, `n-1` below each of those, and so on, which is where
`n!` comes from. There is no pruning to do: nothing can be ruled out early, because every
complete path is valid.

## Iterative, with frames that remember their choice

Per this repo's rule the search uses an explicit stack. Each frame is
`[chosen index, iterator over candidates]`:

- **The iterator** is what lets a frame resume where it left off. Re-scanning candidates
  from the start on every resume would revisit choices already explored and emit
  duplicates.
- **The chosen index** is what tells the frame which element to release when it resumes.

The undo happens at the single point where a frame regains control — the top of the loop,
when its recorded choice is still standing. That placement is the reason it is reliable: a
frame can exit in several ways (pushing a child, recording a leaf, running out of
candidates), and doing the undo at each exit means getting it right four times instead of
once.

## The traps

**Append a copy, not the path.** `results.append(path)` stores a reference to the one list
the search keeps mutating. Every entry ends up aliasing it, and since the path is empty when
the search finishes, the answer reads as `n!` empty lists. It looks like a completely
different kind of failure than a one-word fix.

**An empty input has one permutation, not none.** `permute([])` is `[[]]` — `0!` is 1. It
is tempting to return `[]` for an empty list, and anything counting results downstream then
disagrees with the arithmetic.

**Distinct inputs are an assumption, not a property of the code.** LeetCode guarantees the
values are distinct, and this solution relies on it: with a repeated value it emits that
ordering more than once, because the used flags track *positions* while the results compare
by value. Deduplicating requires sorting and skipping equal siblings — that is LeetCode 47,
a different problem, and pretending this solves it would be the quiet kind of wrong.

## Verification

The reference is `itertools.permutations`, which generates orderings by position in
lexicographic order with no backtracking at all — a genuinely different mechanism, so
agreement means something. Compared on every size from 0 to 6 exhaustively, and on 200
random inputs of distinct values.

Beyond matching, the tests assert the properties that the bookkeeping exists to guarantee,
since those localise a failure better than a diff of two large lists: results are all full
length, each is a rearrangement of the input, all are distinct, all are separate list
objects, the count is exactly `n!`, and the input is unmodified.

Three wrong versions were swapped in to check the suite actually reacts — storing the live
path, never releasing a choice on resume, and returning `[]` for an empty input — and all
three fail it.

One caveat worth recording. Replacing a frame's iterator with a fresh one on resume, instead
of continuing it, makes the suite **hang rather than fail**: the frame re-explores its
candidates forever. Termination is doing the work an assertion would normally do, which is a
weaker signal — a failing test names the problem, a hanging one only says something is
wrong.

## Complexity

- **Time:** `O(n × n!)` — `n!` orderings, each costing `O(n)` to copy out.
- **Space:** `O(n)` for the stack, path and used flags, excluding the `O(n × n!)` result.
