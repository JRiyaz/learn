# 26-longest-substring-without-repeating-characters.md

# Longest Substring Without Repeating Characters

> **🎯 This is your first Sliding Window problem.**
>
> If you deeply understand this lesson, you'll understand almost **70% of Sliding Window interview questions**. Nearly every variable-size sliding window problem is built on the same idea.

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 30 minutes |
| Revision Time | 20 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This is one of the most famous coding interview questions.

Interviewers are testing whether you understand:

- Sliding Window
- Two Pointers
- Hash Set / Hash Map
- Window expansion
- Window shrinking
- Maintaining an invariant

Unlike previous Two Pointer problems, **both pointers move in the same direction**.

This is the foundation for solving:

- Minimum Window Substring
- Longest Repeating Character Replacement
- Permutation in String
- Fruit Into Baskets
- Max Consecutive Ones
- Longest Subarray with K Distinct Elements

______________________________________________________________________

# Problem Statement

Given a string `text`,

find the **length** of the longest substring that contains **no repeated characters**.

A **substring** means:

> Characters must be **contiguous**.

______________________________________________________________________

## Example 1

```text
Input

"abcabcbb"
```

Output

```text
3
```

Explanation

```
"abc"
```

is the longest substring without repeating characters.

______________________________________________________________________

## Example 2

```text
Input

"bbbbb"
```

Output

```text
1
```

______________________________________________________________________

## Example 3

```text
Input

"pwwkew"
```

Output

```text
3
```

One answer is

```
"wke"
```

______________________________________________________________________

# Before Learning the Algorithm

## What is a Substring?

Substring

```
abcdef
```

Examples

```
abc

✔
```

```
cde

✔
```

```
ef

✔
```

Not a substring

```
ace

✖
```

because characters are skipped.

______________________________________________________________________

# Simple English

Imagine people entering a meeting room.

Rule:

```
No duplicate employee IDs allowed.
```

As long as everyone entering has a unique ID,

the meeting room grows.

The moment a duplicate enters,

people start leaving from the left until the duplicate disappears.

That's Sliding Window.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a WebSocket server.

A user session can contain only one active connection per device.

As new connections arrive,

duplicates force the oldest connection to close.

The active session continuously expands and shrinks.

This dynamic range is exactly a **Sliding Window**.

Other examples:

- TCP packet windows
- Kafka consumer batches
- Streaming analytics
- Rate limiting
- Session management

______________________________________________________________________

# Pattern Recognition

## Pattern

**Variable-Size Sliding Window**

______________________________________________________________________

## Recognition Clues

Whenever you see:

- Longest substring
- Shortest substring
- Contiguous
- Window
- At most K
- Without repeating
- Consecutive

Think

```
Sliding Window
```

______________________________________________________________________

# Why Brute Force Fails

Suppose

```
abcabcbb
```

Generate every substring.

```
a

ab

abc

abca

abcab

...
```

For every substring,

check whether duplicates exist.

This produces an enormous number of substrings.

______________________________________________________________________

# Brute Force Solution

## Intuition

Generate every possible substring.

Check whether it contains duplicates.

Keep the longest.

______________________________________________________________________

## Algorithm

```
Start

↓

Every Ending Position

↓

Check Duplicate

↓

Update Answer
```

______________________________________________________________________

## Dry Run

```
abc
```

Substrings

```
a

ab

abc

b

bc

c
```

Largest

```
abc
```

Length

```
3
```

______________________________________________________________________

## Complexity

Total substrings

```
O(n²)
```

Duplicate check

```
O(n)
```

Overall

```
O(n³)
```

Too slow.

______________________________________________________________________

# Better Observation

Suppose

```
abc
```

contains no duplicates.

Now,

add

```
d
```

Still valid.

```
abcd
```

Now add

```
a
```

```
abcda
```

Duplicate appears.

Do we restart everything?

No.

We simply remove characters from the left until the duplicate disappears.

That's the key insight.

______________________________________________________________________

# Sliding Window Concept

Imagine a window.

```
Left                  Right

↓

a b c

↑
```

Window grows.

```
a b c d
```

Still valid.

Grow again.

```
a b c d a
```

Duplicate!

Shrink.

```
b c d a
```

Valid again.

Continue.

______________________________________________________________________

# Understanding the Two Pointers

```
Left Pointer

↓

Beginning of window
```

```
Right Pointer

↓

Expands window
```

Unlike previous problems,

both pointers move

```
Left → Right
```

Only.

They never move backward.

______________________________________________________________________

# Step-by-Step Dry Run

Input

```
abcabcbb
```

Initially

```
Window

{}
```

Answer

```
0
```

______________________________________________________________________

Read

```
a
```

Window

```
a
```

Length

```
1
```

Answer

```
1
```

______________________________________________________________________

Read

```
b
```

Window

```
ab
```

Length

```
2
```

Answer

```
2
```

______________________________________________________________________

Read

```
c
```

Window

```
abc
```

Length

```
3
```

Answer

```
3
```

______________________________________________________________________

Read

```
a
```

Duplicate.

Shrink.

Remove

```
a
```

Window

```
bc
```

Now add

```
a
```

Window

```
bca
```

Length

```
3
```

Answer remains

```
3
```

Continue.

______________________________________________________________________

# Complete Visual Explanation

Input

```
abcabcbb
```

```
Window

[a]
```

↓

```
[a b]
```

↓

```
[a b c]
```

↓

Duplicate

```
a
```

Shrink

```
[b c]
```

↓

Add

```
a
```

↓

```
[b c a]
```

↓

Continue.

Notice

The window

**slides**

instead of restarting.

______________________________________________________________________

# Sliding Window Invariant (Very Important)

The window must always satisfy:

> **Every character inside the window is unique.**

Whenever this rule breaks,

shrink the window until it becomes true again.

This rule is called the **Window Invariant**.

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before processing each new character, the current window contains only unique characters.

Every iteration has two possibilities:

### Case 1

New character isn't inside the window.

Expand.

______________________________________________________________________

### Case 2

Character already exists.

Shrink from the left until it disappears.

Then expand again.

Since both pointers only move forward,

each character enters and leaves the window at most once.

______________________________________________________________________

# Why Is It O(n)?

This confuses many students.

Imagine

```
n = 8
```

Right pointer

```
→ → → → → → → →
```

moves

```
8
```

times.

Left pointer

```
→ → → → → → → →
```

also moves

at most

```
8
```

times.

Total work

```
8 + 8

=

16

=

2n
```

Ignoring constants,

```
O(n)
```

This is one of the biggest advantages of Sliding Window.

______________________________________________________________________

# Edge Cases

### Empty String

```
""
```

Return

```
0
```

______________________________________________________________________

### One Character

```
"a"
```

Return

```
1
```

______________________________________________________________________

### All Same Characters

```
aaaa
```

Answer

```
1
```

______________________________________________________________________

### All Unique

```
abcdef
```

Answer

```
6
```

______________________________________________________________________

### Unicode Characters

The algorithm works correctly because Python sets support Unicode.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n³)
```

Space

```
O(n)
```

______________________________________________________________________

## Sliding Window

Time

```
O(n)
```

Space

```
O(min(n, character_set_size))
```

For lowercase English letters,

space is effectively constant.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import Set


def length_of_longest_substring(text: str) -> int:
    longest = 0

    for start in range(len(text)):
        for end in range(start, len(text)):
            seen: Set[str] = set()
            valid = True

            for character in text[start : end + 1]:
                if character in seen:
                    valid = False
                    break

                seen.add(character)

            if valid:
                longest = max(longest, end - start + 1)

    return longest
```

______________________________________________________________________

## Optimized (Sliding Window)

```python
from typing import Set


def length_of_longest_substring(text: str) -> int:
    window: Set[str] = set()

    left = 0
    longest = 0

    for right in range(len(text)):
        while text[right] in window:
            window.remove(text[left])
            left += 1

        window.add(text[right])

        longest = max(longest, right - left + 1)

    return longest


if __name__ == "__main__":
    value = "abcabcbb"

    print(length_of_longest_substring(value))
```

______________________________________________________________________

# Even Better Optimization (Hash Map)

Instead of removing characters one by one,

store the **last seen index**.

Example

```
a b c a
```

Instead of shrinking repeatedly,

jump directly.

```
Left

↓

Last Seen Index + 1
```

This is the solution many senior engineers prefer.

```python
left = max(left, last_seen[text[right]] + 1)
```

We'll study this optimization later when covering advanced Sliding Window problems.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Restarting after finding a duplicate.

Don't restart.

Slide the window.

______________________________________________________________________

## Mistake 2

Using nested loops.

Sliding Window eliminates them.

______________________________________________________________________

## Mistake 3

Moving the left pointer only once.

Shrink until the window becomes valid again.

______________________________________________________________________

## Mistake 4

Updating the answer before removing duplicates.

Always restore the invariant first.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The brute-force solution generates every substring and checks for duplicates, which is O(n³). I notice that if a substring is already valid, I don't need to start over when a duplicate appears. Instead, I can maintain a sliding window of unique characters using a Hash Set. I expand the window with the right pointer and shrink it with the left pointer whenever a duplicate is found. Since each pointer moves at most `n` times, the algorithm runs in O(n) time."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why is this called a Sliding Window?**

Because the window continuously expands and shrinks while moving through the string.

______________________________________________________________________

**Q. Why use a Hash Set?**

It allows O(1) average-time membership checks.

______________________________________________________________________

**Q. Why is the complexity O(n) instead of O(n²)?**

Each pointer moves only forward,

and each character enters and leaves the window at most once.

______________________________________________________________________

**Q. Can this be optimized further?**

Yes.

Using a Hash Map of last-seen indices allows jumping the left pointer directly.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Variable-Size Sliding Window |
| Recognition | Longest/Shortest Contiguous Substring |
| Brute Force | Generate Every Substring |
| Optimized | Sliding Window + Hash Set |
| Better Optimization | Sliding Window + Hash Map |
| Time | O(n) |
| Space | O(min(n, character_set_size)) |

______________________________________________________________________

# Quick Revision

- Sliding Window works on contiguous data.
- Maintain a window with unique characters.
- Expand using the right pointer.
- Shrink using the left pointer when the window becomes invalid.
- Keep updating the maximum window size.
- Both pointers move only forward.
- Time complexity is O(n).
- This is one of the most important interview patterns.

______________________________________________________________________

# Practice Questions

## Easy

1. Maximum Number of Vowels in a Substring of Given Length
1. Max Consecutive Ones
1. Defanging an IP Address (warm-up)

______________________________________________________________________

## Medium

4. Longest Repeating Character Replacement
1. Permutation in String
1. Minimum Window Substring
1. Fruit Into Baskets
1. Longest Substring with At Most K Distinct Characters

______________________________________________________________________

## Hard (Optional)

9. Substring with Concatenation of All Words
1. Minimum Window Subsequence

______________________________________________________________________

# Key Takeaway

The most important lesson is learning the **Variable-Size Sliding Window** pattern. Instead of recomputing every
substring, maintain a window that always satisfies a specific rule (the **window invariant**) and adjust its boundaries
dynamically. This technique transforms many quadratic string and array problems into elegant linear-time solutions and
is one of the highest-value patterns for technical interviews.

______________________________________________________________________

# Next

[27-valid-parentheses.md](27-valid-parentheses.md)
