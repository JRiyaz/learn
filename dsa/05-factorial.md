# 05-factorial.md

# Factorial

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | High |
| Importance | ⭐⭐⭐⭐☆ |
| Expected Interview Time | 10–15 minutes |
| Revision Time | 5 minutes |

______________________________________________________________________

# Why Interviewers Ask This

At first glance, Factorial looks like a simple mathematics problem.

However, interviewers use it to evaluate whether you understand:

- Iteration
- Recursion
- Base cases
- Multiplicative accumulation
- Time and space complexity
- When recursion is a bad idea

For backend engineers, the biggest takeaway is **understanding recursion**, not memorizing the factorial formula.

______________________________________________________________________

# Problem Statement

Given a non-negative integer `n`, return its factorial.

Factorial is represented as:

```
n!
```

It means multiplying every integer from **1** to **n**.

```
5!

=

5 × 4 × 3 × 2 × 1

=

120
```

______________________________________________________________________

## Example 1

```text
Input:
5

Output:
120
```

______________________________________________________________________

## Example 2

```text
Input:
1

Output:
1
```

______________________________________________________________________

## Example 3

```text
Input:
0

Output:
1
```

______________________________________________________________________

# Simple English

Imagine climbing a staircase.

Instead of adding one step at a time,

you're multiplying every step you've already climbed.

```
5

↓

5 × 4 × 3 × 2 × 1
```

______________________________________________________________________

# Common Misunderstandings

## Why is 0! equal to 1?

This surprises almost everyone.

Mathematically,

```
0!

=

1
```

Think of it this way.

If there are **no numbers to multiply**, the multiplication identity is **1**, just like the sum of no numbers is **0**.

For interviews,

just remember:

```
0! = 1
```

______________________________________________________________________

# Backend Engineering Analogy

Suppose an API has **n independent configuration options**.

To calculate the number of ways they can be arranged,

factorial is used.

Examples include:

- Scheduling jobs
- Ordering tasks
- Generating permutations
- Cryptography
- Search algorithms

Factorial appears frequently in combinatorics and optimization problems.

______________________________________________________________________

# Pattern Recognition

### Pattern

**Multiplicative Accumulation**

Recognition clues:

Whenever you see:

- Product of numbers
- Permutations
- Combinations
- Recursive definition

Think

```
answer *= current_number
```

or

```
f(n) = n × f(n-1)
```

______________________________________________________________________

# Brute Force Solution (Recursive)

## Why Start with Recursion?

Factorial has a natural recursive definition.

```
5!

=

5 × 4!
```

Similarly,

```
4!

=

4 × 3!
```

Continue until

```
1!
```

______________________________________________________________________

## Recursive Formula

```
factorial(n)

=

n × factorial(n-1)
```

Base case

```
factorial(0)

=

1
```

______________________________________________________________________

## Dry Run

Find

```
5!
```

```
factorial(5)

↓

5 × factorial(4)

↓

5 × 4 × factorial(3)

↓

5 × 4 × 3 × factorial(2)

↓

5 × 4 × 3 × 2 × factorial(1)

↓

5 × 4 × 3 × 2 × 1

↓

120
```

______________________________________________________________________

## Visual Explanation

```
factorial(5)

│

├── 5 × factorial(4)

│

├── 4 × factorial(3)

│

├── 3 × factorial(2)

│

├── 2 × factorial(1)

│

└── 1
```

Now unwind

```
1

↓

2

↓

6

↓

24

↓

120
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

Why?

Every recursive call is stored in the call stack.

______________________________________________________________________

## Limitations

For

```
100000!
```

Python throws

```
RecursionError
```

because recursion has a depth limit.

Can we avoid recursion?

Yes.

______________________________________________________________________

# Optimized Solution (Iterative)

## Key Insight

We don't actually need recursion.

We only need to multiply numbers from

```
1

↓

n
```

______________________________________________________________________

## Step-by-Step Algorithm

Example

```
5
```

Start

```
answer = 1
```

Iteration 1

```
answer = 1 × 1

↓

1
```

Iteration 2

```
answer = 1 × 2

↓

2
```

Iteration 3

```
2 × 3

↓

6
```

Iteration 4

```
6 × 4

↓

24
```

Iteration 5

```
24 × 5

↓

120
```

Finished.

______________________________________________________________________

# Visual Explanation

```
answer

1

↓

1

↓

2

↓

6

↓

24

↓

120
```

Think of it as a rolling multiplication.

______________________________________________________________________

# Why This Works

Every iteration multiplies the next integer.

At iteration

```
i
```

the variable

```
answer
```

already stores

```
i!
```

This is called the **loop invariant**.

After the final iteration,

```
answer

=

n!
```

______________________________________________________________________

# Edge Cases

### Zero

```
0!

=

1
```

______________________________________________________________________

### One

```
1!

=

1
```

______________________________________________________________________

### Negative Numbers

Factorial is **not defined**.

Raise an exception or return an appropriate error.

______________________________________________________________________

### Large Numbers

Python supports arbitrarily large integers, so factorials can grow very large without integer overflow (though
computation becomes slower).

______________________________________________________________________

# Complexity Analysis

## Recursive

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

## Iterative

Time

```
O(n)
```

Space

```
O(1)
```

The iterative approach is preferred because it avoids recursion overhead.

______________________________________________________________________

# Production-Quality Python

## Recursive

```python
def factorial_recursive(number: int) -> int:
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    if number <= 1:
        return 1

    return number * factorial_recursive(number - 1)
```

______________________________________________________________________

## Iterative (Recommended)

```python
def factorial(number: int) -> int:
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1

    for current in range(2, number + 1):
        result *= current

    return result


if __name__ == "__main__":
    print(factorial(5))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Forgetting the base case.

Without it,

the recursion never stops.

______________________________________________________________________

## Mistake 2

Returning

```
0
```

for

```
0!
```

Correct answer is

```
1
```

______________________________________________________________________

## Mistake 3

Using recursion for very large inputs.

Python has a recursion limit.

______________________________________________________________________

## Mistake 4

Starting multiplication from

```
0
```

```
answer *= 0

↓

0
```

Everything becomes zero.

Always start from

```
1
```

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The recursive definition of factorial is straightforward because `n! = n × (n-1)!`. However, recursion uses additional stack space and can hit recursion limits for large inputs. An iterative solution performs the same computation in O(n) time while using O(1) extra space, making it preferable in production code."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why is recursion less preferred?**

Because every recursive call consumes stack memory.

______________________________________________________________________

**Q. Why is 0! equal to 1?**

It is defined mathematically as the multiplicative identity and makes many formulas consistent.

______________________________________________________________________

**Q. Can factorial become very large?**

Yes.

For example,

```
100!
```

has 158 digits.

______________________________________________________________________

**Q. Which solution would you use in production?**

The iterative solution because it is simpler and avoids recursion overhead.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Multiplicative Accumulation |
| Recognition | Product of Consecutive Numbers |
| Brute Force | Recursion |
| Optimized | Iteration |
| Time | O(n) |
| Space | O(1) (Iterative) |

______________________________________________________________________

# Quick Revision

- Factorial means multiplying all integers from 1 to n.
- `0!` and `1!` are both equal to `1`.
- Recursive formula is `n × factorial(n-1)`.
- Recursion requires a base case.
- Iterative solution avoids recursion limits.
- Iterative approach uses O(1) space.
- Python integers can grow arbitrarily large.
- Use iteration in production unless recursion is specifically required.

______________________________________________________________________

# Practice Questions

## Easy

1. Fibonacci Number
1. Sum of Natural Numbers
1. Power of a Number
1. Count Digits

______________________________________________________________________

## Medium

5. Climbing Stairs
1. Pascal's Triangle
1. Permutations
1. Combinations

______________________________________________________________________

## Hard (Optional)

9. K-th Permutation Sequence
1. Permutation Sequence II

______________________________________________________________________

# Key Takeaway

Factorial teaches one of the most important programming concepts: **breaking a problem into smaller subproblems
(recursion)** and then recognizing when an **iterative solution is more practical**. In interviews, always discuss both
approaches and explain why iteration is generally preferred in production systems.

______________________________________________________________________

# Next

[06-fibonacci.md](06-fibonacci.md)
