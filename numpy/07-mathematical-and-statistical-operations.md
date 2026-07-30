# NumPy Part 7: Mathematical & Statistical Operations

**Python Version Introduced:** Python 3.x

---

# Learning Objectives

By the end of this lesson, you will be able to:

- Perform common mathematical operations on NumPy arrays.
- Understand aggregation functions such as `sum()`, `mean()`, `median()`, `std()`, and `var()`.
- Use the `axis` parameter correctly.
- Find minimum, maximum, and their indices using `min()`, `max()`, `argmin()`, and `argmax()`.
- Compute cumulative operations with `cumsum()` and `cumprod()`.
- Understand performance considerations of aggregation operations.
- Apply these operations to real-world datasets.

---

# Recap

In the previous lesson, you learned:

- Vectorization
- Broadcasting
- Universal Functions (ufuncs)
- Broadcasting rules
- Using `np.newaxis`

Those concepts allow NumPy to process arrays efficiently.

This lesson focuses on **summarizing and analyzing numerical data**.

---

# Why Mathematical Operations Matter

Imagine you have:

- Sales data for an e-commerce platform.
- Temperature readings from weather stations.
- Student exam scores.
- Sensor data from IoT devices.

Rarely do we need individual values.

Instead, we ask questions such as:

- What is the total sales amount?
- What is the average temperature?
- Which product had the highest revenue?
- Which sensor recorded the lowest value?

These questions are answered using aggregation functions.

---

# Sample Dataset

We'll use this array throughout the lesson.

```python
import numpy as np

sales = np.array([
    [120, 150, 180],
    [200, 175, 190],
    [160, 210, 220]
])
```

```
Rows   → Stores

Columns → Months
```

---

# Understanding the `axis` Parameter

Before learning aggregation functions, it's important to understand `axis`.

Consider:

```python
sales = np.array([
    [120,150,180],
    [200,175,190],
    [160,210,220]
])
```

Shape

```
(3,3)
```

```
Axis 0

↓

120 150 180

200 175 190

160 210 220

↑

Rows
```

Axis 0 moves **down the rows**.

Aggregation happens **column-wise**.

---

Axis 1

```
120 → 150 → 180

200 → 175 → 190

160 → 210 → 220
```

Aggregation happens **row-wise**.

A simple way to remember:

| Axis | Aggregation |
|-------|-------------|
| 0 | Down the rows (column results) |
| 1 | Across the columns (row results) |

---

# `sum()`

## What does it do?

Returns the sum of array elements.

---

## Syntax

```python
np.sum(array, axis=None)
```

or

```python
array.sum(axis=None)
```

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| `axis` | Axis along which to compute the sum. If omitted, sums all elements. |

---

## Return Value

A scalar if `axis=None`; otherwise an array with one value per aggregation axis.

---

## Examples

Entire array.

```python
print(sales.sum())
```

Output

```
1605
```

---

Column totals.

```python
print(sales.sum(axis=0))
```

Output

```
[480 535 590]
```

---

Row totals.

```python
print(sales.sum(axis=1))
```

Output

```
[450 565 590]
```

---

## Copy or View

No copy or view is returned.

The function computes and returns a new result.

---

## Time Complexity

```
O(n)
```

Every element is visited once.

---

## Memory Complexity

```
O(1)
```

for a scalar result, or proportional to the size of the output when using an axis.

---

## Performance Notes

Aggregation functions are implemented in optimized compiled code and are significantly faster than equivalent Python loops.

---

## Common Mistakes

Confusing the `axis` parameter.

---

## Best Practices

Use the `axis` parameter explicitly to improve readability.

---

## Production Insight

Daily sales, total revenue, total website visits, and financial summaries commonly use `sum()`.

---

# `mean()`

## What does it do?

Computes the arithmetic mean.

---

## Syntax

```python
array.mean(axis=None)
```

---

## Example

Overall average.

```python
print(sales.mean())
```

Output

```
178.33
```

---

Average for each month.

```python
print(sales.mean(axis=0))
```

Output

```
[160.0 178.33 196.67]
```

---

Average sales for each store.

```python
print(sales.mean(axis=1))
```

Output

```
[150.0 188.33 196.67]
```

---

## Time Complexity

```
O(n)
```

---

## Production Insight

Averages are used in dashboards, KPI reports, forecasting, and feature engineering.

---

# `median()`

## What does it do?

Returns the middle value after sorting.

---

## Syntax

```python
np.median(array, axis=None)
```

---

Example.

```python
scores = np.array([60, 65, 70, 95, 100])

print(np.median(scores))
```

Output

```
70
```

---

Why use the median?

The median is less affected by extreme outliers than the mean.

Example.

```
Mean

↓

Strongly influenced by 1000

Median

↓

Hardly changes
```

---

# `std()`

## What does it do?

Computes the standard deviation.

---

## Syntax

```python
array.std(axis=None)
```

---

Example.

```python
values = np.array([10,12,14,16])

print(values.std())
```

---

Why is it useful?

A low standard deviation means values are close together.

A high standard deviation indicates greater variability.

---

# `var()`

## What does it do?

Computes the variance.

---

## Syntax

```python
array.var(axis=None)
```

Variance is simply the square of the standard deviation.

---

# `min()` and `max()`

## What do they do?

Return the smallest and largest values.

---

Example.

```python
print(sales.min())
```

Output

```
120
```

```python
print(sales.max())
```

Output

```
220
```

---

Using `axis`.

```python
print(sales.max(axis=0))
```

Output

```
[200 210 220]
```

Each value is the maximum for a column.

---

# `argmin()` and `argmax()`

Sometimes we need the **position**, not the value.

---

Example.

```python
arr = np.array([50,80,30,90])

print(arr.argmax())
```

Output

```
3
```

Meaning

```
90
```

is located at index

```
3
```

Similarly.

```python
print(arr.argmin())
```

Output

```
2
```

---

Using `axis`.

```python
print(sales.argmax(axis=0))
```

Output

```
[1 2 2]
```

This tells us which row contains the maximum value for each column.

---

# Cumulative Operations

Sometimes we want a running total instead of a single result.

---

# `cumsum()`

## What does it do?

Computes the cumulative sum.

---

Example.

```python
arr = np.array([10,20,30,40])

print(arr.cumsum())
```

Output

```
[10 30 60 100]
```

Applications:

- Running revenue
- Running inventory
- Running balances

---

# `cumprod()`

## What does it do?

Computes the cumulative product.

---

Example.

```python
arr = np.array([2,3,4])

print(arr.cumprod())
```

Output

```
[ 2  6 24]
```

Applications:

- Compound growth
- Investment returns
- Probability calculations

---

# Combining Aggregations

Suppose you need a report for each store.

```python
print("Total:", sales.sum(axis=1))
print("Average:", sales.mean(axis=1))
print("Maximum:", sales.max(axis=1))
print("Minimum:", sales.min(axis=1))
```

Output

```
Total:   [450 565 590]
Average: [150.0 188.33 196.67]
Maximum: [180 200 220]
Minimum: [120 175 160]
```

This pattern is common in analytics pipelines.

---

# Performance Notes

Operation | Complexity | Output Size
----------|------------|------------
sum() | O(n) | Scalar or reduced array
mean() | O(n) | Scalar or reduced array
median() | O(n log n)* | Scalar or reduced array
std() | O(n) | Scalar or reduced array
var() | O(n) | Scalar or reduced array
min()/max() | O(n) | Scalar or reduced array
argmin()/argmax() | O(n) | Scalar or reduced array
cumsum() | O(n) | Same size as input
cumprod() | O(n) | Same size as input

\*The exact implementation may vary, but conceptually the median requires identifying the middle value.

---

# Common Mistakes

## Mistake 1

Forgetting the `axis`.

```python
sales.sum()
```

This returns a single value.

If you wanted monthly totals, use:

```python
sales.sum(axis=0)
```

---

## Mistake 2

Confusing `max()` with `argmax()`.

```python
max()
```

returns the value.

```python
argmax()
```

returns the index.

---

## Mistake 3

Using Python's built-in `sum()` on NumPy arrays.

Prefer:

```python
np.sum()

or

array.sum()
```

These are optimized for NumPy arrays.

---

## Mistake 4

Using `mean()` when the dataset contains extreme outliers.

In such cases, `median()` may provide a more representative measure of central tendency.

---

# Best Practices

- Always understand the meaning of the `axis` parameter before aggregating.
- Use NumPy aggregation functions instead of Python loops.
- Choose `median()` when outliers are significant.
- Use cumulative functions for running totals and growth calculations.
- Prefer NumPy methods (`array.sum()`) or functions (`np.sum()`) for clarity and performance.

---

# Production Insight

Aggregation functions are among the most frequently used operations in data processing.

Examples include:

- Calculating monthly revenue.
- Computing average customer ratings.
- Monitoring sensor statistics.
- Generating business intelligence dashboards.
- Producing machine learning features such as averages, variances, and cumulative metrics.

These operations often process millions of values, making NumPy's optimized implementations essential for performance.

---

```markdown id="g7n5tv"
# Questions

### Question

> What is the purpose of the `axis` parameter?

### Answer

It specifies the dimension along which the aggregation is performed. `axis=0` aggregates down the rows (producing column-wise results), while `axis=1` aggregates across the columns (producing row-wise results).

---

### Question

> What is the difference between `max()` and `argmax()`?

### Answer

`max()` returns the largest value, while `argmax()` returns the index of the largest value.

---

### Question

> When is `median()` preferred over `mean()`?

### Answer

When the data contains significant outliers, because the median is less affected by extreme values.

---

### Question

> What does `cumsum()` compute?

### Answer

It computes the running cumulative sum of the elements.
```

---

# Practical Lesson

Using the following dataset:

```python
sales = np.array([
    [120, 150, 180],
    [200, 175, 190],
    [160, 210, 220],
    [180, 195, 205]
])
```

Perform the following tasks:

1. Calculate the total sales for each month.
2. Calculate the total sales for each store.
3. Compute the average sales by month and by store.
4. Find the highest and lowest sales values for each month.
5. Identify which store achieved the highest sales in each month using `argmax()`.
6. Compute the cumulative monthly sales using `cumsum()`.
7. Compare the mean and median of the entire dataset and explain the difference.

---

```markdown id="t9k4wm"
# Knowledge Check

## Question 1

What does `axis=0` represent?

### Answer

Aggregation down the rows, producing one result for each column.

---

## Question 2

What does `axis=1` represent?

### Answer

Aggregation across the columns, producing one result for each row.

---

## Question 3

Which function returns the position of the largest value?

### Answer

`argmax()`.

---

## Question 4

Why might `median()` be a better choice than `mean()` for skewed data?

### Answer

Because it is less influenced by extreme values.

---

## Question 5

What is the purpose of `cumsum()`?

### Answer

To compute a running cumulative sum.

---

## Question 6

Which operation computes the variability of data?

### Answer

`std()` (standard deviation) or `var()` (variance).

---

## Question 7

What is the time complexity of `sum()`?

### Answer

`O(n)` because every element must be processed.

---

## Question 8

Does `sum()` return a view or a copy?

### Answer

Neither. It computes and returns a new aggregated result.
```

---

# Assignment

1. Create a `(6, 4)` array using `np.random.randint()`.
2. Calculate:
   - Total sum
   - Row-wise sums
   - Column-wise sums
   - Overall mean
   - Row-wise means
   - Column-wise means
3. Determine:
   - Minimum and maximum values.
   - Their indices using `argmin()` and `argmax()`.
4. Compute:
   - Standard deviation
   - Variance
   - Cumulative sums
   - Cumulative products
5. Create a summary report showing all statistics and explain what each metric reveals about the dataset.

---

# Summary

In this lesson, you learned how to summarize and analyze numerical data using NumPy's aggregation functions. You explored `sum()`, `mean()`, `median()`, `std()`, `var()`, `min()`, `max()`, `argmin()`, `argmax()`, `cumsum()`, and `cumprod()`, while gaining a solid understanding of the `axis` parameter. These operations are fundamental for analytics, scientific computing, and machine learning, where large datasets must be reduced into meaningful statistics efficiently.

---

# Next Lesson

**File:**

[08-searching-sorting-and-filtering.md](08-searching-sorting-and-filtering.md)
