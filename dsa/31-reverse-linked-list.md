# 31-reverse-linked-list.md

# Reverse Linked List

> **🎯 This is the most important Linked List interview problem.**
>
> Almost every Linked List interview question is based on the same pointer manipulation you'll learn here.
>
> If you master this lesson, problems like:
>
> - Reverse Linked List II
> - Reverse Nodes in k-Group
> - Palindrome Linked List
> - Reorder List
> - Reverse Between
>
> become significantly easier.

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

Interviewers are **not** testing whether you can reverse a list.

They are testing whether you can safely manipulate pointers without losing data.

This problem evaluates:

- Pointer manipulation
- Reference handling
- Iterative thinking
- Temporary variables
- Memory safety

Most candidates know the algorithm.

Many still fail because they lose the remaining list while changing pointers.

______________________________________________________________________

# Problem Statement

Given the head of a singly linked list,

reverse the linked list.

Return the new head.

______________________________________________________________________

## Example

Input

```text
1 → 2 → 3 → 4 → 5 → None
```

Output

```text
5 → 4 → 3 → 2 → 1 → None
```

______________________________________________________________________

# Simple English

Imagine a line of people holding hands.

```
1 → 2 → 3 → 4
```

Every person is pointing to the next person.

Your job is to make everyone turn around.

```
4 → 3 → 2 → 1
```

The difficult part:

Don't break the chain while turning people around.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a workflow.

```
Service A

↓

Service B

↓

Service C

↓

Service D
```

You want

```
Service D

↓

Service C

↓

Service B

↓

Service A
```

If you immediately reverse the first connection,

you lose access to the remaining services.

Therefore,

you first save the next reference,

then reverse the pointer.

Exactly what we do in a linked list.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Pointer Reversal**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Reverse Linked List
- Reverse k Nodes
- Reverse Between
- Reorder List

Think

```
Three Pointers
```

______________________________________________________________________

# Why Arrays Are Easier

Array

```
1 2 3 4
```

Reverse

```
4 3 2 1
```

Swap values.

Done.

______________________________________________________________________

Linked List

```
1 → 2 → 3 → 4
```

There are no indices.

You must reverse the **arrows**.

______________________________________________________________________

# First Important Observation

Every node stores

```
Current

↓

Next
```

To reverse,

we want

```
Current

↓

Previous
```

Simple?

Not quite.

If we immediately change

```
1 → 2
```

into

```
1 → None
```

We've lost

```
2 → 3 → 4
```

forever.

Need a temporary variable.

______________________________________________________________________

# Brute Force Solution

## Intuition

Store all node values.

Reverse them.

Create a new linked list.

______________________________________________________________________

## Algorithm

Traverse

```
1

2

3

4
```

Store

```
[1,2,3,4]
```

Reverse

```
[4,3,2,1]
```

Create a new list.

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

## Limitations

Creates a new list.

Interview expects in-place reversal.

______________________________________________________________________

# Optimized Solution (Three Pointers)

## Key Insight

Use three pointers:

```
Previous
```

```
Current
```

```
Next
```

At every step:

1. Save next.
1. Reverse pointer.
1. Move forward.

______________________________________________________________________

# Understanding the Three Pointers

Initially

```
Previous

↓

None
```

```
Current

↓

1
```

```
Next

↓

2
```

List

```
1 → 2 → 3 → 4
```

______________________________________________________________________

## Step 1

Save

```
Next

↓

2
```

Reverse

```
1 → None
```

Move

```
Previous

↓

1
```

```
Current

↓

2
```

______________________________________________________________________

## Step 2

Save

```
3
```

Reverse

```
2 → 1
```

Move

```
Previous

↓

2
```

```
Current

↓

3
```

Current list

```text
2 → 1 → None

3 → 4 → None
```

______________________________________________________________________

## Step 3

Save

```
4
```

Reverse

```
3 → 2
```

Move.

______________________________________________________________________

## Step 4

Reverse

```
4 → 3
```

Done.

______________________________________________________________________

# Complete Dry Run

Original

```text
1 → 2 → 3 → 4 → None
```

Iteration 1

```text
Previous = None
Current = 1
Next = 2

Reverse

1 → None
```

______________________________________________________________________

Iteration 2

```text
Previous = 1
Current = 2
Next = 3

Reverse

2 → 1
```

______________________________________________________________________

Iteration 3

```text
Previous = 2
Current = 3
Next = 4

Reverse

3 → 2
```

______________________________________________________________________

Iteration 4

```text
Previous = 3
Current = 4
Next = None

Reverse

4 → 3
```

Finished

```text
4 → 3 → 2 → 1 → None
```

______________________________________________________________________

# Visual Explanation

Before

```text
Head
 |
 v

1 → 2 → 3 → 4 → None
```

______________________________________________________________________

After first iteration

```text
1 → None

2 → 3 → 4
```

______________________________________________________________________

After second

```text
2 → 1 → None

3 → 4
```

______________________________________________________________________

After third

```text
3 → 2 → 1 → None

4
```

______________________________________________________________________

Final

```text
4 → 3 → 2 → 1 → None
```

______________________________________________________________________

# Why Is the Temporary Pointer Necessary?

This is the biggest mistake beginners make.

Wrong

```text
Current.next = Previous
```

Immediately.

Now

```
Current.next
```

has changed.

You lost the original next node.

Correct order

```
Save Next

↓

Reverse

↓

Move Forward
```

Never change the pointer before saving it.

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before each iteration:
>
> - `previous` points to the already reversed portion.
> - `current` points to the first node not yet processed.
> - The remaining nodes are still connected in their original order.

Every iteration:

1. Removes one node from the unreversed list.
1. Adds it to the front of the reversed list.

Eventually,

the unreversed list becomes empty,

and `previous` points to the completely reversed list.

______________________________________________________________________

# Recursive Solution

Recursion also works.

Idea

```
Reverse

↓

Smaller List

↓

Attach Current
```

Example

```
1 → 2 → 3
```

Reverse

```
2 → 3
```

Result

```
3 → 2
```

Attach

```
1
```

Final

```
3 → 2 → 1
```

Although elegant,

most interviewers prefer the iterative solution.

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

```text
1
```

______________________________________________________________________

### Two Nodes

```text
1 → 2
```

↓

```text
2 → 1
```

______________________________________________________________________

### Large List

Still processes one node at a time.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Optimized

Time

```
O(n)
```

Every node is visited once.

Space

```
O(1)
```

Only three pointers are used.

______________________________________________________________________

## Recursive

Time

```
O(n)
```

Space

```
O(n)
```

because of the recursion call stack.

______________________________________________________________________

# Production-Quality Python

## Iterative (Recommended)

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    value: int
    next: Optional["ListNode"] = None


def reverse_list(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    previous = None
    current = head

    while current:
        next_node = current.next

        current.next = previous

        previous = current
        current = next_node

    return previous
```

______________________________________________________________________

## Recursive

```python
def reverse_list(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    if head is None or head.next is None:
        return head

    new_head = reverse_list(head.next)

    head.next.next = head
    head.next = None

    return new_head
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Not saving the next node.

You lose the rest of the list.

______________________________________________________________________

## Mistake 2

Updating pointers in the wrong order.

Correct sequence:

```
Save Next

↓

Reverse Pointer

↓

Move Previous

↓

Move Current
```

______________________________________________________________________

## Mistake 3

Returning `current`.

After completion,

`current` is `None`.

The new head is `previous`.

______________________________________________________________________

## Mistake 4

Thinking values are reversed.

We're reversing **links**, not node values.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A straightforward solution stores values and creates a new list, but that uses O(n) extra space. Since the problem asks for in-place reversal, I'll use three pointers: `previous`, `current`, and `next`. Before changing any pointers, I save the next node. Then I reverse the current node's link, move all three pointers forward, and repeat until the list is fully reversed."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why are three pointers needed?**

To avoid losing the rest of the list while reversing links.

______________________________________________________________________

**Q. Why return `previous`?**

Because after the loop,

`previous` points to the new head.

______________________________________________________________________

**Q. Why isn't recursion preferred?**

It uses O(n) stack space and may cause stack overflow for very large lists.

______________________________________________________________________

**Q. Where is pointer reversal used in backend systems?**

The underlying pointer manipulation concepts appear in:

- Memory allocators
- Cache eviction structures
- Linked data structures
- Graph algorithms

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Pointer Reversal |
| Recognition | Reverse Linked Structure |
| Brute Force | Create New List |
| Optimized | Three Pointers |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Reverse links, not values.
- Use `previous`, `current`, and `next`.
- Always save the next node first.
- Reverse one pointer at a time.
- Move all pointers forward.
- Return `previous`, not `current`.
- Time complexity is O(n).
- Space complexity is O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Reverse Linked List II (Intro)
1. Palindrome Linked List
1. Remove Linked List Elements

______________________________________________________________________

## Medium

4. Reorder List
1. Swap Nodes in Pairs
1. Reverse Nodes in k-Group
1. Rotate List

______________________________________________________________________

## Hard (Optional)

8. Reverse Nodes in Even Length Groups
1. Merge k Sorted Lists
1. Copy List with Random Pointer

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning **safe pointer manipulation**. Before changing any pointer, always
preserve the information you'll need next. The pattern of **save → modify → advance** is one of the most fundamental
techniques in linked list algorithms and appears repeatedly in both interviews and systems programming.

______________________________________________________________________

# Next

[32-middle-of-linked-list.md](32-middle-of-linked-list.md)
