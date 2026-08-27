# 42. NumPy & Pandas Overview

**Previous:** [41. TypeScript, Angular Overview](./41-typescript-angular.md)

**Next:** [43. Design Patterns & Architecture](./43-design-patterns-architecture.md)

______________________________________________________________________

## Objective

This is deliberately an **overview topic**, not a deep-dive.

The goal is to give a Python backend engineer enough NumPy and Pandas knowledge to:

- Recognize the core data structures.
- Understand basic array and tabular-data operations.
- Read existing NumPy/Pandas code.
- Understand vectorized operations and broadcasting.
- Understand the difference between views and copies.
- Perform basic filtering, grouping and aggregation.
- Understand joins/merges.
- Handle missing values.
- Read and write common data formats.
- Understand when NumPy, Pandas or normal Python data structures are appropriate.

You are **not** expected to become a data-science specialist from this file.

______________________________________________________________________

# Part 1 — NumPy

# 1. What Is NumPy?

NumPy is a Python library for numerical computing.

Its central data structure is:

```text
ndarray
```

A NumPy array provides efficient operations over homogeneous numerical data.

Conceptually:

```text
Python list
    ↓
general-purpose container

NumPy ndarray
    ↓
numerical array operations
```

______________________________________________________________________

# 2. Why NumPy?

Python lists are flexible, but numerical operations over large lists can require Python-level iteration.

NumPy provides:

```text
Efficient array storage
Vectorized operations
Broadcasting
Fast numerical operations
Multi-dimensional arrays
```

Example:

```python
import numpy as np

values = np.array([1, 2, 3, 4])

result = values * 2

print(result)
# [2 4 6 8]
```

The operation applies to the whole array.

______________________________________________________________________

# 3. `ndarray`

The main NumPy object is the `ndarray`.

Example:

```python
import numpy as np

arr = np.array([10, 20, 30])
```

Conceptually:

```text
arr
 ├── data
 ├── shape
 ├── dimensions
 └── dtype
```

______________________________________________________________________

# 4. Shape

`shape` describes the size of each dimension.

One-dimensional:

```python
arr = np.array([1, 2, 3, 4])

arr.shape
# (4,)
```

Two-dimensional:

```python
arr = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

arr.shape
# (2, 3)
```

This means:

```text
2 rows
3 columns
```

______________________________________________________________________

# 5. Dimensions

The number of dimensions is available through:

```python
arr.ndim
```

Examples:

```text
[1, 2, 3]
→ ndim = 1

[[1, 2], [3, 4]]
→ ndim = 2
```

Higher-dimensional arrays are also possible.

______________________________________________________________________

# 6. `dtype`

NumPy arrays have a data type.

```python
arr = np.array([1, 2, 3])

arr.dtype
```

Possible types include:

```text
int
float
bool
complex
```

and more specialized NumPy types.

______________________________________________________________________

# 7. Why `dtype` Matters

The data type affects:

```text
Memory usage
Precision
Performance
Supported operations
```

For example:

```python
arr = np.array([1, 2, 3], dtype=np.int32)
```

The array explicitly uses a 32-bit integer representation.

______________________________________________________________________

# 8. Indexing

NumPy indexing is similar to Python sequence indexing.

```python
arr = np.array([10, 20, 30, 40])

arr[0]
# 10

arr[2]
# 30
```

For a two-dimensional array:

```python
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

matrix[0, 1]
# 2
```

The first index selects the row and the second selects the column.

______________________________________________________________________

# 9. Slicing

NumPy supports slicing:

```python
arr = np.array([10, 20, 30, 40, 50])

arr[1:4]
# [20 30 40]
```

Two-dimensional slicing:

```python
matrix[:, 1]
```

selects the second column.

______________________________________________________________________

# 10. Boolean Indexing

NumPy supports filtering with boolean expressions.

```python
values = np.array([10, 20, 30, 40])

values[values > 20]
```

Result:

```text
[30 40]
```

This is an important building block for vectorized data processing.

______________________________________________________________________

# 11. Reshape

`reshape()` changes the array's dimensions without changing the underlying values when possible.

```python
arr = np.array([1, 2, 3, 4, 5, 6])

matrix = arr.reshape(2, 3)
```

Result:

```text
[[1 2 3]
 [4 5 6]]
```

The total number of elements must remain compatible.

______________________________________________________________________

# 12. Reshape Mental Model

Before:

```text
6 values
[1 2 3 4 5 6]
```

After:

```text
2 × 3

[1 2 3]
[4 5 6]
```

Same number of elements:

```text
6
```

______________________________________________________________________

# 13. Views vs Copies

This is an important NumPy concept.

A **view** provides another way of looking at existing data.

A **copy** creates independent data.

Conceptually:

```text
Original data
     ↑
    View
```

versus:

```text
Original data     Copy
     ↓              ↓
 separate data   separate data
```

Changes to a view can affect the original array.

______________________________________________________________________

# 14. Example — View

For many slicing operations:

```python
arr = np.array([1, 2, 3, 4])

view = arr[1:3]
```

`view` may share memory with `arr`.

Therefore:

```python
view[0] = 99
```

can also change the corresponding value in `arr`.

The exact memory behavior depends on the operation.

______________________________________________________________________

# 15. Example — Copy

Explicitly request a copy:

```python
copy = arr[1:3].copy()
```

Now modifications to `copy` do not modify the original array.

This distinction matters when manipulating large arrays or passing data between functions.

______________________________________________________________________

# 16. Vectorization

Vectorization means applying operations to entire arrays rather than explicitly writing Python loops.

Instead of:

```python
result = []

for value in values:
    result.append(value * 2)
```

NumPy allows:

```python
result = values * 2
```

This is concise and can be significantly faster for numerical workloads.

______________________________________________________________________

# 17. Why Vectorization Can Be Faster

NumPy's numerical operations are implemented using optimized low-level code.

Conceptually:

```text
Python loop
→ repeated Python-level operations

NumPy vectorized operation
→ optimized array operation
```

The performance difference can be substantial for sufficiently large numerical workloads.

______________________________________________________________________

# 18. Broadcasting

Broadcasting allows NumPy to perform operations between arrays with compatible shapes.

Example:

```python
arr = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

arr + 10
```

Result:

```text
[[11 12 13]
 [14 15 16]]
```

The scalar `10` is effectively applied to every element.

______________________________________________________________________

# 19. Broadcasting Example

A one-dimensional array can also be broadcast across rows:

```python
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

values = np.array([10, 20, 30])

matrix + values
```

Result:

```text
[[11 22 33]
 [14 25 36]]
```

NumPy aligns compatible dimensions to perform the operation.

______________________________________________________________________

# 20. Broadcasting Rule — High Level

Dimensions are compared from the right.

Two dimensions are compatible when they are:

```text
Equal
```

or:

```text
One of them is 1
```

A scalar can broadcast across any compatible array shape.

For this course, remember:

> Broadcasting allows compatible differently shaped arrays to participate in element-wise operations.

______________________________________________________________________

# 21. Basic Arithmetic

NumPy supports element-wise operations:

```python
a + b
a - b
a * b
a / b
a ** 2
```

Example:

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

a + b
# [11 22 33]
```

______________________________________________________________________

# 22. Aggregations

Common aggregation operations include:

```python
values.sum()
values.mean()
values.min()
values.max()
values.std()
```

Example:

```python
values = np.array([10, 20, 30])

values.sum()
# 60

values.mean()
# 20
```

______________________________________________________________________

# 23. Aggregation by Axis

For a matrix:

```python
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
```

You can aggregate across an axis.

For example:

```python
matrix.sum(axis=0)
```

produces column-wise sums:

```text
[5 7 9]
```

And:

```python
matrix.sum(axis=1)
```

produces row-wise sums:

```text
[6 15]
```

______________________________________________________________________

# 24. NumPy vs Python Lists

| Feature | Python List | NumPy ndarray |
|---|---|---|
| General-purpose | Excellent | Primarily numerical |
| Mixed types | Easy | Less typical |
| Vectorized math | No | Yes |
| Multi-dimensional arrays | Nested lists | Native |
| Broadcasting | No | Yes |
| Numerical performance | Often slower for bulk numeric operations | Often faster |
| Flexibility | Very high | More specialized |

Choose based on the problem.

______________________________________________________________________

# 25. When Should You Use NumPy?

NumPy is useful for:

```text
Numerical calculations
Matrices
Arrays
Scientific computing
Vectorized transformations
Large numerical datasets
```

For ordinary application data such as:

```text
Users
Orders
Products
API payloads
```

normal Python structures or Pandas may be more appropriate depending on the task.

______________________________________________________________________

# Part 2 — Pandas

# 26. What Is Pandas?

Pandas is a Python library for working with structured/tabular data.

Its two primary structures are:

```text
Series
DataFrame
```

Conceptually:

```text
NumPy
→ numerical arrays

Pandas
→ labeled/tabular data
```

Pandas is built heavily around NumPy concepts.

______________________________________________________________________

# 27. Series

A Series is a one-dimensional labeled data structure.

```python
import pandas as pd

s = pd.Series([10, 20, 30])
```

Conceptually:

```text
index   value
0       10
1       20
2       30
```

______________________________________________________________________

# 28. DataFrame

A DataFrame is a two-dimensional table.

```python
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35]
})
```

Conceptually:

```text
      name      age
0     Alice      25
1     Bob        30
2     Charlie    35
```

______________________________________________________________________

# 29. DataFrame Mental Model

Think of a DataFrame as:

```text
Rows
+
Columns
+
Index
```

Each column behaves similarly to a Series.

______________________________________________________________________

# 30. Indexing Columns

Select one column:

```python
df["name"]
```

Select multiple columns:

```python
df[["name", "age"]]
```

This is one of the most common Pandas operations.

______________________________________________________________________

# 31. Row Selection

Using `.loc`:

```python
df.loc[0]
```

selects a row by label.

Using `.iloc`:

```python
df.iloc[0]
```

selects a row by integer position.

For this overview, remember:

```text
loc  → label-based
iloc → position-based
```

______________________________________________________________________

# 32. Filtering

Pandas supports boolean filtering.

```python
df[df["age"] > 25]
```

This returns rows where:

```text
age > 25
```

Multiple conditions can be combined.

```python
df[(df["age"] > 25) & (df["age"] < 40)]
```

______________________________________________________________________

# 33. Why Parentheses Matter

When combining Pandas conditions, use:

```python
(df["age"] > 25) & (df["age"] < 40)
```

rather than:

```python
df["age"] > 25 & df["age"] < 40
```

The parentheses make the intended boolean expressions explicit.

______________________________________________________________________

# 34. Creating Columns

You can create a derived column:

```python
df["age_plus_10"] = df["age"] + 10
```

This applies the operation across the column.

Pandas can use vectorized operations for many transformations.

______________________________________________________________________

# 35. Grouping

`groupby()` groups rows by one or more columns.

Example:

```python
df.groupby("department")["salary"].mean()
```

Conceptually:

```text
Group by department
        ↓
Calculate average salary
```

This is one of the most important Pandas operations.

______________________________________________________________________

# 36. Aggregation

Common aggregation functions:

```text
sum
mean
min
max
count
median
```

Example:

```python
df.groupby("department")["salary"].agg(["count", "mean", "max"])
```

This produces multiple statistics per group.

______________________________________________________________________

# 37. GroupBy Mental Model

Think:

```text
Split
 ↓
Apply
 ↓
Combine
```

Example:

```text
DataFrame
   ↓
split by department
   ↓
calculate average salary
   ↓
combine results
```

This mental model makes `groupby()` easier to understand.

______________________________________________________________________

# 38. Merge

Pandas can combine tables using `merge()`.

Example:

```python
users = pd.DataFrame({
    "user_id": [1, 2],
    "name": ["Alice", "Bob"]
})

orders = pd.DataFrame({
    "user_id": [1, 2],
    "amount": [100, 200]
})

result = users.merge(
    orders,
    on="user_id"
)
```

This is conceptually similar to a SQL join.

______________________________________________________________________

# 39. Merge Types

Common merge types:

```text
inner
left
right
outer
```

Conceptually similar to:

```sql
INNER JOIN
LEFT JOIN
RIGHT JOIN
FULL OUTER JOIN
```

For backend engineers, this SQL comparison is useful.

______________________________________________________________________

# 40. Join

Pandas also supports `join()`.

The exact semantics differ from SQL depending on the index and parameters.

For basic understanding:

```text
merge()
→ explicit column-based combination

join()
→ commonly index-oriented combination
```

______________________________________________________________________

# 41. Missing Values

Real-world datasets often contain missing values.

Pandas commonly represents missing data using values such as:

```text
NaN
None
pd.NA
```

The exact representation depends on the data type.

______________________________________________________________________

# 42. Detecting Missing Values

Common operations:

```python
df.isna()
df.notna()
```

For example:

```python
df[df["email"].isna()]
```

finds rows where email is missing.

______________________________________________________________________

# 43. Dropping Missing Values

You can remove missing values:

```python
df.dropna()
```

This is simple but can discard useful data.

Always understand which rows/columns are being removed.

______________________________________________________________________

# 44. Filling Missing Values

You can replace missing values:

```python
df["age"] = df["age"].fillna(0)
```

Or use a more meaningful default:

```python
df["status"] = df["status"].fillna("unknown")
```

The correct strategy depends on what missingness means in the dataset.

______________________________________________________________________

# 45. Missing Values Are a Data Problem

Do not blindly do:

```python
fillna(0)
```

For every column.

For example:

```text
Missing salary
```

does not necessarily mean:

```text
salary = 0
```

Missing data requires domain understanding.

______________________________________________________________________

# 46. Reading Data

Pandas can read common data formats.

CSV:

```python
df = pd.read_csv("users.csv")
```

JSON:

```python
df = pd.read_json("users.json")
```

Other formats are supported through additional readers and dependencies.

______________________________________________________________________

# 47. Writing Data

CSV:

```python
df.to_csv("users.csv", index=False)
```

JSON:

```python
df.to_json("users.json")
```

Pandas can therefore be used for simple data transformation pipelines.

______________________________________________________________________

# 48. Typical Pandas Workflow

A common workflow is:

```text
Read
 ↓
Inspect
 ↓
Clean
 ↓
Filter
 ↓
Transform
 ↓
Group/Aggregate
 ↓
Merge
 ↓
Write
```

Example:

```python
df = pd.read_csv("orders.csv")

df = df[df["amount"] > 100]

summary = (
    df.groupby("customer_id")["amount"]
      .sum()
)
```

______________________________________________________________________

# 49. Pandas vs NumPy

| Feature | NumPy | Pandas |
|---|---|---|
| Primary structure | ndarray | Series/DataFrame |
| Main focus | Numerical arrays | Tabular/labeled data |
| Labels | Limited | Built-in |
| Missing data handling | More manual | Rich support |
| GroupBy | Not primary | Core feature |
| Merge/join | Not primary | Core feature |
| Vectorized operations | Yes | Yes |
| Typical use | Numerical computing | Data analysis/manipulation |

Pandas uses NumPy heavily internally, although modern Pandas also supports additional data types and storage mechanisms.

______________________________________________________________________

# 50. Python Lists vs NumPy vs Pandas

A useful mental model:

```text
Python list
→ general-purpose collection

NumPy ndarray
→ numerical array

Pandas DataFrame
→ labeled table
```

Example:

```text
Need to store arbitrary application objects
→ list

Need fast numerical matrix operations
→ NumPy

Need CSV/table-like data processing
→ Pandas
```

______________________________________________________________________

# 51. NumPy/Pandas in Backend Engineering

These libraries are not required for every backend application.

They become useful when backend systems perform:

```text
Data imports
Data exports
Reporting
Batch processing
Analytics
Numerical transformations
ETL-like workflows
```

For ordinary API CRUD:

```text
FastAPI
+
SQLAlchemy
+
PostgreSQL
```

may be more appropriate than introducing Pandas.

______________________________________________________________________

# 52. Example — Backend Data Export

Suppose an API needs to generate a report.

Flow:

```text
FastAPI
   ↓
Database query
   ↓
Pandas DataFrame
   ↓
Transform/group data
   ↓
CSV
   ↓
Object Storage
```

Pandas can be useful for the transformation/reporting stage.

______________________________________________________________________

# 53. Example — Numerical Backend Processing

Suppose an API receives numerical measurements:

```text
temperature readings
```

NumPy can efficiently perform:

```text
Mean
Min/max
Standard deviation
Vectorized transformations
```

Example:

```python
values = np.array(readings)

average = values.mean()
maximum = values.max()
minimum = values.min()
```

______________________________________________________________________

# 54. Avoiding Unnecessary Pandas in APIs

Pandas can consume significant memory for large datasets.

Avoid blindly doing:

```python
SELECT * FROM huge_table
→ DataFrame
```

when the dataset is too large.

Consider:

```text
Database aggregation
Pagination
Chunked processing
Streaming
Batch jobs
```

Push work to the database when the database is better suited for it.

______________________________________________________________________

# 55. NumPy/Pandas and Database Queries

Suppose you need:

```text
Total sales per customer
```

If the database can efficiently perform:

```sql
SELECT customer_id, SUM(amount)
FROM orders
GROUP BY customer_id;
```

there may be little reason to load every row into Pandas just to calculate the same aggregation.

A useful principle:

> **Perform computation where it is most efficient and closest to the data, while considering maintainability and workload.**

______________________________________________________________________

# 56. Memory Considerations

A backend engineer should be aware that:

```text
Database rows
→ Python objects
→ DataFrame
```

can significantly increase memory usage.

This matters for:

```text
Large CSV files
Large database exports
Batch jobs
ETL pipelines
```

For large datasets, process data incrementally when appropriate.

______________________________________________________________________

# 57. Vectorization vs Python Loops

Prefer vectorized operations when appropriate.

Instead of:

```python
df["total"] = [
    price * quantity
    for price, quantity
    in zip(df["price"], df["quantity"])
]
```

you can often write:

```python
df["total"] = df["price"] * df["quantity"]
```

This is simpler and generally better aligned with Pandas' execution model.

______________________________________________________________________

# 58. A Simple End-to-End Example

```python
import pandas as pd

orders = pd.read_csv("orders.csv")

orders["total"] = (
    orders["price"] *
    orders["quantity"]
)

summary = (
    orders
    .groupby("customer_id")["total"]
    .sum()
    .reset_index()
)

summary.to_csv(
    "customer_totals.csv",
    index=False
)
```

Flow:

```text
CSV
 ↓
DataFrame
 ↓
Vectorized calculation
 ↓
GroupBy
 ↓
Aggregation
 ↓
CSV
```

______________________________________________________________________

# 59. Interview Questions & Answers

## Q1. What is NumPy?

**Answer:**

NumPy is a Python library for numerical computing. Its primary data structure is the `ndarray`, which supports efficient
multi-dimensional numerical operations.

______________________________________________________________________

## Q2. What is an `ndarray`?

**Answer:**

It is NumPy's core multi-dimensional array structure. It has properties such as shape, number of dimensions and data
type.

______________________________________________________________________

## Q3. What is `shape`?

**Answer:**

`shape` describes the size of each dimension of an array. For example, `(2, 3)` represents two rows and three columns.

______________________________________________________________________

## Q4. What is `ndim`?

**Answer:**

`ndim` is the number of dimensions of a NumPy array.

______________________________________________________________________

## Q5. What is `dtype`?

**Answer:**

`dtype` specifies the data type used by elements of a NumPy array, such as an integer or floating-point type.

______________________________________________________________________

## Q6. Why is NumPy often faster than Python loops for numerical operations?

**Answer:**

NumPy can execute vectorized operations using optimized low-level implementations rather than repeatedly performing
operations through the Python interpreter.

______________________________________________________________________

## Q7. What is vectorization?

**Answer:**

Vectorization means applying an operation to an entire array or column rather than explicitly iterating over each
element in Python.

______________________________________________________________________

## Q8. What is broadcasting?

**Answer:**

Broadcasting allows NumPy to perform element-wise operations between arrays with compatible shapes, including operations
involving scalars or differently shaped arrays.

______________________________________________________________________

## Q9. What is the difference between a NumPy view and a copy?

**Answer:**

A view can share the same underlying data with the original array, while a copy owns independent data. Modifying a view
can therefore affect the original array.

______________________________________________________________________

## Q10. Why does view vs copy matter?

**Answer:**

It affects memory usage and whether modifying one array can unintentionally modify another array.

______________________________________________________________________

## Q11. What does `reshape()` do?

**Answer:**

It changes the dimensions of an array while preserving its elements, provided the new shape is compatible with the
number of elements.

______________________________________________________________________

## Q12. What is Pandas?

**Answer:**

Pandas is a Python library for manipulating structured and tabular data. Its main structures are Series and DataFrame.

______________________________________________________________________

## Q13. What is a Series?

**Answer:**

A Series is a one-dimensional labeled data structure in Pandas.

______________________________________________________________________

## Q14. What is a DataFrame?

**Answer:**

A DataFrame is a two-dimensional labeled table consisting of rows and columns.

______________________________________________________________________

## Q15. What is the difference between `loc` and `iloc`?

**Answer:**

`loc` performs label-based selection, while `iloc` performs integer-position-based selection.

______________________________________________________________________

## Q16. How do you filter a DataFrame?

**Answer:**

Use a boolean condition:

```python
df[df["age"] > 30]
```

This returns rows matching the condition.

______________________________________________________________________

## Q17. What is `groupby()`?

**Answer:**

`groupby()` groups rows according to one or more keys so that aggregations or transformations can be performed per
group.

______________________________________________________________________

## Q18. What is the mental model for `groupby()`?

**Answer:**

Split the data into groups, apply an operation to each group and combine the results.

______________________________________________________________________

## Q19. How is Pandas `merge()` related to SQL?

**Answer:**

`merge()` combines DataFrames based on matching keys and is conceptually similar to SQL joins such as INNER JOIN and
LEFT JOIN.

______________________________________________________________________

## Q20. What are common Pandas merge types?

**Answer:**

`inner`, `left`, `right` and `outer`.

______________________________________________________________________

## Q21. How do you detect missing values?

**Answer:**

Common methods include:

```python
df.isna()
df.notna()
```

______________________________________________________________________

## Q22. How do you handle missing values?

**Answer:**

Depending on the meaning of the missing data, you can drop rows/columns with `dropna()` or replace values using
`fillna()`. The correct approach is domain-dependent.

______________________________________________________________________

## Q23. What is the difference between NumPy and Pandas?

**Answer:**

NumPy primarily focuses on efficient numerical arrays and operations. Pandas focuses on labeled, tabular data and
provides functionality such as filtering, grouping, joining and missing-value handling.

______________________________________________________________________

## Q24. When would you use Pandas instead of NumPy?

**Answer:**

Use Pandas when the data is naturally tabular and you need operations such as grouping, filtering, joining, labeled
columns or missing-value handling.

______________________________________________________________________

## Q25. When would you use NumPy instead of Pandas?

**Answer:**

Use NumPy when the problem is primarily numerical array or matrix computation and Pandas' tabular abstractions are
unnecessary.

______________________________________________________________________

## Q26. When would you use neither?

**Answer:**

For ordinary application logic and CRUD operations, Python collections and database/ORM tools may be more appropriate.

______________________________________________________________________

## Q27. Should every FastAPI application use Pandas?

**Answer:**

No. Pandas is useful for data manipulation and reporting workloads but can add unnecessary memory and processing
overhead to ordinary API workloads.

______________________________________________________________________

## Q28. Why might loading a huge database table into Pandas be dangerous?

**Answer:**

The resulting DataFrame and associated Python/Pandas structures can consume substantial memory and potentially exhaust
the application's available memory.

______________________________________________________________________

## Q29. Where should aggregation happen: PostgreSQL or Pandas?

**Answer:**

It depends. If the database can efficiently perform the aggregation and only the result is needed, doing it in the
database can avoid transferring large amounts of data to the application. Pandas may be appropriate when more complex
data transformation is required after retrieval.

______________________________________________________________________

## Q30. What is the backend-engineering value of learning NumPy and Pandas?

**Answer:**

They are useful for reading and maintaining data-processing code, generating reports, performing batch transformations,
handling imports/exports and working with numerical or tabular datasets.

______________________________________________________________________

# 60. Practical Questions

## Q1. You have one million numbers and need their average. What would you consider?

**Answer:**

NumPy is a natural option because it is designed for numerical array operations and can perform the aggregation
efficiently.

______________________________________________________________________

## Q2. You have a CSV containing customers and orders and need total spending per customer. What would you consider?

**Answer:**

Pandas is a natural option because the task involves tabular data, grouping and aggregation.

______________________________________________________________________

## Q3. You need to join two CSV datasets on `user_id`. What Pandas operation would you use?

**Answer:**

`merge()`:

```python
result = users.merge(orders, on="user_id")
```

The exact join type depends on the required semantics.

______________________________________________________________________

## Q4. A Pandas DataFrame contains missing email addresses. How do you find them?

**Answer:**

```python
df[df["email"].isna()]
```

______________________________________________________________________

## Q5. You need to select rows where `amount > 100` and `status == "paid"`. How?

**Answer:**

```python
df[
    (df["amount"] > 100) &
    (df["status"] == "paid")
]
```

______________________________________________________________________

## Q6. You need the average salary per department. How?

**Answer:**

```python
df.groupby("department")["salary"].mean()
```

______________________________________________________________________

## Q7. You need multiple statistics per department. How?

**Answer:**

```python
df.groupby("department")["salary"].agg(
    ["count", "mean", "max"]
)
```

______________________________________________________________________

## Q8. A NumPy slice is modified and the original array changes. Why?

**Answer:**

The slice may be a view sharing the original array's underlying memory. Use `.copy()` when an independent array is
required.

______________________________________________________________________

# 61. Practical Backend Guidelines

### Prefer NumPy when:

```text
Numerical arrays
Matrix operations
Vectorized numerical calculations
Statistical calculations
```

### Prefer Pandas when:

```text
CSV/JSON/tabular data
Data cleaning
Grouping
Aggregation
Joining
Reporting
Batch transformations
```

### Prefer the database when:

```text
The operation is naturally SQL
The database can aggregate efficiently
Large amounts of data should not be transferred
Transactional/database constraints matter
```

### Prefer normal Python structures when:

```text
Data is small
Data is application state
No numerical/table processing is required
```

______________________________________________________________________

# 62. Common Mistakes

## Mistake 1 — Assuming Pandas is always faster

Pandas is not automatically the best solution for every data problem.

______________________________________________________________________

## Mistake 2 — Loading everything into memory

Large datasets can exhaust application memory.

______________________________________________________________________

## Mistake 3 — Ignoring views and copies

Unexpected mutations can create difficult bugs.

______________________________________________________________________

## Mistake 4 — Using loops unnecessarily

Prefer vectorized operations when appropriate.

______________________________________________________________________

## Mistake 5 — Filling all missing values with zero

Missing data does not automatically mean zero.

______________________________________________________________________

## Mistake 6 — Doing database aggregation in Python unnecessarily

If SQL can efficiently reduce millions of rows to a small result, consider doing the aggregation in the database.

______________________________________________________________________

# 63. Final Interview Readiness Checklist

## NumPy

- [ ] Explain NumPy.
- [ ] Explain `ndarray`.
- [ ] Explain shape.
- [ ] Explain dimensions.
- [ ] Explain `dtype`.
- [ ] Perform basic indexing.
- [ ] Perform slicing.
- [ ] Use boolean indexing.
- [ ] Explain views vs copies.
- [ ] Explain `reshape`.
- [ ] Explain vectorization.
- [ ] Explain broadcasting.
- [ ] Perform basic array operations.
- [ ] Perform aggregations.
- [ ] Compare NumPy arrays with Python lists.

## Pandas

- [ ] Explain Series.
- [ ] Explain DataFrame.
- [ ] Select columns.
- [ ] Select rows.
- [ ] Explain `loc`.
- [ ] Explain `iloc`.
- [ ] Filter rows.
- [ ] Create derived columns.
- [ ] Explain `groupby`.
- [ ] Perform aggregations.
- [ ] Explain `merge`.
- [ ] Recognize join types.
- [ ] Detect missing values.
- [ ] Handle missing values.
- [ ] Read CSV.
- [ ] Write CSV.
- [ ] Read/write common data formats.
- [ ] Compare Pandas with NumPy.

## Backend Integration

- [ ] Know when NumPy is useful.
- [ ] Know when Pandas is useful.
- [ ] Know when neither is necessary.
- [ ] Understand memory implications.
- [ ] Know when to push aggregation into the database.
- [ ] Understand batch/reporting use cases.
- [ ] Recognize the risks of loading huge datasets into memory.

______________________________________________________________________

# 64. Final Takeaways

Keep this mental model:

```text
Python list
→ General-purpose collection

NumPy ndarray
→ Numerical array

Pandas Series
→ Labeled one-dimensional data

Pandas DataFrame
→ Labeled tabular data
```

And:

```text
NumPy
→ Arrays
→ Vectorization
→ Broadcasting
→ Numerical operations

Pandas
→ Tables
→ Filtering
→ Grouping
→ Aggregation
→ Merge
→ Missing values
→ Data import/export
```

For a backend engineer, the most important decision is not:

> "Can I use Pandas?"

It is:

> **"Where should this data processing happen?"**

For example:

```text
Large SQL aggregation
→ Database

Numerical array processing
→ NumPy

CSV/report transformation
→ Pandas

Simple API CRUD
→ Python + ORM/database
```

Use the tool that matches the workload.

This file intentionally provides only the overview required to understand and discuss NumPy and Pandas in backend
engineering and interviews.

______________________________________________________________________

**Previous:** [41. TypeScript, Angular Overview](./41-typescript-angular.md)

**Next:** [43. Design Patterns & Architecture](./43-design-patterns-architecture.md)
