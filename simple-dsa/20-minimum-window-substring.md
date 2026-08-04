# 20-minimum-window-substring.md

# Minimum Window Substring — The Most Important Sliding Window Problem

## Interview Confidence

**Difficulty:** ⭐⭐⭐⭐⭐

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 30–35 minutes

**Revision Time:** 10 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given two strings:

- `s`
- `t`

Return the **smallest substring** of `s` that contains **all characters of `t`**, including duplicates.

If no such substring exists, return an empty string.

### Example

```text
Input

s = "ADOBECODEBANC"

t = "ABC"

Output

"BANC"
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> Find the **shortest continuous substring** that contains all required characters.

Notice:

The order doesn't matter.

Duplicates do matter.

Example

```text
t = "AABC"
```

A valid window must contain

```text
A → 2

B → 1

C → 1
```

______________________________________________________________________

# Real-World Analogy

Suppose you're searching server logs.

Required events:

```text
LOGIN
PAYMENT
LOGOUT
```

You want the **smallest time interval** containing all three events.

This is exactly the Minimum Window problem.

Other examples:

- Search engines
- Log analysis
- DNA sequence matching
- Event correlation
- Fraud detection

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Minimum substring
- Contains all characters
- Shortest window
- Continuous sequence

Think:

```text
Variable Sliding Window

+

Frequency Counting
```

______________________________________________________________________

# Key Insight

Unlike previous Sliding Window problems,

this one has **two phases**.

## Phase 1

Expand the window until it becomes valid.

## Phase 2

Shrink the window as much as possible while keeping it valid.

This cycle repeats.

______________________________________________________________________

# Window Invariant

The window is valid if:

> It contains every required character with the required frequency.

Unlike previous problems,

the condition isn't about uniqueness or length.

It's about satisfying required counts.

______________________________________________________________________

# Visual Explanation

Input

```text
ADOBECODEBANC
```

Need

```text
A

B

C
```

Expand

```text
ADOBEC
```

Window becomes valid.

Now shrink.

```text
DOBEC
```

Lost

```text
A
```

Invalid.

Expand again.

Eventually

```text
BANC
```

Valid.

Try shrinking.

Cannot.

Best answer found.

______________________________________________________________________

# Step-by-Step Algorithm

1. Count frequencies of `t`.
1. Expand right pointer.
1. Track how many required characters are satisfied.
1. When window becomes valid:
   - Update best answer.
   - Shrink from left.
1. Continue.

______________________________________________________________________

# Understanding "Satisfied"

Suppose

```text
t

AABC
```

Need

```text
A →2

B →1

C →1
```

Window

```text
AABC
```

Satisfied.

Window

```text
ABBC
```

Not satisfied.

Only one A.

The algorithm tracks how many required frequencies have been fulfilled.

______________________________________________________________________

# Dry Run

```text
s

ADOBECODEBANC

t

ABC
```

Expand

```text
ADOBEC
```

Valid.

Length

```text
6
```

Shrink.

Lose

```text
A
```

Invalid.

Expand again.

Eventually

```text
BANC
```

Length

```text
4
```

Best answer.

______________________________________________________________________

# Why This Works

The right pointer only expands.

The left pointer only shrinks.

Every character enters once.

Every character leaves once.

The smallest valid window is discovered because we always shrink whenever possible.

______________________________________________________________________

# Edge Cases

## Empty Strings

Return

```text
""
```

______________________________________________________________________

## t Longer Than s

Impossible.

Return

```text
""
```

______________________________________________________________________

## No Valid Window

Return

```text
""
```

______________________________________________________________________

## Duplicate Characters

```text
t = AABC
```

Need both As.

Frequency matters.

______________________________________________________________________

# Complexity Analysis

## Time

Each pointer moves at most

```text
n
```

times.

Overall

```text
O(n)
```

______________________________________________________________________

## Space

Frequency maps.

```text
O(k)
```

where

```text
k
```

is the number of distinct characters.

______________________________________________________________________

# Production-Quality Python

```python
from collections import Counter, defaultdict


def min_window(s: str, t: str) -> str:
    """
    Returns the minimum substring containing
    every character of t.

    Time Complexity: O(n)
    Space Complexity: O(k)
    """

    if not s or not t:
        return ""

    target = Counter(t)
    window = defaultdict(int)

    required = len(target)
    formed = 0

    left = 0

    best_length = float("inf")
    best_left = 0

    for right, char in enumerate(s):
        window[char] += 1

        if char in target and window[char] == target[char]:
            formed += 1

        while formed == required:
            if right - left + 1 < best_length:
                best_length = right - left + 1
                best_left = left

            left_char = s[left]
            window[left_char] -= 1

            if (
                left_char in target
                and window[left_char] < target[left_char]
            ):
                formed -= 1

            left += 1

    if best_length == float("inf"):
        return ""

    return s[best_left : best_left + best_length]
```

______________________________________________________________________

# Common Mistakes

## 1. Using a Fixed Window

The answer length is unknown.

The window must expand and shrink.

______________________________________________________________________

## 2. Tracking Only Unique Characters

Wrong.

Need frequencies.

Example

```text
AABC
```

Two As are required.

______________________________________________________________________

## 3. Forgetting to Shrink

Many candidates expand correctly but never minimize the window.

______________________________________________________________________

## 4. Updating the Best Window Too Late

Always update the answer **before** shrinking invalidates the window.

______________________________________________________________________

# Variations

## Medium

- Find All Anagrams in a String
- Permutation in String

______________________________________________________________________

## Hard

- Substring with Concatenation of All Words
- Smallest Range Covering Elements from K Lists

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Recognize a variable Sliding Window.
1. Count required characters.
1. Expand until valid.
1. Shrink while valid.
1. Record the smallest valid window.
1. Continue until the end.

______________________________________________________________________

### Common Follow-ups

### Q: Why use `formed`?

Instead of comparing the entire frequency map after every move, `formed` tells us when all required character counts are
satisfied.

______________________________________________________________________

### Q: Why is this O(n)?

Both pointers only move forward.

Each character is added and removed at most once.

______________________________________________________________________

### Q: Why can't we use a fixed window?

Because we don't know the size of the smallest valid substring beforehand.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Variable Sliding Window |
| Recognition | Minimum substring containing target |
| Invariant | All required frequencies satisfied |
| Time | O(n) |
| Space | O(k) |

______________________________________________________________________

# Practice Problems

## Medium

1. Find All Anagrams in a String
1. Permutation in String
1. Minimum Size Subarray Sum
1. Subarrays with K Different Integers

## Hard

1. Substring with Concatenation of All Words
1. Smallest Range Covering Elements from K Lists

______________________________________________________________________

# Quick Revision

- Variable Sliding Window.
- Count required frequencies.
- Expand until valid.
- Shrink while still valid.
- Update answer before breaking validity.
- Use `formed` to avoid repeated full-map comparisons.
- Time: **O(n)**
- Space: **O(k)**

______________________________________________________________________

# Key Takeaway

This is widely considered the **hardest classic Sliding Window interview problem** because it combines:

- Frequency counting
- Expand–shrink logic
- Window validity
- Window minimization

Master this problem, and you'll understand the majority of advanced Sliding Window interview questions.

______________________________________________________________________

# Navigation

**Previous**

[19-longest-repeating-character-replacement.md](19-longest-repeating-character-replacement.md)

**Next**

[21-stack.md](21-stack.md)
