# 46-top-k-frequent-elements.md

# Top K Frequent Elements

> **🎯 This is the most important Heap interview problem for startups and mid-sized product companies.**
>
> Although the title mentions **Heap**, the real interview skill is choosing the right data structure.
>
> This problem can be solved using:
>
> - Hash Map + Sorting
> - Hash Map + Heap ✅ (Most Interviewed)
> - Hash Map + Bucket Sort (Optimal)
>
> We'll understand all three approaches and why the Heap solution is usually preferred in interviews.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 30–40 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem tests multiple concepts together:

- Hash Maps
- Frequency Counting
- Heap (Priority Queue)
- Trade-offs between multiple solutions
- Complexity analysis

This pattern appears in:

- Trending hashtags
- Most viewed videos
- Top searched products
- Most active users
- Analytics dashboards
- Log aggregation systems

______________________________________________________________________

# Problem Statement

Given an integer array `numbers` and an integer `k`,

return the `k` most frequent elements.

The answer can be returned in **any order**.

______________________________________________________________________

## Example

Input

```text
numbers = [1,1,1,2,2,3]

k = 2
```

Output

```text
[1,2]
```

Explanation

Frequency table

```text
1 → 3

2 → 2

3 → 1
```

Top 2 frequencies

```text
1

2
```

______________________________________________________________________

# Before Learning the Algorithm

Suppose someone asks

> "Who are the top 10 most active users?"

Would you repeatedly scan the logs?

No.

First,

count activities.

Then,

find the largest counts.

Exactly this problem.

______________________________________________________________________

# Backend Engineering Analogy

Imagine an API Gateway receiving requests.

Logs

```text
/user

/user

/login

/user

/login

/products
```

Frequency

```text
/user      → 3

/login     → 2

/products  → 1
```

Need

Top

```
2
```

Most requested APIs.

Exactly Top K Frequent Elements.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Hash Map + Heap**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Top K
- Most frequent
- Highest priority
- Largest K
- Smallest K

Think

```text
Frequency Count

+

Heap
```

______________________________________________________________________

# Brute Force Solution

## Step 1

Count frequencies.

```text
1 → 3

2 → 2

3 → 1
```

______________________________________________________________________

## Step 2

Sort all frequencies.

```text
[(1,3),
 (2,2),
 (3,1)]
```

______________________________________________________________________

Take first

```
k
```

elements.

______________________________________________________________________

# Complexity

Counting

```
O(n)
```

Sorting

```
O(m log m)
```

where

```
m
```

\=

Unique numbers.

Works,

but sorting everything is unnecessary.

______________________________________________________________________

# Better Observation

Suppose

```
10 Million
```

unique users,

Need

```
Top 10
```

Why sort

```
10 Million
```

values?

Only

```
Top 10
```

matters.

______________________________________________________________________

# Optimized Solution (Heap)

## Key Insight

Maintain a

```
Min Heap
```

of size

```
k
```

The heap always stores

the current best

```
k
```

elements.

Whenever a better candidate appears,

remove the smallest.

______________________________________________________________________

# Why Min Heap?

Suppose

```
k = 3
```

Heap

```text
(5)

(8)

(10)
```

Smallest frequency

```
5
```

New frequency

```
12
```

Compare

```
12 > 5
```

Remove

```
5
```

Insert

```
12
```

Heap still contains

Top 3 frequencies.

______________________________________________________________________

# Step-by-Step Dry Run

Input

```text
[1,1,1,2,2,3]
```

Frequency Map

```text
1 → 3

2 → 2

3 → 1
```

Heap Size

```
k = 2
```

______________________________________________________________________

Insert

```
(3,1)
```

Heap

```text
[(3,1)]
```

______________________________________________________________________

Insert

```
(2,2)
```

Heap

```text
[(2,2),
 (3,1)]
```

______________________________________________________________________

Insert

```
(1,3)
```

Heap size

```
3
```

Too large.

Remove smallest frequency

```
1
```

Remaining

```text
[(2,2),
 (3,1)]
```

Answer

```
1

2
```

______________________________________________________________________

# Visual Explanation

Frequency Map

```text
1 → 3

2 → 2

3 → 1
```

↓

Heap

```text
(1)

(2)
```

↓

Insert

```
3
```

↓

Remove

```
1
```

↓

Heap

```text
(2)

(3)
```

Done.

______________________________________________________________________

# Why This Works

Loop Invariant

> Before processing each frequency,
> the heap contains the `k` largest frequencies seen so far.

If the heap grows beyond `k`,

remove the smallest frequency.

Therefore,

the heap always stores exactly the best `k` candidates.

______________________________________________________________________

# Alternative Solution (Bucket Sort)

Frequency cannot exceed

```
n
```

Create buckets

```text
Bucket[1]

Bucket[2]

...

Bucket[n]
```

Each bucket stores numbers having that frequency.

Scan buckets backwards.

Time

```
O(n)
```

This is the optimal solution.

However,

the Heap solution is usually preferred in interviews because it demonstrates Heap knowledge and generalizes well.

______________________________________________________________________

# Edge Cases

### Empty Array

Return

```python
[]
```

______________________________________________________________________

### k = 1

Return the most frequent element.

______________________________________________________________________

### All Elements Unique

```text
1 2 3 4
```

Any

```
k
```

elements are valid.

______________________________________________________________________

### All Same Value

```text
5 5 5
```

Return

```text
[5]
```

______________________________________________________________________

# Complexity Analysis

## Approach 1

Hash Map + Sorting

Time

```
O(n + m log m)
```

Space

```
O(m)
```

______________________________________________________________________

## Approach 2

Hash Map + Heap

Time

```
O(n + m log k)
```

Space

```
O(m + k)
```

______________________________________________________________________

## Approach 3

Bucket Sort

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

# Production-Quality Python

## Heap Solution (Recommended)

```python
from collections import Counter
import heapq
from typing import List


def top_k_frequent(
    numbers: List[int],
    k: int,
) -> List[int]:
    frequency = Counter(numbers)

    min_heap: List[tuple[int, int]] = []

    for value, count in frequency.items():
        heapq.heappush(min_heap, (count, value))

        if len(min_heap) > k:
            heapq.heappop(min_heap)

    return [value for _, value in min_heap]
```

______________________________________________________________________

## Sorting Solution

```python
from collections import Counter
from typing import List


def top_k_frequent(
    numbers: List[int],
    k: int,
) -> List[int]:
    frequency = Counter(numbers)

    ordered = sorted(
        frequency.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        value
        for value, _ in ordered[:k]
    ]
```

______________________________________________________________________

## Bucket Sort Solution

```python
from collections import Counter
from typing import List


def top_k_frequent(
    numbers: List[int],
    k: int,
) -> List[int]:
    frequency = Counter(numbers)

    buckets: List[List[int]] = [
        [] for _ in range(len(numbers) + 1)
    ]

    for value, count in frequency.items():
        buckets[count].append(value)

    result: List[int] = []

    for count in range(len(buckets) - 1, 0, -1):
        for value in buckets[count]:
            result.append(value)

            if len(result) == k:
                return result

    return result
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Sorting the original array.

We need to sort by

```
Frequency
```

not value.

______________________________________________________________________

## Mistake 2

Using a Max Heap.

A Min Heap of size

```
k
```

is more efficient.

______________________________________________________________________

## Mistake 3

Forgetting to remove elements when the heap exceeds size `k`.

______________________________________________________________________

## Mistake 4

Thinking Heap is always optimal.

Bucket Sort is asymptotically faster for this specific problem,

but Heap is more broadly applicable.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "First, I'll count the frequency of every element using a Hash Map. A straightforward solution is to sort the frequency map, but that sorts more data than necessary. Since I only need the top `k` elements, I'll maintain a Min Heap of size `k`. Whenever the heap grows beyond `k`, I'll remove the smallest frequency. This keeps only the `k` most frequent elements."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use a Min Heap instead of a Max Heap?**

A Min Heap lets us efficiently discard the smallest frequency whenever we exceed `k`.

______________________________________________________________________

**Q. Why not sort?**

Sorting processes every unique element, even though we only need the top `k`.

______________________________________________________________________

**Q. Why is Bucket Sort O(n)?**

The maximum possible frequency is `n`, so we can index directly by frequency.

______________________________________________________________________

**Q. Where is this pattern used?**

- Trending topics
- Analytics dashboards
- Leaderboards
- Recommendation systems
- Log aggregation

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Hash Map + Heap |
| Recognition | Top K / Most Frequent |
| Brute Force | Sort Frequencies |
| Optimized | Min Heap |
| Optimal | Bucket Sort |
| Time | O(n + m log k) |
| Space | O(m + k) |

______________________________________________________________________

# Quick Revision

- Count frequencies with a Hash Map.
- A Min Heap of size `k` stores the current best candidates.
- Remove the smallest frequency when the heap grows too large.
- Sorting is simpler but less efficient.
- Bucket Sort achieves O(n) for this problem.
- Heap is the preferred interview solution.
- Time complexity is O(n + m log k).

______________________________________________________________________

# Practice Questions

## Easy

1. Kth Largest Element in a Stream
1. Sort Characters by Frequency
1. Relative Ranks

______________________________________________________________________

## Medium

4. K Closest Points to Origin
1. Kth Largest Element in an Array
1. Reorganize String
1. Task Scheduler

______________________________________________________________________

## Hard (Optional)

8. Merge k Sorted Lists
1. Sliding Window Median
1. Find Median from Data Stream

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning to **choose the right data structure**. Once you've counted frequencies
with a **Hash Map**, the question becomes: *How do I efficiently keep only the best `k` candidates?* A **Min Heap**
answers that perfectly by discarding less important elements while preserving the top `k`. This **Hash Map + Heap**
pattern appears repeatedly in backend systems that process rankings, analytics, and large-scale event streams.

______________________________________________________________________

# Next

[47-number-of-islands.md](47-number-of-islands.md)
