# Aggregations - Part 1

## Introduction

So far in this course, you've learned how to:

- Store data
- Retrieve data
- Filter data
- Join multiple tables

However, real-world applications rarely need individual rows. Instead, they usually need **summaries**.

Examples:

- How many employees work in each department?
- What is the average salary?
- Which department has the highest payroll?
- Which city has the most customers?
- How many orders were placed today?

These questions are answered using **aggregate functions**.

Aggregate functions process **multiple rows** and return **one summarized result**.

This chapter is one of the most important SQL interview topics because almost every interview contains questions
involving aggregates.

______________________________________________________________________

# Sample Database

We'll use this table throughout the chapter.

## Employees

| employee_id | name | department | salary | age | city |
| ----------- | ------- | ---------- | -----: | --: | --------- |
| 1 | Alice | HR | 60000 | 28 | Bangalore |
| 2 | Bob | IT | 85000 | 32 | Hyderabad |
| 3 | Charlie | IT | 90000 | 35 | Bangalore |
| 4 | David | Finance | 75000 | 30 | Chennai |
| 5 | Eva | HR | 65000 | 26 | Mumbai |
| 6 | Frank | Finance | NULL | 41 | Chennai |
| 7 | George | IT | 95000 | 29 | Bangalore |
| 8 | Helen | HR | 70000 | 34 | Bangalore |

Notice that Frank's salary is **NULL**.

We'll use this to understand NULL behavior.

______________________________________________________________________

# What Are Aggregate Functions?

Aggregate functions operate on a collection of rows and produce a single value.

Example

```text
60000
85000
90000
75000

↓

Average

77500
```

Common aggregate functions:

- COUNT()
- SUM()
- AVG()
- MIN()
- MAX()

______________________________________________________________________

# COUNT()

`COUNT()` counts rows.

There are three important forms.

______________________________________________________________________

## COUNT(\*)

Counts every row.

```sql
SELECT COUNT(*)
FROM employees;
```

Result

| count |
| ----: |
| 8 |

NULL values do **not** matter.

Even Frank is counted.

______________________________________________________________________

## COUNT(column)

Counts only rows where the specified column is NOT NULL.

```sql
SELECT COUNT(salary)
FROM employees;
```

Result

| count |
| ----: |
| 7 |

Frank's NULL salary is ignored.

______________________________________________________________________

## COUNT(DISTINCT column)

Counts unique non-NULL values.

```sql
SELECT COUNT(DISTINCT department)
FROM employees;
```

Result

| count |
| ----: |
| 3 |

Departments

- HR
- IT
- Finance

Duplicates are removed.

______________________________________________________________________

# COUNT() with WHERE

You can count only matching rows.

Example

```sql
SELECT COUNT(*)
FROM employees
WHERE department = 'IT';
```

Result

| count |
| ----: |
| 3 |

______________________________________________________________________

# SQLAlchemy

```python
from sqlalchemy import select, func

stmt = (
    select(func.count())
    .select_from(Employee)
)
```

Specific column

```python
stmt = (
    select(func.count(Employee.salary))
)
```

Distinct

```python
stmt = (
    select(
        func.count(Employee.department.distinct())
    )
)
```

______________________________________________________________________

# SQLModel

```python
from sqlmodel import select
from sqlalchemy import func

statement = (
    select(func.count())
    .select_from(Employee)
)
```

______________________________________________________________________

# SUM()

Returns the total.

```sql
SELECT SUM(salary)
FROM employees;
```

Result

| sum |
| -----: |
| 540000 |

Frank's NULL salary is ignored.

______________________________________________________________________

# SUM() with WHERE

```sql
SELECT SUM(salary)
FROM employees
WHERE department='IT';
```

Result

| sum |
| -----: |
| 270000 |

______________________________________________________________________

# SQLAlchemy

```python
stmt = (
    select(func.sum(Employee.salary))
)
```

______________________________________________________________________

# SQLModel

```python
statement = (
    select(func.sum(Employee.salary))
)
```

______________________________________________________________________

# AVG()

Returns the arithmetic mean.

```sql
SELECT AVG(salary)
FROM employees;
```

Result

| avg |
| --------: |
| 77142.857 |

Notice:

Frank's NULL salary is ignored.

Average is calculated only from seven salaries.

______________________________________________________________________

# AVG() with WHERE

```sql
SELECT AVG(salary)
FROM employees
WHERE department='HR';
```

______________________________________________________________________

# SQLAlchemy

```python
stmt = (
    select(func.avg(Employee.salary))
)
```

______________________________________________________________________

# SQLModel

```python
statement = (
    select(func.avg(Employee.salary))
)
```

______________________________________________________________________

# MIN()

Returns the smallest value.

```sql
SELECT MIN(salary)
FROM employees;
```

Result

```text
60000
```

NULL values are ignored.

______________________________________________________________________

# MAX()

Returns the largest value.

```sql
SELECT MAX(salary)
FROM employees;
```

Result

```text
95000
```

______________________________________________________________________

# SQLAlchemy

```python
stmt = (
    select(func.min(Employee.salary))
)

stmt = (
    select(func.max(Employee.salary))
)
```

______________________________________________________________________

# SQLModel

```python
statement = (
    select(func.min(Employee.salary))
)

statement = (
    select(func.max(Employee.salary))
)
```

______________________________________________________________________

# Aggregate Functions Ignore NULL

One of the most common interview questions.

Example

| Salary |
| -----: |
| 60000 |
| 85000 |
| NULL |

Query

```sql
SELECT
COUNT(*),
COUNT(salary),
SUM(salary),
AVG(salary),
MIN(salary),
MAX(salary)
FROM employees;
```

Result

| Expression | Result |
| ------------- | -----: |
| COUNT(\*) | 3 |
| COUNT(salary) | 2 |
| SUM(salary) | 145000 |
| AVG(salary) | 72500 |
| MIN(salary) | 60000 |
| MAX(salary) | 85000 |

Important:

Except for `COUNT(*)`, aggregate functions ignore NULL values.

______________________________________________________________________

# Aggregate Functions with Expressions

Aggregate functions can operate on expressions.

Example

```sql
SELECT
SUM(salary * 12)
FROM employees;
```

Annual payroll.

______________________________________________________________________

# Aliasing Aggregate Columns

Without aliases

```sql
SELECT AVG(salary)
FROM employees;
```

Result

```text
avg
```

Better

```sql
SELECT
AVG(salary) AS average_salary
FROM employees;
```

Always use meaningful aliases.

______________________________________________________________________

# Common Mistakes

### Confusing COUNT(\*) and COUNT(column)

They are **not** the same.

______________________________________________________________________

### Forgetting NULL behavior

Most aggregate functions ignore NULL values.

______________________________________________________________________

### Averaging text columns

Aggregate functions should operate on compatible data types.

______________________________________________________________________

# Best Practices

- Use COUNT(\*) when counting rows.
- Use aliases.
- Understand NULL behavior.
- Filter before aggregating whenever possible.
- Avoid unnecessary calculations inside aggregate functions.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between COUNT(\*) and COUNT(column)?

`COUNT(*)` counts every row returned by the query, regardless of NULL values. `COUNT(column)` counts only the rows where
the specified column contains a non-NULL value. This distinction is frequently tested in SQL interviews because it
affects reporting accuracy when nullable columns are involved.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is an aggregate function?
1. Which aggregate functions ignore NULL values?
1. What is the difference between COUNT(\*) and COUNT(column)?
1. Why is COUNT(DISTINCT) useful?
1. Can aggregate functions be used with expressions?

## Coding

1. Count employees.
1. Count employees in HR.
1. Find total salary.
1. Find highest salary.
1. Find lowest salary.
1. Find average salary.
1. Count unique cities.

______________________________________________________________________

# Hands-on Exercise

Using the Employees table:

1. Count all employees.
1. Count employees with salaries.
1. Calculate total payroll.
1. Calculate IT payroll.
1. Find the average HR salary.
1. Find the minimum and maximum salaries.
1. Rewrite every query using SQLAlchemy.
1. Rewrite every query using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text
COUNT(*)
Rows

COUNT(column)
Non-NULL values

COUNT(DISTINCT)
Unique values

SUM()
Addition

AVG()
Average

MIN()
Smallest

MAX()
Largest

All ignore NULL
except COUNT(*)
```

______________________________________________________________________

# Summary

In this part, you learned:

- COUNT
- COUNT(\*)
- COUNT(column)
- COUNT(DISTINCT)
- SUM
- AVG
- MIN
- MAX
- NULL handling
- Aggregate expressions
- SQLAlchemy equivalents
- SQLModel equivalents

The next part covers **GROUP BY**, **HAVING**, **Conditional Aggregation**, **GROUP BY vs DISTINCT**, **HAVING vs
WHERE**, **Aggregations with JOINs**, interview tricks, and performance considerations.

______________________________________________________________________

## Next File

[Aggregations - Part 2](05-aggregations-part-2.md)
