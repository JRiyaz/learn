# 16-sliding-window.md

# Sliding Window — Processing Continuous Ranges Efficiently

## Interview Confidence

**Difficulty:** ⭐⭐⭐☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Why Interviewers Ask This

A large number of interview problems involve finding something inside a **continuous subarray** or **substring**.

Common examples:

- Longest substring
- Maximum sum of k elements
- Smallest window
- Longest repeating characters
- Minimum window substring

Many candidates solve these using nested loops.

Example:

```text
Start at index 0

↓

Check every ending index

↓

Start at index 1

↓

Check every ending index
```

Time Complexity

```text
O(n²)
```

Interviewers expect you to recognize when a **Sliding Window** can reduce this to **O(n)**.

______________________________________________________________________

# Learning Objectives

After this lesson, you should be able to:

- Understand what a sliding window is.
- Recognize Sliding Window problems.
- Distinguish between Fixed and Variable windows.
- Know when Sliding Window should **not** be used.
- Understand why the algorithm is O(n).

______________________________________________________________________

# What Is a Sliding Window?

A Sliding Window is a **continuous range** inside an array or string.

Example

```text
Array

1 2 3 4 5 6 7

Window Size = 3

[1 2 3]

↓

[2 3 4]

↓

[3 4 5]

↓

[4 5 6]
```

Instead of recalculating everything,

we reuse previous work.

______________________________________________________________________

# Real-World Analogy

Suppose you're monitoring website traffic.

```text
Visitors Per Minute

20 18 25 30 22 19
```

Find the busiest **3-minute period**.

You don't recalculate the total from scratch every time.

Instead,

remove the oldest minute,

add the newest minute.

Exactly like a sliding window.

Other examples:

- CPU usage monitoring
- Network throughput
- Stock prices
- Temperature sensors
- Rolling averages

______________________________________________________________________

# Pattern Recognition

Interview clues:

- Subarray
- Substring
- Continuous sequence
- Window
- Longest
- Shortest
- At most K
- At least K

Think:

> **Sliding Window**

______________________________________________________________________

# Types of Sliding Windows

## 1. Fixed Size Window

Window size never changes.

Example

```text
Find maximum sum of 5 consecutive elements.
```

Visual

```text
1 2 3 4 5 6

[1 2 3]

↓

[2 3 4]

↓

[3 4 5]
```

______________________________________________________________________

## 2. Variable Size Window

Window expands and shrinks.

Example

```text
Longest substring without repeating characters.
```

Visual

```text
a b c a d

<---->

Expand

↓

Duplicate

↓

Shrink

↓

Expand Again
```

This is the most common interview pattern.

______________________________________________________________________

# Fixed Window Example

Suppose

```text
2 4 6 8

Window = 2
```

First window

```text
2+4=6
```

Next window

Instead of

```text
4+6
```

from scratch,

Reuse previous sum.

```text
Old Sum

6

-

2

+

6

=

10
```

This is the optimization.

______________________________________________________________________

# Variable Window Example

Suppose

```text
a b c a
```

Window

```text
abc
```

Unique.

Expand.

```text
abca
```

Duplicate found.

Shrink.

```text
bca
```

Unique again.

Continue.

______________________________________________________________________

# Sliding Window vs Two Pointers

Both use two pointers.

Difference:

### Two Pointers

Usually compare two positions.

```text
L         R
```

______________________________________________________________________

### Sliding Window

Maintains a **continuous region**.

```text
L ---- R
```

The area between the pointers is the important part.

______________________________________________________________________

# General Algorithm

Expand

```text
right += 1
```

Update window.

If invalid,

Shrink.

```text
left += 1
```

Continue.

______________________________________________________________________

# Why Sliding Window Works

Suppose

```text
Longest unique substring
```

Brute Force

```text
Start everywhere.

Expand everywhere.
```

Repeated work.

Sliding Window

Each character

- enters once
- leaves once

Total operations

```text
2n

↓

O(n)
```

______________________________________________________________________

# When NOT to Use Sliding Window

Avoid when:

- Elements are non-contiguous.
- Sorting is required.
- Random subsets are needed.
- The problem involves arbitrary combinations instead of continuous ranges.

Example

```text
Find any three numbers whose sum is 10.
```

Not a Sliding Window problem.

______________________________________________________________________

# Common Interview Problems

## Fixed Window

- Maximum Average Subarray I
- Maximum Sum Subarray of Size K

______________________________________________________________________

## Variable Window

- Longest Substring Without Repeating Characters
- Longest Repeating Character Replacement
- Minimum Window Substring
- Permutation in String
- Fruit Into Baskets

______________________________________________________________________

# Backend Analogy

Suppose your API receives requests every second.

```text
20
25
30
15
18
```

Find:

> Highest traffic during any 60-second interval.

Instead of recomputing every minute,

keep a rolling window.

This is widely used in:

- Rate limiting
- Streaming analytics
- Monitoring dashboards
- Fraud detection
- Event processing

______________________________________________________________________

# Common Mistakes

## 1. Forgetting the Window Must Be Continuous

Sliding Window always operates on contiguous elements.

______________________________________________________________________

## 2. Shrinking Too Early

Expand first.

Shrink only when the window becomes invalid.

______________________________________________________________________

## 3. Recomputing the Entire Window

Reuse previous work whenever possible.

______________________________________________________________________

## 4. Confusing Sliding Window with Two Pointers

All Sliding Window problems use two pointers.

Not all Two Pointer problems are Sliding Window problems.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Is the problem asking about a continuous range?
1. Is brute force checking every subarray?
1. Can previous computation be reused?
1. Should the window be fixed or variable?
1. What condition makes the window invalid?

______________________________________________________________________

### Common Follow-ups

### Q: Why is Sliding Window O(n)?

Every element enters the window once and leaves once.

Total pointer movements are linear.

______________________________________________________________________

### Q: When should I shrink the window?

Only when the problem's condition becomes invalid.

______________________________________________________________________

### Q: Can Sliding Window work on linked lists?

Usually no.

Random access isn't available.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Sliding Window |
| Recognition | Continuous subarray/substring |
| Types | Fixed & Variable |
| Time | O(n) |
| Space | Usually O(1) or O(k) |

______________________________________________________________________

# Practice Problems

## Easy

1. Maximum Average Subarray I
1. Maximum Sum Subarray of Size K

## Medium

1. Longest Substring Without Repeating Characters
1. Permutation in String
1. Fruit Into Baskets
1. Longest Repeating Character Replacement

## Hard

1. Minimum Window Substring
1. Sliding Window Maximum

______________________________________________________________________

# Quick Revision

- Sliding Window works on **continuous ranges**.
- Fixed window → size never changes.
- Variable window → expands and shrinks.
- Expand first.
- Shrink only when necessary.
- Every element enters and leaves at most once.
- Time: **O(n)**.

______________________________________________________________________

# What's Next?

We'll begin with one of the most important Sliding Window interview problems:

**17-longest-substring-without-repeating-characters.md**

This problem introduces the **Expand–Shrink Pattern**, which is the foundation for many advanced Sliding Window
questions.

______________________________________________________________________

# Navigation

**Previous**

[15-3sum.md](15-3sum.md)

**Next**

[17-longest-substring-without-repeating-characters.md](17-longest-substring-without-repeating-characters.md)
