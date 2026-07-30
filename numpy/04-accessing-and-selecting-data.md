# NumPy Part 4: Accessing & Selecting Data

**Python Version Introduced:** Python 3.x

---

# Learning Objectives

By the end of this lesson, you will be able to:

- Access elements from NumPy arrays using indexing.
- Use slicing to extract portions of an array.
- Understand negative indexing.
- Apply Boolean indexing and Fancy indexing.
- Predict which operations return a **View** and which return a **Copy**.
- Avoid common indexing mistakes.
- Write efficient and readable array selection code.

---

# Recap

In the previous lesson, you learned about NumPy's memory model:

- Assignment vs Copy
- Views vs Copies
- Memory sharing
- `OWNDATA`
- `base`
- `np.shares_memory()`
- Contiguous vs Non-contiguous arrays

This lesson builds directly on those concepts because many indexing operations either share or duplicate memory.

---

# Why Data Selection Matters

Creating arrays is only the first step.

Most real-world tasks involve selecting data.

Examples:

- Selecting a specific row from a dataset.
- Extracting a column from a CSV.
- Cropping an image.
- Filtering customers older than 30.
- Selecting pixels above a threshold.

Efficient data selection is one of the most frequently used operations in NumPy.

---

# Indexing Basics

Consider the following array.

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])
```

Access the first element.

```python
print(arr[0])
```

Output

```
10
```

Second element.

```python
print(arr[1])
```

Output

```
20
```

Last element.

```python
print(arr[4])
```

Output

```
50
```

---

# Negative Indexing

Negative indices count from the end.

```python
print(arr[-1])
```

Output

```
50
```

```python
print(arr[-2])
```

Output

```
40
```

This is often cleaner than calculating the last index manually.

---

# Indexing Multi-Dimensional Arrays

```python
matrix = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])
```

Access row 0, column 1.

```python
print(matrix[0, 1])
```

Output

```
20
```

Equivalent to:

```python
print(matrix[0][1])
```

However, the comma notation is preferred because it is faster and more readable.

---

# Selecting Entire Rows

First row.

```python
print(matrix[0])
```

Output

```
[10 20 30]
```

Second row.

```python
print(matrix[1])
```

Output

```
[40 50 60]
```

---

# Selecting Entire Columns

First column.

```python
print(matrix[:, 0])
```

Output

```
[10 40 70]
```

Second column.

```python
print(matrix[:, 1])
```

Output

```
[20 50 80]
```

Remember:

```
matrix[row, column]
```

A colon (`:`) means "select everything along this axis."

---

# Slicing

General syntax:

```python
array[start:stop:step]
```

Like Python lists:

- `start` is inclusive.
- `stop` is exclusive.
- `step` is optional.

---

Example.

```python
arr = np.array([10, 20, 30, 40, 50])

print(arr[1:4])
```

Output

```
[20 30 40]
```

---

Skipping elements.

```python
print(arr[::2])
```

Output

```
[10 30 50]
```

---

Reversing an array.

```python
print(arr[::-1])
```

Output

```
[50 40 30 20 10]
```

---

# Slicing Multi-Dimensional Arrays

```python
matrix = np.array([
    [10,20,30],
    [40,50,60],
    [70,80,90]
])
```

Rows 0 and 1.

```python
print(matrix[0:2])
```

Output

```
[[10 20 30]
 [40 50 60]]
```

---

Columns 1 and 2.

```python
print(matrix[:,1:3])
```

Output

```
[[20 30]
 [50 60]
 [80 90]]
```

---

Submatrix.

```python
print(matrix[1:,1:])
```

Output

```
[[50 60]
 [80 90]]
```

---

# Does Slicing Return a View or Copy?

This is one of the most important NumPy concepts.

```python
arr = np.arange(6)

slice_arr = arr[1:4]
```

Modify the slice.

```python
slice_arr[:] = 100

print(arr)
```

Output

```
[  0 100 100 100   4   5]
```

The original array changed.

Why?

Because **basic slicing returns a View.**

---

Verify.

```python
print(np.shares_memory(arr, slice_arr))
```

Output

```
True
```

---

# Boolean Indexing

Boolean indexing selects elements matching a condition.

```python
arr = np.array([10,20,30,40,50])

result = arr[arr > 25]

print(result)
```

Output

```
[30 40 50]
```

Another example.

```python
print(arr[arr % 20 == 0])
```

Output

```
[20 40]
```

Boolean indexing is extremely common in data analysis.

---

# Does Boolean Indexing Return a View?

No.

Boolean indexing creates a **Copy**.

Example.

```python
arr = np.array([10,20,30,40])

selected = arr[arr > 20]

selected[0] = 999

print(arr)
```

Output

```
[10 20 30 40]
```

The original array is unchanged.

Verify.

```python
print(np.shares_memory(arr, selected))
```

Output

```
False
```

---

# Fancy Indexing

Fancy indexing uses an array (or list) of indices.

```python
arr = np.array([10,20,30,40,50])

selected = arr[[0,2,4]]

print(selected)
```

Output

```
[10 30 50]
```

Indices can be repeated.

```python
print(arr[[2,2,2]])
```

Output

```
[30 30 30]
```

---

# Does Fancy Indexing Return a View?

No.

Fancy indexing always creates a **Copy**.

```python
selected = arr[[1,3]]

selected[:] = 0

print(arr)
```

Output

```
[10 20 30 40 50]
```

Verify.

```python
print(np.shares_memory(arr, selected))
```

Output

```
False
```

---

# Copy vs View Summary

| Operation | View | Copy |
|-----------|:----:|:----:|
| Assignment (`=`) | ✅ | ❌ |
| Basic slicing | ✅ | ❌ |
| `view()` | ✅ | ❌ |
| Boolean indexing | ❌ | ✅ |
| Fancy indexing | ❌ | ✅ |
| `copy()` | ❌ | ✅ |

This table is worth remembering.

---

# Performance Notes

Suppose an array contains 100 million elements.

Basic slicing:

```python
arr[1000:5000]
```

Creates only another view.

Almost no additional memory.

---

Boolean indexing:

```python
arr[arr > 50]
```

Creates a completely new array.

Requires additional memory proportional to the number of selected elements.

---

Fancy indexing:

```python
arr[[1,5,9]]
```

Also creates a new array.

---

# Common Mistakes

## Mistake 1

Assuming slicing creates a copy.

```python
part = arr[:5]
```

It doesn't.

Changes affect the original.

---

## Mistake 2

Using chained indexing.

Instead of:

```python
matrix[0][1]
```

Prefer:

```python
matrix[0,1]
```

It is clearer and avoids creating intermediate objects.

---

## Mistake 3

Expecting Boolean indexing to modify the original.

```python
selected = arr[arr > 10]
```

`selected` is independent.

---

## Mistake 4

Confusing row and column selection.

```
matrix[1]
```

Returns row 2.

```
matrix[:,1]
```

Returns column 2.

---

# Best Practices

- Use comma indexing for multi-dimensional arrays.
- Prefer slicing when possible because it avoids unnecessary copies.
- Use Boolean indexing for filtering.
- Use Fancy indexing when selecting arbitrary positions.
- Verify memory sharing with `np.shares_memory()` when debugging.

---

# Production Insight

Imagine processing a dataset with 50 million records.

Using slicing to process chunks avoids unnecessary memory allocation because slices share memory.

On the other hand, Boolean indexing creates new arrays, which is often necessary for filtering but increases memory usage.

Understanding which operations create copies helps you write scalable data processing pipelines.

---

```markdown id="u6f9qc"
# Questions

### Question

> Which indexing operation usually returns a View?

### Answer

Basic slicing.

---

### Question

> Which indexing operations always return a Copy?

### Answer

Boolean indexing and Fancy indexing.

---

### Question

> How do you select the second column of a matrix?

### Answer

```python
matrix[:,1]
```

---

### Question

> Why is `matrix[0,1]` preferred over `matrix[0][1]`?

### Answer

It is more efficient, more readable, and avoids creating an intermediate object.
```

---

# Practical Lesson

Using the following matrix:

```python
matrix = np.array([
    [10,20,30,40],
    [50,60,70,80],
    [90,100,110,120],
    [130,140,150,160]
])
```

Perform the following tasks:

1. Select the third row.
2. Select the second column.
3. Extract the top-left 2×2 submatrix.
4. Reverse the rows.
5. Select all values greater than 75.
6. Select rows 1 and 3 using Fancy indexing.
7. Verify which results share memory with the original array using `np.shares_memory()`.

---

```markdown id="d4y7ms"
# Knowledge Check

## Question 1

Does basic slicing return a View or a Copy?

### Answer

A View.

---

## Question 2

Does Fancy indexing return a View or a Copy?

### Answer

A Copy.

---

## Question 3

How do you select every row from the third column?

### Answer

```python
array[:,2]
```

---

## Question 4

How do you reverse an array using slicing?

### Answer

```python
array[::-1]
```

---

## Question 5

Why is Boolean indexing more memory-intensive than slicing?

### Answer

Because Boolean indexing creates a new array containing the selected elements, while slicing usually shares the original memory.

---

## Question 6

How can you verify whether two arrays share memory?

### Answer

Use:

```python
np.shares_memory(array1, array2)
```
```

---

# Assignment

1. Create a 5×5 matrix using `np.arange()` and `reshape()`.
2. Perform:
   - Row selection
   - Column selection
   - Submatrix extraction
   - Reverse the rows
   - Reverse the columns
3. Filter all even numbers using Boolean indexing.
4. Select the first, third, and fifth rows using Fancy indexing.
5. For every operation, determine whether the result is a **View** or a **Copy** by using:
   - `np.shares_memory()`
   - `.base`
   - `OWNDATA`

Create a summary table listing each operation and whether it shares memory with the original array.

---

# Summary

In this lesson, you learned how to access and select data efficiently using indexing, slicing, Boolean indexing, and Fancy indexing. More importantly, you learned which operations return **Views** and which create **Copies**, allowing you to predict memory usage and avoid subtle bugs. This knowledge is fundamental for writing efficient NumPy code and prepares you for the next lesson, where you'll explore reshaping arrays and how memory layout affects operations such as `reshape()`, `flatten()`, and `transpose()`.

---

# Next Lesson

**File:**

[05-reshaping-and-array-layout.md](05-reshaping-and-array-layout.md)
