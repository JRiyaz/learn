# 40-merge-sort.md

# Merge Sort

> **🎯 This is the first "real" production-grade sorting algorithm in your DSA journey.**
>
> Unlike Bubble Sort, Selection Sort, and Insertion Sort,
> **Merge Sort guarantees O(n log n) performance**, regardless of the input.
>
> It is one of the best examples of the **Divide and Conquer** paradigm and forms the foundation of many production systems.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 30–40 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers use Merge Sort to evaluate whether you understand:

- Divide and Conquer
- Recursion
- Recursive trees
- Merging sorted data
- Algorithm analysis
- Stable sorting

Merge Sort is widely used in:

- External sorting
- Database systems
- Distributed systems
- Search engines
- Hadoop/Spark
- Log processing
- File merging

______________________________________________________________________

# Problem Statement

Given an unsorted array,

sort it in ascending order using **Merge Sort**.

______________________________________________________________________

## Example

### Input

```text
[38, 27, 43, 3, 9, 82, 10]
```

### Output

```text
[3, 9, 10, 27, 38, 43, 82]
```

______________________________________________________________________

# Before Learning Merge Sort

Suppose someone asks you to sort

```text
38 27 43 3 9 82 10
```

Sorting all seven numbers at once is difficult.

Instead,

split the problem into two smaller problems.

Sort each half.

Then combine them.

This strategy is called:

```
Divide

↓

Conquer

↓

Combine
```

______________________________________________________________________

# Simple English

Imagine sorting a deck of cards.

Instead of sorting all 52 cards together,

split them into two smaller piles.

Sort each pile.

Merge the two sorted piles.

______________________________________________________________________

# Backend Engineering Analogy

Imagine two database shards.

```
Shard A

Sorted Records
```

```
Shard B

Sorted Records
```

To create one global result,

merge the two sorted streams.

This is exactly how:

- External Merge Sort
- Big Data frameworks
- Database query engines

work.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Divide and Conquer**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Divide into halves
- Recursive sorting
- Merge
- Stable sorting
- External sorting

Think

```
Merge Sort
```

______________________________________________________________________

# High-Level Idea

```
Split

↓

Split Again

↓

Split Again

↓

Single Elements

↓

Merge

↓

Merge Again

↓

Sorted Array
```

______________________________________________________________________

# Step 1 — Divide

Input

```text
38 27 43 3 9 82 10
```

Split

```text
38 27 43

3 9 82 10
```

Split again

```text
38

27 43

3 9

82 10
```

Eventually

```text
38

27

43

3

9

82

10
```

Single elements are already sorted.

______________________________________________________________________

# Step 2 — Merge

Merge

```
27

43
```

↓

```text
27 43
```

Merge

```
38

27 43
```

↓

```text
27 38 43
```

Repeat until everything is merged.

______________________________________________________________________

# Visual Explanation

```
38 27 43 3 9 82 10
```

↓

```
38 27 43

3 9 82 10
```

↓

```
38

27 43

3 9

82 10
```

↓

```
38

27

43

3

9

82

10
```

↓

Merge

↓

```
27 38 43

3 9 10 82
```

↓

Final

```text
3 9 10 27 38 43 82
```

______________________________________________________________________

# Why Is Merging Easy?

Suppose

```text
Left

2 5 8
```

```text
Right

1 3 9
```

Both halves are already sorted.

Compare only the first elements.

```
2

1
```

Take

```
1
```

Next

```
2

3
```

Take

```
2
```

Continue until both lists finish.

______________________________________________________________________

# Dry Run of Merge

Left

```text
2 5 8
```

Right

```text
1 3 9
```

Merged

```
1
```

↓

```
1 2
```

↓

```
1 2 3
```

↓

```
1 2 3 5
```

↓

```
1 2 3 5 8
```

↓

```
1 2 3 5 8 9
```

Done.

______________________________________________________________________

# Recursive View

Merge Sort repeatedly performs:

```text
merge_sort(array)

↓

merge_sort(left)

↓

merge_sort(right)

↓

merge(left, right)
```

Each recursive call solves a smaller version of the same problem.

______________________________________________________________________

# Why This Works

Loop Invariant (Merge Step):

> Before each comparison,
> the merged array already contains the smallest elements in sorted order.

Each comparison chooses the smallest remaining element from the two sorted halves.

Since both halves are sorted,

the merged output also remains sorted.

______________________________________________________________________

# Recursion Tree

For

```
8
```

elements

```text
Level 0

8
```

↓

```text
Level 1

4

4
```

↓

```text
Level 2

2

2

2

2
```

↓

```text
Level 3

1

1

1

1

1

1

1

1
```

Height

```
log₂ n
```

At each level,

every element is processed exactly once.

Total

```
n × log n
```

______________________________________________________________________

# Why Is Merge Sort O(n log n)?

Many candidates memorize this.

Let's derive it.

There are

```
log₂ n
```

levels.

At every level,

every element participates in exactly one merge.

Work per level

```
O(n)
```

Levels

```
O(log n)
```

Therefore

```
O(n log n)
```

______________________________________________________________________

# Edge Cases

### Empty Array

Already sorted.

______________________________________________________________________

### One Element

Already sorted.

______________________________________________________________________

### Duplicate Values

Handled correctly.

Merge Sort is **stable**.

______________________________________________________________________

### Reverse Sorted

Still

```
O(n log n)
```

______________________________________________________________________

### Already Sorted

Still

```
O(n log n)
```

Unlike Insertion Sort,

Merge Sort doesn't improve for sorted input.

______________________________________________________________________

# Complexity Analysis

## Time

Best

```
O(n log n)
```

Average

```
O(n log n)
```

Worst

```
O(n log n)
```

Guaranteed.

______________________________________________________________________

## Space

Temporary arrays are used during merging.

```
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def merge_sort(numbers: List[int]) -> List[int]:
    if len(numbers) <= 1:
        return numbers

    middle = len(numbers) // 2

    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])

    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    merged: List[int] = []

    left_index = 0
    right_index = 0

    while (
        left_index < len(left)
        and right_index < len(right)
    ):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])

    return merged


if __name__ == "__main__":
    values = [38, 27, 43, 3, 9, 82, 10]

    print(merge_sort(values))
```

______________________________________________________________________

# In-Place Merge Sort?

Interviewers may ask:

> Can Merge Sort be done in-place?

Technically,

yes.

Practically,

it's extremely complicated.

Most production implementations use

```
O(n)
```

extra space.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Trying to merge unsorted halves.

Always sort recursively before merging.

______________________________________________________________________

## Mistake 2

Forgetting to append remaining elements.

After one list finishes,

the other may still contain elements.

______________________________________________________________________

## Mistake 3

Thinking Merge Sort is in-place.

Standard Merge Sort uses additional memory.

______________________________________________________________________

## Mistake 4

Thinking Merge Sort becomes O(n) for sorted input.

It still performs recursive splitting and merging.

______________________________________________________________________

# Merge Sort vs Insertion Sort

| Feature | Merge Sort | Insertion Sort |
|----------|------------|----------------|
| Stable | ✅ Yes | ✅ Yes |
| Adaptive | ❌ No | ✅ Yes |
| Best Case | O(n log n) | O(n) |
| Worst Case | O(n log n) | O(n²) |
| Extra Space | O(n) | O(1) |
| Production Use | Yes | Yes (Small Arrays) |

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "Sorting the entire array at once is difficult, so I'll divide it into two halves. I recursively sort each half, then merge the two sorted halves into one sorted array. Since every merge processes all elements once and there are log₂(n) levels of recursion, the overall time complexity is O(n log n)."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why is Merge Sort stable?**

Equal elements preserve their original order during merging.

______________________________________________________________________

**Q. Why does it require O(n) space?**

Because temporary arrays are created during the merge step.

______________________________________________________________________

**Q. Where is Merge Sort used?**

- External sorting
- Databases
- Hadoop
- Spark
- File systems
- Search engines

______________________________________________________________________

**Q. Why is Merge Sort preferred for linked lists?**

Merging linked lists is efficient because nodes can be relinked without shifting elements, avoiding the extra copying
required for arrays.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Divide and Conquer |
| Recognition | Split → Sort → Merge |
| Stable | Yes |
| Adaptive | No |
| In-Place | No |
| Best Time | O(n log n) |
| Average Time | O(n log n) |
| Worst Time | O(n log n) |
| Space | O(n) |

______________________________________________________________________

# Quick Revision

- Divide the array into halves.
- Recursively sort each half.
- Merge the sorted halves.
- Single-element arrays are already sorted.
- Merge Sort guarantees O(n log n).
- It is stable.
- It requires O(n) extra space.
- Widely used in production systems and external sorting.

______________________________________________________________________

# Practice Questions

## Easy

1. Merge Two Sorted Arrays
1. Merge Two Sorted Lists
1. Sort an Array

______________________________________________________________________

## Medium

4. Count Inversions
1. Sort Linked List
1. Merge Intervals
1. Kth Largest Element in an Array

______________________________________________________________________

## Hard (Optional)

8. Merge k Sorted Lists
1. Reverse Pairs
1. Count of Smaller Numbers After Self

______________________________________________________________________

# Key Takeaway

The biggest lesson from Merge Sort is the power of **Divide and Conquer**. By repeatedly breaking a difficult problem
into smaller, independent problems and combining their solutions, Merge Sort achieves a guaranteed **O(n log n)**
runtime. This strategy is fundamental not only in sorting but also in many algorithms used in distributed systems,
databases, and large-scale data processing.

______________________________________________________________________

# Next

[41-quick-sort.md](41-quick-sort.md)
