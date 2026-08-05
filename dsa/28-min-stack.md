# 28-min-stack.md

# Min Stack

> **🎯 This lesson teaches one of the most important interview ideas:**
>
> **Augmenting a Data Structure**
>
> Instead of creating a completely new data structure, we enhance an existing **Stack** so it can answer additional questions efficiently.
>
> This is a common technique in backend systems and technical interviews.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐☆ High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 25–30 minutes |
| Revision Time | 15 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem is **not** about stacks.

Interviewers want to know if you can:

- Design a custom data structure
- Store additional metadata
- Trade a little memory for much faster queries
- Maintain information incrementally

This exact idea appears in:

- Database indexes
- Redis
- Caching systems
- Monitoring systems
- Analytics pipelines

______________________________________________________________________

# Problem Statement

Design a stack that supports the following operations:

```text
push(x)
```

Push an element.

______________________________________________________________________

```text
pop()
```

Remove the top element.

______________________________________________________________________

```text
top()
```

Return the top element.

______________________________________________________________________

```text
get_min()
```

Return the minimum element.

______________________________________________________________________

All operations must run in

```text
O(1)
```

time.

______________________________________________________________________

# Before Learning the Algorithm

## Why Is This Difficult?

A normal stack already supports:

```
Push

O(1)
```

```
Pop

O(1)
```

```
Top

O(1)
```

But

```
Minimum?
```

How would you find it?

Suppose

```
8

3

6

1

9
```

Current minimum

```
1
```

Easy.

Now pop

```
9
```

Still

```
1
```

Pop again

```
1
```

Now what?

You must search the entire stack again.

That's

```
O(n)
```

Interview requires

```
O(1)
```

______________________________________________________________________

# Simple English

Imagine a stack of exam papers.

Besides the papers,

you also maintain a sticky note saying:

> "Lowest score so far."

Whenever a new paper is added,

you immediately update the sticky note.

You never need to scan all papers again.

______________________________________________________________________

# Backend Engineering Analogy

Suppose Redis stores:

```
Page Load Times
```

Besides storing every value,

it also maintains:

```
Current Minimum

Current Maximum
```

Whenever new data arrives,

metadata is updated immediately.

Later,

queries become instant.

The same idea appears in:

- Metrics dashboards
- Database indexes
- Monitoring systems
- Time-series databases

______________________________________________________________________

# Pattern Recognition

## Pattern

**Augmented Data Structure**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Design
- Support multiple operations
- Constant time
- Custom data structure

Think

```
Store Extra Information
```

instead of

```
Recompute Everything
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Use a normal stack.

Whenever

```
get_min()
```

is called,

scan the stack.

______________________________________________________________________

## Algorithm

Stack

```
8

3

6

1

9
```

Need minimum.

Scan

```
8

↓

3

↓

6

↓

1

↓

9
```

Minimum

```
1
```

______________________________________________________________________

## Complexity

Push

```
O(1)
```

Pop

```
O(1)
```

Top

```
O(1)
```

Minimum

```
O(n)
```

Too slow.

______________________________________________________________________

# Better Observation

When pushing a new value,

we already know:

```
Current Minimum
```

Why not remember it?

______________________________________________________________________

# Optimized Solution (Two Stacks)

## Key Insight

Maintain

```
Main Stack
```

and

```
Minimum Stack
```

The minimum stack always stores

```
Current Minimum
```

at every level.

______________________________________________________________________

# Understanding the Two Stacks

Initially

```
Main

[]
```

```
Min

[]
```

______________________________________________________________________

Push

```
8
```

Main

```
8
```

Min

```
8
```

______________________________________________________________________

Push

```
3
```

Current minimum

```
min(8,3)

↓

3
```

Main

```
8

3
```

Min

```
8

3
```

______________________________________________________________________

Push

```
6
```

Minimum remains

```
3
```

Main

```
8

3

6
```

Min

```
8

3

3
```

Notice

We store

```
3
```

again.

______________________________________________________________________

Push

```
1
```

Minimum

```
1
```

Main

```
8

3

6

1
```

Min

```
8

3

3

1
```

______________________________________________________________________

Push

```
9
```

Minimum remains

```
1
```

Main

```
8

3

6

1

9
```

Min

```
8

3

3

1

1
```

______________________________________________________________________

# Why Duplicate Minimums?

This is the most important concept.

Suppose

```
Main

8

3

6

1

9
```

Min

```
8

3

3

1

1
```

Pop

```
9
```

Main

```
8

3

6

1
```

Min

```
8

3

3

1
```

Minimum

Still

```
1
```

Now pop

```
1
```

Main

```
8

3

6
```

Min

```
8

3

3
```

Minimum instantly becomes

```
3
```

No searching required.

______________________________________________________________________

# Dry Run

Operations

```
Push 5
```

Main

```
5
```

Min

```
5
```

______________________________________________________________________

Push

```
2
```

Main

```
5

2
```

Min

```
5

2
```

______________________________________________________________________

Push

```
7
```

Main

```
5

2

7
```

Min

```
5

2

2
```

______________________________________________________________________

get_min()

Top of Min Stack

```
2
```

______________________________________________________________________

Pop

```
7
```

Pop from both stacks.

Minimum

Still

```
2
```

______________________________________________________________________

# Visual Explanation

```
Main Stack

8

3

6

1

9
```

```
Min Stack

8

3

3

1

1
```

Notice:

Every level knows

the minimum

up to that point.

______________________________________________________________________

# Alternative Optimized Solution

Instead of using two stacks,

store pairs.

Example

```
(value, current_min)
```

Stack

```
(8,8)

(3,3)

(6,3)

(1,1)

(9,1)
```

Now,

the top element always contains:

```
Current Value

+

Current Minimum
```

This uses only one stack internally and is commonly preferred in production code.

______________________________________________________________________

# Why This Works

Loop Invariant:

> At every position in the stack, the auxiliary stack (or stored pair) contains the minimum value among all elements up to that position.

Whenever a new value is pushed:

```
New Minimum

=

min(Current Minimum, New Value)
```

Whenever a value is popped,

the corresponding minimum is popped as well.

Therefore,

the current minimum is always available in

```
O(1)
```

time.

______________________________________________________________________

# Edge Cases

### Empty Stack

Calling

```
pop()

top()

get_min()
```

should raise an exception or return an appropriate error.

______________________________________________________________________

### One Element

Push

```
5
```

Minimum

```
5
```

Pop

Empty stack.

______________________________________________________________________

### Duplicate Minimum Values

```
2

2

2
```

Works correctly because each minimum is stored.

______________________________________________________________________

### Negative Numbers

```
-3

5

-10
```

Minimum correctly becomes

```
-10
```

______________________________________________________________________

# Complexity Analysis

| Operation | Brute Force | Optimized |
|-----------|------------|-----------|
| Push | O(1) | O(1) |
| Pop | O(1) | O(1) |
| Top | O(1) | O(1) |
| Get Minimum | O(n) | O(1) |

Space

```
O(n)
```

because we maintain an additional stack (or additional metadata).

______________________________________________________________________

# Production-Quality Python

## Optimized (Two Stacks)

```python
from typing import List


class MinStack:
    def __init__(self) -> None:
        self.stack: List[int] = []
        self.min_stack: List[int] = []

    def push(self, value: int) -> None:
        self.stack.append(value)

        if not self.min_stack:
            self.min_stack.append(value)
        else:
            self.min_stack.append(
                min(value, self.min_stack[-1])
            )

    def pop(self) -> int:
        self.min_stack.pop()
        return self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def get_min(self) -> int:
        return self.min_stack[-1]


if __name__ == "__main__":
    stack = MinStack()

    stack.push(8)
    stack.push(3)
    stack.push(6)
    stack.push(1)

    print(stack.get_min())  # 1

    stack.pop()

    print(stack.get_min())  # 3
```

______________________________________________________________________

## Alternative (Single Stack with Pairs)

```python
from typing import List, Tuple


class MinStack:
    def __init__(self) -> None:
        self.stack: List[Tuple[int, int]] = []

    def push(self, value: int) -> None:
        current_min = (
            value
            if not self.stack
            else min(value, self.stack[-1][1])
        )

        self.stack.append((value, current_min))

    def pop(self) -> int:
        value, _ = self.stack.pop()
        return value

    def top(self) -> int:
        return self.stack[-1][0]

    def get_min(self) -> int:
        return self.stack[-1][1]
```

> **Interview Tip:** Explain the two-stack solution first because it's easier to visualize. Then mention the pair-based approach as an optimization in code organization.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Scanning the stack every time `get_min()` is called.

That violates the O(1) requirement.

______________________________________________________________________

## Mistake 2

Only storing new minimum values.

You must store the **current minimum at every level**, otherwise pops won't work correctly.

______________________________________________________________________

## Mistake 3

Forgetting to pop from both stacks.

The two stacks must always stay synchronized.

______________________________________________________________________

## Mistake 4

Not handling an empty stack.

Always consider what `pop()`, `top()`, or `get_min()` should do when no elements exist.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A normal stack gives O(1) push, pop, and top, but finding the minimum requires scanning all elements. Instead of recomputing the minimum each time, I can store the current minimum alongside every push. I can do this either with a second stack or by storing `(value, current_min)` pairs. This allows all operations, including `get_min()`, to run in O(1)."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use two stacks?**

One stores the actual values.

The other stores the minimum value at each depth.

______________________________________________________________________

**Q. Why store duplicate minimum values?**

Because after popping, we need to know what the previous minimum was without recomputing it.

______________________________________________________________________

**Q. Can this be done with one stack?**

Yes.

Store `(value, current_min)` pairs.

______________________________________________________________________

**Q. Where is this pattern used in backend systems?**

- Redis-like caches
- Metrics systems
- Database indexes
- Time-series databases
- Monitoring dashboards

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Augmented Data Structure |
| Recognition | O(1) Extra Operations |
| Brute Force | Scan for Minimum |
| Optimized | Two Stacks / Pair Stack |
| Push | O(1) |
| Pop | O(1) |
| Top | O(1) |
| Get Minimum | O(1) |

______________________________________________________________________

# Quick Revision

- A normal stack cannot return the minimum in O(1).
- Store extra metadata while pushing.
- Maintain a second stack or store `(value, current_min)` pairs.
- Every pop removes metadata too.
- Never recompute the minimum.
- This is an example of augmenting a data structure.
- All operations become O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Implement Queue using Stacks
1. Implement Stack using Queues
1. Baseball Game

______________________________________________________________________

## Medium

4. Daily Temperatures
1. Online Stock Span
1. Asteroid Collision
1. Evaluate Reverse Polish Notation

______________________________________________________________________

## Hard (Optional)

8. Largest Rectangle in Histogram
1. Maximal Rectangle
1. Trapping Rain Water (Stack Approach)

______________________________________________________________________

# Key Takeaway

The most important lesson from this problem is that **you don't always need a new algorithm—you sometimes need a smarter
data structure**. By storing **additional metadata during updates**, you can answer future queries in constant time.
This idea of **augmenting data structures** is widely used in databases, caches, indexing systems, and advanced
interview questions.

______________________________________________________________________

# Next

[29-number-of-recent-calls.md](29-number-of-recent-calls.md)
