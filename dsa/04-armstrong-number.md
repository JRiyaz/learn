# 04-armstrong-number.md

# Armstrong Number

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | Medium |
| Importance | ⭐⭐⭐☆☆ |
| Expected Interview Time | 10–15 minutes |
| Revision Time | 5 minutes |

______________________________________________________________________

# Why Interviewers Ask This

At first glance, Armstrong Number looks like a mathematics problem.

It actually tests whether you understand:

- Digit extraction
- Counting digits
- Reusing previous patterns
- Breaking a problem into smaller steps
- Writing clean iterative code

This question is less about mathematics and more about whether you can manipulate the digits of a number correctly.

______________________________________________________________________

# Problem Statement

An **Armstrong Number** (also called a Narcissistic Number) is a number that is equal to the **sum of each digit raised
to the power of the total number of digits**.

If

```
Number = n
```

contains

```
d digits
```

then

```
Armstrong if

digit1^d + digit2^d + ... + digitN^d == number
```

Return:

- `True` if the number is an Armstrong Number.
- `False` otherwise.

______________________________________________________________________

## Example 1

```text
Input:
153

Output:
True
```

Why?

```
1³ + 5³ + 3³

=

1 + 125 + 27

=

153
```

______________________________________________________________________

## Example 2

```text
Input:
123

Output:
False
```

```
1³ + 2³ + 3³

=

1 + 8 + 27

=

36

≠ 123
```

______________________________________________________________________

## Example 3

```text
Input:
9474

Output:
True
```

```
9⁴ + 4⁴ + 7⁴ + 4⁴

=

6561
+256
+2401
+256

=

9474
```

______________________________________________________________________

# Simple English

Imagine every digit contributes some "energy."

Raise each digit to the power of the total digits.

Add all the energies.

If the total becomes the original number,

it is an Armstrong Number.

______________________________________________________________________

# Common Misunderstandings

Many beginners think:

```
153

↓

1² + 5² + 3²
```

Wrong.

The exponent is **NOT fixed**.

It depends on the number of digits.

Examples

```
153

3 digits

↓

Power = 3
```

```
9474

4 digits

↓

Power = 4
```

______________________________________________________________________

# Backend Engineering Analogy

Imagine a backend validation system.

Every digit in an ID contributes a weighted score.

```
Digit Score

=

digit ^ total_digits
```

If the final score equals the original ID,

the record is considered valid.

This resembles:

- Checksum validation
- Hash verification
- Weighted scoring systems
- Data integrity checks

______________________________________________________________________

# Pattern Recognition

### Pattern

**Digit Extraction + Aggregation**

Recognition clues

Whenever you see

- Sum of digits
- Product of digits
- Reverse digits
- Armstrong Number
- Happy Number

Think

```python
digit = number % 10
number //= 10
```

______________________________________________________________________

# Brute Force Solution

## Intuition

The easiest solution is:

1. Convert number into a string.
1. Count digits.
1. Convert every character back into an integer.
1. Raise it to the required power.
1. Add everything.
1. Compare with original.

______________________________________________________________________

## Algorithm

```
153

↓

"153"

↓

Length = 3

↓

1³ + 5³ + 3³

↓

153

↓

Equal

↓

True
```

______________________________________________________________________

## Dry Run

Input

```
9474
```

Convert to string

```
"9474"
```

Length

```
4
```

Compute

```
9⁴ = 6561

4⁴ = 256

7⁴ = 2401

4⁴ = 256
```

Total

```
9474
```

Equal to original

```
True
```

______________________________________________________________________

## Complexity

Time

```
O(d)
```

where

```
d = number of digits
```

Space

```
O(d)
```

because the string occupies extra memory.

______________________________________________________________________

## Limitations

Although simple,

this solution converts the number into another data type.

Interviewers often ask:

> Can you solve it using arithmetic only?

______________________________________________________________________

# Optimized Solution

## Key Insight

We already know how to process digits.

Use

```python
% 10
```

to extract the last digit.

Use

```python
// 10
```

to remove it.

Raise every extracted digit to the required power and keep adding.

No string conversion needed.

______________________________________________________________________

## Step-by-Step Algorithm

Example

```
153
```

Digit count

```
3
```

Initialize

```
sum = 0
```

______________________________________________________________________

Iteration 1

```
153

↓

digit = 3

↓

3³ = 27

↓

sum = 27

↓

number = 15
```

______________________________________________________________________

Iteration 2

```
15

↓

digit = 5

↓

125

↓

sum = 152

↓

number = 1
```

______________________________________________________________________

Iteration 3

```
1

↓

digit = 1

↓

1

↓

sum = 153
```

Compare

```
153 == 153

↓

True
```

______________________________________________________________________

# Visual Explanation

```
Original

153


Extract

3

↓

3³ = 27

↓

Sum = 27


Extract

5

↓

125

↓

Sum = 152


Extract

1

↓

1

↓

Sum = 153
```

Final

```
153 == Original

✔ Armstrong Number
```

______________________________________________________________________

# Why This Works

Every digit contributes independently.

Since every digit is processed exactly once,

the total becomes

```
digit₁^d
+
digit₂^d
+
...
+
digitₙ^d
```

If that total equals the original number,

the definition of an Armstrong Number is satisfied.

______________________________________________________________________

# Edge Cases

### Zero

```
0

↓

0¹

↓

0

↓

True
```

______________________________________________________________________

### Single Digit

```
7

↓

7¹

↓

7

↓

True
```

Every single-digit number is an Armstrong Number.

______________________________________________________________________

### Large Numbers

Still works correctly.

The only additional work is computing larger powers.

______________________________________________________________________

### Negative Numbers

Traditionally,

negative numbers are **not** considered Armstrong Numbers.

Return

```
False
```

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(d)
```

Space

```
O(d)
```

______________________________________________________________________

## Optimized

Time

```
O(d)
```

Space

```
O(1)
```

Only a few integer variables are used.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
def is_armstrong(number: int) -> bool:
    if number < 0:
        return False

    digits = str(number)
    power = len(digits)

    total = sum(int(digit) ** power for digit in digits)

    return total == number
```

______________________________________________________________________

## Optimized

```python
def is_armstrong(number: int) -> bool:
    if number < 0:
        return False

    original = number
    total = 0

    # Count digits
    digit_count = len(str(number))

    while number > 0:
        digit = number % 10
        total += digit ** digit_count
        number //= 10

    return total == original
```

> **Note:** We still use `len(str(number))` to count digits because counting digits arithmetically would require another loop. In interviews, this is usually acceptable unless the interviewer explicitly asks for a pure arithmetic solution.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using a fixed exponent.

Wrong

```python
digit ** 3
```

Correct

```python
digit ** number_of_digits
```

______________________________________________________________________

## Mistake 2

Forgetting to save the original number.

Once digits are removed,

the original value is lost.

Always write

```python
original = number
```

______________________________________________________________________

## Mistake 3

Using

```python
digit * digit_count
```

instead of

```python
digit ** digit_count
```

______________________________________________________________________

## Mistake 4

Not handling

```
0
```

correctly.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The straightforward solution is to convert the number to a string, determine the number of digits, compute the required powers, and compare the sum with the original number. If arithmetic manipulation is preferred, I can extract digits using `% 10` and `// 10` while computing the same sum."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why store the original number?**

Because the working number becomes 0 after digit extraction.

______________________________________________________________________

**Q. Can this be solved without strings?**

Yes.

Count digits arithmetically first, then process digits again.

______________________________________________________________________

**Q. Why is every single-digit number an Armstrong Number?**

Because

```
digit¹ = digit
```

______________________________________________________________________

**Q. Why is 9474 an Armstrong Number?**

Because

```
9⁴ + 4⁴ + 7⁴ + 4⁴ = 9474
```

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Digit Extraction + Aggregation |
| Recognition | Sum of Digit Powers |
| Key Operations | `% 10`, `// 10`, `**` |
| Brute Force | String Traversal |
| Optimized | Arithmetic Digit Extraction |
| Time | O(d) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Armstrong Number depends on the **number of digits**.
- Extract digits using `% 10`.
- Remove digits using `// 10`.
- Raise every digit to the power of total digits.
- Add all powers.
- Compare with the original number.
- Store the original before modifying it.
- Single-digit numbers are always Armstrong Numbers.
- Arithmetic solution uses constant extra space.

______________________________________________________________________

# Practice Questions

## Easy

1. Count Digits
1. Sum of Digits
1. Reverse Number
1. Palindrome Number

______________________________________________________________________

## Medium

5. Happy Number
1. Plus One
1. Add Digits
1. Harshad Number

______________________________________________________________________

## Hard (Optional)

9. Powerful Integers
1. Count Special Integers

______________________________________________________________________

# Key Takeaway

Armstrong Number reinforces one of the most important interview patterns: **digit extraction**. Once you're comfortable
repeatedly extracting digits with `% 10` and removing them with `// 10`, you'll be able to solve an entire family of
number-based interview questions with confidence.

______________________________________________________________________

# Next

[05-factorial.md](05-factorial.md)
