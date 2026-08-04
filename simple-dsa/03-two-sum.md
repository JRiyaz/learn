# 03-two-sum.md

# Two Sum — Your First Interview Optimization Pattern

## Interview Confidence

**Difficulty:** ⭐☆☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 15–20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up
to the target.

You may assume:

- Exactly one valid answer exists.
- You cannot use the same element twice.
- Return the indices, not the values.

Example:

```text
nums = [2, 7, 11, 15]
target = 9

Output:
[0, 1]
```

______________________________________________________________________

## What Is Actually Being Asked?

The interviewer is asking:

> "Can you efficiently find a pair whose sum equals the target?"

Notice:

❌ Return values? No.

✅ Return indices.

Also:

```text
nums = [3, 3]
target = 6
```

Answer:

```text
[0,1]
```

You cannot use the same element twice.

______________________________________________________________________

# Real-World Analogy

Imagine an e-commerce backend.

A customer has a ₹1000 gift card.

Products:

```text
₹250
₹300
₹750
₹500
```

Find two products whose total equals ₹1000.

Brute force:

Compare every pair.

Optimized:

Remember prices you've already seen.

The optimization pattern is identical.

______________________________________________________________________

# Pattern Recognition

This problem teaches the **Hash Map Lookup Pattern**.

### Recognition Clues

Look for phrases like:

- Find two numbers
- Pair with target
- Complement
- Return indices
- Lookup previous values

### Ask Yourself

Instead of asking:

> "Who can I pair with this number?"

Ask:

> "What number do I need?"

This small change leads directly to the optimal solution.

______________________________________________________________________

# Brute Force Solution

## Intuition

Compare every element with every other element.

Example:

```text
2 7 11 15
```

Check

```text
2+7

2+11

2+15

7+11

7+15

11+15
```

Eventually:

```text
2+7=9
```

Found.

______________________________________________________________________

## Algorithm

For every index:

Check every later index.

If sum equals target:

Return indices.

______________________________________________________________________

## Dry Run

```text
nums = [2,7,11,15]

target = 9
```

```
i=0

2+7=9

Return [0,1]
```

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


def two_sum_brute(nums: List[int], target: int) -> List[int]:
    n = len(nums)

    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]

    return []
```

______________________________________________________________________

# Optimized Solution

## Key Insight

Suppose current number is

```text
7
```

Target

```text
9
```

Instead of searching every remaining element,

ask:

```
What number do I need?

9 - 7 = 2
```

If we've already seen `2`, we're done.

So we store previously visited numbers in a hash map.

______________________________________________________________________

## Visual Explanation

Example

```text
nums

[2] [7] [11] [15]

target = 9
```

Iteration

```
Current = 2

Need = 7

HashMap

{}
```

Store

```
2 → 0
```

Next

```
Current = 7

Need = 2

HashMap

2 → 0
```

Found!

Return

```
[0,1]
```

______________________________________________________________________

## Step-by-Step Algorithm

Initialize empty hash map.

For every number:

```
Need = target - current
```

If needed value already exists:

Return indices.

Otherwise:

Store current number.

Continue.

______________________________________________________________________

# Dry Run

Example

```text
nums = [3,2,4]

target = 6
```

### Step 1

Current

```
3
```

Need

```
3
```

Map

```
{}
```

Store

```
3→0
```

______________________________________________________________________

### Step 2

Current

```
2
```

Need

```
4
```

Map

```
3→0
```

Not found.

Store

```
3→0

2→1
```

______________________________________________________________________

### Step 3

Current

```
4
```

Need

```
2
```

Map

```
3→0

2→1
```

Found.

Answer

```
[1,2]
```

______________________________________________________________________

# Why This Works

When processing each number, all previously visited numbers are stored.

If the required complement exists, we've already recorded its index.

Since every element is processed exactly once, every valid pair will eventually be discovered.

This avoids repeatedly scanning the array.

______________________________________________________________________

# Edge Cases

## Duplicate Numbers

```
[3,3]

target=6
```

Works because the first `3` is stored before processing the second.

______________________________________________________________________

## Negative Numbers

```
[-2,5,8]

target=3
```

Need

```
5
```

Still works.

______________________________________________________________________

## Zero

```
[0,4,3,0]

target=0
```

Works correctly.

______________________________________________________________________

## Empty Array

Return empty list.

______________________________________________________________________

## Single Element

Cannot form a pair.

Return empty list.

______________________________________________________________________

# Complexity Analysis

## Time

Each element is processed once.

Hash map lookup:

```
O(1)
```

Average.

Overall:

```
O(n)
```

______________________________________________________________________

## Space

Hash map stores at most every element.

```
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import Dict, List


def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Returns indices of two numbers whose sum equals target.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    seen: Dict[int, int] = {}

    for index, number in enumerate(nums):
        complement = target - number

        if complement in seen:
            return [seen[complement], index]

        seen[number] = index

    return []
```

______________________________________________________________________

# Common Mistakes

### 1. Sorting the Array

Sorting changes indices.

The problem asks for original indices.

______________________________________________________________________

### 2. Storing Before Checking

Wrong:

```python
seen[number] = index

if complement in seen:
```

Fails for

```
[3]

target=6
```

Always **check first**, then store.

______________________________________________________________________

### 3. Using Nested Loops

Correct but inefficient.

Interviewers expect optimization.

______________________________________________________________________

### 4. Returning Values Instead of Indices

Wrong:

```
[2,7]
```

Correct:

```
[0,1]
```

Read the problem carefully.

______________________________________________________________________

# Variations

## Easy

- Two Sum II (sorted array)
- Contains Duplicate

______________________________________________________________________

## Medium

- 3Sum
- 4Sum
- Two Sum Less Than K
- Pair Sum in BST

Notice how the underlying idea evolves:

- Hash Map
- Two Pointers (sorted arrays)
- Sorting + Two Pointers
- Tree traversal

______________________________________________________________________

# Interview Discussion

### What Interviewers Expect

A strong candidate usually follows this progression:

1. Clarify the problem.
1. Mention brute force.
1. Analyze its complexity.
1. Ask if optimization is expected.
1. Introduce a hash map.
1. Explain the complement idea.
1. Write clean code.
1. Discuss complexity and edge cases.

______________________________________________________________________

### Common Follow-up Questions

**Q:** Can you solve it without extra space?

**A:** Yes, by sorting and using two pointers, but you'll lose original indices unless you store them.

______________________________________________________________________

**Q:** What if the array is already sorted?

Use Two Pointers.

______________________________________________________________________

**Q:** What if there are multiple answers?

Store all matching pairs or modify the algorithm based on requirements.

______________________________________________________________________

**Q:** What if numbers arrive as a stream?

Maintain the hash map while processing incoming values.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Hash Map Lookup |
| Recognition | Find pair, target sum, complement |
| Brute Force | Nested loops |
| Optimal | Hash Map |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Easy

1. Two Sum II
1. Contains Duplicate

## Medium

1. 3Sum
1. 4Sum
1. Top K Frequent Elements
1. Group Anagrams

## Hard (Optional)

1. Subarray Sum Equals K
1. Continuous Subarray Sum

______________________________________________________________________

# Quick Revision

- Return **indices**, not values.
- Think in terms of the **complement**.
- `complement = target - current`.
- Use a hash map for O(1) average lookups.
- Check **before** storing the current element.
- Time: **O(n)**.
- Space: **O(n)**.
- Sorting is usually not appropriate because it changes indices.
- This problem introduces the **Hash Map Lookup Pattern**, one of the most common interview optimizations.

______________________________________________________________________

# Navigation

**Previous**

[02-arrays.md](02-arrays.md)

**Next**

[04-best-time-to-buy-and-sell-stock.md](04-best-time-to-buy-and-sell-stock.md)
