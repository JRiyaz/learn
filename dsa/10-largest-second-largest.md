# 10-largest-second-largest.md

# Largest & Second Largest Element in an Array

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Easy |
| Asked Frequency | Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 15–20 minutes |
| Revision Time | 10 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This is one of the most frequently asked array interview questions.

At first, it looks simple:

> "Find the largest and second largest number."

But interviewers are actually testing:

- Array traversal
- Keeping track of multiple values
- Thinking about edge cases
- Optimizing from multiple passes to a single pass
- Writing clean conditional logic

This problem also teaches an important interview pattern:

> **Maintain running answers while traversing the array.**

You'll use this same idea in problems like:

- Best Time to Buy & Sell Stock
- Maximum Product Subarray
- Maximum Difference
- Running Maximum
- Sliding Window Maximum

______________________________________________________________________

# Problem Statement

Given an integer array,

find:

- The largest element
- The second largest **distinct** element

If a second largest element doesn't exist,

return `-1`.

______________________________________________________________________

## Example 1

```text
Input

[5, 9, 3, 7, 1]
```

Output

```text
Largest = 9

Second Largest = 7
```

______________________________________________________________________

## Example 2

```text
Input

[10]
```

Output

```text
Largest = 10

Second Largest = -1
```

______________________________________________________________________

## Example 3

```text
Input

[8, 8, 8]
```

Output

```text
Largest = 8

Second Largest = -1
```

Because the second largest must be **distinct**.

______________________________________________________________________

# Simple English

Imagine you're organizing a race.

You don't just need the winner.

You also need the runner-up.

Instead of sorting everyone,

you simply remember:

```
Current Winner

Current Runner-up
```

Every new runner either:

- becomes the winner
- becomes the runner-up
- is ignored

______________________________________________________________________

# Backend Engineering Analogy

Imagine an analytics dashboard.

You receive millions of transactions.

Instead of sorting all transactions,

you continuously maintain:

```
Highest Sale

Second Highest Sale
```

Every incoming transaction updates these values if necessary.

This is exactly how many streaming analytics systems work.

Examples:

- Highest API latency
- Top revenue
- Top CPU usage
- Top memory consumers

______________________________________________________________________

# Pattern Recognition

### Pattern

**Running Maximum**

Recognition clues

Whenever you see:

- Largest
- Maximum
- Highest
- Top K (small K)
- Running best value

Think

```
Can I maintain the answer while traversing?
```

______________________________________________________________________

# Brute Force Solution

## Intuition

Sort the array.

The last element becomes the largest.

Move backward until you find a different value.

That's the second largest.

______________________________________________________________________

## Algorithm

Example

```
[5, 9, 3, 7, 1]
```

Sort

```
[1, 3, 5, 7, 9]
```

Largest

```
9
```

Move left

```
7

↓

Different

↓

Second Largest
```

______________________________________________________________________

## Dry Run

Input

```
[4, 10, 7, 10, 5]
```

Sort

```
[4, 5, 7, 10, 10]
```

Largest

```
10
```

Move left

```
10

Same

↓

Ignore
```

Next

```
7

↓

Second Largest
```

______________________________________________________________________

## Complexity

Sorting dominates.

Time

```
O(n log n)
```

Space

Depends on sorting implementation.

Typically

```
O(n)
```

for Python's `sorted()`.

______________________________________________________________________

## Limitations

Sorting rearranges the array.

More importantly,

we don't actually need the entire array sorted.

We only need the top two values.

Can we do this in one traversal?

Yes.

______________________________________________________________________

# Optimized Solution

## Key Insight

Maintain two variables.

```
largest

second_largest
```

Every new element updates one of them.

No sorting needed.

______________________________________________________________________

## Step-by-Step Algorithm

Initialize

```
largest = -∞

second_largest = -∞
```

Example

```
[5, 9, 3, 7, 1]
```

______________________________________________________________________

Read

```
5
```

```
largest = 5

second = -∞
```

______________________________________________________________________

Read

```
9
```

New largest.

Old largest becomes second.

```
largest = 9

second = 5
```

______________________________________________________________________

Read

```
3
```

Smaller than both.

Ignore.

______________________________________________________________________

Read

```
7
```

```
7

>

5

↓

Update second
```

```
largest = 9

second = 7
```

______________________________________________________________________

Read

```
1
```

Ignore.

Finished.

______________________________________________________________________

# Dry Run

Input

```
[4, 8, 6, 10, 5]
```

| Current | Largest | Second Largest |
|---------|---------|----------------|
|4|4|-|
|8|8|4|
|6|8|6|
|10|10|8|
|5|10|8|

Answer

```
Largest = 10

Second Largest = 8
```

______________________________________________________________________

# Visual Explanation

```
Array

5

9

3

7

1
```

```
Largest

5

↓

9

↓

9

↓

9

↓

9
```

```
Second

-

↓

5

↓

5

↓

7

↓

7
```

Notice

The answer is built while scanning.

No sorting required.

______________________________________________________________________

# Why This Works

At every step,

we maintain this invariant:

```
largest

=

Largest element seen so far
```

and

```
second_largest

=

Second largest distinct element seen so far
```

Whenever a new larger value appears,

the old largest automatically becomes second largest.

Thus,

after scanning every element once,

the two variables contain the correct answer.

______________________________________________________________________

# Edge Cases

### Empty Array

```
[]
```

Return

```
(-1, -1)
```

or raise an exception depending on requirements.

______________________________________________________________________

### Single Element

```
[5]
```

Largest

```
5
```

Second Largest

```
-1
```

______________________________________________________________________

### Duplicate Largest

```
[10, 10]
```

Second largest

```
-1
```

______________________________________________________________________

### Negative Numbers

```
[-5, -2, -8]
```

Largest

```
-2
```

Second Largest

```
-5
```

Works correctly.

______________________________________________________________________

# Complexity Analysis

## Brute Force

Time

```
O(n log n)
```

Space

```
O(n)
```

______________________________________________________________________

## Optimized

Time

```
O(n)
```

Space

```
O(1)
```

Only two variables are maintained.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def find_second_largest(numbers: List[int]) -> int:
    if len(numbers) < 2:
        return -1

    sorted_numbers = sorted(numbers)
    largest = sorted_numbers[-1]

    for index in range(len(sorted_numbers) - 2, -1, -1):
        if sorted_numbers[index] != largest:
            return sorted_numbers[index]

    return -1
```

______________________________________________________________________

## Optimized (Recommended)

```python
from math import inf
from typing import List, Tuple


def find_largest_and_second_largest(
    numbers: List[int],
) -> Tuple[int, int]:
    if not numbers:
        return -1, -1

    largest = -inf
    second_largest = -inf

    for number in numbers:
        if number > largest:
            second_largest = largest
            largest = number
        elif largest > number > second_largest:
            second_largest = number

    if second_largest == -inf:
        second_largest = -1

    return largest, second_largest


if __name__ == "__main__":
    values = [5, 9, 3, 7, 1]

    print(find_largest_and_second_largest(values))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Sorting the array immediately.

It works,

but isn't optimal.

______________________________________________________________________

## Mistake 2

Ignoring duplicate largest values.

Example

```
[10, 10]
```

The answer is **not**

```
10
```

Second largest must be distinct.

______________________________________________________________________

## Mistake 3

Updating

```
largest
```

without updating

```
second_largest
```

Remember

Old largest becomes the new second largest.

______________________________________________________________________

## Mistake 4

Using

```python
>=
```

instead of

```python
>
```

This incorrectly treats duplicate values as distinct.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The straightforward solution is to sort the array and pick the last two distinct elements, but sorting is unnecessary because we only need two values. Instead, I can maintain the largest and second largest elements while traversing the array once, achieving O(n) time and O(1) extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why not sort?**

Sorting performs more work than necessary.

We only need two values.

______________________________________________________________________

**Q. What if all elements are equal?**

There is no distinct second largest.

Return

```
-1
```

______________________________________________________________________

**Q. Can this be extended to Top K elements?**

Yes.

For larger values of K,

a **Heap** is commonly used.

______________________________________________________________________

**Q. What if duplicates are allowed?**

Clarify with the interviewer whether "second largest" means the second distinct value or simply the second position
after sorting.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Running Maximum |
| Recognition | Largest / Maximum / Top Values |
| Brute Force | Sort |
| Optimized | Single Pass |
| Time | O(n) |
| Space | O(1) |

______________________________________________________________________

# Quick Revision

- Sorting solves the problem but isn't optimal.
- Keep two variables: `largest` and `second_largest`.
- Update both while traversing once.
- Handle duplicate largest values carefully.
- Works for negative numbers.
- Time complexity is O(n).
- Space complexity is O(1).
- This "running answer" pattern appears in many interview problems.

______________________________________________________________________

# Practice Questions

## Easy

1. Third Maximum Number
1. Maximum Product of Three Numbers
1. Largest Odd Number in String

______________________________________________________________________

## Medium

4. Best Time to Buy and Sell Stock
1. Maximum Subarray
1. Top K Frequent Elements *(preview of Heap)*
1. Kth Largest Element in an Array

______________________________________________________________________

## Hard (Optional)

8. Sliding Window Maximum
1. Maximum Gap
1. Find Median from Data Stream

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning to **maintain the answer while scanning the data** instead of computing
everything first. This "running maximum" technique is one of the most reusable patterns in array problems and forms the
basis for many medium-level interview questions.

______________________________________________________________________

# Next

[11-remove-duplicates.md](11-remove-duplicates.md)
