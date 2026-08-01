# NumPy Part 6: Vectorization & Broadcasting

**Python Version Introduced:** Python 3.x

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will be able to:

- Understand why vectorization is one of NumPy's greatest strengths.
- Explain why Python loops are slower than NumPy operations.
- Use Universal Functions (ufuncs).
- Understand broadcasting and its rules.
- Predict when broadcasting will succeed or fail.
- Write cleaner and significantly faster numerical code.
- Avoid common broadcasting mistakes.
- Apply vectorization techniques used in production systems.

______________________________________________________________________

# Recap

In the previous lesson, you learned how to reshape arrays using operations such as:

- `reshape()`
- `resize()`
- `flatten()`
- `ravel()`
- `transpose()`
- `expand_dims()`
- `squeeze()`

Those operations reorganize data.

This lesson focuses on **processing** that data efficiently.

______________________________________________________________________

# Why Does Vectorization Matter?

Imagine you have one million salaries.

Your task is to increase every salary by 10%.

A beginner might write:

```python
result = []

for salary in salaries:
    result.append(salary * 1.10)
```

This works.

But it is slow.

NumPy provides a much better approach.

```python
result = salaries * 1.10
```

Same result.

Much faster.

Much cleaner.

______________________________________________________________________

# Why Are Python Loops Slow?

Consider this code.

```python
numbers = [1, 2, 3, 4, 5]

result = []

for number in numbers:
    result.append(number * 2)
```

Every iteration involves:

- Loop control
- Python object lookup
- Type checking
- Integer multiplication
- List append

The CPU repeatedly switches between Python objects.

______________________________________________________________________

NumPy performs operations differently.

```python
arr = np.array([1,2,3,4,5])

result = arr * 2
```

Internally, NumPy performs the multiplication in optimized compiled code over contiguous memory.

The Python interpreter is no longer involved for every element.

______________________________________________________________________

# What is Vectorization?

Vectorization means performing one operation on an entire array instead of processing one element at a time.

Instead of

```
1

↓

2

↓

3

↓

4
```

NumPy thinks

```
Entire Array

↓

One Operation

↓

Entire Result
```

______________________________________________________________________

# Example

Without vectorization

```python
numbers = [10,20,30]

result = []

for value in numbers:
    result.append(value + 5)
```

With NumPy

```python
arr = np.array([10,20,30])

result = arr + 5
```

Output

```
[15 25 35]
```

______________________________________________________________________

# Benefits of Vectorization

- Less code
- Faster execution
- Better readability
- Better cache utilization
- Fewer bugs

This is why experienced NumPy users avoid explicit Python loops whenever possible.

______________________________________________________________________

# Element-wise Operations

Consider two arrays.

```python
a = np.array([1,2,3])

b = np.array([10,20,30])
```

Addition

```python
print(a + b)
```

Output

```
[11 22 33]
```

Subtraction

```python
print(b - a)
```

Output

```
[ 9 18 27]
```

Multiplication

```python
print(a * b)
```

Output

```
[10 40 90]
```

Division

```python
print(b / a)
```

Output

```
[10. 10. 10.]
```

Operations occur element by element.

______________________________________________________________________

# Vectorized Comparisons

```python
arr = np.array([10,20,30,40])

print(arr > 20)
```

Output

```
[False False True True]
```

The result itself is a NumPy array.

This makes filtering easy.

```python
print(arr[arr > 20])
```

Output

```
[30 40]
```

______________________________________________________________________

# Universal Functions (ufuncs)

Many NumPy mathematical functions are called **Universal Functions**.

They operate element by element.

Examples include:

- `np.sqrt()`
- `np.exp()`
- `np.log()`
- `np.sin()`
- `np.cos()`
- `np.abs()`

______________________________________________________________________

# Example

```python
arr = np.array([1,4,9,16])

print(np.sqrt(arr))
```

Output

```
[1. 2. 3. 4.]
```

______________________________________________________________________

Another example.

```python
angles = np.array([0, np.pi/2, np.pi])

print(np.sin(angles))
```

Output

```
[0. 1. 0.]
```

______________________________________________________________________

# What Happens Without Broadcasting?

Consider

```python
a = np.array([1,2,3])

b = np.array([10,20])
```

Trying

```python
a + b
```

Produces

```
ValueError
```

The shapes are incompatible.

______________________________________________________________________

# What is Broadcasting?

Broadcasting is NumPy's ability to perform arithmetic on arrays of different shapes.

Instead of physically copying data,

NumPy behaves **as if** the smaller array were expanded.

Example.

```python
arr = np.array([10,20,30])

print(arr + 5)
```

Output

```
[15 25 35]
```

The number

```
5
```

is conceptually treated as

```
[5 5 5]
```

No actual copy is made.

______________________________________________________________________

# Broadcasting Example

```python
matrix = np.array([
    [1,2,3],
    [4,5,6]
])

vector = np.array([10,20,30])

print(matrix + vector)
```

Output

```
[[11 22 33]
 [14 25 36]]
```

The vector is reused for every row.

______________________________________________________________________

Memory concept.

```
Matrix

1 2 3

4 5 6


Vector

10 20 30


Broadcast


10 20 30

10 20 30
```

The repeated rows are conceptual.

NumPy does not allocate another array.

______________________________________________________________________

# Broadcasting Rules

NumPy compares shapes from the **rightmost dimension**.

Two dimensions are compatible if:

- They are equal.

OR

- One of them is 1.

______________________________________________________________________

Example.

```
(3,4)

(4)
```

Internally becomes

```
(3,4)

(1,4)
```

Since

```
1

↓

3
```

can be broadcast,

the operation succeeds.

______________________________________________________________________

Another example.

```
(5,1)

(5,7)
```

The second dimension

```
1

↓

7
```

can be expanded.

Broadcasting succeeds.

______________________________________________________________________

# Broadcasting Failure

```python
a = np.zeros((2,3))

b = np.zeros((4,))
```

Shapes

```
(2,3)

(4)
```

Compare from the end.

```
3

vs

4
```

Neither is 1.

Broadcasting fails.

Result

```
ValueError
```

______________________________________________________________________

# Using `newaxis`

Sometimes arrays need an extra dimension.

Example.

```python
arr = np.array([1,2,3])
```

Shape

```
(3,)
```

Convert to column vector.

```python
column = arr[:, np.newaxis]

print(column.shape)
```

Output

```
(3,1)
```

Equivalent to

```python
np.expand_dims(arr, axis=1)
```

______________________________________________________________________

# Broadcasting with `newaxis`

```python
a = np.array([1,2,3])

b = np.array([10,20,30])
```

```python
result = a[:, np.newaxis] + b

print(result)
```

Output

```
[[11 21 31]
 [12 22 32]
 [13 23 33]]
```

Shapes

```
(3,1)

+

(3,)
```

become

```
(3,1)

+

(1,3)

↓

(3,3)
```

______________________________________________________________________

# Performance Notes

Operation | Complexity | Memory ----------|------------|-------- Vectorized arithmetic | O(n) | O(n) for the result
Broadcasting | O(n) | No duplicated broadcasted data Python loop | O(n) | O(n)

Although both approaches are O(n), vectorized NumPy operations have a much smaller constant factor because they execute
in optimized compiled code.

Broadcasting also avoids allocating repeated copies of smaller arrays.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using Python loops unnecessarily.

Bad

```python
for i in range(len(arr)):
    arr[i] += 1
```

Good

```python
arr += 1
```

______________________________________________________________________

## Mistake 2

Misunderstanding broadcasting.

```
(3,4)

+

(5,)
```

This cannot be broadcast.

______________________________________________________________________

## Mistake 3

Assuming broadcasting copies memory.

It usually doesn't.

Broadcasting is largely a metadata operation.

______________________________________________________________________

## Mistake 4

Forgetting array shapes.

Always check.

```python
print(arr.shape)
```

before debugging broadcasting errors.

______________________________________________________________________

# Best Practices

- Prefer vectorized operations over Python loops.
- Learn broadcasting rules thoroughly.
- Use `np.newaxis` or `expand_dims()` when shapes don't match.
- Check shapes before performing operations.
- Write code that expresses operations on entire arrays rather than individual elements.

______________________________________________________________________

# Production Insight

Vectorization and broadcasting are fundamental to nearly every scientific and machine learning library built on NumPy.

Examples include:

- Normalizing datasets by subtracting column means.
- Applying image transformations to every pixel.
- Scaling financial time-series data.
- Computing neural network activations.
- Processing millions of sensor readings simultaneously.

Efficient use of broadcasting eliminates many explicit loops, resulting in code that is shorter, easier to read, and
significantly faster.

______________________________________________________________________

```markdown id="k2v9mt"
# Questions

### Question

> What is vectorization?

### Answer

Vectorization is performing an operation on an entire array at once instead of processing each element individually with Python loops.

---

### Question

> What is a Universal Function (ufunc)?

### Answer

A NumPy function that performs element-wise operations efficiently on arrays, such as `np.sqrt()`, `np.sin()`, or `np.log()`.

---

### Question

> When are two dimensions compatible for broadcasting?

### Answer

When they are equal or when one of them is 1.

---

### Question

> Does broadcasting usually allocate repeated copies of the smaller array?

### Answer

No. NumPy conceptually expands the array without physically duplicating its data.
```

______________________________________________________________________

# Practical Lesson

Create the following arrays:

```python
a = np.arange(1, 7).reshape(2, 3)

b = np.array([10, 20, 30])

c = np.array([100, 200])
```

Perform these tasks:

1. Add `b` to every row of `a`.
1. Multiply every element of `a` by 5.
1. Compute the square root of every element in `a`.
1. Convert `c` into a column vector using both `np.newaxis` and `expand_dims()`.
1. Add the column vector to `a` using broadcasting.
1. Try to add an incompatible array and explain why NumPy raises an error.
1. Print the shapes of all arrays before each operation to understand broadcasting.

______________________________________________________________________

```markdown id="w7d3pb"
# Knowledge Check

## Question 1

Why is vectorized NumPy code generally faster than Python loops?

### Answer

Because the operations execute in optimized compiled code on contiguous memory instead of invoking the Python interpreter for each element.

---

## Question 2

What does broadcasting allow NumPy to do?

### Answer

Perform element-wise operations on arrays with compatible but different shapes without explicitly copying data.

---

## Question 3

Name three Universal Functions.

### Answer

Examples include `np.sqrt()`, `np.sin()`, `np.log()`, `np.exp()`, and `np.abs()`.

---

## Question 4

Under what conditions are two dimensions broadcast-compatible?

### Answer

They must either be equal or one of them must be 1.

---

## Question 5

What is the purpose of `np.newaxis`?

### Answer

It inserts a new dimension into an array, making it easier to align shapes for broadcasting.

---

## Question 6

Why is broadcasting memory-efficient?

### Answer

Because NumPy conceptually expands arrays using metadata instead of allocating duplicated copies of the data.

---

## Question 7

What should you inspect first when debugging a broadcasting error?

### Answer

The shapes of the arrays using their `shape` attribute.
```

______________________________________________________________________

# Assignment

1. Create a `(4, 5)` matrix using `np.arange()`.
1. Perform the following operations using **vectorization only** (no Python loops):
   - Add 10 to every element.
   - Multiply every element by 3.
   - Compute the square root of every element.
   - Compute the sine of every element.
1. Create row and column vectors and use broadcasting to:
   - Add values to every row.
   - Add values to every column.
1. Intentionally create incompatible shapes and identify which broadcasting rule is violated.
1. For each operation, record:
   - Input shapes
   - Output shape
   - Whether broadcasting occurred
   - Whether additional array duplication was required

______________________________________________________________________

# Summary

In this lesson, you learned why vectorization is central to NumPy's performance and how broadcasting allows arrays with
compatible shapes to participate in efficient element-wise operations. You explored Universal Functions (ufuncs),
broadcasting rules, the use of `np.newaxis`, and the performance advantages of avoiding Python loops. These concepts are
essential for writing fast, readable, and scalable numerical code.

______________________________________________________________________

# Next Lesson

**File:**

[07-mathematical-and-statistical-operations.md](07-mathematical-and-statistical-operations.md)
