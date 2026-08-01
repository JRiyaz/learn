# SQL CRUD & Filtering

## Introduction

Now that you understand how databases are organized and how they guarantee consistency using transactions, it's time to
start writing SQL.

CRUD stands for:

- **C**reate
- **R**ead
- **U**pdate
- **D**elete

These are the four fundamental operations performed on data. Almost every SQL interview begins with CRUD before moving
on to joins, aggregations, or optimization.

In this chapter, we'll learn how to create tables, insert data, retrieve records, update existing records, delete
records, and filter results efficiently.

______________________________________________________________________

# Sample Database

We'll use the following `employees` table throughout this chapter.

| employee_id | name | department | salary | age | city |
| ----------- | ------- | ---------- | ------ | --- | --------- |
| 1 | Alice | HR | 60000 | 28 | Bangalore |
| 2 | Bob | IT | 85000 | 32 | Hyderabad |
| 3 | Charlie | IT | 90000 | 35 | Bangalore |
| 4 | David | Finance | 75000 | 30 | Chennai |
| 5 | Eva | HR | 65000 | 26 | Mumbai |

______________________________________________________________________

# CREATE TABLE

The `CREATE TABLE` statement creates a new table in the database.

## Syntax

```sql
CREATE TABLE table_name (
    column_name datatype constraints
);
```

## Example

```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    age INT,
    city VARCHAR(100)
);
```

______________________________________________________________________

# INSERT

The `INSERT` statement adds new rows into a table.

## Syntax

```sql
INSERT INTO table_name (column1, column2)
VALUES (value1, value2);
```

## Example

```sql
INSERT INTO employees
(employee_id, name, department, salary, age, city)
VALUES
(1, 'Alice', 'HR', 60000, 28, 'Bangalore');
```

Insert multiple rows:

```sql
INSERT INTO employees
(employee_id, name, department, salary, age, city)
VALUES
(2, 'Bob', 'IT', 85000, 32, 'Hyderabad'),
(3, 'Charlie', 'IT', 90000, 35, 'Bangalore');
```

______________________________________________________________________

# SELECT

The `SELECT` statement retrieves data from a table.

## Syntax

```sql
SELECT column_list
FROM table_name;
```

Retrieve all columns:

```sql
SELECT *
FROM employees;
```

Retrieve specific columns:

```sql
SELECT
name,
salary
FROM employees;
```

______________________________________________________________________

# SQLAlchemy Equivalent

```python
from sqlalchemy import select

stmt = select(Employee)
```

Specific columns:

```python
stmt = select(Employee.name, Employee.salary)
```

______________________________________________________________________

# SQLModel Equivalent

```python
from sqlmodel import select

statement = select(Employee)
```

______________________________________________________________________

# UPDATE

The `UPDATE` statement modifies existing rows.

## Syntax

```sql
UPDATE table_name
SET column = value
WHERE condition;
```

Example:

```sql
UPDATE employees
SET salary = 70000
WHERE employee_id = 1;
```

Update multiple columns:

```sql
UPDATE employees
SET
salary = 95000,
department = 'Engineering'
WHERE employee_id = 2;
```

______________________________________________________________________

# SQLAlchemy Equivalent

```python
from sqlalchemy import update

stmt = (
    update(Employee)
    .where(Employee.employee_id == 1)
    .values(salary=70000)
)
```

______________________________________________________________________

# SQLModel Equivalent

```python
employee.salary = 70000
session.add(employee)
session.commit()
```

______________________________________________________________________

# DELETE

Deletes rows from a table.

## Syntax

```sql
DELETE FROM table_name
WHERE condition;
```

Example:

```sql
DELETE FROM employees
WHERE employee_id = 5;
```

⚠️ Never omit the `WHERE` clause unless you intentionally want to delete every row.

______________________________________________________________________

# SQLAlchemy Equivalent

```python
from sqlalchemy import delete

stmt = delete(Employee).where(Employee.employee_id == 5)
```

______________________________________________________________________

# SQLModel Equivalent

```python
session.delete(employee)
session.commit()
```

______________________________________________________________________

# WHERE

Filters rows based on a condition.

Example:

```sql
SELECT *
FROM employees
WHERE department = 'IT';
```

______________________________________________________________________

# SQLAlchemy Equivalent

```python
stmt = (
    select(Employee)
    .where(Employee.department == "IT")
)
```

______________________________________________________________________

# SQLModel Equivalent

```python
statement = (
    select(Employee)
    .where(Employee.department == "IT")
)
```

______________________________________________________________________

# DISTINCT

Returns unique values.

```sql
SELECT DISTINCT department
FROM employees;
```

______________________________________________________________________

# ORDER BY

Sorts results.

Ascending:

```sql
SELECT *
FROM employees
ORDER BY salary;
```

Descending:

```sql
SELECT *
FROM employees
ORDER BY salary DESC;
```

SQLAlchemy

```python
stmt = (
    select(Employee)
    .order_by(Employee.salary.desc())
)
```

______________________________________________________________________

# LIMIT

Returns only a fixed number of rows.

```sql
SELECT *
FROM employees
LIMIT 5;
```

SQLAlchemy

```python
stmt = select(Employee).limit(5)
```

______________________________________________________________________

# OFFSET

Skips rows.

```sql
SELECT *
FROM employees
LIMIT 5 OFFSET 10;
```

Useful for pagination.

______________________________________________________________________

# LIKE

Pattern matching.

Starts with A

```sql
SELECT *
FROM employees
WHERE name LIKE 'A%';
```

Ends with e

```sql
WHERE name LIKE '%e';
```

Contains "ar"

```sql
WHERE name LIKE '%ar%';
```

______________________________________________________________________

# ILIKE (PostgreSQL)

Case-insensitive pattern matching.

```sql
SELECT *
FROM employees
WHERE city ILIKE 'bangalore';
```

______________________________________________________________________

# BETWEEN

Checks whether a value lies within a range.

```sql
SELECT *
FROM employees
WHERE salary BETWEEN 70000 AND 90000;
```

______________________________________________________________________

# IN

Checks whether a value belongs to a list.

```sql
SELECT *
FROM employees
WHERE department IN ('HR', 'IT');
```

______________________________________________________________________

# EXISTS

Checks whether a subquery returns any rows.

```sql
SELECT *
FROM employees e
WHERE EXISTS (
    SELECT 1
    FROM departments d
    WHERE d.department_name = e.department
);
```

We'll study correlated subqueries and `EXISTS` in more detail later.

______________________________________________________________________

# CASE

Adds conditional logic to a query.

```sql
SELECT
name,
salary,
CASE
    WHEN salary >= 90000 THEN 'High'
    WHEN salary >= 70000 THEN 'Medium'
    ELSE 'Low'
END AS salary_band
FROM employees;
```

______________________________________________________________________

# Comparison Table

| SQL | SQLAlchemy | SQLModel |
| -------- | ------------- | -------------------------- |
| SELECT | `select()` | `select()` |
| UPDATE | `update()` | Modify object + `commit()` |
| DELETE | `delete()` | `session.delete()` |
| WHERE | `.where()` | `.where()` |
| ORDER BY | `.order_by()` | `.order_by()` |
| LIMIT | `.limit()` | `.limit()` |

______________________________________________________________________

# Common Mistakes

- Forgetting the `WHERE` clause in `UPDATE`.
- Forgetting the `WHERE` clause in `DELETE`.
- Using `SELECT *` unnecessarily.
- Assuming `LIKE` is case-insensitive in every database.
- Forgetting `ORDER BY` when expecting sorted results.

______________________________________________________________________

# Best Practices

- Select only the columns you need.
- Always use `WHERE` for updates and deletes.
- Prefer parameterized queries in applications.
- Use pagination (`LIMIT` + `OFFSET`) for large datasets.
- Write readable SQL with proper formatting.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between `WHERE`, `HAVING`, and `ON`?

`WHERE` filters rows before grouping, `HAVING` filters groups after aggregation, and `ON` specifies how tables should be
matched during a join. Choosing the correct clause affects both correctness and query performance.

______________________________________________________________________

# Practice Questions

### Conceptual

1. What does CRUD stand for?
1. What is the purpose of `WHERE`?
1. What is the difference between `LIKE` and `ILIKE`?
1. When would you use `DISTINCT`?
1. What is the difference between `LIMIT` and `OFFSET`?
1. What does `CASE` do?

### Coding

1. Retrieve all employees from the IT department.
1. Find employees earning between ₹70,000 and ₹90,000.
1. Display unique department names.
1. Increase the salary of all HR employees by ₹5,000.
1. Delete employees older than 60 years.

______________________________________________________________________

# Hands-on Exercise

Create an `employees` table and insert at least 10 records.

Write SQL queries to:

1. Retrieve all employees.
1. Find employees from Bangalore.
1. Retrieve employees with salaries greater than ₹80,000.
1. Sort employees by age in descending order.
1. Display only the first three employees.
1. Categorize salaries as High, Medium, or Low using `CASE`.

Then write the equivalent SQLAlchemy and SQLModel code for the `SELECT` queries.

______________________________________________________________________

# Cheat Sheet

```text
CREATE TABLE
INSERT INTO
SELECT
UPDATE
DELETE

WHERE
DISTINCT
ORDER BY
LIMIT
OFFSET

LIKE
ILIKE
BETWEEN
IN
EXISTS
CASE
```

______________________________________________________________________

# Summary

In this lesson, you learned:

- CREATE TABLE
- INSERT
- SELECT
- UPDATE
- DELETE
- WHERE
- DISTINCT
- ORDER BY
- LIMIT
- OFFSET
- LIKE
- ILIKE
- BETWEEN
- IN
- EXISTS
- CASE

You also learned the equivalent implementations using **SQLAlchemy** and **SQLModel** for the core CRUD operations.

______________________________________________________________________

## Next File

[Joins (Deep Dive) - Part 1](04-joins-deep-dive-part-1.md)
