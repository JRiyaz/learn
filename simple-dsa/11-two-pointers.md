# 11-two-pointers.md

# Two Pointers — Solving Problems with Two Moving Indices

## Interview Confidence

**Difficulty:** ⭐⭐☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Why Interviewers Ask This

Many candidates solve array problems using nested loops.

Example:

```text
for i:
    for j:
```

Complexity:

```text
O(n²)
```

Interviewers want to know if you can recognize when **both loops can be replaced with two intelligently moving
pointers**, reducing the complexity to **O(n)**.

The Two Pointer pattern is one of the most common interview optimizations.

______________________________________________________________________

# Learning Objectives

After this lesson, you should be able to:

- Understand what pointers are.
- Recognize Two Pointer problems.
- Know the different types of Two Pointer techniques.
- Decide when **not** to use Two Pointers.
- Identify which movement strategy to apply.

______________________________________________________________________

# What Is a Pointer?

In DSA, a **pointer** is simply a variable that refers to an index or position.

Example:

```python
nums = [10, 20, 30, 40]

left = 0
right = 3
```

Visual

```text
Index

0   1   2   3

10  20  30  40

↑           ↑
L           R
```

In Python, these are integer indices.

In C/C++, they may be actual memory pointers.

______________________________________________________________________

# What Is the Two Pointer Technique?

Instead of using one index,

use two.

Move them according to the problem's rules.

Example:

```text
0   1   2   3   4

2   4   6   8   10

↑               ↑

L               R
```

The pointers may:

- move toward each other
- move together
- move independently
- move at different speeds

______________________________________________________________________

# Why Does It Work?

Consider finding two numbers whose sum equals a target.

Brute Force

```text
2 7 11 15

Check every pair

↓

O(n²)
```

If the array is sorted:

```text
2 7 11 15

↑       ↑
L       R
```

You can eliminate half the search space after each comparison.

This is the key idea behind Two Pointers.

______________________________________________________________________

# When Should You Think "Two Pointers"?

Interview clues:

- Sorted array
- Pair
- Triplet
- Palindrome
- Reverse
- Remove duplicates
- Merge
- Compare from both ends
- In-place modification

Whenever you need to compare two positions efficiently, Two Pointers are often a good choice.

______________________________________________________________________

# Types of Two Pointer Problems

## 1. Opposite Direction

Pointers start at opposite ends.

```text
1 2 3 4 5

↑       ↑

L       R
```

Used for:

- Two Sum II
- Valid Palindrome
- Container With Most Water

______________________________________________________________________

## 2. Same Direction

Both pointers move left to right.

```text
1 2 3 4 5

↑
Slow

  ↑
 Fast
```

Used for:

- Remove Duplicates
- Move Zeroes
- Partitioning arrays

______________________________________________________________________

## 3. Fast & Slow Pointer

Fast moves quicker.

```text
Slow

↓

1 → 2 → 3 → 4 → 5

↓

Fast
```

Mostly used in Linked Lists.

Examples:

- Detect Cycle
- Find Middle Node
- Happy Number

______________________________________________________________________

## 4. Sliding Window

Both pointers move forward while maintaining a window.

```text
1 2 3 4 5 6

  <---->

Window
```

This becomes its own major topic later.

______________________________________________________________________

# How to Decide Pointer Movement

The hardest part isn't writing code.

It's deciding:

> Which pointer should move?

General rule:

If the current state cannot produce a better answer,

move the pointer responsible for the limitation.

Examples:

### Sum Too Small

```text
2 4 7 11

↑      ↑

6 < Target
```

Increase sum.

Move left.

______________________________________________________________________

### Sum Too Large

```text
2 4 7 11

↑      ↑

13 > Target
```

Decrease sum.

Move right.

______________________________________________________________________

# Visual Example

Target

```text
9
```

Array

```text
2 3 4 7

↑     ↑

2+7=9
```

Found.

Another example

```text
2 3 8 10

↑      ↑

12

Too large

↓

Move Right
```

______________________________________________________________________

# When NOT to Use Two Pointers

Avoid this pattern if:

- The array is unsorted (unless sorting is allowed).
- Random jumps are required.
- A Hash Map provides a simpler O(n) solution.
- Order cannot be modified but sorting is required.

Example:

Original Two Sum.

Sorting destroys indices.

Hash Map is better.

______________________________________________________________________

# Common Interview Problems

## Easy

- Two Sum II
- Valid Palindrome
- Merge Sorted Array
- Remove Duplicates from Sorted Array
- Move Zeroes

______________________________________________________________________

## Medium

- 3Sum
- Container With Most Water
- Sort Colors
- Partition Labels

______________________________________________________________________

## Hard

- Trapping Rain Water
- Minimum Window Subsequence

______________________________________________________________________

# Two Pointers vs Hash Map

## Hash Map

Good for:

- Fast lookup
- Complements
- Frequency
- Duplicates

Complexity

```text
Time

O(n)

Space

O(n)
```

______________________________________________________________________

## Two Pointers

Good for:

- Sorted arrays
- In-place processing
- Pair comparisons

Complexity

```text
Time

O(n)

Space

O(1)
```

______________________________________________________________________

# Backend Analogy

Suppose two microservices produce sorted logs.

```text
Service A

100
105
110
```

```text
Service B

102
108
120
```

To merge them efficiently:

Use one pointer for each list.

Exactly how Merge Sort works.

Another example:

Searching for two transactions that sum to a payment amount in a sorted ledger.

______________________________________________________________________

# Common Mistakes

## 1. Moving the Wrong Pointer

Understand **why** you're moving it.

Don't guess.

______________________________________________________________________

## 2. Forgetting the Array Must Be Sorted

Many Two Pointer problems rely on ordering.

Without sorting, the reasoning breaks.

______________________________________________________________________

## 3. Infinite Loops

Always ensure at least one pointer moves every iteration.

______________________________________________________________________

## 4. Using Nested Loops

Many Two Pointer problems are disguised O(n²) solutions waiting to be optimized.

______________________________________________________________________

## 5. Crossing Pointers Incorrectly

Loop condition is usually:

```python
while left < right:
```

Not

```python
while left <= right
```

unless the problem specifically requires it.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Can brute force solve it?
1. What's the complexity?
1. Is the array sorted?
1. Can two pointers reduce repeated comparisons?
1. Which pointer should move?
1. Why?

Interviewers care more about **why you moved a pointer** than the pointer movement itself.

______________________________________________________________________

### Common Follow-ups

### Q: Why are Two Pointers O(n)?

Each pointer moves in only one direction.

No pointer revisits earlier positions.

Maximum movements:

```text
Left

n

+

Right

n
```

Total

```text
2n

↓

O(n)
```

______________________________________________________________________

### Q: Can Two Pointers work on unsorted arrays?

Sometimes.

But most classic interview problems require sorted input.

______________________________________________________________________

### Q: Hash Map or Two Pointers?

If sorting is allowed and constant space is desired,

Two Pointers are often preferable.

If original order or indices matter,

Hash Maps are usually better.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Two Pointers |
| Recognition | Sorted array, pair, reverse, palindrome |
| Time | O(n) |
| Space | O(1) |
| Benefit | Eliminates nested loops |

______________________________________________________________________

# Practice Problems

## Easy

1. Two Sum II
1. Valid Palindrome

## Medium

1. 3Sum
1. Container With Most Water
1. Move Zeroes
1. Sort Colors

## Hard

1. Trapping Rain Water
1. Minimum Window Subsequence

______________________________________________________________________

# Quick Revision

- Two pointers replace many nested loops.
- Most problems require a sorted array.
- Opposite-direction pointers compare ends.
- Same-direction pointers compact or partition data.
- Fast/Slow pointers are common in linked lists.
- Sliding Window is a specialized Two Pointer pattern.
- Every pointer movement must have a logical reason.
- Time: **O(n)**, Space: **O(1)**.

______________________________________________________________________

# What's Next?

We'll begin with the most important Two Pointer interview problem:

**12-two-sum-ii.md**

This teaches how sorted arrays allow us to replace a Hash Map with constant-space pointer movement.

______________________________________________________________________

# Navigation

**Previous**

[10-longest-consecutive-sequence.md](10-longest-consecutive-sequence.md)

**Next**

[12-two-sum-ii.md](12-two-sum-ii.md)
