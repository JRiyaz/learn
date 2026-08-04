# 26-queue.md

# Queue — Solving Problems Using First-In, First-Out (FIFO)

## Interview Confidence

**Difficulty:** ⭐⭐☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐☆

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Why Interviewers Ask This

Queues model problems where **the oldest item must be processed first**.

Unlike Stacks (LIFO),

Queues follow **FIFO (First-In, First-Out)**.

Queues appear in:

- Breadth First Search (BFS)
- Task scheduling
- Message brokers
- Rate limiting
- Job processing
- Streaming systems

Understanding queues is essential before learning **Trees**, **Graphs**, and **BFS**.

______________________________________________________________________

# Learning Objectives

After this lesson, you should be able to:

- Understand FIFO.
- Differentiate Queue vs Stack.
- Implement a Queue efficiently in Python.
- Recognize Queue interview problems.
- Understand Monotonic Queues.

______________________________________________________________________

# What Is a Queue?

A Queue is a data structure where:

- New elements enter at the **rear**.
- Oldest elements leave from the **front**.

Think of people waiting in a ticket line.

```
Front

↓

A

B

C

↑

Rear
```

A entered first.

So A leaves first.

______________________________________________________________________

# FIFO Principle

```
Enqueue A

↓

A
```

```
Enqueue B

↓

A

B
```

```
Enqueue C

↓

A

B

C
```

Remove

```
A

↓

B

↓

C
```

First In.

First Out.

______________________________________________________________________

# Real-World Examples

## Printer Queue

```
Job 1

↓

Job 2

↓

Job 3
```

Printer finishes

Job 1 first.

______________________________________________________________________

## Kafka

Messages are consumed in arrival order.

```
Message 1

↓

Message 2

↓

Message 3
```

______________________________________________________________________

## Task Scheduling

Jobs submitted earlier

execute earlier.

______________________________________________________________________

## Customer Support

First customer

gets served first.

______________________________________________________________________

# Queue Operations

## Enqueue

Insert at rear.

```
A

↓

A B

↓

A B C
```

______________________________________________________________________

## Dequeue

Remove front.

```
A B C

↓

B C
```

______________________________________________________________________

## Front (Peek)

See next item.

Don't remove.

______________________________________________________________________

## Is Empty

```
[]
```

Returns

```text
True
```

______________________________________________________________________

# Complexity

| Operation | Complexity |
|-----------|------------|
| Enqueue | O(1) |
| Dequeue | O(1) |
| Peek | O(1) |
| Is Empty | O(1) |

______________________________________________________________________

# Python Implementation

## Wrong

```python
queue = []

queue.append(1)
queue.pop(0)
```

Why?

`pop(0)` shifts every remaining element.

Time

```text
O(n)
```

______________________________________________________________________

## Correct

Use

```python
from collections import deque
```

```python
from collections import deque

queue = deque()

queue.append(10)

queue.append(20)

queue.popleft()
```

Both operations are

```text
O(1)
```

______________________________________________________________________

# Visual Example

```
Front

↓

10

20

30

↑

Rear
```

Dequeue

```
20

30
```

______________________________________________________________________

# Queue vs Stack

| Stack | Queue |
|--------|--------|
| LIFO | FIFO |
| Push | Enqueue |
| Pop | Dequeue |
| Top | Front |
| Latest item processed first | Oldest item processed first |

______________________________________________________________________

# When Should You Think "Queue"?

Interview clues:

- Process in arrival order
- Level by level
- BFS
- Scheduling
- Streaming
- Requests
- Tasks

Think:

```text
Queue
```

______________________________________________________________________

# Types of Queues

## 1. Normal Queue

FIFO.

______________________________________________________________________

## 2. Circular Queue

Reuses freed positions.

Often used in operating systems.

______________________________________________________________________

## 3. Priority Queue

Highest priority removed first.

Implemented using Heaps.

We'll learn this later.

______________________________________________________________________

## 4. Monotonic Queue

Maintains increasing/decreasing order.

Used in

- Sliding Window Maximum
- Stock analysis

______________________________________________________________________

# Backend Analogy

Suppose an e-commerce website receives orders.

```
Order 1

↓

Order 2

↓

Order 3
```

Workers process

Order 1 first.

Exactly FIFO.

Other examples:

- RabbitMQ
- Kafka consumers
- Email queues
- Payment processing
- Notification systems

______________________________________________________________________

# Queue in BFS

Consider a tree.

```
      A
     / \
    B   C
   / \
  D   E
```

Visit

```
A
```

Queue

```
B

C
```

Visit

```
B
```

Queue

```
C

D

E
```

This is Breadth First Search.

______________________________________________________________________

# When NOT to Use Queue

Avoid when:

- Latest item should be processed first.
- Matching nested structures.
- Fast lookup is required.
- Random access is needed.

______________________________________________________________________

# Common Interview Problems

## Easy

- Implement Queue using Stacks

______________________________________________________________________

## Medium

- Number of Recent Calls
- Dota2 Senate
- Rotting Oranges
- Binary Tree Level Order Traversal

______________________________________________________________________

## Hard

- Sliding Window Maximum
- Shortest Path in Binary Matrix

______________________________________________________________________

# Common Mistakes

## 1. Using List Instead of deque

Avoid

```python
pop(0)
```

______________________________________________________________________

## 2. Confusing Queue with Stack

Remember

```
Queue

↓

FIFO
```

______________________________________________________________________

## 3. Forgetting BFS Uses Queue

DFS

↓

Stack

BFS

↓

Queue

______________________________________________________________________

## 4. Using Queue for Priority Problems

Priority Queue

≠

Normal Queue.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Does arrival order matter?
1. Is processing level by level?
1. Is this BFS?
1. Is FIFO required?

______________________________________________________________________

### Common Follow-ups

### Q: Why deque?

Efficient insertion/removal at both ends.

______________________________________________________________________

### Q: Why not Python list?

`pop(0)` is O(n).

______________________________________________________________________

### Q: Stack or Queue for DFS?

Stack.

______________________________________________________________________

### Q: Stack or Queue for BFS?

Queue.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Queue (FIFO) |
| Recognition | Arrival order, BFS, scheduling |
| Operations | Enqueue, Dequeue |
| Python | collections.deque |
| Time | O(1) |

______________________________________________________________________

# Practice Problems

## Easy

1. Implement Queue using Stacks
1. Number of Recent Calls

## Medium

1. Rotting Oranges
1. Binary Tree Level Order Traversal
1. Dota2 Senate
1. Open the Lock

## Hard

1. Sliding Window Maximum
1. Shortest Path in Binary Matrix

______________________________________________________________________

# Quick Revision

- Queue = First In, First Out.
- Enqueue at rear.
- Dequeue from front.
- Use `collections.deque`.
- BFS uses Queue.
- Scheduling systems use Queue.
- Time: **O(1)**.

______________________________________________________________________

# What's Next?

We'll begin with one of the simplest Queue interview problems:

**27-number-of-recent-calls.md**

This introduces the idea of maintaining a rolling set of events using a Queue.

______________________________________________________________________

# Navigation

**Previous**

[25-largest-rectangle-in-histogram.md](25-largest-rectangle-in-histogram.md)

**Next**

[27-number-of-recent-calls.md](27-number-of-recent-calls.md)
