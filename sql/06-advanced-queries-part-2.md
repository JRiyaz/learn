# Advanced Queries - Part 2

## Introduction

In Part 1, we covered:

- Scalar Subqueries
- Multi-row Subqueries
- Correlated Subqueries
- EXISTS
- NOT EXISTS
- ANY
- ALL

In this chapter, we'll cover:

- Common Table Expressions (CTEs)
- Recursive CTEs
- UNION
- UNION ALL
- INTERSECT
- EXCEPT

These features make SQL queries more readable, reusable, and expressive. They are frequently tested in senior backend
interviews.

______________________________________________________________________

# Common Table Expression (CTE)

A **Common Table Expression (CTE)** is a named temporary result set that exists only for the duration of a single SQL
statement.

A CTE improves readability by breaking a complex query into logical steps.

General syntax:

```sql
WITH cte_name AS (
    SELECT ...
)
SELECT ...
FROM cte_name;
```

______________________________________________________________________

# Why Use a CTE?

Without a CTE, complex queries often contain deeply nested subqueries.

Example without a CTE:

```sql
SELECT department_id, average_salary
FROM (
    SELECT
        department_id,
        AVG(salary) AS average_salary
    FROM employees
    GROUP BY department_id
) AS dept_stats;
```

The same query using a CTE:

```sql
WITH department_stats AS (
    SELECT
        department_id,
        AVG(salary) AS average_salary
    FROM employees
    GROUP BY department_id
)
SELECT
    department_id,
    average_salary
FROM department_stats;
```

The CTE version is easier to read and maintain.

______________________________________________________________________

# Multiple CTEs

A query can define multiple CTEs.

```sql
WITH department_salary AS (
    SELECT
        department_id,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
),
employee_count AS (
    SELECT
        department_id,
        COUNT(*) AS total_employees
    FROM employees
    GROUP BY department_id
)
SELECT
    ds.department_id,
    ds.avg_salary,
    ec.total_employees
FROM department_salary ds
JOIN employee_count ec
ON ds.department_id = ec.department_id;
```

______________________________________________________________________

# SQLAlchemy Equivalent

```python
from sqlalchemy import select, func

department_stats = (
    select(
        Employee.department_id,
        func.avg(Employee.salary).label("average_salary")
    )
    .group_by(Employee.department_id)
    .cte("department_stats")
)

stmt = select(department_stats)
```

______________________________________________________________________

# SQLModel Equivalent

SQLModel uses SQLAlchemy internally, so the same `.cte()` method is available.

______________________________________________________________________

# Recursive CTE

A Recursive CTE references itself.

It is useful for hierarchical data such as:

- Employee → Manager
- Folder → Subfolder
- Categories
- Organization charts
- Bill of Materials

Recursive CTEs have two parts:

1. Anchor Query
1. Recursive Query

______________________________________________________________________

# Example

Employees

| employee_id | name | manager_id |
| ----------: | ------- | ---------: |
| 1 | Alice | NULL |
| 2 | Bob | 1 |
| 3 | Charlie | 2 |
| 4 | David | 3 |

Retrieve the entire management hierarchy.

```sql
WITH RECURSIVE employee_hierarchy AS (

    SELECT
        employee_id,
        name,
        manager_id,
        1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.employee_id,
        e.name,
        e.manager_id,
        eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh
        ON e.manager_id = eh.employee_id
)

SELECT *
FROM employee_hierarchy;
```

Result

| Employee | Level |
| -------- | ----: |
| Alice | 1 |
| Bob | 2 |
| Charlie | 3 |
| David | 4 |

______________________________________________________________________

# UNION

`UNION` combines results from two queries and removes duplicate rows.

Rules:

- Same number of columns
- Compatible data types
- Same logical meaning

Example

```sql
SELECT city
FROM customers

UNION

SELECT city
FROM suppliers;
```

Duplicate cities appear only once.

______________________________________________________________________

# UNION ALL

`UNION ALL` combines results without removing duplicates.

```sql
SELECT city
FROM customers

UNION ALL

SELECT city
FROM suppliers;
```

This is generally faster than `UNION` because SQL does not perform duplicate elimination.

______________________________________________________________________

# UNION vs UNION ALL

| UNION | UNION ALL |
| ------------------------ | ------------------------ |
| Removes duplicates | Keeps duplicates |
| Slower | Faster |
| Uses DISTINCT internally | No duplicate elimination |

Interview tip:

Prefer `UNION ALL` when duplicates are acceptable.

______________________________________________________________________

# INTERSECT

Returns only rows common to both queries.

Example

```sql
SELECT city
FROM customers

INTERSECT

SELECT city
FROM suppliers;
```

Result

Only cities that appear in both tables.

______________________________________________________________________

# EXCEPT

Returns rows from the first query that do **not** appear in the second.

```sql
SELECT city
FROM customers

EXCEPT

SELECT city
FROM suppliers;
```

Useful for finding missing records.

______________________________________________________________________

# SQLAlchemy Set Operations

```python
from sqlalchemy import union, union_all, intersect, except_

query1 = select(Customer.city)
query2 = select(Supplier.city)

stmt = union(query1, query2)

stmt = union_all(query1, query2)

stmt = intersect(query1, query2)

stmt = except_(query1, query2)
```

______________________________________________________________________

# SQLModel

SQLModel uses the same SQLAlchemy functions for set operations.

______________________________________________________________________

# CTE vs Subquery

Interview question.

| CTE | Subquery |
| -------------------------------- | --------------------------------- |
| Named | Anonymous |
| Easier to read | Can become deeply nested |
| Can be referenced multiple times | Repeated if needed multiple times |
| Supports recursion | No recursion |

A CTE does **not** automatically make a query faster. It primarily improves readability and maintainability. Query
optimizers may inline CTEs depending on the database and version.

______________________________________________________________________

# EXISTS vs JOIN

Another interview favorite.

Suppose we want departments that have employees.

Using EXISTS:

```sql
SELECT department_name
FROM departments d
WHERE EXISTS (
    SELECT 1
    FROM employees e
    WHERE e.department_id = d.department_id
);
```

Using JOIN:

```sql
SELECT DISTINCT
    d.department_name
FROM departments d
JOIN employees e
ON d.department_id = e.department_id;
```

Discussion:

- `EXISTS` expresses an existence check directly.
- `JOIN` combines rows and may require `DISTINCT` to remove duplicates.
- The optimizer may produce similar execution plans, but choose the construct that best expresses the intent.

______________________________________________________________________

# Performance Considerations

## Subqueries

- Simple scalar subqueries are usually efficient.
- Correlated subqueries may execute repeatedly unless optimized.

## CTEs

- Improve readability.
- Can simplify debugging.
- Do not assume performance gains.

## UNION

Removing duplicates requires additional work.

Prefer `UNION ALL` when duplicate removal is unnecessary.

## EXISTS

Excellent for existence checks because the database can stop searching after finding the first match.

______________________________________________________________________

# Common Mistakes

### Using UNION instead of UNION ALL

If duplicates are acceptable, `UNION ALL` is faster.

______________________________________________________________________

### Forgetting Recursive Termination

Recursive CTEs must eventually stop.

Otherwise, they can recurse indefinitely or until database limits are reached.

______________________________________________________________________

### Different Column Counts

This is invalid:

```sql
SELECT employee_id
FROM employees

UNION

SELECT department_id, department_name
FROM departments;
```

Both queries must return the same number of columns.

______________________________________________________________________

### Incompatible Data Types

Ensure corresponding columns have compatible data types.

______________________________________________________________________

# Best Practices

- Prefer CTEs for complex logic.
- Use meaningful CTE names.
- Choose `UNION ALL` unless duplicate removal is required.
- Use `EXISTS` for existence checks.
- Test recursive queries with small datasets first.
- Compare execution plans when optimizing.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between a CTE and a subquery?

A CTE is a named temporary result set that exists only for the duration of a single SQL statement. It improves
readability, can be referenced multiple times, and supports recursion. A subquery is anonymous and embedded directly
within another query. Both can solve similar problems, but CTEs are often easier to understand and maintain.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a CTE?
1. What is a Recursive CTE?
1. Explain `UNION`.
1. Explain `UNION ALL`.
1. Explain `INTERSECT`.
1. Explain `EXCEPT`.
1. When would you choose `UNION ALL` instead of `UNION`?
1. When would you prefer `EXISTS` over a `JOIN`?

## Coding

1. Write a CTE to calculate average salary by department.
1. Rewrite a nested subquery using a CTE.
1. Build an employee hierarchy using a recursive CTE.
1. Find common cities using `INTERSECT`.
1. Find cities present only in the customer table using `EXCEPT`.
1. Combine two result sets using both `UNION` and `UNION ALL` and explain the difference.

______________________________________________________________________

# Hands-on Exercise

Using the Employees and Departments tables:

1. Create a CTE for department statistics.
1. Rewrite the query without a CTE.
1. Write a recursive employee-manager hierarchy.
1. Compare `UNION` and `UNION ALL`.
1. Solve one problem using `EXISTS` and another using a `JOIN`.
1. Rewrite applicable examples using SQLAlchemy.
1. Rewrite applicable examples using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text
Subquery
→ Query inside another query

CTE
→ Named temporary result set

Recursive CTE
→ Hierarchical queries

UNION
→ Removes duplicates

UNION ALL
→ Keeps duplicates

INTERSECT
→ Common rows

EXCEPT
→ Rows only in first query
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Common Table Expressions (CTEs)
- Multiple CTEs
- Recursive CTEs
- UNION
- UNION ALL
- INTERSECT
- EXCEPT
- CTE vs Subquery
- EXISTS vs JOIN
- SQLAlchemy equivalents
- SQLModel equivalents
- Performance considerations
- Interview patterns
- Best practices

You now have a solid understanding of advanced SQL query construction, from reusable query blocks to recursive
hierarchies and set operations.

______________________________________________________________________

## Next File

[Window Functions](07-window-functions.md)
