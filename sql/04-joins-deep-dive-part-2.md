# Joins (Deep Dive) - Part 2

## Introduction

In Part 1, we learned how **INNER JOIN** returns only the matching rows between two tables.

In this chapter, we'll cover the remaining join types:

- LEFT JOIN
- RIGHT JOIN
- FULL OUTER JOIN

These joins are commonly asked in interviews because they test your understanding of `NULL` handling and how unmatched
rows are returned.

We'll continue using the same sample tables.

______________________________________________________________________

# Sample Data

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

Notice:

- Eva does **not** belong to any department.
- Marketing has **no employees**.

These unmatched rows help illustrate different join behaviors.

______________________________________________________________________

# LEFT JOIN (LEFT OUTER JOIN)

A **LEFT JOIN** returns:

- All rows from the **left table**
- Matching rows from the right table
- `NULL` for right-table columns when no match exists

Diagram

```text
Employees                     Departments

Alice    ───────────────► HR
Bob      ───────────────► Engineering
Charlie  ───────────────► Engineering
David    ───────────────► Finance
Eva      ───────────────► NULL
```

Everything from the **Employees** table is returned.

______________________________________________________________________

## SQL Syntax

```sql
SELECT
    e.employee_id,
    e.name,
    d.department_name
FROM employees e
LEFT JOIN departments d
ON e.department_id = d.department_id;
```

Result

| employee_id | name | department_name |
| ----------- | ------- | --------------- |
| 1 | Alice | HR |
| 2 | Bob | Engineering |
| 3 | Charlie | Engineering |
| 4 | David | Finance |
| 5 | Eva | NULL |

Unlike INNER JOIN, Eva is included.

______________________________________________________________________

# SQLAlchemy Equivalent

```python
from sqlalchemy import select

stmt = (
    select(Employee.name, Department.department_name)
    .outerjoin(
        Department,
        Employee.department_id == Department.department_id
    )
)
```

> In SQLAlchemy, `outerjoin()` produces a **LEFT OUTER JOIN** by default.

______________________________________________________________________

# SQLModel Equivalent

```python
from sqlmodel import select

statement = (
    select(Employee, Department)
    .outerjoin(
        Department,
        Employee.department_id == Department.department_id
    )
)
```

______________________________________________________________________

# When Should You Use LEFT JOIN?

LEFT JOIN is useful when you want **every record from the left table**, even if related data is missing.

Examples:

- All employees, including those without departments.
- All customers, including those who have never placed an order.
- All students, including those who have not enrolled in any course.

______________________________________________________________________

# Finding Missing Records Using LEFT JOIN

One of the most common interview questions is:

**"Find employees who don't belong to any department."**

```sql
SELECT
    e.employee_id,
    e.name
FROM employees e
LEFT JOIN departments d
ON e.department_id = d.department_id
WHERE d.department_id IS NULL;
```

Result

| employee_id | name |
| ----------- | ---- |
| 5 | Eva |

This pattern is extremely common.

______________________________________________________________________

# RIGHT JOIN (RIGHT OUTER JOIN)

A **RIGHT JOIN** returns:

- All rows from the **right table**
- Matching rows from the left table
- `NULL` for left-table columns when no match exists

Diagram

```text
Employees                     Departments

Alice    ───────────────► HR
Bob      ───────────────► Engineering
Charlie  ───────────────► Engineering
David    ───────────────► Finance
NULL     ◄────────────── Marketing
```

Marketing appears even though no employee belongs to it.

______________________________________________________________________

## SQL Syntax

```sql
SELECT
    e.name,
    d.department_name
FROM employees e
RIGHT JOIN departments d
ON e.department_id = d.department_id;
```

Result

| name | department_name |
| ------- | --------------- |
| Alice | HR |
| Bob | Engineering |
| Charlie | Engineering |
| David | Finance |
| NULL | Marketing |

______________________________________________________________________

# Should You Use RIGHT JOIN?

In practice, **RIGHT JOIN is rarely used**.

Almost every RIGHT JOIN can be rewritten as a LEFT JOIN by swapping the table order.

Example:

Instead of

```sql
A RIGHT JOIN B
```

Write

```sql
B LEFT JOIN A
```

Many development teams avoid RIGHT JOIN entirely for consistency.

______________________________________________________________________

# SQLAlchemy Equivalent

SQLAlchemy does not provide a dedicated `right_join()` API.

Instead, swap the table order and use `outerjoin()`.

Example:

```python
stmt = (
    select(Department.department_name, Employee.name)
    .select_from(Department)
    .outerjoin(
        Employee,
        Department.department_id == Employee.department_id
    )
)
```

This produces the same logical result as a RIGHT JOIN.

______________________________________________________________________

# FULL OUTER JOIN

A FULL OUTER JOIN returns:

- All matching rows
- Unmatched rows from the left table
- Unmatched rows from the right table

Diagram

```text
Employees                     Departments

Alice    ───────────────► HR
Bob      ───────────────► Engineering
Charlie  ───────────────► Engineering
David    ───────────────► Finance
Eva      ───────────────► NULL
NULL     ◄────────────── Marketing
```

Everything appears.

______________________________________________________________________

## SQL Syntax

```sql
SELECT
    e.name,
    d.department_name
FROM employees e
FULL OUTER JOIN departments d
ON e.department_id = d.department_id;
```

Result

| name | department_name |
| ------- | --------------- |
| Alice | HR |
| Bob | Engineering |
| Charlie | Engineering |
| David | Finance |
| Eva | NULL |
| NULL | Marketing |

______________________________________________________________________

# SQLAlchemy Equivalent

SQLAlchemy supports FULL OUTER JOIN using the `full=True` parameter.

```python
stmt = (
    select(Employee.name, Department.department_name)
    .join(
        Department,
        Employee.department_id == Department.department_id,
        full=True
    )
)
```

> This generates `FULL OUTER JOIN` on databases that support it (such as PostgreSQL).

______________________________________________________________________

# SQLModel Equivalent

Since SQLModel uses SQLAlchemy underneath, the same join expression can be used.

______________________________________________________________________

# INNER vs LEFT vs RIGHT vs FULL

| Join | Returns |
| ---------- | ----------------------------------- |
| INNER | Only matching rows |
| LEFT | All left rows + matching right rows |
| RIGHT | All right rows + matching left rows |
| FULL OUTER | All rows from both tables |

______________________________________________________________________

# NULL Behavior

One of the biggest interview topics.

Consider Eva.

```text
Employee

Eva

DepartmentID = NULL
```

When joining:

```sql
ON employee.department_id = department.department_id
```

No department matches because `NULL` is **not equal to anything**, including another `NULL`.

Remember:

```sql
NULL = NULL
```

does **not** evaluate to `TRUE`.

Instead, SQL returns **UNKNOWN**.

Always use:

```sql
IS NULL
```

or

```sql
IS NOT NULL
```

Never:

```sql
= NULL
```

______________________________________________________________________

# Common Mistakes

### Using `= NULL`

Incorrect

```sql
WHERE department_id = NULL;
```

Correct

```sql
WHERE department_id IS NULL;
```

______________________________________________________________________

### Forgetting Which Table Is Left

The "left" table is simply the table written immediately after `FROM`.

Example

```sql
FROM employees
LEFT JOIN departments
```

Employees is the left table.

______________________________________________________________________

### Assuming RIGHT JOIN Is Faster

It isn't.

The optimizer typically treats equivalent LEFT and RIGHT joins similarly. Choose the one that makes the query easiest to
read.

______________________________________________________________________

# Best Practices

- Prefer LEFT JOIN over RIGHT JOIN for readability.
- Use `IS NULL` to find missing relationships.
- Use FULL OUTER JOIN only when you truly need unmatched rows from both tables.
- Select only required columns.
- Join using indexed key columns.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** How would you find employees who are not assigned to any department?

Use a `LEFT JOIN` from `employees` to `departments` and filter where the department key from the right table is `NULL`.

```sql
SELECT e.employee_id, e.name
FROM employees e
LEFT JOIN departments d
ON e.department_id = d.department_id
WHERE d.department_id IS NULL;
```

This works because unmatched rows in the right table are represented with `NULL`.

______________________________________________________________________

# Practice Questions

### Conceptual

1. What is a LEFT JOIN?
1. What is a RIGHT JOIN?
1. What is a FULL OUTER JOIN?
1. Why is `IS NULL` used instead of `= NULL`?
1. Why is RIGHT JOIN less common?

### Coding

1. List all employees, including those without departments.
1. Find departments without employees.
1. Display all departments, even if they have no employees.
1. Return all employees and departments using a FULL OUTER JOIN.

______________________________________________________________________

# Hands-on Exercise

Using the Employees and Departments tables:

1. Write an INNER JOIN.
1. Write a LEFT JOIN.
1. Write a RIGHT JOIN.
1. Write a FULL OUTER JOIN.
1. Find employees without departments.
1. Find departments without employees.
1. Rewrite the LEFT JOIN using SQLAlchemy.
1. Rewrite the LEFT JOIN using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text
INNER JOIN
→ Matching rows only

LEFT JOIN
→ All left rows + matching right rows

RIGHT JOIN
→ All right rows + matching left rows

FULL OUTER JOIN
→ All rows from both tables

Use IS NULL
Never use = NULL
```

______________________________________________________________________

# Summary

In this part, you learned:

- LEFT JOIN
- RIGHT JOIN
- FULL OUTER JOIN
- Finding unmatched rows
- NULL behavior in joins
- SQLAlchemy equivalents
- SQLModel equivalents
- Common interview patterns
- Best practices

In the final part, we'll cover \*\*CROSS JOIN, SELF JOIN, multiple joins, `ON` vs `WHERE`, join execution strategies
(Nested Loop, Hash Join, Merge Join), performance considerations, and advanced interview questions.

______________________________________________________________________

## Next File

[Joins (Deep Dive) - Part 3](04-joins-deep-dive-part-3.md)
