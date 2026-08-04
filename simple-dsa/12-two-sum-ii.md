# 12-two-sum-ii.md

# Two Sum II — Learning the Opposite Direction Two Pointer Pattern

## Interview Confidence

**Difficulty:** ⭐⭐☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 15–20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given a **1-indexed sorted array** of integers `numbers` and an integer `target`, return the indices of the two numbers
such that they add up to the target.

Requirements:

- Exactly one solution exists.
- You cannot use the same element twice.
- Return **1-based indices**.

### Example

```text
numbers = [2, 7, 11, 15]
target = 9

Output

[1, 2]
```

______________________________________________________________________

# What Is Actually Being Asked?

This looks almost identical to **Two Sum**, but there is one important difference:

> **The array is already sorted.**

That changes the optimal solution completely.

Instead of using a Hash Map, we can solve it using **Two Pointers** with **O(1)** extra space.

______________________________________________________________________

# Real-World Analogy

Imagine you have receipts sorted by amount.

```text
₹10
₹20
₹30
₹40
₹50
```

You need to find two receipts whose total is ₹60.

Because they're sorted, you don't need to compare every pair.

You can eliminate impossible combinations after each comparison.

______________________________________________________________________

# Pattern Recognition

Think Two Pointers when you see:

- Sorted array
- Pair
- Sum equals target
- Constant space preferred

This is the classic **Opposite Direction Two Pointer** problem.

______________________________________________________________________

# Brute Force Solution

Compare every pair.

```text
2 + 7

2 + 11

2 + 15

7 + 11

...
```

### Complexity

Time

```text
O(n²)
```

Space

```text
O(1)
```

______________________________________________________________________

# Better Solution (Hash Map)

Exactly like the original Two Sum.

### Complexity

Time

```text
O(n)
```

Space

```text
O(n)
```

Correct, but it ignores the advantage of the sorted array.

______________________________________________________________________

# Optimal Solution

## Key Insight

Place one pointer at each end.

```text
2   7   11   15

↑            ↑

L            R
```

Calculate the sum.

Three possibilities exist.

### Case 1

Sum equals target.

Done.

______________________________________________________________________

### Case 2

Sum is too small.

```text
2 + 11 = 13

Need 15
```

Moving the right pointer left makes the sum even smaller.

Wrong direction.

Increase the sum instead.

Move the **left pointer**.

______________________________________________________________________

### Case 3

Sum is too large.

```text
7 + 15 = 22

Need 18
```

Moving the left pointer right increases the sum further.

Wrong direction.

Decrease the sum.

Move the **right pointer**.

______________________________________________________________________

# Why Pointer Movement Works

Suppose

```text
2 5 8 12 15

↑         ↑

2 + 15 = 17
```

Target

```text
20
```

Current sum is too small.

Should we move the right pointer?

```text
2 + 12 = 14
```

Even worse.

The only way to increase the sum is to move the left pointer.

Likewise,

if the sum is too large,

the only useful move is reducing the right value.

This is the key intuition interviewers expect.

______________________________________________________________________

# Visual Explanation

Target

```text
9
```

```text
2 7 11 15

↑      ↑

17

Too large

↓

Move Right
```

Now

```text
2 7 11

↑   ↑

13

Too large

↓

Move Right
```

Now

```text
2 7

↑ ↑

9

Found
```

______________________________________________________________________

# Step-by-Step Algorithm

Initialize

```text
left = 0

right = n - 1
```

While

```text
left < right
```

Compute

```text
current_sum
```

If

```text
current_sum == target
```

Return answer.

Else if

```text
current_sum < target
```

Move left.

Else

Move right.

______________________________________________________________________

# Dry Run

```text
numbers = [2,3,4]

target = 6
```

Initial

```text
2 3 4

↑   ↑
```

Sum

```text
6
```

Return

```text
[1,3]
```

______________________________________________________________________

Another Example

```text
1 2 4 6 10

target = 8
```

```text
1 + 10 = 11

Too large

↓

Move Right
```

```text
1 + 6 = 7

Too small

↓

Move Left
```

```text
2 + 6 = 8

Done
```

______________________________________________________________________

# Why This Works

The array is sorted.

When the sum is:

Too small

```text
Need bigger values
```

Move left.

When the sum is:

Too large

```text
Need smaller values
```

Move right.

Each movement eliminates many impossible pairs.

Each pointer moves only forward or backward once.

Hence,

linear time.

______________________________________________________________________

# Edge Cases

## Two Elements

```text
[2,7]
```

Works immediately.

______________________________________________________________________

## Negative Numbers

```text
[-5,-2,4,10]
```

Sorting still preserves the pointer logic.

______________________________________________________________________

## Duplicate Values

```text
[1,2,2,4]
```

No problem.

______________________________________________________________________

## Target at Ends

```text
1 2 3 8

Target = 9
```

Found immediately.

______________________________________________________________________

# Complexity Analysis

## Time

Each pointer moves at most

```text
n
```

times.

Overall

```text
O(n)
```

______________________________________________________________________

## Space

Only two variables.

```text
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def two_sum(numbers: List[int], target: int) -> List[int]:
    """
    Returns the 1-based indices of two numbers
    whose sum equals the target.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    left = 0
    right = len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]

        if current_sum == target:
            return [left + 1, right + 1]

        if current_sum < target:
            left += 1
        else:
            right -= 1

    return []
```

______________________________________________________________________

# Common Mistakes

## 1. Using a Hash Map

Works.

But misses the opportunity for

```text
O(1)
```

space.

______________________________________________________________________

## 2. Forgetting 1-Based Indexing

Problem asks for

```text
left + 1

right + 1
```

______________________________________________________________________

## 3. Moving Both Pointers

Only one pointer should move each iteration.

______________________________________________________________________

## 4. Moving the Wrong Pointer

Remember:

```text
Small Sum

↓

Move Left
```

```text
Large Sum

↓

Move Right
```

______________________________________________________________________

# Variations

## Easy

- Squares of a Sorted Array
- Merge Sorted Array

______________________________________________________________________

## Medium

- 3Sum
- 4Sum
- Container With Most Water
- Boats to Save People

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Recognize sorted input.
1. Mention brute force.
1. Explain why Hash Map works.
1. Notice constant-space optimization.
1. Introduce Two Pointers.
1. Justify every pointer movement.
1. Analyze complexity.

______________________________________________________________________

### Common Follow-ups

### Q: Why not always use a Hash Map?

Hash Maps require

```text
O(n)
```

extra memory.

Two Pointers achieve

```text
O(1)
```

______________________________________________________________________

### Q: Why does moving the left pointer increase the sum?

Because the array is sorted.

Moving right means encountering equal or larger values.

______________________________________________________________________

### Q: Can this work on an unsorted array?

No.

The pointer movement logic depends on sorted order.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Opposite Direction Two Pointers |
| Recognition | Sorted array, pair, target sum |
| Brute Force | Nested loops |
| Better | Hash Map |
| Optimal | Two Pointers |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Practice Problems

## Easy

1. Squares of a Sorted Array
1. Merge Sorted Array

## Medium

1. 3Sum
1. Container With Most Water
1. Boats to Save People
1. Partition Labels

## Hard

1. Trapping Rain Water
1. 4Sum II

______________________________________________________________________

# Quick Revision

- Sorted array → Think Two Pointers.
- Start from both ends.
- Sum too small → Move left.
- Sum too large → Move right.
- Return **1-based indices**.
- Time: **O(n)**
- Space: **O(1)**

______________________________________________________________________

# Key Takeaway

The biggest lesson isn't how to solve Two Sum II.

It's learning this interview habit:

> **Whenever the input is sorted, ask yourself: "Can Two Pointers eliminate my nested loops?"**

This single observation helps solve dozens of interview problems efficiently.

______________________________________________________________________

# Navigation

**Previous**

[11-two-pointers.md](11-two-pointers.md)

**Next**

[13-valid-palindrome.md](13-valid-palindrome.md)
