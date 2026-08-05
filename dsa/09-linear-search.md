# 09-linear-search.md

# Linear Search

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 10–15 minutes |
| Revision Time | 5 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Linear Search is probably the simplest searching algorithm.

Yet, interviewers ask it because it tests whether you understand:

- Array traversal
- Loops
- Early termination
- Time complexity
- When a simple solution is actually the best solution

Many candidates immediately think about **Binary Search** whenever they hear the word "search."

However, Binary Search only works on **sorted** data.

If the data is **unsorted**, Linear Search is often the correct choice.

Understanding **when NOT to optimize** is an important engineering skill.

______________________________________________________________________

# Problem Statement

Given an array and a target value,

find the index of the target.

If the target doesn't exist,

return `-1`.

______________________________________________________________________

## Example 1

```text
Input

numbers = [10, 25, 7, 15, 30]

target = 15
```

Output

```text
3
```

______________________________________________________________________

## Example 2

```text
Input

numbers = [10, 25, 7, 15, 30]

target = 100
```

Output

```text
-1
```

______________________________________________________________________

# Simple English

Imagine you're looking for a specific book on a shelf.

The books are **not arranged alphabetically**.

The only option is:

```
Look at first book

↓

Look at second book

↓

Look at third book

↓

...

Until found
```

That's exactly what Linear Search does.

______________________________________________________________________

# Common Misunderstandings

### Does Linear Search require sorting?

No.

It works on:

```
[9, 2, 7, 1, 15]
```

as well as

```
[1, 2, 7, 9, 15]
```

Sorting is **not required**.

______________________________________________________________________

### Does it always check every element?

No.

It stops immediately after finding the target.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a backend service stores a small list of feature flags.

```python
[
    "beta-login",
    "dark-mode",
    "new-dashboard",
    "chatbot"
]
```

A request asks:

```
Is "chatbot" enabled?
```

The service checks each flag one by one.

Since the list is tiny,

using a database index or binary search would actually make the solution more complicated.

Linear Search is often perfectly acceptable for small datasets.

Other examples:

- Finding a user in a short in-memory list
- Searching API routes
- Configuration lookup
- Middleware execution chain
- Request validation

______________________________________________________________________

# Pattern Recognition

### Pattern

**Sequential Traversal**

Recognition clues

Whenever you see:

- Search in unsorted array
- Find first occurrence
- Check every element
- Scan the list

Think

```
Traverse from left to right
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Check every element.

If it matches,

return its index.

Otherwise,

continue.

If you reach the end,

return

```
-1
```

______________________________________________________________________

## Algorithm

```
Array

10 25 7 15 30

Target

15
```

Compare

```
10

↓

No
```

```
25

↓

No
```

```
7

↓

No
```

```
15

↓

Yes

↓

Return index 3
```

______________________________________________________________________

## Dry Run

Input

```
[5, 11, 8, 20]

Target = 8
```

Iteration 1

```
Index 0

Value 5

No
```

Iteration 2

```
Index 1

Value 11

No
```

Iteration 3

```
Index 2

Value 8

Found

Return 2
```

Stop immediately.

______________________________________________________________________

## Complexity

### Best Case

Target is the first element.

```
O(1)
```

______________________________________________________________________

### Worst Case

Target is last element

or doesn't exist.

```
O(n)
```

______________________________________________________________________

### Space

```
O(1)
```

______________________________________________________________________

## Limitations

Suppose the array contains

```
10 million elements.
```

Searching one by one becomes expensive.

If the array is sorted,

Binary Search is much faster.

We'll study that later.

______________________________________________________________________

# Optimized Solution

## Is There Any Better Algorithm?

For an **unsorted array**,

**No.**

This is an important interview lesson.

Many candidates try to invent a faster algorithm.

Interviewers expect you to say:

> "Since the data is unsorted and we need to find an arbitrary element, every algorithm may need to inspect every element in the worst case. Therefore, O(n) is optimal."

This is your optimized solution.

______________________________________________________________________

## Small Optimization

Instead of

```python
for i in range(len(numbers)):
```

Python allows

```python
enumerate(numbers)
```

This is cleaner and more readable.

The complexity remains the same.

______________________________________________________________________

# Visual Explanation

Searching

```
[8, 12, 4, 25, 30]
```

Target

```
25
```

```
Index

0

↓

1

↓

2

↓

3

↓

Found

↓

Stop
```

Notice

```
Element

30
```

is never checked.

Because the search stops immediately.

______________________________________________________________________

# Why This Works

The algorithm guarantees correctness because:

- Every element is checked exactly once.
- If the target exists,
eventually it will be visited.
- If the target doesn't exist,
every element is examined before returning `-1`.

There is no possibility of missing an element.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

Return

```
-1
```

______________________________________________________________________

### Single Element (Found)

```
[8]

Target

8

↓

0
```

______________________________________________________________________

### Single Element (Not Found)

```
[8]

Target

2

↓

-1
```

______________________________________________________________________

### Duplicate Values

```
[5, 8, 8, 10]
```

Return the **first occurrence** unless stated otherwise.

______________________________________________________________________

### Large Arrays

Still works,

but performance becomes

```
O(n)
```

______________________________________________________________________

# Complexity Analysis

| Case | Time |
|------|------|
| Best | O(1) |
| Average | O(n) |
| Worst | O(n) |

Space

```
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def linear_search(numbers: List[int], target: int) -> int:
    for index, value in enumerate(numbers):
        if value == target:
            return index

    return -1


if __name__ == "__main__":
    values = [10, 25, 7, 15, 30]

    print(linear_search(values, 15))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Forgetting to return

```
-1
```

when the element isn't found.

______________________________________________________________________

## Mistake 2

Returning the value instead of the index.

Question asks for

```
Index
```

not

```
Element
```

______________________________________________________________________

## Mistake 3

Looping one step too far.

Wrong

```python
range(len(numbers) + 1)
```

This causes

```
IndexError
```

______________________________________________________________________

## Mistake 4

Continuing the search after finding the target.

Once found,

return immediately.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Since the array is unsorted, the only guaranteed way to find the target is to inspect elements one by one. I'll traverse the array from left to right and stop immediately when I find the target. In the worst case, I may have to examine every element, giving O(n) time complexity."

______________________________________________________________________

### Common Follow-up Questions

**Q. Can this be faster?**

Not for an unsorted array.

______________________________________________________________________

**Q. When should I use Binary Search instead?**

When the data is sorted.

______________________________________________________________________

**Q. Why return immediately?**

There's no need to inspect the remaining elements once the target has been found.

______________________________________________________________________

**Q. Why use `enumerate()`?**

It provides both the index and the value, making the code cleaner and more Pythonic.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Sequential Traversal |
| Recognition | Unsorted Search |
| Brute Force | Scan Every Element |
| Optimized | Linear Search (Already Optimal) |
| Best Time | O(1) |
| Worst Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Linear Search works on both sorted and unsorted arrays.
- Traverse elements one by one.
- Stop immediately when the target is found.
- Return `-1` if the target doesn't exist.
- Best case is O(1).
- Worst case is O(n).
- For unsorted arrays, O(n) is optimal.
- Prefer `enumerate()` in Python.

______________________________________________________________________

# Practice Questions

## Easy

1. Search Insert Position
1. Find Numbers with Even Number of Digits
1. Check If N and Its Double Exist

______________________________________________________________________

## Medium

4. First Missing Positive
1. Find Peak Element
1. Search a 2D Matrix
1. Search in Rotated Sorted Array *(observe why Linear Search is not ideal)*

______________________________________________________________________

## Hard (Optional)

8. Median of Two Sorted Arrays
1. Find Minimum in Rotated Sorted Array II
1. Search in Rotated Sorted Array II

______________________________________________________________________

# Key Takeaway

The biggest lesson from Linear Search is **choosing the right algorithm for the given data**. Optimization isn't always
about using a more complex algorithm—it's about understanding the constraints. For an unsorted array, Linear Search is
not just the simplest solution; it's also the **optimal** one in the general case.

______________________________________________________________________

# Next

[10-largest-second-largest.md](10-largest-second-largest.md)
