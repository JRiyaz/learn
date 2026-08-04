# 13-valid-palindrome.md

# Valid Palindrome — Learning Inward Two Pointer Traversal

## Interview Confidence

**Difficulty:** ⭐⭐☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐☆

**Expected Interview Time:** 15 minutes

**Revision Time:** 3 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given a string `s`, return `True` if it is a palindrome, otherwise return `False`.

Rules:

- Ignore non-alphanumeric characters.
- Ignore uppercase/lowercase differences.

### Example 1

```text
Input

"A man, a plan, a canal: Panama"

Output

True
```

Because after cleaning:

```text
amanaplanacanalpanama
```

which reads the same forwards and backwards.

______________________________________________________________________

### Example 2

```text
Input

"race a car"

Output

False
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is **not** asking you to compare the original string.

They're asking you to compare the **normalized** string.

Normalization means:

- Ignore spaces
- Ignore punctuation
- Ignore case

______________________________________________________________________

# Real-World Analogy

Suppose you're building a search engine.

Users search:

```text
ChatGPT

chatgpt

CHATGPT

Chat-GPT
```

Internally, the search engine normalizes the text before comparison.

Likewise, in this problem we normalize characters before checking symmetry.

Other examples:

- Username validation
- URL normalization
- Text search
- Duplicate detection

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Palindrome
- Compare from both ends
- Ignore characters
- Symmetry

Immediately think:

> **Opposite Direction Two Pointers**

______________________________________________________________________

# Brute Force Solution

## Intuition

Create a cleaned string.

Reverse it.

Compare.

Example

```text
madam

↓

madam[::-1]

↓

madam
```

Works.

______________________________________________________________________

## Complexity

Cleaning

```text
O(n)
```

Reverse

```text
O(n)
```

Comparison

```text
O(n)
```

Overall

```text
Time  : O(n)
Space : O(n)
```

Extra memory is required.

______________________________________________________________________

# Optimal Solution

## Key Insight

We don't need another string.

Instead,

compare characters directly from both ends.

```text
m a d a m

↑       ↑
```

If characters match,

move inward.

```text
  ↑   ↑
```

Continue until pointers cross.

______________________________________________________________________

# Handling Special Characters

Suppose

```text
A man, a plan!
```

When the left pointer sees:

```text
' '
```

Skip it.

When the right pointer sees:

```text
','
```

Skip it.

Only compare letters and digits.

______________________________________________________________________

# Visual Explanation

```text
A man, a plan, a canal: Panama

↑                             ↑

A == a

Move
```

Skip spaces

```text
m == m

Move
```

Skip comma

```text
a == a

Move
```

Continue...

Eventually

```text
Pointers Cross

↓

Palindrome
```

______________________________________________________________________

# Step-by-Step Algorithm

Initialize

```text
left = 0

right = len(s)-1
```

While

```text
left < right
```

Skip invalid characters.

Convert both characters to lowercase.

Compare.

If different

Return False.

Otherwise

Move both pointers inward.

Return True.

______________________________________________________________________

# Why This Works

A palindrome is perfectly symmetric.

Every character on the left must match the corresponding character on the right.

If even one pair differs,

the string cannot be a palindrome.

By comparing from the outside inward,

every character is examined only once.

______________________________________________________________________

# Dry Run

Input

```text
"Aba"
```

Pointers

```text
A b a

↑   ↑
```

Lowercase

```text
a == a
```

Move

```text
  ↑
```

Pointers meet.

Return

```text
True
```

______________________________________________________________________

Another Example

```text
race a car
```

Compare

```text
r == r
```

Move

Compare

```text
a == a
```

Move

Compare

```text
c != e
```

Return

```text
False
```

______________________________________________________________________

# Edge Cases

## Empty String

```text
""
```

A palindrome.

______________________________________________________________________

## Only Spaces

```text
"   "
```

After normalization

```text
""
```

Palindrome.

______________________________________________________________________

## Only Symbols

```text
"!@#$"
```

No valid characters.

Palindrome.

______________________________________________________________________

## One Character

Always palindrome.

______________________________________________________________________

## Mixed Case

```text
RaceCar
```

Palindrome.

______________________________________________________________________

# Complexity Analysis

## Time

Each pointer moves at most once across the string.

```text
O(n)
```

______________________________________________________________________

## Space

Only two pointers.

```text
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
def is_palindrome(s: str) -> bool:
    """
    Returns True if the string is a valid palindrome.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    left = 0
    right = len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1

        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

______________________________________________________________________

# Alternative Solution

Normalize first.

```python
clean = "".join(c.lower() for c in s if c.isalnum())

return clean == clean[::-1]
```

### Complexity

```text
Time  : O(n)

Space : O(n)
```

Cleaner,

but uses extra memory.

______________________________________________________________________

# Common Mistakes

## 1. Forgetting to Ignore Symbols

Wrong

```text
"A man, a plan..."
```

Spaces and commas must be skipped.

______________________________________________________________________

## 2. Forgetting Case Conversion

```text
A != a
```

Convert to lowercase.

______________________________________________________________________

## 3. Creating Multiple Temporary Strings

Works,

but wastes memory.

______________________________________________________________________

## 4. Comparing Before Skipping

Always skip invalid characters first.

______________________________________________________________________

# Variations

## Easy

- Valid Palindrome II
- Reverse String

______________________________________________________________________

## Medium

- Palindromic Substrings
- Longest Palindromic Substring
- Reverse Words in a String
- Reverse Vowels of a String

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Mention reverse-string solution.
1. Observe O(n) extra memory.
1. Recognize symmetry.
1. Introduce Two Pointers.
1. Skip invalid characters.
1. Compare lowercase letters.
1. Explain O(1) space.

______________________________________________________________________

### Common Follow-ups

### Q: Why Two Pointers?

Because the comparison naturally starts from both ends.

______________________________________________________________________

### Q: Why not reverse?

It creates another string.

Interviewers usually prefer constant space.

______________________________________________________________________

### Q: What if Unicode is involved?

The same algorithm works.

Normalization rules may vary depending on the application's requirements.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Opposite Direction Two Pointers |
| Recognition | Palindrome, symmetry |
| Brute Force | Reverse string |
| Optimal | Two Pointers |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Practice Problems

## Easy

1. Valid Palindrome II
1. Reverse String

## Medium

1. Reverse Words in a String
1. Reverse Vowels of a String
1. Longest Palindromic Substring
1. Palindromic Substrings

## Hard

1. Shortest Palindrome
1. Palindrome Pairs

______________________________________________________________________

# Quick Revision

- Palindrome = symmetry.
- Use two pointers from both ends.
- Skip non-alphanumeric characters.
- Compare lowercase characters.
- Move inward after every successful comparison.
- Time: **O(n)**
- Space: **O(1)**

______________________________________________________________________

# Key Takeaway

This problem teaches another important Two Pointer idea:

> **Two Pointers aren't only for arrays—they work equally well for strings.**

Whenever a problem asks you to compare **both ends** of a sequence, think of inward-moving pointers before considering
more complex approaches.

______________________________________________________________________

# Navigation

**Previous**

[12-two-sum-ii.md](12-two-sum-ii.md)

**Next**

[14-container-with-most-water.md](14-container-with-most-water.md)
