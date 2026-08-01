# Advanced Queries - Part 1

## Introduction

By now, you can:

- Retrieve data
- Filter data
- Join multiple tables
- Aggregate data

The next step is writing **advanced SQL queries**.

These queries are extremely common in software engineering interviews because they test your ability to solve complex
data retrieval problems without writing procedural code.

In this chapter, we'll cover:

- Subqueries
- Correlated Subqueries
- EXISTS
- NOT EXISTS
- ANY
- ALL

The remaining advanced topics—CTEs, Recursive CTEs, and Set Operations—will be covered in Part 2.

______________________________________________________________________

# Sample Database

## Employees

| employee_id | name | department_id | salary |
| ----------- | ------- | ------------: | -----: |
| 1 | Alice | 1 | 60000 |
| 2 | Bob | 2 | 85000 |
| 3 | Charlie | 2 | 90000 |
| 4 | David | 3 | 75000 |
| 5 | Eva | 1 | 65000 |
| 6 | Frank | 3 | 95000 |

## Departments

| department_id | department_name |
| ------------: | --------------- |
| 1 | HR |
| 2 | Engineering |
| 3 | Finance |

______________________________________________________________________

# What is a Subquery?

A **subquery** is a query written inside another query.

The inner query executes first.

Its result is then used by the outer query.

General syntax

```sql
SELECT ...
FROM table
WHERE column OPERATOR (
    SELECT ...
);
```

A subquery can appear in:

- SELECT
- FROM
- WHERE
- HAVING

______________________________________________________________________

# Single-Row Subquery

Find employees earning more than the average salary.

```sql
SELECT
    name,
    salary
FROM employees
WHERE salary >
(
    SELECT AVG(salary)
    FROM employees
);
```

Execution order

```text
Calculate average salary

↓

Return average

↓

Compare every employee salary

↓

Return matching rows
```

______________________________________________________________________

# Multi-Row Subquery

Find employees working in HR or Finance.

```sql
SELECT
    name
FROM employees
WHERE department_id IN
(
    SELECT department_id
    FROM departments
    WHERE department_name IN ('HR', 'Finance')
);
```

The subquery returns multiple department IDs.

______________________________________________________________________

# Subquery in SELECT

A subquery can produce a value for every returned row.

Example

```sql
SELECT
    name,
    salary,
    (
        SELECT AVG(salary)
        FROM employees
    ) AS average_salary
FROM employees;
```

Result

| Name | Salary | Average Salary |
| ----- | -----: | -------------: |
| Alice | 60000 | 78333.33 |
| Bob | 85000 | 78333.33 |

The average salary appears for every row.

______________________________________________________________________

# Subquery in FROM

A subquery can act as a temporary table.

```sql
SELECT
    department_id,
    average_salary
FROM
(
    SELECT
        department_id,
        AVG(salary) AS average_salary
    FROM employees
    GROUP BY department_id
) AS department_stats;
```

This technique is called a **derived table**.

______________________________________________________________________

# SQLAlchemy Equivalent

Single-row subquery

```python
from sqlalchemy import select, func

avg_salary = (
    select(func.avg(Employee.salary))
    .scalar_subquery()
)

stmt = (
    select(Employee)
    .where(Employee.salary > avg_salary)
)
```

______________________________________________________________________

# SQLModel Equivalent

```python
from sqlmodel import select
from sqlalchemy import func

avg_salary = (
    select(func.avg(Employee.salary))
    .scalar_subquery()
)

statement = (
    select(Employee)
    .where(Employee.salary > avg_salary)
)
```

______________________________________________________________________

# Correlated Subquery

A correlated subquery references a column from the outer query.

Unlike a normal subquery, it executes once **for each row** of the outer query.

Example

Find employees earning more than the average salary in their own department.

```sql
SELECT
    e.name,
    e.salary
FROM employees e
WHERE salary >
(
    SELECT AVG(salary)
    FROM employees
    WHERE department_id = e.department_id
);
```

Notice:

```sql
e.department_id
```

belongs to the outer query.

This makes the subquery correlated.

______________________________________________________________________

# Normal vs Correlated Subquery

| Normal | Correlated |
| -------------------- | ---------------------------- |
| Executes once | Executes for every outer row |
| Faster in many cases | Can be slower |
| Independent | Depends on outer query |

______________________________________________________________________

# EXISTS

`EXISTS` checks whether a subquery returns **at least one row**.

If yes:

```text
TRUE
```

Otherwise

```text
FALSE
```

Example

Find departments having employees.

```sql
SELECT
    department_name
FROM departments d
WHERE EXISTS
(
    SELECT 1
    FROM employees e
    WHERE e.department_id = d.department_id
);
```

The value `1` is conventional. SQL only checks whether a row exists—it does not use the returned value.

______________________________________________________________________

# Why SELECT 1?

Interview question.

These are equivalent:

```sql
SELECT 1
```

```sql
SELECT *
```

```sql
SELECT employee_id
```

With `EXISTS`, the selected columns are ignored.

Using `SELECT 1` clearly communicates that only existence matters.

______________________________________________________________________

# NOT EXISTS

Returns rows where the subquery returns **no rows**.

Example

Find departments without employees.

```sql
SELECT
    department_name
FROM departments d
WHERE NOT EXISTS
(
    SELECT 1
    FROM employees e
    WHERE e.department_id = d.department_id
);
```

This is often preferable to `NOT IN` when NULL values may be present.

______________________________________________________________________

# EXISTS vs IN

Both can solve similar problems, but they are not identical.

| EXISTS | IN |
| -------------------------------------- | ---------------------------------- |
| Checks for row existence | Checks membership |
| Often efficient for correlated queries | Good for small lookup sets |
| Stops after first match | Compares against entire result set |

Modern query optimizers often rewrite these internally, but understanding the semantics is important for interviews.

______________________________________________________________________

# ANY

`ANY` compares a value against **any value** returned by a subquery.

Example

Employees earning more than at least one HR employee.

```sql
SELECT
    name,
    salary
FROM employees
WHERE salary > ANY
(
    SELECT salary
    FROM employees
    WHERE department_id = 1
);
```

If the condition is true for at least one returned value, the row is included.

______________________________________________________________________

# ALL

`ALL` compares a value against **every value** returned by a subquery.

Example

Employees earning more than every HR employee.

```sql
SELECT
    name,
    salary
FROM employees
WHERE salary > ALL
(
    SELECT salary
    FROM employees
    WHERE department_id = 1
);
```

This is much stricter than `ANY`.

______________________________________________________________________

# SQLAlchemy Example (EXISTS)

```python
from sqlalchemy import exists, select

stmt = (
    select(Department)
    .where(
        exists(
            select(1).where(
                Employee.department_id ==
                Department.department_id
            )
        )
    )
)
```

______________________________________________________________________

# Common Mistakes

### Using `=` instead of `IN`

Incorrect

```sql
WHERE department_id =
(
    SELECT department_id
    FROM departments
)
```

If the subquery returns multiple rows, this produces an error.

Use `IN` instead.

______________________________________________________________________

### Confusing EXISTS with IN

Remember:

- `EXISTS` checks for matching rows.
- `IN` checks membership in a list of values.

______________________________________________________________________

### Writing Correlated Subqueries Unnecessarily

Sometimes a JOIN is simpler and faster.

Always consider both approaches.

______________________________________________________________________

# Best Practices

- Use scalar subqueries only when a single value is expected.
- Prefer `EXISTS` for existence checks.
- Avoid deeply nested subqueries.
- Use aliases for readability.
- Compare correlated subqueries with JOIN solutions during optimization.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between a subquery and a correlated subquery?

A normal subquery is independent of the outer query and typically executes once. A correlated subquery references
columns from the outer query and executes once for each row processed by the outer query. Correlated subqueries are more
expressive but may be slower depending on the execution plan.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a subquery?
1. What is a correlated subquery?
1. Explain `EXISTS`.
1. Explain `NOT EXISTS`.
1. Explain `ANY`.
1. Explain `ALL`.
1. When would you prefer `EXISTS` over `IN`?

## Coding

1. Find employees earning above the company average.
1. Find employees earning above their department average.
1. Find departments with employees.
1. Find departments without employees.
1. Find employees earning more than every HR employee.
1. Find employees earning more than at least one Finance employee.

______________________________________________________________________

# Hands-on Exercise

Using the Employees and Departments tables:

1. Write one scalar subquery.
1. Write one correlated subquery.
1. Solve the same problem using a JOIN.
1. Write queries using `EXISTS` and `NOT EXISTS`.
1. Rewrite all examples using SQLAlchemy.
1. Rewrite all applicable examples using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text
Subquery
→ Query inside another query

Scalar Subquery
→ Returns one value

Correlated Subquery
→ Executes per outer row

EXISTS
→ Checks row existence

NOT EXISTS
→ Checks absence

ANY
→ Compare with at least one value

ALL
→ Compare with every value
```

______________________________________________________________________

# Summary

In this part, you learned:

- Scalar subqueries
- Multi-row subqueries
- Subqueries in SELECT and FROM
- Correlated subqueries
- EXISTS
- NOT EXISTS
- ANY
- ALL
- SQLAlchemy equivalents
- SQLModel equivalents
- Interview patterns
- Best practices

The next part covers **CTEs, Recursive CTEs, UNION, UNION ALL, INTERSECT, EXCEPT, advanced interview questions,
performance considerations, and common optimization techniques.**

______________________________________________________________________

## Next File

[Advanced Queries - Part 2](06-advanced-queries-part-2.md)
