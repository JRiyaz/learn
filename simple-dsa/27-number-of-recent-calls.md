# 27-number-of-recent-calls.md

# Number of Recent Calls — The Rolling Queue Pattern

## Interview Confidence

**Difficulty:** ⭐☆☆☆☆

**Asked Frequency:** ⭐⭐⭐☆☆

**Importance:** ⭐⭐⭐⭐☆

**Expected Interview Time:** 10–15 minutes

**Revision Time:** 3 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Implement a class `RecentCounter`.

Each function call receives a timestamp `t`.

Return the number of requests made during the last **3000 milliseconds**, including the current request.

Specifically, count all requests in the range:

```text
[t - 3000, t]
```

It is guaranteed that every new timestamp is greater than the previous timestamp.

______________________________________________________________________

### Example

```text
Input

ping(1)

Output

1
```

______________________________________________________________________

```text
Input

ping(100)

Output

2
```

______________________________________________________________________

```text
Input

ping(3001)

Output

3
```

______________________________________________________________________

```text
Input

ping(3002)

Output

3
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> Keep only the requests that occurred during the last 3000 milliseconds.

Older requests are no longer useful.

They should be removed.

______________________________________________________________________

# Real-World Analogy

Imagine an API Gateway.

Requests arrive at:

```text
1000

2000

2500

6000
```

When request

```text
6000
```

arrives,

requests before

```text
3000
```

are no longer relevant.

Exactly the same idea.

Other examples:

- Rate limiting
- Recent notifications
- Monitoring systems
- Streaming analytics

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Recent
- Last K seconds
- Rolling window
- Streaming
- Requests

Think:

```text
Queue
```

______________________________________________________________________

# Brute Force Solution

Store every request forever.

For every new request,

scan all previous timestamps.

Count valid ones.

______________________________________________________________________

## Complexity

Time

```text
O(n)
```

per request.

Too slow.

______________________________________________________________________

# Optimal Solution

## Key Insight

Timestamps are strictly increasing.

That means:

The oldest request is always at the front.

Whenever a request becomes too old,

remove it.

Exactly FIFO.

Exactly a Queue.

______________________________________________________________________

# Visual Explanation

Queue

```
1

100

3001
```

New request

```text
3002
```

Valid interval

```text
[2,3002]
```

Remove

```text
1
```

Queue becomes

```
100

3001

3002
```

Answer

```text
3
```

______________________________________________________________________

# Step-by-Step Algorithm

When a new request arrives:

1. Add timestamp.
1. Remove timestamps older than:

```text
t - 3000
```

3. Queue size is the answer.

______________________________________________________________________

# Dry Run

Request

```text
1
```

Queue

```
1
```

Answer

```text
1
```

______________________________________________________________________

Request

```text
100
```

Queue

```
1

100
```

Answer

```text
2
```

______________________________________________________________________

Request

```text
3001
```

Queue

```
1

100

3001
```

All valid.

Answer

```text
3
```

______________________________________________________________________

Request

```text
3002
```

Valid interval

```text
[2,3002]
```

Remove

```text
1
```

Queue

```
100

3001

3002
```

Answer

```text
3
```

______________________________________________________________________

# Why This Works

Because timestamps always increase,

once a request becomes too old,

it will never become valid again.

So it is safe to permanently remove it.

______________________________________________________________________

# Edge Cases

## First Request

Queue empty.

Answer

```text
1
```

______________________________________________________________________

## Exactly 3000 ms Apart

Keep it.

Interval is inclusive.

______________________________________________________________________

## Many Requests

Still efficient.

Old requests leave only once.

______________________________________________________________________

# Complexity Analysis

Suppose

```text
n
```

requests arrive.

Every request:

- enters once
- leaves once

Total work

```text
O(n)
```

Therefore,

each request is

```text
O(1)
```

amortized.

______________________________________________________________________

## Space

Worst case

All requests occur within

3000 ms.

```text
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from collections import deque


class RecentCounter:
    """
    Counts requests received
    during the last 3000 milliseconds.

    Time Complexity:
        O(1) amortized per ping()

    Space Complexity:
        O(n)
    """

    def __init__(self) -> None:
        self.requests = deque()

    def ping(self, t: int) -> int:
        self.requests.append(t)

        while self.requests[0] < t - 3000:
            self.requests.popleft()

        return len(self.requests)
```

______________________________________________________________________

# Why Amortized O(1)?

Interviewers often ask this.

Suppose

```text
1000 requests
```

Every request

- enters once
- leaves once

No request is removed twice.

Total queue operations

```text
2n
```

Therefore

Average work per request

```text
O(1)
```

This is called **amortized analysis**.

______________________________________________________________________

# Common Mistakes

## 1. Scanning Every Request

Unnecessary.

Old requests are permanently useless.

______________________________________________________________________

## 2. Using a List

Avoid

```python
pop(0)
```

Use

```python
deque
```

______________________________________________________________________

## 3. Removing Only One Request

There may be multiple expired requests.

Always use

```python
while
```

______________________________________________________________________

## 4. Forgetting the Interval Is Inclusive

Keep requests satisfying:

```text
t >= current - 3000
```

______________________________________________________________________

# Variations

## Medium

- Sliding Window Maximum
- Moving Average from Data Stream
- Hit Counter
- Logger Rate Limiter

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Data arrives in chronological order.
1. Old data never becomes useful again.
1. Queue naturally stores requests in arrival order.
1. Remove expired requests.
1. Queue size is the answer.

______________________________________________________________________

### Common Follow-ups

### Q: Why Queue?

Oldest request expires first.

FIFO.

______________________________________________________________________

### Q: Why amortized O(1)?

Each timestamp enters once and leaves once.

______________________________________________________________________

### Q: Why deque?

Constant-time insertion and removal from both ends.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Rolling Queue |
| Recognition | Recent events, streaming, last K seconds |
| Store | Timestamps |
| Time | O(1) amortized |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Easy

1. Moving Average from Data Stream
1. Design Circular Queue

## Medium

1. Hit Counter
1. Logger Rate Limiter
1. Dota2 Senate
1. Sliding Window Maximum

## Hard

1. Shortest Subarray with Sum at Least K
1. Constrained Subsequence Sum

______________________________________________________________________

# Quick Revision

- Queue stores timestamps.
- Oldest request is at the front.
- Remove expired requests using `while`.
- Queue size equals the answer.
- Use `collections.deque`.
- Time: **O(1)** amortized.
- Space: **O(n)**.

______________________________________________________________________

# Key Takeaway

This problem introduces the **Rolling Queue Pattern**.

The invariant is:

> **The queue always contains only the requests that are still inside the valid time window.**

This same idea is used in:

- Rate limiters
- Streaming analytics
- Monitoring dashboards
- Time-series databases
- Event processing systems

______________________________________________________________________

# Navigation

**Previous**

[26-queue.md](26-queue.md)

**Next**

[28-binary-tree-level-order-traversal.md](28-binary-tree-level-order-traversal.md)
