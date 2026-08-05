# 06-fibonacci.md

# Fibonacci Number

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 15–20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

Many beginners think Fibonacci is about mathematics.

It isn't.

Interviewers ask this problem because it introduces one of the most important ideas in programming:

- Recursion
- Overlapping subproblems
- Dynamic Programming
- Memoization
- Space Optimization

This single problem teaches the evolution of problem solving.

```
Brute Force
      ↓
Better Solution
      ↓
Best Solution
```

Many Dynamic Programming interview questions are simply an extension of Fibonacci.

______________________________________________________________________

# Problem Statement

The Fibonacci sequence is defined as:

```
F(0) = 0

F(1) = 1

F(n) = F(n-1) + F(n-2)
```

Given an integer `n`, return the `n`th Fibonacci number.

______________________________________________________________________

## Example 1

```text
Input:
5

Output:
5
```

Sequence

```
0 1 1 2 3 5
```

______________________________________________________________________

## Example 2

```text
Input:
7

Output:
13
```

Sequence

```
0 1 1 2 3 5 8 13
```

______________________________________________________________________

# Simple English

Imagine two rabbits.

Every month,

the next generation is produced using the previous two generations.

```
Month 0

0

Month 1

1

Month 2

0 + 1 = 1

Month 3

1 + 1 = 2

Month 4

1 + 2 = 3

Month 5

2 + 3 = 5
```

Every number depends on the previous two numbers.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a caching system.

A service asks for

```
fib(50)
```

Without caching,

the service computes the same values repeatedly.

```
fib(10)

computed

1000 times
```

With caching,

```
fib(10)

computed

once
```

This is exactly how Redis or in-memory caches improve API performance.

______________________________________________________________________

# Pattern Recognition

Pattern:

**Dynamic Programming**

Recognition clues

Whenever you see

- Previous answer needed
- Overlapping calculations
- Repeated recursion
- Minimum cost
- Maximum profit
- Number of ways

Think

```
Can I save previously computed results?
```

______________________________________________________________________

# Brute Force Solution (Recursive)

## Intuition

The formula itself tells us how to solve it.

```
fib(n)

=

fib(n-1)

+

fib(n-2)
```

Just implement the definition.

______________________________________________________________________

## Algorithm

```
fib(5)

↓

fib(4)

+

fib(3)
```

Each problem breaks into two smaller problems.

______________________________________________________________________

## Dry Run

```
fib(5)

↓

fib(4) + fib(3)

↓

(fib(3)+fib(2))

+

(fib(2)+fib(1))
```

Notice something?

```
fib(3)

appears twice

fib(2)

appears THREE times

fib(1)

appears MANY times
```

The same work is repeated again and again.

______________________________________________________________________

# Recursive Tree

```
                fib(5)
               /      \
          fib(4)      fib(3)
          /    \      /     \
     fib(3) fib(2) fib(2) fib(1)
      /  \      \      \
 fib(2) fib(1) fib(1) fib(0)
```

Highlighted repetition

```
fib(3)

computed twice


fib(2)

computed three times
```

This is the main problem.

______________________________________________________________________

## Complexity

Time

```
O(2ⁿ)
```

Space

```
O(n)
```

Very slow.

______________________________________________________________________

## Limitations

For

```
fib(45)
```

the recursive solution performs millions of unnecessary calls.

Can we avoid repeated calculations?

Yes.

______________________________________________________________________

# Better Solution (Memoization)

## Key Insight

If

```
fib(10)
```

has already been computed,

why compute it again?

Store the answer.

Next time,

reuse it.

This technique is called

```
Memoization
```

______________________________________________________________________

## Algorithm

```
Need fib(6)

↓

Check cache

↓

Already exists?

↓

Yes

↓

Return immediately
```

No extra computation.

______________________________________________________________________

## Dry Run

```
fib(5)

↓

Store

fib(2)=1

fib(3)=2

fib(4)=3

fib(5)=5
```

Every Fibonacci number is computed exactly once.

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

Much faster.

______________________________________________________________________

# Optimized Solution (Bottom-Up DP)

## Key Insight

Instead of solving

```
Top

↓

Bottom
```

solve

```
Bottom

↓

Top
```

Start with known answers.

```
0

1
```

Then keep building.

______________________________________________________________________

## Step-by-Step Algorithm

Find

```
fib(7)
```

Start

```
previous = 0

current = 1
```

Iteration

```
0

1

↓

1

↓

2

↓

3

↓

5

↓

8

↓

13
```

No recursion.

No cache.

Only two variables.

______________________________________________________________________

# Visual Explanation

```
Index

0

1

2

3

4

5

6

7
```

Values

```
0

1

1

2

3

5

8

13
```

Every new value

```
=

previous

+

current
```

______________________________________________________________________

# Why This Works

Observe

```
fib(5)

depends only on

fib(4)

and

fib(3)
```

Older values are never used again.

Therefore,

instead of storing

```
Entire array
```

we only keep

```
Previous

Current
```

Memory drops from

```
O(n)

↓

O(1)
```

______________________________________________________________________

# Edge Cases

### n = 0

```
Answer

0
```

______________________________________________________________________

### n = 1

```
Answer

1
```

______________________________________________________________________

### Large n

Recursive solution becomes extremely slow.

Iterative solution remains efficient.

______________________________________________________________________

### Negative Numbers

Usually invalid unless the interviewer defines negative Fibonacci numbers.

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

## Iterative (Best)

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

## Brute Force

```python
def fibonacci_recursive(number: int) -> int:
    if number <= 1:
        return number

    return (
        fibonacci_recursive(number - 1)
        + fibonacci_recursive(number - 2)
    )
```

______________________________________________________________________

## Better (Memoization)

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(number: int) -> int:
    if number <= 1:
        return number

    return fibonacci(number - 1) + fibonacci(number - 2)
```

> `@lru_cache` automatically stores previously computed values, eliminating repeated recursive calls.

______________________________________________________________________

## Optimized (Recommended)

```python
def fibonacci(number: int) -> int:
    if number <= 1:
        return number

    previous = 0
    current = 1

    for _ in range(2, number + 1):
        previous, current = current, previous + current

    return current


if __name__ == "__main__":
    print(fibonacci(7))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Writing only the recursive solution.

Interviewers often expect you to recognize its inefficiency and improve it.

______________________________________________________________________

## Mistake 2

Not handling

```
0
```

and

```
1
```

These are the base cases.

______________________________________________________________________

## Mistake 3

Confusing recursion with Dynamic Programming.

Recursion alone does **not** optimize anything.

DP means storing or reusing previous results.

______________________________________________________________________

## Mistake 4

Creating an unnecessary array.

Only the previous two Fibonacci numbers are required.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The recursive solution directly follows the mathematical definition, but it recomputes the same subproblems many times, leading to exponential complexity. Memoization reduces this to O(n) by caching results. Since each Fibonacci number depends only on the previous two, we can optimize further using an iterative solution with constant extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why is recursion slow?**

Because it solves the same subproblems repeatedly.

______________________________________________________________________

**Q. What is Memoization?**

Caching results of recursive calls.

______________________________________________________________________

**Q. Difference between Memoization and Tabulation?**

Memoization:

- Top-down
- Recursive

Tabulation:

- Bottom-up
- Iterative

______________________________________________________________________

**Q. Which solution is best in production?**

The iterative solution because it is fast, uses O(1) space, and avoids recursion overhead.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Dynamic Programming |
| Recognition | Previous Results Needed |
| Brute Force | Pure Recursion |
| Better | Memoization |
| Best | Bottom-Up Iteration |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Fibonacci is the foundation of Dynamic Programming.
- Pure recursion has overlapping subproblems.
- Memoization stores previously computed answers.
- Tabulation builds answers from the bottom up.
- Iterative DP uses only two variables.
- Recursive solution is O(2ⁿ).
- Iterative solution is O(n) time and O(1) space.
- Prefer the iterative solution in production.

______________________________________________________________________

# Practice Questions

## Easy

1. Climbing Stairs
1. Tribonacci Number
1. Min Cost Climbing Stairs

______________________________________________________________________

## Medium

4. House Robber
1. Decode Ways
1. Coin Change
1. Unique Paths

______________________________________________________________________

## Hard (Optional)

8. Longest Increasing Subsequence
1. Edit Distance
1. Word Break

______________________________________________________________________

# Key Takeaway

Fibonacci is **far more than a math problem**—it's your introduction to **Dynamic Programming**. The most important
lesson is recognizing **overlapping subproblems** and learning how to eliminate redundant work using memoization or
bottom-up iteration. This thought process will be reused in dozens of medium-level interview questions.

______________________________________________________________________

# Next

[07-gcd-lcm.md](07-gcd-lcm.md)
