# Joins (Deep Dive) - Part 3

## Introduction

In the previous parts, we covered:

- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- FULL OUTER JOIN

In this final part, we'll cover:

- CROSS JOIN
- SELF JOIN
- Multiple Table Joins
- `ON` vs `WHERE`
- Logical Query Execution Order
- Join Algorithms
- Join Performance
- Interview Tips

These topics are frequently discussed in senior backend interviews because they test not only SQL syntax but also your
understanding of how databases execute joins internally.

______________________________________________________________________

# CROSS JOIN

A **CROSS JOIN** returns the **Cartesian Product** of two tables.

Every row from the first table is combined with every row from the second table.

If:

- Table A has **3 rows**
- Table B has **4 rows**

The result contains:

```text
3 × 4 = 12 rows
```

______________________________________________________________________

## Example

### Employees

| Name |
| ----- |
| Alice |
| Bob |

### Projects

| Project |
| ------- |
| Alpha |
| Beta |
| Gamma |

Query

```sql
SELECT
    e.name,
    p.project
FROM employees e
CROSS JOIN projects p;
```

Result

| Name | Project |
| ----- | ------- |
| Alice | Alpha |
| Alice | Beta |
| Alice | Gamma |
| Bob | Alpha |
| Bob | Beta |
| Bob | Gamma |

______________________________________________________________________

## When is CROSS JOIN Useful?

Although uncommon, CROSS JOIN is useful for:

- Generating combinations
- Calendar generation
- Matrix reports
- Test data generation

______________________________________________________________________

## SQLAlchemy

```python
from sqlalchemy import select

stmt = (
    select(Employee.name, Project.project_name)
    .select_from(Employee)
    .join(Project, true())
)
```

> `true()` produces a Cartesian product. Be careful—this can generate very large result sets.

______________________________________________________________________

## SQLModel

```python
from sqlmodel import select
from sqlalchemy import true

statement = (
    select(Employee, Project)
    .join(Project, true())
)
```

______________________________________________________________________

# SELF JOIN

A SELF JOIN joins a table with itself.

It is useful when rows within the same table are related.

Example:

Employee → Manager

______________________________________________________________________

## Employees

| employee_id | name | manager_id |
| ----------: | ------- | ---------: |
| 1 | Alice | NULL |
| 2 | Bob | 1 |
| 3 | Charlie | 1 |
| 4 | David | 2 |

______________________________________________________________________

## SQL

```sql
SELECT
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.employee_id;
```

Result

| Employee | Manager |
| -------- | ------- |
| Alice | NULL |
| Bob | Alice |
| Charlie | Alice |
| David | Bob |

______________________________________________________________________

## SQLAlchemy

```python
from sqlalchemy.orm import aliased
from sqlalchemy import select

Manager = aliased(Employee)

stmt = (
    select(Employee.name, Manager.name)
    .join(
        Manager,
        Employee.manager_id == Manager.employee_id,
        isouter=True
    )
)
```

______________________________________________________________________

## SQLModel

SQLModel uses SQLAlchemy's `aliased()` for self joins.

______________________________________________________________________

# Multiple Table Joins

SQL can join more than two tables.

Example

```
Employees
      │
Departments
      │
Locations
      │
Countries
```

______________________________________________________________________

## SQL

```sql
SELECT
    e.name,
    d.department_name,
    l.city,
    c.country_name
FROM employees e
JOIN departments d
ON e.department_id = d.department_id
JOIN locations l
ON d.location_id = l.location_id
JOIN countries c
ON l.country_id = c.country_id;
```

There is no practical limit to the number of joins, but excessive joins can impact readability and performance.

______________________________________________________________________

# ON vs WHERE

This is one of the most common interview questions.

Many developers incorrectly assume they behave the same.

They do **not**.

______________________________________________________________________

## ON

`ON` specifies **how rows should be matched** during the join.

```sql
SELECT *
FROM employees e
JOIN departments d
ON e.department_id = d.department_id;
```

______________________________________________________________________

## WHERE

`WHERE` filters rows **after** the join has been performed.

```sql
SELECT *
FROM employees e
JOIN departments d
ON e.department_id = d.department_id
WHERE d.department_name = 'Engineering';
```

______________________________________________________________________

## Important Difference with LEFT JOIN

Consider:

```sql
SELECT
    e.name,
    d.department_name
FROM employees e
LEFT JOIN departments d
ON e.department_id = d.department_id
WHERE d.department_name = 'Engineering';
```

Although it starts as a LEFT JOIN, the `WHERE` clause removes rows where `department_name` is `NULL`.

Effectively, this behaves like an INNER JOIN.

Instead, if the filtering condition belongs to the relationship itself, place it in the `ON` clause.

```sql
SELECT
    e.name,
    d.department_name
FROM employees e
LEFT JOIN departments d
ON e.department_id = d.department_id
AND d.department_name = 'Engineering';
```

Now every employee is preserved, but only Engineering departments are matched.

This distinction is a classic interview question.

______________________________________________________________________

# Logical Query Execution Order

SQL is written in one order but logically processed in another.

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

DISTINCT

↓

ORDER BY

↓

LIMIT / OFFSET
```

Understanding this order explains why aliases cannot normally be referenced in `WHERE`, why `HAVING` works after
grouping, and why filtering in `ON` and `WHERE` can produce different results.

______________________________________________________________________

# How Databases Execute Joins

The optimizer chooses the best join algorithm based on statistics, indexes, and table sizes.

The three most common algorithms are:

- Nested Loop Join
- Hash Join
- Merge Join

______________________________________________________________________

# Nested Loop Join

One table is scanned row by row.

For each row, the database searches the matching rows in the second table.

```text
Employee 1
      ↓
Search Department

Employee 2
      ↓
Search Department
```

Good for:

- Small tables
- Indexed lookups

______________________________________________________________________

# Hash Join

The database builds an in-memory hash table from one relation.

The second table probes the hash table for matching keys.

Excellent for:

- Equality joins
- Large datasets

Frequently chosen by PostgreSQL.

______________________________________________________________________

# Merge Join

Both tables are sorted by the join key.

The database walks through both tables simultaneously.

Best when:

- Both inputs are already sorted
- Indexes provide ordered access

______________________________________________________________________

# Join Performance

Good join performance depends on:

- Appropriate indexes on join columns
- Selecting only required columns
- Avoiding unnecessary joins
- Filtering early when possible
- Keeping table statistics up to date

______________________________________________________________________

# Indexes and Joins

Joining on indexed columns is usually much faster.

Example

```sql
ON employees.department_id = departments.department_id
```

If both columns are indexed, the optimizer has more efficient execution strategies available.

______________________________________________________________________

# Common Mistakes

### Missing Join Condition

```sql
SELECT *
FROM employees
JOIN departments;
```

This results in a Cartesian product in systems that allow it or produces an error depending on the SQL dialect.

______________________________________________________________________

### Filtering in the Wrong Place

Understand whether a condition belongs in:

- `ON`
- `WHERE`

Especially for OUTER JOINs.

______________________________________________________________________

### Using SELECT \*

Retrieve only the required columns.

______________________________________________________________________

### Joining Unrelated Columns

Always join using logically related keys such as primary keys and foreign keys.

______________________________________________________________________

# Best Practices

- Prefer explicit `JOIN` syntax.
- Use meaningful aliases.
- Join on indexed columns.
- Avoid unnecessary CROSS JOINs.
- Understand how OUTER JOINs interact with `WHERE`.
- Examine execution plans for slow joins.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why can a LEFT JOIN behave like an INNER JOIN?

A LEFT JOIN preserves all rows from the left table by returning `NULL` for unmatched rows on the right. However, if the
`WHERE` clause filters on a column from the right table (for example, `WHERE d.department_name = 'Engineering'`), all
rows containing `NULL` are removed. As a result, only matched rows remain, making the query behave like an INNER JOIN.
To preserve unmatched rows, move such filtering conditions into the `ON` clause when appropriate.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a CROSS JOIN?
1. What is a SELF JOIN?
1. Explain the difference between `ON` and `WHERE`.
1. When is a Hash Join preferred?
1. What is a Cartesian Product?
1. Why can a LEFT JOIN become an INNER JOIN?

## Coding

1. Display every employee-project combination.
1. Display employees with their managers.
1. Join four related tables.
1. Rewrite a RIGHT JOIN using a LEFT JOIN.
1. Find employees without managers.
1. Explain the execution order of a join query.

______________________________________________________________________

# Hands-on Exercise

Create the following tables:

- Employees
- Departments
- Locations
- Countries
- Projects

Write queries to:

1. Perform a CROSS JOIN.
1. Perform a SELF JOIN.
1. Join four tables.
1. Demonstrate the difference between filtering in `ON` and `WHERE`.
1. Rewrite all queries using SQLAlchemy.
1. Rewrite all applicable queries using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text
INNER JOIN
→ Matching rows only

LEFT JOIN
→ All left rows

RIGHT JOIN
→ All right rows

FULL OUTER JOIN
→ All rows

CROSS JOIN
→ Cartesian Product

SELF JOIN
→ Table joined with itself

Remember

ON
→ Matching

WHERE
→ Filtering
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- CROSS JOIN
- SELF JOIN
- Multiple table joins
- `ON` vs `WHERE`
- Logical query execution order
- Nested Loop Join
- Hash Join
- Merge Join
- Join performance
- Indexing considerations
- SQLAlchemy equivalents
- SQLModel equivalents
- Common interview questions
- Best practices

You now have a complete understanding of SQL joins, from basic syntax to internal execution and performance
considerations.

______________________________________________________________________

## Next File

[Aggregations - Part 1](05-aggregations-part-1.md)
