# 06-hash-maps.md

# Hash Maps — The Most Important Data Structure for Interviews

## Interview Confidence

**Difficulty:** ⭐⭐☆☆☆

**Asked Frequency:** ⭐⭐⭐⭐⭐

**Importance:** ⭐⭐⭐⭐⭐

**Expected Interview Time:** 20 minutes

**Revision Time:** 5 minutes

______________________________________________________________________

# Why Interviewers Ask This

Hash Maps are one of the most frequently used data structures in coding interviews.

Many problems that initially appear to require nested loops can be optimized using a Hash Map.

Typical examples include:

- Two Sum
- Group Anagrams
- Top K Frequent Elements
- Subarray Sum Equals K
- LRU Cache
- Copy List with Random Pointer

If you understand Hash Maps well, you'll solve a large percentage of Easy and Medium interview questions efficiently.

______________________________________________________________________

# Learning Objectives

After this lesson, you should be able to:

- Explain what a Hash Map is.
- Understand hashing at a high level.
- Know when to use a Hash Map.
- Distinguish between Hash Maps and Hash Sets.
- Recognize interview patterns involving Hash Maps.

______________________________________________________________________

# What Is a Hash Map?

A Hash Map stores **key-value pairs**.

Example:

```python
student_marks = {
    "Alice": 95,
    "Bob": 88,
    "Charlie": 91,
}
```

Here,

```text
Key      Value

Alice -> 95
Bob   -> 88
Charlie -> 91
```

You retrieve values using keys.

```python
print(student_marks["Alice"])
```

Output

```text
95
```

______________________________________________________________________

# Real-World Analogy

Imagine a company employee directory.

Without a Hash Map:

```text
Search employee ID

↓

Read every record
```

With a Hash Map:

```text
Employee ID

↓

Direct lookup

↓

Employee details
```

Backend examples:

- User ID → User Profile
- Session ID → Session Data
- Product ID → Product
- JWT Token → User
- Cache Key → Cached Response

______________________________________________________________________

# Hash Map vs Array

Array

```text
Index -> Value

0 -> Apple

1 -> Mango

2 -> Orange
```

Hash Map

```text
Key -> Value

"apple" -> 100

"banana" -> 80

"mango" -> 120
```

Arrays require numeric indices.

Hash Maps allow meaningful keys.

______________________________________________________________________

# How Does a Hash Map Work?

Suppose you store:

```python
prices["apple"] = 120
```

Internally:

```text
"apple"

↓

Hash Function

↓

Large Integer

↓

Bucket

↓

Store Value
```

The hash function converts the key into a number.

That number determines where the value is stored.

You don't need to know the exact algorithm during interviews—just understand that hashing enables very fast lookups.

______________________________________________________________________

# Common Operations

## Insert

```python
prices["apple"] = 120
```

Average Complexity

```text
O(1)
```

______________________________________________________________________

## Lookup

```python
prices["apple"]
```

Average Complexity

```text
O(1)
```

______________________________________________________________________

## Update

```python
prices["apple"] = 150
```

Average Complexity

```text
O(1)
```

______________________________________________________________________

## Delete

```python
del prices["apple"]
```

Average Complexity

```text
O(1)
```

______________________________________________________________________

# Visual Representation

```text
Dictionary

+------------------+

"user1" -> Profile

"user2" -> Profile

"user3" -> Profile

+------------------+
```

Lookup

```text
"user2"

↓

Hash Function

↓

Bucket

↓

Profile
```

______________________________________________________________________

# Hash Map vs Hash Set

Hash Map

```python
{
    "Alice": 95,
    "Bob": 88,
}
```

Stores:

```text
Key + Value
```

Hash Set

```python
{"Alice", "Bob"}
```

Stores:

```text
Only Values
```

Use a Hash Set when you only care whether something exists.

Use a Hash Map when additional information must be stored.

______________________________________________________________________

# When Should You Think "Hash Map"?

Interview clues:

- Count frequency
- Return indices
- Store positions
- Cache results
- Previous occurrence
- Group by something
- Fast lookup
- Complement
- Mapping relationships

Whenever you repeatedly search for information you've already processed, a Hash Map is often the right choice.

______________________________________________________________________

# Common Interview Patterns

## 1. Frequency Counting

Example:

```text
apple

banana

apple

apple
```

Store

```text
apple -> 3

banana -> 1
```

______________________________________________________________________

## 2. Value → Index

Example:

```text
2 -> index 0

7 -> index 1
```

Used in:

- Two Sum

______________________________________________________________________

## 3. Character Counting

```text
aabbccc

↓

a -> 2

b -> 2

c -> 3
```

Used in:

- Valid Anagram
- Ransom Note

______________________________________________________________________

## 4. Grouping

```text
eat

tea

ate
```

Grouped together because they are anagrams.

______________________________________________________________________

## 5. Caching

```text
Request

↓

Cache Lookup

↓

Database

↓

Store Result
```

Very common in backend systems.

______________________________________________________________________

# Python Dictionary Essentials

Create

```python
scores = {}
```

Insert

```python
scores["Alice"] = 95
```

Lookup

```python
scores["Alice"]
```

Safe Lookup

```python
scores.get("Alice")
```

Default Value

```python
scores.get("David", 0)
```

Delete

```python
del scores["Alice"]
```

Check Existence

```python
"Alice" in scores
```

Iterate

```python
for key, value in scores.items():
    print(key, value)
```

______________________________________________________________________

# Useful Python Methods

Count Frequencies

```python
frequency = {}

for num in nums:
    frequency[num] = frequency.get(num, 0) + 1
```

This pattern appears in many interview problems.

______________________________________________________________________

# Complexity Analysis

| Operation | Average |
|-----------|---------|
| Insert | O(1) |
| Lookup | O(1) |
| Update | O(1) |
| Delete | O(1) |
| Iterate | O(n) |

Worst-case complexity can degrade due to hash collisions, but interview discussions generally assume average-case
performance.

______________________________________________________________________

# Common Mistakes

## 1. Confusing Hash Map and Hash Set

Need counts?

Use Hash Map.

Need existence?

Use Hash Set.

______________________________________________________________________

## 2. Forgetting Missing Keys

Wrong

```python
count = frequency[word]
```

Safer

```python
count = frequency.get(word, 0)
```

______________________________________________________________________

## 3. Modifying While Iterating

Avoid changing dictionary size while looping over it.

______________________________________________________________________

## 4. Assuming Order Matters

Modern Python dictionaries preserve insertion order, but interview algorithms usually should not rely on ordering unless
the problem explicitly requires it.

______________________________________________________________________

# Production-Quality Example

Frequency Counter

```python
from typing import Dict, List


def count_frequency(numbers: List[int]) -> Dict[int, int]:
    """
    Counts occurrences of each number.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    frequency: Dict[int, int] = {}

    for number in numbers:
        frequency[number] = frequency.get(number, 0) + 1

    return frequency
```

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

1. Identify repeated lookups.
1. Replace repeated searching with a Hash Map.
1. Explain stored key and value.
1. Analyze complexity.
1. Write clean code.

______________________________________________________________________

### Common Follow-ups

**Q:** Why not use a list?

A list requires O(n) search.

A Hash Map provides O(1) average lookup.

______________________________________________________________________

**Q:** Why not use a database?

A Hash Map is an in-memory data structure optimized for very fast access.

______________________________________________________________________

**Q:** Can keys be mutable?

No.

Keys should be immutable (e.g., integers, strings, tuples).

Lists cannot be dictionary keys.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|-------|
| Pattern | Fast Key-Value Lookup |
| Recognition | Count, map, previous occurrence, cache |
| Primary Data Structure | Hash Map |
| Average Lookup | O(1) |
| Space | O(n) |

______________________________________________________________________

# Practice Questions

## Easy

1. Valid Anagram
1. Ransom Note

## Medium

1. Group Anagrams
1. Top K Frequent Elements
1. Isomorphic Strings
1. Subarray Sum Equals K

## Hard

1. LRU Cache
1. Minimum Window Substring

______________________________________________________________________

# Quick Revision

- Hash Maps store **key-value pairs**.
- Average lookup, insert, update, and delete are **O(1)**.
- Use them to avoid repeated searching.
- Common uses:
  - Frequency counting
  - Value → Index mapping
  - Caching
  - Grouping
- Use `.get(key, default)` to safely access values.
- Use a Hash Set when only existence matters.

______________________________________________________________________

# What's Next?

We'll apply everything from this lesson to one of the most common frequency-counting interview questions:

**Valid Anagram**

This introduces the **Frequency Counting Pattern**, another foundational technique used throughout interview problems.

______________________________________________________________________

# Navigation

**Previous**

[05-contains-duplicate.md](05-contains-duplicate.md)

**Next**

[07-valid-anagram.md](07-valid-anagram.md)
