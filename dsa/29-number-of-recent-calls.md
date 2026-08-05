# 29-number-of-recent-calls.md

# Number of Recent Calls

> **🎯 This is your first Queue problem.**
>
> The goal is **not** to count calls.
>
> The real lesson is learning when data should leave in the **same order it arrived**.
>
> That's exactly what a **Queue (FIFO)** is designed for.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐☆ Medium |
| Importance | ⭐⭐⭐⭐☆ |
| Expected Interview Time | 15–20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem teaches one of the most important streaming patterns.

Interviewers want to know whether you understand:

- Queue (FIFO)
- Sliding Time Window
- Streaming Data
- Continuous Processing
- Removing expired data

Unlike Stack problems,

here we always remove the **oldest** element.

This pattern appears everywhere in backend engineering:

- API Rate Limiting
- Monitoring systems
- Streaming analytics
- Kafka consumers
- Metrics aggregation
- Real-time dashboards

______________________________________________________________________

# Problem Statement

Implement a class `RecentCounter`.

Each time `ping(time)` is called,

return the number of requests received during the last

```text
3000 milliseconds
```

inclusive.

That means,

count all requests in

```text
[time - 3000, time]
```

The input times are strictly increasing.

______________________________________________________________________

## Example

```text
Operations

ping(1)

ping(100)

ping(3001)

ping(3002)
```

Outputs

```text
1

2

3

3
```

______________________________________________________________________

# Understanding the Problem

When

```text
ping(3002)
```

arrives,

only requests between

```text
2

and

3002
```

should remain.

Old requests are discarded.

______________________________________________________________________

# Simple English

Imagine a supermarket.

Customers enter in this order:

```
1

100

3001

3002
```

At time

```
3002
```

we only care about customers who entered during the last

```
3000
```

milliseconds.

Older customers leave the queue.

______________________________________________________________________

# Backend Engineering Analogy

Imagine an API Gateway.

Every incoming request timestamp is stored.

To enforce a rate limit:

```
Maximum

100

requests

per

minute
```

Old requests are automatically removed.

Only recent requests matter.

Exactly the same algorithm is used.

Other examples:

- Login throttling
- Sliding window rate limiting
- Request monitoring
- Streaming event processing

______________________________________________________________________

# Pattern Recognition

## Pattern

**Queue + Sliding Time Window**

______________________________________________________________________

## Recognition Clues

Whenever you see:

- Recent
- Last K seconds
- Sliding window
- Stream
- Oldest expires
- Continuous events

Think

```
Queue
```

______________________________________________________________________

# Why Not Use a List?

Suppose

```
[1,100,3001,3002]
```

When

```
1
```

expires,

removing the first element of a Python list requires shifting every remaining element.

```
O(n)
```

Queues avoid this.

______________________________________________________________________

# Brute Force Solution

## Intuition

Store every request.

Whenever a new request arrives,

scan the entire list.

Count recent requests.

______________________________________________________________________

## Algorithm

Requests

```
1

100

3001

3002
```

Current

```
3002
```

Scan

```
1

Too old
```

```
100

Keep
```

```
3001

Keep
```

```
3002

Keep
```

Count

```
3
```

______________________________________________________________________

## Complexity

Time

```
O(n)
```

per request.

Space

```
O(n)
```

Too slow.

______________________________________________________________________

# Better Observation

Once a request becomes older than

```
3000
```

milliseconds,

it will **never become valid again**.

Therefore,

remove it permanently.

______________________________________________________________________

# Optimized Solution (Queue)

## Key Insight

Maintain a queue of only valid requests.

Whenever a new request arrives:

1. Add it.
1. Remove expired requests from the front.
1. Queue size is the answer.

______________________________________________________________________

# Why Queue?

Requests arrive in order.

Oldest request

↓

Leaves first.

Newest request

↓

Enters last.

Exactly

```
FIFO
```

______________________________________________________________________

# Step-by-Step Algorithm

Initially

```
Queue

[]
```

______________________________________________________________________

Call

```
ping(1)
```

Queue

```
[1]
```

Answer

```
1
```

______________________________________________________________________

Call

```
ping(100)
```

Queue

```
[1,100]
```

Nothing expires.

Answer

```
2
```

______________________________________________________________________

Call

```
ping(3001)
```

Valid range

```
1

↓

3001
```

Queue

```
1

100

3001
```

Answer

```
3
```

______________________________________________________________________

Call

```
ping(3002)
```

Valid range

```
2

↓

3002
```

Request

```
1
```

expires.

Queue becomes

```
100

3001

3002
```

Answer

```
3
```

______________________________________________________________________

# Visual Explanation

```
Queue

[]
```

↓

```
[1]
```

↓

```
[1,100]
```

↓

```
[1,100,3001]
```

↓

New Request

```
3002
```

↓

Remove expired

```
1
```

↓

```
[100,3001,3002]
```

Done.

______________________________________________________________________

# Why This Works

Loop Invariant:

> The queue always contains only requests whose timestamps fall within the last 3000 milliseconds.

Whenever a new request arrives:

```
Append
```

Then

```
Remove expired timestamps
```

Since timestamps are strictly increasing,

expired requests are always at the front.

No searching is required.

______________________________________________________________________

# Why Is It O(n)?

This surprises many people.

Suppose

```
1000
```

requests arrive.

Each request:

- Enters the queue exactly once.
- Leaves the queue exactly once.

Even though a loop removes old requests,

the total number of removals is

```
n
```

Therefore,

overall complexity is

```
O(n)
```

or

```
O(1)
```

amortized per request.

______________________________________________________________________

# Queue vs Stack

| Stack | Queue |
|--------|-------|
| Last In First Out | First In First Out |
| Undo | Streaming |
| Function Calls | Request Processing |
| Parsing | Rate Limiting |
| DFS | BFS |

______________________________________________________________________

# Edge Cases

### First Request

Queue

```
[]
```

↓

```
[100]
```

Answer

```
1
```

______________________________________________________________________

### All Requests Recent

Nothing removed.

______________________________________________________________________

### Many Expired Requests

All expired requests are removed.

______________________________________________________________________

### Exactly 3000 Milliseconds

Range is inclusive.

Example

```
Current

4000
```

Request

```
1000
```

is still valid.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n)
```

per request.

Space

```
O(n)
```

______________________________________________________________________

## Queue Solution

Each request is:

- Added once
- Removed once

Time

```
O(1)
```

amortized

```
O(n)
```

overall.

Space

```
O(n)
```

Worst case,

all requests remain within the window.

______________________________________________________________________

# Production-Quality Python

## Optimized (Recommended)

```python
from collections import deque


class RecentCounter:
    def __init__(self) -> None:
        self.requests = deque()

    def ping(self, time: int) -> int:
        self.requests.append(time)

        while self.requests[0] < time - 3000:
            self.requests.popleft()

        return len(self.requests)


if __name__ == "__main__":
    counter = RecentCounter()

    print(counter.ping(1))
    print(counter.ping(100))
    print(counter.ping(3001))
    print(counter.ping(3002))
```

______________________________________________________________________

# Why Use `deque` Instead of a List?

Python list

```python
pop(0)
```

takes

```
O(n)
```

because all remaining elements shift left.

`deque`

```python
popleft()
```

takes

```
O(1)
```

Always prefer `collections.deque` when removing from the front.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using a list instead of a queue.

Front removal becomes expensive.

______________________________________________________________________

## Mistake 2

Scanning all requests every time.

Expired requests should be removed permanently.

______________________________________________________________________

## Mistake 3

Using

```python
if
```

instead of

```python
while
```

Multiple requests may expire at once.

______________________________________________________________________

## Mistake 4

Using

```python
<=
```

instead of

```python
<
```

Remember,

the interval

```
[time - 3000, time]
```

is inclusive.

Requests exactly at `time - 3000` must remain.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A brute-force solution stores every request and scans the entire list for every new ping, which is inefficient. Since timestamps arrive in increasing order, expired requests always appear at the front. A queue lets me append new requests at the back and remove expired ones from the front. After removing all outdated timestamps, the queue size is exactly the number of recent requests."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use a Queue?**

Because the oldest request always leaves first.

______________________________________________________________________

**Q. Why use `while` instead of `if`?**

Several requests may expire after one new request arrives.

______________________________________________________________________

**Q. Why use `deque`?**

It supports O(1) insertion at the back and O(1) removal from the front.

______________________________________________________________________

**Q. Where is this pattern used in backend systems?**

- Rate limiting
- Streaming analytics
- Monitoring dashboards
- Sliding window metrics
- Event processing

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Queue + Sliding Time Window |
| Recognition | Recent Events / Time Window |
| Brute Force | Scan All Requests |
| Optimized | Queue (`deque`) |
| Time | O(1) amortized |
| Space | O(n) |

______________________________________________________________________

# Quick Revision

- Use a Queue for FIFO processing.
- Store only recent requests.
- Append new requests.
- Remove expired requests from the front.
- Use `while`, not `if`.
- Use `deque`, not a list.
- Each request enters and leaves once.
- Amortized time complexity is O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Moving Average from Data Stream
1. Implement Queue using Stacks
1. Design Circular Queue

______________________________________________________________________

## Medium

4. Dota2 Senate
1. Sliding Window Maximum
1. Hit Counter
1. Time-Based Key-Value Store

______________________________________________________________________

## Hard (Optional)

8. Design Browser History
1. Shortest Subarray with Sum at Least K
1. Design Search Autocomplete System

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is recognizing **streaming problems**. When data arrives in chronological order and
old data naturally expires, a **Queue** is usually the right data structure. Instead of repeatedly scanning all
historical data, maintain only the active window, giving efficient real-time processing—exactly how many backend systems
handle metrics, rate limits, and event streams.

______________________________________________________________________

# Next

[30-linked-list-basics.md](30-linked-list-basics.md)
