# 07-valid-anagram.md

# Valid Anagram — The Frequency Counting Pattern

## Interview Confidence

**Difficulty:** ⭐☆☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐☆

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 10–15 minutes

**Revision Time:** 3 minutes

______________________________________________________________________

# Problem Statement

## Original Problem

Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, otherwise return `False`.

An anagram is formed by rearranging the letters of another word using **all** the original letters **exactly once**.

### Example 1

```text
s = "anagram"
t = "nagaram"

Output:
True
```

### Example 2

```text
s = "rat"
t = "car"

Output:
False
```

______________________________________________________________________

# What Is Actually Being Asked?

The interviewer is **not** asking:

- Are the strings in the same order?
- Do they contain similar letters?

They're asking:

> Does every character appear the **same number of times** in both strings?

For example,

```text
listen
silent
```

Both contain:

```text
l -> 1
i -> 1
s -> 1
t -> 1
e -> 1
n -> 1
```

Therefore,

```text
True
```

______________________________________________________________________

# Real-World Analogy

Suppose you're building a backend service that compares two invoices.

Invoice A

```text
Apple
Apple
Banana
```

Invoice B

```text
Banana
Apple
Apple
```

The order doesn't matter.

The quantity of each item does.

Exactly the same idea applies here.

Other examples:

- Inventory comparison
- Shopping cart validation
- Log comparison
- File checksum verification (conceptually)

______________________________________________________________________

# Pattern Recognition

This problem introduces the **Frequency Counting Pattern**.

Whenever you see:

- Same elements?
- Same characters?
- Count occurrences
- Rearranged
- Permutation
- Frequency

Think:

> Count occurrences using a Hash Map.

______________________________________________________________________

# Brute Force Solution

## Intuition

Sort both strings.

If they're identical after sorting,

they are anagrams.

Example

```text
listen

↓

eilnst
```

```text
silent

↓

eilnst
```

Equal.

Return

```text
True
```

______________________________________________________________________

## Complexity

Sorting each string

```text
O(n log n)
```

Space

Depends on language implementation.

______________________________________________________________________

## Python

```python
def is_anagram_sort(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)
```

Although simple, this is **not** the optimal solution.

______________________________________________________________________

# Optimal Solution

## Key Insight

Instead of sorting,

count the frequency of every character.

If both strings have identical frequencies,

they are anagrams.

______________________________________________________________________

# Visual Explanation

Example

```text
s = "aab"

↓

a -> 2

b -> 1
```

```text
t = "aba"

↓

a -> 2

b -> 1
```

Frequency maps are identical.

Return

```text
True
```

______________________________________________________________________

# Step-by-Step Algorithm

If lengths differ:

Return `False`.

Create a frequency map.

Traverse first string.

Increment count.

Traverse second string.

Decrement count.

If any count becomes negative,

return `False`.

Finally,

all counts should be zero.

______________________________________________________________________

# Dry Run

```text
s = "abb"

t = "bab"
```

Initial Map

```text
{}
```

After first string

```text
a -> 1

b -> 2
```

Process second string

```text
b -> 1

a -> 0

b -> 0
```

All counts are zero.

Answer

```text
True
```

______________________________________________________________________

# Why This Works

Two strings are anagrams if and only if:

Every character appears exactly the same number of times.

The frequency map records this information.

Matching frequencies guarantee identical character composition.

______________________________________________________________________

# Edge Cases

## Different Lengths

```text
abc

ab
```

Immediately return

```text
False
```

______________________________________________________________________

## Empty Strings

```text
""

""
```

Return

```text
True
```

______________________________________________________________________

## One Character

```text
"a"

"a"
```

Return

```text
True
```

______________________________________________________________________

## Different Counts

```text
aab

abb
```

Return

```text
False
```

______________________________________________________________________

## Unicode Characters

The algorithm works for any hashable character, not just English letters.

______________________________________________________________________

# Complexity Analysis

## Time

Single pass over both strings.

```text
O(n)
```

______________________________________________________________________

## Space

At most one entry per unique character.

```text
O(k)
```

where `k` is the number of distinct characters.

For lowercase English letters, `k ≤ 26`, making it effectively constant.

______________________________________________________________________

# Production-Quality Python

```python
from typing import Dict


def is_anagram(s: str, t: str) -> bool:
    """
    Returns True if t is an anagram of s.

    Time Complexity: O(n)
    Space Complexity: O(k)
    """

    if len(s) != len(t):
        return False

    frequency: Dict[str, int] = {}

    for char in s:
        frequency[char] = frequency.get(char, 0) + 1

    for char in t:
        if char not in frequency:
            return False

        frequency[char] -= 1

        if frequency[char] < 0:
            return False

    return True
```

______________________________________________________________________

# Alternative Solution

Python's `Counter` makes this concise.

```python
from collections import Counter


def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)
```

### Interview Advice

Use this only if the interviewer allows standard library helpers.

Otherwise, implement the frequency map yourself to demonstrate understanding.

______________________________________________________________________

# Common Mistakes

## 1. Ignoring Length

Always check first.

Different lengths can never be anagrams.

______________________________________________________________________

## 2. Using Nested Loops

This results in

```text
O(n²)
```

Avoid repeated searches.

______________________________________________________________________

## 3. Comparing Sets

Wrong

```python
set(s) == set(t)
```

Example

```text
aab

abb
```

Both sets are

```text
{a,b}
```

But they are **not** anagrams.

______________________________________________________________________

## 4. Forgetting Frequency Counts

Presence alone isn't enough.

Counts must match.

______________________________________________________________________

# Variations

## Easy

- Ransom Note
- Find the Difference

______________________________________________________________________

## Medium

- Group Anagrams
- Permutation in String
- Find All Anagrams in a String
- Minimum Window Substring

Notice that all of these rely on the same frequency-counting idea.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Observe that order is irrelevant.
1. Realize only frequencies matter.
1. Mention sorting solution.
1. Optimize using a Hash Map.
1. Explain complexity.

______________________________________________________________________

### Common Follow-ups

### Q: Why check length first?

Different lengths can never have identical frequencies.

______________________________________________________________________

### Q: Can this be done without extra space?

Yes.

Sort both strings.

Time:

```text
O(n log n)
```

______________________________________________________________________

### Q: If only lowercase English letters are allowed?

Use an array of size 26 instead of a dictionary.

Lookup becomes slightly faster with lower memory overhead.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Frequency Counting |
| Recognition | Same elements, counts, permutation |
| Brute Force | Sorting |
| Optimal | Hash Map Frequency Count |
| Time | O(n) |
| Space | O(k) |

______________________________________________________________________

# Practice Problems

## Easy

1. Ransom Note
1. Find the Difference

## Medium

1. Group Anagrams
1. Permutation in String
1. Find All Anagrams in a String
1. Isomorphic Strings

## Hard

1. Minimum Window Substring
1. Word Pattern II

______________________________________________________________________

# Quick Revision

- Order doesn't matter.
- Character frequency does.
- Check lengths first.
- Count characters using a Hash Map.
- Compare frequencies.
- Sorting works but costs **O(n log n)**.
- Frequency counting is **O(n)**.
- Don't use `set()` because it ignores duplicate counts.

______________________________________________________________________

# Key Takeaway

When the problem asks:

> "Do these two collections contain the same elements with the same counts?"

Immediately think:

> **Frequency Counting using a Hash Map.**

This pattern appears repeatedly in interview questions involving strings, arrays, and even trees.

______________________________________________________________________

# Navigation

**Previous**

[06-hash-maps.md](06-hash-maps.md)

**Next**

[08-group-anagrams.md](08-group-anagrams.md)
