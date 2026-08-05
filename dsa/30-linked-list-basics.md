# 30-linked-list-basics.md

# Linked List Basics (Create, Traverse, Insert & Delete)

> **🎯 This is your first Linked List lesson.**
>
> Don't think of this as learning another data structure.
>
> Think of it as learning **how memory can be connected using references instead of contiguous storage**.
>
> Many interview problems become easy once you truly understand how pointers move.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 30–35 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers are **not** testing whether you can memorize Linked List code.

They want to know whether you understand:

- References (Pointers)
- Dynamic memory
- Node manipulation
- Traversal
- Insert/Delete without shifting
- Pointer updates

Nearly every Linked List interview problem builds upon these fundamentals.

If you understand today's lesson,

then

- Reverse Linked List
- Detect Cycle
- Merge Lists
- Remove Nth Node
- Reorder List

become much easier.

______________________________________________________________________

# Before Learning Linked Lists

## Arrays

An array looks like this.

```
Index

0   1   2   3
```

```
Value

10  20  30  40
```

Memory

```
+----+----+----+----+
|10  |20  |30  |40  |
+----+----+----+----+
```

Everything is stored together.

______________________________________________________________________

Suppose we insert

```
15
```

at the beginning.

```
10

↓

Shift

20

↓

Shift

30

↓

Shift

40
```

Many values move.

Insertion

```
O(n)
```

______________________________________________________________________

# What is a Linked List?

Instead of storing values together,

every value lives inside a **Node**.

Each node stores:

```
Data
```

and

```
Reference to Next Node
```

Example

```
+------+------+
| 10 |  •----|----+
+------+------+
                |
                v
         +------+------+
         | 20 |  •----|----+
         +------+------+
                         |
                         v
                  +------+------+
                  | 30 | None |
                  +------+------+
```

Nodes don't need to be adjacent in memory.

Only the references connect them.

______________________________________________________________________

# Backend Engineering Analogy

Imagine microservices.

Instead of storing everything in one file,

every service knows:

```
Who comes next.
```

Like

```
Auth Service

↓

User Service

↓

Payment Service

↓

Notification Service
```

Each service contains only the address of the next service.

Exactly how a Linked List works.

Other examples:

- Browser Forward Chain
- Playlist
- Undo History
- Blockchain (conceptually chained)
- Free Memory Lists

______________________________________________________________________

# Components of a Linked List

Every node has

```
+------------------+
| Value            |
+------------------+
| Next Pointer     |
+------------------+
```

Example

```
Node

+-----+------+
| 10  |   •------+
+-----+------+
               |
               v
```

______________________________________________________________________

# Head Pointer

The Linked List begins with

```
Head
```

```
Head

↓

10 → 20 → 30 → None
```

Lose the head,

lose the entire list.

______________________________________________________________________

# Tail Node

The last node points to

```
None
```

```
10 → 20 → 30 → None
                ^
              Tail
```

______________________________________________________________________

# Pattern Recognition

## Pattern

**Pointer Manipulation**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Node
- Next
- Previous
- List
- Reverse
- Delete
- Insert

Think

```
Pointers
```

not

```
Indices
```

______________________________________________________________________

# Creating a Linked List

Suppose

```
10

20

30
```

Create three nodes.

```
Node1

↓

10
```

```
Node2

↓

20
```

```
Node3

↓

30
```

Connect

```
10

↓

20

↓

30

↓

None
```

Done.

______________________________________________________________________

# Visual Explanation

```
Head
  |
  v
+----+----+     +----+----+     +----+------+
|10  | •--|---->|20  | •--|---->|30  | None |
+----+----+     +----+----+     +----+------+
```

______________________________________________________________________

# Traversing a Linked List

Traversal means

```
Visit

↓

Every Node
```

Start

```
Current

↓

Head
```

Visit

```
10
```

Move

```
Current

↓

Next
```

Visit

```
20
```

Repeat until

```
Current

=

None
```

______________________________________________________________________

# Dry Run

```
Head

↓

10 → 20 → 30
```

Current

```
10
```

↓

Print

```
10
```

↓

Move

```
20
```

↓

Print

```
20
```

↓

Move

```
30
```

↓

Print

```
30
```

↓

Move

```
None
```

Stop.

______________________________________________________________________

# Inserting at the Beginning

Current

```
10 → 20 → 30
```

New Node

```
5
```

First,

point

```
5

↓

10
```

Then

move head.

```
Head

↓

5 → 10 → 20 → 30
```

______________________________________________________________________

# Visual

Before

```
Head

↓

10 → 20
```

After

```
Head

↓

5 → 10 → 20
```

______________________________________________________________________

# Inserting at the End

Traverse until

```
Next

=

None
```

Current

```
30
```

Attach

```
40
```

```
10 → 20 → 30 → 40
```

______________________________________________________________________

# Inserting After a Node

Suppose

```
10 → 20 → 30
```

Insert

```
25
```

after

```
20
```

Wrong order

```
20

↓

25
```

Oops.

Lost

```
30
```

Correct steps

Save

```
30
```

↓

Point

```
25

↓

30
```

↓

Point

```
20

↓

25
```

Done.

______________________________________________________________________

# Visual

Before

```
10 → 20 → 30
```

After

```
10 → 20 → 25 → 30
```

______________________________________________________________________

# Deleting the First Node

Current

```
Head

↓

10 → 20 → 30
```

Move head.

```
Head

↓

20 → 30
```

Done.

______________________________________________________________________

# Deleting a Middle Node

Current

```
10 → 20 → 30
```

Delete

```
20
```

Instead of

```
20
```

point

```
10

↓

30
```

Now

```
20
```

becomes unreachable.

______________________________________________________________________

# Visual

Before

```
10 → 20 → 30
```

After

```
10 ─────→ 30
```

______________________________________________________________________

# Why Insert/Delete Are Fast

Arrays

```
10 20 30 40
```

Insert

↓

Shift everything.

______________________________________________________________________

Linked List

```
10 → 20 → 30
```

Only change

```
One Pointer
```

No shifting.

______________________________________________________________________

# Why Searching Is Slow

Need

```
30
```

Must visit

```
10

↓

20

↓

30
```

Unlike arrays,

there is no index.

______________________________________________________________________

# Why This Works

Loop Invariant (Traversal):

> Before each iteration, `current` points to the next unvisited node.

Each iteration:

1. Process current node.
1. Move to the next node.

Eventually,

`current` becomes

```
None
```

Every node has been visited exactly once.

______________________________________________________________________

# Edge Cases

### Empty List

```
Head

↓

None
```

______________________________________________________________________

### One Node

```
10
```

______________________________________________________________________

### Insert Into Empty List

New node becomes

```
Head
```

______________________________________________________________________

### Delete Last Node

Need to update the previous node's

```
next

↓

None
```

______________________________________________________________________

# Complexity Analysis

| Operation | Time |
|-----------|------|
| Access by Index | O(n) |
| Search | O(n) |
| Traverse | O(n) |
| Insert at Head | O(1) |
| Delete at Head | O(1) |
| Insert at Tail (without tail pointer) | O(n) |
| Delete at Tail | O(n) |

______________________________________________________________________

# Production-Quality Python

## Node Definition

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    value: int
    next: Optional["ListNode"] = None
```

______________________________________________________________________

## Create a Linked List

```python
head = ListNode(10)
head.next = ListNode(20)
head.next.next = ListNode(30)
```

______________________________________________________________________

## Traverse

```python
def traverse(head: Optional[ListNode]) -> None:
    current = head

    while current:
        print(current.value)
        current = current.next
```

______________________________________________________________________

## Insert at Beginning

```python
def insert_at_head(
    head: Optional[ListNode],
    value: int,
) -> ListNode:
    new_node = ListNode(value)
    new_node.next = head

    return new_node
```

______________________________________________________________________

## Insert at End

```python
def insert_at_tail(
    head: Optional[ListNode],
    value: int,
) -> ListNode:
    new_node = ListNode(value)

    if head is None:
        return new_node

    current = head

    while current.next:
        current = current.next

    current.next = new_node

    return head
```

______________________________________________________________________

## Delete First Node

```python
def delete_head(
    head: Optional[ListNode],
) -> Optional[ListNode]:
    if head is None:
        return None

    return head.next
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Losing the rest of the list.

Always save references before changing pointers.

______________________________________________________________________

## Mistake 2

Forgetting to update `head`.

Especially when inserting or deleting the first node.

______________________________________________________________________

## Mistake 3

Using indices like arrays.

Linked Lists have no random access.

______________________________________________________________________

## Mistake 4

Not checking for `None`.

Always handle empty lists safely.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Unlike arrays, linked lists store elements as nodes connected through references. This allows O(1) insertion and deletion at the head because only pointers change. However, searching and random access require traversal from the head, giving O(n) time. Most linked list problems are solved by carefully manipulating pointers rather than moving data."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use a Linked List instead of an array?**

When frequent insertions and deletions are required.

______________________________________________________________________

**Q. Why is searching O(n)?**

Because nodes don't have indices.

You must traverse sequentially.

______________________________________________________________________

**Q. Why is insertion at the head O(1)?**

Only one pointer (`head`) changes.

______________________________________________________________________

**Q. Where are Linked Lists used in backend systems?**

- LRU Cache
- Memory allocators
- Free lists
- Hash table collision chains
- Browser history
- Undo/Redo systems

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Pointer Manipulation |
| Recognition | Nodes / Next References |
| Main Operations | Traverse, Insert, Delete |
| Insert at Head | O(1) |
| Search | O(n) |
| Random Access | O(n) |

______________________________________________________________________

# Quick Revision

- A linked list is a chain of nodes.
- Every node stores a value and a reference to the next node.
- `head` points to the first node.
- The last node points to `None`.
- Traversal moves node by node.
- Insertions and deletions change pointers, not data.
- Searching requires sequential traversal.
- Pointer updates are the foundation of all linked list problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Design Linked List
1. Remove Linked List Elements
1. Delete Node in a Linked List

______________________________________________________________________

## Medium

4. Remove Nth Node From End of List
1. Odd Even Linked List
1. Partition List
1. Rotate List

______________________________________________________________________

## Hard (Optional)

8. Reverse Nodes in k-Group
1. Merge k Sorted Lists
1. Copy List with Random Pointer

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is that **Linked Lists optimize pointer manipulation instead of indexed access**.
Arrays move data; linked lists move **references**. Once you're comfortable visualizing how pointers change during
insertion and deletion, nearly every linked list interview problem becomes much easier to reason about.

______________________________________________________________________

# Next

[31-reverse-linked-list.md](31-reverse-linked-list.md)
