# NumPy Part 9: Linear Algebra Essentials

**Python Version Introduced:** Python 3.x

---

# Learning Objectives

By the end of this lesson, you will be able to:

- Understand why linear algebra is fundamental to data science, machine learning, graphics, and scientific computing.
- Differentiate between element-wise multiplication and matrix multiplication.
- Perform matrix multiplication using `@` and `np.matmul()`.
- Compute dot products using `np.dot()`.
- Transpose matrices correctly.
- Calculate matrix inverses using `np.linalg.inv()`.
- Compute determinants using `np.linalg.det()`.
- Solve systems of linear equations using `np.linalg.solve()`.
- Understand when **not** to compute matrix inverses.
- Apply linear algebra operations in production systems.

---

# Recap

In the previous lesson, you learned how to:

- Search arrays
- Sort arrays
- Filter arrays
- Find unique values
- Use Boolean conditions efficiently

Those operations help prepare data.

This lesson focuses on **transforming data mathematically**, which is the foundation of machine learning, optimization, simulations, computer graphics, robotics, and scientific computing.

---

# Why Linear Algebra?

Suppose you are building:

- A recommendation engine
- A neural network
- A 3D game engine
- A robotics controller
- A financial forecasting model

All of them rely heavily on linear algebra.

Some examples:

```
Images

↓

Matrices

↓

Filters

↓

New Images
```

```
Features

↓

Weight Matrix

↓

Predictions
```

```
Coordinates

↓

Transformation Matrix

↓

Rotation / Scaling
```

Without linear algebra, modern machine learning would not exist.

---

# Scalars, Vectors, and Matrices

Before using NumPy's linear algebra functions, let's review the terminology.

### Scalar

A single value.

```python
x = 5
```

```
5
```

---

### Vector

A one-dimensional collection of numbers.

```python
v = np.array([2, 4, 6])
```

```
[2 4 6]
```

Shape

```
(3,)
```

---

### Matrix

A two-dimensional collection of numbers.

```python
m = np.array([
    [1,2],
    [3,4]
])
```

```
1 2

3 4
```

Shape

```
(2,2)
```

---

# Element-wise Multiplication

Suppose

```python
A = np.array([
    [1,2],
    [3,4]
])

B = np.array([
    [5,6],
    [7,8]
])
```

Using

```python
A * B
```

Output

```
[[ 5 12]
 [21 32]]
```

Each element is multiplied independently.

This is **not** matrix multiplication.

---

# Matrix Multiplication

Linear algebra defines a different operation.

Instead of multiplying matching elements,

each output value is computed using

```
Row

×

Column
```

Diagram

```
A

1 2

3 4


B

5 6

7 8


↓

Result

19 22

43 50
```

---

# Matrix Multiplication with `@`

## What does it do?

Performs matrix multiplication.

---

## Syntax

```python
A @ B
```

---

## Example

```python
A = np.array([
    [1,2],
    [3,4]
])

B = np.array([
    [5,6],
    [7,8]
])

print(A @ B)
```

Output

```
[[19 22]
 [43 50]]
```

---

# `np.matmul()`

The same operation can be written as

```python
np.matmul(A, B)
```

Output

```
[[19 22]
 [43 50]]
```

The `@` operator internally calls matrix multiplication and is generally preferred for readability.

---

# Matrix Multiplication Rules

If

```
(m × n)

×

(p × q)
```

then

```
n

must equal

p
```

The result has shape

```
(m × q)
```

---

Example

```
(2 × 3)

×

(3 × 4)

↓

(2 × 4)
```

Valid.

---

Example

```
(2 × 3)

×

(2 × 4)
```

Invalid.

The inner dimensions do not match.

NumPy raises

```
ValueError
```

---

# `dot()`

## What does it do?

Computes the dot product.

Its behavior depends on the dimensions of the inputs.

---

## Syntax

```python
np.dot(a, b)
```

---

### Vector Dot Product

```python
a = np.array([1,2,3])

b = np.array([4,5,6])

print(np.dot(a,b))
```

Output

```
32
```

Calculation

```
1×4

+

2×5

+

3×6

=

32
```

---

### Matrix Dot Product

```python
print(np.dot(A,B))
```

Produces the same result as matrix multiplication for two 2D arrays.

---

# `@` vs `dot()`

| Operation | Recommended Usage |
|------------|-------------------|
| `@` | Matrix multiplication |
| `np.matmul()` | Matrix multiplication |
| `np.dot()` | Dot products and compatible matrix multiplication |

For modern code, prefer `@` for matrix multiplication because it clearly expresses mathematical intent.

---

# Matrix Transpose

Transpose swaps rows and columns.

```python
A = np.array([
    [1,2,3],
    [4,5,6]
])

print(A.T)
```

Output

```
[[1 4]
 [2 5]
 [3 6]]
```

Shape changes

```
(2,3)

↓

(3,2)
```

---

# Identity Matrix

An identity matrix behaves like the number `1` for matrix multiplication.

```
1 0 0

0 1 0

0 0 1
```

Create one.

```python
I = np.eye(3)

print(I)
```

Output

```
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
```

Property

```
A @ I = A
```

---

# Matrix Inverse

## What does it do?

Computes the inverse of a square matrix.

---

## Syntax

```python
np.linalg.inv(matrix)
```

---

Example

```python
A = np.array([
    [1,2],
    [3,4]
])

print(np.linalg.inv(A))
```

Output

```
[[-2.   1. ]
 [ 1.5 -0.5]]
```

Verification

```python
print(A @ np.linalg.inv(A))
```

Output (approximately)

```
[[1. 0.]
 [0. 1.]]
```

Small floating-point errors are expected.

---

# When Can a Matrix Be Inverted?

Only square matrices with a non-zero determinant are invertible.

If a matrix is singular,

```python
np.linalg.inv()
```

raises

```
LinAlgError
```

---

# Determinant

## What does it do?

Measures certain mathematical properties of a square matrix, including whether it is invertible.

---

## Syntax

```python
np.linalg.det(matrix)
```

---

Example

```python
A = np.array([
    [1,2],
    [3,4]
])

print(np.linalg.det(A))
```

Output

```
-2.0
```

Since the determinant is not zero,

the matrix is invertible.

---

# Solving Linear Equations

Suppose we want to solve

```
2x + y = 5

x + 3y = 6
```

Represent it as

```
A × x = b
```

```python
A = np.array([
    [2,1],
    [1,3]
])

b = np.array([
    5,
    6
])

solution = np.linalg.solve(A,b)

print(solution)
```

Output

```
[1.8 1.4]
```

---

# Why Not Use the Inverse?

Many beginners write

```python
x = np.linalg.inv(A) @ b
```

Although mathematically correct,

this is **not recommended**.

Instead use

```python
np.linalg.solve(A,b)
```

Reasons:

- Faster
- More numerically stable
- Uses optimized algorithms
- Preferred in scientific computing

This is an important production practice.

---

# Norm

A norm measures the "size" or "length" of a vector.

---

## Syntax

```python
np.linalg.norm(vector)
```

---

Example

```python
v = np.array([3,4])

print(np.linalg.norm(v))
```

Output

```
5.0
```

Applications

- Distance calculations
- Machine learning
- Similarity measures
- Optimization

---

# Performance Notes

Operation | Complexity (Typical)
----------|----------------------
Transpose | O(1) (metadata change)
Dot Product | O(n)
Matrix Multiplication | O(n³) for dense square matrices (naïve; optimized libraries may perform better)
Determinant | O(n³)
Inverse | O(n³)
Solve Linear System | O(n³)

The exact performance depends on the underlying BLAS/LAPACK implementation and matrix characteristics.

---

# Common Mistakes

## Mistake 1

Using

```python
A * B
```

when matrix multiplication is intended.

Use

```python
A @ B
```

instead.

---

## Mistake 2

Computing an inverse just to solve equations.

Prefer

```python
np.linalg.solve()
```

---

## Mistake 3

Ignoring matrix shapes.

Always verify

```python
print(A.shape)
print(B.shape)
```

before multiplication.

---

## Mistake 4

Comparing floating-point results with `==`.

Instead, use

```python
np.allclose()
```

when checking results that involve floating-point arithmetic.

---

# Best Practices

- Use `@` for matrix multiplication.
- Use `np.linalg.solve()` instead of explicitly computing inverses for linear systems.
- Verify matrix dimensions before multiplication.
- Expect small floating-point rounding errors.
- Use `np.allclose()` when validating numerical results.
- Keep matrix operations vectorized instead of using nested Python loops.

---

# Production Insight

Linear algebra powers almost every modern machine learning algorithm.

Examples include:

- Linear regression
- Logistic regression
- Principal Component Analysis (PCA)
- Neural networks
- Kalman filters
- Recommendation systems
- Computer vision
- Robotics

In production systems, matrix multiplication and solving linear systems are often delegated to highly optimized numerical libraries. Writing NumPy code that expresses operations in terms of matrices allows these optimizations to be utilized automatically.

---

```markdown id="m2v7kp"
# Questions

### Question

> What is the difference between `A * B` and `A @ B`?

### Answer

`A * B` performs element-wise multiplication, while `A @ B` performs matrix multiplication according to the rules of linear algebra.

---

### Question

> Why is `np.linalg.solve()` preferred over `np.linalg.inv(A) @ b`?

### Answer

Because it is faster, more numerically stable, and avoids explicitly computing the inverse matrix.

---

### Question

> When can a matrix be inverted?

### Answer

Only when it is square and has a non-zero determinant.

---

### Question

> What does `np.linalg.norm()` measure?

### Answer

The length (or magnitude) of a vector.
```

---

# Practical Lesson

Given the following matrices:

```python
A = np.array([
    [2, 1],
    [5, 3]
])

B = np.array([
    [1, 4],
    [2, 6]
])

b = np.array([7, 19])
```

Complete the following tasks:

1. Perform element-wise multiplication.
2. Perform matrix multiplication using both `@` and `np.matmul()`.
3. Compute the transpose of `A`.
4. Calculate the determinant of `A`.
5. Compute the inverse of `A`.
6. Verify that `A @ inverse(A)` is approximately equal to the identity matrix using `np.allclose()`.
7. Solve the linear system `A × x = b`.
8. Compute the Euclidean norm of each row of `A`.

---

```markdown id="q5r9dz"
# Knowledge Check

## Question 1

What is the primary difference between element-wise multiplication and matrix multiplication?

### Answer

Element-wise multiplication multiplies corresponding elements, while matrix multiplication combines rows and columns according to linear algebra rules.

---

## Question 2

Which operator is preferred for matrix multiplication in modern NumPy?

### Answer

The `@` operator.

---

## Question 3

When is a matrix invertible?

### Answer

When it is square and its determinant is non-zero.

---

## Question 4

Which function should you use to solve `A × x = b`?

### Answer

`np.linalg.solve()`.

---

## Question 5

Why should you avoid computing matrix inverses unnecessarily?

### Answer

Because computing an inverse is slower and less numerically stable than solving the system directly.

---

## Question 6

What does `np.linalg.det()` compute?

### Answer

The determinant of a square matrix.

---

## Question 7

Why should `np.allclose()` be used instead of `==` for floating-point results?

### Answer

Because floating-point arithmetic introduces small rounding errors, making exact equality unreliable.

---

## Question 8

What is the typical time complexity of dense matrix multiplication?

### Answer

Approximately `O(n³)` (though optimized numerical libraries may use more advanced algorithms internally).
```

---

# Assignment

1. Create two compatible random matrices using `np.random.randint()`.
2. Perform:
   - Element-wise multiplication.
   - Matrix multiplication.
   - Matrix transpose.
3. Generate a random invertible `3 × 3` matrix.
4. Compute:
   - Determinant.
   - Inverse.
   - Verify the inverse using `np.allclose(A @ inv(A), np.eye(3))`.
5. Create and solve at least three different systems of linear equations using `np.linalg.solve()`.
6. Compare solving with `np.linalg.solve()` and `np.linalg.inv(A) @ b`, and explain why the former is preferred in production code.

---

# Summary

In this lesson, you learned the core linear algebra operations provided by NumPy. You explored matrix multiplication using `@` and `np.matmul()`, dot products, transposition, determinants, inverses, norms, and solving systems of linear equations. You also learned an important engineering practice: avoid computing matrix inverses when solving equations—use `np.linalg.solve()` instead. These concepts form the mathematical backbone of machine learning, computer graphics, optimization, and scientific computing.

---

# Next Lesson

**File:**

[10-random-numbers.md](10-random-numbers.md)
