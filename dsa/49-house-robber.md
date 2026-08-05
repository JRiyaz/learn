# 49-house-robber.md

# House Robber

> **🎯 This is the most important beginner Dynamic Programming problem after Climbing Stairs.**
>
> Unlike Climbing Stairs, where we **count the number of ways**, this problem teaches how to **make the best decision at every step**.
>
> It introduces one of the most common DP interview patterns:
>
> **"Take it or Skip it."**
>
> This exact thinking appears in dozens of interview problems.

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

Interviewers want to evaluate whether you understand:

- Dynamic Programming state definition
- Decision making
- Optimal substructure
- Space optimization
- Converting recursion into DP

This pattern appears in:

- House Robber II
- Delete and Earn
- Paint House
- Stock Buy/Sell
- Maximum Sum of Non-Adjacent Elements
- Weighted Interval Scheduling

______________________________________________________________________

# Problem Statement

You are a robber planning to rob houses along a street.

Each house contains some money.

The constraint:

> If you rob **two adjacent houses**, the alarm will be triggered.

Return the **maximum amount of money** you can rob.

______________________________________________________________________

## Example 1

Input

```text
[1, 2, 3, 1]
```

Output

```text
4
```

Explanation

Rob

```text
1 + 3 = 4
```

Do not rob

```text
2 + 1 = 3
```

______________________________________________________________________

## Example 2

Input

```text
[2, 7, 9, 3, 1]
```

Output

```text
12
```

Rob

```text
2 + 9 + 1
```

Total

```text
12
```

______________________________________________________________________

# Before Learning the Algorithm

Imagine walking down a street.

At every house,

you have only **two choices**:

```text
Take

or

Skip
```

Nothing else.

That observation is the entire problem.

______________________________________________________________________

# Backend Engineering Analogy

Imagine scheduled maintenance windows.

Running maintenance on two adjacent servers causes downtime.

For every server:

```
Maintain

or

Skip
```

Goal

Maximize overall benefit.

Exactly the same optimization problem.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Decision Dynamic Programming**

______________________________________________________________________

## Recognition Clues

Whenever you hear:

- Maximize
- Minimize
- Cannot choose adjacent
- Choose or skip
- Non-overlapping

Think

```text
Take

vs

Skip
```

______________________________________________________________________

# Brute Force Solution

At every house

```text
Take

↓

Skip next

or

Skip current
```

Recursive Tree

Example

```text
[2,7,9]
```

```text
            2
         /     \
      Take     Skip
       |         |
       9         7
```

The same subproblems appear repeatedly.

______________________________________________________________________

# Why Is This Bad?

Suppose

```
House 4
```

is reached from two different paths.

We compute

```
Best Answer From House 4
```

multiple times.

Repeated work.

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

______________________________________________________________________

# Better Observation

The answer for

```
House i
```

never changes.

Compute it once.

Reuse it.

Dynamic Programming.

______________________________________________________________________

# Key Insight

For every house,

we have exactly two choices.

______________________________________________________________________

## Choice 1

Rob current house.

Then

cannot rob previous house.

Money

```text
Current Value

+

Best Until i-2
```

______________________________________________________________________

## Choice 2

Skip current house.

Money

```text
Best Until i-1
```

______________________________________________________________________

Take maximum.

______________________________________________________________________

# DP Formula

```text
dp[i]

=

max(

dp[i-1],

dp[i-2] + money[i]

)
```

This is the heart of the problem.

______________________________________________________________________

# Step-by-Step Dry Run

Input

```text
[2,7,9,3,1]
```

______________________________________________________________________

House

```
0

↓

2
```

DP

```
2
```

______________________________________________________________________

House

```
1

↓

7
```

Best

```
7
```

______________________________________________________________________

House

```
2

↓

9
```

Take

```
2+9=11
```

Skip

```
7
```

Best

```
11
```

______________________________________________________________________

House

```
3

↓

3
```

Take

```
7+3=10
```

Skip

```
11
```

Best

```
11
```

______________________________________________________________________

House

```
4

↓

1
```

Take

```
11+1=12
```

Skip

```
11
```

Best

```
12
```

Answer

```
12
```

______________________________________________________________________

# Visual Explanation

Input

```text
2 7 9 3 1
```

DP

```text
2

7

11

11

12
```

Every box stores

```
Best Profit So Far
```

______________________________________________________________________

# Why This Works

Loop Invariant

> Before computing `dp[i]`,
> we already know the maximum profit for all previous houses.

At every house,

we compare:

```text
Take

↓

Skip Previous

or

Skip Current
```

Whichever is larger becomes

```
dp[i]
```

______________________________________________________________________

# From DP Array to O(1) Space

Notice

Need only

```text
dp[i-1]

dp[i-2]
```

Older values are never used again.

Therefore,

replace the array with

two variables.

______________________________________________________________________

# Space Optimization

Instead of

```text
2

7

11

11

12
```

Keep only

```text
previous_two

previous_one
```

Example

```text
2

7
```

↓

```text
7

11
```

↓

```text
11

11
```

↓

```text
11

12
```

______________________________________________________________________

# Edge Cases

### Empty List

Answer

```
0
```

______________________________________________________________________

### One House

Return that value.

______________________________________________________________________

### Two Houses

Take the larger amount.

______________________________________________________________________

### All Same Value

Works correctly.

______________________________________________________________________

### Large Input

Still

```
O(n)
```

______________________________________________________________________

# Complexity Analysis

## Recursive

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

## Memoization

```python
from functools import lru_cache
from typing import List


def rob(houses: List[int]) -> int:
    @lru_cache(maxsize=None)
    def solve(index: int) -> int:
        if index >= len(houses):
            return 0

        take = houses[index] + solve(index + 2)
        skip = solve(index + 1)

        return max(take, skip)

    return solve(0)
```

______________________________________________________________________

## Bottom-Up DP

```python
from typing import List


def rob(houses: List[int]) -> int:
    if not houses:
        return 0

    if len(houses) == 1:
        return houses[0]

    dp = [0] * len(houses)

    dp[0] = houses[0]
    dp[1] = max(houses[0], houses[1])

    for index in range(2, len(houses)):
        dp[index] = max(
            dp[index - 1],
            dp[index - 2] + houses[index],
        )

    return dp[-1]
```

______________________________________________________________________

## Space-Optimized (Recommended)

```python
from typing import List


def rob(houses: List[int]) -> int:
    previous_two = 0
    previous_one = 0

    for money in houses:
        current = max(
            previous_one,
            previous_two + money,
        )

        previous_two = previous_one
        previous_one = current

    return previous_one
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Trying to greedily take the larger adjacent house.

Greedy does not always produce the optimal answer.

______________________________________________________________________

## Mistake 2

Not recognizing the two choices:

```
Take

Skip
```

Every DP state comes from these decisions.

______________________________________________________________________

## Mistake 3

Thinking the DP array is required.

Only the previous two values are needed.

______________________________________________________________________

## Mistake 4

Confusing

Current House Value

with

Maximum Profit So Far.

The DP state stores

the best profit,

not the current money.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "At every house, I have two choices: rob it or skip it. If I rob it, I must skip the previous house, so the profit becomes `dp[i-2] + houses[i]`. If I skip it, the profit remains `dp[i-1]`. I'll take the maximum of these two choices. Since each state depends only on the previous two states, I can optimize the space to O(1)."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why isn't a greedy solution correct?**

A locally larger house may prevent a better overall combination later.

______________________________________________________________________

**Q. Why is this Dynamic Programming?**

Because the problem has optimal substructure and overlapping subproblems.

______________________________________________________________________

**Q. Why can the DP array be removed?**

Each state depends only on the previous two states.

______________________________________________________________________

**Q. Where is this pattern used?**

- Stock trading
- Scheduling
- Resource allocation
- Interval selection
- Weighted optimization problems

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Take or Skip DP |
| State | `dp[i]` = Best profit up to house `i` |
| Formula | `max(dp[i-1], dp[i-2] + value)` |
| Brute Force | Recursion |
| Better | Memoization |
| Best | Bottom-Up + O(1) Space |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- At every house, choose **Take** or **Skip**.
- If you take the current house, you must skip the previous one.
- DP recurrence: `max(dp[i-1], dp[i-2] + money[i])`.
- Recursive solution repeats work.
- Memoization removes duplicate computation.
- Bottom-up DP is iterative.
- Space can be optimized to O(1).
- This is the classic "Take or Skip" DP pattern.

______________________________________________________________________

# Practice Questions

## Easy

1. Min Cost Climbing Stairs
1. Fibonacci Number
1. Climbing Stairs

______________________________________________________________________

## Medium

4. House Robber II
1. Delete and Earn
1. Paint House
1. Best Time to Buy and Sell Stock with Cooldown

______________________________________________________________________

## Hard (Optional)

8. Burst Balloons
1. Maximum Profit in Job Scheduling
1. Cherry Pickup

______________________________________________________________________

# Key Takeaway

The biggest lesson from House Robber is recognizing that **every DP problem starts with defining the right state and the
available choices**. Here, the state is the **maximum profit up to a given house**, and the choices are simply **take**
or **skip**. Once you identify those choices, the recurrence becomes obvious, and the solution naturally progresses from
recursion to memoization to an O(1)-space dynamic programming solution.

______________________________________________________________________

# Next

[50-jump-game.md](50-jump-game.md)
