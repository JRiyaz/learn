# 01-reverse-number.md

# Reverse Number

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

At first glance, reversing a number looks like a simple math problem.

It isn't.

Interviewers use this problem to check whether you understand:

- Integer arithmetic
- Modulus (`%`)
- Integer division (`//`)
- Loops
- Building a result digit by digit
- Thinking algorithmically instead of relying on shortcuts

Many beginners immediately convert the integer into a string. While that works in Python, interviewers usually want to
know whether you understand **how numbers actually work**.

______________________________________________________________________

# Problem Statement

Given an integer, reverse its digits.

### Example 1

```text
Input:
12345

Output:
54321
```

### Example 2

```text
Input:
9070

Output:
709
```

Notice the leading zero disappears because integers don't store leading zeros.

______________________________________________________________________

# Simple English

Imagine someone writes a number on paper.

Your task is to write the digits in reverse order.

```
12345

↓

54321
```

______________________________________________________________________

# What is Actually Being Asked?

The interviewer wants to know:

> Can you extract digits one at a time and rebuild the number?

______________________________________________________________________

# Backend Engineering Analogy

Suppose your logging system generates IDs:

```
123456
```

Now another service stores digits in reverse order for compression or encoding.

Instead of manipulating strings, you process one digit at a time.

Many serialization, encoding, checksum and parsing algorithms work similarly.

______________________________________________________________________

# Pattern Recognition

### Pattern

**Digit Extraction**

### Recognition Clues

Whenever you see:

- Reverse digits
- Count digits
- Sum digits
- Check palindrome number
- Armstrong number

Think:

```
digit = n % 10
n = n // 10
```

This pattern appears repeatedly in interview questions.

______________________________________________________________________

# Brute Force Solution

## Intuition

The easiest solution is:

1. Convert number to string
1. Reverse string
1. Convert back to integer

Python makes this very easy.

______________________________________________________________________

## Algorithm

```
12345

↓

"12345"

↓

"54321"

↓

54321
```

______________________________________________________________________

## Dry Run

```
Input

12345

↓

Convert to string

"12345"

↓

Reverse

"54321"

↓

Convert back

54321
```

______________________________________________________________________

## Complexity

Time:

```
O(n)
```

where n = number of digits

Space:

```
O(n)
```

because a new string is created.

______________________________________________________________________

## Limitations

Interviewers usually ask:

> Can you do it **without converting to a string?**

That's where the optimized approach comes in.

______________________________________________________________________

# Optimized Solution

## Key Insight

Instead of reversing characters,

reverse **digits**.

Every iteration:

- Take last digit
- Append it to answer
- Remove last digit from original number

______________________________________________________________________

## Step 1

Take last digit.

```
digit = number % 10
```

Example

```
12345 % 10

=

5
```

______________________________________________________________________

## Step 2

Append digit to answer.

Current answer:

```
0
```

After adding 5

```
answer = answer * 10 + digit

0 * 10 + 5

=

5
```

______________________________________________________________________

## Step 3

Remove last digit.

```
number = number // 10
```

```
12345

↓

1234
```

______________________________________________________________________

## Repeat

Continue until

```
number == 0
```

______________________________________________________________________

# Complete Dry Run

Input

```
12345
```

| Number | Digit | Answer |
|---------|-------|---------|
|12345|5|5|
|1234|4|54|
|123|3|543|
|12|2|5432|
|1|1|54321|
|0|-|Done|

Final answer

```
54321
```

______________________________________________________________________

# Visual Explanation

```
number = 12345

Iteration 1

12345

      ↑
      5

answer

0

↓

5


Iteration 2

1234

     ↑
     4

answer

5

↓

54


Iteration 3

123

    ↑
    3

↓

543


Iteration 4

12

   ↑
   2

↓

5432


Iteration 5

1

↑
1

↓

54321
```

______________________________________________________________________

# Why This Works

Each iteration removes exactly one digit.

```
12345

↓

1234

↓

123

↓

12

↓

1

↓

0
```

At the same time,

every extracted digit becomes the next digit of the answer.

The invariant is:

> After every iteration, `answer` contains the reverse of all processed digits.

______________________________________________________________________

# Edge Cases

### Single Digit

```
7

↓

7
```

______________________________________________________________________

### Zero

```
0

↓

0
```

______________________________________________________________________

### Trailing Zeros

```
1200

↓

21
```

Integers don't keep leading zeros.

______________________________________________________________________

### Very Large Numbers

Works correctly because Python integers have arbitrary precision.

______________________________________________________________________

### Negative Numbers (if interviewer asks)

```
-123

↓

-321
```

Handle sign separately.

______________________________________________________________________

# Complexity Analysis

### Time Complexity

There is one iteration per digit.

```
O(d)
```

where

```
d = number of digits
```

______________________________________________________________________

### Space Complexity

Only three variables are used.

```
number
digit
answer
```

Therefore

```
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
def reverse_number(number: int) -> int:
    """Return the reversed form of a non-negative integer."""

    reversed_number = 0

    while number > 0:
        digit = number % 10
        reversed_number = reversed_number * 10 + digit
        number //= 10

    return reversed_number


if __name__ == "__main__":
    print(reverse_number(12345))
```

______________________________________________________________________

# Common Mistakes

### Mistake 1

Using

```python
/
```

instead of

```python
//
```

This creates floating-point values.

______________________________________________________________________

### Mistake 2

Forgetting

```python
answer *= 10
```

Without multiplying by 10, digits won't shift left.

______________________________________________________________________

### Mistake 3

Updating the number before extracting the digit.

Wrong:

```python
number //= 10
digit = number % 10
```

Always extract first.

______________________________________________________________________

### Mistake 4

Ignoring negative numbers if the interviewer explicitly mentions them.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "A straightforward solution is converting the number to a string and reversing it. However, that uses extra space. Since interviewers often expect arithmetic manipulation, I'll extract digits using modulus, build the reversed number, and remove processed digits using integer division."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use `% 10`?**

It extracts the last digit.

______________________________________________________________________

**Q. Why multiply by 10?**

To shift existing digits left before appending the next digit.

______________________________________________________________________

**Q. Can this overflow?**

In Python, no.

In Java/C++, overflow checks may be required.

______________________________________________________________________

**Q. Can you solve it recursively?**

Yes, but the iterative solution is simpler and uses constant extra space.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Digit Extraction |
| Recognition | Reverse / Sum / Count Digits |
| Key Operations | `% 10`, `// 10` |
| Time | O(d) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Reverse numbers using arithmetic, not strings.
- `% 10` extracts the last digit.
- `// 10` removes the last digit.
- Multiply the answer by 10 before appending a new digit.
- Process digits until the number becomes 0.
- Time complexity is O(d).
- Space complexity is O(1).
- This pattern is reused in palindrome, Armstrong, and digit-sum problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Palindrome Number
1. Count Digits
1. Sum of Digits
1. Add Digits

## Medium

5. Reverse Integer (LeetCode 7)
1. Plus One
1. Largest Number
1. Maximum Swap

## Hard (Optional)

9. Integer to English Words
1. Smallest Good Base

______________________________________________________________________

# Key Takeaway

Whenever you need to process the digits of an integer, think in terms of repeatedly extracting the last digit with `%
10`, processing it, and removing it with `// 10`. This simple pattern forms the foundation for many number-based
interview problems.

______________________________________________________________________

# Next

[02-palindrome-number.md](02-palindrome-number.md)
