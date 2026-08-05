# 02-palindrome-number.md

# Palindrome Number

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

This problem looks very similar to **Reverse Number**, but interviewers are testing something different.

They want to know whether you can:

- Reuse an existing idea
- Think before writing code
- Identify edge cases
- Compare different approaches
- Optimize instead of blindly coding

Many beginners immediately start writing code. Good candidates first realize:

> "If I can reverse a number, I can compare it with the original."

That realization is what interviewers are looking for.

______________________________________________________________________

# Problem Statement

Given an integer, determine whether it is a palindrome.

A palindrome reads the same from left to right and right to left.

Return:

- `True` if it is a palindrome.
- `False` otherwise.

______________________________________________________________________

## Example 1

```text
Input:
121

Output:
True
```

______________________________________________________________________

## Example 2

```text
Input:
123

Output:
False
```

______________________________________________________________________

## Example 3

```text
Input:
1221

Output:
True
```

______________________________________________________________________

# Simple English

A palindrome is something that looks identical even after reversing.

Example:

```
121

↓

121
```

Same number.

Another example:

```
123

↓

321
```

Different.

Therefore,

```
123

is NOT a palindrome.
```

______________________________________________________________________

# Common Misunderstandings

Many people think:

> "Palindrome means even number of digits."

Wrong.

These are all palindromes:

```
7

11

121

1221

12321
```

Odd or even digits doesn't matter.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a distributed system generates request IDs.

Some monitoring system marks IDs as **special** if they remain identical after reversing.

```
1221

↓

1221

Valid
```

Instead of comparing characters, we compare the numeric representation.

This is similar to checksum verification or validation rules in backend services.

______________________________________________________________________

# Pattern Recognition

Pattern:

**Digit Extraction**

Recognition clues:

Whenever you see:

- Reverse Number
- Palindrome Number
- Armstrong Number
- Sum of Digits
- Count Digits

Think:

```
digit = number % 10

number = number // 10
```

Exactly the same pattern as the previous lesson.

______________________________________________________________________

# Brute Force Solution

## Intuition

Reverse the number.

Compare it with the original.

If both are equal,

it's a palindrome.

______________________________________________________________________

## Algorithm

```
Store original number

↓

Reverse the number

↓

Compare

↓

Equal?

↓

True

Else

False
```

______________________________________________________________________

## Dry Run

Input

```
1221
```

Reverse

```
1221

↓

1221
```

Compare

```
1221 == 1221

True
```

______________________________________________________________________

Input

```
1234
```

Reverse

```
1234

↓

4321
```

Compare

```
1234 == 4321

False
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
O(1)
```

if reversed using arithmetic.

```
O(d)
```

if converted to string.

______________________________________________________________________

## Limitations

We reverse the **entire** number.

Can we do less work?

Yes.

That leads to the optimized solution.

______________________________________________________________________

# Optimized Solution

## Key Insight

To determine whether something is a palindrome,

we don't need to reverse the **entire** number.

We only need to compare:

- Left half
- Right half

For numbers,

we can reverse only the last half.

This avoids unnecessary work and also avoids overflow in languages like Java or C++.

______________________________________________________________________

## Step-by-Step Algorithm

Example

```
12321
```

Initial

```
Left Side

123

Right Side

21
```

Reverse only the right side.

Iteration 1

```
Number

12321

Digit

1

Half Reverse

1

Remaining

1232
```

Iteration 2

```
Digit

2

Half Reverse

12

Remaining

123
```

Stop because

```
Remaining <= Half Reverse
```

Now compare

```
123

12
```

Since this is an odd-length number,

remove the middle digit.

```
12 == 12
```

Palindrome.

______________________________________________________________________

# Visual Explanation

Example

```
1221
```

```
Original

1 2 | 2 1
      ↑

Reverse right half

1 2

Compare

12 == 12

Palindrome
```

Example

```
12321
```

```
1 2 3 | 2 1
        ↑

Reverse

12

Remaining

123

Remove middle digit

123 // 10

↓

12

Compare

12 == 12
```

______________________________________________________________________

# Why This Works

Every iteration moves one digit

from

```
Original Number
```

to

```
Reversed Half
```

Eventually,

the reversed half contains exactly half of the digits.

For

Even digits

```
1221

↓

12

12
```

Compare directly.

For

Odd digits

```
12321

↓

123

12
```

Ignore the middle digit.

```
123 // 10

↓

12
```

Compare again.

______________________________________________________________________

# Edge Cases

### Zero

```
0

↓

Palindrome
```

______________________________________________________________________

### Single Digit

```
8

↓

Palindrome
```

______________________________________________________________________

### Negative Number

```
-121
```

Not a palindrome.

Reason:

```
-

appears only on one side.
```

______________________________________________________________________

### Ending With Zero

Example

```
120
```

Reverse

```
021

↓

21
```

Not equal.

Any positive number ending in zero cannot be a palindrome.

Only

```
0
```

itself is valid.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(d)
```

Space

```
O(1)
```

______________________________________________________________________

## Optimized

Time

```
O(d/2)

≈ O(d)
```

Space

```
O(1)
```

The optimized solution processes only half the digits.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
def is_palindrome(number: int) -> bool:
    if number < 0:
        return False

    original = number
    reversed_number = 0

    while number > 0:
        digit = number % 10
        reversed_number = reversed_number * 10 + digit
        number //= 10

    return original == reversed_number
```

______________________________________________________________________

## Optimized

```python
def is_palindrome(number: int) -> bool:
    if number < 0:
        return False

    if number != 0 and number % 10 == 0:
        return False

    reversed_half = 0

    while number > reversed_half:
        digit = number % 10
        reversed_half = reversed_half * 10 + digit
        number //= 10

    return (
        number == reversed_half
        or number == reversed_half // 10
    )
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using strings immediately.

Works,

but interviewers usually expect arithmetic.

______________________________________________________________________

## Mistake 2

Ignoring negative numbers.

```
-121
```

is never a palindrome.

______________________________________________________________________

## Mistake 3

Forgetting numbers ending in zero.

```
10

↓

01

↓

1
```

Not equal.

______________________________________________________________________

## Mistake 4

Comparing before handling odd-length numbers.

Remember:

```
12321

↓

Remove middle digit first.
```

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The simplest approach is reversing the number and comparing it with the original. However, since we only need to compare both halves, we can reverse only half of the digits, reducing unnecessary work and avoiding overflow in fixed-width integer languages."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why not convert to string?**

Because interviewers often want arithmetic manipulation.

______________________________________________________________________

**Q. Why reverse only half?**

Because the first half never changes.

Only one side needs reversing.

______________________________________________________________________

**Q. Why check trailing zeros?**

Numbers ending with zero cannot start with zero after reversal.

______________________________________________________________________

**Q. Why ignore the middle digit?**

The middle digit doesn't affect whether the number reads the same from both directions.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Digit Extraction |
| Recognition | Reverse / Palindrome / Digit Problems |
| Key Operations | `% 10`, `// 10` |
| Brute Force | Reverse Entire Number |
| Optimized | Reverse Half the Number |
| Time | O(d) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- A palindrome reads the same forwards and backwards.
- Reverse-and-compare is the easiest solution.
- Use `% 10` to extract digits.
- Use `// 10` to remove digits.
- Negative numbers are never palindromes.
- Numbers ending in zero (except 0) are never palindromes.
- Optimized solution reverses only half the digits.
- Both solutions use constant extra space.

______________________________________________________________________

# Practice Questions

## Easy

1. Reverse Integer
1. Count Digits
1. Sum of Digits
1. Happy Number

______________________________________________________________________

## Medium

5. Reverse Integer (Overflow Handling)
1. Add Digits
1. Plus One
1. Integer to Roman

______________________________________________________________________

## Hard (Optional)

9. Nearest Palindrome
1. Super Palindromes

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is recognizing when you **don't need to process the entire input**. By reversing
only half the digits, you solve the problem with the same asymptotic complexity but a cleaner, more efficient approach
that scales well to languages with fixed-size integers.

______________________________________________________________________

# Next

[03-prime-number.md](03-prime-number.md)
