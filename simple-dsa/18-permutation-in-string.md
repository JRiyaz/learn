# 18-permutation-in-string.md

# Permutation in String — Fixed Sliding Window + Frequency Matching

## Interview Confidence

**Difficulty:** ⭐⭐⭐☆☆

**Asked Frequency:** ⭐⭐⭐⭐☆

**Importance:** ⭐⭐⭐⭐☆

**Expected Interview Time:** 20–25 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given two strings:

- `s1`
- `s2`

Return `True` if `s2` contains a permutation of `s1`.

A permutation means the characters can appear in **any order**.

### Example 1

```text
s1 = "ab"
s2 = "eidbaooo"

Output

True
```

Because

```text
"ba"
```

exists inside `s2`.

______________________________________________________________________

### Example 2

```text
s1 = "ab"
s2 = "eidboaoo"

Output

False
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> Does any substring of `s2` contain **exactly the same character frequencies** as `s1`?

Notice:

```text
ab

ba
```

Same frequency.

Different order.

Still valid.

______________________________________________________________________

# Real-World Analogy

Imagine a fraud detection system.

Expected transaction types:

```text
Deposit
Withdrawal
```

Incoming stream:

```text
Transfer
Deposit
Withdrawal
Refund
```

The order doesn't matter.

You only care whether a **continuous window** contains exactly the required events.

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Permutation
- Continuous substring
- Fixed length
- Same frequency

Think:

```text
Fixed Sliding Window

+

Frequency Counting
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Generate every substring of length:

```text
len(s1)
```

For each substring:

Count frequencies.

Compare with `s1`.

Example

```text
s2

e i d b a o

↓

ei

↓

id

↓

db

↓

ba
```

Compare each one.

______________________________________________________________________

## Complexity

Suppose

```text
n = len(s2)

m = len(s1)
```

Time

```text
O(n × m)
```

Too slow.

______________________________________________________________________

# Optimal Solution

## Key Insight

The window size never changes.

Window size is always:

```text
len(s1)
```

Instead of recounting frequencies every time,

update only the characters entering and leaving the window.

______________________________________________________________________

# Visual Explanation

```text
s1

ab
```

Need

```text
a → 1

b → 1
```

Window

```text
ei
```

Frequency

```text
e →1

i →1
```

Not equal.

Slide.

```text
id
```

Slide.

```text
db
```

Slide.

```text
ba
```

Frequency

```text
a →1

b →1
```

Equal.

Return

```text
True
```

______________________________________________________________________

# Step-by-Step Algorithm

1. Count characters in `s1`.
1. Build the first window.
1. Compare frequencies.
1. Slide one character.
1. Remove left character.
1. Add right character.
1. Compare again.

Repeat.

______________________________________________________________________

# Why This Works

Every valid permutation has:

- the same length
- the same character frequencies

Sliding the window avoids rebuilding frequencies from scratch.

Each step performs only:

- one removal
- one insertion

______________________________________________________________________

# Dry Run

```text
s1 = ab

s2 = eidbaooo
```

Window

```text
ei
```

Not equal.

______________________________________________________________________

Slide

```text
id
```

Not equal.

______________________________________________________________________

Slide

```text
db
```

Not equal.

______________________________________________________________________

Slide

```text
ba
```

Matches.

Return

```text
True
```

______________________________________________________________________

# Edge Cases

## s1 Longer Than s2

Impossible.

Return

```text
False
```

______________________________________________________________________

## Same Strings

```text
abc

abc
```

Return

```text
True
```

______________________________________________________________________

## Repeated Characters

```text
s1 = aab
```

Window must also contain:

```text
a →2

b →1
```

______________________________________________________________________

## Empty String

Depending on the platform's definition, an empty pattern is generally considered to be present in any string. On
LeetCode, the constraints avoid this case.

______________________________________________________________________

# Complexity Analysis

Assume lowercase English letters.

## Time

Build first window

```text
O(m)
```

Slide through string

```text
O(n)
```

Overall

```text
O(n)
```

______________________________________________________________________

## Space

Frequency arrays

```text
26
```

characters.

```text
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
from typing import List


def check_inclusion(s1: str, s2: str) -> bool:
    """
    Returns True if s2 contains
    a permutation of s1.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    if len(s1) > len(s2):
        return False

    target = [0] * 26
    window = [0] * 26

    for char in s1:
        target[ord(char) - ord("a")] += 1

    window_size = len(s1)

    for i, char in enumerate(s2):
        window[ord(char) - ord("a")] += 1

        if i >= window_size:
            left_char = s2[i - window_size]
            window[ord(left_char) - ord("a")] -= 1

        if window == target:
            return True

    return False
```

______________________________________________________________________

# Why Use Arrays Instead of Dictionaries?

The problem states:

```text
Lowercase English letters
```

Only

```text
26
```

possible characters.

Instead of

```python
{
    'a': 2,
    'b': 1
}
```

Use

```text
Index

0 -> a

1 -> b

...

25 -> z
```

Array lookup is slightly faster and uses less memory.

If the character set were Unicode or arbitrary strings, a dictionary would be more appropriate.

______________________________________________________________________

# Common Mistakes

## 1. Rebuilding Frequency Every Window

Avoid

```text
Count

↓

Compare

↓

Count Again
```

Update incrementally instead.

______________________________________________________________________

## 2. Wrong Window Size

Always

```text
len(s1)
```

______________________________________________________________________

## 3. Forgetting to Remove Left Character

The window must always represent exactly the current substring.

______________________________________________________________________

## 4. Using a Variable Window

This is a **fixed** Sliding Window problem.

______________________________________________________________________

# Variations

## Medium

- Find All Anagrams in a String
- Minimum Window Substring
- Longest Repeating Character Replacement
- Maximum Average Subarray

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Recognize fixed-length substring.
1. Count frequencies.
1. Maintain a fixed Sliding Window.
1. Update frequencies while sliding.
1. Compare counts.
1. Return as soon as a match appears.

______________________________________________________________________

### Common Follow-ups

### Q: Why is this a fixed window?

Every permutation has the same length as `s1`.

______________________________________________________________________

### Q: Why arrays instead of dictionaries?

The alphabet size is fixed (26 lowercase letters), making arrays faster and simpler.

______________________________________________________________________

### Q: Why not sort every window?

Sorting every substring would cost:

```text
O(n × m log m)
```

Much slower than maintaining rolling frequencies.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Fixed Sliding Window |
| Recognition | Fixed-length substring, permutation |
| Window Size | len(s1) |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Practice Problems

## Easy

1. Maximum Average Subarray I
1. Find All Anagrams in a String

## Medium

1. Minimum Size Subarray Sum
1. Longest Repeating Character Replacement
1. Fruit Into Baskets
1. Maximum Erasure Value

## Hard

1. Minimum Window Substring
1. Sliding Window Maximum

______________________________________________________________________

# Quick Revision

- Window size is fixed.
- Count frequencies of `s1`.
- Maintain rolling frequencies for the window.
- Remove one character.
- Add one character.
- Compare frequencies.
- Arrays are ideal because the alphabet size is fixed.
- Time: **O(n)**
- Space: **O(1)**

______________________________________________________________________

# Key Takeaway

This problem introduces the **Fixed Sliding Window** pattern.

The invariant is:

> **The window always has exactly the same size as `s1`.**

Unlike the previous lesson, the window never expands or shrinks—it only **slides**.

______________________________________________________________________

# Navigation

**Previous**

[17-longest-substring-without-repeating-characters.md](17-longest-substring-without-repeating-characters.md)

**Next**

[19-longest-repeating-character-replacement.md](19-longest-repeating-character-replacement.md)
