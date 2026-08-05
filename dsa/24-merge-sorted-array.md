# 24-merge-sorted-array.md

# Merge Sorted Array

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 20–25 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This is one of the most misunderstood interview questions.

Many candidates immediately create a new array.

That works.

Then the interviewer asks:

> "Can you do it **in-place**?"

This problem teaches one of the most important interview patterns:

> **Two Pointers starting from the END**

Understanding this pattern helps in problems involving:

- In-place merging
- Array modification
- Memory optimization
- Sorted data processing

This exact idea is used in:

- Merge Sort
- Database merge operations
- Storage engines
- Log compaction
- External sorting

______________________________________________________________________

# Problem Statement

You are given two sorted arrays.

```text
numbers1
```

has enough extra space at the end to hold all elements.

```text
numbers2
```

contains additional sorted elements.

Merge them into

```text
numbers1
```

so that the final array remains sorted.

______________________________________________________________________

## Example

```text
Input

numbers1 = [1,2,3,0,0,0]

m = 3

numbers2 = [2,5,6]

n = 3
```

Output

```text
[1,2,2,3,5,6]
```

______________________________________________________________________

# Simple English

Imagine two sorted queues.

```
Queue A

1 2 3
```

```
Queue B

2 5 6
```

You want one sorted queue.

Most people start from the beginning.

That's difficult because inserting elements shifts everything.

Instead,

start from the back,

where empty space already exists.

______________________________________________________________________

# Backend Engineering Analogy

Suppose two database shards contain sorted records.

```
Shard A

100

200

300
```

```
Shard B

150

250

400
```

While merging,

it's expensive to repeatedly move earlier records.

Instead,

fill the output buffer from the end.

This minimizes data movement.

The same idea appears in:

- Merge Sort
- SSTable compaction (LSM Trees)
- External sorting
- File merging

______________________________________________________________________

# Pattern Recognition

## Pattern

**Two Pointers (Backward Traversal)**

______________________________________________________________________

## Recognition Clues

Whenever you see:

- Two sorted arrays
- Merge
- In-place
- Extra space at the end

Think

```
Start

↓

From the Back
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Create another array.

Merge exactly like Merge Sort.

Finally,

copy the merged result back.

______________________________________________________________________

## Algorithm

```
numbers1

1 2 3
```

```
numbers2

2 5 6
```

Compare

```
1

↓

Copy
```

Compare

```
2

2
```

Copy smaller.

Continue.

Result

```
1 2 2 3 5 6
```

Copy back into

```
numbers1
```

______________________________________________________________________

## Dry Run

```
A

1 4
```

```
B

2 3
```

Merged

```
1

2

3

4
```

Done.

______________________________________________________________________

## Complexity

Time

```
O(m+n)
```

Space

```
O(m+n)
```

______________________________________________________________________

## Limitations

Extra array required.

Can we use the empty space already available?

Yes.

______________________________________________________________________

# Optimized Solution

## Key Insight

The extra space is already at the end.

Example

```
1 2 3 _ _ _
```

If we start filling from the front,

we overwrite useful values.

Instead,

fill from the end.

______________________________________________________________________

# Understanding the Three Pointers

We'll use:

```
Pointer A

↓

Last valid element in numbers1
```

```
Pointer B

↓

Last element in numbers2
```

```
Write Pointer

↓

Last position of numbers1
```

______________________________________________________________________

Initially

```
numbers1

1 2 3 _ _ _
```

```
numbers2

2 5 6
```

Pointers

```
      A

      3
```

```
      B

      6
```

```
          W
```

______________________________________________________________________

Compare

```
3

6
```

Larger

```
6
```

Place it at

```
W
```

Result

```
1 2 3 _ _ 6
```

Move

```
B

↓

Left
```

Move

```
W

↓

Left
```

______________________________________________________________________

Compare

```
3

5
```

Place

```
5
```

```
1 2 3 _ 5 6
```

Continue.

______________________________________________________________________

# Step-by-Step Dry Run

Input

```
numbers1

1 2 3 0 0 0
```

```
numbers2

2 5 6
```

______________________________________________________________________

Step 1

Compare

```
3

6
```

↓

```
1 2 3 0 0 6
```

______________________________________________________________________

Step 2

Compare

```
3

5
```

↓

```
1 2 3 0 5 6
```

______________________________________________________________________

Step 3

Compare

```
3

2
```

↓

```
1 2 3 3 5 6
```

______________________________________________________________________

Step 4

Compare

```
2

2
```

Choose either.

↓

```
1 2 2 3 5 6
```

Done.

______________________________________________________________________

# Visual Explanation

Initial

```
1 2 3 _ _ _

      A

          W
```

```
2 5 6

    B
```

↓

Move largest

↓

```
1 2 3 _ _ 6
```

↓

```
1 2 3 _ 5 6
```

↓

```
1 2 3 3 5 6
```

↓

```
1 2 2 3 5 6
```

Finished.

______________________________________________________________________

# Why Start From the End?

Suppose we started here.

```
1 2 3 _ _ _
```

Insert

```
2
```

Now

```
3
```

must move.

Then

```
5
```

must move.

Repeated shifting becomes expensive.

Starting from the end avoids overwriting existing values.

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before each iteration, every position after the write pointer already contains its correct final value.

Each iteration places the largest remaining value.

Once placed,

that position never changes again.

Eventually,

every element reaches its correct position.

______________________________________________________________________

# Edge Cases

### numbers2 Empty

```
numbers2 = []
```

Nothing to merge.

______________________________________________________________________

### numbers1 Empty

```
numbers1

0 0 0
```

Simply copy

```
numbers2
```

______________________________________________________________________

### Duplicate Values

```
1 2 2

2 2 3
```

Works correctly.

______________________________________________________________________

### Negative Numbers

Works naturally.

______________________________________________________________________

### One Array Larger

Still works.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(m+n)
```

Space

```
O(m+n)
```

______________________________________________________________________

## Optimized

Time

```
O(m+n)
```

Space

```
O(1)
```

Only three pointers are used.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def merge(
    numbers1: List[int],
    m: int,
    numbers2: List[int],
    n: int,
) -> None:
    merged = []

    first = 0
    second = 0

    while first < m and second < n:
        if numbers1[first] <= numbers2[second]:
            merged.append(numbers1[first])
            first += 1
        else:
            merged.append(numbers2[second])
            second += 1

    merged.extend(numbers1[first:m])
    merged.extend(numbers2[second:n])

    numbers1[:] = merged
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List


def merge(
    numbers1: List[int],
    m: int,
    numbers2: List[int],
    n: int,
) -> None:
    first = m - 1
    second = n - 1
    write = m + n - 1

    while first >= 0 and second >= 0:
        if numbers1[first] > numbers2[second]:
            numbers1[write] = numbers1[first]
            first -= 1
        else:
            numbers1[write] = numbers2[second]
            second -= 1

        write -= 1

    while second >= 0:
        numbers1[write] = numbers2[second]
        second -= 1
        write -= 1


if __name__ == "__main__":
    values1 = [1, 2, 3, 0, 0, 0]
    values2 = [2, 5, 6]

    merge(values1, 3, values2, 3)

    print(values1)
```

______________________________________________________________________

# Why Don't We Copy Remaining Elements from numbers1?

This is one of the most common interview questions.

Suppose

```
numbers1

1 2 3
```

```
numbers2

5 6
```

After placing

```
6

5
```

the remaining

```
1 2 3
```

are **already in the correct position**.

Nothing needs to be done.

Only leftover elements from

```
numbers2
```

must be copied.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Starting from the front.

This overwrites values.

______________________________________________________________________

## Mistake 2

Forgetting to copy remaining elements from

```
numbers2
```

______________________________________________________________________

## Mistake 3

Trying to copy remaining elements from

```
numbers1
```

They are already correctly placed.

______________________________________________________________________

## Mistake 4

Using only two pointers.

A third pointer is required for writing.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A straightforward solution merges both arrays into a new array and copies the result back, but that uses extra space. Since `numbers1` already has enough space at the end, I can merge from the back using three pointers. At each step, I place the larger of the two current elements into the last available position. This avoids overwriting values and achieves O(1) extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why merge from the end?**

Because the empty positions are already there.

No existing values are overwritten.

______________________________________________________________________

**Q. Why only copy remaining elements from `numbers2`?**

Remaining elements in `numbers1` are already in their correct positions.

______________________________________________________________________

**Q. How many pointers are needed?**

Three:

- Last element of `numbers1`
- Last element of `numbers2`
- Write position

______________________________________________________________________

**Q. Where is this used in backend engineering?**

- Merge Sort
- Database compaction
- External sorting
- Storage engines
- Log merging

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Two Pointers (Backward) |
| Recognition | Merge Sorted Arrays In-place |
| Brute Force | Extra Array |
| Optimized | Three Backward Pointers |
| Time | O(m+n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Don't merge from the front.
- Use three pointers.
- Always compare the largest remaining elements.
- Fill the array from the back.
- Copy remaining elements from `numbers2` only.
- Time complexity is O(m+n).
- Space complexity is O(1).
- This is one of the most important in-place merging techniques.

______________________________________________________________________

# Practice Questions

## Easy

1. Merge Two Sorted Lists
1. Squares of a Sorted Array
1. Sorted Merge (Cracking the Coding Interview)

______________________________________________________________________

## Medium

4. Merge Intervals
1. Insert Interval
1. Sort Colors
1. Kth Smallest Element in a Sorted Matrix

______________________________________________________________________

## Hard (Optional)

8. Median of Two Sorted Arrays
1. Merge k Sorted Lists
1. Count of Smaller Numbers After Self

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning the **Backward Two Pointer** pattern. Whenever you need to merge sorted
data **in-place** and extra space already exists at the end, start filling from the back instead of the front. This
avoids unnecessary shifting and is a technique widely used in storage engines, merge sort, and database systems.

______________________________________________________________________

# Next

[25-3sum.md](25-3sum.md)
