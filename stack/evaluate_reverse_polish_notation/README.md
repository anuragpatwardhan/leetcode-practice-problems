# Evaluate Reverse Polish Notation

**Number:** 150
**Difficulty:** Medium
**Pattern:** Stack
**Problem:** https://leetcode.com/problems/evaluate-reverse-polish-notation/

## Problem

Evaluate an arithmetic expression written in reverse Polish (postfix) notation, where
each operator follows its two operands.

## Approach

Postfix notation exists precisely so that a stack can evaluate it without any parsing:
there are no parentheses and no precedence rules, because the order is already explicit
in the token sequence.

Scan left to right. Push every number. On an operator, pop two operands, apply it, push
the result. The final stack holds one value — the answer.

The algorithm is four lines; the correctness lives entirely in three details.

**Operand order.** The stack returns operands in reverse, so the *first* pop is the
right-hand side. This is worth stating explicitly because a swap still produces correct
answers for `+` and `*` and only breaks on `-` and `/` — the kind of bug that passes a
casual test and fails on a hidden one.

**Division truncates toward zero, not down.** Python's `//` floors, so `-7 // 2` is
`-4`, while this problem wants `-3`. The usual fix is `int(a / b)`, which truncates
correctly but routes an integer through a float and silently loses precision past
`2**53`. Dividing the magnitudes and reapplying the sign stays exact for any integer,
and the tests check an operand just past that boundary.

**A negative literal is not an operator.** `"-11"` must be read as a number. An exact
dictionary lookup (`token in operators`) distinguishes it; a "starts with `-`" check
would not, and neither would trying `int(token)` inside a bare `except`.

The random test builds expression trees and evaluates each one independently while
emitting its postfix form, so the solution is compared against a value derived without
using a stack at all.

## Complexity

- **Time:** `O(n)` — one pass, constant work per token.
- **Space:** `O(n)` for the operand stack; an expression of all literals followed by all
  operators pushes everything before reducing anything.
