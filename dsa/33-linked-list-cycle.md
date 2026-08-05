# 33-linked-list-cycle.md

# Linked List Cycle

> **🎯 This lesson teaches one of the most beautiful algorithms in computer science:**
>
> **Floyd's Cycle Detection Algorithm (Tortoise and Hare Algorithm)**
>
> At first, it feels like magic.
>
> By the end of this lesson, you'll understand **why it works**, not just memorize it.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 20–25 minutes |
| Revision Time | 15 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers use this problem to test whether you can:

- Recognize cycles
- Use Fast & Slow Pointers
- Avoid unnecessary memory
- Reason mathematically about pointer movement

Many beginners solve it using a Hash Set.

That works.

Interviewers then ask:

> "Can you solve it using **O(1) extra space**?"

The expected answer is **Floyd's Cycle Detection Algorithm**.

This same technique is used in:

- Loop detection
- Deadlock detection
- Functional graph analysis
- Happy Number
- Pollard's Rho algorithm (number theory)

______________________________________________________________________

# Problem Statement

Given the head of a linked list,

determine whether the linked list contains a cycle.

A cycle exists if a node's `next` pointer points to an earlier node instead of `None`.

Return:

```text
True
```

if a cycle exists,

otherwise

```text
False
```

______________________________________________________________________

## Example 1

```text
1 → 2 → 3 → 4
      ↑       |
      |_______|
```

Output

```text
True
```

______________________________________________________________________

## Example 2

```text
1 → 2 → 3 → None
```

Output

```text
False
```

______________________________________________________________________

# Before Learning the Algorithm

## What Is a Cycle?

Normally

```text
1 → 2 → 3 → 4 → None
```

Traversal eventually stops.

______________________________________________________________________

Cycle

```text
1 → 2 → 3 → 4
    ↑       |
    |_______|
```

Traversal never ends.

```
2

↓

3

↓

4

↓

2

↓

3

↓

4

...
```

Forever.

______________________________________________________________________

# Backend Engineering Analogy

Imagine two microservices calling each other.

```
Service A

↓

Service B

↓

Service C

↓

Service A
```

Requests never terminate.

Infinite loop.

Cycle detection algorithms help detect these dependency loops.

Other examples:

- Circular dependencies
- Workflow engines
- Package managers
- Graph processing
- Distributed systems

______________________________________________________________________

# Pattern Recognition

## Pattern

**Fast & Slow Pointers (Floyd's Algorithm)**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Cycle
- Infinite Loop
- Loop Detection
- Circular
- Repeated Traversal

Think

```
Fast

+

Slow
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Remember every node you've visited.

If you visit the same node again,

a cycle exists.

______________________________________________________________________

## Algorithm

Create

```
Hash Set
```

Traverse.

For every node

```
Already Seen?

↓

Yes

↓

Cycle
```

Otherwise

Store it.

______________________________________________________________________

## Dry Run

```text
1 → 2 → 3 → 4
      ↑       |
      |_______|
```

Visited

```
{}
```

↓

```
{1}
```

↓

```
{1,2}
```

↓

```
{1,2,3}
```

↓

```
{1,2,3,4}
```

↓

Back to

```
2
```

Already exists.

Return

```
True
```

______________________________________________________________________

## Complexity

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Limitation

Extra memory.

Can we detect a cycle without remembering nodes?

Yes.

______________________________________________________________________

# Optimized Solution (Floyd's Algorithm)

## Key Insight

Use two pointers.

```
Slow

↓

1 Step
```

```
Fast

↓

2 Steps
```

If no cycle exists,

Fast reaches

```
None
```

If a cycle exists,

Fast eventually catches Slow.

______________________________________________________________________

# Why Will They Meet?

Imagine a circular running track.

Slow runner

```
1 step
```

Fast runner

```
2 steps
```

Even if Fast starts behind,

it gains

```
1 step
```

every iteration.

Eventually,

Fast catches Slow.

Exactly the same happens inside a cycle.

______________________________________________________________________

# Understanding Pointer Movement

List

```text
1 → 2 → 3 → 4
      ↑       |
      |_______|
```

Initially

```
Slow

↓

1
```

```
Fast

↓

1
```

______________________________________________________________________

Iteration 1

Slow

↓

```
2
```

Fast

↓

```
3
```

______________________________________________________________________

Iteration 2

Slow

↓

```
3
```

Fast

↓

```
2
```

______________________________________________________________________

Iteration 3

Slow

↓

```
4
```

Fast

↓

```
4
```

They meet.

Cycle exists.

______________________________________________________________________

# Visual Explanation

```
Cycle

2 → 3 → 4
↑       |
|_______|
```

Pointers

```
S

↓

2
```

```
F

↓

2
```

↓

```
S → 3

F → 4
```

↓

```
S → 4

F → 3
```

↓

```
S → 2

F → 2
```

Meeting point.

______________________________________________________________________

# What If No Cycle Exists?

Example

```text
1 → 2 → 3 → None
```

Slow

```
1 → 2 → 3
```

Fast

```
1 → 3 → None
```

Fast reaches

```
None
```

No cycle.

______________________________________________________________________

# Why This Works (Intuition)

Inside the cycle,

Fast gains

```
1 node
```

on Slow during every iteration.

Suppose the cycle length is

```
k
```

After enough iterations,

the distance between them becomes

```
0 (mod k)
```

Meaning

They occupy the same node.

This is guaranteed.

______________________________________________________________________

# Loop Invariant

> Before each iteration:
>
> - Slow has moved `k` steps.
> - Fast has moved `2k` steps.

If no cycle exists,

Fast eventually reaches `None`.

If a cycle exists,

both pointers enter the cycle.

Inside the cycle,

Fast gains one node per iteration,

so a meeting is inevitable.

______________________________________________________________________

# Why Is This Better Than Hash Set?

Hash Set

Needs memory proportional to the number of visited nodes.

Floyd's Algorithm

Uses only

```
Two Pointers
```

No extra storage.

Much more memory efficient.

______________________________________________________________________

# Edge Cases

### Empty List

```text
None
```

Return

```
False
```

______________________________________________________________________

### One Node

```text
1 → None
```

Return

```
False
```

______________________________________________________________________

### One Node Cycle

```text
1
↑
|
└───
```

Return

```
True
```

______________________________________________________________________

### Long Cycle

Works regardless of cycle length.

______________________________________________________________________

# Complexity Analysis

## Hash Set

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Floyd's Algorithm

Time

```
O(n)
```

Space

```
O(1)
```

This is the expected interview solution.

______________________________________________________________________

# Production-Quality Python

## Brute Force (Hash Set)

```python
from typing import Optional, Set


class ListNode:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional["ListNode"] = None


def has_cycle(head: Optional[ListNode]) -> bool:
    visited: Set[ListNode] = set()

    current = head

    while current:
        if current in visited:
            return True

        visited.add(current)
        current = current.next

    return False
```

______________________________________________________________________

## Optimized (Floyd's Algorithm)

```python
from typing import Optional


class ListNode:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional["ListNode"] = None


def has_cycle(head: Optional[ListNode]) -> bool:
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Comparing node values instead of node references.

Example

```text
1 → 2 → 1
```

Two different nodes can contain the same value.

Compare the node objects,

not their values.

______________________________________________________________________

## Mistake 2

Moving the fast pointer only one step.

Then both pointers always remain together.

No cycle detection.

______________________________________________________________________

## Mistake 3

Using

```python
while fast:
```

instead of

```python
while fast and fast.next:
```

The fast pointer moves two steps.

You must ensure both are available.

______________________________________________________________________

## Mistake 4

Thinking they meet only at the cycle's start.

They can meet **anywhere inside the cycle**.

Meeting itself is enough to prove a cycle exists.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A straightforward solution stores every visited node in a Hash Set and checks whether a node is visited twice. That works in O(n) time but uses O(n) extra space. Since the interviewer asked for constant extra space, I'll use Floyd's Cycle Detection Algorithm. A slow pointer moves one step, and a fast pointer moves two steps. If there's no cycle, the fast pointer reaches `None`. If there is a cycle, the fast pointer eventually catches the slow pointer inside the cycle."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why does the fast pointer always catch the slow pointer?**

Inside a cycle,

it gains one node every iteration.

Eventually,

the gap becomes zero.

______________________________________________________________________

**Q. Where do they meet?**

Anywhere inside the cycle.

Not necessarily the beginning.

______________________________________________________________________

**Q. Why compare node references instead of values?**

Different nodes can contain identical values.

Only reference equality proves they are the same node.

______________________________________________________________________

**Q. Where is this algorithm used?**

- Cycle detection
- Happy Number
- Functional graphs
- Dependency analysis
- Loop detection

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Fast & Slow Pointers (Floyd's Algorithm) |
| Recognition | Cycle Detection |
| Brute Force | Hash Set |
| Optimized | Two Pointers |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- A cycle means traversal never reaches `None`.
- Hash Set solution is easy but uses extra memory.
- Floyd's Algorithm uses two pointers.
- Slow moves one step.
- Fast moves two steps.
- If they meet, a cycle exists.
- If Fast reaches `None`, no cycle exists.
- Time complexity is O(n).
- Space complexity is O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Happy Number
1. Middle of the Linked List
1. Circular Array Loop (conceptual)

______________________________________________________________________

## Medium

4. Linked List Cycle II
1. Find the Duplicate Number
1. Reorder List
1. Circular Queue

______________________________________________________________________

## Hard (Optional)

8. Copy List with Random Pointer
1. LFU Cache
1. Detect Cycles in Directed Graphs

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is understanding **Floyd's Cycle Detection Algorithm**. Instead of remembering
every visited node, you exploit the fact that a faster pointer will inevitably catch a slower one inside a loop. This
elegant combination of **mathematical reasoning** and **pointer manipulation** is one of the most celebrated algorithms
in interview preparation.

______________________________________________________________________

# Next

[34-merge-two-sorted-lists.md](34-merge-two-sorted-lists.md)
