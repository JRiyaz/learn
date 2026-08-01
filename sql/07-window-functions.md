# Window Functions

## Introduction

Window Functions are one of the most powerful features in SQL and are among the most frequently asked topics in
**mid-level and senior software engineering interviews**.

Unlike aggregate functions, which reduce multiple rows into a single result, **window functions perform calculations
across a set of related rows while preserving every individual row**.

For example, window functions help answer questions like:

- Rank employees by salary.
- Find the highest-paid employee in each department.
- Calculate a running total.
- Compare an employee's salary with the previous employee.
- Find the next order date for every customer.
- Calculate moving averages.

These operations are extremely difficult without window functions.

______________________________________________________________________

# Aggregate Functions vs Window Functions

Aggregate functions collapse rows.

Example:

```sql
SELECT
    department,
    AVG(salary)
FROM employees
GROUP BY department;
```

Result

| Department | Average Salary |
| ---------- | -------------: |
| HR | 65000 |
| IT | 90000 |
| Finance | 75000 |

Notice that one row is returned for each department.

______________________________________________________________________

Window functions preserve rows.

```sql
SELECT
    name,
    department,
    salary,
    AVG(salary) OVER(PARTITION BY department) AS department_average
FROM employees;
```

Result

| Name | Department | Salary | Department Average |
| ------- | ---------- | -----: | -----------------: |
| Alice | HR | 60000 | 65000 |
| Eva | HR | 70000 | 65000 |
| Bob | IT | 85000 | 90000 |
| Charlie | IT | 95000 | 90000 |

Every employee remains visible.

______________________________________________________________________

# Sample Data

| employee_id | name | department | salary |
| ----------- | ------- | ---------- | -----: |
| 1 | Alice | HR | 60000 |
| 2 | Bob | IT | 85000 |
| 3 | Charlie | IT | 95000 |
| 4 | David | Finance | 75000 |
| 5 | Eva | HR | 70000 |
| 6 | Frank | Finance | 80000 |

______________________________________________________________________

# OVER()

Every window function requires an `OVER()` clause.

General syntax

```sql
FUNCTION(...) OVER(...)
```

The `OVER()` clause tells SQL which rows belong to the window.

Example

```sql
SELECT
name,
salary,
AVG(salary) OVER()
FROM employees;
```

The average salary is displayed for every row.

______________________________________________________________________

# PARTITION BY

`PARTITION BY` divides rows into independent groups.

Example

```sql
SELECT
name,
department,
salary,
AVG(salary) OVER(
    PARTITION BY department
) AS department_average
FROM employees;
```

Each department becomes its own window.

Think of it as:

```text
HR
-------------
Alice
Eva

IT
-------------
Bob
Charlie

Finance
-------------
David
Frank
```

Each partition is processed independently.

______________________________________________________________________

# ORDER BY inside OVER()

Do not confuse:

```sql
ORDER BY
```

with

```sql
OVER(ORDER BY ...)
```

Inside `OVER()`, the ordering affects the window calculation.

Outside `OVER()`, it affects the final output.

Example

```sql
SELECT
name,
salary,
SUM(salary)
OVER(
ORDER BY salary
) AS running_total
FROM employees;
```

______________________________________________________________________

# ROW_NUMBER()

Assigns a unique sequential number.

```sql
SELECT
name,
salary,
ROW_NUMBER() OVER(
ORDER BY salary DESC
) AS row_num
FROM employees;
```

Result

| Name | Salary | Row Number |
| ------- | -----: | ---------: |
| Charlie | 95000 | 1 |
| Bob | 85000 | 2 |
| Frank | 80000 | 3 |
| David | 75000 | 4 |

No ties.

______________________________________________________________________

# SQLAlchemy

```python
from sqlalchemy import select, func

stmt = select(
    Employee.name,
    Employee.salary,
    func.row_number()
        .over(order_by=Employee.salary.desc())
        .label("row_num")
)
```

______________________________________________________________________

# SQLModel

```python
statement = select(
    Employee.name,
    Employee.salary,
    func.row_number()
        .over(order_by=Employee.salary.desc())
)
```

______________________________________________________________________

# RANK()

Ranks rows.

Ties receive the same rank.

The next rank is skipped.

```sql
SELECT
name,
salary,
RANK() OVER(
ORDER BY salary DESC
) AS salary_rank
FROM employees;
```

Example

| Salary | Rank |
| -----: | ---: |
| 95000 | 1 |
| 90000 | 2 |
| 90000 | 2 |
| 85000 | 4 |

Rank 3 is skipped.

______________________________________________________________________

# DENSE_RANK()

Similar to `RANK()`.

No gaps.

```sql
SELECT
name,
salary,
DENSE_RANK() OVER(
ORDER BY salary DESC
) AS dense_rank
FROM employees;
```

Example

| Salary | Dense Rank |
| -----: | ---------: |
| 95000 | 1 |
| 90000 | 2 |
| 90000 | 2 |
| 85000 | 3 |

______________________________________________________________________

# ROW_NUMBER vs RANK vs DENSE_RANK

| Function | Duplicate Rank | Skips Numbers |
| ---------- | -------------- | ------------- |
| ROW_NUMBER | No | No |
| RANK | Yes | Yes |
| DENSE_RANK | Yes | No |

This comparison is a classic interview question.

______________________________________________________________________

# LEAD()

Returns a value from the next row.

```sql
SELECT
name,
salary,
LEAD(salary)
OVER(
ORDER BY salary
) AS next_salary
FROM employees;
```

______________________________________________________________________

# LAG()

Returns a value from the previous row.

```sql
SELECT
name,
salary,
LAG(salary)
OVER(
ORDER BY salary
) AS previous_salary
FROM employees;
```

______________________________________________________________________

# FIRST_VALUE()

Returns the first value in the window.

```sql
SELECT
name,
FIRST_VALUE(name)
OVER(
ORDER BY salary DESC
)
FROM employees;
```

______________________________________________________________________

# LAST_VALUE()

Returns the last value in the current window frame.

```sql
SELECT
name,
LAST_VALUE(name)
OVER(
    ORDER BY salary
    ROWS BETWEEN UNBOUNDED PRECEDING
    AND UNBOUNDED FOLLOWING
)
FROM employees;
```

> **Interview Note:** Without explicitly defining the window frame, `LAST_VALUE()` often surprises developers because the default frame ends at the current row. Explicitly specifying the frame avoids incorrect results.

______________________________________________________________________

# NTILE()

Splits rows into approximately equal groups.

Example

```sql
SELECT
name,
salary,
NTILE(4)
OVER(
ORDER BY salary
)
FROM employees;
```

Useful for quartiles and percentiles.

______________________________________________________________________

# Running Total

A common interview problem.

```sql
SELECT
name,
salary,
SUM(salary)
OVER(
ORDER BY employee_id
) AS running_total
FROM employees;
```

______________________________________________________________________

# Moving Average

Average of the current row and two previous rows.

```sql
SELECT
employee_id,
salary,
AVG(salary)
OVER(
ORDER BY employee_id
ROWS BETWEEN 2 PRECEDING
AND CURRENT ROW
) AS moving_average
FROM employees;
```

______________________________________________________________________

# Top N Per Group

Find the highest-paid employee in every department.

```sql
WITH ranked AS (
SELECT
*,
ROW_NUMBER()
OVER(
PARTITION BY department
ORDER BY salary DESC
) AS rn
FROM employees
)
SELECT *
FROM ranked
WHERE rn = 1;
```

This is one of the most common SQL interview questions.

______________________________________________________________________

# SQLAlchemy Example

```python
ranked = (
    select(
        Employee,
        func.row_number()
        .over(
            partition_by=Employee.department,
            order_by=Employee.salary.desc()
        )
        .label("rn")
    )
).cte("ranked")

stmt = select(ranked).where(ranked.c.rn == 1)
```

______________________________________________________________________

# SQLModel

Uses the same SQLAlchemy window expressions.

______________________________________________________________________

# Performance Considerations

- Window functions usually require sorting.
- Indexes on `PARTITION BY` and `ORDER BY` columns can improve performance.
- Large partitions increase memory usage.
- Avoid unnecessary window functions in large queries.

______________________________________________________________________

# Common Mistakes

### Confusing GROUP BY with Window Functions

`GROUP BY` reduces rows.

Window functions preserve rows.

______________________________________________________________________

### Forgetting PARTITION BY

Without `PARTITION BY`, the entire result set becomes one window.

______________________________________________________________________

### Using ROW_NUMBER Instead of RANK

Remember:

- `ROW_NUMBER()` never produces duplicate numbers.
- `RANK()` allows ties.
- `DENSE_RANK()` allows ties without gaps.

______________________________________________________________________

### Incorrect LAST_VALUE()

Always verify the window frame.

______________________________________________________________________

# Best Practices

- Prefer window functions over self-joins for ranking problems.
- Use descriptive aliases.
- Add `PARTITION BY` only when logically needed.
- Understand the difference between ranking functions.
- Review execution plans for very large datasets.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`?

`ROW_NUMBER()` assigns a unique sequential number to every row, even when values are tied. `RANK()` assigns the same
rank to tied rows but skips subsequent rank values. `DENSE_RANK()` also assigns the same rank to tied rows but does not
leave gaps. Use `ROW_NUMBER()` when every row must be uniquely ordered, `RANK()` when ranking positions matter, and
`DENSE_RANK()` when consecutive rankings are required.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a window function?
1. Explain the purpose of `OVER()`.
1. What does `PARTITION BY` do?
1. Difference between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`.
1. Explain `LEAD()` and `LAG()`.
1. What is a running total?
1. What is a moving average?

## Coding

1. Rank employees by salary.
1. Rank employees within each department.
1. Find the highest-paid employee in every department.
1. Calculate a running salary total.
1. Compare each employee's salary with the previous employee.
1. Divide employees into four salary quartiles.

______________________________________________________________________

# Hands-on Exercise

Using the Employees table:

1. Assign row numbers ordered by salary.
1. Assign department-wise ranks.
1. Find the top two earners in each department.
1. Calculate running totals.
1. Calculate moving averages.
1. Display previous and next salaries using `LAG()` and `LEAD()`.
1. Rewrite all examples using SQLAlchemy.
1. Rewrite all applicable examples using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text
OVER()

↓

PARTITION BY

↓

ORDER BY

↓

ROW_NUMBER()

RANK()

DENSE_RANK()

LEAD()

LAG()

FIRST_VALUE()

LAST_VALUE()

NTILE()
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- Window Functions
- OVER()
- PARTITION BY
- ORDER BY inside OVER()
- ROW_NUMBER()
- RANK()
- DENSE_RANK()
- LEAD()
- LAG()
- FIRST_VALUE()
- LAST_VALUE()
- NTILE()
- Running Totals
- Moving Averages
- Top N Per Group
- SQLAlchemy equivalents
- SQLModel equivalents
- Performance considerations
- Interview patterns
- Best practices

You now have a solid understanding of window functions, one of the most valuable SQL topics for technical interviews.

______________________________________________________________________

## Next File

[Constraints & Indexes](08-constraints-indexes.md)
