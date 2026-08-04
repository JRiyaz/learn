# 21-stack.md

# Stack — Solving Problems Using Last-In, First-Out (LIFO)

## Interview Confidence

**Difficulty:** ⭐⭐☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Why Interviewers Ask This

Stacks appear in far more places than most engineers realize.

Whenever you see:

- Nested structures
- Undo operations
- Backtracking
- Function calls
- Expression evaluation
- Matching pairs

there's a good chance a **Stack** is involved.

Many interview problems that look complicated become simple once you recognize the **LIFO (Last-In, First-Out)**
behavior.

______________________________________________________________________

# Learning Objectives

After this lesson, you should be able to:

- Understand what a Stack is.
- Explain the LIFO principle.
- Recognize Stack interview problems.
- Understand Monotonic Stacks.
- Know when **not** to use a Stack.

______________________________________________________________________

# What Is a Stack?

A Stack is a data structure where the **last inserted element is the first one removed**.

Think of a stack of plates.

```
+-------+
| Plate |
+-------+

+-------+
| Plate |
+-------+

+-------+
| Plate |
+-------+
```

You can only:

- Add to the top.
- Remove from the top.

You cannot remove the middle plate.

______________________________________________________________________

# LIFO Principle

```
Push A

↓

[A]

Push B

↓

[B]
[A]

Push C

↓

[C]
[B]
[A]
```

Now remove:

```
Pop

↓

C

Pop

↓

B

Pop

↓

A
```

Last In.

First Out.

______________________________________________________________________

# Real-World Examples

## Browser History

```
Google

↓

YouTube

↓

GitHub
```

Press Back.

```
GitHub removed.

↓

YouTube
```

Exactly a Stack.

______________________________________________________________________

## Undo Feature

Text Editor

```
Type A

↓

Type B

↓

Delete
```

Undo removes the most recent operation.

______________________________________________________________________

## Function Calls

```
main()

↓

login()

↓

authenticate()

↓

database()
```

When database finishes,

execution returns in reverse order.

The programming language runtime maintains a **call stack** for this.

______________________________________________________________________

# Stack Operations

## Push

Add to top.

```
Before

[1]

[2]
```

Push

```
3
```

Result

```
[3]

[2]

[1]
```

______________________________________________________________________

## Pop

Remove top.

```
3

↓

Removed
```

______________________________________________________________________

## Peek (Top)

Look at top.

Don't remove.

```
Top

↓

3
```

______________________________________________________________________

## Is Empty

```
[]

↓

True
```

______________________________________________________________________

# Complexity

| Operation | Complexity |
|-----------|------------|
| Push | O(1) |
| Pop | O(1) |
| Peek | O(1) |
| Is Empty | O(1) |

______________________________________________________________________

# Python Implementation

Python lists already behave like stacks.

```python
stack = []

stack.append(10)

stack.append(20)

stack.pop()
```

Avoid

```python
pop(0)
```

because it shifts elements and is O(n).

______________________________________________________________________

# Visual Example

```
Stack

Top

↓

30

20

10
```

Pop

```
30
```

Remaining

```
20

10
```

______________________________________________________________________

# When Should You Think "Stack"?

Interview clues:

- Valid parentheses
- Nested
- Undo
- Reverse processing
- Previous element
- Next greater/smaller element
- Expression evaluation
- Depth-first traversal

Think:

> **The most recently seen item matters most.**

______________________________________________________________________

# Common Stack Patterns

## 1. Matching Pairs

```
()

[]

{}
```

Example:

- Valid Parentheses
- HTML parsing
- XML parsing

______________________________________________________________________

## 2. Undo Operations

```
Action

↓

Push

Undo

↓

Pop
```

______________________________________________________________________

## 3. Monotonic Stack

Maintain increasing or decreasing order.

Used in:

- Daily Temperatures
- Next Greater Element
- Largest Rectangle in Histogram
- Stock Span

______________________________________________________________________

## 4. Expression Evaluation

```
3 + (2 × 5)
```

Stacks help process nested expressions.

______________________________________________________________________

# Stack vs Queue

## Stack

```
Top

↓

3

2

1
```

Removal

```
3
```

LIFO.

______________________________________________________________________

## Queue

```
Front

↓

1

2

3
```

Removal

```
1
```

FIFO.

______________________________________________________________________

# Backend Analogy

Suppose a microservice receives nested API calls.

```
Request

↓

Authentication

↓

Authorization

↓

Database
```

When returning,

the last function exits first.

Exactly how the call stack behaves.

Other examples:

- Recursive API processing
- Nested JSON parsing
- XML parsing
- Compiler design

______________________________________________________________________

# When NOT to Use a Stack

Avoid when:

- First-In First-Out is required.
- Random access is needed.
- Priority determines processing.
- Elements need sorting.

______________________________________________________________________

# Common Interview Problems

## Easy

- Valid Parentheses
- Baseball Game

______________________________________________________________________

## Medium

- Daily Temperatures
- Next Greater Element II
- Decode String
- Evaluate Reverse Polish Notation

______________________________________________________________________

## Hard

- Largest Rectangle in Histogram
- Basic Calculator
- Trapping Rain Water *(Monotonic Stack approach)*

______________________________________________________________________

# Common Mistakes

## 1. Using Queue Instead

Remember

```
Stack

↓

LIFO
```

______________________________________________________________________

## 2. Popping Empty Stack

Always check

```python
if stack:
```

before popping.

______________________________________________________________________

## 3. Forgetting Peek

Sometimes you only need to inspect.

Don't always pop.

______________________________________________________________________

## 4. Using Stack When Hash Map Is Better

If you need fast lookup by key,

use a Hash Map.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Is the latest element the most important?
1. Is nesting involved?
1. Is there matching or balancing?
1. Do we need to remember previous values?
1. Would a Stack naturally model the problem?

______________________________________________________________________

### Common Follow-ups

### Q: Why is Push O(1)?

It inserts at the end.

______________________________________________________________________

### Q: Why use a list in Python?

`append()` and `pop()` from the end are both O(1) on average.

______________________________________________________________________

### Q: When should I use `collections.deque`?

`deque` is ideal for queues and can also be used as a stack. For interview stack problems, a list is usually sufficient.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Stack (LIFO) |
| Recognition | Nested, matching, undo, previous element |
| Operations | Push, Pop, Peek |
| Time | O(1) |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Easy

1. Valid Parentheses
1. Baseball Game

## Medium

1. Daily Temperatures
1. Decode String
1. Evaluate Reverse Polish Notation
1. Next Greater Element II

## Hard

1. Largest Rectangle in Histogram
1. Basic Calculator

______________________________________________________________________

# Quick Revision

- Stack = Last In, First Out.
- Push → Add.
- Pop → Remove.
- Peek → Inspect top.
- Python list works well as a stack.
- Think Stack when solving:
  - Nested structures
  - Matching pairs
  - Undo operations
  - Previous/Next element problems

______________________________________________________________________

# What's Next?

We'll start with the most important Stack interview question:

**22-valid-parentheses.md**

This introduces the **Matching Pair Pattern**, which is the foundation for many Stack problems.

______________________________________________________________________

# Navigation

**Previous**

[20-minimum-window-substring.md](20-minimum-window-substring.md)

**Next**

[22-valid-parentheses.md](22-valid-parentheses.md)
