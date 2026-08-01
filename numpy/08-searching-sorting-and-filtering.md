# NumPy Part 8: Searching, Sorting & Filtering

**Python Version Introduced:** Python 3.x

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will be able to:

- Search for values efficiently in NumPy arrays.
- Sort arrays in ascending or descending order.
- Obtain sorted indices using `argsort()`.
- Find unique values using `unique()`.
- Filter data using `where()`.
- Locate non-zero elements using `nonzero()`.
- Validate conditions using `any()` and `all()`.
- Check membership using `isin()`.
- Insert values into sorted arrays using `searchsorted()`.
- Understand performance characteristics of searching and sorting operations.

______________________________________________________________________

# Recap

In the previous lesson, you learned how to summarize numerical data using:

- `sum()`
- `mean()`
- `median()`
- `std()`
- `var()`
- `min()`
- `max()`
- `argmin()`
- `argmax()`
- `cumsum()`
- `cumprod()`

Those operations answer questions like:

> "How much?"

This lesson answers questions like:

- Where is the value?
- Which records satisfy a condition?
- How do I sort the data?
- Which values are unique?

______________________________________________________________________

# Why Searching & Sorting Matter

Imagine an e-commerce company.

Every day it needs to:

- Find orders above ₹10,000.
- Sort products by price.
- Remove duplicate customer IDs.
- Check if a product exists.
- Find where to insert a new score into a leaderboard.

These are everyday data-processing tasks.

NumPy provides optimized functions for all of them.

______________________________________________________________________

# Searching vs Filtering vs Sorting

Although these terms are often used together, they solve different problems.

| Operation | Purpose |
|-----------|----------|
| Searching | Locate values or positions |
| Filtering | Keep only matching values |
| Sorting | Rearrange values into order |

Understanding the distinction makes code easier to read and maintain.

______________________________________________________________________

# `sort()`

## What does it do?

Returns a sorted copy of an array.

______________________________________________________________________

## Syntax

```python
np.sort(array, axis=-1)
```

or

```python
array.sort()
```

______________________________________________________________________

## Parameters

| Parameter | Description |
|-----------|-------------|
| `axis` | Axis along which to sort |

______________________________________________________________________

## Return Value

`np.sort()` returns a new sorted array.

`array.sort()` sorts the array **in place** and returns `None`.

______________________________________________________________________

## Example

```python
import numpy as np

arr = np.array([8, 3, 6, 1, 5])

print(np.sort(arr))
```

Output

```
[1 3 5 6 8]
```

Original array

```
[8 3 6 1 5]
```

remains unchanged.

______________________________________________________________________

# In-Place Sorting

```python
arr = np.array([8,3,6,1,5])

arr.sort()

print(arr)
```

Output

```
[1 3 5 6 8]
```

The original array has changed.

______________________________________________________________________

# Sorting Along an Axis

Consider

```python
matrix = np.array([
    [3,1,2],
    [6,4,5]
])
```

Sort each row.

```python
print(np.sort(matrix))
```

Output

```
[[1 2 3]
 [4 5 6]]
```

______________________________________________________________________

Sort each column.

```python
print(np.sort(matrix, axis=0))
```

Output

```
[[3 1 2]
 [6 4 5]]
```

Each column is sorted independently.

______________________________________________________________________

# Descending Order

NumPy sorts in ascending order by default.

To reverse:

```python
arr = np.sort(arr)[::-1]
```

Output

```
[8 6 5 3 1]
```

______________________________________________________________________

# `argsort()`

## What does it do?

Returns the indices that would sort an array.

______________________________________________________________________

## Syntax

```python
np.argsort(array)
```

______________________________________________________________________

## Example

```python
scores = np.array([90,75,85])

print(np.argsort(scores))
```

Output

```
[1 2 0]
```

Meaning

```
scores[1] = 75

scores[2] = 85

scores[0] = 90
```

______________________________________________________________________

## Why is this useful?

Imagine two arrays.

```python
names = np.array([
    "Alice",
    "Bob",
    "Charlie"
])

scores = np.array([
    90,
    75,
    85
])
```

```python
order = np.argsort(scores)

print(names[order])
print(scores[order])
```

Output

```
['Bob' 'Charlie' 'Alice']

[75 85 90]
```

This is a common technique when sorting related datasets.

______________________________________________________________________

# `unique()`

## What does it do?

Returns the unique values in an array.

______________________________________________________________________

## Syntax

```python
np.unique(array)
```

______________________________________________________________________

## Example

```python
arr = np.array([
    2,4,2,6,4,8
])

print(np.unique(arr))
```

Output

```
[2 4 6 8]
```

Duplicates are removed.

The output is sorted.

______________________________________________________________________

## Production Usage

Removing duplicate:

- Customer IDs
- Product IDs
- Categories
- Labels

______________________________________________________________________

# `where()`

## What does it do?

Returns values or indices based on a condition.

______________________________________________________________________

## Syntax

```python
np.where(condition)
```

or

```python
np.where(condition, x, y)
```

______________________________________________________________________

## Example 1

Find indices.

```python
arr = np.array([10,20,30,40])

print(np.where(arr > 20))
```

Output

```
(array([2,3]),)
```

______________________________________________________________________

## Example 2

Conditional replacement.

```python
arr = np.array([10,20,30,40])

result = np.where(
    arr > 20,
    1,
    0
)

print(result)
```

Output

```
[0 0 1 1]
```

Equivalent to

```
If value >20

↓

1

Else

↓

0
```

______________________________________________________________________

# `nonzero()`

## What does it do?

Returns the indices of non-zero elements.

______________________________________________________________________

## Syntax

```python
np.nonzero(array)
```

______________________________________________________________________

## Example

```python
arr = np.array([
    0,2,0,5,7
])

print(np.nonzero(arr))
```

Output

```
(array([1,3,4]),)
```

Useful for:

- Sparse data
- Image processing
- Mask generation

______________________________________________________________________

# `any()`

## What does it do?

Returns `True` if **at least one** element satisfies the condition.

______________________________________________________________________

Example.

```python
arr = np.array([2,4,6])

print(np.any(arr > 5))
```

Output

```
True
```

______________________________________________________________________

# `all()`

## What does it do?

Returns `True` only if **every** element satisfies the condition.

______________________________________________________________________

Example.

```python
print(np.all(arr > 1))
```

Output

```
True
```

Another example.

```python
print(np.all(arr > 5))
```

Output

```
False
```

______________________________________________________________________

# `isin()`

## What does it do?

Checks membership.

______________________________________________________________________

## Syntax

```python
np.isin(array, values)
```

______________________________________________________________________

## Example

```python
arr = np.array([
    10,20,30,40
])

print(np.isin(
    arr,
    [20,40]
))
```

Output

```
[False True False True]
```

Very useful for filtering categories or IDs.

______________________________________________________________________

# `searchsorted()`

## What does it do?

Finds the insertion position that keeps a sorted array ordered.

______________________________________________________________________

## Syntax

```python
np.searchsorted(sorted_array, value)
```

______________________________________________________________________

## Example

```python
arr = np.array([
    10,20,30,40
])

print(np.searchsorted(arr,25))
```

Output

```
2
```

Meaning

```
25
```

should be inserted before

```
30
```

______________________________________________________________________

## Real-World Usage

Applications include:

- Leaderboards
- Ranking systems
- Maintaining sorted logs
- Financial order books

______________________________________________________________________

# Performance Notes

Operation | Average Complexity | Output ----------|-------------------|------- sort() | O(n log n) | Sorted array
argsort() | O(n log n) | Indices unique() | O(n log n)\* | Unique values where() | O(n) | Indices or values nonzero() |
O(n) | Indices any() | O(n) | Boolean all() | O(n) | Boolean isin() | O(n + m) (conceptually) | Boolean mask
searchsorted() | O(log n) | Insertion index

\*`unique()` typically sorts internally to produce sorted unique values.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Confusing `sort()` and `argsort()`.

```python
sort()
```

returns values.

```python
argsort()
```

returns indices.

______________________________________________________________________

## Mistake 2

Expecting `array.sort()` to return a new array.

It modifies the original array and returns `None`.

______________________________________________________________________

## Mistake 3

Using Python loops for filtering.

Bad

```python
result = []

for x in arr:
    if x > 20:
        result.append(x)
```

Good

```python
result = arr[arr > 20]
```

______________________________________________________________________

## Mistake 4

Using `==` repeatedly for membership tests.

Instead of

```python
(arr == 2) | (arr == 5)
```

Prefer

```python
np.isin(arr,[2,5])
```

______________________________________________________________________

# Best Practices

- Use `np.sort()` when you need to preserve the original array.
- Use `array.sort()` when modifying the original array is acceptable.
- Use `argsort()` to sort related datasets consistently.
- Prefer Boolean masks and `where()` over Python loops.
- Use `searchsorted()` for efficient insertion into sorted arrays.
- Use `any()` and `all()` for concise validation checks.

______________________________________________________________________

# Production Insight

Searching, sorting, and filtering operations are the foundation of data processing pipelines.

Examples include:

- Sorting products by price.
- Filtering fraudulent transactions.
- Finding duplicate customer records.
- Checking data quality rules.
- Maintaining ranked recommendation lists.
- Building preprocessing pipelines for machine learning.

These operations are often applied to millions of records, making NumPy's optimized implementations far more efficient
than Python loops.

______________________________________________________________________

```markdown id="n4q8wx"
# Questions

### Question

> What is the difference between `sort()` and `argsort()`?

### Answer

`sort()` returns sorted values, while `argsort()` returns the indices that would produce the sorted order.

---

### Question

> When would you use `searchsorted()`?

### Answer

When you need to determine where a value should be inserted into a sorted array while preserving the order.

---

### Question

> What does `np.where(condition, x, y)` do?

### Answer

It returns elements from `x` where the condition is `True` and elements from `y` where the condition is `False`.

---

### Question

> What is the purpose of `np.unique()`?

### Answer

It returns the sorted unique values from an array.
```

______________________________________________________________________

# Practical Lesson

Create the following dataset:

```python
scores = np.array([
    85, 72, 90, 72, 95, 88, 90, 60
])
```

Perform these tasks:

1. Sort the scores in ascending order.
1. Sort them in descending order.
1. Find the indices that would sort the array.
1. Remove duplicate scores.
1. Find the indices of scores greater than 85 using `where()`.
1. Replace all scores below 75 with `0` using `where()`.
1. Check whether the scores contain `95` and `100` using `isin()`.
1. Determine where a new score of `87` should be inserted using `searchsorted()`.
1. Verify whether all scores are above 50 and whether any score is above 90.

______________________________________________________________________

```markdown id="c7v5lp"
# Knowledge Check

## Question 1

Which function returns sorted indices instead of sorted values?

### Answer

`argsort()`.

---

## Question 2

Does `array.sort()` modify the original array?

### Answer

Yes. It sorts the array in place.

---

## Question 3

Which function removes duplicate values?

### Answer

`np.unique()`.

---

## Question 4

Which function returns insertion positions in a sorted array?

### Answer

`np.searchsorted()`.

---

## Question 5

What is the difference between `any()` and `all()`?

### Answer

`any()` returns `True` if at least one element satisfies the condition, while `all()` returns `True` only if every element satisfies it.

---

## Question 6

Which function is best suited for membership testing?

### Answer

`np.isin()`.

---

## Question 7

What is the approximate time complexity of sorting?

### Answer

`O(n log n)`.

---

## Question 8

Why is `argsort()` useful when working with multiple related arrays?

### Answer

Because it allows the same sorted index order to be applied to other arrays, keeping related data aligned.
```

______________________________________________________________________

# Assignment

1. Generate an array of 100 random integers between 1 and 100.
1. Perform the following operations:
   - Sort the array in ascending and descending order.
   - Remove duplicate values.
   - Find all values greater than 75.
   - Replace values below 25 with `-1` using `where()`.
   - Determine whether all values are positive.
   - Check whether any values exceed 95.
1. Create a second array containing labels (for example, `"A"`, `"B"`, `"C"`, ...) corresponding to the numbers.
1. Use `argsort()` to sort both arrays while preserving the relationship between values and labels.
1. Insert several new values into the sorted array conceptually using `searchsorted()` and explain why binary search makes this operation efficient.

______________________________________________________________________

# Summary

In this lesson, you learned how to search, sort, and filter data efficiently using NumPy. You explored `sort()`,
`argsort()`, `unique()`, `where()`, `nonzero()`, `any()`, `all()`, `isin()`, and `searchsorted()`, while understanding
their performance characteristics and practical applications. These operations are fundamental for preparing data for
analysis, reporting, and machine learning.

______________________________________________________________________

# Next Lesson

**File:**

[09-linear-algebra-essentials.md](09-linear-algebra-essentials.md)
