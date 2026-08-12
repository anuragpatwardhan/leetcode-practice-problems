# Best Time to Buy and Sell Stock

**Number:** 121
**Difficulty:** Easy
**Pattern:** Running minimum, single pass
**Problem:** https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

## Problem

Given daily prices, return the best profit from buying on one day and selling on a
later one, or `0` if no trade makes money.

## Approach

The brute force tries every buy/sell pair at `O(n^2)`. The reduction comes from noticing
that the two loops are not really independent: **for any given sell day, the only buy
day worth considering is the cheapest one before it.** Every other choice yields strictly
less. So the inner loop collapses into a single running minimum.

Walk once, keeping the cheapest price seen so far. At each day, the best trade ending
today is `price - cheapest_so_far`; keep the largest across the whole walk.

Updating the minimum *before* measuring the profit is safe. In the worst case the
current price is itself the new minimum, giving a profit of `0` — which never displaces
a real profit, and correctly represents that buying and selling on the same day earns
nothing.

The case worth testing is that the best buy is **not** always the global minimum:
in `[3, 1, 2, 100]` the cheapest day is `1`, and there the answer agrees — but in
`[9, 2, 8, 1]` the global minimum arrives last with nothing after it to sell into, so
a solution anchored to the global minimum returns `0` instead of `6`. Tracking the
minimum *as it evolves* handles both without a special case.

## Complexity

- **Time:** `O(n)` — one pass.
- **Space:** `O(1)` — two scalars.
