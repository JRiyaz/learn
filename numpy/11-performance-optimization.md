# NumPy Part 11: Performance Optimization

**Python Version Introduced:** Python 3.x

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will be able to:

- Understand where NumPy gets its performance from.
- Identify common performance bottlenecks in numerical Python code.
- Measure execution time correctly.
- Reduce unnecessary memory allocations.
- Write cache-friendly NumPy code.
- Choose appropriate data types for performance and memory efficiency.
- Recognize when vectorization is beneficial and when it is not.
- Apply production-ready optimization techniques without sacrificing readability.

______________________________________________________________________

# Recap

In the previous lesson, you learned about:

- Modern random number generation
- Reproducibility
- Probability distributions
- Random sampling
- Shuffling and permutations

Throughout this NumPy course, you've learned how to manipulate arrays efficiently.

Now we'll answer an engineering question:

> **How do we make NumPy code as fast and memory-efficient as possible?**

______________________________________________________________________

# Performance Before Optimization

A common mistake is optimizing code before measuring it.

Never assume a piece of code is slow.

Instead:

```
Measure

↓

Identify Bottleneck

↓

Optimize

↓

Measure Again
```

This principle applies to every production system.

______________________________________________________________________

# Where Does NumPy Get Its Speed?

NumPy's performance comes from several design decisions.

```
Python Objects

↓

Slow
```

vs

```
Homogeneous Data

↓

Contiguous Memory

↓

Compiled Loops

↓

Fast
```

Key reasons:

- Contiguous memory layout
- Homogeneous data types
- Optimized C implementations
- CPU cache efficiency
- Vectorized operations
- Optimized BLAS/LAPACK routines (for many linear algebra operations)

______________________________________________________________________

# Measuring Performance

Never rely on intuition.

Instead, measure.

______________________________________________________________________

## Using `timeit`

```python
import numpy as np
import timeit

arr = np.arange(1_000_000)

execution_time = timeit.timeit(
    lambda: arr * 2,
    number=100
)

print(execution_time)
```

Why `timeit`?

- Repeats execution
- Reduces measurement noise
- More reliable than manual timing for small benchmarks

______________________________________________________________________

## Why Not `time.time()`?

```python
import time

start = time.time()

arr * 2

end = time.time()
```

This is acceptable for coarse measurements but less reliable for benchmarking very fast operations.

Use:

- `timeit` for micro-benchmarks
- Profilers for large applications

______________________________________________________________________

# Vectorization vs Python Loops

Suppose

```python
numbers = np.arange(1_000_000)
```

Python loop

```python
result = []

for value in numbers:
    result.append(value * 2)
```

Vectorized

```python
result = numbers * 2
```

The second version is dramatically faster because the loop executes in optimized compiled code rather than the Python
interpreter.

______________________________________________________________________

# Avoid Python Loops

Bad

```python
total = 0

for value in arr:
    total += value
```

Good

```python
total = arr.sum()
```

NumPy operations are almost always preferable for numerical workloads.

______________________________________________________________________

# Memory Allocation

Every new array consumes memory.

Consider

```python
result = arr * 2
```

A new array is created.

Sometimes that's unavoidable.

Sometimes it isn't.

______________________________________________________________________

# In-Place Operations

Instead of

```python
arr = arr * 2
```

use

```python
arr *= 2
```

Benefits:

- No additional output array
- Less memory usage
- Often faster

______________________________________________________________________

## Example

```python
arr = np.arange(5)

arr *= 10

print(arr)
```

Output

```
[ 0 10 20 30 40]
```

______________________________________________________________________

# Temporary Arrays

Consider

```python
result = (arr + 5) * 10
```

Conceptually,

NumPy performs

```
arr

↓

arr + 5

↓

Temporary Array

↓

Multiply

↓

Result
```

The temporary array increases memory usage.

For very large datasets, this matters.

______________________________________________________________________

## Reducing Temporaries

When appropriate, reuse arrays.

Example

```python
arr += 5

arr *= 10
```

Whether this is appropriate depends on whether modifying the original data is acceptable.

______________________________________________________________________

# Choosing the Right Data Type

Not every dataset requires 64-bit integers or floats.

Example

```python
arr64 = np.arange(
    1_000_000,
    dtype=np.int64
)

arr32 = np.arange(
    1_000_000,
    dtype=np.int32
)
```

Memory

```
int64

↓

8 bytes

int32

↓

4 bytes
```

Choosing an appropriate dtype can halve memory usage.

______________________________________________________________________

## Floating Point Types

| Type | Bytes |
|------|------:|
| float16 | 2 |
| float32 | 4 |
| float64 | 8 |

Choose based on:

- Required precision
- Memory constraints
- Compatibility with downstream libraries

______________________________________________________________________

# Cache-Friendly Access

CPUs load nearby memory together.

Example.

```
1 2 3 4 5 6 7 8
```

Reading sequentially is efficient.

Jumping randomly across memory causes more cache misses.

NumPy's contiguous arrays take advantage of this.

______________________________________________________________________

# Contiguous vs Non-Contiguous Arrays

```python
arr = np.arange(12).reshape(3,4)

print(arr.flags)
```

Example

```
C_CONTIGUOUS : True
```

Now transpose.

```python
t = arr.T

print(t.flags)
```

Often

```
C_CONTIGUOUS : False
```

Some operations on non-contiguous arrays can be slower because memory is accessed with larger strides.

______________________________________________________________________

# Copy Only When Necessary

Suppose

```python
view = arr[:5]
```

No copy.

Now

```python
copy = arr[:5].copy()
```

Memory doubles for that slice.

Ask yourself:

> Do I really need an independent copy?

If not, prefer views.

______________________________________________________________________

# Broadcasting Saves Memory

Consider

```python
matrix = np.ones((1000,1000))

vector = np.arange(1000)

result = matrix + vector
```

Broadcasting conceptually repeats the vector.

However,

NumPy does **not** create

```
1000

copies
```

of the vector.

This saves both memory and execution time.

______________________________________________________________________

# Avoid Repeated Computation

Bad

```python
for _ in range(100):

    np.mean(arr)
```

If the data doesn't change,

compute it once.

```python
mean = np.mean(arr)

for _ in range(100):
    print(mean)
```

______________________________________________________________________

# Preallocation

Growing arrays repeatedly is expensive.

Bad

```python
result = np.array([])

for i in range(1000):
    result = np.append(result, i)
```

Each `append()` creates a new array.

Better

```python
result = np.empty(1000)

for i in range(1000):
    result[i] = i
```

Even better,

if possible, eliminate the loop entirely using vectorized operations.

______________________________________________________________________

# Profiling Before Optimizing

Optimization without profiling is risky.

Typical workflow

```
Application

↓

Profiler

↓

Slow Function

↓

Optimize

↓

Measure Again
```

Useful tools include:

- `timeit`
- `cProfile`
- `line_profiler` (third-party)

Always identify the actual bottleneck before making changes.

______________________________________________________________________

# Performance Summary

Technique | Benefit ----------|--------- Vectorization | Eliminates Python loops Views | Avoid unnecessary copies
Broadcasting | Avoids duplicated data In-place operations | Reduces memory allocations Appropriate dtype | Lowers memory
usage Contiguous memory | Better cache performance Preallocation | Avoids repeated reallocations Profiling | Optimizes
the correct code

______________________________________________________________________

# Common Mistakes

## Mistake 1

Optimizing before measuring.

Always benchmark first.

______________________________________________________________________

## Mistake 2

Using Python loops for numerical operations.

Prefer vectorized NumPy functions.

______________________________________________________________________

## Mistake 3

Calling `np.append()` repeatedly in a loop.

It reallocates memory every time.

______________________________________________________________________

## Mistake 4

Using `float64` or `int64` without considering whether a smaller dtype is sufficient.

______________________________________________________________________

## Mistake 5

Creating unnecessary copies with `.copy()`.

Only create copies when independent data ownership is required.

______________________________________________________________________

# Best Practices

- Measure performance before optimizing.
- Use vectorized operations whenever practical.
- Reuse arrays when modifying data is acceptable.
- Choose the smallest appropriate dtype.
- Prefer views over copies.
- Take advantage of broadcasting.
- Avoid repeated memory allocations.
- Keep code readable; optimize only where it matters.

______________________________________________________________________

# Production Insight

Performance optimization is about balancing speed, memory, and maintainability.

Large-scale data processing systems often spend more time moving data than performing arithmetic. Efficient NumPy code
minimizes unnecessary memory allocations, maximizes cache locality, and expresses computations using vectorized
operations.

Examples include:

- Processing terabytes of sensor data.
- Feature engineering for machine learning.
- Financial analytics.
- Scientific simulations.
- Image and video processing.

The fastest code is not always the most valuable. Production systems prioritize correctness, maintainability, and
measurable performance improvements.

______________________________________________________________________

```markdown id="y5p8nl"
# Questions

### Question

> Why should optimization begin with measurement?

### Answer

Because assumptions about performance are often incorrect. Measuring identifies the actual bottlenecks before time is spent optimizing.

---

### Question

> Why are vectorized operations faster than Python loops?

### Answer

Because they execute optimized compiled code over contiguous memory instead of repeatedly invoking the Python interpreter.

---

### Question

> Why is `arr *= 2` often preferable to `arr = arr * 2`?

### Answer

It performs the operation in place, avoiding an additional array allocation when modifying the original array is acceptable.

---

### Question

> Why should `.copy()` be used carefully?

### Answer

Because it duplicates memory. Views are usually more memory-efficient when independent ownership is unnecessary.
```

______________________________________________________________________

# Practical Lesson

Generate a large dataset.

```python
import numpy as np

arr = np.arange(10_000_000)
```

Perform the following tasks:

1. Measure the execution time of:
   - A Python loop doubling every value.
   - A vectorized multiplication (`arr * 2`).
1. Compare:
   - `arr = arr * 2`
   - `arr *= 2`
1. Create:
   - A view using slicing.
   - A copy using `.copy()`.
Verify memory sharing using `np.shares_memory()`.
1. Compare the memory usage of:
   - `int64`
   - `int32`
   - `float32`
1. Demonstrate broadcasting by adding a vector to a large matrix and explain why the vector is not duplicated in memory.

______________________________________________________________________

```markdown id="c4w7tm"
# Knowledge Check

## Question 1

Why is `timeit` generally preferred over `time.time()` for benchmarking?

### Answer

Because it performs repeated measurements and reduces timing noise, making results more reliable for small operations.

---

## Question 2

What is the main performance advantage of vectorization?

### Answer

It eliminates Python-level loops by executing optimized compiled operations on entire arrays.

---

## Question 3

Why can choosing `int32` instead of `int64` improve performance?

### Answer

It reduces memory usage, allowing more data to fit into CPU caches and lowering memory bandwidth requirements when the reduced range is sufficient.

---

## Question 4

What is a temporary array?

### Answer

An intermediate array created during an expression, such as `(arr + 5) * 10`, which increases memory usage.

---

## Question 5

Why is repeatedly calling `np.append()` inside a loop inefficient?

### Answer

Because NumPy arrays have fixed sizes, so each append creates a new array and copies the existing data.

---

## Question 6

What is the advantage of broadcasting?

### Answer

It performs operations on compatible shapes without physically duplicating smaller arrays.

---

## Question 7

When should you use `.copy()`?

### Answer

Only when you need an independent array that can be modified without affecting the original.

---

## Question 8

What are the three major goals of performance optimization?

### Answer

Improve execution speed, reduce memory usage, and maintain code correctness and readability.
```

______________________________________________________________________

# Assignment

Build a performance comparison report.

1. Create arrays containing **10 million** elements.
1. Benchmark:
   - Python loop vs vectorized multiplication.
   - `arr = arr * 2` vs `arr *= 2`.
1. Compare memory consumption of:
   - `int32`
   - `int64`
   - `float32`
   - `float64`
1. Demonstrate:
   - View vs copy.
   - Contiguous vs transposed arrays.
   - Broadcasting without data duplication.
1. Produce a table summarizing:
   - Execution time.
   - Memory usage.
   - Whether temporary arrays were created.
   - Whether the operation returned a view or a copy.
1. Conclude with recommendations for writing high-performance NumPy code suitable for production environments.

______________________________________________________________________

# Summary

In this lesson, you learned the engineering principles behind writing efficient NumPy code. You explored how to measure
performance using `timeit`, why vectorization outperforms Python loops, how in-place operations and appropriate data
types reduce memory usage, and how views, broadcasting, and contiguous memory improve efficiency. Most importantly, you
learned that optimization should always be guided by measurement and profiling rather than assumptions.

______________________________________________________________________

# Next Lesson

**File:**

[12-numpy-project-and-best-practices.md](12-numpy-project-and-best-practices.md)
