# Time Complexity & Algorithm Analysis

## Interview Confidence

Difficulty: ⭐☆☆☆☆

Asked Frequency: ⭐⭐⭐⭐⭐

Importance: ⭐⭐⭐⭐⭐

Expected Interview Time: 15 minutes

Revision Time: 3 minutes

______________________________________________________________________

# Why Interviewers Ask This

Before an interviewer evaluates whether you know a particular algorithm, they evaluate **how you think**.

Most interview questions are not about arriving at the correct answer. They are about whether you can:

- compare multiple approaches
- reason about efficiency
- identify bottlenecks
- improve an existing solution

This is why almost every interview eventually includes questions like:

> "Can you do better?"

or

> "What's the time complexity?"

If you cannot answer those confidently, even a correct solution often isn't considered complete.

______________________________________________________________________

# Concept

Imagine you wrote two APIs.

API A processes one million users in **1 second**.

API B processes one million users in **2 minutes**.

Both are correct.

Which one would your company deploy?

Obviously API A.

Interviewers think exactly the same way.

They don't only care **whether** your algorithm works.

They care:

- How fast?
- How much memory?
- Will it still work if the input becomes huge?

Time Complexity is simply a language for answering those questions.

______________________________________________________________________

# Real-World Analogy

Suppose your backend service needs to search a user.

### Approach 1

Read every user from the database until you find the correct one.

```
User1
User2
User3
...
User999999
```

Worst case:

You inspect every row.

______________________________________________________________________

### Approach 2

The user table has an index.

The database immediately jumps to the row.

```
B-Tree Index

        M
      /   \
     G     T
```

Much fewer operations.

Same result.

Huge performance difference.

That's what algorithms are about.

______________________________________________________________________

# What Time Complexity Actually Measures

A common misunderstanding:

It does **NOT** measure seconds.

Instead, it measures:

> How does the number of operations grow as the input size grows?

Suppose:

```
n = number of elements
```

If input doubles,

How much extra work do we do?

That is Time Complexity.

______________________________________________________________________

# Constant Time — O(1)

Example

```python
value = numbers[5]
```

No matter whether the list has

```
10 elements

100 elements

10 million elements
```

Still one lookup.

ASCII

```
Input Size

10 -----------> 1 operation

100 ----------> 1 operation

1000 ---------> 1 operation
```

Always constant.

Backend example:

Redis lookup.

Dictionary lookup.

Array indexing.

______________________________________________________________________

# Linear Time — O(n)

Example

```python
for num in numbers:
    print(num)
```

Every new element is visited once.

```
10 elements

↓

10 operations

100 elements

↓

100 operations

1000 elements

↓

1000 operations
```

Growth is proportional.

______________________________________________________________________

Backend examples

- scanning logs
- reading CSV
- processing Kafka messages
- validating uploaded records

______________________________________________________________________

# Quadratic Time — O(n²)

Nested loops.

```python
for i in numbers:
    for j in numbers:
        ...
```

Example

```
5 elements

25 comparisons

100 elements

10000 comparisons
```

ASCII

```
n

↓

Loop 1

↓

Loop 2

↓

n × n
```

Growth becomes explosive.

______________________________________________________________________

Backend example

Comparing every user with every other user.

Duplicate detection using nested loops.

______________________________________________________________________

# Logarithmic Time — O(log n)

Imagine searching a dictionary.

You don't start at page 1.

You open somewhere in the middle.

If the word is later,

Discard half.

Repeat.

```
1000 pages

↓

500

↓

250

↓

125

↓

63

↓

31

↓

16

↓

8

↓

4

↓

2

↓

1
```

Very efficient.

Backend examples

- Database indexes
- Binary Search
- B-Trees
- Segment Trees

______________________________________________________________________

# Linearithmic Time — O(n log n)

Algorithms like Merge Sort.

```
Split

↓

Split

↓

Merge

↓

Merge
```

Many efficient sorting algorithms belong here.

______________________________________________________________________

# Exponential Time — O(2ⁿ)

Every decision branches.

Example

```
Take element

Don't take element

↓

Take

Don't take

↓

Take

Don't take
```

Number of possibilities doubles repeatedly.

Typical in:

- Backtracking
- Naive recursion

______________________________________________________________________

# Factorial Time — O(n!)

Every possible ordering.

Example

```
ABC

ACB

BAC

BCA

CAB

CBA
```

Very expensive.

Usually appears in permutation problems.

______________________________________________________________________

# Big-O Doesn't Count Constants

Suppose

```python
for num in numbers:
    ...

for num in numbers:
    ...
```

Operations

```
2n
```

Big-O

```
O(n)
```

Constants are ignored.

______________________________________________________________________

Similarly

```
5n

100n

0.5n
```

All are simply

```
O(n)
```

______________________________________________________________________

# Dropping Smaller Terms

Example

```
n² + n
```

As n becomes huge,

```
1,000,000²

vs

1,000,000
```

The quadratic term dominates.

Therefore

```
O(n²)
```

______________________________________________________________________

# Space Complexity

Time measures work.

Space measures memory.

Example

```python
copy = []

for num in numbers:
    copy.append(num)
```

Extra memory grows with n.

Space

```
O(n)
```

______________________________________________________________________

Example

```python
total = 0

for num in numbers:
    total += num
```

Only one variable.

Space

```
O(1)
```

______________________________________________________________________

# Complexity Cheat Sheet

| Complexity | Name | Practical |
|------------|------|-----------|
| O(1) | Constant | Excellent |
| O(log n) | Logarithmic | Excellent |
| O(n) | Linear | Very Good |
| O(n log n) | Linearithmic | Good |
| O(n²) | Quadratic | Acceptable only for small inputs |
| O(2ⁿ) | Exponential | Usually too slow |
| O(n!) | Factorial | Almost never acceptable |

______________________________________________________________________

# Pattern Recognition

Whenever you solve a problem, ask yourself:

1. How many loops?

1. Does each loop visit everything?

1. Is recursion branching?

1. Is data being copied?

1. Can previous work be reused?

These five questions alone solve most complexity discussions.

______________________________________________________________________

# Common Problems

These interview questions frequently begin with brute-force solutions whose main purpose is to improve complexity:

- Two Sum
- Contains Duplicate
- Product of Array Except Self
- Merge Intervals
- Binary Search
- Valid Parentheses
- Number of Islands
- Kth Largest Element

______________________________________________________________________

# Brute Force Approach

A brute-force solution focuses on correctness first.

Example:

Find duplicates.

Brute force:

Compare every element with every other element.

```
1

↓

2

↓

3

↓

4
```

Nested loops.

Time Complexity:

```
O(n²)
```

Space:

```
O(1)
```

Simple but inefficient.

______________________________________________________________________

# Better Approach

Ask:

Can I remember what I've already seen?

Use a hash set.

```
Seen

↓

{}

↓

Add

↓

Check

↓

Duplicate?
```

Time Complexity:

```
O(n)
```

Space:

```
O(n)
```

A common interview optimization.

______________________________________________________________________

# Optimal Approach

The "optimal" solution depends on constraints.

Sometimes the fastest algorithm uses more memory.

Sometimes less memory is preferred.

Always discuss the trade-off before coding.

Interviewers value this reasoning.

______________________________________________________________________

# Dry Run

Example:

```
[3, 1, 4, 1]
```

Brute force:

```
3 vs 1
3 vs 4
3 vs 1

1 vs 4

1 vs 1

Duplicate found
```

Hash Set:

```
{}

↓

3

↓

{3}

↓

1

↓

{3,1}

↓

4

↓

{3,1,4}

↓

1 already exists

Duplicate
```

______________________________________________________________________

# Python Template

```python
from typing import List


def process(items: List[int]) -> int:
    """
    Demonstrates a simple linear scan.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    total = 0

    for item in items:
        total += item

    return total
```

______________________________________________________________________

# Common Mistakes

1. Counting constants in Big-O.
1. Forgetting nested loops become O(n²).
1. Ignoring auxiliary memory.
1. Assuming recursion uses no space.
1. Confusing average case and worst case.
1. Believing Big-O measures seconds.
1. Forgetting that hash tables use extra memory.

______________________________________________________________________

# Follow-up Questions

### 1. Is O(2n) different from O(n)?

No. Constants are ignored.

______________________________________________________________________

### 2. Is O(log n) faster than O(n)?

Yes, especially for very large inputs.

______________________________________________________________________

### 3. Can O(n²) ever be acceptable?

Yes, when the input size is very small.

______________________________________________________________________

### 4. Why do interviewers ask for complexity before code?

They want to evaluate your reasoning process, not just your implementation.

______________________________________________________________________

### 5. Is lower space complexity always better?

Not necessarily. Trading memory for speed is common in backend systems.

______________________________________________________________________

# Quick Revision

- Time Complexity measures growth, not seconds.
- Space Complexity measures extra memory.
- Big-O ignores constants.
- Dominant terms determine complexity.
- Hash maps often trade space for speed.
- Nested loops are usually O(n²).
- Binary search is O(log n).
- Always discuss trade-offs before coding.

______________________________________________________________________

# Practice Questions

## Easy

1. Two Sum
1. Contains Duplicate

## Medium

1. Product of Array Except Self
1. Top K Frequent Elements
1. Group Anagrams
1. Longest Consecutive Sequence

## Hard

1. Median of Two Sorted Arrays
1. Trapping Rain Water

______________________________________________________________________

# Navigation

**Previous**

None

**Next**

[02-arrays.md](02-arrays.md)
