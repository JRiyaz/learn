# 48-climbing-stairs.md

# Climbing Stairs

> **🎯 Welcome to Dynamic Programming (DP).**
>
> Many engineers fear DP because they think it's full of complex mathematics.
>
> It isn't.
>
> **Dynamic Programming is simply remembering answers you've already computed so you don't solve the same problem repeatedly.**
>
> Climbing Stairs is the perfect first DP problem because it introduces every fundamental DP concept in a simple way.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 25–35 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Interviewers use this problem to test whether you understand:

- Recursion
- Overlapping Subproblems
- Memoization
- Bottom-Up DP
- Space Optimization

This same pattern appears in:

- Fibonacci
- House Robber
- Coin Change
- Decode Ways
- Word Break
- Unique Paths

______________________________________________________________________

# Problem Statement

You are climbing a staircase with **n** steps.

Each time,

you can climb either:

- **1 step**
- **2 steps**

Return the total number of **distinct ways** to reach the top.

______________________________________________________________________

## Example 1

```text
n = 2
```

Ways

```text
1 + 1

2
```

Answer

```text
2
```

______________________________________________________________________

## Example 2

```text
n = 3
```

Ways

```text
1 + 1 + 1

1 + 2

2 + 1
```

Answer

```text
3
```

______________________________________________________________________

# Before Learning Dynamic Programming

Suppose

```
n = 5
```

Question

How many ways can we reach step

```
5
```

Think backwards.

The final move must be:

```
1 Step
```

or

```
2 Steps
```

Therefore,

we must have come from:

```
Step 4

or

Step 3
```

That's the key insight.

______________________________________________________________________

# Backend Engineering Analogy

Imagine processing jobs.

To reach

```
Job 10
```

the previous completed job must have been:

```
Job 9

or

Job 8
```

Instead of recomputing everything,

reuse previously computed results.

Exactly Dynamic Programming.

______________________________________________________________________

# Pattern Recognition

## Pattern

**1-D Dynamic Programming**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Count ways
- Number of paths
- Minimum cost
- Maximum profit
- Choices at every step

Think

```
Dynamic Programming
```

______________________________________________________________________

# Brute Force Solution (Pure Recursion)

## Intuition

To reach step

```
n
```

we can come from

```
n-1
```

or

```
n-2
```

Recursive Formula

```text
Ways(n)

=

Ways(n-1)

+

Ways(n-2)
```

______________________________________________________________________

# Recursive Tree

Example

```
Ways(5)
```

```text
                5
             /     \
            4       3
          /  \     /  \
         3    2   2    1
       /  \
      2    1
```

Notice

```
Ways(3)
```

is computed

multiple times.

Huge waste.

______________________________________________________________________

# Why Is This Bad?

Repeated computation.

Example

```
Ways(3)
```

computed twice.

```
Ways(2)
```

computed three times.

As

```
n
```

grows,

duplicate work grows exponentially.

______________________________________________________________________

# Complexity

Time

```
O(2ⁿ)
```

Space

```
O(n)
```

Recursive stack.

______________________________________________________________________

# Better Observation

If

```
Ways(3)
```

was already computed,

why compute it again?

Store it.

Reuse it.

This is

```
Memoization
```

______________________________________________________________________

# Optimized Solution 1 — Memoization (Top-Down DP)

Store answers in a dictionary.

First time

```
Ways(5)
```

↓

Compute.

Second time

↓

Reuse.

______________________________________________________________________

# Complexity

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

# Better Observation Again

Notice

```
Ways(i)

depends only on

Ways(i-1)

Ways(i-2)
```

Need only

two variables.

______________________________________________________________________

# Optimized Solution 2 — Bottom-Up DP

Build answers

from

```
1

↓

2

↓

3

↓

...
```

Instead of recursion.

______________________________________________________________________

# Visual Explanation

Suppose

```
n = 5
```

Table

```text
Step

Ways
```

```text
1

1
```

```text
2

2
```

```text
3

3
```

```text
4

5
```

```text
5

8
```

Notice

Every value is the sum of the previous two.

Exactly Fibonacci.

______________________________________________________________________

# Why Is This Fibonacci?

Let's compare.

Fibonacci

```text
F(n)

=

F(n-1)

+

F(n-2)
```

Climbing Stairs

```text
Ways(n)

=

Ways(n-1)

+

Ways(n-2)
```

Same recurrence.

Different story.

______________________________________________________________________

# Step-by-Step Dry Run

Need

```
n = 5
```

Known

```text
Ways(1)=1

Ways(2)=2
```

Compute

```
Ways(3)

=

2+1

=

3
```

Compute

```
Ways(4)

=

3+2

=

5
```

Compute

```
Ways(5)

=

5+3

=

8
```

Answer

```
8
```

______________________________________________________________________

# Why This Works

Loop Invariant

> Before computing step `i`,
> we already know the correct number of ways for every smaller step.

Since

```
Ways(i)

depends only on

Ways(i-1)

Ways(i-2)
```

the answer is always available.

______________________________________________________________________

# Space Optimization

Need only

```text
Previous

Current
```

Example

```text
1

2
```

↓

```text
2

3
```

↓

```text
3

5
```

↓

```text
5

8
```

Old values are no longer needed.

______________________________________________________________________

# Edge Cases

### n = 1

Answer

```
1
```

______________________________________________________________________

### n = 2

Answer

```
2
```

______________________________________________________________________

### Large n

DP handles efficiently.

______________________________________________________________________

# Complexity Analysis

## Pure Recursion

Time

```
O(2ⁿ)
```

Space

```
O(n)
```

______________________________________________________________________

## Memoization

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Bottom-Up DP

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Optimized DP

Time

```
O(n)
```

Space

```
O(1)
```

______________________________________________________________________

# Production-Quality Python

## Recursive (Brute Force)

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n

    return (
        climb_stairs(n - 1)
        + climb_stairs(n - 2)
    )
```

______________________________________________________________________

## Memoization (Top-Down DP)

```python
from functools import lru_cache


def climb_stairs(n: int) -> int:
    @lru_cache(maxsize=None)
    def ways(step: int) -> int:
        if step <= 2:
            return step

        return ways(step - 1) + ways(step - 2)

    return ways(n)
```

______________________________________________________________________

## Bottom-Up DP

```python
from typing import List


def climb_stairs(n: int) -> int:
    if n <= 2:
        return n

    dp: List[int] = [0] * (n + 1)

    dp[1] = 1
    dp[2] = 2

    for step in range(3, n + 1):
        dp[step] = dp[step - 1] + dp[step - 2]

    return dp[n]
```

______________________________________________________________________

## Space-Optimized DP (Recommended)

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n

    previous = 1
    current = 2

    for _ in range(3, n + 1):
        previous, current = (
            current,
            previous + current,
        )

    return current
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using plain recursion.

Causes exponential runtime.

______________________________________________________________________

## Mistake 2

Not recognizing overlapping subproblems.

Repeated computation is the reason DP exists.

______________________________________________________________________

## Mistake 3

Thinking DP always needs arrays.

Sometimes

two variables

are enough.

______________________________________________________________________

## Mistake 4

Confusing recursion with DP.

Recursion

↓

Method

DP

↓

Optimization Technique.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "To reach step `n`, the last move must come from either step `n-1` or `n-2`. That gives the recurrence `ways(n) = ways(n-1) + ways(n-2)`. A recursive solution recomputes the same states repeatedly, so I'll use Dynamic Programming. Since each state depends only on the previous two, I can optimize the space to O(1)."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why is this DP?**

Because the problem has overlapping subproblems and an optimal recurrence relation.

______________________________________________________________________

**Q. Why can space be reduced to O(1)?**

Only the previous two states are needed.

______________________________________________________________________

**Q. Is this Fibonacci?**

Yes.

The recurrence is identical.

______________________________________________________________________

**Q. Where is this pattern used?**

- Coin Change
- Decode Ways
- House Robber
- Unique Paths
- Stock Trading DP

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | 1-D Dynamic Programming |
| Recurrence | dp[i] = dp[i-1] + dp[i-2] |
| Brute Force | Recursion |
| Better | Memoization |
| Best | Bottom-Up + Space Optimization |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Think backwards from the destination.
- Last move comes from `n-1` or `n-2`.
- Recursive solution repeats work.
- Memoization avoids recomputation.
- Bottom-Up DP builds answers iteratively.
- Only two previous values are required.
- Same recurrence as Fibonacci.
- Space can be optimized to O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Min Cost Climbing Stairs
1. Fibonacci Number
1. N-th Tribonacci Number

______________________________________________________________________

## Medium

4. House Robber
1. Decode Ways
1. Coin Change
1. Unique Paths

______________________________________________________________________

## Hard (Optional)

8. Word Break
1. Perfect Squares
1. Longest Increasing Subsequence

______________________________________________________________________

# Key Takeaway

The biggest lesson from Climbing Stairs is understanding the essence of **Dynamic Programming**: **don't solve the same
subproblem twice**. Once you identify the recurrence relation and recognize overlapping subproblems, the solution
naturally evolves from recursion → memoization → bottom-up DP → space optimization. This progression is the foundation
for solving almost every introductory DP interview problem.

______________________________________________________________________

# Next

[49-house-robber.md](49-house-robber.md)
