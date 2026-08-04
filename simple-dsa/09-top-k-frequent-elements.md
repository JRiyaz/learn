# 09-top-k-frequent-elements.md

# Top K Frequent Elements — Frequency + Bucket Sort Pattern

## Interview Confidence

**Difficulty:** ⭐⭐⭐☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 25 minutes

**Revision Time:** 7 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.

You may return the answer in any order.

### Example

```text
nums = [1,1,1,2,2,3]

k = 2

Output

[1,2]
```

Another example

```text
nums = [1]

k = 1

Output

[1]
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> Find the elements that occur most frequently.

Notice that you're **not** asked to:

- Sort the array
- Return frequencies
- Return elements in sorted order

You're simply looking for the **top K frequent elements**.

______________________________________________________________________

# Real-World Analogy

Imagine you're analyzing API requests.

```text
/login
/login
/login
/profile
/profile
/orders
```

Frequency

```text
/login  -> 3

/profile -> 2

/orders -> 1
```

If your manager asks:

> "Show me the top 2 most requested endpoints."

The answer is:

```text
/login

/profile
```

Other backend examples:

- Most searched products
- Most active users
- Most common errors
- Trending hashtags
- Frequently purchased items

______________________________________________________________________

# Pattern Recognition

This problem combines **two patterns**:

1. Frequency Counting (Hash Map)
1. Efficient Top-K Retrieval

Interview clues:

- Top K
- Most frequent
- Highest count
- Trending
- Popular

Think:

```text
Count first

↓

Then retrieve Top K
```

______________________________________________________________________

# Brute Force Solution

## Intuition

1. Count frequencies.
1. Sort by frequency.
1. Return first K elements.

Example

```text
1 -> 3

2 -> 2

3 -> 1
```

Sort

```text
3

2

1
```

Take first two.

______________________________________________________________________

## Complexity

Counting

```text
O(n)
```

Sorting

```text
O(m log m)
```

where

```text
m = unique elements
```

Overall

```text
O(n + m log m)
```

Good.

But interviewers usually ask:

> "Can you do better than sorting?"

______________________________________________________________________

# Better Solution (Heap)

Use a Max Heap (or Min Heap of size K).

Steps

```text
Count

↓

Build Heap

↓

Extract K elements
```

Complexity

```text
O(n log k)
```

Very common in production systems handling streaming data.

______________________________________________________________________

# Optimal Solution (Bucket Sort)

## Key Insight

What's the maximum possible frequency?

Suppose

```text
n = len(nums)
```

An element can appear at most

```text
n
```

times.

Therefore,

create buckets indexed by frequency.

______________________________________________________________________

# Visual Explanation

Input

```text
1 1 1 2 2 3
```

Frequency Map

```text
1 -> 3

2 -> 2

3 -> 1
```

Buckets

```text
Index

0

1 -> [3]

2 -> [2]

3 -> [1]

4

5

6
```

Traverse buckets from the end.

```text
6

↓

5

↓

4

↓

3

↓

Take 1

↓

2

↓

Take 2
```

Answer

```text
[1,2]
```

______________________________________________________________________

# Step-by-Step Algorithm

### Step 1

Build frequency map.

### Step 2

Create

```python
len(nums) + 1
```

empty buckets.

### Step 3

Place every number into its frequency bucket.

### Step 4

Traverse buckets backwards.

Collect elements until K are found.

______________________________________________________________________

# Why This Works

Every element appears exactly once in the frequency map.

Each frequency maps directly to one bucket.

By scanning buckets from highest frequency to lowest,

we naturally retrieve the most frequent elements first.

No sorting required.

______________________________________________________________________

# Edge Cases

## One Element

```text
[5]

k=1
```

Answer

```text
[5]
```

______________________________________________________________________

## All Unique

```text
1 2 3 4
```

Each frequency = 1.

Any K elements are valid.

______________________________________________________________________

## All Same

```text
7 7 7 7
```

One bucket contains

```text
7
```

______________________________________________________________________

## k = Number of Unique Elements

Return every unique element.

______________________________________________________________________

# Complexity Analysis

## Bucket Sort

### Time

Frequency counting

```text
O(n)
```

Bucket creation

```text
O(n)
```

Bucket traversal

```text
O(n)
```

Overall

```text
O(n)
```

______________________________________________________________________

### Space

Frequency map

```text
O(m)
```

Buckets

```text
O(n)
```

Overall

```text
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import Dict, List


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Returns the k most frequent elements.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    frequency: Dict[int, int] = {}

    for number in nums:
        frequency[number] = frequency.get(number, 0) + 1

    buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]

    for number, count in frequency.items():
        buckets[count].append(number)

    result: List[int] = []

    for count in range(len(buckets) - 1, 0, -1):
        for number in buckets[count]:
            result.append(number)

            if len(result) == k:
                return result

    return result
```

______________________________________________________________________

# Alternative Solution (Heap)

Python provides a simple implementation.

```python
from collections import Counter
import heapq


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    frequency = Counter(nums)

    return heapq.nlargest(
        k,
        frequency.keys(),
        key=frequency.get,
    )
```

### Interview Advice

If the interviewer asks for:

> Better than O(n log n)

Mention Bucket Sort.

If they ask for:

> Streaming data

Mention Heaps.

______________________________________________________________________

# Common Mistakes

## 1. Sorting Entire Array

Wrong.

We care about frequency,

not value.

______________________________________________________________________

## 2. Sorting Frequency Map

Correct.

But slower than Bucket Sort.

______________________________________________________________________

## 3. Forgetting Multiple Elements Per Bucket

Several numbers can share the same frequency.

Each bucket should store a list.

______________________________________________________________________

## 4. Returning Frequencies

Problem asks for

```text
Elements
```

not counts.

______________________________________________________________________

# Variations

## Easy

- Sort Characters By Frequency

______________________________________________________________________

## Medium

- Top K Frequent Words
- K Closest Points to Origin
- Kth Largest Element
- Task Scheduler

Notice how "Top K" often introduces either a **Heap** or **Bucket Sort**.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Count frequencies.
1. Mention sorting solution.
1. Analyze complexity.
1. Improve using Heap.
1. Mention Bucket Sort for O(n).
1. Write clean implementation.

______________________________________________________________________

### Common Follow-ups

### Q: Why Bucket Sort?

Because frequency is bounded by

```text
n
```

making bucket indexing possible.

______________________________________________________________________

### Q: Which is used more in production?

Usually Heaps.

They work well with streaming and continuously arriving data.

______________________________________________________________________

### Q: Which is faster here?

Bucket Sort.

Linear time.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Frequency + Bucket Sort |
| Recognition | Top K, Most Frequent |
| Brute Force | Sort by frequency |
| Better | Heap |
| Optimal | Bucket Sort |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Easy

1. Sort Characters By Frequency
1. Majority Element

## Medium

1. Top K Frequent Words
1. K Closest Points to Origin
1. Kth Largest Element in an Array
1. Task Scheduler

## Hard

1. Merge K Sorted Lists
1. Sliding Window Median

______________________________________________________________________

# Quick Revision

- Count frequencies first.
- Frequency ≤ `len(nums)`.
- Create buckets indexed by frequency.
- Traverse buckets backwards.
- No sorting required.
- Bucket Sort → **O(n)**.
- Heap → **O(n log k)**.
- For streaming systems, prefer Heaps.

______________________________________________________________________

# Key Takeaway

This problem teaches a valuable interview principle:

> **Sometimes you don't sort the data—you sort by a bounded property.**

Here, the bounded property is **frequency**, allowing Bucket Sort to outperform general sorting.

You'll revisit this idea when studying:

- Heaps
- Bucket Sort
- Counting Sort
- Priority Queues
- Streaming algorithms

______________________________________________________________________

# Navigation

**Previous**

[08-group-anagrams.md](08-group-anagrams.md)

**Next**

[10-longest-consecutive-sequence.md](10-longest-consecutive-sequence.md)
