# 02-arrays.md

# Arrays — The Foundation of Almost Every DSA Problem

## Interview Confidence

**Difficulty:** ⭐☆☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 15–20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Why Interviewers Ask This

If you look at the majority of coding interview questions, you'll notice something interesting:

> Almost every problem either directly uses an array or can be converted into one.

Examples:

- Search products
- Find duplicates
- Compute statistics
- Sliding Window
- Two Pointers
- Prefix Sum
- Dynamic Programming

Even strings are simply arrays of characters.

If you become comfortable thinking in terms of arrays, you've already built the foundation for more than half of the
interview patterns you'll encounter.

Interviewers are not testing whether you know Python lists.

They're testing whether you understand:

- memory layout
- iteration
- indexing
- trade-offs
- how to recognize array-based problems

______________________________________________________________________

# Learning Objectives

After this lesson, you should be able to:

✅ Explain what an array really is.

✅ Explain why arrays are fast.

✅ Understand random access.

✅ Understand insertion/deletion costs.

✅ Recognize array interview questions.

✅ Know when arrays are the wrong choice.

______________________________________________________________________

# What Is an Array?

Most beginners think:

> "An array is a list."

That's true from a programming perspective.

But interviewers expect a lower-level understanding.

A better definition is:

> An array is a collection of elements stored **contiguously in memory**.

The keyword is:

**contiguous**

That means the elements live one after another.

Imagine apartment numbers:

```
101
102
103
104
105
```

Each apartment is adjacent.

Arrays work similarly.

```
Memory

+----+----+----+----+----+
| 10 | 20 | 30 | 40 | 50 |
+----+----+----+----+----+
```

The computer knows:

- first address
- element size

From those two pieces of information, it can compute the location of any element instantly.

______________________________________________________________________

# Why Contiguous Memory Matters

Suppose the first element starts at address:

```
1000
```

Each integer occupies:

```
4 bytes
```

Then memory looks like this:

```
Address      Value

1000         10
1004         20
1008         30
1012         40
1016         50
```

Need index 3?

Computer computes:

```
Address = Base + Index × Size

1000 + (3 × 4)

= 1012
```

No searching.

No scanning.

Just arithmetic.

This is why indexing is **O(1)**.

______________________________________________________________________

# Real-World Backend Analogy

Suppose your API returns:

```json
[
  "Laptop",
  "Mouse",
  "Keyboard",
  "Monitor"
]
```

Internally:

```
products[0]

products[1]

products[2]
```

Another example:

Kafka consumer receives:

```
Batch

Message1
Message2
Message3
Message4
```

The batch is usually represented as an array.

Analytics systems:

```
Daily Revenue

[1200, 1500, 1700, 1600]
```

Image processing:

Every image is essentially a 2D array.

Machine Learning:

Feature vectors are arrays.

Database query results:

Rows are often materialized as arrays or array-like structures before processing.

Arrays are everywhere.

______________________________________________________________________

# Array Operations

Let's examine the cost of common operations.

______________________________________________________________________

## Access by Index

Example:

```python
numbers = [10, 20, 30, 40]

print(numbers[2])
```

Output

```
30
```

Time Complexity

```
O(1)
```

Why?

Direct address calculation.

______________________________________________________________________

## Traverse

```python
for value in numbers:
    print(value)
```

Visits every element once.

Complexity

```
O(n)
```

______________________________________________________________________

## Search

Find:

```
40
```

Need to inspect:

```
10

↓

20

↓

30

↓

40
```

Worst case

```
O(n)
```

Unless the array has additional properties (such as being sorted).

______________________________________________________________________

## Insert at End

```
Before

10 20 30

↓

Append 40

↓

10 20 30 40
```

Average complexity:

```
O(1)
```

Occasionally, the array grows and elements are copied into a larger block, making a single append costlier, but over
many appends the average remains O(1) (amortized).

______________________________________________________________________

## Insert at Beginning

Before

```
10 20 30 40
```

Insert:

```
5
```

Everything shifts.

```
5 10 20 30 40
```

Complexity

```
O(n)
```

______________________________________________________________________

## Delete First Element

```
10 20 30 40

↓

20 30 40
```

Everything shifts left.

```
O(n)
```

______________________________________________________________________

## Delete Last Element

```
10 20 30

↓

10 20
```

```
O(1)
```

______________________________________________________________________

# Visual Summary

```
Operation          Complexity

Access             O(1)

Update             O(1)

Traversal          O(n)

Search             O(n)

Append             O(1) amortized

Insert Front       O(n)

Delete Front       O(n)

Delete End         O(1)
```

______________________________________________________________________

# Static vs Dynamic Arrays

Many interview questions use the word "array," but languages differ.

## Static Array

Size fixed.

```
[ _ ][ _ ][ _ ][ _ ]
```

Cannot grow.

Languages:

- C
- C++

______________________________________________________________________

## Dynamic Array

Automatically resizes.

Python list.

Java ArrayList.

C++ vector.

Go slices.

When full:

```
Old

+----+----+----+
|10|20|30|
+----+----+----+
```

Allocate a larger block.

```
+----+----+----+----+----+----+
|10|20|30|
+----+----+----+----+----+----+
```

Copy elements.

Continue.

______________________________________________________________________

# Python Lists Are Dynamic Arrays

When you write:

```python
numbers = []
```

You are **not** creating a linked list.

Python's built-in `list` is implemented as a dynamic array.

That's why:

```python
numbers[100]
```

is still O(1).

______________________________________________________________________

# When Arrays Are a Bad Choice

Arrays are excellent when:

- frequent indexing
- sequential processing
- cache-friendly access
- fixed or append-heavy workloads

Arrays are poor when:

- frequent insertion at the front
- frequent deletion from the middle
- unknown insertion positions

Example:

Implement browser history.

A linked list (or more commonly, stacks) may be more appropriate depending on the operations required.

______________________________________________________________________

# Pattern Recognition

When should you think "This is an array problem"?

Common interview clues:

- Given an array...
- Given a list of numbers...
- Return indices...
- Find duplicates...
- Maximum/minimum...
- Prefix...
- Consecutive...
- Running total...
- Rearrange...
- Rotate...
- Reverse...
- Merge...

These keywords often indicate array-based reasoning.

______________________________________________________________________

# Common Problems

These classic problems introduce the most important array patterns.

## Easy

- Two Sum
- Contains Duplicate
- Best Time to Buy and Sell Stock

## Medium

- Product of Array Except Self
- Rotate Array
- Maximum Product Subarray
- Merge Intervals
- Set Matrix Zeroes
- Spiral Matrix

## Hard (Optional)

- Trapping Rain Water
- First Missing Positive

Notice that each of these later teaches a different pattern rather than "more array knowledge."

______________________________________________________________________

# How Array Problems Usually Evolve

Interviewers often start with a simple scan.

```
Read

↓

Compare

↓

Track

↓

Return
```

Then they introduce constraints:

- Can you do it in one pass?
- Can you reduce memory?
- Can you avoid sorting?
- Can you use two pointers?
- Can you use a hash map?

Learning to recognize these progressions is more valuable than memorizing solutions.

______________________________________________________________________

# Common Mistakes

## 1. Off-by-One Errors

Example:

```python
for i in range(len(nums)):
```

vs.

```python
for i in range(len(nums) - 1):
```

Always verify loop boundaries.

______________________________________________________________________

## 2. Modifying While Iterating

```python
for value in numbers:
    if value == 5:
        numbers.remove(value)
```

This can skip elements because indices shift.

______________________________________________________________________

## 3. Assuming Search Is O(1)

Only index access is O(1).

Searching an unsorted array is O(n).

______________________________________________________________________

## 4. Forgetting Edge Cases

Always think about:

- empty array
- one element
- duplicates
- negative numbers
- already sorted
- all identical values

______________________________________________________________________

## 5. Using Extra Memory Unnecessarily

Many problems can be solved in-place.

Interviewers often ask:

> "Can you do it without allocating another array?"

______________________________________________________________________

# Follow-up Questions

### 1. Why is indexing O(1)?

Because the address is computed directly using the base address and index.

______________________________________________________________________

### 2. Why is searching O(n)?

Because, in an unsorted array, any element could contain the target.

______________________________________________________________________

### 3. Why is inserting at the front expensive?

Every subsequent element must shift one position.

______________________________________________________________________

### 4. Why is appending usually O(1)?

Dynamic arrays reserve extra capacity, so most appends don't require resizing.

______________________________________________________________________

### 5. Why are arrays cache-friendly?

Contiguous memory improves CPU cache locality, reducing memory access latency.

______________________________________________________________________

### 6. When would you choose a linked list instead?

When frequent insertions and deletions at arbitrary positions dominate and random access isn't required.

______________________________________________________________________

### 7. Are Python tuples arrays?

Tuples are immutable sequence types backed by contiguous storage concepts, but unlike lists they cannot be resized after
creation.

______________________________________________________________________

### 8. Why are arrays preferred in analytics workloads?

Sequential access is fast and cache-efficient.

______________________________________________________________________

# Quick Revision

- Arrays store elements contiguously.
- Random access is O(1).
- Searching an unsorted array is O(n).
- Appending is O(1) amortized.
- Inserting at the front is O(n).
- Python lists are dynamic arrays.
- Arrays are cache-friendly.
- Most interview questions start with arrays.
- Always think about indexing, scanning, and trade-offs.

______________________________________________________________________

# Practice Questions

## Easy

1. Two Sum
1. Best Time to Buy and Sell Stock

## Medium

1. Product of Array Except Self
1. Rotate Array
1. Maximum Subarray
1. Merge Intervals

## Hard

1. Trapping Rain Water
1. First Missing Positive

> **Do not solve these yet.** We will cover them in a carefully chosen order.

______________________________________________________________________

# What's Next?

The first representative problem for arrays is one of the most important interview questions because it introduces your
first optimization pattern.

## Next Lesson

**03-two-sum.md**

You'll learn:

- How interviewers expect you to think.
- How to move from brute force to an optimized solution.
- Why a hash map transforms an O(n²) solution into O(n).
- How to recognize when this pattern applies to entirely different problems.

This lesson will use the full deep-dive format with problem statement, brute force, optimized solution, proofs,
diagrams, edge cases, interview discussion, production-quality Python code, and related variations.

______________________________________________________________________

# Navigation

**Previous**

[01-time-complexity.md](01-time-complexity.md)

**Next**

[03-two-sum.md](03-two-sum.md)
