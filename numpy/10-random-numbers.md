# NumPy Part 10: Random Number Generation

**Python Version Introduced:** Python 3.x

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will be able to:

- Understand why random number generation is essential in scientific computing and machine learning.
- Distinguish between truly random and pseudorandom numbers.
- Use NumPy's modern random number generation API.
- Generate random integers, floating-point numbers, and samples from common probability distributions.
- Understand reproducibility using random seeds.
- Randomly shuffle and sample data.
- Choose appropriate random distributions for different problems.
- Apply best practices for production-quality random number generation.

______________________________________________________________________

# Recap

In the previous lesson, you learned about:

- Matrix multiplication
- Dot products
- Matrix inversion
- Determinants
- Solving linear systems
- Vector norms

These operations are heavily used in machine learning.

However, machine learning also depends on **randomness** for tasks such as:

- Initializing model parameters
- Splitting datasets
- Sampling training data
- Simulating systems
- Running Monte Carlo algorithms

______________________________________________________________________

# Why Random Numbers Matter

Suppose you are building:

- A recommendation system
- A neural network
- A fraud detection model
- A weather simulation
- A financial risk model

Random numbers are used throughout these systems.

Examples include:

- Randomly splitting training and test data.
- Initializing neural network weights.
- Simulating thousands of future market scenarios.
- Randomly sampling customer behavior.

Without high-quality random number generation, many algorithms become biased or difficult to reproduce.

______________________________________________________________________

# True Random vs Pseudorandom

Computers cannot generate truly random numbers without external physical processes.

Instead, they generate **pseudorandom** numbers.

A pseudorandom number generator (PRNG):

- Starts from an initial state called a **seed**.
- Produces a deterministic sequence.
- Appears statistically random.

Example:

```
Seed

↓

42

↓

0.773956

↓

0.438878

↓

0.858598

...
```

Using the same seed always produces the same sequence.

______________________________________________________________________

# Legacy vs Modern API

Older NumPy code often uses:

```python
np.random.rand()
np.random.randint()
np.random.seed()
```

Modern NumPy recommends using a **Generator** object.

```python
rng = np.random.default_rng()
```

Why?

- Better algorithms.
- Improved statistical quality.
- Independent random streams.
- Easier parallel programming.

For new code, prefer the `Generator` API.

______________________________________________________________________

# Creating a Random Generator

```python
import numpy as np

rng = np.random.default_rng()
```

Now generate random numbers using `rng`.

______________________________________________________________________

# Reproducibility with Seeds

## Why Use a Seed?

Suppose you are debugging a machine learning model.

Without a fixed seed:

```python
rng = np.random.default_rng()

print(rng.random(5))
```

Every execution produces different results.

This makes debugging difficult.

______________________________________________________________________

With a seed:

```python
rng = np.random.default_rng(42)

print(rng.random(5))
```

Every execution produces the same sequence.

This is called **reproducibility**.

______________________________________________________________________

## Best Practice

Use fixed seeds for:

- Experiments
- Unit tests
- Tutorials
- Scientific research

Avoid fixed seeds in production systems that require fresh randomness.

______________________________________________________________________

# `random()`

## What does it do?

Generates floating-point numbers uniformly distributed between 0 (inclusive) and 1 (exclusive).

______________________________________________________________________

## Syntax

```python
rng.random(size=None)
```

______________________________________________________________________

## Parameters

| Parameter | Description |
|-----------|-------------|
| `size` | Shape of the output |

______________________________________________________________________

## Return Value

An array (or scalar) of floating-point numbers.

______________________________________________________________________

## Example

```python
rng = np.random.default_rng(42)

print(rng.random(5))
```

Example output

```
[0.77395605 0.43887844 0.85859792 0.69736803 0.09417735]
```

______________________________________________________________________

# `integers()`

## What does it do?

Generates random integers.

______________________________________________________________________

## Syntax

```python
rng.integers(low, high=None, size=None)
```

______________________________________________________________________

## Parameters

| Parameter | Description |
|-----------|-------------|
| `low` | Lowest value (inclusive) |
| `high` | Highest value (exclusive) |
| `size` | Output shape |

______________________________________________________________________

## Example

```python
rng = np.random.default_rng(42)

print(
    rng.integers(
        1,
        10,
        size=5
    )
)
```

Example output

```
[1 7 6 4 4]
```

Notice:

```
10
```

is excluded.

______________________________________________________________________

# Random Arrays

Generate a matrix.

```python
matrix = rng.random((3,4))

print(matrix)
```

Shape

```
(3,4)
```

This is useful for:

- Simulations
- Initializing weights
- Testing algorithms

______________________________________________________________________

# Common Probability Distributions

Real-world data rarely follows a uniform distribution.

NumPy provides many probability distributions.

______________________________________________________________________

# Uniform Distribution

Every value has the same probability.

```python
rng.uniform(
    10,
    20,
    size=5
)
```

Produces random numbers between 10 and 20.

Applications:

- Random sampling
- Simulations
- Random initialization

______________________________________________________________________

# Normal Distribution

The most common distribution in statistics.

Most values cluster around the mean.

```python
rng.normal(
    loc=0,
    scale=1,
    size=5
)
```

Parameters:

| Parameter | Meaning |
|-----------|---------|
| `loc` | Mean |
| `scale` | Standard deviation |

Applications:

- Measurement errors
- Heights
- Machine learning
- Statistical modeling

______________________________________________________________________

# Binomial Distribution

Represents repeated yes/no experiments.

```python
rng.binomial(
    n=10,
    p=0.5,
    size=5
)
```

Applications:

- Coin flips
- Success/failure experiments
- Reliability analysis

______________________________________________________________________

# Choice Sampling

## What does it do?

Randomly selects values from an array.

______________________________________________________________________

## Syntax

```python
rng.choice(
    data,
    size,
    replace=True
)
```

______________________________________________________________________

## Example

```python
colors = np.array([
    "Red",
    "Blue",
    "Green",
    "Black"
])

print(
    rng.choice(
        colors,
        size=2
    )
)
```

Example output

```
['Blue' 'Black']
```

______________________________________________________________________

## Sampling Without Replacement

```python
rng.choice(
    colors,
    size=3,
    replace=False
)
```

Each value appears at most once.

This is useful for train/test splitting and random selection.

______________________________________________________________________

# Shuffling

## `shuffle()`

Shuffles an array **in place**.

```python
arr = np.arange(10)

rng.shuffle(arr)

print(arr)
```

The original array changes.

______________________________________________________________________

## `permutation()`

Returns a shuffled copy.

```python
arr = np.arange(10)

new = rng.permutation(arr)

print(new)
print(arr)
```

The original array remains unchanged.

______________________________________________________________________

# Random Booleans

Generate random True/False values.

```python
mask = rng.integers(
    0,
    2,
    size=10,
    dtype=bool
)

print(mask)
```

Applications:

- Random masking
- Data augmentation
- Feature selection

______________________________________________________________________

# Performance Notes

Operation | Typical Complexity | Notes ----------|--------------------|------ `random()` | O(n) | Uniform floats
`integers()` | O(n) | Random integers `choice()` | O(k) to O(n)\* | Depends on replacement strategy `shuffle()` | O(n) |
In-place `permutation()` | O(n) | Returns a copy Distribution sampling | O(n) | Depends on algorithm

\*Sampling without replacement may require additional work depending on the requested sample size.

______________________________________________________________________

# Common Mistakes

## Mistake 1

Using the legacy API in new projects.

Prefer:

```python
rng = np.random.default_rng()
```

instead of

```python
np.random.seed()
```

______________________________________________________________________

## Mistake 2

Forgetting reproducibility.

Without a fixed seed,

results change every execution.

______________________________________________________________________

## Mistake 3

Misunderstanding the upper bound.

```python
rng.integers(1,10)
```

Generates values from

```
1

through

9
```

The upper bound is excluded.

______________________________________________________________________

## Mistake 4

Using `shuffle()` when the original array must remain unchanged.

Use `permutation()` instead.

______________________________________________________________________

## Mistake 5

Choosing the wrong probability distribution.

Uniform and normal distributions model very different types of data.

Always choose the distribution that matches the problem domain.

______________________________________________________________________

# Best Practices

- Use `np.random.default_rng()` for all new projects.
- Set seeds for experiments and testing.
- Avoid fixed seeds in production systems requiring unpredictable randomness.
- Use `choice(replace=False)` for random sampling without duplicates.
- Use `permutation()` when the original data must be preserved.
- Understand the statistical assumptions behind each probability distribution.

______________________________________________________________________

# Production Insight

Random number generation underpins many production systems.

Examples include:

- Train/test dataset splitting.
- Cross-validation.
- Weight initialization in deep learning.
- Monte Carlo simulations for financial risk.
- Randomized algorithms.
- A/B testing.
- Synthetic data generation.
- Stochastic optimization.

Poor random number management can make experiments impossible to reproduce or introduce subtle statistical bias.

______________________________________________________________________

```markdown id="f3k8wp"
# Questions

### Question

> Why should new NumPy code use `default_rng()` instead of the legacy API?

### Answer

Because it provides improved algorithms, better statistical quality, independent random streams, and is the recommended modern interface.

---

### Question

> What is the purpose of setting a random seed?

### Answer

It ensures reproducible sequences of pseudorandom numbers, making experiments and debugging repeatable.

---

### Question

> What is the difference between `shuffle()` and `permutation()`?

### Answer

`shuffle()` modifies the original array in place, while `permutation()` returns a shuffled copy.

---

### Question

> Which distribution would you typically use to model measurement errors?

### Answer

The normal (Gaussian) distribution.
```

______________________________________________________________________

# Practical Lesson

Create a random number generator with a seed of `123`.

```python
rng = np.random.default_rng(123)
```

Complete the following tasks:

1. Generate:
   - Ten random floating-point numbers.
   - Ten random integers between 50 and 100.
1. Create a `5 × 5` matrix of random floating-point numbers.
1. Generate:
   - Five samples from a normal distribution with mean `100` and standard deviation `15`.
   - Five samples from a uniform distribution between `0` and `1`.
1. Randomly select five unique values from `np.arange(20)`.
1. Shuffle an array in place and compare it with using `permutation()`.
1. Create a random Boolean mask of length `20`.
1. Run the program twice with the same seed and verify that the outputs are identical.

______________________________________________________________________

```markdown id="u9m2rd"
# Knowledge Check

## Question 1

What is a pseudorandom number generator (PRNG)?

### Answer

A deterministic algorithm that produces sequences of numbers that appear random, starting from an initial seed.

---

## Question 2

Why is reproducibility important in machine learning experiments?

### Answer

It allows experiments to be repeated exactly, making debugging, validation, and scientific comparison possible.

---

## Question 3

What is the recommended way to create a random number generator in modern NumPy?

### Answer

`np.random.default_rng()`.

---

## Question 4

Does `rng.integers(low, high)` include the `high` value?

### Answer

No. The upper bound is exclusive.

---

## Question 5

Which function modifies an array in place: `shuffle()` or `permutation()`?

### Answer

`shuffle()`.

---

## Question 6

Which distribution is commonly used to model naturally occurring measurements?

### Answer

The normal (Gaussian) distribution.

---

## Question 7

When would you use `choice(replace=False)`?

### Answer

When sampling unique values without replacement.

---

## Question 8

Should production systems always use a fixed random seed?

### Answer

No. Fixed seeds are valuable for testing and experiments, but production systems often require fresh randomness depending on the application.
```

______________________________________________________________________

# Assignment

Build a simple simulation toolkit.

1. Create a reusable `Generator` using `np.random.default_rng(42)`.
1. Generate:
   - A `100 × 5` matrix of random features.
   - A vector of random binary labels.
1. Simulate rolling two dice 100,000 times and calculate:
   - Frequency of each possible sum.
   - Probability of rolling a sum of 7.
1. Randomly split a dataset of 1,000 samples into:
   - 80% training
   - 20% testing
without replacement.
1. Compare samples generated from:
   - Uniform distribution
   - Normal distribution
   - Binomial distribution
and explain appropriate real-world use cases for each.
1. Ensure the entire simulation is reproducible by rerunning it with the same seed and verifying identical results.

______________________________________________________________________

# Summary

In this lesson, you learned how NumPy generates pseudorandom numbers using its modern `Generator` API. You explored
reproducibility through seeds, generated random integers and floating-point numbers, sampled from common probability
distributions, randomly selected and shuffled data, and learned the difference between in-place and copy-based
randomization. These concepts are fundamental to simulations, testing, statistical analysis, and machine learning
workflows.

______________________________________________________________________

# Next Lesson

**File:**

[11-performance-optimization.md](11-performance-optimization.md)
