# 08-power-of-two.md

# Power of Two

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 10–15 minutes |
| Revision Time | 5 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This problem looks deceptively simple.

Many candidates solve it using loops, but interviewers are often looking for a deeper understanding of **binary
representation** and **bit manipulation**.

This question tests whether you can:

- Recognize patterns in binary numbers
- Improve a brute-force solution
- Understand bitwise operations
- Write efficient code

For backend engineers, understanding bits is valuable because they appear in:

- Permissions (Linux file permissions)
- Feature flags
- Network protocols
- Memory alignment
- Hashing
- Compression

______________________________________________________________________

# Problem Statement

Given an integer `n`, determine whether it is a power of two.

Return:

- `True` if `n` is a power of two.
- `False` otherwise.

______________________________________________________________________

## Example 1

```text
Input:
1

Output:
True
```

Because

```
2⁰ = 1
```

______________________________________________________________________

## Example 2

```text
Input:
16

Output:
True
```

Because

```
2⁴ = 16
```

______________________________________________________________________

## Example 3

```text
Input:
18

Output:
False
```

Because

```
16 < 18 < 32
```

______________________________________________________________________

## Example 4

```text
Input:
0

Output:
False
```

______________________________________________________________________

# Simple English

A power of two is obtained by multiplying 2 repeatedly.

```
1

↓

2

↓

4

↓

8

↓

16

↓

32

↓

64
```

If your number appears in this sequence,

it's a power of two.

______________________________________________________________________

# Backend Engineering Analogy

Suppose your caching system allocates memory in blocks.

```
1 KB

2 KB

4 KB

8 KB

16 KB

32 KB
```

Most operating systems and databases allocate memory in powers of two because it aligns efficiently with binary
hardware.

Examples:

- Redis memory allocation
- CPU cache lines
- Buffer sizes
- Page sizes
- Network packet sizes

______________________________________________________________________

# Pattern Recognition

### Pattern

**Bit Manipulation**

Recognition clues:

Whenever you see:

- Power of Two
- Power of Four
- Count Set Bits
- Single Number
- Bit Masks

Think:

```
Binary Representation
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Keep dividing the number by 2.

If you eventually reach 1,

it's a power of two.

If at any point the number is not divisible by 2,

it isn't.

______________________________________________________________________

## Algorithm

Example

```
16
```

```
16

↓

8

↓

4

↓

2

↓

1

↓

Power of Two
```

______________________________________________________________________

Example

```
18
```

```
18

↓

9
```

Now

```
9

is not divisible by 2
```

Stop.

Answer

```
False
```

______________________________________________________________________

## Dry Run

Input

```
32
```

```
32

↓

16

↓

8

↓

4

↓

2

↓

1
```

Reached

```
1
```

Return

```
True
```

______________________________________________________________________

## Complexity

Time

```
O(log n)
```

because the number is divided by 2 each iteration.

Space

```
O(1)
```

______________________________________________________________________

## Limitations

Although efficient,

we're still performing multiple divisions.

Can we answer this with **one bit operation**?

Yes.

______________________________________________________________________

# Optimized Solution (Bit Manipulation)

## Key Insight

Let's write powers of two in binary.

| Decimal | Binary |
|---------|--------|
|1|0001|
|2|0010|
|4|0100|
|8|1000|
|16|10000|

Notice something?

Every power of two has **exactly one bit set to 1**.

______________________________________________________________________

Now subtract one.

Example

```
16

10000
```

```
15

01111
```

Perform

```
10000

AND

01111
```

Result

```
00000
```

Interesting!

______________________________________________________________________

Let's try

```
8

1000
```

```
7

0111
```

```
1000

AND

0111

↓

0000
```

Again,

zero.

______________________________________________________________________

Now try

```
10

1010
```

```
9

1001
```

```
1010

AND

1001

↓

1000
```

Not zero.

Therefore,

```
10

is NOT a power of two.
```

______________________________________________________________________

# The Formula

A positive number is a power of two if:

```python
n > 0 and (n & (n - 1)) == 0
```

This is one of the most common bit manipulation tricks asked in interviews.

______________________________________________________________________

# Why Does This Work?

A power of two has only one set bit.

Example

```
100000
```

Subtracting one changes it into

```
011111
```

Notice

```
Original

100000

New

011111
```

There is **no position where both numbers have a 1**.

Therefore

```
AND

↓

0
```

For any non-power of two,

multiple bits are already set,

so the AND operation is not zero.

______________________________________________________________________

# Visual Explanation

Example

```
16

10000
```

```
15

01111
```

```
10000

AND

01111

↓

00000

✔
```

______________________________________________________________________

Example

```
18

10010
```

```
17

10001
```

```
10010

AND

10001

↓

10000

✖
```

______________________________________________________________________

# Edge Cases

### Zero

```
0
```

Not a power of two.

______________________________________________________________________

### One

```
1

=

2⁰
```

Power of two.

______________________________________________________________________

### Negative Numbers

Never powers of two in this context.

Return

```
False
```

______________________________________________________________________

### Large Numbers

The bitwise solution still runs in constant time.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(log n)
```

Space

```
O(1)
```

______________________________________________________________________

## Optimized

Time

```
O(1)
```

Space

```
O(1)
```

The optimized solution performs only a few bitwise operations regardless of input size.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
def is_power_of_two(number: int) -> bool:
    if number <= 0:
        return False

    while number > 1:
        if number % 2 != 0:
            return False

        number //= 2

    return True
```

______________________________________________________________________

## Optimized (Recommended)

```python
def is_power_of_two(number: int) -> bool:
    if number <= 0:
        return False

    return (number & (number - 1)) == 0


if __name__ == "__main__":
    print(is_power_of_two(16))
    print(is_power_of_two(18))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Forgetting to handle

```
0
```

```
0 & -1

=

0
```

Without checking

```python
number > 0
```

the formula incorrectly returns `True`.

Always write:

```python
number > 0 and (number & (number - 1)) == 0
```

______________________________________________________________________

## Mistake 2

Using

```python
and
```

instead of

```python
&
```

`and` is a logical operator.

`&` is a bitwise operator.

______________________________________________________________________

## Mistake 3

Not understanding **why** the bit trick works.

Interviewers often ask you to explain the reasoning, not just write the formula.

______________________________________________________________________

## Mistake 4

Memorizing the expression.

Instead,

remember this rule:

> **Every power of two has exactly one set bit.**

The formula naturally follows.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A straightforward solution repeatedly divides the number by two until reaching one or finding an odd remainder. A more efficient solution observes that powers of two have exactly one set bit in binary. Therefore, for any positive power of two, `n & (n - 1)` clears that single set bit and produces zero."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why does `n & (n - 1)` work?**

Because subtracting one flips the only set bit to zero and all lower bits to one. Their AND becomes zero.

______________________________________________________________________

**Q. Why check `n > 0`?**

Because `0` is not a power of two, even though `0 & -1` equals `0`.

______________________________________________________________________

**Q. Is `1` a power of two?**

Yes.

```
1 = 2⁰
```

______________________________________________________________________

**Q. Where is this useful in backend engineering?**

- Memory allocation
- Hash table sizes
- Buffer alignment
- Feature flags
- Permission masks
- Network protocols

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Bit Manipulation |
| Recognition | Power of Two / Binary |
| Brute Force | Divide by 2 |
| Optimized | `n & (n - 1)` |
| Time | O(1) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Powers of two have exactly one set bit.
- Brute force repeatedly divides by 2.
- Optimized solution uses `n & (n - 1)`.
- Always check `number > 0`.
- `&` is a bitwise operator, not a logical operator.
- The optimized solution runs in constant time.
- This pattern is commonly used in systems programming and backend infrastructure.

______________________________________________________________________

# Practice Questions

## Easy

1. Number of 1 Bits
1. Counting Bits
1. Power of Four

______________________________________________________________________

## Medium

4. Single Number
1. Missing Number
1. Bitwise AND of Numbers Range
1. Reverse Bits

______________________________________________________________________

## Hard (Optional)

8. Maximum XOR of Two Numbers in an Array
1. Minimum One Bit Operations to Make Integers Zero
1. Trie + XOR Problems

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is that **understanding the binary representation of numbers can completely change
your solution**. What starts as a looping problem becomes a constant-time solution with a single bitwise expression.
This is one of the most frequently used and recognized bit manipulation patterns in technical interviews.

______________________________________________________________________

# Next

[09-linear-search.md](09-linear-search.md)
