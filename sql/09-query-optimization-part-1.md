# Query Optimization & Execution Plans - Part 1

## Introduction

Writing a SQL query that returns the correct result is only half the job.

The other half is ensuring that it runs **efficiently**.

Consider the following scenarios:

- A query returns results in **5 milliseconds**.
- The same query on a production database takes **30 seconds**.
- A report that worked yesterday suddenly becomes slow after the data grows.

Why does this happen?

The answer lies in **query optimization**.

Query optimization is one of the most important topics for backend engineers because databases spend most of their time
executing queries—not parsing SQL.

A well-written query combined with proper indexing can reduce execution time from minutes to milliseconds.

______________________________________________________________________

# What is Query Optimization?

Query optimization is the process of executing a SQL query in the most efficient way possible.

The database optimizer attempts to determine:

- Which indexes to use
- Which join algorithm to choose
- Which table should be scanned first
- Whether sorting can be avoided
- Whether filtering can happen earlier

The optimizer generates an **Execution Plan**, which describes how the database intends to execute the query.

______________________________________________________________________

# SQL Query Lifecycle

When a SQL query is submitted, the database does not execute it immediately.

It goes through several stages.

```text id="wd4ncp"
SQL Query

↓

Parser

↓

Validator

↓

Query Optimizer

↓

Execution Plan

↓

Execution Engine

↓

Results
```

______________________________________________________________________

# Parser

The parser checks whether the SQL statement is syntactically correct.

Example

```sql id="53j3wo"
SELECT *
FROM employees;
```

Valid.

Example

```sql id="tgb3lh"
SELEC *
FROM employees;
```

Produces a syntax error.

______________________________________________________________________

# Validator

The validator checks:

- Does the table exist?
- Do the referenced columns exist?
- Does the user have permission?

Example

```sql id="bjlwm0"
SELECT salary
FROM employees;
```

Valid.

Example

```sql id="jlwm1a"
SELECT annual_salary
FROM employees;
```

Produces an "unknown column" error.

______________________________________________________________________

# Query Optimizer

The optimizer is often called the **brain of the database**.

Given multiple ways to execute a query, it estimates the cost of each one and chooses the cheapest plan.

Example

```sql id="jlwm1b"
SELECT *
FROM employees
WHERE employee_id = 10;
```

Possible strategies:

```text id="jlwm1c"
Option 1

Sequential Scan

↓

Cost = High

--------------------

Option 2

Primary Key Index

↓

Cost = Very Low
```

The optimizer normally chooses the second option.

______________________________________________________________________

# What is an Execution Plan?

An execution plan describes **how** the database will execute a query.

It is not the query result.

Instead, it shows:

- Scan method
- Join method
- Estimated rows
- Estimated cost
- Sort operations
- Filters
- Index usage

Understanding execution plans is one of the most valuable SQL interview skills.

______________________________________________________________________

# EXPLAIN

`EXPLAIN` shows the execution plan without executing the query.

Example

```sql id="jlwm1d"
EXPLAIN
SELECT *
FROM employees
WHERE employee_id = 10;
```

Typical PostgreSQL output

```text id="jlwm1e"
Index Scan

Cost

Rows

Width
```

The exact output differs across database engines.

______________________________________________________________________

# EXPLAIN ANALYZE

`EXPLAIN ANALYZE` executes the query and shows the **actual** execution statistics.

Example

```sql id="jlwm1f"
EXPLAIN ANALYZE
SELECT *
FROM employees
WHERE employee_id = 10;
```

Additional information includes:

- Actual execution time
- Actual rows processed
- Loops
- Buffers (database-dependent)

This is one of the first tools used when investigating slow queries.

> **Caution:** Because `EXPLAIN ANALYZE` executes the query, avoid using it carelessly on expensive `UPDATE`, `DELETE`, or `INSERT` statements in production.

______________________________________________________________________

# Understanding Cost

Execution plans contain **cost estimates**.

Example

```text id="jlwm1g"
cost=0.29..8.30
```

These are **relative planner units**, not milliseconds.

The optimizer compares costs to choose the cheapest execution strategy.

Lower estimated cost generally indicates a more efficient plan.

______________________________________________________________________

# Sequential Scan

A Sequential Scan reads every row in the table.

Example

```sql id="jlwm1h"
SELECT *
FROM employees
WHERE city = 'Bangalore';
```

If no suitable index exists, the database may scan every row.

Conceptually

```text id="jlwm1i"
Row 1

↓

Row 2

↓

Row 3

↓

...

↓

Row N
```

______________________________________________________________________

# When is Sequential Scan Good?

Many developers think sequential scans are always bad.

They are not.

A Sequential Scan is often the best choice when:

- The table is very small.
- Most rows are required.
- Using an index would require many random reads.

Interview Tip:

**A Sequential Scan is not automatically a performance problem.**

______________________________________________________________________

# Index Scan

An Index Scan uses an index to locate matching rows.

Example

```sql id="jlwm1j"
SELECT *
FROM employees
WHERE employee_id = 25;
```

If `employee_id` is indexed:

```text id="jlwm1k"
Index

↓

Matching Key

↓

Matching Row
```

This avoids scanning the entire table.

______________________________________________________________________

# When is an Index Scan Used?

Usually when:

- Filtering on indexed columns.
- Returning a small percentage of rows.
- Looking up primary keys.
- Performing selective joins.

______________________________________________________________________

# Index Only Scan

Sometimes the database can answer a query using only the index.

Example

Suppose an index exists on:

```text id="jlwm1l"
(employee_id, salary)
```

Query

```sql id="jlwm1m"
SELECT employee_id, salary
FROM employees
WHERE employee_id = 10;
```

Since both requested columns exist in the index, the database may avoid reading the table entirely.

This is known as an **Index Only Scan**.

______________________________________________________________________

# Bitmap Index Scan

A Bitmap Index Scan is commonly used when many rows match an indexed condition.

Conceptually:

```text id="jlwm1n"
Index

↓

Bitmap of Matching Rows

↓

Read Table Pages Efficiently
```

Bitmap scans reduce random disk access when many matching rows are spread across the table.

______________________________________________________________________

# Comparing Scan Types

| Scan Type | Best Use Case |
| ----------------- | --------------------------------------- |
| Sequential Scan | Small tables or large result sets |
| Index Scan | Highly selective queries |
| Index Only Scan | All required columns exist in the index |
| Bitmap Index Scan | Many matching indexed rows |

______________________________________________________________________

# Statistics and the Optimizer

The optimizer relies on table statistics.

Statistics include information such as:

- Approximate row count
- Value distribution
- NULL fraction
- Distinct values

Outdated statistics can lead to poor execution plans.

In PostgreSQL, statistics are refreshed by `ANALYZE` (or automatically through autovacuum).

______________________________________________________________________

# SQLAlchemy Performance Tip

Select only required columns.

Avoid

```python id="jlwm1o"
stmt = select(Employee)
```

Prefer

```python id="jlwm1p"
stmt = select(
    Employee.employee_id,
    Employee.name
)
```

Fetching unnecessary columns increases network and memory usage.

______________________________________________________________________

# SQLModel Performance Tip

The same principle applies.

Retrieve only the columns you actually need whenever possible.

______________________________________________________________________

# Common Mistakes

### Assuming Indexes Are Always Used

The optimizer may intentionally choose a Sequential Scan.

______________________________________________________________________

### Ignoring Execution Plans

Never guess.

Verify using `EXPLAIN` or `EXPLAIN ANALYZE`.

______________________________________________________________________

### Using SELECT \*

Fetching unnecessary columns increases I/O.

______________________________________________________________________

### Optimizing Before Measuring

Always identify the bottleneck before changing indexes or rewriting queries.

______________________________________________________________________

# Best Practices

- Examine execution plans before optimizing.
- Keep table statistics up to date.
- Index frequently filtered columns.
- Retrieve only required columns.
- Measure performance using actual execution plans.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Is a Sequential Scan always bad?

No. A Sequential Scan is often the fastest option for small tables or queries that return a large percentage of rows.
Using an index in these situations may require many random page reads, making it slower than scanning the table
sequentially. The optimizer chooses the plan with the lowest estimated cost based on available statistics.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is query optimization?
1. What is an execution plan?
1. What is the difference between `EXPLAIN` and `EXPLAIN ANALYZE`?
1. What is a Sequential Scan?
1. What is an Index Scan?
1. What is an Index Only Scan?
1. When is a Sequential Scan preferable?

## Coding

1. View the execution plan for a primary key lookup.
1. Compare plans before and after creating an index.
1. Observe the difference between `EXPLAIN` and `EXPLAIN ANALYZE`.
1. Identify whether a query performs a Sequential Scan or an Index Scan.

______________________________________________________________________

# Hands-on Exercise

1. Create an `employees` table with at least 100,000 rows.
1. Query using a non-indexed column and inspect the execution plan.
1. Create an index and compare the new plan.
1. Compare `SELECT *` with selecting only required columns.
1. Rewrite applicable examples using SQLAlchemy and SQLModel.

______________________________________________________________________

# Cheat Sheet

```text id="jlwm1q"
SQL Query

↓

Parser

↓

Validator

↓

Optimizer

↓

Execution Plan

↓

Execution

Scans

Sequential Scan
Index Scan
Index Only Scan
Bitmap Index Scan
```

______________________________________________________________________

# Summary

In this part, you learned:

- Query optimization
- SQL query lifecycle
- Execution plans
- EXPLAIN
- EXPLAIN ANALYZE
- Cost estimates
- Sequential Scan
- Index Scan
- Index Only Scan
- Bitmap Index Scan
- Optimizer statistics
- Performance best practices

In the next part, we'll cover **Nested Loop, Hash Join, Merge Join, Sorting, Predicate Pushdown, SARGable Queries,
Pagination Optimization, the N+1 Query Problem, SQLAlchemy optimization, and real-world interview case studies.**

______________________________________________________________________

## Next File

[Query Optimization & Execution Plans - Part 2](09-query-optimization-part-2.md)
