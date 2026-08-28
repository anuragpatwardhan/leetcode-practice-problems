# Word Search

**Number:** 79
**Difficulty:** Medium
**Pattern:** Backtracking on a grid
**Problem:** https://leetcode.com/problems/word-search/

## Problem

Given a grid of letters and a word, decide whether the word can be spelled by moving
between orthogonally adjacent cells, using no cell more than once.

## Approach

From every cell matching the first letter, walk outward matching one letter per step. The
constraint that makes this backtracking rather than plain traversal is **"no cell more than
once"**: the set of used cells depends on the route taken, so it cannot be a global visited
set the way it is in [Number of Islands](../number_of_islands/).

That difference is the whole problem. In a flood fill, a cell visited once never needs
visiting again, so marking it permanently is correct and is what makes the search linear.
Here, a cell used by a route that turns out to be a dead end must become available again to
every other route. So the mark has to be *undone* when the search retreats past it, and the
state being tracked is not "seen" but "on the current path".

The search is an explicit stack, per this repo's rule that depth tracking input size goes
iterative. Each frame holds its cell and an iterator over the four directions, so resuming
a frame continues where it left off rather than rescanning neighbours it already rejected.

## The trap

**Marking without unmarking.** Both halves are one line, and the missing half fails
silently — the search still terminates, still returns a boolean, and is right on most
inputs. It is only wrong when a route abandons cells that the successful route needs.

The test for it is:

```
B B B B          word: BBBABA
A B A A
```

which returns `True` correctly and `False` without the unmark. That board was found by
differential comparison against an exhaustive search, not by reading the code — a fair
measure of how invisible the bug is. Hand-written examples mostly succeed on the first
route they try and never exercise the retreat at all.

**The board is not modified.** The usual solution overwrites each visited cell with a
sentinel and restores it on the way out, which makes the path set free. It works, but a bug
in the restore hands the caller back a corrupted board, and the corruption depends on which
routes happened to fail. A path set costs `O(len(word))` and cannot do that.

## Two prunes

Both are about the case the naive search chokes on: a board where almost every path is
viable until the last letter.

- **Letter counts.** If the word needs more of some letter than the board holds, no path
  can exist. A board of all `A` against `"AAAA…B"` goes from exponential to a single pass.
- **Direction.** The number of starting cells is the branching factor of the entire search,
  so if the word's last letter is rarer on the board than its first, the word is reversed
  and spelled backwards. A path read backwards is still a path, so the answer is unchanged.

The suite pins down that reversing is **answer-preserving** — via random differential
testing and an explicit both-directions case — but it does not assert that it is *faster*.
Flipping the comparison to pick the worse end passes every test. That is the honest state
of it: correctness is verified, the performance claim is reasoned rather than measured.

## Verification

The reference enumerates self-avoiding walks and reads the letters off them, which is the
problem's definition rather than a second copy of the algorithm. It is exponential and only
ever runs on boards up to 4×4.

Checked over 300 random boards on a two-letter alphabet, where words collide constantly and
both answers occur often, plus 300 on three letters, where matches are rarer and the
rejection paths get exercised. A third set generates words by walking a random path on the
board, so the answer is known to be `True` in advance — a solution that rejects everything
passes the first two suites far more easily than it should.

## Complexity

- **Time:** `O(rows × cols × 3^len(word))` worst case — each step has three onward
  directions after the one it came from. The prunes do not change this bound; they remove
  the inputs that actually reach it.
- **Space:** `O(len(word))` for the stack and the path set.
