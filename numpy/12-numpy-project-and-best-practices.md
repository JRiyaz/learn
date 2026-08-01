# NumPy Part 12: Production Project & NumPy Best Practices

**Python Version Introduced:** Python 3.x

______________________________________________________________________

# Learning Objectives

By the end of this lesson, you will be able to:

- Apply the major NumPy concepts learned throughout this course in a realistic project.
- Design a data processing pipeline using NumPy.
- Choose efficient NumPy operations based on performance and memory considerations.
- Follow production-ready coding practices.
- Identify common anti-patterns and avoid them.
- Know when NumPy is the right tool—and when it is not.

______________________________________________________________________

# Recap

Over the past eleven lessons, you learned:

- NumPy architecture and `ndarray`
- Creating arrays
- Memory model
- Views vs copies
- Indexing and slicing
- Reshaping
- Vectorization
- Broadcasting
- Mathematical operations
- Searching, sorting, and filtering
- Linear algebra
- Random number generation
- Performance optimization

Now it's time to combine these concepts into a realistic engineering workflow.

______________________________________________________________________

# Project Scenario

Imagine you work at a company that manufactures IoT temperature sensors.

Every sensor reports:

- Sensor ID
- Temperature
- Humidity
- Battery level

Every minute.

One day contains:

```
10,000 sensors

×

1,440 readings

=

14.4 million records
```

The engineering team must answer questions such as:

- Which sensors are faulty?
- What is the daily average temperature?
- Which sensors have low battery?
- Which readings are outliers?
- Which sensors require maintenance?

The data has already been loaded into NumPy arrays.

Your task is to process it efficiently.

______________________________________________________________________

# Step 1 — Generate Sample Data

```python
import numpy as np

rng = np.random.default_rng(42)

num_sensors = 10_000

temperature = rng.normal(
    loc=25,
    scale=3,
    size=num_sensors
)

humidity = rng.uniform(
    20,
    90,
    size=num_sensors
)

battery = rng.uniform(
    0,
    100,
    size=num_sensors
)

sensor_ids = np.arange(num_sensors)
```

This simulates one reading from every sensor.

______________________________________________________________________

# Step 2 — Basic Statistics

Calculate:

```python
print(temperature.mean())

print(temperature.min())

print(temperature.max())

print(temperature.std())
```

Typical engineering questions:

- Is the average temperature reasonable?
- Are there abnormal spikes?
- Is variability increasing over time?

______________________________________________________________________

# Step 3 — Detect Faulty Sensors

Suppose any sensor reporting

```
Temperature

>

35°C
```

should be inspected.

```python
faulty = temperature > 35
```

Retrieve the IDs.

```python
faulty_ids = sensor_ids[faulty]

print(faulty_ids)
```

No Python loop is required.

______________________________________________________________________

# Step 4 — Battery Monitoring

Sensors below

```
20%
```

battery require replacement.

```python
low_battery = battery < 20

replace_ids = sensor_ids[low_battery]
```

Count them.

```python
print(low_battery.sum())
```

Notice that Boolean arrays can also be aggregated because:

```
True

↓

1

False

↓

0
```

______________________________________________________________________

# Step 5 — Combine Conditions

Suppose maintenance is required only when:

- Battery < 20%

AND

- Temperature > 35°C

```python
maintenance = (
    (battery < 20)
    &
    (temperature > 35)
)

maintenance_ids = sensor_ids[maintenance]
```

______________________________________________________________________

# Step 6 — Sort by Temperature

Engineering wants the hottest sensors first.

```python
order = np.argsort(
    temperature
)[::-1]

sorted_ids = sensor_ids[order]

sorted_temp = temperature[order]
```

Because `argsort()` returns indices, related arrays stay aligned.

______________________________________________________________________

# Step 7 — Normalize Data

Many machine learning algorithms perform better when features have similar scales.

One common approach is **standardization**.

```python
normalized = (
    temperature
    - temperature.mean()
) / temperature.std()
```

The resulting data has:

```
Mean ≈ 0

Standard Deviation ≈ 1
```

______________________________________________________________________

# Step 8 — Simulate Missing Values

Real-world data is rarely perfect.

Introduce some missing values.

```python
temperature = temperature.astype(float)

temperature[100:110] = np.nan
```

Compute the mean.

```python
print(temperature.mean())
```

Output

```
nan
```

Instead, use

```python
print(np.nanmean(temperature))
```

NumPy provides a family of `nan*` functions such as:

- `np.nanmean()`
- `np.nanmedian()`
- `np.nanstd()`
- `np.nansum()`

These ignore missing values.

______________________________________________________________________

# Step 9 — Reshape Data

Suppose one sensor reports every hour.

```python
hourly = np.arange(24)

daily = hourly.reshape(
    6,
    4
)
```

Reshaping allows data to be viewed differently without moving memory when possible.

______________________________________________________________________

# Step 10 — Performance Improvements

Bad

```python
result = []

for value in temperature:

    result.append(value * 1.8 + 32)
```

Good

```python
fahrenheit = (
    temperature * 1.8
) + 32
```

The second version is:

- Shorter
- Faster
- More readable
- More memory efficient

______________________________________________________________________

# End-to-End Pipeline

A simplified processing pipeline looks like this:

```
Raw Sensor Data

↓

Validation

↓

Filtering

↓

Cleaning

↓

Normalization

↓

Statistics

↓

Feature Engineering

↓

Machine Learning

↓

Reports / Predictions
```

NumPy forms the computational foundation of many of these stages.

______________________________________________________________________

# NumPy Best Practices

## 1. Prefer Vectorization

Instead of

```python
for value in arr:
    ...
```

Use

```python
arr * 2
```

______________________________________________________________________

## 2. Understand Views vs Copies

Avoid unnecessary `.copy()` calls.

Views reduce memory usage.

______________________________________________________________________

## 3. Choose Appropriate Data Types

Instead of

```python
float64
```

consider

```python
float32
```

when precision requirements allow.

This can significantly reduce memory consumption.

______________________________________________________________________

## 4. Use Broadcasting

Instead of creating repeated arrays,

allow NumPy to broadcast.

Broadcasting is both cleaner and more memory efficient.

______________________________________________________________________

## 5. Profile Before Optimizing

Never assume.

Always measure.

Useful tools:

- `timeit`
- `cProfile`

______________________________________________________________________

## 6. Avoid Growing Arrays

Bad

```python
np.append(...)
```

inside loops.

Better

- Preallocate.
- Vectorize.
- Build Python lists first if the final size is unknown, then convert once to a NumPy array.

______________________________________________________________________

## 7. Prefer Modern Random API

Use

```python
rng = np.random.default_rng()
```

instead of the legacy random API.

______________________________________________________________________

## 8. Use Boolean Masks

Instead of nested loops,

use

```python
arr[arr > 50]
```

This is faster and easier to read.

______________________________________________________________________

## 9. Use the Right Tool

NumPy excels at:

- Dense numerical arrays
- Matrix operations
- Scientific computing
- Vectorized computation

NumPy is **not** ideal for:

- Labeled tabular data (use Pandas)
- Distributed processing
- SQL-like joins
- Sparse matrices (specialized libraries are often better)

Choosing the right abstraction is an important engineering decision.

______________________________________________________________________

## 10. Write Readable Code

This

```python
temperature[
    (temperature > 30)
    &
    (battery > 20)
]
```

is clearer than a complex loop.

Readable code is easier to maintain, debug, and optimize.

______________________________________________________________________

# Common Anti-Patterns

Avoid these patterns in production.

| Anti-Pattern | Better Approach |
|--------------|----------------|
| Python loops over arrays | Vectorized operations |
| `np.append()` inside loops | Preallocate or collect first |
| Excessive `.copy()` | Use views where appropriate |
| Ignoring dtypes | Choose the smallest appropriate dtype |
| Computing inverses unnecessarily | Use `np.linalg.solve()` |
| Sorting values when indices are needed | Use `argsort()` |
| Using legacy random APIs | Use `default_rng()` |

______________________________________________________________________

# Production Insight

A typical machine learning preprocessing pipeline looks like:

```
CSV

↓

Pandas

↓

Cleaning

↓

NumPy Arrays

↓

Feature Engineering

↓

Scikit-Learn

↓

Model

↓

Prediction
```

Notice that NumPy often sits at the center of the computational workflow.

Many libraries—including Pandas, SciPy, Scikit-learn, XGBoost, TensorFlow, and PyTorch—either build on NumPy concepts or
provide interoperability with NumPy arrays.

Understanding NumPy well makes learning the rest of the Python data ecosystem significantly easier.

______________________________________________________________________

```markdown id="w6m9ta"
# Questions

### Question

> Why is NumPy considered the foundation of the Python scientific ecosystem?

### Answer

Because it provides the efficient array data structure and numerical operations that many higher-level libraries build upon.

---

### Question

> Why should `argsort()` be preferred when sorting related datasets?

### Answer

Because it returns sorting indices that can be applied consistently to multiple arrays, preserving relationships between them.

---

### Question

> Why are Boolean masks preferred over Python loops for filtering?

### Answer

Because they are vectorized, concise, and execute efficiently in optimized compiled code.

---

### Question

> When should Pandas be chosen instead of NumPy?

### Answer

When working primarily with labeled, heterogeneous tabular data that requires indexing, grouping, joins, or missing-value handling.
```

______________________________________________________________________

# Practical Lesson

Build a miniature sensor analytics system.

Generate synthetic data for:

```python
num_sensors = 5000
```

Create arrays for:

- Sensor IDs
- Temperature
- Humidity
- Battery percentage
- Signal strength

Perform the following tasks:

1. Compute summary statistics for every measurement.
1. Detect:
   - High temperatures (`> 35°C`)
   - Low battery (`< 20%`)
   - Weak signal (`< 30%`)
1. Identify sensors satisfying multiple fault conditions.
1. Sort sensors by temperature and battery level.
1. Normalize temperature values.
1. Introduce missing values and compute statistics using the `nan*` functions.
1. Produce a summary report containing:
   - Total sensors
   - Faulty sensors
   - Sensors requiring maintenance
   - Average battery level
   - Maximum recorded temperature

Implement the solution without explicit Python loops over the sensor arrays.

______________________________________________________________________

```markdown id="r2k8pf"
# Knowledge Check

## Question 1

What is the primary performance advantage of vectorization?

### Answer

It executes operations in optimized compiled code while eliminating Python-level loops.

---

## Question 2

Why should unnecessary copies be avoided?

### Answer

Because they increase memory consumption and may reduce performance.

---

## Question 3

Which NumPy functions ignore missing (`NaN`) values during aggregation?

### Answer

Functions such as `np.nanmean()`, `np.nanmedian()`, `np.nanstd()`, and `np.nansum()`.

---

## Question 4

Why is `np.argsort()` useful when sorting multiple related arrays?

### Answer

Because it returns index positions that preserve relationships between arrays.

---

## Question 5

When should you choose `float32` over `float64`?

### Answer

When the reduced precision is sufficient and lowering memory usage is beneficial.

---

## Question 6

Why is `np.random.default_rng()` recommended?

### Answer

Because it provides the modern random number generation API with improved statistical properties and better design.

---

## Question 7

Which library is typically used after NumPy for labeled tabular datasets?

### Answer

Pandas.

---

## Question 8

What are the three most important principles for writing efficient NumPy code?

### Answer

Vectorize operations, minimize unnecessary memory allocations, and measure performance before optimizing.
```

______________________________________________________________________

# Assignment

Build a **production-style sensor data analytics pipeline**.

Requirements:

1. Simulate **100,000 sensor readings** with:
   - Sensor ID
   - Temperature
   - Humidity
   - Battery level
   - Pressure
1. Perform:
   - Data validation
   - Statistical summaries
   - Outlier detection
   - Boolean filtering
   - Sorting and ranking
   - Feature normalization
1. Generate:
   - Daily operational summary
   - Maintenance report
   - Top 20 hottest sensors
   - Lowest battery sensors
1. Benchmark the pipeline using `timeit`.
1. Ensure the implementation:
   - Uses vectorized operations.
   - Avoids unnecessary copies.
   - Uses appropriate dtypes.
   - Uses the modern random number generator.
1. Document the design decisions and explain why each NumPy operation was chosen.

______________________________________________________________________

# Summary

Congratulations! You have completed the NumPy curriculum.

Across twelve lessons, you progressed from understanding the `ndarray` memory model to building a production-style data
processing pipeline. Along the way, you learned array creation, memory management, indexing, reshaping, vectorization,
broadcasting, statistical operations, searching and sorting, linear algebra, random number generation, and performance
optimization.

More importantly, you learned the engineering principles behind NumPy:

- Think in terms of whole-array operations rather than element-by-element loops.
- Understand when data is shared versus copied.
- Optimize based on measurement rather than assumptions.
- Balance performance, memory usage, correctness, and readability.

These concepts provide the foundation for the rest of the Python data ecosystem.

______________________________________________________________________

# Next Lesson

**File:**

[01-pandas-architecture-and-dataframe-fundamentals.md](01-pandas-architecture-and-dataframe-fundamentals.md)
