# NumPy Part 5: Reshaping & Array Layout

**Python Version Introduced:** Python 3.x

---

# Learning Objectives

By the end of this lesson, you will be able to:

- Understand how NumPy reshapes arrays without moving data.
- Explain when reshaping returns a View or creates a Copy.
- Use `reshape()`, `resize()`, `flatten()`, `ravel()`, `transpose()`, `swapaxes()`, `moveaxis()`, `expand_dims()`, and `squeeze()`.
- Understand C-order and Fortran-order memory layouts.
- Recognize contiguous and non-contiguous arrays.
- Choose the most memory-efficient reshaping operation.
- Avoid common reshaping mistakes.

---

# Recap

In the previous lesson, you learned:

- Basic indexing
- Slicing
- Boolean indexing
- Fancy indexing
- Views vs Copies during indexing

Those concepts are essential because reshaping also depends heavily on how an array is stored in memory.

---

# Why Reshape Arrays?

Imagine receiving data from different sources.

Examples:

A CSV file

```
10
20
30
40
50
60
```

An image

```
1920 × 1080 × 3
```

A neural network

```
(batch, height, width, channels)
```

Although the data is the same, different algorithms expect different shapes.

Reshaping lets us change how NumPy interprets the same memory without changing the underlying values.

---

# Shape vs Data

Consider

```python
import numpy as np

arr = np.arange(12)

print(arr)
```

Output

```
[0 1 2 3 4 5 6 7 8 9 10 11]
```

Memory

```
+--------------------------------------------+
|0|1|2|3|4|5|6|7|8|9|10|11|
+--------------------------------------------+
```

Now reshape it.

```python
matrix = arr.reshape(3, 4)

print(matrix)
```

Output

```
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
```

Did the data move?

No.

Only NumPy's interpretation of the memory changed.

---

# reshape()

## What does it do?

Returns an array with a new shape.

Whenever possible, it **does not copy the data**.

---

## Syntax

```python
array.reshape(shape)
```

or

```python
array.reshape(rows, columns)
```

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| shape | New dimensions |

---

## Return Value

Returns a reshaped ndarray.

---

## Example

```python
arr = np.arange(12)

matrix = arr.reshape(3, 4)

print(matrix)
```

Output

```
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
```

---

# Number of Elements Must Stay the Same

This works.

```python
arr = np.arange(12)

arr.reshape(2, 6)
```

This also works.

```python
arr.reshape(4, 3)
```

This fails.

```python
arr.reshape(5, 3)
```

Error

```
ValueError
```

Because

```
12 ≠ 15
```

NumPy cannot invent or discard data.

---

# Using -1

One dimension can be inferred automatically.

```python
arr = np.arange(12)

matrix = arr.reshape(3, -1)

print(matrix)
```

Output

```
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
```

NumPy calculates the missing dimension.

---

# Copy or View?

This is extremely important.

```python
arr = np.arange(12)

matrix = arr.reshape(3, 4)
```

Check memory.

```python
np.shares_memory(arr, matrix)
```

Output

```
True
```

Most reshapes return a **View**.

However, this is **not guaranteed**.

If the requested shape cannot be represented using the existing memory layout, NumPy may create a copy or raise an error, depending on the operation.

---

# resize()

## What does it do?

Changes the size of the array itself.

Unlike `reshape()`, it can change the total number of elements.

---

## Syntax

```python
array.resize(new_shape)
```

---

## Example

```python
arr = np.arange(6)

arr.resize((3, 4))

print(arr)
```

Output

```
[[0 1 2 3]
 [4 5 0 0]
 [0 0 0 0]]
```

New elements are filled with zeros.

---

## Shrinking

```python
arr = np.arange(10)

arr.resize((5,))

print(arr)
```

Output

```
[0 1 2 3 4]
```

Extra elements are discarded.

---

## Important Difference

| reshape() | resize() |
|-----------|----------|
| Returns new view/array | Modifies original array |
| Number of elements unchanged | Number of elements may change |

---

# flatten()

## What does it do?

Returns a one-dimensional version of an array.

---

## Syntax

```python
array.flatten()
```

---

## Example

```python
matrix = np.array([
    [1,2],
    [3,4]
])

flat = matrix.flatten()

print(flat)
```

Output

```
[1 2 3 4]
```

---

## Copy or View?

Always returns a **Copy**.

```python
flat[0] = 100

print(matrix)
```

Output

```
[[1 2]
 [3 4]]
```

The original array is unchanged.

---

# ravel()

## What does it do?

Returns a flattened array.

Unlike `flatten()`, it tries to avoid copying.

---

## Example

```python
flat = matrix.ravel()
```

---

## Copy or View?

Usually returns a **View**.

If that's impossible, it creates a Copy.

Verify.

```python
np.shares_memory(matrix, flat)
```

Often

```
True
```

---

# flatten() vs ravel()

| flatten() | ravel() |
|------------|---------|
| Always Copy | Usually View |
| More memory | Less memory |
| Safer | Faster |

---

# transpose()

## What does it do?

Swaps rows and columns.

---

## Syntax

```python
array.transpose()
```

or

```python
array.T
```

---

Example.

```python
matrix = np.array([
    [1,2,3],
    [4,5,6]
])

print(matrix.T)
```

Output

```
[[1 4]
 [2 5]
 [3 6]]
```

---

## Copy or View?

Usually returns a **View**.

Verify.

```python
np.shares_memory(matrix, matrix.T)
```

Usually

```
True
```

---

# swapaxes()

Useful for arrays with three or more dimensions.

Example.

```python
arr = np.zeros((2,3,4))

new = np.swapaxes(arr, 0, 2)

print(new.shape)
```

Output

```
(4,3,2)
```

---

# moveaxis()

Moves one axis to another position.

Example.

```python
arr = np.zeros((2,3,4))

new = np.moveaxis(arr, 0, -1)

print(new.shape)
```

Output

```
(3,4,2)
```

Useful in:

- Deep Learning
- Image Processing
- Scientific Computing

---

# expand_dims()

Adds a new axis.

Example.

```python
arr = np.array([1,2,3])

new = np.expand_dims(arr, axis=0)

print(new.shape)
```

Output

```
(1,3)
```

Another example.

```python
new = np.expand_dims(arr, axis=1)

print(new.shape)
```

Output

```
(3,1)
```

Useful for converting vectors into row or column matrices and preparing data for broadcasting or machine learning models.

---

# squeeze()

Removes axes of length 1.

```python
arr = np.zeros((1,3,1))

print(arr.shape)
```

Output

```
(1,3,1)
```

Now.

```python
new = np.squeeze(arr)

print(new.shape)
```

Output

```
(3,)
```

---

# C-Order vs Fortran-Order

NumPy stores arrays in **row-major order (C-order)** by default.

Example.

```
[[1 2 3]
 [4 5 6]]
```

Memory

```
1 2 3 4 5 6
```

Fortran-order stores columns first.

```
1 4 2 5 3 6
```

Check.

```python
arr.flags
```

Example.

```
C_CONTIGUOUS : True

F_CONTIGUOUS : False
```

Most NumPy code uses C-order.

Some scientific libraries use Fortran-order.

---

# Performance Notes

Operation | Usually Copy? | Complexity | Memory
----------|---------------|------------|--------
reshape() | Usually No | O(1) | O(1)
flatten() | Yes | O(n) | O(n)
ravel() | Usually No | O(1) | O(1)
transpose() | Usually No | O(1) | O(1)
expand_dims() | No | O(1) | O(1)
squeeze() | No | O(1) | O(1)

When an operation can return a view, it is generally much faster because it avoids copying the underlying data.

---

# Common Mistakes

## Mistake 1

Using `flatten()` when `ravel()` is sufficient.

This creates unnecessary copies.

---

## Mistake 2

Trying to reshape into an incompatible size.

```python
np.arange(10).reshape(3,4)
```

Raises a `ValueError`.

---

## Mistake 3

Assuming `reshape()` always returns a View.

It usually does, but not in every situation.

---

## Mistake 4

Confusing `resize()` and `reshape()`.

`resize()` changes the original array.

`reshape()` returns a reshaped array.

---

# Best Practices

- Prefer `reshape()` over manual loops.
- Use `-1` when one dimension can be inferred.
- Prefer `ravel()` for performance when a view is acceptable.
- Use `flatten()` only when you need an independent array.
- Use `.T` or `transpose()` to swap rows and columns.
- Verify memory sharing with `np.shares_memory()` when performance matters.

---

# Production Insight

Modern machine learning and data processing pipelines frequently reshape data between different stages.

Examples include:

- Converting images from `(height, width, channels)` to `(channels, height, width)`.
- Flattening feature maps before feeding them into dense neural network layers.
- Transforming one-dimensional sensor data into two-dimensional matrices for visualization.
- Preparing batches of data for GPU processing.

Efficient reshaping operations that reuse existing memory help reduce memory consumption and improve overall performance, especially when working with large datasets.

---

```markdown id="m6t2kp"
# Questions

### Question

> Why is `reshape()` usually faster than manually rearranging data?

### Answer

Because it typically changes only the array's metadata without copying the underlying data.

---

### Question

> What is the main difference between `flatten()` and `ravel()`?

### Answer

`flatten()` always returns a copy, while `ravel()` returns a view whenever possible.

---

### Question

> What does `reshape(-1, 4)` mean?

### Answer

NumPy automatically calculates the missing dimension while ensuring the total number of elements remains unchanged.

---

### Question

> Which operation modifies the original array: `reshape()` or `resize()`?

### Answer

`resize()` modifies the original array, whereas `reshape()` returns a reshaped array.
```

---

# Practical Lesson

Create the following array:

```python
arr = np.arange(24)
```

Complete these tasks:

1. Reshape it into:
   - `(4, 6)`
   - `(2, 3, 4)`
2. Use `-1` to infer one dimension automatically.
3. Flatten the array using both `flatten()` and `ravel()`.
4. Check whether each flattened array shares memory with the original.
5. Transpose a 3×4 matrix and verify whether it shares memory.
6. Add and remove dimensions using `expand_dims()` and `squeeze()`.
7. Inspect the array's `C_CONTIGUOUS` and `F_CONTIGUOUS` flags before and after transposing.

---

```markdown id="p3w8nc"
# Knowledge Check

## Question 1

What condition must always be true when using `reshape()`?

### Answer

The total number of elements must remain the same.

---

## Question 2

Which function always returns a copy: `flatten()` or `ravel()`?

### Answer

`flatten()`.

---

## Question 3

What does `reshape(-1, n)` allow NumPy to do?

### Answer

Automatically calculate the missing dimension.

---

## Question 4

Which function changes the size of the original array?

### Answer

`resize()`.

---

## Question 5

Does `transpose()` usually return a view or a copy?

### Answer

It usually returns a view.

---

## Question 6

What is the purpose of `expand_dims()`?

### Answer

To insert a new axis of length 1 into an array.

---

## Question 7

What does `squeeze()` do?

### Answer

It removes axes whose length is 1.

---

## Question 8

Why is `ravel()` generally more memory-efficient than `flatten()`?

### Answer

Because it reuses the existing data buffer whenever possible instead of creating a new copy.
```

---

# Assignment

1. Create a 3×4 matrix using `np.arange()`.
2. Perform the following operations:
   - Reshape it into `(2, 6)` and `(4, 3)`.
   - Flatten it using both `flatten()` and `ravel()`.
   - Transpose the matrix.
   - Add a new dimension at the beginning and end using `expand_dims()`.
   - Remove singleton dimensions using `squeeze()`.
3. For each resulting array, record:
   - Shape
   - `C_CONTIGUOUS`
   - `F_CONTIGUOUS`
   - Whether it shares memory with the original array
4. Create a comparison table showing which operations returned views and which returned copies, and explain why each behavior is beneficial in real-world applications.

---

# Summary

In this lesson, you learned how NumPy changes the interpretation of array data through reshaping operations without necessarily moving data in memory. You explored `reshape()`, `resize()`, `flatten()`, `ravel()`, `transpose()`, `swapaxes()`, `moveaxis()`, `expand_dims()`, and `squeeze()`, while understanding when these operations return views or copies. You also learned about C-order and Fortran-order memory layouts and why choosing the right reshaping operation is important for both performance and memory efficiency.

---

# Next Lesson

**File:**

[06-vectorization-and-broadcasting.md](06-vectorization-and-broadcasting.md)
