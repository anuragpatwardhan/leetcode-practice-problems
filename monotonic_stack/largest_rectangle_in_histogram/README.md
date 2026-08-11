# Largest Rectangle in Histogram

**Number:** 84
**Difficulty:** Hard
**Pattern:** Monotonic stack
**Problem:** https://leetcode.com/problems/largest-rectangle-in-histogram/

## Problem

Given bar heights of unit width, return the area of the largest rectangle that fits
entirely under the histogram.

## Approach

Rather than search over rectangles, search over **heights**. Every maximal rectangle is
capped by its shortest bar, so it is enough to ask, for each bar: how far can a
rectangle of exactly this height extend left and right? The answer is the run of
neighbouring bars at least this tall, bounded on each side by the first shorter bar.

Finding "first shorter bar on each side" for every position is the monotonic stack
pattern, and it can be done in the same pass that computes the areas.

The stack holds `(start_index, height)` pairs with strictly increasing heights. For
each new bar:

- Pop every pending entry taller than it. Each pop is a bar that can extend no further
  right, so its rectangle is finished and its area is `height × (current - start)`.
- **The new bar inherits the start index of the last entry popped.** This is the step
  that is easy to get wrong. Every bar between that start and here was at least as tall
  as the popped bar, so it is certainly at least as tall as the current, shorter one —
  meaning the current bar's rectangle can reach all the way back. Without this, the
  widest rectangle in `[6, 1, 6]` would never be found, because the `1` would think it
  begins at its own index.

Anything left on the stack at the end was never capped on the right, so those
rectangles run to the end of the histogram and are measured in a final sweep.

Storing the start index alongside the height avoids the usual trick of appending a
sentinel zero bar, and keeps the input untouched.

## Complexity

- **Time:** `O(n)` — each bar is pushed once and popped at most once.
- **Space:** `O(n)` for the stack, which holds every bar when heights strictly
  increase.
