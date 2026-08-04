# 10-longest-consecutive-sequence.md

# Longest Consecutive Sequence — The Sequence Start Pattern

## Interview Confidence

**Difficulty:** ⭐⭐⭐☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20–25 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given an unsorted array of integers `nums`, return the length of the longest consecutive sequence.

Your algorithm must run in **O(n)** time.

A consecutive sequence consists of numbers that follow each other by exactly 1.

### Example 1

```text
Input

[100, 4, 200, 1, 3, 2]

Output

4

Explanation

Sequence:

1 → 2 → 3 → 4
```

### Example 2

```text
Input

[0,3,7,2,5,8,4,6,0,1]

Output

9

Sequence:

0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is **not** asking you to sort the array.

They explicitly require an **O(n)** solution.

The real question is:

> "How can we find consecutive numbers without sorting?"

______________________________________________________________________

# Real-World Analogy

Imagine a backend service tracking user login days.

```text
User logged in on:

5
6
7
20
21
40
```

You want to know the user's longest login streak.

Instead of sorting every request, you want to quickly determine where each streak begins and how long it continues.

Similar examples:

- Daily active user streaks
- Consecutive order IDs
- Continuous sensor readings
- Event sequence detection

______________________________________________________________________

# Pattern Recognition

This problem teaches the **Sequence Start Pattern**.

Interview clues:

- Consecutive
- Longest streak
- O(n)
- Unsorted array

Think:

> "Don't start counting from every number. Only start from the beginning of a sequence."

______________________________________________________________________

# Brute Force Solution

## Intuition

For every number:

Keep checking whether:

```text
number + 1

number + 2

number + 3
```

exist.

Example

```text
1

↓

2

↓

3

↓

4
```

Repeat this for every element.

Many sequences are checked repeatedly.

______________________________________________________________________

## Complexity

Worst case

```text
O(n²)
```

______________________________________________________________________

# Better Solution

Sort the array.

Example

```text
100 4 200 1 3 2

↓

1 2 3 4 100 200
```

Now scan once.

Whenever numbers differ by 1,

increase streak.

Otherwise,

start a new streak.

______________________________________________________________________

## Complexity

Sorting

```text
O(n log n)
```

Still doesn't satisfy the problem.

______________________________________________________________________

# Optimal Solution

## Key Insight

Store all numbers in a Hash Set.

Only begin counting if the current number is the **start** of a sequence.

How do we know?

A number is the start if

```text
number - 1
```

does **not** exist.

______________________________________________________________________

# Visual Explanation

Input

```text
100 4 200 1 3 2
```

Hash Set

```text
{100,4,200,1,3,2}
```

Check

```text
100

99?

No

Start sequence
```

Length

```text
100
```

______________________________________________________________________

Check

```text
4

3?

Yes

Skip
```

Because another number already started this sequence.

______________________________________________________________________

Check

```text
1

0?

No

Start
```

Count

```text
1

↓

2

↓

3

↓

4
```

Length

```text
4
```

______________________________________________________________________

# Step-by-Step Algorithm

1. Insert all numbers into a Hash Set.
1. For every number:
   - If `number - 1` exists, skip it.
   - Otherwise:
     - Count consecutive numbers.
1. Track the maximum length.

______________________________________________________________________

# Why This Works

Every sequence is explored exactly once.

Example

```text
1 2 3 4
```

Without optimization

```text
Start at 1

Start at 2

Start at 3

Start at 4
```

Repeated work.

With optimization

```text
Only start at 1
```

Each element participates in at most one sequence expansion.

Therefore,

overall complexity becomes **O(n)**.

______________________________________________________________________

# Dry Run

Input

```text
[100,4,200,1,3,2]
```

Hash Set

```text
{100,4,200,1,3,2}
```

Iteration

```text
100

99 not found

Length = 1
```

______________________________________________________________________

```text
4

3 exists

Skip
```

______________________________________________________________________

```text
200

199 missing

Length = 1
```

______________________________________________________________________

```text
1

0 missing

Count

1

2

3

4
```

Maximum

```text
4
```

______________________________________________________________________

# Edge Cases

## Empty Array

```text
[]
```

Answer

```text
0
```

______________________________________________________________________

## One Element

```text
[10]
```

Answer

```text
1
```

______________________________________________________________________

## Duplicates

```text
[1,2,2,3]
```

Hash Set removes duplicates automatically.

Sequence

```text
1 2 3
```

Length

```text
3
```

______________________________________________________________________

## Negative Numbers

```text
[-2,-1,0,1]
```

Works exactly the same.

______________________________________________________________________

# Complexity Analysis

## Time

Building Hash Set

```text
O(n)
```

Each sequence explored once.

Overall

```text
O(n)
```

______________________________________________________________________

## Space

Hash Set

```text
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def longest_consecutive(nums: List[int]) -> int:
    """
    Returns the length of the longest consecutive sequence.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    numbers = set(nums)
    longest = 0

    for number in numbers:
        if number - 1 in numbers:
            continue

        current = number
        length = 1

        while current + 1 in numbers:
            current += 1
            length += 1

        longest = max(longest, length)

    return longest
```

______________________________________________________________________

# Common Mistakes

## 1. Sorting First

Correct.

But complexity becomes

```text
O(n log n)
```

The problem explicitly asks for **O(n)**.

______________________________________________________________________

## 2. Starting From Every Number

Repeated work.

Always check

```text
number - 1
```

first.

______________________________________________________________________

## 3. Forgetting Duplicates

Use a Hash Set.

Duplicates disappear automatically.

______________________________________________________________________

## 4. Iterating Over the Original List

Prefer iterating over the set to avoid processing duplicate values multiple times.

______________________________________________________________________

# Variations

## Easy

- Missing Number

______________________________________________________________________

## Medium

- Longest Increasing Subsequence (different problem)
- Longest Arithmetic Sequence
- Largest Divisible Subset

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Mention sorting solution.
1. Observe O(n log n).
1. Notice O(n) requirement.
1. Use Hash Set.
1. Only begin at sequence starts.
1. Explain why every sequence is visited once.

______________________________________________________________________

### Common Follow-ups

### Q: Why check `number - 1`?

If it exists,

this number is already inside another sequence.

No need to start again.

______________________________________________________________________

### Q: Why iterate over the set?

Avoid duplicate work.

______________________________________________________________________

### Q: Can this be solved in O(1) space?

Not while maintaining O(n) time.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Sequence Start |
| Recognition | Consecutive, longest streak, O(n) |
| Brute Force | Check every sequence |
| Better | Sort |
| Optimal | Hash Set + Start Detection |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Easy

1. Missing Number
1. Happy Number

## Medium

1. Longest Increasing Subsequence *(different pattern)*
1. Number of Islands
1. Daily Temperatures
1. Hand of Straights

## Hard

1. Frog Jump
1. Sliding Window Median

______________________________________________________________________

# Quick Revision

- Store all numbers in a Hash Set.
- Only start counting if `number - 1` doesn't exist.
- Expand forward until the sequence ends.
- Every sequence is explored exactly once.
- Time: **O(n)**
- Space: **O(n)**
- Don't sort when the problem explicitly asks for O(n).

______________________________________________________________________

# Key Takeaway

This problem teaches an important optimization strategy:

> **Don't process every element as a starting point. First identify valid starting points.**

This idea appears in many interview problems involving intervals, graphs, linked lists, and trees, where avoiding
redundant work is the key to achieving optimal complexity.

______________________________________________________________________

# Navigation

**Previous**

[09-top-k-frequent-elements.md](09-top-k-frequent-elements.md)

**Next**

[11-two-pointers.md](11-two-pointers.md)
