# 41-quick-sort.md

# Quick Sort

> **🎯 Quick Sort is one of the fastest sorting algorithms used in practice.**
>
> Although Merge Sort guarantees **O(n log n)**, Quick Sort is often **faster in the real world** because:
>
> - It has excellent cache locality.
> - It sorts **in-place**.
> - It requires very little extra memory.
>
> Understanding Quick Sort is essential for interviews because it teaches **partitioning**, a technique that appears in many advanced algorithms.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 35–45 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers use Quick Sort to evaluate whether you understand:

- Divide and Conquer
- Partitioning
- Recursion
- Pivot selection
- In-place algorithms
- Average vs Worst Case complexity

Quick Sort's partitioning idea is used in:

- Quick Select
- Top-K problems
- Database query optimization
- Distributed systems
- Search engines

______________________________________________________________________

# Problem Statement

Given an unsorted array,

sort it in ascending order using **Quick Sort**.

______________________________________________________________________

## Example

### Input

```text
[10, 7, 8, 9, 1, 5]
```

### Output

```text
[1, 5, 7, 8, 9, 10]
```

______________________________________________________________________

# Before Learning Quick Sort

Merge Sort says:

```
Split first

↓

Sort later
```

Quick Sort says:

```
Put one element in its correct position first

↓

Then sort both sides
```

This is the biggest conceptual difference.

______________________________________________________________________

# Simple English

Imagine arranging students by height.

Choose one student.

Everyone shorter stands to the left.

Everyone taller stands to the right.

That student's position is now fixed forever.

Repeat for both groups.

______________________________________________________________________

# Backend Engineering Analogy

Imagine distributing requests around a load balancer.

Choose one server as a reference.

Requests with lower latency go left.

Requests with higher latency go right.

Then repeat inside each group.

Exactly the partitioning process.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Divide and Conquer + Partitioning**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Pivot
- Partition
- Quick Select
- Kth Largest
- In-place sorting

Think

```
Quick Sort
```

______________________________________________________________________

# High-Level Idea

Choose

```
Pivot
```

↓

Partition

```text
Smaller | Pivot | Larger
```

↓

Recursively sort both halves.

______________________________________________________________________

# Step 1 — Choose a Pivot

Input

```text
10 7 8 9 1 5
```

Choose

```
Pivot = 5
```

______________________________________________________________________

# Step 2 — Partition

Rearrange the array so that:

```text
Smaller than 5

↓

Left
```

```text
Greater than 5

↓

Right
```

Possible result

```text
1 5 10 7 8 9
```

Notice

```
5
```

is now in its final sorted position.

It never moves again.

______________________________________________________________________

# Step 3 — Recursively Sort

Sort

Left

```text
1
```

Already sorted.

Sort

Right

```text
10 7 8 9
```

Repeat the same process.

______________________________________________________________________

# Visual Explanation

Initial

```text
10 7 8 9 1 5
```

↓

Pivot

```
5
```

↓

Partition

```text
1 | 5 | 10 7 8 9
```

↓

Choose Pivot

```
9
```

↓

Partition

```text
7 8 | 9 | 10
```

↓

Choose Pivot

```
8
```

↓

```text
7 | 8 | 10
```

↓

Final

```text
1 5 7 8 9 10
```

______________________________________________________________________

# Understanding Partitioning

Partitioning is the heart of Quick Sort.

One common approach is the **Lomuto Partition Scheme**.

Steps:

1. Choose the last element as the pivot.
1. Keep an index `i` for the position where the next smaller element should go.
1. Scan the array.
1. Whenever an element is smaller than the pivot, swap it with index `i`.
1. Finally, place the pivot in its correct position.

______________________________________________________________________

# Dry Run (Lomuto Partition)

Array

```text
10 7 8 9 1 5
```

Pivot

```
5
```

Initially

```
i = -1
```

Scan

```
10
```

Greater.

Nothing happens.

______________________________________________________________________

Scan

```
7
```

Greater.

______________________________________________________________________

Scan

```
8
```

Greater.

______________________________________________________________________

Scan

```
9
```

Greater.

______________________________________________________________________

Scan

```
1
```

Smaller.

Increment

```
i = 0
```

Swap

```text
1 7 8 9 10 5
```

______________________________________________________________________

Finished scanning.

Swap Pivot

```text
1 5 8 9 10 7
```

Pivot index

```
1
```

Done.

______________________________________________________________________

# Why Does Partition Work?

After partitioning,

everything

Left

```
< Pivot
```

Everything

Right

```
> Pivot
```

Therefore,

the pivot is already in its final sorted position.

Only the left and right partitions remain unsorted.

______________________________________________________________________

# Recursive Tree

Example

```text
10 7 8 9 1 5
```

↓

```text
1

5

10 7 8 9
```

↓

```text
7 8

9

10
```

↓

Continue until every partition has one element.

______________________________________________________________________

# Why This Works

Loop Invariant (Partition):

> Before processing each element:
>
> - Elements before index `i` are smaller than the pivot.
> - Elements between `i+1` and the current index are greater than or equal to the pivot.
> - Elements after the current index are not yet processed.

At the end,

swapping the pivot into position guarantees:

```text
Left < Pivot < Right
```

______________________________________________________________________

# Pivot Selection Matters

Suppose

```text
1 2 3 4 5
```

Always choosing the last element gives

```
Pivot = 5
```

Left

```
1 2 3 4
```

Right

```
Empty
```

Very unbalanced.

Recursion depth

```
n
```

Worst case

```
O(n²)
```

______________________________________________________________________

Better Pivot Choices

- Random Pivot
- Median-of-Three
- Middle Element

These reduce the chance of worst-case partitions.

______________________________________________________________________

# Why Is Quick Sort Usually Faster Than Merge Sort?

Both average

```
O(n log n)
```

But Quick Sort:

- Works in-place.
- Doesn't create temporary arrays.
- Accesses memory sequentially (better CPU cache usage).

In practice,

it is often faster for arrays.

______________________________________________________________________

# Edge Cases

### Empty Array

Already sorted.

______________________________________________________________________

### One Element

Already sorted.

______________________________________________________________________

### Duplicate Values

Works,

but standard Quick Sort is **not stable**.

______________________________________________________________________

### Already Sorted

Worst case if pivot selection is poor.

______________________________________________________________________

### Reverse Sorted

Also worst case with poor pivot choice.

______________________________________________________________________

# Complexity Analysis

## Best Case

Balanced partitions.

Time

```
O(n log n)
```

______________________________________________________________________

## Average Case

Random data.

Time

```
O(n log n)
```

______________________________________________________________________

## Worst Case

Highly unbalanced partitions.

Time

```
O(n²)
```

______________________________________________________________________

## Space

Recursion stack.

Average

```
O(log n)
```

Worst

```
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def quick_sort(numbers: List[int]) -> None:
    def partition(left: int, right: int) -> int:
        pivot = numbers[right]
        smaller = left - 1

        for current in range(left, right):
            if numbers[current] <= pivot:
                smaller += 1
                numbers[smaller], numbers[current] = (
                    numbers[current],
                    numbers[smaller],
                )

        numbers[smaller + 1], numbers[right] = (
            numbers[right],
            numbers[smaller + 1],
        )

        return smaller + 1

    def sort(left: int, right: int) -> None:
        if left >= right:
            return

        pivot_index = partition(left, right)

        sort(left, pivot_index - 1)
        sort(pivot_index + 1, right)

    sort(0, len(numbers) - 1)


if __name__ == "__main__":
    values = [10, 7, 8, 9, 1, 5]

    quick_sort(values)

    print(values)
```

______________________________________________________________________

# Hoare vs Lomuto Partition

There are two famous partition schemes.

### Lomuto

- Easier to understand
- Easier to code
- More swaps

### Hoare

- Fewer swaps
- Faster in practice
- Slightly harder to implement

For interviews,

Lomuto is perfectly acceptable unless the interviewer asks otherwise.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Forgetting that the pivot must end in its correct position.

______________________________________________________________________

## Mistake 2

Recursing on the pivot again.

Correct recursion:

```python
left ... pivot - 1
```

and

```python
pivot + 1 ... right
```

______________________________________________________________________

## Mistake 3

Choosing a poor pivot repeatedly.

This causes O(n²) performance.

______________________________________________________________________

## Mistake 4

Thinking Quick Sort is stable.

Equal elements may change their relative order.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Quick Sort chooses a pivot, partitions the array so that smaller elements are on the left and larger elements are on the right, then recursively sorts both partitions. After partitioning, the pivot is already in its final position. Although the worst case is O(n²), the average case is O(n log n), and its in-place nature makes it very fast in practice."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why is Quick Sort often faster than Merge Sort?**

Because it sorts in-place and has excellent cache locality.

______________________________________________________________________

**Q. Why is the worst case O(n²)?**

Poor pivot selection creates highly unbalanced partitions.

______________________________________________________________________

**Q. Is Quick Sort stable?**

No.

Equal elements may change order.

______________________________________________________________________

**Q. Where is partitioning used besides sorting?**

- Quick Select
- Top-K elements
- Median finding
- Database optimizers

______________________________________________________________________

# Merge Sort vs Quick Sort

| Feature | Merge Sort | Quick Sort |
|----------|------------|------------|
| Stable | ✅ Yes | ❌ No |
| In-Place | ❌ No | ✅ Yes |
| Worst Case | O(n log n) | O(n²) |
| Average | O(n log n) | O(n log n) |
| Extra Space | O(n) | O(log n) |
| Cache Friendly | ❌ Less | ✅ More |

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Divide & Conquer + Partition |
| Recognition | Pivot-Based Sorting |
| Stable | No |
| In-Place | Yes |
| Best Time | O(n log n) |
| Average Time | O(n log n) |
| Worst Time | O(n²) |
| Space | O(log n) average |

______________________________________________________________________

# Quick Revision

- Choose a pivot.
- Partition the array.
- Pivot reaches its final position.
- Recursively sort left and right partitions.
- Average complexity is O(n log n).
- Worst case is O(n²).
- In-place sorting algorithm.
- Often faster than Merge Sort in practice.

______________________________________________________________________

# Practice Questions

## Easy

1. Sort an Array
1. Kth Largest Element in an Array
1. Sort Colors

______________________________________________________________________

## Medium

4. Quick Select
1. Top K Frequent Elements
1. Wiggle Sort II
1. K Closest Points to Origin

______________________________________________________________________

## Hard (Optional)

8. Median of Medians
1. Merge k Sorted Arrays
1. External Sorting Strategy Comparison

______________________________________________________________________

# Key Takeaway

The biggest lesson from Quick Sort is the power of **partitioning**. Instead of completely sorting first, Quick Sort
ensures that **one element (the pivot) reaches its final position immediately**, reducing the problem into two smaller
independent subproblems. This partitioning idea extends far beyond sorting and is widely used in selection algorithms,
databases, and large-scale distributed systems.

______________________________________________________________________

# Next

[42-binary-tree-traversals.md](42-binary-tree-traversals.md)
