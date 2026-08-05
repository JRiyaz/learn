# 34-merge-two-sorted-lists.md

# Merge Two Sorted Lists

> **🎯 This lesson combines everything you've learned about Linked Lists.**
>
> You'll use:
>
> - Pointer Manipulation
> - Traversal
> - Dummy Node
> - Incremental Construction
>
> This is one of the most frequently asked Linked List interview questions because it tests whether you can manipulate pointers without creating unnecessary complexity.

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

This problem tests whether you can:

- Traverse two linked lists simultaneously
- Manipulate pointers safely
- Avoid unnecessary node creation
- Build a new linked list incrementally
- Handle edge cases like empty lists

The exact same idea is used in:

- Merge Sort
- External Sorting
- Database merge operations
- SSTable Compaction
- Kafka log compaction
- File merging

______________________________________________________________________

# Problem Statement

You are given the heads of two **sorted** linked lists.

Merge them into a **single sorted linked list**.

The merged list should consist of the **existing nodes**, not newly created data nodes.

Return the head of the merged list.

______________________________________________________________________

## Example

### Input

```text
List 1

1 → 2 → 4
```

```text
List 2

1 → 3 → 4
```

### Output

```text
1 → 1 → 2 → 3 → 4 → 4
```

______________________________________________________________________

# Before Learning the Algorithm

## Why Not Copy Values?

One approach is:

- Read every value.
- Store them in an array.
- Sort.
- Create a new linked list.

It works.

But interviewers expect you to reuse the existing nodes.

This saves both memory and time.

______________________________________________________________________

# Simple English

Imagine two queues of customers already sorted by token number.

```
Queue A

1

2

4
```

```
Queue B

1

3

4
```

Instead of asking everyone to stand in a new queue,

simply connect the next smallest customer to the result.

______________________________________________________________________

# Backend Engineering Analogy

Suppose two database shards each return sorted records.

```
Shard A

100

200

400
```

```
Shard B

100

300

400
```

To produce one sorted response,

the query engine repeatedly chooses the smaller current record.

Exactly the same algorithm.

This is also how:

- Merge Sort
- Log Compaction
- External Sorting
- Storage Engines

merge sorted data.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Two Pointers + Dummy Node**

______________________________________________________________________

## Recognition Clues

Whenever you see:

- Two sorted linked lists
- Merge
- Reuse nodes
- Maintain order

Think

```
Two Pointers
```

plus

```
Dummy Node
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Traverse both lists.

Store all values.

Sort them.

Create a new linked list.

______________________________________________________________________

## Algorithm

Input

```text
1 → 2 → 4

1 → 3 → 4
```

Store

```text
[1,2,4,1,3,4]
```

Sort

```text
[1,1,2,3,4,4]
```

Create a new list.

______________________________________________________________________

## Complexity

Traversal

```
O(m+n)
```

Sorting

```
O((m+n) log(m+n))
```

Space

```
O(m+n)
```

Not ideal.

______________________________________________________________________

# Better Observation

Both lists are **already sorted**.

Why sort again?

Simply compare the current nodes.

______________________________________________________________________

# Optimized Solution

## Key Insight

Keep one pointer on each list.

Always choose the smaller node.

Append it to the merged list.

Move that pointer forward.

Repeat until one list finishes.

______________________________________________________________________

# Why Use a Dummy Node?

Without a dummy node,

the first insertion becomes a special case.

Example

Without dummy

```python
if head is None:
    head = node
```

Special logic.

______________________________________________________________________

With dummy

```
Dummy

↓

0
```

Every insertion becomes identical.

At the end,

ignore the dummy.

Return

```
dummy.next
```

______________________________________________________________________

# Understanding the Pointers

Initially

```text
List A

1 → 2 → 4
```

```text
List B

1 → 3 → 4
```

Dummy

```text
0
```

Tail

↓

```
0
```

______________________________________________________________________

Compare

```
1

1
```

Choose either.

Suppose

Left.

Result

```text
0 → 1
```

Move

Left Pointer.

______________________________________________________________________

Compare

```
2

1
```

Choose

Right.

Result

```text
0 → 1 → 1
```

Move

Right Pointer.

______________________________________________________________________

Compare

```
2

3
```

Choose

Left.

Continue.

______________________________________________________________________

# Complete Dry Run

Input

```text
L1

1 → 2 → 4
```

```text
L2

1 → 3 → 4
```

______________________________________________________________________

Step 1

Merged

```text
0 → 1
```

______________________________________________________________________

Step 2

```text
0 → 1 → 1
```

______________________________________________________________________

Step 3

```text
0 → 1 → 1 → 2
```

______________________________________________________________________

Step 4

```text
0 → 1 → 1 → 2 → 3
```

______________________________________________________________________

Step 5

```text
0 → 1 → 1 → 2 → 3 → 4
```

______________________________________________________________________

List 2 finished.

Append remaining

```
4
```

Final

```text
1 → 1 → 2 → 3 → 4 → 4
```

______________________________________________________________________

# Visual Explanation

Before

```text
L1

1 → 2 → 4
```

```text
L2

1 → 3 → 4
```

↓

Dummy

```text
0
```

↓

```text
0 → 1
```

↓

```text
0 → 1 → 1
```

↓

```text
0 → 1 → 1 → 2
```

↓

```text
0 → 1 → 1 → 2 → 3
```

↓

```text
0 → 1 → 1 → 2 → 3 → 4 → 4
```

Return

```
dummy.next
```

______________________________________________________________________

# Why Dummy Nodes Are So Popular

Without Dummy

```
First insertion

↓

Special Case
```

With Dummy

```
Every insertion

↓

Same Code
```

Dummy nodes simplify many linked list algorithms:

- Merge Lists
- Partition List
- Remove Duplicates
- Swap Nodes
- Reverse Between

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before each iteration:
>
> - The merged list is already sorted.
> - `tail` points to its last node.
> - `list1` and `list2` still point to the smallest remaining elements in their respective lists.

Each iteration chooses the smaller current node.

Since both lists are sorted,

the chosen node is guaranteed to be the next smallest overall.

______________________________________________________________________

# What Happens When One List Ends?

Example

```text
L1

1 → 2
```

```text
L2

3 → 4 → 5
```

After merging

```text
1 → 2
```

List 1 finishes.

Remaining list

```
3 → 4 → 5
```

is already sorted.

Simply connect it.

No comparisons needed.

______________________________________________________________________

# Edge Cases

### First List Empty

```text
None

1 → 2
```

Return second list.

______________________________________________________________________

### Second List Empty

Return first list.

______________________________________________________________________

### Both Empty

Return

```
None
```

______________________________________________________________________

### Duplicate Values

Handled naturally.

______________________________________________________________________

### Different Lengths

Works correctly.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O((m+n) log(m+n))
```

Space

```
O(m+n)
```

______________________________________________________________________

## Optimized

Time

```
O(m+n)
```

Each node is visited once.

Space

```
O(1)
```

No additional nodes are created (excluding the dummy node).

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


def merge_two_lists(
    list1: Optional[ListNode],
    list2: Optional[ListNode],
) -> Optional[ListNode]:
    dummy = ListNode(0)
    tail = dummy

    while list1 and list2:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next

        tail = tail.next

    if list1:
        tail.next = list1
    else:
        tail.next = list2

    return dummy.next
```

______________________________________________________________________

# Recursive Solution

Some interviewers also like the recursive version.

```python
def merge_two_lists(
    list1: Optional[ListNode],
    list2: Optional[ListNode],
) -> Optional[ListNode]:
    if not list1:
        return list2

    if not list2:
        return list1

    if list1.value <= list2.value:
        list1.next = merge_two_lists(
            list1.next,
            list2,
        )
        return list1

    list2.next = merge_two_lists(
        list1,
        list2.next,
    )

    return list2
```

Elegant,

but uses recursion stack.

The iterative solution is generally preferred.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Creating entirely new nodes.

Reuse the existing ones.

______________________________________________________________________

## Mistake 2

Forgetting to move `tail`.

The merged list stops growing.

______________________________________________________________________

## Mistake 3

Forgetting to append the remaining list.

Some nodes are lost.

______________________________________________________________________

## Mistake 4

Returning `dummy` instead of `dummy.next`.

The dummy node is not part of the answer.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Both lists are already sorted, so I don't need to sort again. I'll maintain pointers into both lists and repeatedly choose the smaller current node. A dummy node simplifies the implementation because I don't need special handling for the first insertion. Once one list is exhausted, I simply attach the remaining nodes from the other list."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use a dummy node?**

It removes special-case logic for the first node.

______________________________________________________________________

**Q. Why can we append the remaining list directly?**

Because it is already sorted.

______________________________________________________________________

**Q. Why reuse nodes instead of creating new ones?**

It saves memory and matches the interview requirement.

______________________________________________________________________

**Q. Where is this used in backend systems?**

- Merge Sort
- Database query engines
- Storage engines
- Log compaction
- External sorting

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Two Pointers + Dummy Node |
| Recognition | Merge Sorted Linked Lists |
| Brute Force | Copy + Sort |
| Optimized | Pointer Manipulation |
| Time | O(m+n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- The lists are already sorted.
- Compare the current nodes.
- Append the smaller node.
- Move the corresponding pointer.
- Move the tail pointer.
- Append the remaining list.
- Return `dummy.next`.
- Time complexity is O(m+n).

______________________________________________________________________

# Practice Questions

## Easy

1. Merge Sorted Array
1. Intersection of Two Linked Lists
1. Remove Duplicates from Sorted List

______________________________________________________________________

## Medium

4. Merge k Sorted Lists
1. Sort List
1. Partition List
1. Odd Even Linked List

______________________________________________________________________

## Hard (Optional)

8. Reverse Nodes in k-Group
1. Merge k Sorted Arrays
1. External Merge Sort

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning to **build a linked list incrementally using a dummy node**. Dummy
nodes eliminate edge cases, and the **compare → attach → advance** pattern appears repeatedly in linked list algorithms,
merge sort, and many backend data-processing systems.

______________________________________________________________________

# Next

[35-binary-search.md](35-binary-search.md)
