# NumPy Part 3: NumPy Memory Model - Views, Copies & Memory Sharing

**Python Version Introduced:** Python 3.x

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will be able to:

- Understand how NumPy stores array data in memory.
- Explain the difference between a View and a Copy.
- Predict whether common operations share memory.
- Use `.base`, `np.shares_memory()`, and `np.may_share_memory()`.
- Understand memory ownership (`OWNDATA`).
- Explain contiguous and non-contiguous arrays.
- Avoid common bugs caused by shared memory.
- Write more memory-efficient NumPy code.

______________________________________________________________________

# Recap

In the previous lesson, you learned how to create arrays using:

- `array()`
- `zeros()`
- `ones()`
- `full()`
- `empty()`
- `eye()`
- `arange()`
- `linspace()`

You also saw that some functions may create a copy while others try to reuse existing memory.

This lesson explains **why**.

______________________________________________________________________

# Why Should You Care?

Consider this code.

```python
import numpy as np

arr = np.arange(6)

view = arr

view[0] = 999

print(arr)
```

Output

```
[999   1   2   3   4   5]
```

Many beginners expect only `view` to change.

Instead, both changed.

Why?

Because **there is only one array in memory**.

Understanding this behaviour prevents some of the most common NumPy bugs.

______________________________________________________________________

# ndarray Has Two Parts

Every NumPy array consists of two logical components.

```
ndarray Object

+-------------------------+
| Shape                   |
| Dimensions              |
| Strides                 |
| dtype                   |
| Flags                   |
| Pointer                 |
+-----------+-------------+
            |
            |
            ▼

+---------------------------------------+
| 10 | 20 | 30 | 40 | 50 | 60 | ...
+---------------------------------------+

          Data Buffer
```

The **ndarray object** stores metadata.

The **data buffer** stores the actual values.

Multiple arrays can point to the same data buffer.

This is the foundation of Views.

______________________________________________________________________

# Assignment vs Copy

These two lines look similar.

They are completely different.

______________________________________________________________________

## Assignment

```python
arr1 = np.array([1, 2, 3])

arr2 = arr1
```

Memory

```
arr1
   \
    \
     ------> Data Buffer

    /
   /
arr2
```

Only one array exists.

Changing one changes the other.

```python
arr2[0] = 100

print(arr1)
```

Output

```
[100   2   3]
```

______________________________________________________________________

## Copy

```python
arr1 = np.array([1, 2, 3])

arr2 = arr1.copy()
```

Memory

```
arr1 ------> Buffer A

arr2 ------> Buffer B
```

Independent arrays.

```python
arr2[0] = 100

print(arr1)
```

Output

```
[1 2 3]
```

______________________________________________________________________

# What Is a View?

A **View** is another ndarray object that points to the same data buffer.

```
Original

+----------------+
| ndarray Object |
+----------------+
        |
        ▼

+------------------------+
|1|2|3|4|5|6|
+------------------------+

        ▲
        |
+----------------+
| View Object    |
+----------------+
```

Only one copy of the data exists.

______________________________________________________________________

# Creating a View

```python
arr = np.arange(6)

view = arr.view()
```

Modify the view.

```python
view[0] = 999

print(arr)
```

Output

```
[999   1   2   3   4   5]
```

Both arrays share memory.

______________________________________________________________________

# What Is a Copy?

A copy duplicates the data buffer.

```
Original

1 2 3 4 5

Copy

1 2 3 4 5
```

Changing one array does not affect the other.

```python
copy = arr.copy()

copy[0] = 500

print(arr)
print(copy)
```

Output

```
[999   1   2   3   4   5]

[500   1   2   3   4   5]
```

______________________________________________________________________

# How to Check Whether Memory Is Shared

## Using `.base`

```python
arr = np.arange(5)

view = arr.view()
```

```python
print(view.base)
```

Output

```
[0 1 2 3 4]
```

The `base` attribute points to the original array that owns the memory.

Now create a copy.

```python
copy = arr.copy()

print(copy.base)
```

Output

```
None
```

A copied array owns its own memory.

______________________________________________________________________

# Using `np.shares_memory()`

This is the most reliable way to check memory sharing.

```python
arr = np.arange(5)

view = arr.view()

print(np.shares_memory(arr, view))
```

Output

```
True
```

Now check a copy.

```python
copy = arr.copy()

print(np.shares_memory(arr, copy))
```

Output

```
False
```

______________________________________________________________________

# Using `np.may_share_memory()`

```python
np.may_share_memory(a, b)
```

Unlike `shares_memory()`, this function performs a faster, conservative check.

It may return:

```
True
```

even when arrays don't actually share memory.

### When should you use it?

Mostly for optimisation in advanced code.

For everyday development, prefer:

```python
np.shares_memory()
```

______________________________________________________________________

# Memory Ownership

Every array has flags describing its memory.

```python
arr = np.arange(5)

print(arr.flags)
```

Example output

```
C_CONTIGUOUS : True
F_CONTIGUOUS : False
OWNDATA      : True
WRITEABLE    : True
```

The most important flag for now is:

```
OWNDATA
```

______________________________________________________________________

## What Does `OWNDATA` Mean?

If:

```python
arr.flags["OWNDATA"]
```

returns

```
True
```

the array owns its data buffer.

Example.

```python
arr = np.arange(5)

print(arr.flags["OWNDATA"])
```

Output

```
True
```

Now create a view.

```python
view = arr.view()

print(view.flags["OWNDATA"])
```

Output

```
False
```

The view borrows memory from another array.

______________________________________________________________________

# Contiguous Arrays

A contiguous array stores values next to each other.

```
Address

1000 -> 1

1008 -> 2

1016 -> 3

1024 -> 4
```

This layout is very CPU-friendly.

Most arrays you create are contiguous.

```python
arr = np.arange(10)

print(arr.flags["C_CONTIGUOUS"])
```

Output

```
True
```

______________________________________________________________________

# Non-Contiguous Arrays

Some operations create arrays that no longer access memory sequentially.

Example.

```python
arr = np.arange(10)

view = arr[::2]
```

Result

```
[0 2 4 6 8]
```

Memory still looks like

```
0 1 2 3 4 5 6 7 8 9
```

The new array skips elements.

It is no longer contiguous.

Check it.

```python
print(view.flags["C_CONTIGUOUS"])
```

Output

```
False
```

______________________________________________________________________

# Why Does This Matter?

Many NumPy operations are faster on contiguous arrays.

Some functions may create copies automatically when given non-contiguous arrays.

We'll encounter this with:

- `reshape()`
- `transpose()`
- `flatten()`
- `ravel()`

______________________________________________________________________

# Which Operations Usually Return Views?

| Operation | View | Copy |
|-----------|:----:|:----:|
| Assignment (`=`) | ✅ | ❌ |
| `view()` | ✅ | ❌ |
| Basic slicing | ✅ | ❌ |
| `reshape()` | Usually | Sometimes |
| `transpose()` | Usually | Sometimes |
| `ravel()` | Usually | Sometimes |

______________________________________________________________________

# Which Operations Usually Return Copies?

| Operation | View | Copy |
|-----------|:----:|:----:|
| `copy()` | ❌ | ✅ |
| Fancy indexing | ❌ | ✅ |
| Boolean indexing | ❌ | ✅ |
| `flatten()` | ❌ | ✅ |
| Most dtype conversions | ❌ | ✅ |

We'll explain each of these in detail in later lessons.

______________________________________________________________________

# Common Bug #1

```python
arr = np.arange(6)

slice_arr = arr[:3]

slice_arr[:] = 0

print(arr)
```

Output

```
[0 0 0 3 4 5]
```

Why?

Because slicing returned a **View**.

______________________________________________________________________

# Common Bug #2

```python
arr = np.arange(6)

copy = arr.copy()

copy[:] = 0

print(arr)
```

Output

```
[0 1 2 3 4 5]
```

Nothing happened to the original.

______________________________________________________________________

# Common Bug #3

```python
arr = np.arange(6)

another = arr

another *= 10

print(arr)
```

Output

```
[ 0 10 20 30 40 50]
```

Remember:

Assignment does **not** create another array.

It creates another reference.

______________________________________________________________________

# Best Practices

- Use `.copy()` when you need an independent array.
- Assume slicing shares memory unless you know otherwise.
- Use `np.shares_memory()` to verify memory sharing.
- Check `OWNDATA` when debugging.
- Avoid unnecessary copies when working with large datasets.
- Be cautious when passing arrays between functions that modify data in place.

______________________________________________________________________

# Production Insight

Imagine processing a 5 GB image dataset.

Creating unnecessary copies could double memory usage to 10 GB, leading to slower performance or memory exhaustion.

On the other hand, accidentally modifying a shared view could corrupt data used elsewhere in your application.

Experienced NumPy users consciously choose between views and copies based on whether they prioritise memory efficiency
or data isolation.

Understanding this trade-off is essential when working with large-scale data processing, scientific computing, and
machine learning.

______________________________________________________________________

```markdown id="k4q8bn"
# Questions

### Question

> What is the difference between assignment (`=`) and `.copy()`?

### Answer

Assignment creates another reference to the same array, while `.copy()` creates a completely new array with its own memory.

---

### Question

> How can you check if two arrays definitely share memory?

### Answer

Use `np.shares_memory(array1, array2)`.

---

### Question

> What does `OWNDATA = False` indicate?

### Answer

The array does not own its data buffer. It is using memory owned by another array, such as a view.

---

### Question

> Why are views generally more memory-efficient than copies?

### Answer

Because they reuse the existing data buffer instead of allocating new memory.
```

______________________________________________________________________

# Practical Lesson

Write a program that:

1. Creates an array using `np.arange(10)`.
1. Creates:
   - An assignment (`=`).
   - A view using `.view()`.
   - A copy using `.copy()`.
1. Modify each array and observe how the original changes.
1. Check:
   - `.base`
   - `OWNDATA`
   - `np.shares_memory()`
1. Create a slice (`arr[::2]`) and determine whether it is contiguous by checking `C_CONTIGUOUS`.

______________________________________________________________________

```markdown id="z8m1yf"
# Knowledge Check

## Question 1

What are the two main components of an `ndarray`?

### Answer

The ndarray object (metadata such as shape, dtype, strides, and flags) and the data buffer that stores the actual values.

---

## Question 2

Does `arr2 = arr1` create a new array?

### Answer

No. It creates another reference to the same array.

---

## Question 3

Which function guarantees a completely independent array?

### Answer

`arr.copy()`.

---

## Question 4

How do you check whether an array owns its memory?

### Answer

Check `arr.flags["OWNDATA"]`.

---

## Question 5

What is the difference between `np.shares_memory()` and `np.may_share_memory()`?

### Answer

`np.shares_memory()` determines whether arrays actually share memory, while `np.may_share_memory()` performs a faster, conservative check that may report possible sharing even when none exists.

---

## Question 6

Why can views improve performance?

### Answer

Views reuse the existing data buffer, avoiding additional memory allocation and data copying.
```

______________________________________________________________________

# Assignment

1. Create an array and produce:
   - An assignment.
   - A view.
   - A copy.
1. Modify each one and record how the original array changes.
1. Use `.base`, `OWNDATA`, `np.shares_memory()`, and `np.may_share_memory()` to investigate the relationships between the arrays.
1. Create several slices (`arr[1:5]`, `arr[::2]`, `arr[::-1]`) and determine:
   - Whether they share memory.
   - Whether they are contiguous.
1. Write a short explanation of when you would choose a view instead of a copy in a real-world application.

______________________________________________________________________

# Summary

In this lesson, you learned how NumPy stores data internally and why understanding its memory model is essential. You
explored the difference between assignment, views, and copies, learned how to inspect memory ownership using `.base` and
`OWNDATA`, and used `np.shares_memory()` to determine whether arrays share the same underlying data. These concepts form
the foundation for understanding indexing, slicing, reshaping, and many performance characteristics of NumPy.

______________________________________________________________________

# Next Lesson

**File:**

[04-accessing-and-selecting-data.md](04-accessing-and-selecting-data.md)
