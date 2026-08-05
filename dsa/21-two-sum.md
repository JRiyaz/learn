# 21-two-sum.md

# Two Sum

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | ⭐⭐⭐⭐⭐ Extremely High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 20–25 minutes |
| Revision Time | 15 minutes |

______________________________________________________________________

# Why Interviewers Ask This

If there is **one problem** you should absolutely master for interviews,

it's **Two Sum**.

This problem introduces one of the most important interview patterns:

> **Hash Map for Fast Lookup**

Interviewers are testing whether you can:

- Replace nested loops with a Hash Map
- Trade memory for speed
- Recognize complements
- Solve lookup problems efficiently

This single pattern appears in dozens of interview questions:

- Two Sum
- Three Sum
- Four Sum
- Contains Duplicate
- Group Anagrams
- Intersection of Arrays
- Subarray Sum Equals K
- Longest Consecutive Sequence

Master this problem thoroughly.

______________________________________________________________________

# Problem Statement

Given an integer array `numbers`

and an integer `target`,

return the **indices** of the two numbers whose sum equals the target.

You may assume:

- Exactly one valid answer exists.
- You cannot use the same element twice.

______________________________________________________________________

## Example 1

```text
Input

numbers = [2,7,11,15]

target = 9
```

Output

```text
[0,1]
```

Because

```
2 + 7 = 9
```

______________________________________________________________________

## Example 2

```text
Input

numbers = [3,2,4]

target = 6
```

Output

```text
[1,2]
```

______________________________________________________________________

## Example 3

```text
Input

numbers = [3,3]

target = 6
```

Output

```text
[0,1]
```

______________________________________________________________________

# Simple English

Imagine you have shopping bills.

```
2

7

11

15
```

You want two bills that total

```
9
```

Instead of trying every pair,

ask yourself:

```
Current Bill = 2

Need

7
```

Can you quickly check whether

```
7
```

exists?

That's exactly what a Hash Map helps us do.

______________________________________________________________________

# Backend Engineering Analogy

Suppose an e-commerce system receives an order.

```
Order Total

₹1000
```

You want to find two coupons whose values add up to

```
₹1000
```

Instead of comparing every coupon with every other coupon,

store previously seen coupons in a Hash Map.

Lookup becomes instant.

Similar ideas appear in:

- Cache lookups
- Database indexing
- API request deduplication
- Authentication token lookup

______________________________________________________________________

# Pattern Recognition

## Pattern

**Hash Map + Complement Lookup**

______________________________________________________________________

## Recognition Clues

Whenever the problem contains:

- Two numbers
- Pair sum
- Find complement
- Lookup
- Target value

Think

```
Target

-

Current Number

=

Complement
```

Use a Hash Map.

______________________________________________________________________

# Brute Force Solution

## Intuition

Try every possible pair.

If the sum matches,

return the indices.

______________________________________________________________________

## Algorithm

Input

```
[2,7,11,15]

Target

9
```

Check

```
2 + 7

=

9

✔
```

Return

```
[0,1]
```

______________________________________________________________________

## Dry Run

Input

```
[3,2,4]

Target

6
```

Compare

```
3 + 2

=

5
```

No.

______________________________________________________________________

Compare

```
3 + 4

=

7
```

No.

______________________________________________________________________

Compare

```
2 + 4

=

6

✔
```

Return

```
[1,2]
```

______________________________________________________________________

## Complexity

Nested loops.

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

For

```
100,000
```

elements,

nested loops become impractical.

Can we search in constant time?

Yes.

______________________________________________________________________

# Optimized Solution (Hash Map)

## Key Insight

Instead of asking:

```
Who pairs with me?
```

Ask

```
What number do I need?
```

Formula

```
Complement

=

Target

-

Current Number
```

Before processing the current number,

check whether the complement has already been seen.

If yes,

we're done.

Otherwise,

store the current number.

______________________________________________________________________

# Step-by-Step Algorithm

Input

```
Numbers

[2,7,11,15]

Target

9
```

Initially

```
Hash Map

{}
```

______________________________________________________________________

Read

```
2
```

Need

```
7
```

Hash Map

```
{}
```

Not found.

Store

```
2 → Index 0
```

______________________________________________________________________

Read

```
7
```

Need

```
2
```

Hash Map

```
{2 : 0}
```

Found.

Return

```
[0,1]
```

Done.

______________________________________________________________________

# Dry Run

Input

```
[3,2,4]

Target

6
```

______________________________________________________________________

Read

```
3
```

Need

```
3
```

Map

```
{}
```

Store

```
3 → 0
```

______________________________________________________________________

Read

```
2
```

Need

```
4
```

Not found.

Store

```
2 → 1
```

______________________________________________________________________

Read

```
4
```

Need

```
2
```

Found.

Return

```
[1,2]
```

______________________________________________________________________

# Visual Explanation

```
Numbers

2

7

11

15
```

```
Hash Map

{}
```

↓

Store

```
2 : 0
```

↓

Need

```
2
```

↓

Found

↓

Answer

```
0 1
```

______________________________________________________________________

# Why This Works

Loop Invariant:

> Before processing the current element, the hash map contains every previously seen number and its index.

For each number,

there are only two possibilities:

### Case 1

Its complement has already appeared.

Return immediately.

______________________________________________________________________

### Case 2

Complement hasn't appeared.

Store the current number.

Since every element is processed exactly once,

the first valid pair will always be found.

______________________________________________________________________

# Why Do We Check Before Inserting?

Consider

```
[3,3]

Target

6
```

First

```
3
```

Need

```
3
```

Map is empty.

Store

```
3 → 0
```

Second

```
3
```

Need

```
3
```

Found.

Return

```
0 1
```

If we inserted before checking,

we could accidentally match an element with itself.

______________________________________________________________________

# Edge Cases

### Two Elements

```
[2,7]
```

Works immediately.

______________________________________________________________________

### Duplicate Numbers

```
[3,3]
```

Handled correctly.

______________________________________________________________________

### Negative Numbers

```
[-3,4,3,90]

Target

0
```

Answer

```
[-3,3]
```

Works correctly.

______________________________________________________________________

### Zero

```
[0,4,3,0]

Target

0
```

Answer

```
0

+

0
```

Correct.

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

Each lookup and insertion into the Hash Map takes **O(1)** on average.

Space

```
O(n)
```

Worst case,

every element is stored.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def two_sum(numbers: List[int], target: int) -> List[int]:
    for first in range(len(numbers)):
        for second in range(first + 1, len(numbers)):
            if numbers[first] + numbers[second] == target:
                return [first, second]

    return []
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import Dict, List


def two_sum(numbers: List[int], target: int) -> List[int]:
    indices: Dict[int, int] = {}

    for index, number in enumerate(numbers):
        complement = target - number

        if complement in indices:
            return [indices[complement], index]

        indices[number] = index

    return []


if __name__ == "__main__":
    values = [2, 7, 11, 15]

    print(two_sum(values, 9))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Checking every pair.

Use a Hash Map instead.

______________________________________________________________________

## Mistake 2

Storing first,

then checking.

Always

```
Check

↓

Store
```

______________________________________________________________________

## Mistake 3

Returning values instead of indices.

The problem asks for

```
Indices
```

______________________________________________________________________

## Mistake 4

Thinking Hash Maps are always O(1).

Technically,

lookup is

```
Average

O(1)
```

Worst case

```
O(n)
```

because of hash collisions.

Modern hash table implementations make collisions rare.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The brute-force solution checks every possible pair, giving O(n²) time complexity. Instead, I can use a hash map to store previously seen numbers and their indices. For each current number, I calculate the complement (`target - current`) and check whether it already exists in the map. This reduces the time complexity to O(n) while using O(n) extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why calculate the complement?**

Because if

```
a + b = target
```

then

```
b = target - a
```

______________________________________________________________________

**Q. Why check before inserting?**

To avoid pairing an element with itself.

______________________________________________________________________

**Q. What if there are multiple answers?**

This problem guarantees exactly one solution.

Other variants may require returning all pairs.

______________________________________________________________________

**Q. Why use a Hash Map instead of sorting?**

Sorting changes the original indices.

Although sorting plus two pointers is possible,

extra work is required to preserve indices.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Hash Map Lookup |
| Recognition | Pair Sum / Complement |
| Brute Force | Nested Loops |
| Optimized | Hash Map |
| Time | O(n) |
| Space | O(n) |

______________________________________________________________________

# Quick Revision

- Compute the complement: `target - current`.
- Check the Hash Map first.
- Store the current number afterward.
- Return indices, not values.
- Time complexity is O(n).
- Space complexity is O(n).
- Hash Maps trade memory for speed.
- This is one of the most reusable interview patterns.

______________________________________________________________________

# Practice Questions

## Easy

1. Contains Duplicate
1. Intersection of Two Arrays
1. Happy Number

______________________________________________________________________

## Medium

4. Two Sum II - Input Array Is Sorted
1. Three Sum
1. Four Sum
1. Subarray Sum Equals K

______________________________________________________________________

## Hard (Optional)

8. 4Sum II
1. Count of Range Sum
1. Minimum Window Substring

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning the **Hash Map + Complement** pattern. Instead of searching for a
matching pair using nested loops, transform the problem into a **constant-time lookup** by asking, *"What value do I
need to reach the target?"* This way of thinking appears throughout interview questions involving lookups, frequencies,
caching, and indexing.

______________________________________________________________________

# Next

[22-contains-duplicate.md](22-contains-duplicate.md)
