# 32-middle-of-linked-list.md

# Middle of the Linked List

> **🎯 This lesson introduces one of the most powerful interview techniques:**
>
> **Fast and Slow Pointers (Tortoise and Hare Algorithm)**
>
> This single pattern is used in:
>
> - Middle of Linked List
> - Detect Cycle
> - Happy Number
> - Find Start of Cycle
> - Palindrome Linked List
> - Reorder List
> - Split Linked List

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 15–20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Most beginners solve this problem in **two traversals**:

1. Count nodes.
1. Traverse again to the middle.

It works.

Interviewers then ask:

> "Can you do it in one pass?"

The expected solution uses two pointers moving at different speeds.

This is one of the most elegant techniques in DSA.

______________________________________________________________________

# Problem Statement

Given the head of a singly linked list,

return the **middle node**.

If there are two middle nodes,

return the **second** middle node.

______________________________________________________________________

## Example 1

Input

```text
1 → 2 → 3 → 4 → 5
```

Output

```text
3
```

______________________________________________________________________

## Example 2

Input

```text
1 → 2 → 3 → 4 → 5 → 6
```

Output

```text
4
```

Notice

There are two middle nodes

```
3

4
```

Return

```
4
```

______________________________________________________________________

# Simple English

Imagine two runners on a track.

Runner A

```
Walks

1 step
```

Runner B

```
Runs

2 steps
```

When Runner B reaches the finish line,

Runner A will naturally be standing in the middle.

That is exactly how this algorithm works.

______________________________________________________________________

# Backend Engineering Analogy

Imagine processing a queue of events.

One monitoring process examines:

```
Every Event
```

Another examines:

```
Every Second Event
```

When the faster process reaches the end,

the slower process is automatically positioned halfway through the stream.

This idea appears in:

- Streaming systems
- Cycle detection
- Distributed algorithms
- Memory management

______________________________________________________________________

# Pattern Recognition

## Pattern

**Fast & Slow Pointers**

______________________________________________________________________

## Recognition Clues

Whenever you see:

- Middle
- Halfway
- Cycle
- Split
- Meeting point
- One pass

Think

```
Slow Pointer

1 Step
```

```
Fast Pointer

2 Steps
```

______________________________________________________________________

# Brute Force Solution

## Intuition

First,

count the nodes.

Second,

walk to

```
Count / 2
```

______________________________________________________________________

## Algorithm

Example

```text
1 → 2 → 3 → 4 → 5
```

Count

```
5
```

Middle

```
5 // 2

=

2
```

Move

```
2
```

steps.

Answer

```
3
```

______________________________________________________________________

## Dry Run

```text
1 → 2 → 3 → 4
```

Count

```
4
```

Middle

```
4 // 2

=

2
```

Move

```
2
```

steps.

Return

```
3
```

(second middle)

______________________________________________________________________

## Complexity

First traversal

```
O(n)
```

Second traversal

```
O(n)
```

Overall

```
O(n)
```

Space

```
O(1)
```

Works,

but requires two passes.

______________________________________________________________________

# Better Observation

Can we find the middle while traversing only once?

Yes.

Use two pointers.

______________________________________________________________________

# Optimized Solution (Fast & Slow Pointers)

## Key Insight

Move

```
Slow

↓

1 Step
```

Move

```
Fast

↓

2 Steps
```

When

```
Fast

↓

End
```

Slow is automatically at the middle.

______________________________________________________________________

# Understanding the Pointers

Initially

```text
1 → 2 → 3 → 4 → 5
```

Both

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

## Iteration 1

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

## Iteration 2

Slow

↓

```
3
```

Fast

↓

```
5
```

______________________________________________________________________

Fast cannot move further.

Stop.

Slow

↓

```
3
```

Answer.

______________________________________________________________________

# Dry Run (Even Length)

```text
1 → 2 → 3 → 4 → 5 → 6
```

Initially

```
S

↓

1
```

```
F

↓

1
```

______________________________________________________________________

Iteration 1

```
S

↓

2
```

```
F

↓

3
```

______________________________________________________________________

Iteration 2

```
S

↓

3
```

```
F

↓

5
```

______________________________________________________________________

Iteration 3

```
S

↓

4
```

```
F

↓

None
```

Return

```
4
```

(second middle)

______________________________________________________________________

# Visual Explanation

Odd Length

```text
1 → 2 → 3 → 4 → 5
```

```
S
F
```

↓

```text
1 → 2 → 3 → 4 → 5

    S
        F
```

↓

```text
1 → 2 → 3 → 4 → 5

        S
                F
```

Done.

______________________________________________________________________

Even Length

```text
1 → 2 → 3 → 4 → 5 → 6
```

↓

```text
S

F
```

↓

```text
    S

        F
```

↓

```text
        S

                F
```

↓

```text
            S

                    F
```

Answer

```
4
```

______________________________________________________________________

# Why Does This Work?

Suppose

```
Fast

=

2 × Slow
```

When Fast reaches

```
n
```

nodes,

Slow has moved

```
n / 2
```

nodes.

Exactly the middle.

This is why the algorithm works without explicitly counting anything.

______________________________________________________________________

# Loop Invariant

> Before each iteration:
>
> - `slow` has moved `k` steps.
> - `fast` has moved `2k` steps.

When `fast` reaches the end,

`slow` has traveled exactly half the distance.

______________________________________________________________________

# Why Do We Return the Second Middle?

Interviewers often ask this.

Condition

```python
while fast and fast.next:
```

causes the slow pointer to advance one final time when the list length is even.

Therefore,

the slow pointer lands on the **second** middle node.

______________________________________________________________________

# Edge Cases

### Empty List

```text
None
```

Return

```text
None
```

______________________________________________________________________

### One Node

```text
1
```

Return

```
1
```

______________________________________________________________________

### Two Nodes

```text
1 → 2
```

Return

```
2
```

(second middle)

______________________________________________________________________

### Large List

Still requires only one traversal.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n)
```

(two passes)

Space

```
O(1)
```

______________________________________________________________________

## Optimized

Time

```
O(n)
```

(one pass)

Space

```
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    value: int
    next: Optional["ListNode"] = None


def middle_node(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow
```

______________________________________________________________________

# Alternative (Two Passes)

```python
def middle_node(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    count = 0
    current = head

    while current:
        count += 1
        current = current.next

    middle = count // 2

    current = head

    for _ in range(middle):
        current = current.next

    return current
```

Works,

but not preferred.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Moving both pointers one step.

Then both reach the end together.

No middle is found.

______________________________________________________________________

## Mistake 2

Using

```python
while fast:
```

instead of

```python
while fast and fast.next:
```

This may cause

```python
fast.next.next
```

to access `None`.

______________________________________________________________________

## Mistake 3

Thinking this works only for linked lists.

The Fast & Slow Pointer pattern also appears in:

- Cycle detection
- Arrays
- Number sequences

______________________________________________________________________

## Mistake 4

Returning the first middle when the problem expects the second.

Always read the problem carefully.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A straightforward solution counts the nodes and then traverses again to the middle. However, that requires two passes. Instead, I can use two pointers: a slow pointer that moves one node at a time and a fast pointer that moves two nodes at a time. When the fast pointer reaches the end of the list, the slow pointer will be at the middle. This gives a clean one-pass solution with O(1) extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why does the slow pointer end up in the middle?**

Because it moves half as fast as the fast pointer.

______________________________________________________________________

**Q. Why check both `fast` and `fast.next`?**

To safely move the fast pointer two steps.

______________________________________________________________________

**Q. Why return the second middle?**

The loop condition naturally advances the slow pointer one extra step for even-length lists.

______________________________________________________________________

**Q. Where is this pattern used?**

- Detecting cycles
- Finding cycle entry
- Palindrome Linked List
- Splitting lists
- Happy Number

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Fast & Slow Pointers |
| Recognition | Middle / Halfway / Cycle |
| Brute Force | Count + Traverse |
| Optimized | Two Pointers |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Use two pointers.
- Slow moves one step.
- Fast moves two steps.
- When fast reaches the end, slow reaches the middle.
- Requires only one traversal.
- Time complexity is O(n).
- Space complexity is O(1).
- This pattern is reused in many linked list interview problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Linked List Cycle
1. Happy Number
1. Remove Nth Node From End of List

______________________________________________________________________

## Medium

4. Palindrome Linked List
1. Reorder List
1. Split Linked List in Parts
1. Delete the Middle Node of a Linked List

______________________________________________________________________

## Hard (Optional)

8. Linked List Cycle II
1. Copy List with Random Pointer
1. Reverse Nodes in k-Group

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is mastering the **Fast & Slow Pointer** pattern. By moving two pointers at
different speeds, you can determine relative positions—such as the middle of a list—without counting elements or making
multiple passes. This elegant idea is one of the highest-value pointer techniques in coding interviews.

______________________________________________________________________

# Next

[33-linked-list-cycle.md](33-linked-list-cycle.md)
