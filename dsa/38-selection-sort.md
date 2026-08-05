# 38-selection-sort.md

# Selection Sort

> **🎯 Selection Sort teaches an important engineering mindset:**
>
> Instead of repeatedly swapping elements like Bubble Sort,
> **find the best candidate first, then perform only one swap.**
>
> While Selection Sort is rarely used in production, it introduces the concept of **selection**, which appears in many advanced algorithms.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐☆☆ Medium |
| Importance | ⭐⭐⭐⭐☆ |
| Expected Interview Time | 15–20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers use Selection Sort to evaluate whether you understand:

- Sorting fundamentals
- Finding minimum/maximum values
- Nested loops
- In-place sorting
- Trade-offs between comparisons and swaps

It also prepares you for:

- Heap Sort
- Priority Queues
- Greedy algorithms
- Selection algorithms (Quick Select)

______________________________________________________________________

# Problem Statement

Given an array,

sort it in ascending order using **Selection Sort**.

______________________________________________________________________

## Example

### Input

```text
[64, 25, 12, 22, 11]
```

### Output

```text
[11, 12, 22, 25, 64]
```

______________________________________________________________________

# Before Learning Selection Sort

Suppose we have

```text
64 25 12 22 11
```

Instead of swapping repeatedly,

ask one question:

> **What is the smallest number in the unsorted part?**

Answer

```
11
```

Swap it with the first element.

Done.

Repeat for the remaining unsorted portion.

______________________________________________________________________

# Simple English

Imagine arranging books by height.

Instead of moving books one by one,

you first find the **shortest book**,

place it in the first position,

then repeat for the remaining books.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a scheduler assigning jobs.

Instead of constantly rearranging jobs,

it first chooses:

- Highest priority job
- Smallest execution time
- Earliest deadline

Then schedules it.

This is exactly a **selection** strategy.

The same concept appears in:

- CPU scheduling
- Task prioritization
- Greedy algorithms
- Heap-based scheduling

______________________________________________________________________

# Pattern Recognition

## Pattern

**Repeated Selection**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Find smallest
- Find largest
- Select minimum
- Place in correct position

Think

```
Selection Sort
```

______________________________________________________________________

# Bubble Sort vs Selection Sort

Bubble Sort

```
Compare neighbors

↓

Many swaps
```

Selection Sort

```
Find minimum

↓

One swap
```

______________________________________________________________________

# Brute Force Idea

Selection Sort itself is already the straightforward algorithm.

The learning focus is understanding its process.

______________________________________________________________________

# Key Insight

At every iteration,

the left portion becomes sorted.

The right portion remains unsorted.

Repeatedly:

1. Find smallest value.
1. Swap once.

______________________________________________________________________

# Step-by-Step Dry Run

Input

```text
64 25 12 22 11
```

______________________________________________________________________

## Pass 1

Current minimum

```
64
```

Compare

```
25
```

Smaller.

New minimum.

______________________________________________________________________

Compare

```
12
```

Smaller.

______________________________________________________________________

Compare

```
22
```

Ignore.

______________________________________________________________________

Compare

```
11
```

Smallest.

Swap

```text
11 25 12 22 64
```

Notice

```
11
```

is permanently fixed.

______________________________________________________________________

## Pass 2

Remaining

```text
25 12 22 64
```

Smallest

```
12
```

Swap

```text
11 12 25 22 64
```

______________________________________________________________________

## Pass 3

Remaining

```text
25 22 64
```

Smallest

```
22
```

Swap

```text
11 12 22 25 64
```

______________________________________________________________________

Sorted.

______________________________________________________________________

# Visual Explanation

Initial

```text
64 25 12 22 11
```

↓

Find Minimum

```
11
```

↓

```text
11 25 12 22 64
```

↓

Find Minimum

```
12
```

↓

```text
11 12 25 22 64
```

↓

Find Minimum

```
22
```

↓

```text
11 12 22 25 64
```

↓

Done.

______________________________________________________________________

# Why Does It Work?

After every pass,

one element reaches its **final correct position**.

Unlike Bubble Sort,

Selection Sort doesn't care about local order.

It only cares about placing the correct minimum.

______________________________________________________________________

# Loop Invariant

> Before each iteration:
>
> The left portion of the array is already sorted.
>
> Every element in the left portion is smaller than every element in the right portion.

Each iteration extends the sorted region by one element.

______________________________________________________________________

# Bubble Sort vs Selection Sort

| Bubble Sort | Selection Sort |
|-------------|----------------|
| Many swaps | One swap per pass |
| Adjacent comparisons | Scan entire unsorted region |
| Stable | Not Stable |
| Can stop early | Always scans entire array |

______________________________________________________________________

# Why Is Selection Sort Not Stable?

Consider

```text
2A 2B 1
```

After selecting

```
1
```

Swap

```text
1 2B 2A
```

The relative order of

```
2A

2B
```

changed.

Therefore,

Selection Sort is **not stable**.

______________________________________________________________________

# Edge Cases

### Empty Array

Already sorted.

______________________________________________________________________

### One Element

Already sorted.

______________________________________________________________________

### Already Sorted

Selection Sort still scans the entire array.

No early exit.

______________________________________________________________________

### Reverse Sorted

Works correctly.

______________________________________________________________________

### Duplicate Values

Correct,

but relative order may change.

______________________________________________________________________

# Complexity Analysis

Selection Sort always performs the same number of comparisons.

Unlike Bubble Sort,

its performance does **not** improve for already sorted arrays.

______________________________________________________________________

Time

Best

```
O(n²)
```

Average

```
O(n²)
```

Worst

```
O(n²)
```

Space

```
O(1)
```

______________________________________________________________________

# Number of Comparisons

Suppose

```
n = 5
```

Comparisons

```
4

+

3

+

2

+

1

=

10
```

General formula

```
n(n-1)/2
```

Therefore,

```
O(n²)
```

______________________________________________________________________

# Number of Swaps

One swap per pass.

Maximum

```
n - 1
```

This is much fewer than Bubble Sort.

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def selection_sort(numbers: List[int]) -> None:
    length = len(numbers)

    for start in range(length - 1):
        minimum_index = start

        for current in range(start + 1, length):
            if numbers[current] < numbers[minimum_index]:
                minimum_index = current

        numbers[start], numbers[minimum_index] = (
            numbers[minimum_index],
            numbers[start],
        )


if __name__ == "__main__":
    values = [64, 25, 12, 22, 11]

    selection_sort(values)

    print(values)
```

______________________________________________________________________

# Optimization

Many beginners ask:

Can Selection Sort stop early?

Unfortunately,

No.

Even if the array appears sorted,

you still must verify that the current element is truly the smallest.

Therefore,

Selection Sort always performs

```
O(n²)
```

comparisons.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Swapping immediately after finding a smaller element.

Wrong.

First finish scanning.

Then swap once.

______________________________________________________________________

## Mistake 2

Forgetting to update the minimum index.

The smallest value changes during scanning.

______________________________________________________________________

## Mistake 3

Thinking Selection Sort is stable.

It is **not**.

______________________________________________________________________

## Mistake 4

Expecting best-case O(n).

Selection Sort always scans the unsorted region.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Selection Sort repeatedly finds the smallest element in the unsorted portion of the array and places it in its correct position. Unlike Bubble Sort, which performs many swaps, Selection Sort performs only one swap per pass. Although it always requires O(n²) comparisons, it minimizes the number of swaps."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why does Selection Sort perform fewer swaps than Bubble Sort?**

Because it swaps only after identifying the minimum element.

______________________________________________________________________

**Q. Is Selection Sort stable?**

No.

Swapping can change the relative order of equal elements.

______________________________________________________________________

**Q. Can Selection Sort stop early?**

No.

Every pass must scan the remaining unsorted elements.

______________________________________________________________________

**Q. Where is the idea of selection used?**

- Greedy algorithms
- Priority queues
- Scheduling
- Quick Select
- Heap algorithms

______________________________________________________________________

# Bubble Sort vs Selection Sort vs Insertion Sort

| Feature | Bubble | Selection | Insertion |
|----------|---------|-----------|-----------|
| Stable | ✅ Yes | ❌ No | ✅ Yes |
| Adaptive | ✅ Yes | ❌ No | ✅ Yes |
| Swaps | Many | Few | Few shifts |
| Best Case | O(n) | O(n²) | O(n) |
| Average | O(n²) | O(n²) | O(n²) |

Notice

Insertion Sort often performs better on nearly sorted data,

which we'll study next.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Repeated Selection |
| Recognition | Find Minimum, Place First |
| Stable | No |
| In-Place | Yes |
| Best Time | O(n²) |
| Average Time | O(n²) |
| Worst Time | O(n²) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Find the smallest element.
- Swap once per pass.
- The sorted region grows from left to right.
- Performs fewer swaps than Bubble Sort.
- Always scans the remaining unsorted region.
- Not stable.
- Time complexity is O(n²).
- Useful for understanding selection-based algorithms.

______________________________________________________________________

# Practice Questions

## Easy

1. Minimum Absolute Difference
1. Array Partition
1. Sort Array By Increasing Frequency

______________________________________________________________________

## Medium

4. Kth Largest Element in an Array
1. Top K Frequent Elements
1. Sort Colors
1. Find K Closest Elements

______________________________________________________________________

## Hard (Optional)

8. Median of Medians
1. External Sorting
1. Kth Smallest Element in a Sorted Matrix

______________________________________________________________________

# Key Takeaway

The biggest lesson from Selection Sort is that **choosing the best candidate before acting** can reduce unnecessary
work. While Selection Sort isn't efficient for large datasets, the idea of **repeatedly selecting the optimal element**
is a powerful concept that appears in greedy algorithms, scheduling, heaps, and many real-world systems.

______________________________________________________________________

# Next

[39-insertion-sort.md](39-insertion-sort.md)
