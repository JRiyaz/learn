# File

`numpy/01-numpy-architecture-and-ndarray-fundamentals.md`

# NumPy Part 1: NumPy Architecture & ndarray Fundamentals

**Python Version Introduced:** Python 3.x

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will be able to:

- Explain why NumPy exists.
- Understand the limitations of Python lists for numerical computing.
- Describe what an `ndarray` is.
- Understand how NumPy stores data in memory.
- Explain contiguous memory and homogeneous data.
- Understand `shape`, `size`, `ndim`, `dtype`, `itemsize`, and `nbytes`.
- Understand the difference between Python objects and NumPy arrays.
- Learn when NumPy is the right choice.
- Gain a high-level understanding of Views vs Copies (covered in depth later).

______________________________________________________________________

# Recap

Before learning NumPy, you should already be comfortable with:

- Variables
- Functions
- Classes
- Lists
- Tuples
- Dictionaries
- Loops
- Modules
- Packages
- Virtual Environments

NumPy extends Python—it does **not** replace it.

______________________________________________________________________

# Why Was NumPy Created?

Python is a fantastic general-purpose language.

However, it was never designed for large-scale numerical computation.

Imagine processing:

- 10 million stock prices
- 4K image pixels
- GPS coordinates
- Scientific simulations
- Machine Learning datasets

Python lists become inefficient for these workloads because every element is a full Python object.

NumPy was created to solve this problem.

Its goals are:

- Faster computation
- Less memory usage
- Efficient mathematical operations
- Better CPU cache utilisation
- Vectorized computation

Today, almost every scientific and machine learning library in Python is built on top of NumPy.

______________________________________________________________________

# Python List Internals

Let's create a simple list.

```python
numbers = [10, 20, 30]
```

It looks like this:

```
[10, 20, 30]
```

Internally, it is **not** stored like this.

It is closer to:

```
List

┌───────────┐
│ Pointer ──────────────┐
├───────────┤           │
│ Pointer ────────┐     │
├───────────┤     │     │
│ Pointer ──┐     │     │
└───────────┘     │     │
                  ▼     ▼

          Python Integer Objects

        +-----------+
        | int: 10   |
        +-----------+

        +-----------+
        | int: 20   |
        +-----------+

        +-----------+
        | int: 30   |
        +-----------+
```

Each integer is a complete Python object containing:

- Object header
- Reference count
- Type information
- Actual value

This design makes Python incredibly flexible.

It also introduces overhead.

______________________________________________________________________

# Why Is This Slow?

Suppose you have one million integers.

Python stores:

- One million integer objects
- One million references
- One million object headers

The CPU must constantly jump around memory to read the values.

This leads to:

- More memory usage
- Poor cache locality
- Slower computations

______________________________________________________________________

# NumPy's Solution

NumPy stores raw values directly in memory.

Instead of storing Python objects:

```
10
20
30
40
50
```

Memory looks like:

```
+----+----+----+----+----+
|10  |20  |30  |40  |50  |
+----+----+----+----+----+
```

Every element occupies the same number of bytes.

No Python objects.

No pointers.

Just raw numerical values.

______________________________________________________________________

# Contiguous Memory

This is one of NumPy's biggest advantages.

Contiguous memory means every element is stored immediately after the previous one.

```
Address

1000 -> 10

1008 -> 20

1016 -> 30

1024 -> 40

1032 -> 50
```

Because the CPU reads neighbouring memory very efficiently, operations become dramatically faster.

This is one of the main reasons NumPy outperforms Python lists for numerical work.

______________________________________________________________________

# Homogeneous Data

Python lists can contain anything.

```python
items = [
    10,
    "Hello",
    True,
    3.14
]
```

NumPy arrays are designed to store elements of the same data type.

```python
import numpy as np

numbers = np.array([10, 20, 30])
```

Every element is an integer.

Another example:

```python
temperatures = np.array([
    36.2,
    36.7,
    37.1
])
```

Every element is a floating-point number.

Homogeneous storage allows NumPy to:

- Use less memory
- Execute compiled operations efficiently
- Predict the location of every element instantly

______________________________________________________________________

# Creating Your First ndarray

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print(arr)
```

Output

```
[1 2 3 4 5]
```

Check its type.

```python
type(arr)
```

Output

```
<class 'numpy.ndarray'>
```

______________________________________________________________________

# What is an ndarray?

`ndarray` stands for:

**N-Dimensional Array**

It is the core data structure in NumPy.

Everything in NumPy revolves around the `ndarray`.

Whether you're working with:

- A list of numbers
- A spreadsheet
- An image
- Audio samples
- Scientific measurements

they are all represented as `ndarray` objects.

______________________________________________________________________

# Understanding Dimensions

## 0-D (Scalar)

```python
np.array(42)
```

Output

```
42
```

______________________________________________________________________

## 1-D

```python
np.array([1, 2, 3])
```

______________________________________________________________________

## 2-D

```python
np.array([
    [1,2,3],
    [4,5,6]
])
```

______________________________________________________________________

## 3-D

```python
np.array([
    [
        [1,2],
        [3,4]
    ],
    [
        [5,6],
        [7,8]
    ]
])
```

Images, videos and deep learning tensors often use higher-dimensional arrays.

______________________________________________________________________

# Important ndarray Attributes

Consider:

```python
arr = np.array([
    [10,20,30],
    [40,50,60]
])
```

______________________________________________________________________

## shape

```python
arr.shape
```

Output

```
(2, 3)
```

Meaning:

- 2 rows
- 3 columns

______________________________________________________________________

## ndim

```python
arr.ndim
```

Output

```
2
```

Number of dimensions.

______________________________________________________________________

## size

```python
arr.size
```

Output

```
6
```

Total number of elements.

______________________________________________________________________

## dtype

```python
arr.dtype
```

Possible output

```
int64
```

Represents the data type stored in the array.

______________________________________________________________________

## itemsize

```python
arr.itemsize
```

Possible output

```
8
```

Each integer occupies **8 bytes** (`int64`).

If the array used `int32`, the value would typically be **4 bytes**.

This is useful when working with large datasets, where choosing a smaller data type can significantly reduce memory
usage.

______________________________________________________________________

## nbytes

```python
arr.nbytes
```

Output

```
48
```

Calculation:

```
6 elements × 8 bytes = 48 bytes
```

Unlike `sys.getsizeof()`, `nbytes` reports only the memory used by the array's data buffer.

______________________________________________________________________

# Why `dtype` Matters

Consider:

```python
arr = np.array([1, 2, 3], dtype=np.int32)
```

Each value typically uses **4 bytes**.

Now:

```python
arr = np.array([1, 2, 3], dtype=np.int64)
```

Each value typically uses **8 bytes**.

For an array with 100 million integers, choosing the appropriate `dtype` can save hundreds of megabytes of memory.

We'll explore data types in more detail in a later lesson.

______________________________________________________________________

# Views vs Copies (Introduction)

Suppose:

```python
arr = np.array([1,2,3])
```

Some NumPy operations create a **View**.

A view shares the same underlying memory.

```
Original Array
      │
      ▼
+------------------+
| 1 2 3 4 5 6      |
+------------------+
      ▲
      │
     View
```

Modifying the view also modifies the original array.

Other operations create a **Copy**.

```
Original

1 2 3

Copy

1 2 3
```

The copy has its own memory.

Changes do **not** affect the original.

This distinction is extremely important for both correctness and performance.

We'll dedicate an entire lesson to it later.

______________________________________________________________________

# Where is NumPy Used?

NumPy is the foundation for many Python libraries:

- Pandas
- Matplotlib
- Seaborn
- SciPy
- Scikit-Learn
- OpenCV
- TensorFlow
- PyTorch (conceptually similar tensors)

If you understand NumPy well, learning these libraries becomes much easier.

______________________________________________________________________

# Best Practices

- Import NumPy as `np`.
- Choose an appropriate `dtype`.
- Use NumPy arrays instead of Python lists for numerical computations.
- Prefer vectorized operations over Python loops (covered later).
- Understand memory usage before working with large datasets.

______________________________________________________________________

# Production Insight

In production systems, arrays can contain millions of values.

For example:

- Image processing pipelines
- Recommendation systems
- Fraud detection
- Scientific simulations
- Machine learning training

A poor choice of `dtype` or unnecessary memory copies can increase memory usage dramatically and slow down applications.

Engineers working with data-intensive systems routinely consider memory layout, data types, and copy behaviour to build
efficient solutions.

______________________________________________________________________

```markdown id="t9c4zs"
# Questions

### Question

> Why is a NumPy array generally faster than a Python list for numerical computations?

### Answer

Because NumPy stores homogeneous data in contiguous memory and performs operations using optimized compiled code, whereas Python lists store references to individual Python objects.

---

### Question

> What does `itemsize` represent?

### Answer

The number of bytes used to store a single element in the array.

---

### Question

> What is the difference between `size` and `nbytes`?

### Answer

`size` is the total number of elements, while `nbytes` is the total memory consumed by the array's data buffer (`size × itemsize`).

---

### Question

> What is the difference between a View and a Copy?

### Answer

A View shares the same underlying memory as the original array, whereas a Copy allocates new memory and is completely independent.
```

______________________________________________________________________

# Practical Lesson

Write a program that:

1. Creates a 2×3 NumPy array.
1. Prints:
   - `shape`
   - `ndim`
   - `size`
   - `dtype`
   - `itemsize`
   - `nbytes`
1. Create another array with `dtype=np.int32` and compare `itemsize` and `nbytes`.
1. Repeat using `dtype=np.float64`.
1. Explain how changing the data type affects memory usage.

______________________________________________________________________

```markdown id="w7n6pf"
# Knowledge Check

## Question 1

Why are Python lists inefficient for large numerical computations?

### Answer

Because each element is stored as a separate Python object with additional metadata, leading to higher memory usage and slower access.

---

## Question 2

What does `ndarray` stand for?

### Answer

N-Dimensional Array.

---

## Question 3

What information does the `shape` attribute provide?

### Answer

The size of each dimension in the array.

---

## Question 4

How is `nbytes` calculated?

### Answer

`nbytes = size × itemsize`

---

## Question 5

Which attribute tells you the number of bytes occupied by a single element?

### Answer

`itemsize`

---

## Question 6

What is the key difference between a View and a Copy?

### Answer

A View shares memory with the original array, while a Copy has its own separate memory.
```

______________________________________________________________________

# Assignment

1. Compare a Python list and a NumPy array containing one million integers.
1. Measure:
   - `itemsize`
   - `nbytes`
   - `dtype`
1. Create arrays using:
   - `int32`
   - `int64`
   - `float32`
   - `float64`
1. Record how memory usage changes for each data type.
1. Research two real-world applications where reducing memory usage with an appropriate `dtype` would have a significant impact.

______________________________________________________________________

# Summary

In this lesson, you learned why NumPy was created and how its `ndarray` differs fundamentally from Python lists. You
explored contiguous memory, homogeneous data, core array attributes such as `shape`, `size`, `ndim`, `dtype`,
`itemsize`, and `nbytes`, and gained an introduction to views and copies. These concepts form the foundation for
understanding how NumPy achieves its performance and will support everything you learn in the rest of the course.

______________________________________________________________________

# Next Lesson

**File:**

[02-creating-numpy-arrays.md](02-creating-numpy-arrays.md)
