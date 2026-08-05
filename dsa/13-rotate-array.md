# 13-rotate-array.md

# Rotate Array

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium (Easy Pattern) |
| Asked Frequency | Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 20–25 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem is not about rotating an array.

Interviewers use it to test whether you understand:

- Array manipulation
- Index calculations
- Modulo arithmetic
- In-place algorithms
- Reversal technique

Many candidates immediately create another array.

Interviewers then ask:

> "Can you do it in-place?"

The real interview is about reducing **space complexity** from **O(n)** to **O(1)**.

______________________________________________________________________

# Problem Statement

Given an integer array and an integer `k`, rotate the array to the **right** by `k` steps.

The rotation must be done **in-place**.

______________________________________________________________________

## Example 1

```text
Input

numbers = [1,2,3,4,5,6,7]

k = 3
```

Output

```text
[5,6,7,1,2,3,4]
```

______________________________________________________________________

## Example 2

```text
Input

numbers = [-1,-100,3,99]

k = 2
```

Output

```text
[3,99,-1,-100]
```

______________________________________________________________________

# Simple English

Imagine people standing in a circle.

```
A B C D E
```

Rotate once.

```
E A B C D
```

Rotate again.

```
D E A B C
```

Instead of moving one person at a time,

we want a smarter way.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a load balancer.

Servers are arranged as:

```
S1 S2 S3 S4
```

Every hour,

the primary server changes.

After rotation,

```
S4 S1 S2 S3
```

Another example:

A circular buffer used for:

- Kafka partitions
- Ring buffers
- Round-robin scheduling
- Token rotation

Rotation is a common operation in backend systems.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Array Reversal + Modulo Arithmetic**

______________________________________________________________________

## Recognition Clues

If the problem contains:

- Rotate array
- Circular shift
- In-place
- Constant extra space
- Wrap around

Think:

```
Reverse

+

Reverse

+

Reverse
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Rotate the array one step at a time.

Repeat this process `k` times.

______________________________________________________________________

## Algorithm

Example

```
[1,2,3,4,5]
```

Rotate once

```
[5,1,2,3,4]
```

Rotate again

```
[4,5,1,2,3]
```

Repeat until

```
k
```

rotations are completed.

______________________________________________________________________

## Dry Run

Input

```
[1,2,3,4]

k = 2
```

After first rotation

```
4 1 2 3
```

After second rotation

```
3 4 1 2
```

Done.

______________________________________________________________________

## Complexity

Each rotation moves every element.

Time

```
O(n × k)
```

Space

```
O(1)
```

______________________________________________________________________

## Limitations

Suppose

```
n = 1,000,000

k = 500,000
```

This becomes extremely slow.

Can we rotate everything at once?

Yes.

______________________________________________________________________

# Better Solution (Extra Array)

## Key Insight

Every element knows exactly where it should go.

Current index

```
i
```

New index

```
(i + k) % n
```

______________________________________________________________________

Example

```
Array

1 2 3 4 5
```

```
k = 2
```

Index

```
0

↓

2
```

Index

```
1

↓

3
```

Index

```
2

↓

4
```

Index

```
3

↓

0
```

Index

```
4

↓

1
```

New array

```
4 5 1 2 3
```

______________________________________________________________________

## Dry Run

```
numbers = [1,2,3,4,5]

k = 2
```

| Old Index | Value | New Index |
|-----------|------|-----------|
|0|1|2|
|1|2|3|
|2|3|4|
|3|4|0|
|4|5|1|

______________________________________________________________________

## Complexity

Time

```
O(n)
```

Space

```
O(n)
```

Much faster,

but requires another array.

______________________________________________________________________

# Optimized Solution (Three Reversals)

## Key Insight

This is one of the most beautiful interview tricks.

Instead of moving elements,

reverse sections of the array.

______________________________________________________________________

Example

```
1 2 3 4 5 6 7

k = 3
```

______________________________________________________________________

### Step 1

Reverse entire array

```
7 6 5 4 3 2 1
```

______________________________________________________________________

### Step 2

Reverse first

```
k
```

elements.

```
5 6 7 4 3 2 1
```

______________________________________________________________________

### Step 3

Reverse remaining elements.

```
5 6 7 1 2 3 4
```

Finished.

Exactly what we wanted.

______________________________________________________________________

# Why Does This Work?

Let's understand the intuition.

Original

```
1 2 3 4 | 5 6 7
```

Desired

```
5 6 7 | 1 2 3 4
```

Instead of moving two groups,

we:

Reverse everything

```
7 6 5 | 4 3 2 1
```

Reverse first group

```
5 6 7 | 4 3 2 1
```

Reverse second group

```
5 6 7 | 1 2 3 4
```

The order inside each group is restored.

The groups themselves are swapped.

______________________________________________________________________

# Visual Explanation

Original

```
1 2 3 4 5 6 7
```

↓

Reverse All

```
7 6 5 4 3 2 1
```

↓

Reverse First 3

```
5 6 7 4 3 2 1
```

↓

Reverse Remaining

```
5 6 7 1 2 3 4
```

Done.

______________________________________________________________________

# Important Observation

Suppose

```
k = 10

Array Length = 7
```

Rotating

```
10
```

times is the same as rotating

```
3
```

times.

Why?

```
10 % 7

=

3
```

Always begin with

```python
k %= len(numbers)
```

This avoids unnecessary work.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

Nothing to rotate.

______________________________________________________________________

### One Element

```
[5]
```

No change.

______________________________________________________________________

### k = 0

No rotation.

______________________________________________________________________

### k > n

Always compute

```
k % n
```

______________________________________________________________________

### Array Length = 0

Avoid division by zero.

Check

```python
if not numbers:
    return
```

before using modulo.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n × k)
```

Space

```
O(1)
```

______________________________________________________________________

## Extra Array

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Three-Reversal Technique

Time

```
O(n)
```

Space

```
O(1)
```

Best solution.

______________________________________________________________________

# Production-Quality Python

## Better Solution (Extra Array)

```python
from typing import List


def rotate(numbers: List[int], k: int) -> None:
    if not numbers:
        return

    length = len(numbers)
    k %= length

    rotated = [0] * length

    for index, value in enumerate(numbers):
        rotated[(index + k) % length] = value

    numbers[:] = rotated
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List


def reverse(
    numbers: List[int],
    left: int,
    right: int,
) -> None:
    while left < right:
        numbers[left], numbers[right] = (
            numbers[right],
            numbers[left],
        )
        left += 1
        right -= 1


def rotate(numbers: List[int], k: int) -> None:
    if not numbers:
        return

    length = len(numbers)
    k %= length

    reverse(numbers, 0, length - 1)
    reverse(numbers, 0, k - 1)
    reverse(numbers, k, length - 1)


if __name__ == "__main__":
    values = [1, 2, 3, 4, 5, 6, 7]

    rotate(values, 3)

    print(values)
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Forgetting

```python
k %= len(numbers)
```

Large values of `k` produce incorrect results.

______________________________________________________________________

## Mistake 2

Not checking for an empty array.

Calling

```python
k %= len(numbers)
```

when the array is empty causes

```
ZeroDivisionError
```

______________________________________________________________________

## Mistake 3

Reversing the wrong ranges.

Correct order:

1. Entire array
1. First `k`
1. Remaining elements

______________________________________________________________________

## Mistake 4

Thinking the reversal algorithm is magic.

Always visualize the two groups:

```
A | B

↓

Reverse

↓

Reverse A

↓

Reverse B
```

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The simplest solution rotates the array one step at a time, but that requires O(n × k) time. A better solution places each element directly into its new position using an extra array, giving O(n) time and O(n) space. Since the problem requires in-place modification, I'll use the three-reversal technique, which achieves O(n) time and O(1) extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use modulo?**

Because rotating by the array length results in the same array.

```
k %= n
```

reduces unnecessary rotations.

______________________________________________________________________

**Q. Why does the reversal algorithm work?**

It swaps the two groups while restoring their internal order.

______________________________________________________________________

**Q. Which solution would you use in production?**

If memory is available and readability is important, the extra-array solution is perfectly fine.

If memory efficiency is required or the interviewer explicitly asks for in-place modification, use the three-reversal
technique.

______________________________________________________________________

**Q. Is this a Two Pointer problem?**

Yes.

The `reverse()` helper uses two pointers moving toward each other.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Array Reversal |
| Recognition | Rotate / Circular Shift / In-place |
| Brute Force | Repeated Rotation |
| Better | Extra Array |
| Optimized | Three Reversals |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Rotating one step at a time is inefficient.
- Always compute `k %= len(array)`.
- Extra-array solution is O(n) time and O(n) space.
- Three-reversal solution is O(n) time and O(1) space.
- Reverse:
  1. Entire array
  1. First `k` elements
  1. Remaining elements
- Check for an empty array before using modulo.
- The reversal pattern is widely used in array problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Rotate String
1. Shift 2D Grid
1. Circular Array Rotation

______________________________________________________________________

## Medium

4. Rotate Image
1. Next Permutation
1. Cyclic Rotation
1. Circular Array Loop

______________________________________________________________________

## Hard (Optional)

8. Rotate List (Linked List)
1. Freedom Trail
1. Sliding Window Maximum on Circular Array

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is that **understanding the structure of the data can eliminate unnecessary
movement**. Instead of rotating elements individually, the **three-reversal technique** transforms the array with three
simple operations, achieving an elegant in-place solution that is frequently asked in interviews.

______________________________________________________________________

# Next

[14-best-time-to-buy-sell-stock.md](14-best-time-to-buy-sell-stock.md)
