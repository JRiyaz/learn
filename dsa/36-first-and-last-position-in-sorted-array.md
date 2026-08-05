# 36-first-and-last-position-in-sorted-array.md

# Find First and Last Position of Element in Sorted Array

> **🎯 This lesson teaches the most important Binary Search variation.**
>
> Most interview questions are **not** about finding whether an element exists.
>
> They are about finding:
>
> - First occurrence
> - Last occurrence
> - Lower Bound
> - Upper Bound
> - Insertion Position
> - Boundary Conditions
>
> If you understand this lesson, you can solve a huge family of Binary Search problems.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 30–35 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Most candidates know ordinary Binary Search.

Interviewers ask this question to test whether you understand:

- Binary Search variations
- Boundary searching
- Duplicate values
- Loop invariants
- Off-by-one handling

This pattern appears in:

- Database indexes
- Log processing
- Time-series queries
- Search engines
- Analytics systems

______________________________________________________________________

# Problem Statement

Given a **sorted array** and a target value,

find:

- The **first occurrence**
- The **last occurrence**

Return

```text
[first_index, last_index]
```

If the target does not exist,

return

```text
[-1, -1]
```

______________________________________________________________________

## Example 1

Input

```text
Numbers

[5,7,7,8,8,10]

Target

8
```

Output

```text
[3,4]
```

______________________________________________________________________

## Example 2

Input

```text
[5,7,7,8,8,10]

Target

6
```

Output

```text
[-1,-1]
```

______________________________________________________________________

# Before Learning the Algorithm

Suppose

```text
1 2 2 2 2 3 4
```

Ordinary Binary Search finds

```
2
```

Maybe

```text
Index 2
```

But

Is it the first?

Maybe not.

Need

```
Boundary Search
```

______________________________________________________________________

# Simple English

Imagine a row of students.

```
A A A B B B C
```

Someone asks:

Where does

```
B
```

start?

Where does

```
B
```

end?

You aren't looking for

```
A B C
```

You're looking for the **boundary**.

______________________________________________________________________

# Backend Engineering Analogy

Suppose database logs are sorted by status.

```
ERROR

ERROR

ERROR

INFO

INFO

WARNING
```

You need

```
All ERROR rows.
```

First,

find where

```
ERROR
```

starts.

Then,

find where it ends.

Exactly the same problem.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Binary Search on Boundaries**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- First occurrence
- Last occurrence
- Lower bound
- Upper bound
- Range
- Leftmost
- Rightmost

Think

```
Modified Binary Search
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Scan the array.

Remember

- first match
- last match

______________________________________________________________________

## Algorithm

Input

```text
5 7 7 8 8 10
```

Need

```
8
```

Scan

```
5

↓

7

↓

7

↓

8

First = 3
```

Continue

↓

```
8

Last = 4
```

Done.

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

Ignores the fact that the array is sorted.

______________________________________________________________________

# Better Observation

Ordinary Binary Search stops immediately after finding

```
8
```

Instead,

continue searching.

______________________________________________________________________

For

```
First Occurrence
```

Search

```
Left Half
```

even after finding the target.

______________________________________________________________________

For

```
Last Occurrence
```

Search

```
Right Half
```

even after finding the target.

______________________________________________________________________

# Optimized Solution

We perform

```
Two Binary Searches
```

______________________________________________________________________

## Binary Search 1

Find

```
First Occurrence
```

Whenever target is found,

save answer.

Continue searching left.

______________________________________________________________________

## Binary Search 2

Find

```
Last Occurrence
```

Whenever target is found,

save answer.

Continue searching right.

______________________________________________________________________

# Dry Run (First Occurrence)

Input

```text
5 7 7 8 8 10
```

Target

```
8
```

______________________________________________________________________

Iteration 1

Middle

```
7
```

Move Right.

______________________________________________________________________

Iteration 2

Middle

```
8
```

Save

```
3
```

Continue Left.

Search Space

```
5 7 7
```

Done.

First

```
3
```

______________________________________________________________________

# Dry Run (Last Occurrence)

Input

```text
5 7 7 8 8 10
```

Middle

```
8
```

Save

```
3
```

Continue Right.

Later

Find

```
8
```

again.

Save

```
4
```

Continue Right.

Finished.

Answer

```
4
```

______________________________________________________________________

# Visual Explanation

Array

```text
5 7 7 8 8 10
```

Target

```
8
```

```
L      M      R
```

↓

Found.

Save.

↓

Continue Left.

First occurrence found.

______________________________________________________________________

Repeat

↓

Continue Right.

Last occurrence found.

______________________________________________________________________

# Why Doesn't Ordinary Binary Search Work?

Suppose

```text
2 2 2 2 2
```

Ordinary search might return

```
2
```

at

```
Index 2
```

Need

```
0
```

and

```
4
```

Therefore,

finding the target isn't enough.

Need

```
Boundary
```

______________________________________________________________________

# Why This Works

Loop Invariant (First Occurrence):

> If the target exists further left,
> it is still inside the current search space.

Whenever the target is found,

store the index,

but continue searching left.

______________________________________________________________________

Loop Invariant (Last Occurrence):

> If the target exists further right,
> it is still inside the current search space.

Store the answer,

continue searching right.

Eventually,

the search space becomes empty,

and the stored index is the correct boundary.

______________________________________________________________________

# General Pattern

This lesson introduces one of the most useful interview ideas:

Instead of asking:

```
Did I find it?
```

Ask:

```
Can there still be a better answer?
```

If yes,

continue Binary Search.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

Return

```
[-1,-1]
```

______________________________________________________________________

### One Element

```
[5]
```

Target

```
5
```

Return

```
[0,0]
```

______________________________________________________________________

### Target Missing

Return

```
[-1,-1]
```

______________________________________________________________________

### All Same Values

```text
2 2 2 2
```

Return

```
[0,3]
```

______________________________________________________________________

### Target at Beginning

Works correctly.

______________________________________________________________________

### Target at End

Works correctly.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n)
```

Space

```
O(1)
```

______________________________________________________________________

## Optimized

Two Binary Searches

Each

```
O(log n)
```

Overall

```
O(log n)
```

Space

```
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def search_range(
    numbers: List[int],
    target: int,
) -> List[int]:
    def find_first() -> int:
        left = 0
        right = len(numbers) - 1
        answer = -1

        while left <= right:
            middle = left + (right - left) // 2

            if numbers[middle] == target:
                answer = middle
                right = middle - 1
            elif numbers[middle] < target:
                left = middle + 1
            else:
                right = middle - 1

        return answer

    def find_last() -> int:
        left = 0
        right = len(numbers) - 1
        answer = -1

        while left <= right:
            middle = left + (right - left) // 2

            if numbers[middle] == target:
                answer = middle
                left = middle + 1
            elif numbers[middle] < target:
                left = middle + 1
            else:
                right = middle - 1

        return answer

    return [find_first(), find_last()]


if __name__ == "__main__":
    values = [5, 7, 7, 8, 8, 10]

    print(search_range(values, 8))
```

______________________________________________________________________

# Even Better Design (Reusable Boundary Function)

Many senior engineers avoid writing two separate Binary Searches.

Instead,

they create one reusable function.

```python
def boundary_search(find_first: bool):
```

Inside,

only one line changes.

First occurrence

```python
right = middle - 1
```

Last occurrence

```python
left = middle + 1
```

This avoids duplicate code.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Returning immediately after finding the target.

You haven't found the boundary yet.

______________________________________________________________________

## Mistake 2

Forgetting to save the answer.

Always store the current index before continuing.

______________________________________________________________________

## Mistake 3

Searching the wrong side.

First occurrence

↓

Search left.

Last occurrence

↓

Search right.

______________________________________________________________________

## Mistake 4

Using Linear Search after Binary Search.

That defeats the purpose.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A linear scan works in O(n), but the array is sorted. Ordinary Binary Search only finds one occurrence, not necessarily the first or last. I'll perform two modified Binary Searches. In the first, whenever I find the target, I store the index and continue searching the left half. In the second, I store the index and continue searching the right half. This finds both boundaries in O(log n) time."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why perform two Binary Searches?**

Because the conditions for finding the left boundary and right boundary are different.

______________________________________________________________________

**Q. Why not stop after finding the target?**

The target may appear multiple times.

______________________________________________________________________

**Q. Why save the answer before continuing?**

The current match might already be the correct boundary.

If a better boundary exists,

it will be found by continuing the search.

______________________________________________________________________

**Q. Where is this pattern used in backend systems?**

- Database range queries
- Time-series data
- Search engines
- Analytics
- Log filtering

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Binary Search on Boundaries |
| Recognition | First/Last Occurrence |
| Brute Force | Linear Scan |
| Optimized | Two Modified Binary Searches |
| Time | O(log n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Ordinary Binary Search finds any occurrence.
- Boundary search finds the first or last occurrence.
- Save the answer when the target is found.
- Continue searching for a better boundary.
- First occurrence searches left.
- Last occurrence searches right.
- Overall complexity is O(log n).
- This pattern is the foundation of advanced Binary Search problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Search Insert Position
1. Find Smallest Letter Greater Than Target
1. Peak Index in a Mountain Array

______________________________________________________________________

## Medium

4. Find Peak Element
1. Search in Rotated Sorted Array
1. Find Minimum in Rotated Sorted Array
1. Koko Eating Bananas

______________________________________________________________________

## Hard (Optional)

8. Median of Two Sorted Arrays
1. Split Array Largest Sum
1. Find in Mountain Array

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is that **Binary Search is not just for finding values—it is for finding
boundaries**. Once you understand how to continue searching even after finding the target, you unlock an entire class of
interview problems involving ranges, insertion points, lower bounds, upper bounds, and optimization problems.

______________________________________________________________________

# Next

[37-bubble-sort.md](37-bubble-sort.md)
