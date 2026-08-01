# Query Optimization & Execution Plans - Part 2

## Introduction

In Part 1, we learned how a database parses, validates, optimizes, and executes a query. We also explored execution
plans, scan types, and how indexes influence performance.

In this chapter, we'll cover:

- Join Algorithms
- Sorting
- Predicate Pushdown
- SARGable Queries
- Pagination Optimization
- N+1 Query Problem
- SQLAlchemy Optimization
- SQLModel Optimization
- Real-world Performance Tuning
- Interview Tips

These topics are extremely common in senior backend interviews because they demonstrate an understanding of how
databases behave under real production workloads.

______________________________________________________________________

# Join Algorithms

When two tables are joined, the database optimizer chooses an algorithm based on:

- Table size
- Available indexes
- Estimated number of matching rows
- Available memory
- Statistics

The three most common join algorithms are:

- Nested Loop Join
- Hash Join
- Merge Join

The optimizer—not the developer—usually chooses the algorithm automatically.

______________________________________________________________________

# Nested Loop Join

The simplest join algorithm.

For every row in the outer table, the database searches the inner table for matching rows.

Conceptually:

```text id="4kzvsm"
Employee 1
      ↓
Search Department

Employee 2
      ↓
Search Department

Employee 3
      ↓
Search Department
```

______________________________________________________________________

## Best Use Cases

Nested Loop Join performs well when:

- One table is small.
- An index exists on the join column.
- Few rows are expected.

Example

```sql id="r5y2s8"
SELECT
    e.name,
    d.department_name
FROM employees e
JOIN departments d
ON e.department_id = d.department_id;
```

If `departments.department_id` is indexed, Nested Loop can be very efficient.

______________________________________________________________________

# Hash Join

Hash Join is commonly used for equality joins.

Steps:

1. Build a hash table from the smaller input.
1. Scan the larger table.
1. Probe the hash table for matches.

Conceptually:

```text id="4o7kwr"
Departments

↓

Build Hash Table

↓

Employees

↓

Lookup Matching Department
```

______________________________________________________________________

## Best Use Cases

Hash Join is efficient when:

- Joining large tables.
- Equality comparisons (`=`).
- No useful index exists.
- Enough memory is available.

Hash Join is frequently chosen by PostgreSQL.

______________________________________________________________________

# Merge Join

Merge Join requires both inputs to be sorted by the join key.

The database scans both tables simultaneously.

Conceptually:

```text id="j63sph"
Employees (Sorted)

↓

Departments (Sorted)

↓

Walk Both Together
```

______________________________________________________________________

## Best Use Cases

Merge Join performs well when:

- Inputs are already sorted.
- Indexes provide ordered access.
- Large datasets are joined.

______________________________________________________________________

# Comparing Join Algorithms

| Join Type | Best For | Requires Index |
| ----------- | -------------------- | ---------------- |
| Nested Loop | Small lookups | Often beneficial |
| Hash Join | Large equality joins | No |
| Merge Join | Sorted inputs | Usually helpful |

Interview Tip:

Do **not** try to force a join algorithm unless there is a strong reason. The optimizer usually makes the best choice.

______________________________________________________________________

# Sort Operations

Sorting can be expensive.

Example

```sql id="cvcf5v"
SELECT *
FROM employees
ORDER BY salary DESC;
```

If an index on `salary` exists, the database may avoid an explicit sort.

Otherwise, it performs a sorting operation.

Sorting large datasets may require additional memory or temporary disk space.

______________________________________________________________________

# Predicate Pushdown

Predicate Pushdown means filtering data as early as possible.

Example

Less efficient:

```sql id="m8n7fi"
SELECT *
FROM employees
WHERE department_id = 2;
```

Suppose another operation processes all employees before filtering.

A better execution plan pushes the filter closer to the table scan so fewer rows are processed by later operators.

Although modern optimizers often do this automatically, writing clear queries helps.

______________________________________________________________________

# SARGable Queries

SARGable stands for **Search ARGument Able**.

A SARGable query allows the optimizer to use an index efficiently.

Good example

```sql id="f54r7y"
SELECT *
FROM employees
WHERE salary > 80000;
```

If `salary` is indexed, the optimizer can use the index.

______________________________________________________________________

## Non-SARGable Query

```sql id="rphj7w"
SELECT *
FROM employees
WHERE salary + 1000 > 81000;
```

The database must evaluate the expression for every row.

The index on `salary` cannot usually be used efficiently.

Rewrite it as:

```sql id="2uqzj4"
SELECT *
FROM employees
WHERE salary > 80000;
```

______________________________________________________________________

## Another Example

Less efficient:

```sql id="kj2twb"
SELECT *
FROM employees
WHERE UPPER(name) = 'ALICE';
```

Better:

Store normalized data when appropriate, or use database features such as functional indexes (where supported) if
case-insensitive searches are common.

______________________________________________________________________

# Covering Indexes

Suppose an index exists on:

```text id="3x6fy0"
(employee_id, salary)
```

Query

```sql id="d2nn66"
SELECT
employee_id,
salary
FROM employees
WHERE employee_id = 5;
```

The database may satisfy the query entirely from the index.

Benefits:

- Fewer page reads
- Faster execution
- Reduced I/O

______________________________________________________________________

# Pagination

A common interview topic.

Basic pagination

```sql id="o6dcgw"
SELECT *
FROM employees
ORDER BY employee_id
LIMIT 20 OFFSET 1000;
```

Problem:

Large offsets become slower because many rows must still be processed before returning the requested page.

______________________________________________________________________

# Keyset Pagination

Instead of OFFSET:

```sql id="ljs2jv"
SELECT *
FROM employees
WHERE employee_id > 1000
ORDER BY employee_id
LIMIT 20;
```

Advantages:

- More efficient on large datasets
- Stable results when rows are inserted or deleted
- Preferred for APIs and infinite scrolling

Interview Tip:

For very large tables, keyset pagination is usually preferable to deep OFFSET pagination.

______________________________________________________________________

# N+1 Query Problem

A classic ORM interview question.

Bad approach:

```text id="5otjlwm"
Load Employees

↓

For each Employee

↓

Load Department
```

If there are 100 employees:

```text id="jlwm5p"
1 + 100 Queries
```

This is the N+1 Query Problem.

______________________________________________________________________

## Better Approach

Retrieve everything in one query.

```sql id="jlwm5q"
SELECT
e.name,
d.department_name
FROM employees e
JOIN departments d
ON e.department_id = d.department_id;
```

______________________________________________________________________

# SQLAlchemy Optimization

### Select Only Required Columns

Instead of:

```python id="jlwm5r"
stmt = select(Employee)
```

Prefer:

```python id="jlwm5s"
stmt = select(
    Employee.employee_id,
    Employee.name
)
```

______________________________________________________________________

### Avoid N+1

Use eager loading when appropriate.

```python id="jlwm5t"
from sqlalchemy.orm import joinedload

stmt = (
    select(Employee)
    .options(
        joinedload(Employee.department)
    )
)
```

Other loading strategies include `selectinload()` and `subqueryload()`. Choosing the right one depends on the
relationship and query pattern.

______________________________________________________________________

### Batch Inserts

Instead of inserting rows one by one:

```python id="jlwm5u"
for employee in employees:
    session.add(employee)
```

Prefer batching when appropriate.

```python id="jlwm5v"
session.add_all(employees)
session.commit()
```

For very large imports, SQLAlchemy also provides bulk operations, though they come with trade-offs.

______________________________________________________________________

# SQLModel Optimization

The same optimization principles apply because SQLModel uses SQLAlchemy internally.

Focus on:

- Efficient filtering
- Proper joins
- Eager loading when appropriate
- Avoiding unnecessary object loading

______________________________________________________________________

# Reading an Execution Plan

Example

```text id="jlwm5w"
Index Scan

↓

Nested Loop

↓

Sort

↓

Output
```

Interpretation:

1. Read rows using an index.
1. Join tables using Nested Loop.
1. Sort the result.
1. Return rows.

Understanding execution plans is more valuable than memorizing optimizer internals.

______________________________________________________________________

# Real-world Optimization Example

Original query

```sql id="jlwm5x"
SELECT *
FROM employees
WHERE department_id = 2
ORDER BY salary;
```

Improvements:

- Select only required columns.
- Add an index on `(department_id, salary)` if this query is common.
- Verify the new execution plan using `EXPLAIN ANALYZE`.
- Measure performance before and after.

______________________________________________________________________

# Common Mistakes

### Adding Indexes Without Measuring

Indexes improve some queries and slow down writes.

Always validate with execution plans.

______________________________________________________________________

### Ignoring Execution Plans

Never assume.

Inspect the optimizer's decisions.

______________________________________________________________________

### Using OFFSET for Deep Pagination

Large offsets become increasingly expensive.

Consider keyset pagination.

______________________________________________________________________

### Loading Entire Objects

Retrieve only the data required.

______________________________________________________________________

### Premature Optimization

Optimize after identifying real bottlenecks.

______________________________________________________________________

# Best Practices

- Measure before optimizing.
- Read execution plans.
- Keep statistics current.
- Design indexes around real query patterns.
- Prefer SARGable predicates.
- Avoid unnecessary sorting.
- Eliminate N+1 queries.
- Benchmark changes before deploying.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you optimize a slow SQL query?

I would first inspect the execution plan using `EXPLAIN` or `EXPLAIN ANALYZE` to identify bottlenecks such as sequential
scans, expensive joins, or sorts. Next, I'd verify whether appropriate indexes exist, rewrite non-SARGable predicates if
necessary, reduce unnecessary columns, and ensure filters are applied efficiently. After making changes, I'd compare
execution plans and benchmark the new query to confirm that performance has improved.

______________________________________________________________________

# Practice Questions

## Conceptual

1. Explain Nested Loop Join.
1. Explain Hash Join.
1. Explain Merge Join.
1. What is Predicate Pushdown?
1. What is a SARGable query?
1. Why is OFFSET pagination slow?
1. What is the N+1 Query Problem?
1. Why should execution plans be inspected before optimizing?

## Coding

1. Optimize a query using an index.
1. Rewrite a non-SARGable predicate.
1. Replace OFFSET pagination with keyset pagination.
1. Compare execution plans before and after adding an index.
1. Eliminate an N+1 query using SQLAlchemy eager loading.

______________________________________________________________________

# Hands-on Exercise

Using the Employees and Departments tables:

1. Create indexes on frequently filtered columns.
1. Compare execution plans before and after indexing.
1. Rewrite non-SARGable queries.
1. Compare OFFSET pagination with keyset pagination.
1. Eliminate an N+1 problem using SQLAlchemy.
1. Rewrite applicable examples using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text id="jlwm5y"
Join Algorithms

Nested Loop
Hash Join
Merge Join

↓

Optimization

EXPLAIN
EXPLAIN ANALYZE

↓

SARGable Queries

↓

Indexes

↓

Keyset Pagination

↓

Avoid N+1
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Nested Loop Join
- Hash Join
- Merge Join
- Sort operations
- Predicate Pushdown
- SARGable queries
- Covering indexes
- Pagination optimization
- Keyset pagination
- N+1 Query Problem
- SQLAlchemy optimization
- SQLModel optimization
- Reading execution plans
- Real-world optimization strategies
- Performance best practices

You now have a strong understanding of how modern relational databases execute and optimize queries, and how to reason
about performance in production systems and technical interviews.

______________________________________________________________________

## Next File

[Transactions, Locking & Concurrency](10-transactions-locking-concurrency.md)
