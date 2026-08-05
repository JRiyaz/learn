# 07-gcd-lcm.md

# GCD & LCM

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | High |
| Importance | ⭐⭐⭐⭐☆ |
| Expected Interview Time | 15–20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

GCD (Greatest Common Divisor) and LCM (Least Common Multiple) are classic interview questions because they test whether
you can:

- Identify patterns
- Improve a brute-force algorithm
- Understand mathematical reasoning
- Apply optimization instead of brute force

More importantly, the **Euclidean Algorithm** is considered one of the most elegant algorithms in Computer Science.

______________________________________________________________________

# Problem Statement

Given two positive integers `a` and `b`:

- Find their **Greatest Common Divisor (GCD)**.
- Find their **Least Common Multiple (LCM)**.

______________________________________________________________________

## Example

```
Input

a = 12
b = 18
```

Output

```
GCD = 6

LCM = 36
```

______________________________________________________________________

# Simple English

## GCD

The largest number that divides both numbers.

Example

```
12

Factors

1 2 3 4 6 12
```

```
18

Factors

1 2 3 6 9 18
```

Common factors

```
1 2 3 6
```

Largest

```
6
```

______________________________________________________________________

## LCM

The smallest number that both numbers can divide evenly.

Example

```
12

Multiples

12 24 36 48 ...
```

```
18

Multiples

18 36 54 ...
```

First common multiple

```
36
```

______________________________________________________________________

# Backend Engineering Analogy

Imagine two scheduled jobs.

Job A runs every

```
12 minutes
```

Job B runs every

```
18 minutes
```

When will they run together again?

Answer

```
36 minutes
```

That's the **LCM**.

______________________________________________________________________

Suppose two log files are split into blocks.

One has block size

```
12 KB
```

Another has

```
18 KB
```

What's the largest block size that can divide both exactly?

That's the **GCD**.

These concepts appear in:

- Scheduling systems
- Cron jobs
- Distributed processing
- Memory alignment
- Networking
- Data partitioning

______________________________________________________________________

# Pattern Recognition

Pattern

**Repeated Reduction**

Recognition clues

Whenever you see

- Common divisor
- Greatest divisor
- Synchronization
- Scheduling
- Cyclic repetition

Think

```
Can the problem be reduced repeatedly?
```

______________________________________________________________________

# Brute Force Solution (GCD)

## Intuition

Check every number from

```
1

↓

min(a, b)
```

The largest number dividing both is the answer.

______________________________________________________________________

## Algorithm

Example

```
12

18
```

Check

```
1

↓

2

↓

3

↓

4

↓

5

↓

6

↓

...

↓

12
```

Largest divisor found

```
6
```

______________________________________________________________________

## Dry Run

```
12

18
```

```
1

Divides both

✔
```

```
2

✔
```

```
3

✔
```

```
4

Only divides 12

✖
```

```
5

✖
```

```
6

✔
```

Continue...

Largest answer

```
6
```

______________________________________________________________________

## Complexity

Time

```
O(min(a,b))
```

Space

```
O(1)
```

______________________________________________________________________

## Limitations

Suppose

```
a = 1,000,000

b = 999,999
```

Checking every number is slow.

Can we avoid checking every divisor?

Yes.

______________________________________________________________________

# Optimized Solution (Euclidean Algorithm)

## Key Insight

Suppose

```
GCD(18,12)
```

Notice

```
18

=

12 × 1 + 6
```

Now ask

```
GCD(12,6)
```

Instead of

```
GCD(18,12)
```

Nothing changes.

Because

```
Every divisor of 18 and 12

also divides

6
```

So we can reduce the problem.

______________________________________________________________________

## Euclidean Formula

Instead of

```
GCD(a,b)
```

compute

```
GCD(b, a % b)
```

Repeat until

```
b == 0
```

Then

```
a

is the GCD
```

______________________________________________________________________

# Why Does This Work?

Take

```
48

18
```

```
48

=

18 × 2 + 12
```

Any number dividing

```
48

and

18
```

must also divide

```
12
```

Therefore

```
GCD(48,18)

=

GCD(18,12)
```

We keep shrinking the numbers until one becomes zero.

______________________________________________________________________

# Step-by-Step Dry Run

Find

```
GCD(48,18)
```

Step 1

```
48 % 18

=

12
```

New problem

```
GCD(18,12)
```

______________________________________________________________________

Step 2

```
18 % 12

=

6
```

New problem

```
GCD(12,6)
```

______________________________________________________________________

Step 3

```
12 % 6

=

0
```

New problem

```
GCD(6,0)
```

Stop.

Answer

```
6
```

______________________________________________________________________

# Visual Explanation

```
GCD(48,18)

↓

GCD(18,12)

↓

GCD(12,6)

↓

GCD(6,0)

↓

Answer = 6
```

Every step makes the problem smaller.

______________________________________________________________________

# Finding LCM

Once GCD is known,

LCM is easy.

Formula

```
LCM(a,b)

=

(a × b)

/

GCD(a,b)
```

Example

```
12 × 18

=

216
```

```
216 / 6

=

36
```

Answer

```
LCM = 36
```

______________________________________________________________________

# Why This Formula Works

Observe

```
GCD × LCM

=

a × b
```

Example

```
12

18
```

```
GCD

6
```

```
LCM

36
```

```
6 × 36

=

216
```

```
12 × 18

=

216
```

Always true.

______________________________________________________________________

# Edge Cases

### Same Numbers

```
GCD(10,10)

=

10
```

```
LCM(10,10)

=

10
```

______________________________________________________________________

### One Number is 1

```
GCD(1,15)

=

1
```

```
LCM(1,15)

=

15
```

______________________________________________________________________

### One Number is 0

```
GCD(0,10)

=

10
```

```
LCM(0,10)

=

0
```

______________________________________________________________________

### Both Zero

Mathematically undefined.

Handle according to system requirements.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(min(a,b))
```

Space

```
O(1)
```

______________________________________________________________________

## Euclidean Algorithm

Time

```
O(log(min(a,b)))
```

Space

```
O(1)
```

This is dramatically faster.

Example

```
1,000,000

999,999
```

The Euclidean algorithm finishes in only a handful of iterations instead of nearly a million checks.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
def gcd_brute_force(first: int, second: int) -> int:
    limit = min(first, second)
    gcd = 1

    for divisor in range(1, limit + 1):
        if first % divisor == 0 and second % divisor == 0:
            gcd = divisor

    return gcd
```

______________________________________________________________________

## Optimized (Euclidean Algorithm)

```python
def gcd(first: int, second: int) -> int:
    while second != 0:
        first, second = second, first % second

    return abs(first)
```

______________________________________________________________________

## LCM

```python
def gcd(first: int, second: int) -> int:
    while second != 0:
        first, second = second, first % second

    return abs(first)


def lcm(first: int, second: int) -> int:
    if first == 0 or second == 0:
        return 0

    return abs(first * second) // gcd(first, second)


if __name__ == "__main__":
    print(gcd(48, 18))
    print(lcm(12, 18))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Checking divisors all the way up to the larger number.

Only the smaller number needs to be considered in the brute-force solution.

______________________________________________________________________

## Mistake 2

Using

```python
/
```

instead of

```python
//
```

LCM is an integer.

Always use integer division.

______________________________________________________________________

## Mistake 3

Forgetting to handle zero.

The LCM of any number with zero is zero.

______________________________________________________________________

## Mistake 4

Memorizing the Euclidean algorithm without understanding **why** `a % b` works.

Always remember:

> The remainder preserves the common divisors.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A straightforward solution is to check every possible divisor up to the smaller number, but that's inefficient. The Euclidean Algorithm repeatedly replaces the problem `GCD(a, b)` with `GCD(b, a % b)`, which keeps the same answer while rapidly reducing the input size. Once I have the GCD, I can compute the LCM using the relationship `(a × b) / GCD`."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why does `GCD(a, b) = GCD(b, a % b)`?**

Because any divisor common to `a` and `b` must also divide the remainder `a % b`.

______________________________________________________________________

**Q. Why is the Euclidean algorithm so fast?**

The numbers shrink significantly after each iteration, giving a logarithmic time complexity.

______________________________________________________________________

**Q. Can I use Python's built-in function?**

Yes.

```python
import math

math.gcd(a, b)
```

But in interviews, you're usually expected to implement it yourself.

______________________________________________________________________

**Q. Where is LCM used in software engineering?**

- Task scheduling
- Cron jobs
- Periodic synchronization
- Cyclic events
- Data partitioning

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Repeated Reduction |
| Recognition | GCD / Common Divisor |
| Brute Force | Check all divisors |
| Optimized | Euclidean Algorithm |
| Time | O(log(min(a,b))) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- GCD is the largest common divisor.
- LCM is the smallest common multiple.
- Brute force checks every divisor.
- Euclidean Algorithm repeatedly computes `a % b`.
- Stop when the second number becomes zero.
- The remaining first number is the GCD.
- `LCM = (a × b) / GCD`.
- Euclidean Algorithm runs in **O(log n)**.
- It is one of the most important algorithms in computer science.

______________________________________________________________________

# Practice Questions

## Easy

1. Find GCD of N Numbers
1. Find All Divisors of a Number
1. Check Coprime Numbers

______________________________________________________________________

## Medium

4. Fraction Addition and Subtraction
1. Nth Magical Number
1. Water and Jug Problem
1. GCD Traversal

______________________________________________________________________

## Hard (Optional)

8. Replace Non-Coprime Numbers in Array
1. Count Different Subsequences GCDs
1. Greatest Common Divisor Traversal

______________________________________________________________________

# Key Takeaway

The Euclidean Algorithm is a perfect example of **algorithmic optimization through mathematical insight**. Instead of
checking every possible divisor, it repeatedly reduces the problem size while preserving the answer, giving an elegant
**O(log n)** solution. This style of thinking—reducing a large problem into an equivalent smaller one—appears throughout
DSA and system design.

______________________________________________________________________

# Next

[08-power-of-two.md](08-power-of-two.md)
