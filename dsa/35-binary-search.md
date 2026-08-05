# 35-binary-search.md

# Binary Search

> **🎯 This is one of the most important algorithms in Computer Science.**
>
> Many candidates memorize Binary Search.
>
> Very few truly understand **why it works**.
>
> After this lesson, you should be able to solve most startup interview Binary Search questions with confidence.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 20–25 minutes |
| Revision Time | 15 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers use Binary Search to test whether you understand:

- Divide and Conquer
- Searching efficiently
- Loop invariants
- Boundary conditions
- Off-by-one errors
- Problem reduction

Binary Search is used in almost every software domain:

- Database indexing (B-Trees, B+ Trees)
- Search engines
- Memory allocators
- Version control systems
- Scheduling systems
- Distributed databases
- Pagination
- Load balancing

______________________________________________________________________

# Problem Statement

Given a **sorted array** and a target value,

return the index of the target.

If the target doesn't exist,

return

```text
-1
```

______________________________________________________________________

## Example 1

Input

```text
Numbers

[-1,0,3,5,9,12]

Target

9
```

Output

```text
4
```

______________________________________________________________________

## Example 2

Input

```text
Numbers

[-1,0,3,5,9,12]

Target

2
```

Output

```text
-1
```

______________________________________________________________________

# Before Learning Binary Search

Suppose someone asks:

Find

```
87
```

inside

```
1

2

3

...

100
```

Would you check

```
1

↓

2

↓

3

↓

...
```

No.

You naturally open the book near the middle.

That's Binary Search.

______________________________________________________________________

# Simple English

Imagine searching for a word in a dictionary.

You don't start from page one.

You open somewhere in the middle.

If your word comes later,

discard the first half.

Otherwise,

discard the second half.

Repeat.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a database index.

Instead of scanning millions of records,

the index repeatedly narrows the search space.

```
1 Million Rows

↓

500K

↓

250K

↓

125K
```

This is exactly Binary Search.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Divide and Conquer**

______________________________________________________________________

## Recognition Clues

Whenever you see:

- Sorted array
- Sorted list
- Sorted data
- Search
- Find index
- First/Last occurrence

Think

```
Binary Search
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Start from the beginning.

Compare every element.

______________________________________________________________________

## Algorithm

Input

```text
[-1,0,3,5,9,12]
```

Need

```
9
```

Check

```
-1
```

↓

```
0
```

↓

```
3
```

↓

```
5
```

↓

```
9

✔
```

Return

```
4
```

______________________________________________________________________

## Complexity

Time

```
O(n)
```

Space

```
O(1)
```

______________________________________________________________________

## Limitation

Too slow for very large datasets.

______________________________________________________________________

# Better Observation

The array is already sorted.

Why search both halves?

After checking the middle,

one half can never contain the answer.

Discard it.

______________________________________________________________________

# Binary Search Idea

Suppose

```text
1 2 3 4 5 6 7 8 9
```

Need

```
8
```

Middle

```
5
```

Target

```
8
```

is larger.

Discard

```
1 2 3 4 5
```

Only search

```
6 7 8 9
```

Repeat.

______________________________________________________________________

# Understanding the Three Variables

Binary Search always keeps track of:

```
Left
```

Beginning of search space.

______________________________________________________________________

```
Right
```

End of search space.

______________________________________________________________________

```
Middle
```

Current element.

______________________________________________________________________

Initially

```text
Left

↓

-1 0 3 5 9 12

              ↑

            Right
```

______________________________________________________________________

# Step-by-Step Dry Run

Input

```text
[-1,0,3,5,9,12]
```

Target

```
9
```

______________________________________________________________________

Iteration 1

```
Left

0
```

```
Right

5
```

Middle

```
2
```

Value

```
3
```

Target larger.

Move

```
Left

↓

3
```

______________________________________________________________________

Iteration 2

Search Space

```text
5 9 12
```

Middle

```
4
```

Value

```
9
```

Found.

Return

```
4
```

______________________________________________________________________

# Visual Explanation

```
-1 0 3 5 9 12

L       M      R
```

Target

```
9
```

↓

Discard Left Half

```
5 9 12

L M R
```

↓

Found.

______________________________________________________________________

# Why It Works

Loop Invariant:

> Before every iteration,
>
> if the target exists,
>
> it is guaranteed to be inside the current search space:
>
> ```text
> [left, right]
> ```

Each comparison removes **half** the remaining search space.

Eventually,

either:

- Target is found.
- Search space becomes empty.

______________________________________________________________________

# Why Is It So Fast?

Suppose

```
1 Million Elements
```

Linear Search

Worst case

```
1,000,000

comparisons
```

Binary Search

```
1,000,000

↓

500,000

↓

250,000

↓

125,000

↓

...
```

Only about

```
20
```

comparisons.

That's why Binary Search is incredibly powerful.

______________________________________________________________________

# Why Calculate Mid Like This?

Most people write:

```python
mid = (left + right) // 2
```

In Python,

this is perfectly safe.

However,

in languages like Java or C++,

large values can overflow.

Safer formula

```python
mid = left + (right - left) // 2
```

Professional interviewers appreciate this version because it's portable across languages.

______________________________________________________________________

# Edge Cases

### Empty Array

```text
[]
```

Return

```
-1
```

______________________________________________________________________

### One Element

```text
[5]
```

Target

```
5
```

Return

```
0
```

______________________________________________________________________

### Target Not Found

```text
1 2 3
```

Target

```
10
```

Return

```
-1
```

______________________________________________________________________

### First Element

Return

```
0
```

______________________________________________________________________

### Last Element

Return last index.

______________________________________________________________________

# Complexity Analysis

## Linear Search

Time

```
O(n)
```

Space

```
O(1)
```

______________________________________________________________________

## Binary Search

Time

```
O(log n)
```

Space

```
O(1)
```

Every iteration halves the search space.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def search(numbers: List[int], target: int) -> int:
    for index, value in enumerate(numbers):
        if value == target:
            return index

    return -1
```

______________________________________________________________________

## Optimized (Iterative Binary Search)

```python
from typing import List


def binary_search(
    numbers: List[int],
    target: int,
) -> int:
    left = 0
    right = len(numbers) - 1

    while left <= right:
        middle = left + (right - left) // 2

        if numbers[middle] == target:
            return middle

        if numbers[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1


if __name__ == "__main__":
    values = [-1, 0, 3, 5, 9, 12]

    print(binary_search(values, 9))
```

______________________________________________________________________

## Recursive Version

```python
from typing import List


def binary_search(
    numbers: List[int],
    target: int,
) -> int:
    def search(left: int, right: int) -> int:
        if left > right:
            return -1

        middle = left + (right - left) // 2

        if numbers[middle] == target:
            return middle

        if numbers[middle] < target:
            return search(middle + 1, right)

        return search(left, middle - 1)

    return search(0, len(numbers) - 1)
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using Binary Search on an unsorted array.

Binary Search **requires sorted data**.

______________________________________________________________________

## Mistake 2

Using

```python
while left < right
```

instead of

```python
while left <= right
```

The last remaining element might never be checked.

______________________________________________________________________

## Mistake 3

Updating boundaries incorrectly.

Wrong

```python
left = middle
```

Correct

```python
left = middle + 1
```

Otherwise,

the search space doesn't shrink,

leading to an infinite loop.

______________________________________________________________________

## Mistake 4

Returning immediately when the search space becomes one element without checking it.

Always allow the loop to inspect the final candidate.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A linear search takes O(n) time. Since the array is sorted, I can eliminate half of the remaining elements after each comparison. I'll maintain `left` and `right` boundaries, compute the middle index, compare the middle value with the target, and shrink the search space accordingly until I either find the target or the search space becomes empty."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why must the array be sorted?**

Because Binary Search relies on ordering to safely discard half the search space.

______________________________________________________________________

**Q. Why use `left <= right`?**

It ensures the final remaining element is checked.

______________________________________________________________________

**Q. Why move `left = middle + 1` instead of `middle`?**

To guarantee progress and avoid infinite loops.

______________________________________________________________________

**Q. Where is Binary Search used in backend engineering?**

- Database indexes
- Storage engines
- Search services
- Pagination
- Scheduling
- Resource allocation

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Divide and Conquer |
| Recognition | Sorted Search Space |
| Brute Force | Linear Search |
| Optimized | Binary Search |
| Time | O(log n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Binary Search requires sorted data.
- Maintain `left` and `right`.
- Compute `middle`.
- Compare with the target.
- Eliminate half the search space.
- Continue until `left > right`.
- Time complexity is O(log n).
- One of the most fundamental interview algorithms.

______________________________________________________________________

# Practice Questions

## Easy

1. Search Insert Position
1. Guess Number Higher or Lower
1. Valid Perfect Square

______________________________________________________________________

## Medium

4. Search in Rotated Sorted Array
1. Koko Eating Bananas
1. Capacity To Ship Packages Within D Days
1. Find Peak Element

______________________________________________________________________

## Hard (Optional)

8. Median of Two Sorted Arrays
1. Split Array Largest Sum
1. Russian Doll Envelopes

______________________________________________________________________

# Key Takeaway

The biggest lesson from Binary Search is that **you don't search faster by checking more—you search faster by
eliminating impossible answers**. Whenever a problem has a **sorted search space**, think about how each comparison can
safely discard half of the remaining candidates. This mindset is far more important than memorizing the code.

______________________________________________________________________

# Next

[36-first-and-last-position-in-sorted-array.md](36-first-and-last-position-in-sorted-array.md)
