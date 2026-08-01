# Joins (Deep Dive) - Part 1

## Introduction

One of the most important concepts in SQL is the **JOIN** operation. In real-world applications, data is rarely stored
in a single table. Instead, it is divided across multiple related tables to reduce redundancy and improve data
integrity.

For example:

- An employee belongs to a department.
- A customer places many orders.
- A student enrolls in multiple courses.
- An order contains multiple products.

If related data is stored in separate tables, how do we retrieve it together?

The answer is **JOIN**.

Joins combine rows from two or more tables based on a related column.

This is one of the most frequently tested SQL topics in interviews, from junior to senior software engineering roles.

______________________________________________________________________

# Why Do We Need Joins?

Consider the following database.

## Employees

| employee_id | name | department_id |
| ----------: | ------- | ------------: |
| 1 | Alice | 1 |
| 2 | Bob | 2 |
| 3 | Charlie | 2 |
| 4 | David | 3 |
| 5 | Eva | NULL |

## Departments

| department_id | department_name |
| ------------: | --------------- |
| 1 | HR |
| 2 | Engineering |
| 3 | Finance |
| 4 | Marketing |

Suppose we want the following output.

| Employee | Department |
| -------- | ----------- |
| Alice | HR |
| Bob | Engineering |
| Charlie | Engineering |
| David | Finance |

The department name does not exist inside the `employees` table.

It exists in another table.

A **JOIN** combines these tables into a single result.

______________________________________________________________________

# What is a JOIN?

A JOIN combines rows from two or more tables using a related column.

General syntax:

```sql
SELECT columns
FROM table1
JOIN table2
ON table1.column = table2.column;
```

The `ON` clause specifies how the rows should be matched.

______________________________________________________________________

# Types of Joins

SQL supports several join types.

- INNER JOIN
- LEFT JOIN (LEFT OUTER JOIN)
- RIGHT JOIN (RIGHT OUTER JOIN)
- FULL OUTER JOIN
- CROSS JOIN
- SELF JOIN

We'll study each one in detail.

______________________________________________________________________

# INNER JOIN

An INNER JOIN returns **only the rows that have matching values in both tables**.

This is the most commonly used join.

Diagram

```text
Employees                Departments

 Alice  ----------- HR
 Bob    ----------- Engineering
 Charlie----------- Engineering
 David  ----------- Finance
 Eva    ----------- NULL

Only matching rows are returned.
```

______________________________________________________________________

## SQL Syntax

```sql
SELECT
    e.employee_id,
    e.name,
    d.department_name
FROM employees e
INNER JOIN departments d
ON e.department_id = d.department_id;
```

Result

| employee_id | name | department_name |
| ----------- | ------- | --------------- |
| 1 | Alice | HR |
| 2 | Bob | Engineering |
| 3 | Charlie | Engineering |
| 4 | David | Finance |

Notice that Eva is missing because her `department_id` is `NULL`.

Marketing is also missing because no employee belongs to it.

______________________________________________________________________

# SQLAlchemy Equivalent

```python
from sqlalchemy import select

stmt = (
    select(Employee.name, Department.department_name)
    .join(
        Department,
        Employee.department_id == Department.department_id
    )
)
```

______________________________________________________________________

# SQLModel Equivalent

```python
from sqlmodel import select

statement = (
    select(Employee, Department)
    .join(
        Department,
        Employee.department_id == Department.department_id
    )
)
```

______________________________________________________________________

# How INNER JOIN Works

Many beginners imagine that SQL magically combines tables.

Internally, SQL performs matching based on the join condition.

Think of it like this:

```text
Employees

Alice ---- department_id = 1

↓

Search Departments

department_id = 1

↓

Found HR

↓

Return Row
```

The database repeats this process for every row.

Modern databases optimize this using sophisticated join algorithms (covered later).

______________________________________________________________________

# Understanding the ON Clause

The `ON` clause defines the matching condition.

Example

```sql
ON employees.department_id = departments.department_id
```

This means

```text
Take one employee

↓

Compare department_id

↓

Find matching department

↓

Return combined row
```

Without the `ON` clause, SQL would not know how to relate the two tables.

______________________________________________________________________

# Table Aliases

Instead of repeatedly writing long table names, aliases improve readability.

Without aliases

```sql
SELECT
employees.name,
departments.department_name
FROM employees
INNER JOIN departments
ON employees.department_id = departments.department_id;
```

With aliases

```sql
SELECT
e.name,
d.department_name
FROM employees e
JOIN departments d
ON e.department_id = d.department_id;
```

Aliases are considered best practice in production SQL.

______________________________________________________________________

# Joining More Than Two Tables

SQL allows joining multiple tables.

Example

Employees

↓

Departments

↓

Locations

```sql
SELECT
e.name,
d.department_name,
l.city
FROM employees e
JOIN departments d
ON e.department_id = d.department_id
JOIN locations l
ON d.location_id = l.location_id;
```

The result combines information from three tables.

______________________________________________________________________

# INNER JOIN with Additional Conditions

You can add filters using `WHERE`.

```sql
SELECT
e.name,
d.department_name
FROM employees e
JOIN departments d
ON e.department_id = d.department_id
WHERE d.department_name = 'Engineering';
```

Result

| name | department_name |
| ------- | --------------- |
| Bob | Engineering |
| Charlie | Engineering |

______________________________________________________________________

# Execution Order

Although we write SQL in one order, the database logically processes it like this:

```text
FROM

↓

JOIN

↓

ON

↓

WHERE

↓

GROUP BY

↓

HAVING

↓

SELECT

↓

ORDER BY

↓

LIMIT
```

Understanding this order helps explain why some queries behave unexpectedly and is a common interview topic.

______________________________________________________________________

# Common Mistakes

### Forgetting the ON clause

Incorrect

```sql
SELECT *
FROM employees
JOIN departments;
```

Most databases either produce an error or behave as a CROSS JOIN depending on the SQL dialect and syntax.

______________________________________________________________________

### Joining on the wrong columns

Incorrect

```sql
ON employees.employee_id = departments.department_id
```

Always join related keys.

Correct

```sql
ON employees.department_id = departments.department_id
```

______________________________________________________________________

### Selecting `*` unnecessarily

Instead of

```sql
SELECT *
```

Prefer

```sql
SELECT
e.name,
d.department_name
```

This improves readability and can reduce unnecessary data transfer.

______________________________________________________________________

# Best Practices

- Use meaningful table aliases.
- Join using indexed columns whenever possible.
- Select only the columns you need.
- Keep join conditions simple and explicit.
- Prefer explicit `JOIN` syntax over older comma-separated joins.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between an INNER JOIN and a LEFT JOIN?

An INNER JOIN returns only the rows that have matching values in both tables. A LEFT JOIN returns all rows from the left
table, even if there is no matching row in the right table. When no match exists, the columns from the right table are
returned as `NULL`.

______________________________________________________________________

# Practice Questions

### Conceptual

1. What is a JOIN?
1. Why do we use joins?
1. What is an INNER JOIN?
1. What is the purpose of the `ON` clause?
1. Why are table aliases useful?
1. Can SQL join more than two tables?

### Coding

1. Retrieve employee names with department names.
1. Show only Engineering employees.
1. Join Employees, Departments, and Locations.
1. Retrieve employee IDs with department IDs.
1. Display only employee names and department names.

______________________________________________________________________

# Hands-on Exercise

Create the following tables:

- Employees
- Departments

Insert at least five records into each table.

Write queries to:

1. Retrieve employee names with department names.
1. Display only Finance employees.
1. Join three tables by introducing a Locations table.
1. Rewrite each query using SQLAlchemy.
1. Rewrite each query using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text
INNER JOIN

Returns only matching rows.

Syntax

SELECT columns
FROM table1
JOIN table2
ON table1.column = table2.column;
```

______________________________________________________________________

# Summary

In this part, you learned:

- Why joins are needed
- INNER JOIN
- JOIN syntax
- Table aliases
- Multiple table joins
- Execution order
- Common mistakes
- SQLAlchemy equivalent
- SQLModel equivalent

In the next part, we'll cover LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN, NULL behavior, and compare all join types
visually.

______________________________________________________________________

## Next File

[Joins (Deep Dive) - Part 2](04-joins-deep-dive-part-2.md)
