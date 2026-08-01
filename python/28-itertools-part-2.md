# File: python/28-itertools-part-2.md

# Python Functional Programming - Part 6

# `itertools` Part 2 - Combinatorics, Grouping and Advanced Iterator Patterns

> **Course:** Backend Engineering Roadmap
>
> **Module:** Functional Python
>
> **Lesson:** 6
>
> **Difficulty:** ⭐⭐⭐⭐☆
>
> **Estimated Time:** 180 Minutes

______________________________________________________________________

# Python Version Introduced

| Feature | Python Version |
|----------|----------------|
| `product()` | Python 2.6 |
| `permutations()` | Python 2.6 |
| `combinations()` | Python 2.6 |
| `combinations_with_replacement()` | Python 2.7 |
| `groupby()` | Python 2.4 |
| `tee()` | Python 2.4 |
| `accumulate()` | Python 3.2 |
| `pairwise()` | Python 3.10 |

### Important Notes

- Every function in this lesson returns an **iterator**.
- Most functions are implemented in **C**, making them highly efficient.
- Some operations can generate **enormous numbers of results**, so understanding computational complexity is essential.
- `pairwise()` is only available in **Python 3.10+**.

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will understand:

- Cartesian products
- Permutations
- Combinations
- Combinations with replacement
- Running totals with `accumulate()`
- Grouping data with `groupby()`
- Duplicating iterators using `tee()`
- Consecutive pairs using `pairwise()`
- Time and memory considerations
- Production examples

______________________________________________________________________

# Recap

Previously we learned

- `count()`
- `cycle()`
- `repeat()`
- `chain()`
- `islice()`

These functions helped us build efficient iterator pipelines.

Today we'll study the remaining high-value tools in `itertools`.

Many of these are used in:

- Analytics
- Recommendation engines
- Search algorithms
- Scheduling systems
- Machine Learning
- Data Engineering

______________________________________________________________________

# Overview

Today's functions

```
itertools

│

├── product()

├── permutations()

├── combinations()

├── combinations_with_replacement()

├── accumulate()

├── groupby()

├── tee()

└── pairwise()
```

______________________________________________________________________

# Part 1 — product()

______________________________________________________________________

# What is product()?

`product()` computes the **Cartesian Product**.

If you've studied SQL,

this is similar to a

```
CROSS JOIN
```

______________________________________________________________________

# What is a Cartesian Product?

Suppose

```python
colours = [

    "Red",

    "Blue"

]

sizes = [

    "S",

    "M"
]
```

Possible combinations

```
Red S

Red M

Blue S

Blue M
```

Every colour is paired with every size.

______________________________________________________________________

# Example

```python
from itertools import product

result = product(

    colours,

    sizes

)

print(list(result))
```

Output

```
[

('Red', 'S'),

('Red', 'M'),

('Blue', 'S'),

('Blue', 'M')

]
```

______________________________________________________________________

# Visualising product()

```
Colours

↓

Red

Blue

        ×

Sizes

↓

S

M

↓

Cartesian Product

↓

Red S

Red M

Blue S

Blue M
```

______________________________________________________________________

# Production Example

Suppose an e-commerce website sells

- 5 colours
- 8 sizes

Generating all product variants

```python
variants = product(

    colours,

    sizes
)
```

______________________________________________________________________

# Repeated Product

```python
from itertools import product

print(

    list(

        product(

            "AB",

            repeat=3

        )

    )

)
```

Output

```
AAA

AAB

ABA

ABB

BAA

BAB

BBA

BBB
```

Useful for brute-force search or generating fixed-length combinations.

______________________________________________________________________

# Complexity Warning

Suppose

```
100 × 100 × 100
```

Possible outputs

```
1,000,000
```

The number of combinations grows exponentially.

______________________________________________________________________

# Part 2 — permutations()

______________________________________________________________________

# What is a Permutation?

A permutation is

```
Order Matters
```

Example

```
ABC

ACB

BAC

BCA

CAB

CBA
```

All six are different.

______________________________________________________________________

# Example

```python
from itertools import permutations

letters = [

    "A",

    "B",

    "C"

]

print(

    list(

        permutations(

            letters

        )

    )

)
```

Output

```
(

'A',

'B',

'C'

)

...

6 results
```

There are

```
3!

=

6
```

permutations.

______________________________________________________________________

# Choosing Length

```python
print(

    list(

        permutations(

            letters,

            2

        )

    )

)
```

Output

```
AB

AC

BA

BC

CA

CB
```

______________________________________________________________________

# When Do We Use Permutations?

Whenever

```
Order Matters
```

Examples

- Password generation
- Seat arrangements
- Route optimisation
- Task ordering

______________________________________________________________________

# Part 3 — combinations()

______________________________________________________________________

# What is a Combination?

A combination means

```
Order Does NOT Matter
```

Example

```
AB

BA
```

These are considered identical.

______________________________________________________________________

# Example

```python
from itertools import combinations

letters = [

    "A",

    "B",

    "C"

]

print(

    list(

        combinations(

            letters,

            2

        )

    )

)
```

Output

```
AB

AC

BC
```

Notice

```
BA

CA

CB
```

do not appear.

______________________________________________________________________

# Visualising

```
Choose 2

From

A

B

C

↓

AB

AC

BC
```

______________________________________________________________________

# Production Example

Suppose

```
5 Developers
```

Need

```
2-person teams
```

Use

```python
combinations(

    developers,

    2
)
```

______________________________________________________________________

# Part 4 — combinations_with_replacement()

______________________________________________________________________

# What Changes?

Normal combinations

```
AB
```

Cannot contain

```
AA
```

Replacement allows repeated values.

______________________________________________________________________

# Example

```python
from itertools import combinations_with_replacement

letters = [

    "A",

    "B"

]

print(

    list(

        combinations_with_replacement(

            letters,

            2

        )

    )

)
```

Output

```
AA

AB

BB
```

______________________________________________________________________

# Production Example

Suppose an ice cream shop allows

```
Chocolate

Chocolate
```

as a valid two-scoop order.

Replacement is allowed.

______________________________________________________________________

# Part 5 — accumulate()

______________________________________________________________________

# The Problem

Suppose

```python
numbers = [

    10,

    20,

    30,

    40

]
```

We want

```
10

30

60

100
```

Running totals.

______________________________________________________________________

# accumulate()

```python
from itertools import accumulate

numbers = [

    10,

    20,

    30,

    40

]

print(

    list(

        accumulate(

            numbers

        )

    )

)
```

Output

```
[

10,

30,

60,

100

]
```

______________________________________________________________________

# Visualising

```
10

↓

10

↓

10 + 20

↓

30

↓

30 + 30

↓

60

↓

60 + 40

↓

100
```

______________________________________________________________________

# Custom Operation

Suppose multiplication.

```python
from itertools import accumulate

import operator

numbers = [

    2,

    3,

    4

]

print(

    list(

        accumulate(

            numbers,

            operator.mul

        )

    )

)
```

Output

```
2

6

24
```

______________________________________________________________________

# Production Example

Running account balance.

Transactions

```
+100

-25

+50
```

Balances

```
100

75

125
```

______________________________________________________________________

# Part 6 — groupby()

______________________________________________________________________

# The Biggest Misunderstanding

Many developers think

```
groupby()
```

works like SQL

```
GROUP BY
```

It does not.

______________________________________________________________________

# Why?

It groups only

```
Adjacent
```

values.

Example

```python
numbers = [

    1,

    1,

    2,

    2,

    1
]
```

Using

```python
groupby(numbers)
```

Produces

```
1 1

2 2

1
```

The final

```
1
```

creates a new group.

______________________________________________________________________

# Example

```python
from itertools import groupby

numbers = [

    1,

    1,

    2,

    2,

    1

]

for key, group in groupby(

    numbers

):

    print(

        key,

        list(group)

    )
```

Output

```
1 [1, 1]

2 [2, 2]

1 [1]
```

______________________________________________________________________

# Sorting First

Suppose

```python
employees = [

    ("HR", "Alice"),

    ("Engineering", "Bob"),

    ("HR", "Charlie")
]
```

Sort first.

```python
employees = sorted(

    employees,

    key=lambda x: x[0]
)
```

Then

```python
groupby(...)
```

Now all departments are adjacent.

> **Important:** Unlike SQL, `itertools.groupby()` **does not** collect identical keys from the entire iterable. It only groups consecutive items with the same key.

______________________________________________________________________

# Production Example

Grouping log entries by date after sorting.

______________________________________________________________________

# Part 7 — tee()

______________________________________________________________________

# The Problem

Iterators are consumed.

```python
numbers = iter(

    [1, 2, 3]
)

print(

    list(numbers)

)

print(

    list(numbers)

)
```

Output

```
[1, 2, 3]

[]
```

The iterator is exhausted.

______________________________________________________________________

# tee()

```python
from itertools import tee

numbers = iter(

    [1, 2, 3]
)

a,

b = tee(numbers)

print(list(a))

print(list(b))
```

Output

```
[1, 2, 3]

[1, 2, 3]
```

______________________________________________________________________

# How Does tee() Work?

It creates independent iterators.

Internally,

Python buffers values as needed.

This means memory usage grows if one iterator runs far ahead of the other.

______________________________________________________________________

# Production Example

One iterator

```
Validation
```

Another

```
Database Insert
```

Without reading the source twice.

______________________________________________________________________

# Part 8 — pairwise()

______________________________________________________________________

# What is pairwise()?

Added in Python 3.10.

Produces consecutive pairs.

______________________________________________________________________

# Example

```python
from itertools import pairwise

numbers = [

    10,

    20,

    30,

    40

]

print(

    list(

        pairwise(

            numbers

        )

    )

)
```

Output

```
(

10,

20

)

(

20,

30

)

(

30,

40

)
```

______________________________________________________________________

# Visualising

```
10

20

30

40

↓

(10,20)

↓

(20,30)

↓

(30,40)
```

______________________________________________________________________

# Production Example

Calculating response time differences.

```python
timestamps = [

    100,

    115,

    130,

    170
]
```

Compare consecutive timestamps.

______________________________________________________________________

# Complexity Summary

| Function | Output Growth |
|----------|---------------|
| `product()` | Exponential |
| `permutations()` | Factorial |
| `combinations()` | Combinatorial |
| `accumulate()` | Linear |
| `groupby()` | Linear |
| `tee()` | Linear + buffer |
| `pairwise()` | Linear |

Understanding these complexities is important when working with large datasets.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using

```python
groupby()
```

without sorting.

Groups may appear split unexpectedly.

______________________________________________________________________

## Mistake 2

Generating huge permutation sets.

```
10!

=

3,628,800
```

results.

______________________________________________________________________

## Mistake 3

Assuming

```python
tee()
```

duplicates data without additional memory usage.

It buffers values internally.

______________________________________________________________________

## Mistake 4

Using

```python
product()
```

without considering exponential growth.

______________________________________________________________________

# Best Practices

✅ Sort data before using `groupby()` unless consecutive grouping is exactly what you need.

✅ Be aware of combinatorial explosion with `product()`, `permutations()` and `combinations()`.

✅ Use `accumulate()` instead of maintaining manual running totals.

✅ Use `pairwise()` instead of manual index arithmetic.

✅ Use `tee()` sparingly and understand its buffering behaviour.

❌ Don't materialise millions of permutations into a list unless absolutely necessary.

______________________________________________________________________

# Production Insight

The combinatoric functions in `itertools` are powerful, but they're also among the easiest ways to accidentally create
performance problems.

For example:

- `permutations(range(12))` would generate **479,001,600** results.
- `product(range(1000), repeat=3)` would represent **1 billion** tuples.

In production systems, these functions are usually consumed lazily inside pipelines rather than converted into lists.

Functions such as `groupby()`, `accumulate()` and `pairwise()` are much more common in everyday backend applications
because they process data incrementally without explosive growth.

______________________________________________________________________

# Questions

### Question

> What is the difference between `permutations()` and `combinations()`?

### Answer

`permutations()` treats different orders as distinct results, while `combinations()` ignores ordering.

______________________________________________________________________

### Question

> Why does `groupby()` often require sorting first?

### Answer

Because it groups only consecutive items with the same key rather than all matching items throughout the iterable.

______________________________________________________________________

### Question

> What problem does `tee()` solve?

### Answer

It allows multiple independent iterators to consume the same input iterator without rereading the original data source.

______________________________________________________________________

### Question

> When would you use `accumulate()`?

### Answer

When calculating running totals, cumulative products or other incremental aggregations.

______________________________________________________________________

# Practical Lesson

Create a file:

```
itertools_part_2.py
```

```python
from itertools import (
    product,
    combinations,
    permutations,
    accumulate,
    groupby,
    pairwise,
)

import operator


print(list(product(["A", "B"], [1, 2])))

print(list(combinations("ABC", 2)))

print(list(permutations("ABC", 2)))

print(list(accumulate([10, 20, 30])))

print(
    list(
        accumulate(
            [2, 3, 4],
            operator.mul,
        )
    )
)

for key, group in groupby([1, 1, 2, 2, 3]):
    print(key, list(group))

print(list(pairwise([10, 20, 30, 40])))
```

Expected Output

```
[('A', 1), ('A', 2), ('B', 1), ('B', 2)]

[('A', 'B'), ('A', 'C'), ('B', 'C')]

[('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

[10, 30, 60]

[2, 6, 24]

1 [1, 1]
2 [2, 2]
3 [3]

[(10, 20), (20, 30), (30, 40)]
```

______________________________________________________________________

# Questions

## Question 1

What is the difference between `product()` and `combinations()`?

### Answer

`product()` generates every possible pairing between iterables, while `combinations()` selects unique groups of a
specified size from a single iterable without considering order.

______________________________________________________________________

## Question 2

Why should you be careful when using `permutations()`?

### Answer

The number of permutations grows factorially, becoming extremely large even for modest input sizes.

______________________________________________________________________

## Question 3

Why does `groupby()` sometimes produce multiple groups with the same key?

### Answer

Because it groups only adjacent elements. If identical keys are separated, each consecutive block becomes a separate
group.

______________________________________________________________________

## Question 4

When is `pairwise()` useful?

### Answer

When comparing consecutive elements, such as calculating time differences, detecting trends or validating ordered data.

______________________________________________________________________

## Question 5

What is the trade-off when using `tee()`?

### Answer

It avoids rereading the original iterator but buffers values internally, which can increase memory usage if the
duplicated iterators are consumed at different speeds.

______________________________________________________________________

# Assignment

## Exercise 1

Generate every possible SKU using:

```python
colours = ["Black", "White"]
sizes = ["S", "M", "L"]
```

using `product()`.

______________________________________________________________________

## Exercise 2

Given

```python
players = ["Alice", "Bob", "Charlie", "David"]
```

Generate every unique two-player team using `combinations()`.

Then generate every possible batting order using `permutations()`.

Compare the number of outputs.

______________________________________________________________________

## Exercise 3

Given daily sales

```python
sales = [120, 80, 95, 110, 150]
```

Use `accumulate()` to calculate cumulative sales.

Then repeat using multiplication to observe the difference.

______________________________________________________________________

## Exercise 4

Given

```python
logs = [
    ("INFO", "Started"),
    ("INFO", "Connected"),
    ("ERROR", "Database"),
    ("ERROR", "Timeout"),
    ("INFO", "Recovered"),
]
```

Sort the logs appropriately and use `groupby()` to group entries by log level.

Explain why sorting is required.

______________________________________________________________________

# Summary

In this lesson, you learned:

- ✅ How `product()` generates Cartesian products.
- ✅ The difference between permutations and combinations.
- ✅ When replacement is useful in combinations.
- ✅ How `accumulate()` performs cumulative calculations.
- ✅ Why `groupby()` requires consecutive keys.
- ✅ How `tee()` duplicates iterators.
- ✅ How `pairwise()` simplifies adjacent comparisons.
- ✅ The computational complexity of combinatoric iterator functions.

______________________________________________________________________

# Module Complete – Functional Python 🎉

You have now completed the **Functional Python** module.

Topics mastered:

- ✅ Functional Programming Principles
- ✅ Pure Functions
- ✅ Immutability
- ✅ `map()`
- ✅ `filter()`
- ✅ `reduce()`
- ✅ Comprehensions
- ✅ Generator Expressions
- ✅ `zip()`
- ✅ `enumerate()`
- ✅ `any()`
- ✅ `all()`
- ✅ `functools`
- ✅ `itertools`

You now have a strong understanding of Python's functional programming toolkit and lazy evaluation model—concepts that
appear frequently in production backend systems and technical interviews.

______________________________________________________________________

# What's Next

**Module 4 – Concurrency & Parallelism**

**File:** [29-String-Deep-Dive-part-1](29-string-deep-dive-part-1.md)
