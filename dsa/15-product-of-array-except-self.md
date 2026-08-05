# 15-product-of-array-except-self.md

# Product of Array Except Self

______________________________________________________________________

# Interview Confidence

| Item | Value |
|------|------|
| Difficulty | Medium |
| Asked Frequency | ⭐⭐⭐⭐⭐ Very High |
| Importance | ⭐⭐⭐⭐⭐ |
| Expected Interview Time | 25–30 minutes |
| Revision Time | 15 minutes |

______________________________________________________________________

# Why Interviewers Ask This

This is one of the **most popular Medium-level interview questions**.

At first glance, the problem looks easy:

> "Multiply all the numbers except the current one."

However, interviewers are actually testing:

- Prefix computations
- Suffix computations
- Space optimization
- Problem decomposition
- Handling edge cases (especially zeroes)

Many candidates immediately think:

> "Find the total product and divide by the current element."

The interviewer intentionally adds the constraint:

> **Do not use division.**

The real challenge is learning the **Prefix-Suffix Pattern**, which appears in many interview questions.

______________________________________________________________________

# Problem Statement

Given an integer array `numbers`, return an array `answer` where:

```text
answer[i]
```

contains the product of **every element except** `numbers[i]`.

Do **not** use division.

______________________________________________________________________

## Example 1

```text
Input

[1,2,3,4]
```

Output

```text
[24,12,8,6]
```

Explanation

```
Position 0

2 × 3 × 4

=

24
```

```
Position 1

1 × 3 × 4

=

12
```

______________________________________________________________________

## Example 2

```text
Input

[-1,1,0,-3,3]
```

Output

```text
[0,0,9,0,0]
```

______________________________________________________________________

# Simple English

Imagine five workers.

Each worker wants to know:

> "What would be the total work done if **I didn't work today**?"

Each worker needs the product of everyone else's contribution.

______________________________________________________________________

# Common Misunderstandings

Most beginners think:

```
Total Product

↓

Divide by current element
```

Example

```
[1,2,3,4]

Total

24
```

```
24 / 1

=

24
```

```
24 / 2

=

12
```

Works.

But consider

```
[1,2,0,4]
```

Total product becomes

```
0
```

Division no longer works.

That's why interviewers prohibit it.

______________________________________________________________________

# Backend Engineering Analogy

Imagine a distributed system with multiple servers.

Each server contributes to the total system throughput.

```
Server A

×

Server B

×

Server C

×

Server D
```

For maintenance,

you want to know:

> "What would the total throughput be if one server goes offline?"

Instead of recalculating everything every time,

we precompute reusable information.

This is exactly what **prefix** and **suffix** arrays do.

______________________________________________________________________

# Pattern Recognition

## Pattern

**Prefix + Suffix**

______________________________________________________________________

## Recognition Clues

If the question contains:

- Product except self
- Left side
- Right side
- Range product
- Exclude current element

Think

```
Prefix

+

Suffix
```

______________________________________________________________________

# Brute Force Solution

## Intuition

For every position,

multiply every other element.

______________________________________________________________________

## Algorithm

Input

```
[1,2,3,4]
```

For index

```
0
```

Multiply

```
2 × 3 × 4

=

24
```

For index

```
1
```

Multiply

```
1 × 3 × 4

=

12
```

Continue for every index.

______________________________________________________________________

## Dry Run

```
[1,2,3]
```

Index

```
0

↓

2 × 3

=

6
```

Index

```
1

↓

1 × 3

=

3
```

Index

```
2

↓

1 × 2

=

2
```

Answer

```
[6,3,2]
```

______________________________________________________________________

## Complexity

Outer loop

```
n
```

Inner loop

```
n
```

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

Too many repeated multiplications.

Can we reuse previous calculations?

Yes.

______________________________________________________________________

# Better Solution (Prefix & Suffix Arrays)

## Key Insight

Let's focus on one position.

Example

```
[1,2,3,4]
```

For

```
3
```

we need

```
1 × 2

×

4
```

Notice

```
Everything Left

×

Everything Right
```

Instead of recomputing,

store both.

______________________________________________________________________

## Prefix Array

Prefix product stores:

> Product of everything **before** the current index.

Example

```
Numbers

1 2 3 4
```

Prefix

```
1 1 2 6
```

Why?

|Index|Product Before|
|------|--------------|
|0|1|
|1|1|
|2|1×2=2|
|3|1×2×3=6|

______________________________________________________________________

## Suffix Array

Suffix product stores:

> Product of everything **after** the current index.

Numbers

```
1 2 3 4
```

Suffix

```
24 12 4 1
```

Actually,

using the definition "after current":

|Index|Product After|
|------|-------------|
|0|2×3×4 = 24|
|1|3×4 = 12|
|2|4 = 4|
|3|1|

______________________________________________________________________

Now simply multiply

```
Prefix

×

Suffix
```

Example

Index

```
2
```

```
Prefix

2
```

```
Suffix

4
```

Answer

```
8
```

Correct.

______________________________________________________________________

## Complexity

Time

```
O(n)
```

Space

```
O(n)
```

______________________________________________________________________

# Optimized Solution (Without Extra Prefix & Suffix Arrays)

## Key Insight

Do we really need **two extra arrays?**

No.

We can store the prefix products directly inside the answer array.

Then,

during a second pass,

maintain a running suffix product.

______________________________________________________________________

# Step 1 - Build Prefix Products

Input

```
[1,2,3,4]
```

Initially

```
answer

[1,1,1,1]
```

Fill prefix values.

|Index|Answer|
|------|------|
|0|1|
|1|1|
|2|2|
|3|6|

Now

```
answer

=

Prefix Products
```

______________________________________________________________________

# Step 2 - Traverse Backwards

Maintain

```
suffix = 1
```

Start from the end.

______________________________________________________________________

Index

```
3
```

```
answer[3]

=

6 × 1

=

6
```

Update

```
suffix

=

1 × 4

=

4
```

______________________________________________________________________

Index

```
2
```

```
answer[2]

=

2 × 4

=

8
```

Update

```
suffix

=

4 × 3

=

12
```

______________________________________________________________________

Index

```
1
```

```
1 × 12

=

12
```

Update

```
suffix

=

24
```

______________________________________________________________________

Index

```
0
```

```
1 × 24

=

24
```

Finished.

Answer

```
24 12 8 6
```

______________________________________________________________________

# Visual Explanation

Input

```
1 2 3 4
```

Prefix

```
1 1 2 6
```

Suffix while traversing backwards

```
24 12 4 1
```

Multiply

```
1×24

↓

24
```

```
1×12

↓

12
```

```
2×4

↓

8
```

```
6×1

↓

6
```

Final

```
24 12 8 6
```

______________________________________________________________________

# Why This Works

For every position

```
i
```

The answer is

```
Product of Left

×

Product of Right
```

The prefix pass computes

```
Left Product
```

The backward pass computes

```
Right Product
```

Since every element is included exactly once on each side,

the final multiplication gives:

```
All elements

Except

Current
```

______________________________________________________________________

# Edge Cases

### Single Element

```
[5]
```

Output

```
[1]
```

There are no other elements to multiply.

______________________________________________________________________

### Contains One Zero

```
[1,2,0,4]
```

Only the position containing zero gets the product of the non-zero elements.

Everything else becomes zero.

______________________________________________________________________

### Contains Multiple Zeroes

```
[1,0,3,0]
```

Every answer becomes

```
0
```

______________________________________________________________________

### Negative Numbers

Works correctly because multiplication handles signs naturally.

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

## Prefix + Suffix Arrays

Time

```
O(n)
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

> **Interview Note:** The output array is **not counted** as extra space because the problem requires returning it.

______________________________________________________________________

# Production-Quality Python

## Brute Force

```python
from typing import List


def product_except_self(numbers: List[int]) -> List[int]:
    result = []

    for index in range(len(numbers)):
        product = 1

        for current in range(len(numbers)):
            if current != index:
                product *= numbers[current]

        result.append(product)

    return result
```

______________________________________________________________________

## Optimized (Recommended)

```python
from typing import List


def product_except_self(numbers: List[int]) -> List[int]:
    length = len(numbers)
    answer = [1] * length

    # Prefix products
    prefix = 1
    for index in range(length):
        answer[index] = prefix
        prefix *= numbers[index]

    # Suffix products
    suffix = 1
    for index in range(length - 1, -1, -1):
        answer[index] *= suffix
        suffix *= numbers[index]

    return answer


if __name__ == "__main__":
    values = [1, 2, 3, 4]

    print(product_except_self(values))
```

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using division.

The problem explicitly forbids it.

______________________________________________________________________

## Mistake 2

Not understanding what the prefix array stores.

It stores the product of elements **before** the current index.

______________________________________________________________________

## Mistake 3

Forgetting to reset

```python
suffix = 1
```

before the backward traversal.

______________________________________________________________________

## Mistake 4

Thinking the output array counts as extra space.

In interview problems,

the returned array is **excluded** from space complexity calculations.

______________________________________________________________________

# Interview Discussion

### Expected Thought Process

> "The brute-force solution computes the product for every index separately, resulting in O(n²) time. Instead, I observe that each answer consists of the product of elements to the left and the product of elements to the right. I first compute prefix products, then traverse backward while maintaining a running suffix product. This gives an O(n) solution without using division and with O(1) extra space."

______________________________________________________________________

### Common Follow-up Questions

**Q. Why not use division?**

Because arrays may contain zeroes, and the problem explicitly disallows division.

______________________________________________________________________

**Q. Why don't we need separate prefix and suffix arrays?**

We can reuse the output array for prefix products and compute suffix products on the fly.

______________________________________________________________________

**Q. Why is the output array not counted as extra space?**

Because it's required by the problem specification.

______________________________________________________________________

**Q. What interview pattern does this teach?**

The **Prefix-Suffix Pattern**, which is used in many range-product, cumulative-sum, and preprocessing problems.

______________________________________________________________________

# Pattern Summary

| Item | Value |
|------|------|
| Pattern | Prefix + Suffix |
| Recognition | Exclude Current Element |
| Brute Force | Nested Loops |
| Better | Prefix & Suffix Arrays |
| Optimized | Prefix Array + Running Suffix |
| Time | O(n) |
| Space | O(1) Extra |

______________________________________________________________________

# Quick Revision

- Don't use division.
- Brute force repeats unnecessary multiplications.
- Prefix stores products before each index.
- Suffix stores products after each index.
- Build prefix in one pass.
- Apply suffix in a backward pass.
- Output array doubles as the prefix array.
- Time complexity is O(n).
- Extra space complexity is O(1).

______________________________________________________________________

# Practice Questions

## Easy

1. Running Sum of 1D Array
1. Find Pivot Index
1. Range Sum Query - Immutable

______________________________________________________________________

## Medium

4. Subarray Product Less Than K
1. Maximum Product Subarray
1. Trapping Rain Water
1. Product of the Last K Numbers

______________________________________________________________________

## Hard (Optional)

8. Candy
1. Maximum Sum Circular Subarray
1. Count Subarrays With Fixed Bounds

______________________________________________________________________

# Key Takeaway

The biggest lesson from this problem is learning the **Prefix-Suffix Pattern**. Instead of recalculating information for
every position, preprocess what lies to the **left** and **right** of each index and combine them. This transforms a
quadratic solution into a linear one and introduces a powerful technique that appears throughout array, dynamic
programming, and range query problems.

______________________________________________________________________

# Next

[16-reverse-string.md](16-reverse-string.md)
