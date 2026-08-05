# 11-remove-duplicates.md

# Remove Duplicates from Sorted Array

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

This problem is **not** about removing duplicates.

It's about whether you understand:

- Two Pointer technique
- In-place modification
- Reading and writing using different pointers
- Space optimization

Most beginners immediately think:

> "I'll create a new array."

The interviewer intentionally adds the constraint:

> **Modify the array in-place using O(1) extra space.**

That's what they're actually testing.

______________________________________________________________________

# Problem Statement

You are given a **sorted** array.

Remove all duplicate elements **in-place**.

Return the number of unique elements.

The first `k` elements of the array should contain only unique values.

______________________________________________________________________

## Example 1

```text
Input

[1,1,2]
```

Output

```text
k = 2

Array

[1,2,_]
```

The value after index `k` doesn't matter.

______________________________________________________________________

## Example 2

```text
Input

[0,0,1,1,1,2,2,3,3,4]
```

Output

```text
k = 5

Array

[0,1,2,3,4,_,_,_,_,_]
```

______________________________________________________________________

# Simple English

Imagine students standing in a line.

```
A

A

B

B

B

C

D

D
```

Your job isn't to create another line.

Your job is to move students forward so that only one student of each name remains.

```
A

B

C

D

_

_

_

_
```

______________________________________________________________________

# Backend Engineering Analogy

Suppose a database query returns sorted user IDs.

```
101

101

101

205

205

300
```

Before sending the response,

you want only unique IDs.

Instead of creating another list,

you overwrite duplicates in the same memory buffer.

This reduces memory usage.

The same idea appears in:

- Database result processing
- Log deduplication
- Cache cleanup
- Streaming pipelines

______________________________________________________________________

# Pattern Recognition

## Pattern

**Two Pointers**

______________________________________________________________________

## Recognition Clues

If the question contains phrases like:

- Sorted array
- Remove duplicates
- Modify in-place
- Constant extra space
- Compress array
- Shift elements

Think:

```
Two Pointers
```

One pointer reads.

One pointer writes.

______________________________________________________________________

# Brute Force Solution

## Intuition

Create another array.

Whenever a new value appears,

add it.

Ignore duplicates.

______________________________________________________________________

## Algorithm

Input

```
[1,1,2,2,3]
```

New array

```
[]
```

Read

```
1

↓

[1]
```

Read

```
1

Duplicate

Ignore
```

Read

```
2

↓

[1,2]
```

Read

```
2

Ignore
```

Read

```
3

↓

[1,2,3]
```

Done.

______________________________________________________________________

## Dry Run

```
Input

1 1 2 3 3
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
[1]
```

↓

```
[1,2]
```

↓

```
[1,2,3]
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

The interviewer explicitly says

```
Modify in-place
```

Creating another array violates the requirement.

______________________________________________________________________

# Optimized Solution (Two Pointers)

## Key Insight

Because the array is sorted,

duplicates are adjacent.

Example

```
1 1 1 2 2 3 4 4
```

We don't need another array.

We simply overwrite duplicates.

______________________________________________________________________

# Understanding the Two Pointers

We'll use two pointers.

```
Read Pointer

↓

Scans every element.
```

```
Write Pointer

↓

Points to the next unique position.
```

______________________________________________________________________

Initially

```
Array

1 1 2 3 3
```

```
Write

↓

1
```

```
Read

↓

1
```

______________________________________________________________________

Read moves to second element.

```
1

Same as previous

Ignore
```

Write stays.

______________________________________________________________________

Read moves again.

```
2

Different

↓

Copy to write position.
```

Array becomes

```
1 2 2 3 3
```

Move write.

______________________________________________________________________

Continue.

______________________________________________________________________

# Step-by-Step Dry Run

Input

```
[1,1,2,3,3]
```

Initially

```
Write = 0

Read = 1
```

______________________________________________________________________

### Read = 1

```
1

==

1
```

Duplicate.

Ignore.

______________________________________________________________________

### Read = 2

```
2

!=

1
```

Copy.

```
1 2 2 3 3
```

```
Write = 1
```

______________________________________________________________________

### Read = 3

```
3

!=

2
```

Copy.

```
1 2 3 3 3
```

```
Write = 2
```

______________________________________________________________________

### Read = 4

```
3

==

3
```

Duplicate.

Ignore.

Finished.

Unique count

```
Write + 1

=

3
```

______________________________________________________________________

# Visual Explanation

Original

```
Index

0 1 2 3 4

↓

1 1 2 3 3
```

Step 1

```
W
R

1 1 2 3 3
```

______________________________________________________________________

Step 2

```
Duplicate

Move Read
```

```
W

R

1 1 2 3 3
```

______________________________________________________________________

Step 3

```
Unique

Copy

1 2 2 3 3
```

```
    W

      R
```

______________________________________________________________________

Step 4

```
Unique

1 2 3 3 3
```

```
      W

        R
```

Done.

Only the first

```
3
```

elements matter.

______________________________________________________________________

# Why This Works

Because the array is sorted,

all duplicates appear together.

The **read pointer** visits every element.

Whenever a new unique value is found,

the **write pointer** stores it.

Loop Invariant:

> Before each iteration, all elements from index `0` to `write` are unique and correctly placed.

At the end,

the first

```
write + 1
```

elements contain every unique value exactly once.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

Return

```
0
```

______________________________________________________________________

### One Element

```
[7]
```

Return

```
1
```

______________________________________________________________________

### All Duplicates

```
[5,5,5,5]
```

Return

```
1
```

______________________________________________________________________

### No Duplicates

```
[1,2,3,4]
```

Return

```
4
```

______________________________________________________________________

### Large Array

Still works in

```
O(n)
```

time.

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

No extra array is created.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def remove_duplicates(numbers: List[int]) -> int:
    if not numbers:
        return 0

    unique_numbers = [numbers[0]]

    for number in numbers[1:]:
        if number != unique_numbers[-1]:
            unique_numbers.append(number)

    numbers[: len(unique_numbers)] = unique_numbers

    return len(unique_numbers)
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List


def remove_duplicates(numbers: List[int]) -> int:
    if not numbers:
        return 0

    write = 0

    for read in range(1, len(numbers)):
        if numbers[read] != numbers[write]:
            write += 1
            numbers[write] = numbers[read]

    return write + 1


if __name__ == "__main__":
    values = [0, 0, 1, 1, 2, 2, 3]

    length = remove_duplicates(values)

    print(length)
    print(values[:length])
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Creating another array.

The interviewer specifically asks for

```
O(1)
```

extra space.

______________________________________________________________________

## Mistake 2

Using only one pointer.

You need

- one pointer to read
- one pointer to write

______________________________________________________________________

## Mistake 3

Moving the write pointer every iteration.

Move it **only when a new unique value is found**.

______________________________________________________________________

## Mistake 4

Returning

```python
write
```

instead of

```python
write + 1
```

Because `write` stores the **index**, not the count.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Since the array is sorted, duplicate values appear next to each other. I can maintain two pointers: one to read every element and another to write only unique values. This lets me modify the array in-place while using constant extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why does sorting matter?**

Because duplicates become adjacent.

Without sorting,

this approach doesn't work.

______________________________________________________________________

**Q. Why are two pointers needed?**

One scans the input.

One tracks where the next unique value should be written.

______________________________________________________________________

**Q. Can this work for an unsorted array?**

Not with O(1) extra space.

You'd typically need a hash set.

______________________________________________________________________

**Q. What happens to the remaining elements?**

They don't matter.

Only the first `k` elements are considered valid.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Two Pointers |
| Recognition | Sorted Array + In-place Modification |
| Brute Force | Extra Array |
| Optimized | Read/Write Pointers |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- The array is already sorted.
- Duplicates are adjacent.
- Use one pointer to read.
- Use another pointer to write unique values.
- Move the write pointer only when a new value is found.
- Return `write + 1`.
- Time complexity is O(n).
- Space complexity is O(1).
- This is one of the most important Two Pointer interview patterns.

______________________________________________________________________

# Practice Questions

## Easy

1. Remove Element
1. Merge Sorted Array
1. Remove Duplicates from Sorted List

______________________________________________________________________

## Medium

4. Remove Duplicates from Sorted Array II
1. Sort Colors
1. Move Zeroes
1. Partition Array According to Pivot

______________________________________________________________________

## Hard (Optional)

8. First Missing Positive
1. Trapping Rain Water
1. Median of Two Sorted Arrays

______________________________________________________________________

# Key Takeaway

The biggest lesson is understanding the **Read-Write Pointer** pattern. One pointer explores the input, while the other
builds the desired output **in the same array**. This pattern appears repeatedly in array, string, and linked list
interview problems, making it one of the most valuable techniques to master.

______________________________________________________________________

# Next

[12-move-zeroes.md](12-move-zeroes.md)
