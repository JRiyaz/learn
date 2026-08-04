# 25-largest-rectangle-in-histogram.md

# Largest Rectangle in Histogram — The Monotonic Increasing Stack Pattern

## Interview Confidence

**Difficulty:** ⭐⭐⭐⭐☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 30–35 minutes

**Revision Time:** 10 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

You are given an array `heights`.

Each value represents the height of a histogram bar.

Every bar has width **1**.

Find the **largest rectangle** that can be formed.

______________________________________________________________________

### Example

```text
Input

[2,1,5,6,2,3]
```

Output

```text
10
```

Rectangle

```text
5 × 2

=

10
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> For every bar,

what is the **widest rectangle** where this bar is the shortest bar?

This question is the key insight.

______________________________________________________________________

# Real-World Analogy

Imagine buildings.

```text
Height

2

1

5

6

2

3
```

Suppose you want the biggest billboard that can fit between buildings.

The billboard height is limited by the shortest building.

Exactly the same problem.

Other examples:

- Skyline analysis
- Warehouse storage
- Resource allocation
- Memory utilization

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Histogram
- Largest rectangle
- Previous smaller
- Next smaller

Think immediately:

```text
Monotonic Increasing Stack
```

______________________________________________________________________

# Brute Force Solution

For every bar:

Expand left.

Expand right.

Until a shorter bar appears.

Example

```text
Height

5
```

Expand

```text
←

5

6

→
```

Area

```text
5 × Width
```

Repeat for every bar.

______________________________________________________________________

## Complexity

Time

```text
O(n²)
```

Too slow.

______________________________________________________________________

# Key Insight

Instead of expanding every bar repeatedly,

determine the exact moment when a bar can no longer grow.

That moment occurs when we encounter a **smaller bar**.

______________________________________________________________________

# Why a Monotonic Increasing Stack?

Maintain bars in increasing order.

Example

```text
1

2

5

6
```

Everything is increasing.

Nothing to calculate yet.

Then

```text
2
```

appears.

Now

```text
6

>

2
```

The bar of height

```text
6
```

cannot extend further.

Its maximum rectangle is now known.

Compute it immediately.

______________________________________________________________________

# Visual Explanation

Input

```text
2 1 5 6 2 3
```

Stack

```text
2
```

Read

```text
1
```

Smaller.

Pop

```text
2
```

Compute rectangle.

Push

```text
1
```

Continue.

______________________________________________________________________

Read

```text
5
```

Increasing.

Push.

______________________________________________________________________

Read

```text
6
```

Increasing.

Push.

______________________________________________________________________

Read

```text
2
```

Smaller.

Resolve

```text
6
```

Then

```text
5
```

Compute both rectangles.

Push

```text
2
```

______________________________________________________________________

# Width Calculation

This is the hardest part.

Suppose

```text
2 1 5 6 2
```

Pop

```text
6
```

Current index

```text
4
```

Previous smaller

```text
Index 2
```

Rectangle width

```text
Current Index

-

Previous Smaller

-

1
```

Formula

```text
Width

=

right

-

left

-

1
```

where

- `right` is the current index.
- `left` is the new top of the stack after popping.

______________________________________________________________________

# Step-by-Step Algorithm

Create empty stack.

Traverse bars.

If current height is smaller:

Keep popping.

For every popped bar:

Compute width.

Compute area.

Update maximum.

Push current index.

After traversal,

pop remaining bars.

______________________________________________________________________

# Why This Works

Every bar enters the stack once.

Leaves once.

The first smaller bar on the right tells us:

> The rectangle cannot extend further.

The previous smaller bar on the left tells us:

> The rectangle cannot extend backward.

Together,

they define the maximum possible width.

______________________________________________________________________

# Dry Run

Input

```text
2 1 2
```

Stack

```text
2
```

Read

```text
1
```

Pop

```text
2
```

Area

```text
2 × 1 = 2
```

Push

```text
1
```

Read

```text
2
```

Push.

End.

Resolve remaining bars.

Maximum

```text
3
```

______________________________________________________________________

# Edge Cases

## One Bar

```text
5
```

Answer

```text
5
```

______________________________________________________________________

## Increasing Heights

```text
1 2 3 4
```

Need final cleanup after traversal.

______________________________________________________________________

## Decreasing Heights

```text
4 3 2 1
```

Frequent popping.

Still

```text
O(n)
```

______________________________________________________________________

## Equal Heights

Treat them consistently.

Using `>=` while popping avoids duplicate width calculations.

______________________________________________________________________

# Complexity Analysis

## Time

Every index:

- pushed once
- popped once

Overall

```text
O(n)
```

______________________________________________________________________

## Space

Worst case

Increasing heights.

```text
O(n)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def largest_rectangle_area(heights: List[int]) -> int:
    """
    Returns the largest rectangle area
    in a histogram.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    stack: List[int] = []
    maximum_area = 0

    extended = heights + [0]

    for index, height in enumerate(extended):
        while stack and extended[stack[-1]] > height:
            top = stack.pop()
            current_height = extended[top]

            if stack:
                width = index - stack[-1] - 1
            else:
                width = index

            maximum_area = max(
                maximum_area,
                current_height * width,
            )

        stack.append(index)

    return maximum_area
```

______________________________________________________________________

# Why Add a Sentinel `0`?

Without it,

bars remaining in the stack after traversal must be processed separately.

Appending

```text
0
```

forces every remaining bar to be popped naturally.

This simplifies the implementation.

______________________________________________________________________

# Common Mistakes

## 1. Forgetting Width Formula

Remember

```text
Width

=

right

-

left

-

1
```

______________________________________________________________________

## 2. Forgetting Final Cleanup

Either:

- append a sentinel `0`, or
- process the remaining stack after the loop.

______________________________________________________________________

## 3. Storing Heights Instead of Indices

Need indices to compute widths.

______________________________________________________________________

## 4. Using `if` Instead of `while`

One smaller bar may resolve multiple previous bars.

Always use

```python
while
```

______________________________________________________________________

# Variations

## Medium

- Maximal Rectangle
- Daily Temperatures
- Online Stock Span

______________________________________________________________________

## Hard

- Trapping Rain Water
- Sum of Subarray Minimums

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Mention brute force.
1. Observe repeated expansion.
1. Introduce Monotonic Increasing Stack.
1. Explain previous smaller and next smaller.
1. Derive width formula.
1. Analyze O(n).

______________________________________________________________________

### Common Follow-ups

### Q: Why an increasing stack?

A smaller incoming bar tells us taller bars can no longer extend.

______________________________________________________________________

### Q: Why store indices?

Widths depend on positions, not just heights.

______________________________________________________________________

### Q: Why append `0`?

To flush the remaining bars automatically.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Monotonic Increasing Stack |
| Recognition | Histogram, largest rectangle |
| Store | Indices |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Practice Problems

## Medium

1. Daily Temperatures
1. Online Stock Span
1. Maximal Rectangle
1. Next Smaller Element

## Hard

1. Trapping Rain Water
1. Sum of Subarray Minimums

______________________________________________________________________

# Quick Revision

- Use a **Monotonic Increasing Stack**.
- Store indices.
- A smaller bar resolves previous taller bars.
- Width = `right - left - 1`.
- Append a sentinel `0` for cleanup.
- Time: **O(n)**
- Space: **O(n)**

______________________________________________________________________

# Key Takeaway

This is one of the most challenging Stack interview problems because it combines:

- Monotonic Stack
- Previous Smaller Element
- Next Smaller Element
- Geometry (area calculation)

The crucial insight is:

> **A bar's maximum rectangle is known exactly when a shorter bar appears.**

That observation transforms an **O(n²)** solution into an elegant **O(n)** algorithm.

______________________________________________________________________

# Navigation

**Previous**

[24-evaluate-reverse-polish-notation.md](24-evaluate-reverse-polish-notation.md)

**Next**

[26-queue.md](26-queue.md)
