# 05-contains-duplicate.md

# Contains Duplicate — The Fast Membership Lookup Pattern

## Interview Confidence

**Difficulty:** ⭐☆☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 10–15 minutes

**Revision Time:** 3 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given an integer array `nums`, return:

- `True` if any value appears **at least twice**
- `False` if every element is unique

Example 1

```text
nums = [1,2,3,1]

Output:
True
```

Example 2

```text
nums = [1,2,3,4]

Output:
False
```

______________________________________________________________________

## What Is Actually Being Asked?

The interviewer is asking:

> "Can you efficiently determine whether you've seen a value before?"

You're **not** asked:

- Which value is duplicated?
- How many times it appears?
- Where it appears.

Just determine whether **any duplicate exists**.

______________________________________________________________________

# Real-World Analogy

Imagine you're importing users from a CSV file.

```text
alice@example.com
bob@example.com
charlie@example.com
alice@example.com
```

Before inserting into the database, you need to detect duplicate emails.

A slow solution compares every email with every other email.

A better solution keeps a collection of emails already processed.

The moment an email appears again, you stop.

The same idea is used in:

- User registration
- API idempotency
- Payment transaction IDs
- Event deduplication
- Kafka consumers
- Cache key validation

______________________________________________________________________

# Pattern Recognition

This problem teaches the **Hash Set Membership Pattern**.

Whenever you see:

- duplicate
- unique
- already seen
- repeated value
- distinct elements

Think immediately:

> **Hash Set**

______________________________________________________________________

# Brute Force Solution

## Intuition

Compare every element with every other element.

If two values are equal,

return `True`.

Otherwise,

return `False`.

______________________________________________________________________

## Visual

```text
1 2 3 1

Compare

1 with 2

1 with 3

1 with 1

Duplicate found
```

______________________________________________________________________

## Algorithm

For every element:

Compare with every later element.

If equal:

Return `True`.

Else continue.

______________________________________________________________________

## Complexity

Time

```text
O(n²)
```

Space

```text
O(1)
```

______________________________________________________________________

## Python

```python
from typing import List


def contains_duplicate_brute(nums: List[int]) -> bool:
    n = len(nums)

    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True

    return False
```

______________________________________________________________________

# Optimal Solution

## Key Insight

Instead of asking:

> "Does any future element equal me?"

Ask:

> "Have I already seen this value?"

Maintain a **hash set**.

If the current value already exists,

duplicate found.

Otherwise,

store it.

______________________________________________________________________

# Visual Explanation

Example

```text
nums

[1] [2] [3] [1]
```

Start

```text
Seen

{}
```

______________________________________________________________________

Current = 1

```text
{}

↓

{1}
```

______________________________________________________________________

Current = 2

```text
{1}

↓

{1,2}
```

______________________________________________________________________

Current = 3

```text
{1,2}

↓

{1,2,3}
```

______________________________________________________________________

Current = 1

Already exists.

Return

```text
True
```

______________________________________________________________________

# Step-by-Step Algorithm

Initialize empty set.

For every number:

If number already exists:

Return `True`.

Else:

Insert into set.

After traversal:

Return `False`.

______________________________________________________________________

# Why This Works

A set contains only unique values.

Every processed number is stored exactly once.

When a duplicate appears,

membership lookup immediately succeeds.

Since each lookup is **O(1)** on average,

the overall solution becomes **O(n)**.

______________________________________________________________________

# Edge Cases

## Empty Array

```text
[]
```

No duplicates.

Return

```text
False
```

______________________________________________________________________

## One Element

```text
[5]
```

Cannot have duplicates.

Return

```text
False
```

______________________________________________________________________

## All Same

```text
[2,2,2,2]
```

Duplicate detected immediately.

______________________________________________________________________

## Negative Numbers

```text
[-1,-2,-3,-1]
```

Works exactly the same.

______________________________________________________________________

## Large Input

Millions of elements.

Still linear time.

______________________________________________________________________

# Complexity Analysis

## Time

Each element:

- lookup → O(1)
- insert → O(1)

Average total:

```text
O(n)
```

______________________________________________________________________

## Space

Worst case:

Every element is unique.

```text
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List, Set


def contains_duplicate(nums: List[int]) -> bool:
    """
    Returns True if any duplicate exists.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    seen: Set[int] = set()

    for number in nums:
        if number in seen:
            return True

        seen.add(number)

    return False
```

______________________________________________________________________

# Alternative Solution

Python provides a concise solution:

```python
def contains_duplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))
```

### Complexity

Time

```text
O(n)
```

Space

```text
O(n)
```

### Interview Advice

This is elegant but **don't start with it** in interviews.

Interviewers want to understand your reasoning before seeing shortcuts.

Explain the hash set approach first.

______________________________________________________________________

# Common Mistakes

## 1. Using a List Instead of a Set

Wrong

```python
seen = []

if num in seen:
```

Membership in a list is

```text
O(n)
```

Overall complexity becomes

```text
O(n²)
```

______________________________________________________________________

## 2. Sorting First

Sorting works:

```python
nums.sort()
```

Then compare neighbors.

Complexity:

```text
O(n log n)
```

Still slower than a hash set.

Also modifies the input.

______________________________________________________________________

## 3. Forgetting Average Complexity

Hash tables provide average

```text
O(1)
```

Worst case is rare and usually ignored in interviews unless explicitly discussed.

______________________________________________________________________

## 4. Using Extra Nested Loops

Avoid unnecessary comparisons.

______________________________________________________________________

# Variations

## Easy

- Contains Duplicate II
- Valid Anagram

______________________________________________________________________

## Medium

- Longest Consecutive Sequence
- Top K Frequent Elements
- Group Anagrams
- Find All Duplicates in an Array

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Mention brute force.
1. Analyze O(n²).
1. Notice repeated membership checks.
1. Introduce hash set.
1. Explain why lookup becomes O(1).
1. Code cleanly.
1. Discuss complexity.

______________________________________________________________________

### Common Follow-ups

### Q: Why use a set instead of a list?

Set lookup is O(1).

List lookup is O(n).

______________________________________________________________________

### Q: Can this be solved without extra memory?

Yes.

Sort first.

Compare adjacent elements.

Time:

```text
O(n log n)
```

Space:

Depends on sorting algorithm.

______________________________________________________________________

### Q: Which solution would you choose?

Unless memory is extremely constrained,

use the hash set.

It is simpler and faster.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Hash Set Membership |
| Recognition | Duplicate, unique, already seen |
| Brute Force | Nested loops |
| Optimal | Hash Set |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Easy

1. Contains Duplicate II
1. Valid Anagram

## Medium

1. Top K Frequent Elements
1. Longest Consecutive Sequence
1. Group Anagrams
1. Find All Duplicates in an Array

## Hard (Optional)

1. First Missing Positive
1. Minimum Window Substring (introduces advanced hash map usage)

______________________________________________________________________

# Quick Revision

- Duplicate detection usually suggests a **Hash Set**.
- Store previously seen values.
- If current value already exists, return `True`.
- Hash set lookup is **O(1)** on average.
- Overall complexity:
  - Time → **O(n)**
  - Space → **O(n)**
- Don't use a list for membership checks.
- Sorting is an alternative but slower.

______________________________________________________________________

# Key Takeaway

This problem introduces one of the most important interview habits:

> **When you repeatedly ask "Have I seen this before?", think Hash Set.**

You'll use this exact pattern in many later problems, including:

- Longest Consecutive Sequence
- Happy Number
- Cycle Detection
- Graph Traversals (Visited Set)
- BFS & DFS
- Cache Implementations
- Event Deduplication in Distributed Systems

______________________________________________________________________

# Navigation

**Previous**

[04-best-time-to-buy-and-sell-stock.md](04-best-time-to-buy-and-sell-stock.md)

**Next**

[06-hash-maps.md](06-hash-maps.md)
