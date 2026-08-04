# 14-container-with-most-water.md

# Container With Most Water — The Greedy Two Pointer Pattern

## Interview Confidence

**Difficulty:** ⭐⭐⭐☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20–25 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

You are given an integer array `height`.

Each element represents the height of a vertical line.

Find two lines that together with the x-axis form a container capable of holding the maximum amount of water.

Return the maximum area.

### Example

```text
height = [1,8,6,2,5,4,8,3,7]

Output

49
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> Which two lines produce the largest rectangle?

The area is calculated as:

```text
Area = Width × Height
```

where:

```text
Width  = right - left

Height = min(left_height, right_height)
```

The shorter line limits the water level.

______________________________________________________________________

# Real-World Analogy

Imagine building two walls to store rainwater.

```text
Height

8         8

|         |

|         |

+---------+
```

The water level can never exceed the **shorter wall**.

This same principle appears in:

- Reservoir design
- Water storage systems
- Buffer capacity calculations
- Capacity planning

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Maximum area
- Two boundaries
- Width and height
- Sorted movement not required
- Constant space

Think:

> **Opposite Direction Two Pointers + Greedy Choice**

______________________________________________________________________

# Brute Force Solution

## Intuition

Try every possible pair.

```text
Choose line 1

↓

Pair with every other line

↓

Compute area

↓

Repeat
```

Example

```text
1 8 6 2

Compare

(1,8)

(1,6)

(1,2)

(8,6)

...
```

______________________________________________________________________

## Complexity

Time

```text
O(n²)
```

Space

```text
O(1)
```

Too slow.

______________________________________________________________________

# Optimal Solution

## Key Insight

Start with the widest container.

```text
1 8 6 2 5 4 8 3 7

↑               ↑
```

Maximum width.

Now ask:

> Which pointer should move?

______________________________________________________________________

### Important Observation

Area depends on

```text
min(height[left], height[right])
```

Suppose

```text
2           8

↑           ↑
```

The shorter wall is **2**.

Moving the taller wall:

```text
2       7

↑       ↑
```

Width decreases.

Shorter wall is still **2**.

Area **cannot improve**.

The only hope is finding a taller left wall.

Therefore:

> **Move the shorter pointer.**

______________________________________________________________________

# Why Moving the Taller Pointer Never Helps

Suppose

```text
Left = 3

Right = 10

Width = 8
```

Area

```text
3 × 8 = 24
```

Move the taller wall.

Width becomes

```text
7
```

Height is still limited by

```text
3
```

Maximum possible area

```text
3 × 7 = 21
```

Smaller.

So moving the taller wall cannot produce a better answer.

This is the greedy proof interviewers expect.

______________________________________________________________________

# Visual Explanation

```text
1 8 6 2 5 4 8 3 7

↑               ↑

Area

min(1,7) × 8

=

8
```

Move left.

```text
1 8 6 2 5 4 8 3 7

  ↑             ↑

Area

min(8,7) × 7

=

49
```

Best so far.

Now

Left wall is taller.

Move right.

Continue until pointers meet.

______________________________________________________________________

# Step-by-Step Algorithm

Initialize

```text
left = 0

right = n - 1

best = 0
```

While

```text
left < right
```

Calculate area.

Update best.

Move the shorter pointer.

Repeat.

______________________________________________________________________

# Dry Run

```text
1 2 4 3
```

Initial

```text
↑     ↑
```

Area

```text
1 × 3 = 3
```

Move left.

```text
  ↑   ↑
```

Area

```text
2 × 2 = 4
```

Move left.

```text
    ↑ ↑
```

Area

```text
3
```

Answer

```text
4
```

______________________________________________________________________

# Why This Works

Each iteration removes one impossible solution.

When the shorter wall moves,

there is a chance of finding a taller wall.

When the taller wall moves,

the width decreases while the limiting height does not improve.

Therefore,

the greedy decision is always safe.

______________________________________________________________________

# Edge Cases

## Two Elements

```text
[5,6]
```

Area

```text
5 × 1 = 5
```

______________________________________________________________________

## Equal Heights

```text
5 5
```

Move either pointer.

______________________________________________________________________

## Strictly Increasing

```text
1 2 3 4 5
```

Algorithm still works.

______________________________________________________________________

## Strictly Decreasing

```text
5 4 3 2 1
```

Still works.

______________________________________________________________________

## All Equal

```text
3 3 3 3
```

Best area uses the widest distance.

______________________________________________________________________

# Complexity Analysis

## Time

Each pointer moves at most

```text
n
```

times.

Overall

```text
O(n)
```

______________________________________________________________________

## Space

Only a few variables.

```text
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def max_area(height: List[int]) -> int:
    """
    Returns the maximum amount of water.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    left = 0
    right = len(height) - 1
    maximum_area = 0

    while left < right:
        width = right - left
        current_height = min(height[left], height[right])
        maximum_area = max(maximum_area, width * current_height)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return maximum_area
```

______________________________________________________________________

# Common Mistakes

## 1. Moving the Taller Pointer

Wrong.

The shorter wall limits the area.

______________________________________________________________________

## 2. Forgetting Width Changes

Every pointer movement decreases width.

Only move when there's a chance to increase height.

______________________________________________________________________

## 3. Comparing Areas Incorrectly

Remember

```text
Area

=

Width

×

Minimum Height
```

Not

```text
Maximum Height
```

______________________________________________________________________

## 4. Using Nested Loops

Correct.

But

```text
O(n²)
```

______________________________________________________________________

# Variations

## Medium

- Trapping Rain Water
- 3Sum
- Boats to Save People
- Max Number of K-Sum Pairs

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Mention brute force.
1. Explain O(n²).
1. Observe width always decreases.
1. Identify shorter wall as the limiting factor.
1. Justify moving only the shorter pointer.
1. Analyze complexity.

______________________________________________________________________

### Common Follow-ups

### Q: Why move the shorter wall?

Because only increasing the limiting height can compensate for losing width.

______________________________________________________________________

### Q: Why not move both pointers?

You might skip the optimal solution.

Only eliminate one impossible choice at a time.

______________________________________________________________________

### Q: Can sorting help?

No.

The positions determine the width.

Sorting destroys that information.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Greedy Two Pointers |
| Recognition | Max area, two boundaries |
| Brute Force | Compare every pair |
| Optimal | Two Pointers |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Practice Problems

## Easy

1. Merge Sorted Array
1. Squares of a Sorted Array

## Medium

1. Trapping Rain Water
1. Boats to Save People
1. Max Number of K-Sum Pairs
1. 3Sum

## Hard

1. Trapping Rain Water II
1. Largest Rectangle in Histogram *(different pattern)*

______________________________________________________________________

# Quick Revision

- Area = Width × Minimum Height.
- Start with the widest container.
- The shorter wall limits the water level.
- Move only the shorter pointer.
- Time: **O(n)**
- Space: **O(1)**
- Never sort—the positions matter.

______________________________________________________________________

# Key Takeaway

This problem teaches one of the most important interview ideas:

> **Every pointer movement should eliminate only choices that can never lead to a better answer.**

The proof that **moving the taller wall cannot improve the result** is the heart of this problem and is often what
interviewers care about most.

______________________________________________________________________

# Navigation

**Previous**

[13-valid-palindrome.md](13-valid-palindrome.md)

**Next**

[15-3sum.md](15-3sum.md)
