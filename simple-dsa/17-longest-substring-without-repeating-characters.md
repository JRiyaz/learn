# 17-longest-substring-without-repeating-characters.md

# Longest Substring Without Repeating Characters — The Expand-Shrink Pattern

## Interview Confidence

**Difficulty:** ⭐⭐⭐☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20–25 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given a string `s`, find the length of the **longest substring** without repeating characters.

A **substring** is a **continuous** sequence of characters.

### Example 1

```text
Input

"abcabcbb"

Output

3

Explanation

"abc"
```

### Example 2

```text
Input

"bbbbb"

Output

1
```

### Example 3

```text
Input

"pwwkew"

Output

3

Explanation

"wke"
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is asking:

> Find the longest **continuous** sequence where every character is unique.

Notice:

```text
"pwke"
```

is **not** valid because it is a subsequence, not a substring.

Only continuous characters count.

______________________________________________________________________

# Real-World Analogy

Suppose a backend service generates session IDs.

```
A B C A D E
```

You want the longest sequence before a character repeats.

Other examples:

- Longest unique URL path
- Unique API requests
- Longest period without duplicate events
- Longest streak of unique users

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Longest substring
- Continuous sequence
- Without repeating
- Unique characters

Think:

```text
Variable Sliding Window

+

Hash Set / Hash Map
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Start from every character.

Expand until a duplicate appears.

Repeat for every starting position.

Example

```text
abcabc

Start at a

↓

abc

↓

abca

Duplicate
```

Repeat from

```text
b

↓

bc

↓

bca

...
```

______________________________________________________________________

## Complexity

Time

```text
O(n²)
```

Space

```text
O(n)
```

Too slow.

______________________________________________________________________

# Optimal Solution

## Key Insight

Maintain a window containing **only unique characters**.

Expand the window by moving `right`.

If a duplicate appears:

Shrink from the left until the window becomes valid again.

______________________________________________________________________

# Visual Explanation

```text
String

a b c a d

L
R
```

Window

```text
[a]
```

Unique.

Expand.

```text
[a b]
```

Expand.

```text
[a b c]
```

Expand.

```text
[a b c a]
```

Duplicate!

Shrink.

Remove

```text
a
```

Window becomes

```text
[b c a]
```

Unique again.

Continue.

______________________________________________________________________

# Why Shrinking Works

Suppose

```text
abcdea
```

Window

```text
abcdea
```

Duplicate

```text
a
```

Instead of restarting,

remove characters from the left until only one `a` remains.

We reuse almost all previous work.

______________________________________________________________________

# Step-by-Step Algorithm

Initialize

```text
left = 0

right = 0

seen = {}
```

Expand right.

If duplicate exists:

Move left while removing characters.

Update maximum window length.

Repeat.

______________________________________________________________________

# Dry Run

Input

```text
"abba"
```

Start

```text
[a]
```

Length

```text
1
```

Expand

```text
[a b]
```

Length

```text
2
```

Expand

```text
[a b b]
```

Duplicate.

Shrink.

Remove

```text
a
```

Still duplicate.

Remove

```text
b
```

Window

```text
[b]
```

Continue.

Maximum remains

```text
2
```

______________________________________________________________________

# Why This Works

The window always satisfies:

> Every character appears only once.

Whenever this condition breaks,

we restore it by shrinking.

Each character:

- enters the window once
- leaves the window once

Therefore,

the total work is linear.

______________________________________________________________________

# Edge Cases

## Empty String

```text
""
```

Answer

```text
0
```

______________________________________________________________________

## One Character

```text
"a"
```

Answer

```text
1
```

______________________________________________________________________

## All Unique

```text
abcdef
```

Answer

```text
6
```

______________________________________________________________________

## All Same

```text
aaaaa
```

Answer

```text
1
```

______________________________________________________________________

# Complexity Analysis

## Time

Each character enters once.

Each character leaves once.

```text
O(n)
```

______________________________________________________________________

## Space

Hash Set stores at most all unique characters.

```text
O(k)
```

where `k` is the number of unique characters.

______________________________________________________________________

# Production-Quality Python

## Approach 1 (Hash Set)

```python
from typing import Set


def length_of_longest_substring(s: str) -> int:
    """
    Returns the length of the longest substring
    without repeating characters.

    Time Complexity: O(n)
    Space Complexity: O(k)
    """

    seen: Set[str] = set()

    left = 0
    longest = 0

    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1

        seen.add(s[right])
        longest = max(longest, right - left + 1)

    return longest
```

______________________________________________________________________

## Approach 2 (Hash Map - Faster)

Instead of removing one character at a time,

jump directly to the correct position.

```python
from typing import Dict


def length_of_longest_substring(s: str) -> int:
    last_seen: Dict[str, int] = {}

    left = 0
    longest = 0

    for right, char in enumerate(s):
        if char in last_seen:
            left = max(left, last_seen[char] + 1)

        last_seen[char] = right
        longest = max(longest, right - left + 1)

    return longest
```

This is the version most experienced engineers prefer.

______________________________________________________________________

# Common Mistakes

## 1. Restarting From Scratch

Don't.

Shrink the existing window.

______________________________________________________________________

## 2. Forgetting Continuous Substring

Substrings must be contiguous.

______________________________________________________________________

## 3. Moving Left Backwards

Never do

```python
left = last_seen[char] + 1
```

Always write

```python
left = max(left, last_seen[char] + 1)
```

Otherwise,

`left` can move backwards.

Example

```text
abba
```

This is one of the most common interview bugs.

______________________________________________________________________

## 4. Forgetting to Update Last Seen Index

Always store the latest position.

______________________________________________________________________

# Variations

## Medium

- Longest Repeating Character Replacement
- Fruit Into Baskets
- Permutation in String
- Maximum Erasure Value

______________________________________________________________________

## Hard

- Minimum Window Substring
- Sliding Window Maximum

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Identify it as a substring problem.
1. Recognize Sliding Window.
1. Maintain unique characters.
1. Expand right.
1. Shrink left when invalid.
1. Keep track of the maximum length.

______________________________________________________________________

### Common Follow-ups

### Q: Why use a Hash Set?

Fast duplicate detection.

______________________________________________________________________

### Q: Why use a Hash Map?

Allows jumping directly to the duplicate's last position.

Less pointer movement.

______________________________________________________________________

### Q: Why `max(left, last_seen + 1)`?

Because `left` should never move backwards.

Example

```text
abba
```

Without `max()`, the algorithm becomes incorrect.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Variable Sliding Window |
| Recognition | Longest substring, unique characters |
| Window State | Always unique |
| Time | O(n) |
| Space | O(k) |

______________________________________________________________________

# Practice Problems

## Easy

1. Maximum Average Subarray I
1. Find All Anagrams in a String

## Medium

1. Fruit Into Baskets
1. Longest Repeating Character Replacement
1. Maximum Erasure Value
1. Permutation in String

## Hard

1. Minimum Window Substring
1. Sliding Window Maximum

______________________________________________________________________

# Quick Revision

- Continuous substring → Sliding Window.
- Expand using `right`.
- Shrink using `left`.
- Keep the window valid (unique characters).
- Use a Hash Set or Hash Map.
- Never move `left` backwards.
- Time: **O(n)**
- Space: **O(k)**

______________________________________________________________________

# Key Takeaway

This is the **foundation of nearly every variable Sliding Window interview problem**.

The invariant is:

> **The window must always satisfy the problem's condition.**

For this problem:

```text
Every character inside the window is unique.
```

Every future Sliding Window problem simply changes this invariant.

______________________________________________________________________

# Navigation

**Previous**

[16-sliding-window.md](16-sliding-window.md)

**Next**

[18-permutation-in-string.md](18-permutation-in-string.md)
