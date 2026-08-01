# NumPy Part 2: Creating NumPy Arrays

**Python Version Introduced:** Python 3.x

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will be able to:

- Create arrays using the most commonly used NumPy functions.
- Choose the appropriate array creation function for different scenarios.
- Understand how `np.array()` creates arrays from Python objects.
- Learn how `dtype` is inferred and how to control it.
- Understand memory implications of array creation.
- Learn which creation functions allocate new memory.
- Understand common pitfalls while creating arrays.
- Apply best practices used in production code.

______________________________________________________________________

# Recap

In the previous lesson, you learned:

- Why NumPy exists.
- The difference between Python lists and NumPy arrays.
- Contiguous memory.
- Homogeneous data.
- `shape`, `size`, `ndim`, `dtype`, `itemsize`, and `nbytes`.
- A high-level introduction to Views vs Copies.

In this lesson, we'll learn the various ways to create NumPy arrays efficiently.

______________________________________________________________________

# Why Does NumPy Have So Many Array Creation Functions?

A common question is:

> "Why can't I just use `np.array()` everywhere?"

Technically, you can.

However, different scenarios require different initialization strategies.

For example:

| Scenario | Best Function |
|----------|---------------|
| Existing Python data | `array()` |
| Empty matrix of zeros | `zeros()` |
| Matrix of ones | `ones()` |
| Fixed constant values | `full()` |
| Allocate memory only | `empty()` |
| Sequential integers | `arange()` |
| Evenly spaced values | `linspace()` |
| Identity matrix | `eye()` |

Choosing the right function makes code more readable and often more efficient.

______________________________________________________________________

# Creating Arrays with `np.array()`

## What does it do?

Creates a NumPy array from an existing Python object such as:

- list
- tuple
- nested list
- another NumPy array

______________________________________________________________________

## Syntax

```python
np.array(object, dtype=None, copy=True)
```

______________________________________________________________________

## Important Parameters

| Parameter | Description |
|-----------|-------------|
| `object` | Input data |
| `dtype` | Desired data type |
| `copy` | Whether a copy should be made when possible |

______________________________________________________________________

## Example

```python
import numpy as np

numbers = np.array([10, 20, 30])

print(numbers)
```

Output

```
[10 20 30]
```

______________________________________________________________________

## Nested Lists

```python
matrix = np.array([
    [1, 2],
    [3, 4]
])

print(matrix)
```

Output

```
[[1 2]
 [3 4]]
```

______________________________________________________________________

# How Does NumPy Determine the Data Type?

If `dtype` isn't specified, NumPy chooses one that can represent all elements.

Example:

```python
arr = np.array([1, 2, 3])

print(arr.dtype)
```

Output

```
int64
```

Now mix integers and floats.

```python
arr = np.array([1, 2, 3.5])

print(arr)
print(arr.dtype)
```

Output

```
[1.  2.  3.5]

float64
```

The integers are automatically promoted to floating-point values.

______________________________________________________________________

# Specifying the Data Type

You can explicitly control the data type.

```python
arr = np.array(
    [1, 2, 3],
    dtype=np.float32
)

print(arr.dtype)
```

Output

```
float32
```

This is common when memory usage matters.

______________________________________________________________________

# Should You Specify `dtype`?

For small arrays, it doesn't matter much.

For very large datasets, it matters significantly.

Example:

Suppose you store 100 million integers.

| dtype | Memory per element |
|--------|--------------------|
| int32 | 4 bytes |
| int64 | 8 bytes |

Choosing `int32` instead of `int64` could reduce memory usage by hundreds of megabytes.

______________________________________________________________________

# Does `np.array()` Create a Copy?

This is one of the most common questions.

### Case 1: Python List

```python
numbers = [1, 2, 3]

arr = np.array(numbers)
```

A **new NumPy array** is created.

Changing the original list does **not** affect the array.

```python
numbers[0] = 100

print(numbers)
print(arr)
```

Output

```
[100, 2, 3]

[1 2 3]
```

______________________________________________________________________

### Case 2: Existing NumPy Array

```python
arr1 = np.array([1, 2, 3])

arr2 = np.array(arr1)
```

By default, a copy is created.

```python
arr2[0] = 100

print(arr1)
print(arr2)
```

Output

```
[1 2 3]

[100 2 3]
```

______________________________________________________________________

### Using `copy=False`

```python
arr2 = np.array(arr1, copy=False)
```

NumPy will try to avoid creating a copy.

> **Note:** `copy=False` is a request, not a guarantee. If NumPy needs a new array (for example, because of a required dtype conversion), it may still create one.

We'll revisit this topic in the Memory Model lesson.

______________________________________________________________________

# Creating Arrays Filled with Zeros

## What does it do?

Creates an array where every element is zero.

______________________________________________________________________

## Syntax

```python
np.zeros(shape, dtype=float)
```

______________________________________________________________________

## Example

```python
arr = np.zeros(5)

print(arr)
```

Output

```
[0. 0. 0. 0. 0.]
```

______________________________________________________________________

Matrix example.

```python
matrix = np.zeros((3, 4))

print(matrix)
```

Output

```
[[0. 0. 0. 0.]
 [0. 0. 0. 0.]
 [0. 0. 0. 0.]]
```

______________________________________________________________________

## Copy or View?

Creates a **new array**.

Every call allocates new memory.

______________________________________________________________________

## Common Use Cases

- Placeholder arrays
- Machine learning weight initialization
- Image buffers
- Scientific computations

______________________________________________________________________

# Creating Arrays Filled with Ones

```python
matrix = np.ones((2, 3))

print(matrix)
```

Output

```
[[1. 1. 1.]
 [1. 1. 1.]]
```

______________________________________________________________________

## Copy or View?

Always allocates new memory.

______________________________________________________________________

# Creating Arrays Filled with Any Value

```python
arr = np.full((2, 4), 7)

print(arr)
```

Output

```
[[7 7 7 7]
 [7 7 7 7]]
```

______________________________________________________________________

## When Should You Use `full()`?

Instead of:

```python
np.ones((5, 5)) * 100
```

Prefer:

```python
np.full((5, 5), 100)
```

It's clearer and expresses your intent directly.

______________________________________________________________________

# Creating Empty Arrays

```python
arr = np.empty((3, 3))

print(arr)
```

Possible output

```
[[6.9e-310 6.9e-310 0.0e+000]
 [6.9e-310 6.9e-310 0.0e+000]
 [0.0e+000 0.0e+000 0.0e+000]]
```

The values are unpredictable.

NumPy only allocates memory.

It does **not** initialize it.

______________________________________________________________________

## When Should You Use `empty()`?

Only when:

- Performance matters.
- Every element will be overwritten before being read.

Otherwise, prefer `zeros()`.

______________________________________________________________________

# Creating Identity Matrices

```python
identity = np.eye(4)

print(identity)
```

Output

```
[[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]
```

Identity matrices are common in:

- Linear algebra
- Machine learning
- Computer graphics

______________________________________________________________________

# `eye()` vs `identity()`

```python
np.eye(3)
```

```python
np.identity(3)
```

Both create square identity matrices.

`eye()` is generally preferred because it also supports rectangular matrices and diagonal offsets.

______________________________________________________________________

# Creating Sequential Values with `arange()`

## Syntax

```python
np.arange(start, stop, step)
```

______________________________________________________________________

Example

```python
arr = np.arange(0, 10, 2)

print(arr)
```

Output

```
[0 2 4 6 8]
```

Notice that the stop value is excluded, just like Python's `range()`.

______________________________________________________________________

# Creating Evenly Spaced Values with `linspace()`

## Syntax

```python
np.linspace(start, stop, num)
```

______________________________________________________________________

Example

```python
arr = np.linspace(0, 1, 5)

print(arr)
```

Output

```
[0.
 0.25
 0.50
 0.75
 1.]
```

Unlike `arange()`, the end value is included by default.

______________________________________________________________________

# `arange()` vs `linspace()`

| `arange()` | `linspace()` |
|------------|--------------|
| Uses step size | Uses number of values |
| End value excluded | End value included by default |
| Best for integer sequences | Best for numerical sampling |

A simple rule:

- Know the step → `arange()`
- Know how many values → `linspace()`

______________________________________________________________________

# Introduction to Random Arrays

```python
arr = np.random.randint(
    1,
    100,
    size=5
)

print(arr)
```

Possible output

```
[12 45 81  6 39]
```

We'll study random number generation in detail in a dedicated lesson.

______________________________________________________________________

# Common Mistakes

### Forgetting the Shape Tuple

Incorrect

```python
np.zeros(3, 4)
```

Correct

```python
np.zeros((3, 4))
```

______________________________________________________________________

### Assuming `empty()` Returns Zeros

Incorrect assumption:

```python
arr = np.empty(5)
```

Never rely on its initial values.

______________________________________________________________________

### Using `arange()` with Floating-Point Steps

```python
np.arange(0, 1, 0.1)
```

Floating-point precision can sometimes produce unexpected results.

For evenly spaced floating-point values, prefer `linspace()`.

______________________________________________________________________

### Forgetting to Specify `dtype` for Large Arrays

The default data type may consume more memory than necessary.

When appropriate, choose a smaller type such as `float32` or `int32`.

______________________________________________________________________

# Best Practices

- Use `array()` for existing data.
- Specify `dtype` when memory usage matters.
- Prefer `full()` over multiplying an array of ones.
- Use `zeros()` instead of `empty()` unless you're certain every value will be overwritten.
- Use `linspace()` for evenly spaced floating-point values.
- Use `eye()` instead of `identity()` for greater flexibility.

______________________________________________________________________

# Production Insight

Creating arrays efficiently is the first step in building performant numerical applications.

For example:

- Computer vision libraries allocate image buffers using array creation functions.
- Machine learning frameworks initialize model parameters with zeros, ones, or random values.
- Financial applications generate time intervals using `arange()` or `linspace()`.
- Scientific simulations allocate large arrays before performing numerical computations.

Choosing the appropriate array creation function improves readability and can reduce unnecessary memory allocations.

______________________________________________________________________

```markdown id="b3x9vn"
# Questions

### Question

> Why should you prefer `linspace()` over `arange()` for evenly spaced floating-point values?

### Answer

Because `linspace()` generates a fixed number of evenly spaced values and avoids floating-point step accumulation issues that can occur with `arange()`.

---

### Question

> Does `np.zeros()` return a view or allocate new memory?

### Answer

It always allocates a new array with its own memory.

---

### Question

> What is the purpose of the `dtype` parameter?

### Answer

It specifies the data type of the array, allowing you to control memory usage and numerical precision.

---

### Question

> Does `np.array(existing_array)` always share memory with the original array?

### Answer

No. By default, it creates a copy. Using `copy=False` allows NumPy to avoid copying when possible, but it is not guaranteed.
```

______________________________________________________________________

# Practical Lesson

Write a program that:

1. Creates a one-dimensional array from a Python list.
1. Creates:
   - A 4×4 zero matrix.
   - A 3×5 matrix of ones.
   - A 2×3 matrix filled with the value `99`.
1. Creates:
   - An identity matrix.
   - An array using `arange()`.
   - An array using `linspace()`.
1. Creates arrays using both `int32` and `int64` and compares their `itemsize` and `nbytes`.
1. Experiment with `copy=False` using an existing NumPy array and observe whether the arrays share memory (don't worry if the behaviour isn't always the same—we'll explain it fully in the next lesson).

______________________________________________________________________

```markdown id="g5n8tw"
# Knowledge Check

## Question 1

When should you use `np.array()`?

### Answer

When you already have existing data, such as a Python list, tuple, or another array, that you want to convert into a NumPy array.

---

## Question 2

What is the main difference between `arange()` and `linspace()`?

### Answer

`arange()` generates values based on a step size, while `linspace()` generates a specified number of evenly spaced values.

---

## Question 3

Why is `np.empty()` generally faster than `np.zeros()`?

### Answer

Because it allocates memory without initializing the elements.

---

## Question 4

Which function is more appropriate for creating a matrix filled with the value `50`?

### Answer

`np.full()`.

---

## Question 5

Does `copy=False` guarantee that no copy will be made?

### Answer

No. It only tells NumPy to avoid copying if possible. A copy may still be created if required.

---

## Question 6

Why might you explicitly choose `float32` instead of `float64`?

### Answer

To reduce memory usage when the additional precision of `float64` is unnecessary.
```

______________________________________________________________________

# Assignment

1. Create arrays using every function covered in this lesson:
   - `array()`
   - `zeros()`
   - `ones()`
   - `full()`
   - `empty()`
   - `eye()`
   - `arange()`
   - `linspace()`
1. Compare the memory usage (`itemsize` and `nbytes`) of arrays created with `int32`, `int64`, `float32`, and `float64`.
1. Compare the outputs of `arange(0, 1, 0.1)` and `linspace(0, 1, 10)` and explain the differences.
1. Create a NumPy array from another NumPy array using both the default behaviour and `copy=False`. Observe how changes to one array affect the other, and note your observations. We'll explain the underlying reasons in the next lesson.

______________________________________________________________________

# Summary

In this lesson, you learned the most common ways to create NumPy arrays and when to use each approach. You explored
`array()`, `zeros()`, `ones()`, `full()`, `empty()`, `eye()`, `arange()`, and `linspace()`, learned how NumPy infers
data types, how to control them with `dtype`, and the memory implications of different choices. You also received an
introduction to copy behaviour, preparing you for the next lesson on NumPy's memory model.

______________________________________________________________________

# Next Lesson

**File:**

[03-numpy-memory-model-views-and-copies.md](03-numpy-memory-model-views-and-copies.md)
