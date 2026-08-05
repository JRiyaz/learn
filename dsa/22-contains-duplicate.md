# 22-contains-duplicate.md

# Contains Duplicate

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 10–15 minutes |
| Revision Time | 5 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This looks like one of the simplest array questions.

In reality, interviewers use it to test whether you can:

- Recognize when **Hash Set** is better than a list
- Perform fast membership lookups
- Optimize from **O(n²)** to **O(n)**
- Choose the correct data structure

This is usually the first interview problem where you'll learn:

> **Hash Set = Fast Existence Check**

Understanding this pattern helps with problems like:

- Longest Consecutive Sequence
- Happy Number
- Valid Sudoku
- Detect Cycle
- Remove Duplicates
- Word Break

______________________________________________________________________

# Problem Statement

Given an integer array,

return

```text
True
```

if **any value appears more than once**.

Otherwise return

```text
False
```

______________________________________________________________________

## Example 1

```text
Input

[1,2,3,1]
```

Output

```text
True
```

Because

```
1
```

appears twice.

______________________________________________________________________

## Example 2

```text
Input

[1,2,3,4]
```

Output

```text
False
```

Every value is unique.

______________________________________________________________________

## Example 3

```text
Input

[1,1,1,3,3,4,3,2,4,2]
```

Output

```text
True
```

______________________________________________________________________

# Simple English

Imagine people entering a building.

Every person has an ID card.

As each person enters,

you ask:

> "Have I already seen this ID?"

If yes,

there is a duplicate.

You don't need to count everyone.

You only need to remember **who has already entered**.

______________________________________________________________________

# Backend Engineering Analogy

Suppose your API receives request IDs.

```
REQ-101

REQ-102

REQ-101
```

The third request is a duplicate.

To detect duplicate requests,

systems store previously seen IDs in a **Hash Set**.

This technique is widely used in:

- Idempotency keys
- Request deduplication
- Fraud detection
- Cache validation
- Event processing
- Kafka consumer deduplication

______________________________________________________________________

# Pattern Recognition

## Pattern

**Hash Set (Fast Membership Check)**

______________________________________________________________________

## Recognition Clues

Whenever the problem contains:

- Duplicate
- Already seen
- Exists?
- Visited
- Unique values

Think

```
Hash Set
```

instead of

```
List
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Compare every number with every other number.

If any pair matches,

return

```
True
```

______________________________________________________________________

## Algorithm

Input

```
[1,2,3,1]
```

Compare

```
1

↓

2
```

No.

↓

```
1

↓

3
```

No.

↓

```
1

↓

1

✔
```

Duplicate found.

Return

```
True
```

______________________________________________________________________

## Dry Run

Input

```
[4,5,6]
```

Compare

```
4

↓

5
```

No.

↓

```
4

↓

6
```

No.

↓

```
5

↓

6
```

No.

Return

```
False
```

______________________________________________________________________

## Complexity

Time

```
O(n²)
```

Space

```
O(1)
```

______________________________________________________________________

## Limitations

Too many comparisons.

Can we remember what we've already seen?

Yes.

______________________________________________________________________

# Optimized Solution (Hash Set)

## Key Insight

Instead of comparing against every previous element,

store previously seen values in a Hash Set.

For each number:

```
Already in set?

↓

Yes

↓

Duplicate
```

Otherwise

```
Store it.
```

______________________________________________________________________

# Step-by-Step Algorithm

Input

```
[1,2,3,1]
```

Initially

```
Seen

{}
```

______________________________________________________________________

Read

```
1
```

Already exists?

```
No
```

Store

```
{1}
```

______________________________________________________________________

Read

```
2
```

Store

```
{1,2}
```

______________________________________________________________________

Read

```
3
```

Store

```
{1,2,3}
```

______________________________________________________________________

Read

```
1
```

Already exists?

```
Yes
```

Return

```
True
```

Done.

______________________________________________________________________

# Dry Run

Input

```
[5,6,7]
```

Seen

```
{}
```

↓

```
5
```

↓

```
{5}
```

↓

```
6
```

↓

```
{5,6}
```

↓

```
7
```

↓

```
{5,6,7}
```

Finished.

No duplicates.

______________________________________________________________________

# Visual Explanation

```
Numbers

1

2

3

1
```

```
Seen

{}
```

↓

```
{1}
```

↓

```
{1,2}
```

↓

```
{1,2,3}
```

↓

Need to insert

```
1
```

Already exists.

Duplicate.

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before processing the current element, the set contains every unique element seen so far.

Each iteration has only two possibilities:

### Case 1

Current number already exists.

Duplicate found.

Return immediately.

______________________________________________________________________

### Case 2

Number not found.

Insert it into the set.

Since every element is processed exactly once,

the first repeated element is detected immediately.

______________________________________________________________________

# Another Optimized Solution

Python allows converting the array into a set.

Example

```python
len(numbers) != len(set(numbers))
```

Why?

Because sets automatically remove duplicates.

Example

```
[1,2,2,3]
```

List length

```
4
```

Set

```
{1,2,3}
```

Length

```
3
```

Different lengths

↓

Duplicate exists.

______________________________________________________________________

# Which Solution Should You Mention?

### During Interviews

Prefer

```python
seen = set()
```

because it demonstrates the algorithm.

### Production Python

Using

```python
len(numbers) != len(set(numbers))
```

is concise and perfectly acceptable.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

Return

```
False
```

______________________________________________________________________

### One Element

```
[5]
```

Return

```
False
```

______________________________________________________________________

### All Duplicates

```
[7,7,7]
```

Return

```
True
```

______________________________________________________________________

### Negative Numbers

```
[-1,-2,-1]
```

Works correctly.

______________________________________________________________________

### Large Input

Still requires only one traversal.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n²)
```

Space

```
O(1)
```

______________________________________________________________________

## Optimized

Time

```
O(n)
```

Average-case lookup and insertion into a Hash Set are O(1).

Space

```
O(n)
```

Worst case,

every element is unique.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def contains_duplicate(numbers: List[int]) -> bool:
    for first in range(len(numbers)):
        for second in range(first + 1, len(numbers)):
            if numbers[first] == numbers[second]:
                return True

    return False
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List, Set


def contains_duplicate(numbers: List[int]) -> bool:
    seen: Set[int] = set()

    for number in numbers:
        if number in seen:
            return True

        seen.add(number)

    return False


if __name__ == "__main__":
    values = [1, 2, 3, 1]

    print(contains_duplicate(values))
```

______________________________________________________________________

## Pythonic Solution

```python
from typing import List


def contains_duplicate(numbers: List[int]) -> bool:
    return len(numbers) != len(set(numbers))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using a list instead of a set.

Checking

```python
if number in list
```

takes

```
O(n)
```

Checking

```python
if number in set
```

takes

```
Average O(1)
```

______________________________________________________________________

## Mistake 2

Counting frequencies unnecessarily.

The problem only asks:

```
Does a duplicate exist?
```

A set is enough.

______________________________________________________________________

## Mistake 3

Thinking sets preserve insertion order.

Historically, sets are considered unordered collections.

Don't rely on their order in algorithms.

______________________________________________________________________

## Mistake 4

Confusing Hash Set with Hash Map.

Hash Set

```
Stores values only.
```

Hash Map

```
Stores key-value pairs.
```

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The brute-force solution compares every pair, resulting in O(n²) time. Since I only need to know whether I've seen a value before, I can use a Hash Set. As I iterate through the array, I check whether the current number already exists in the set. If it does, I return `True`; otherwise, I insert it and continue. This reduces the time complexity to O(n)."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why use a Hash Set instead of a Hash Map?**

Because we only care about existence,

not counts or indices.

______________________________________________________________________

**Q. Why not sort the array first?**

Sorting gives

```
O(n log n)
```

The Hash Set solution is faster:

```
O(n)
```

______________________________________________________________________

**Q. When would a Hash Map be better?**

When you need:

- frequencies
- indices
- additional information

______________________________________________________________________

**Q. Why is Hash Set lookup O(1)?**

Because hashing allows direct access to the bucket where the value is stored.

Average-case performance is O(1).

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Hash Set |
| Recognition | Duplicate / Already Seen |
| Brute Force | Nested Loops |
| Optimized | Hash Set |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Quick Revision

- Duplicate detection is an existence problem.
- Hash Set is ideal for existence checks.
- Check before inserting.
- Stop immediately after finding a duplicate.
- Average lookup is O(1).
- Time complexity is O(n).
- Space complexity is O(n).
- This pattern appears in many graph, array, and string problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Happy Number
1. Missing Number
1. Single Number

______________________________________________________________________

## Medium

4. Longest Consecutive Sequence
1. Valid Sudoku
1. Find All Duplicates in an Array
1. Intersection of Two Arrays II

______________________________________________________________________

## Hard (Optional)

8. First Missing Positive
1. N-Queens
1. Word Ladder

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is recognizing **existence-check problems**. Whenever a question asks, *"Have I
already seen this value?"*, your first instinct should be **Hash Set**. This simple pattern replaces expensive repeated
searches with constant-time lookups and is one of the most commonly used techniques in backend systems and coding
interviews.

______________________________________________________________________

# Next

[23-group-anagrams.md](23-group-anagrams.md)
