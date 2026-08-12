# Valid Parentheses

**Number:** 20
**Difficulty:** Easy
**Pattern:** Stack
**Problem:** https://leetcode.com/problems/valid-parentheses/

## Problem

Given a string of `()`, `[]` and `{}`, decide whether every bracket is closed by the
correct type in the correct order.

## Approach

Counting brackets is not enough: `([)]` has two of each and is still invalid. What
matters is **order**, specifically that brackets close in the reverse of the order they
opened — which is exactly last-in-first-out, so a stack is the natural fit.

Push every opener. On a closer, the top of the stack must be its matching opener; pop
and compare. A mapping from closer to opener keeps that comparison to one lookup.

Three ways a string fails, and all three need handling:

- **Wrong type** — the popped opener does not match, as in `(]`.
- **Closer with nothing open** — the stack is empty when a closer arrives, as in `()]`.
  Popping without checking would raise instead of returning `False`.
- **Opener never closed** — the scan finishes with a non-empty stack, as in `(((`. This
  one is easy to forget because no mismatch is ever detected during the loop; the final
  emptiness check is what catches it.

The tests compare against an independent reference that repeatedly deletes adjacent
matched pairs and asks whether anything remains — a completely different method,
checked over hundreds of random bracket strings.

## Complexity

- **Time:** `O(n)` — one pass, constant work per character.
- **Space:** `O(n)` for the stack, which holds every character when the string is all
  openers.
