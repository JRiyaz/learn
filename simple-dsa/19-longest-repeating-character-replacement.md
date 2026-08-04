# 19-longest-repeating-character-replacement.md

# Longest Repeating Character Replacement — The Flexible Sliding Window Pattern

## Interview Confidence

**Difficulty:** ⭐⭐⭐⭐☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 25–30 minutes

**Revision Time:** 7 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

You are given a string `s` and an integer `k`.

You can replace **at most `k` characters** with any uppercase English letter.

Return the length of the **longest substring** that can be made of the same character.

### Example 1

```text
Input

s = "ABAB"
k = 2

Output

4
```

Replace two characters.

```text
ABAB

↓

AAAA
```

Length

```text
4
```

______________________________________________________________________

### Example 2

```text
Input

s = "AABABBA"
k = 1

Output

4
```

One valid substring is

```text
AABA

↓

AAAA
```

Length

```text
4
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> "What is the longest continuous window that can be converted into one repeated character using at most `k` replacements?"

Notice:

We are **not** actually performing replacements.

We are only checking if a window **could** be converted.

______________________________________________________________________

# Real-World Analogy

Imagine a quality-control system.

Products:

```text
A A B A B
```

You can repair only **one** defective item.

Question:

> What's the largest continuous batch that can become identical?

Exactly the same problem.

Other examples:

- Packet correction
- DNA mutation analysis
- OCR text correction
- Signal noise removal

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Longest substring
- At most K changes
- Replace
- Continuous sequence

Think:

```text
Variable Sliding Window

+

Frequency Counting
```

______________________________________________________________________

# Key Insight

Suppose the current window is

```text
A A B A
```

Frequency

```text
A → 3

B → 1
```

To make every character identical,

we only need to replace

```text
1
```

character.

General rule:

```text
Characters to replace

=

Window Size

-

Most Frequent Character
```

This formula is the heart of the problem.

______________________________________________________________________

# Why This Formula Works

Window

```text
A A B A C
```

Frequency

```text
A → 3

B → 1

C → 1
```

Window Size

```text
5
```

Most Frequent

```text
3
```

Replace

```text
5 - 3 = 2
```

Convert

```text
B

↓

A

C

↓

A
```

Result

```text
A A A A A
```

______________________________________________________________________

# Window Invariant

The window is valid if:

```text
Window Size

-

Maximum Frequency

≤ k
```

If this becomes false,

the window is invalid.

Shrink it.

This is the invariant maintained throughout the algorithm.

______________________________________________________________________

# Visual Explanation

```text
A A B A B

↑
L

↑
R
```

Window

```text
A
```

Expand

```text
AA
```

Expand

```text
AAB
```

Window Size

```text
3
```

Max Frequency

```text
2
```

Need

```text
1
```

replacement.

Still valid.

Expand again.

Continue until

```text
Needed Replacements > k
```

Shrink.

______________________________________________________________________

# Step-by-Step Algorithm

Initialize

```text
left = 0
```

Maintain:

- frequency map
- maximum frequency
- best answer

For every right pointer:

1. Add new character.
1. Update maximum frequency.
1. If window becomes invalid,
shrink from the left.
1. Update answer.

______________________________________________________________________

# Dry Run

Input

```text
AABABBA

k = 1
```

Window

```text
A
```

Longest

```text
1
```

Expand

```text
AA
```

Longest

```text
2
```

Expand

```text
AAB
```

Need

```text
1
```

replacement.

Valid.

Expand

```text
AABA
```

Need

```text
1
```

Valid.

Longest

```text
4
```

Expand

```text
AABAB
```

Need

```text
2
```

Invalid.

Shrink.

Continue.

Final answer

```text
4
```

______________________________________________________________________

# Why We Don't Recompute Maximum Frequency

A common interview question is:

> "Why don't we decrease `max_frequency` when shrinking?"

Example

```text
A A A B C
```

Suppose

```text
max_frequency = 3
```

After shrinking,

it may no longer be exactly 3.

Surprisingly,

that's okay.

Why?

Because a slightly stale `max_frequency` may delay shrinking, but it **never causes us to miss the optimal answer**. It
only makes the window appear more permissive temporarily, and future expansions eventually correct it.

Maintaining an exact maximum every shrink would require rescanning the frequency map, making the implementation more
complex without improving the asymptotic complexity.

______________________________________________________________________

# Edge Cases

## Empty String

Answer

```text
0
```

______________________________________________________________________

## k = 0

No replacements.

Need the longest existing block.

______________________________________________________________________

## All Same

```text
AAAAAA
```

Answer

```text
6
```

______________________________________________________________________

## Large k

```text
ABC

k = 10
```

Whole string becomes identical.

Answer

```text
3
```

______________________________________________________________________

# Complexity Analysis

## Time

Each pointer moves at most once.

```text
O(n)
```

______________________________________________________________________

## Space

Frequency map.

English uppercase letters.

```text
O(1)
```

______________________________________________________________________

# Production-Quality Python

```python
from collections import defaultdict


def character_replacement(s: str, k: int) -> int:
    """
    Returns the longest substring that can
    become one repeating character.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    frequency = defaultdict(int)

    left = 0
    max_frequency = 0
    longest = 0

    for right, char in enumerate(s):
        frequency[char] += 1
        max_frequency = max(max_frequency, frequency[char])

        while (right - left + 1) - max_frequency > k:
            frequency[s[left]] -= 1
            left += 1

        longest = max(longest, right - left + 1)

    return longest
```

______________________________________________________________________

# Common Mistakes

## 1. Actually Replacing Characters

Don't.

We're only checking if replacement is **possible**.

______________________________________________________________________

## 2. Forgetting the Formula

Always remember:

```text
Replacements Needed

=

Window Size

-

Maximum Frequency
```

______________________________________________________________________

## 3. Recomputing Maximum Frequency Every Time

Unnecessary.

Keep the highest value seen.

______________________________________________________________________

## 4. Shrinking Too Early

Shrink only when:

```text
Window Size

-

Maximum Frequency

>

k
```

______________________________________________________________________

# Variations

## Medium

- Max Consecutive Ones III
- Fruit Into Baskets
- Maximize the Confusion of an Exam

______________________________________________________________________

## Hard

- Minimum Window Substring
- Sliding Window Maximum

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Recognize a variable Sliding Window.
1. Count character frequencies.
1. Track the most frequent character.
1. Calculate replacements needed.
1. Shrink only when replacements exceed `k`.
1. Update the longest valid window.

______________________________________________________________________

### Common Follow-ups

### Q: Why subtract the maximum frequency?

Because those characters are already correct.

Everything else must be replaced.

______________________________________________________________________

### Q: Why not recompute the maximum frequency after shrinking?

It isn't necessary for correctness and would complicate the implementation.

______________________________________________________________________

### Q: Why is this O(n)?

Each character enters and leaves the window at most once.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Variable Sliding Window |
| Recognition | Longest substring with at most K changes |
| Invariant | Window Size − Max Frequency ≤ K |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Practice Problems

## Easy

1. Max Consecutive Ones
1. Maximum Average Subarray I

## Medium

1. Max Consecutive Ones III
1. Fruit Into Baskets
1. Maximize the Confusion of an Exam
1. Frequency of the Most Frequent Element *(different optimization)*

## Hard

1. Minimum Window Substring
1. Sliding Window Maximum

______________________________________________________________________

# Quick Revision

- Variable Sliding Window.
- Track character frequencies.
- Track the most frequent character.
- Formula:

```text
Window Size − Max Frequency
```

- If replacements needed exceed `k`, shrink.
- Time: **O(n)**
- Space: **O(1)**

______________________________________________________________________

# Key Takeaway

This problem introduces one of the most useful Sliding Window ideas:

> **A window doesn't have to be perfect—it only has to satisfy the problem's constraint.**

Here, the constraint is:

```text
Window Size − Max Frequency ≤ k
```

Many advanced Sliding Window problems are solved by identifying a similar **window invariant**.

______________________________________________________________________

# Navigation

**Previous**

[18-permutation-in-string.md](18-permutation-in-string.md)

**Next**

[20-minimum-window-substring.md](20-minimum-window-substring.md)
