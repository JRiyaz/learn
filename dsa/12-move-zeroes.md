# 12-move-zeroes.md

# Move Zeroes

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem is **not** about moving zeroes.

It is actually about understanding:

- Two Pointer pattern
- In-place array modification
- Stable ordering
- Swapping elements
- Efficient traversal

Many candidates solve this by creating a new array.

Interviewers intentionally add the constraint:

> **Do it in-place without creating another array.**

This problem builds directly on **Remove Duplicates from Sorted Array**.

Instead of skipping duplicates, we skip **zeroes**.

______________________________________________________________________

# Problem Statement

Given an integer array,

move all `0`s to the end of the array **while maintaining the relative order of non-zero elements**.

The operation must be performed **in-place**.

______________________________________________________________________

## Example 1

```text
Input

[0,1,0,3,12]
```

Output

```text
[1,3,12,0,0]
```

______________________________________________________________________

## Example 2

```text
Input

[1,2,3]
```

Output

```text
[1,2,3]
```

______________________________________________________________________

## Example 3

```text
Input

[0,0,0]
```

Output

```text
[0,0,0]
```

______________________________________________________________________

# Simple English

Imagine people standing in a queue.

Some positions are empty.

```
_ A _ B C _ D
```

Your job is to move everyone forward,

while keeping their order.

```
A B C D _ _ _
```

Notice:

```
A

stays before

B

B

stays before

C
```

The relative order never changes.

______________________________________________________________________

# Common Misunderstanding

Many people think:

```
Move all zeroes
```

means

```
Sort the array.
```

Wrong.

Sorting

```
[0,1,0,3,12]
```

produces

```
[0,0,1,3,12]
```

This is **not** the expected answer.

The order of non-zero elements must remain unchanged.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a message queue.

Some messages are marked as

```
Deleted
```

represented by

```
0
```

Instead of creating another queue,

you compact the existing queue by moving valid messages forward.

This is called **compaction**.

Similar ideas appear in:

- Kafka log compaction
- Garbage collection
- Memory compaction
- Database page cleanup

______________________________________________________________________

# Pattern Recognition

## Pattern

**Two Pointers (Read & Write)**

______________________________________________________________________

## Recognition Clues

If the question contains phrases like:

- Move elements
- Shift values
- Maintain order
- In-place
- Constant space
- Stable order

Think

```
Read Pointer

+

Write Pointer
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Create another array.

First,

copy all non-zero values.

Then,

append zeroes.

______________________________________________________________________

## Algorithm

Input

```
[0,1,0,3,12]
```

New array

```
[]
```

Copy non-zeroes

```
[1]

↓

[1,3]

↓

[1,3,12]
```

Append zeroes

```
[1,3,12,0,0]
```

______________________________________________________________________

## Dry Run

```
Input

0 1 0 3 12
```

```
New Array

[]
```

↓

```
[1]
```

↓

```
[1,3]
```

↓

```
[1,3,12]
```

↓

```
[1,3,12,0,0]
```

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

______________________________________________________________________

## Limitations

Uses another array.

The interviewer explicitly asks for

```
O(1)
```

extra space.

______________________________________________________________________

# Optimized Solution (Two Pointers)

## Key Insight

Instead of creating another array,

move every non-zero value to the earliest available position.

Everything after that automatically becomes zero.

______________________________________________________________________

## Understanding the Pointers

```
Read Pointer

↓

Scans every element.
```

```
Write Pointer

↓

Points to the next location where a non-zero value should go.
```

______________________________________________________________________

Initially

```
0 1 0 3 12

W
R
```

Read sees

```
0
```

Ignore.

Move read.

______________________________________________________________________

```
0 1 0 3 12

W
  R
```

Read sees

```
1
```

Swap

```
1 0 0 3 12
```

Move both pointers.

______________________________________________________________________

Continue until the end.

______________________________________________________________________

# Step-by-Step Dry Run

Input

```
[0,1,0,3,12]
```

Initially

```
Write = 0
```

______________________________________________________________________

### Read = 0

```
Value

0

Ignore
```

______________________________________________________________________

### Read = 1

```
Value

1

Swap with write
```

Array

```
1 0 0 3 12
```

Write

```
1
```

______________________________________________________________________

### Read = 2

```
0

Ignore
```

______________________________________________________________________

### Read = 3

Swap

```
1 3 0 0 12
```

______________________________________________________________________

### Read = 4

Swap

```
1 3 12 0 0
```

Done.

______________________________________________________________________

# Visual Explanation

Original

```
0 1 0 3 12
```

```
W
R
```

↓

```
0 1 0 3 12

W
  R
```

↓

Swap

```
1 0 0 3 12

  W
    R
```

↓

Ignore zero

↓

Swap

```
1 3 0 0 12

    W
        R
```

↓

Swap

```
1 3 12 0 0
```

Finished.

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before every iteration, all elements before the **write pointer** are non-zero and appear in their original relative order.

Every time the read pointer finds a non-zero element,

it is moved to the write pointer.

Since elements are processed from left to right,

their order never changes.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

No changes.

______________________________________________________________________

### All Zeroes

```
0 0 0
```

Nothing changes.

______________________________________________________________________

### No Zeroes

```
1 2 3
```

Already correct.

______________________________________________________________________

### Single Element

```
0
```

or

```
5
```

Works correctly.

______________________________________________________________________

### Large Arrays

Still requires only one traversal.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Optimized

Time

```
O(n)
```

Space

```
O(1)
```

Every element is visited exactly once.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def move_zeroes(numbers: List[int]) -> None:
    non_zeroes = [number for number in numbers if number != 0]
    zero_count = len(numbers) - len(non_zeroes)

    numbers[:] = non_zeroes + [0] * zero_count
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List


def move_zeroes(numbers: List[int]) -> None:
    write = 0

    for read in range(len(numbers)):
        if numbers[read] != 0:
            numbers[write], numbers[read] = (
                numbers[read],
                numbers[write],
            )
            write += 1


if __name__ == "__main__":
    values = [0, 1, 0, 3, 12]

    move_zeroes(values)

    print(values)
```

______________________________________________________________________

# Why Do We Swap?

Many students ask:

> "Why not simply assign the value?"

Example

```
0 1 0 3 12
```

If we only write

```
numbers[write] = numbers[read]
```

we overwrite data and lose values.

Swapping safely moves:

```
Non-zero

↓

Front
```

and

```
Zero

↓

Back
```

in one operation.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Sorting the array.

Sorting changes the relative order.

______________________________________________________________________

## Mistake 2

Creating another array.

Violates the in-place requirement.

______________________________________________________________________

## Mistake 3

Moving the write pointer for every element.

Move it **only** after processing a non-zero value.

______________________________________________________________________

## Mistake 4

Not preserving the order of non-zero elements.

This is one of the key requirements.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The straightforward solution is to create a new array containing all non-zero elements and then append zeroes. However, since the problem requires in-place modification, I'll use two pointers. The read pointer scans every element, while the write pointer tracks where the next non-zero element should be placed. This preserves the relative order and uses constant extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use two pointers?**

One reads the original array.

One builds the compacted array.

______________________________________________________________________

**Q. Why swap instead of overwrite?**

Swapping keeps all values intact without requiring an additional pass to restore overwritten elements.

> **Note:** An alternative optimized solution performs two passes:
>
> 1. Copy all non-zero values forward.
> 1. Fill the remaining positions with zeroes.
>
> This avoids unnecessary swaps and is also accepted in interviews.

______________________________________________________________________

**Q. Does the order of non-zero elements change?**

No.

The algorithm is stable.

______________________________________________________________________

**Q. Why is this considered a Two Pointer problem?**

Because two indices move independently:

- Read pointer scans.
- Write pointer tracks the next insertion position.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Two Pointers |
| Recognition | Move / Shift / Compact In-place |
| Brute Force | Extra Array |
| Optimized | Read & Write Pointers |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Don't sort the array.
- Preserve the order of non-zero elements.
- Use one pointer to read.
- Use one pointer to write.
- Ignore zeroes.
- Swap non-zero values into the write position.
- Move the write pointer only after processing a non-zero value.
- Time complexity is O(n).
- Space complexity is O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Remove Element
1. Remove Duplicates from Sorted Array
1. Duplicate Zeros

______________________________________________________________________

## Medium

4. Sort Colors
1. Partition Array According to Pivot
1. Wiggle Sort
1. Squares of a Sorted Array

______________________________________________________________________

## Hard (Optional)

8. First Missing Positive
1. Trapping Rain Water
1. Candy Crush (Array Simulation)

______________________________________________________________________

# Key Takeaway

The core lesson is the **Read-Write Pointer** technique. Instead of creating another array, you **compact** the existing
array by continuously placing valid elements into the earliest available position. This idea appears in memory
compaction, database storage engines, log cleanup, and many interview problems involving in-place array modifications.

______________________________________________________________________

# Next

[13-rotate-array.md](13-rotate-array.md)
