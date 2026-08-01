# Constraints & Indexes

## Introduction

A database is only as good as the quality of the data it stores.

Imagine an employee table where:

- Two employees have the same Employee ID.
- An order references a customer that doesn't exist.
- A salary is negative.
- A user's email is duplicated.
- A product has no name.

These issues can lead to inconsistent and unreliable data.

**Constraints** help maintain data integrity by enforcing rules on the data stored in a table.

On the other hand, **Indexes** improve query performance by allowing the database to locate rows efficiently without
scanning the entire table.

Constraints and indexes are among the most frequently discussed topics in SQL interviews because they directly affect
both **correctness** and **performance**.

______________________________________________________________________

# What are Constraints?

A constraint is a rule applied to one or more columns to ensure that only valid data is stored.

Common constraints:

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE
- NOT NULL
- CHECK
- DEFAULT

______________________________________________________________________

# PRIMARY KEY

A PRIMARY KEY uniquely identifies every row in a table.

Properties:

- Unique
- Cannot contain NULL
- One PRIMARY KEY per table
- Can consist of one or more columns

Example

```sql id="u5bgso"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100)
);
```

Example

```text id="ny9gw9"
Employee ID

1
2
3
4
```

Duplicate values are rejected.

______________________________________________________________________

# Composite PRIMARY KEY

A PRIMARY KEY can consist of multiple columns.

Example

```sql id="p1lv9m"
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id)
);
```

Here:

```text id="mxvwv0"
student_id + course_id
```

together uniquely identify each enrollment.

______________________________________________________________________

# FOREIGN KEY

A FOREIGN KEY creates a relationship between two tables.

Example

```sql id="x0oqeu"
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    department_id INT,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);
```

The database prevents inserting an employee with a department that does not exist.

______________________________________________________________________

# ON DELETE Actions

Interview question.

Suppose a department is deleted.

What should happen to employees?

SQL provides several options.

______________________________________________________________________

## CASCADE

Delete child rows automatically.

```sql id="ml7kwy"
FOREIGN KEY (department_id)
REFERENCES departments(department_id)
ON DELETE CASCADE
```

Deleting a department deletes all related employees.

______________________________________________________________________

## SET NULL

```sql id="owoe3j"
ON DELETE SET NULL
```

The foreign key becomes NULL.

Useful when the relationship is optional.

______________________________________________________________________

## RESTRICT

```sql id="ybysq9"
ON DELETE RESTRICT
```

Prevent deletion if dependent rows exist.

Many databases also support `NO ACTION`, which is similar in effect, although the exact timing of constraint checking
can differ depending on the database.

______________________________________________________________________

# UNIQUE

Ensures all values are unique.

Example

```sql id="vxlz1v"
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    email VARCHAR(255) UNIQUE
);
```

Duplicate email addresses are rejected.

Unlike a PRIMARY KEY:

- Multiple UNIQUE constraints can exist.
- Most databases allow NULL values in UNIQUE columns, but the exact behavior varies by database engine.

______________________________________________________________________

# NOT NULL

Ensures a column always contains a value.

```sql id="nlxzzs"
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```

Attempting to insert NULL fails.

______________________________________________________________________

# CHECK

Validates data using an expression.

Example

```sql id="0ckivl"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    salary DECIMAL(10,2),
    CHECK (salary >= 0)
);
```

Negative salaries are rejected.

Another example

```sql id="6r5m9z"
CHECK (
    age >= 18
)
```

______________________________________________________________________

# DEFAULT

Assigns a default value when none is provided.

Example

```sql id="jjlwm2"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    status VARCHAR(20)
    DEFAULT 'ACTIVE'
);
```

If status is omitted, it becomes:

```text id="c41x20"
ACTIVE
```

______________________________________________________________________

# Constraint Comparison

| Constraint | Purpose |
| ----------- | --------------------------- |
| PRIMARY KEY | Unique row identifier |
| FOREIGN KEY | Relationship between tables |
| UNIQUE | Prevent duplicates |
| NOT NULL | Prevent NULL values |
| CHECK | Validate data |
| DEFAULT | Supply default value |

______________________________________________________________________

# SQLAlchemy Constraints

Example

```python id="4vfjlwm"
from sqlalchemy import (
    Column,
    Integer,
    String,
    CheckConstraint,
    ForeignKey
)

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(
        Integer,
        primary_key=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    __table_args__ = (
        CheckConstraint("salary >= 0"),
    )
```

______________________________________________________________________

# SQLModel Constraints

```python id="xiwkmo"
from sqlmodel import SQLModel, Field

class Employee(SQLModel, table=True):

    employee_id: int = Field(
        primary_key=True
    )

    email: str = Field(
        unique=True
    )

    department_id: int | None = Field(
        foreign_key="departments.department_id"
    )
```

Complex constraints such as `CheckConstraint` are typically added through SQLAlchemy table arguments because SQLModel
builds on top of SQLAlchemy.

______________________________________________________________________

# What is an Index?

An index is a data structure that allows the database to find rows quickly.

Without an index

```text id="j4mw98"
Book

↓

Page 1

↓

Page 2

↓

Page 3

↓

...

↓

Page 500
```

The database may need to scan every row.

With an index

```text id="3o72sh"
Index

↓

Employee ID

↓

Jump directly to row
```

This significantly reduces lookup time.

______________________________________________________________________

# Why are Indexes Fast?

Most relational databases implement indexes using **B-Tree** structures (or variants such as B+ Trees).

Instead of scanning every row, the database traverses the tree to locate matching values efficiently.

Conceptually:

```text id="b8i66a"
Root

↓

Branch

↓

Leaf

↓

Matching Row
```

The exact implementation depends on the database engine.

______________________________________________________________________

# Creating an Index

```sql id="jlwmm8"
CREATE INDEX idx_employee_name
ON employees(name);
```

______________________________________________________________________

# Composite Index

Indexes can contain multiple columns.

```sql id="cmulux"
CREATE INDEX idx_department_salary
ON employees(
    department_id,
    salary
);
```

Useful for queries like:

```sql id="z0rgmx"
WHERE department_id = 2
AND salary > 80000
```

______________________________________________________________________

# How Composite Indexes Work

Given an index on:

```text id="wsk3eu"
(department_id, salary)
```

These queries can use it efficiently:

```sql id="b8yv3g"
WHERE department_id = 1
```

```sql id="5qqyod"
WHERE department_id = 1
AND salary > 70000
```

This usually **cannot** use the index efficiently:

```sql id="8s26p9"
WHERE salary > 70000
```

This is known as the **leftmost prefix rule** for B-tree indexes.

______________________________________________________________________

# Unique Index

A UNIQUE constraint is generally backed by a unique index.

You can also create unique indexes directly.

```sql id="x3cmut"
CREATE UNIQUE INDEX idx_email
ON users(email);
```

______________________________________________________________________

# Partial Index (PostgreSQL)

A partial index indexes only rows matching a condition.

```sql id="djlwm1"
CREATE INDEX idx_active_users
ON users(email)
WHERE status = 'ACTIVE';
```

Useful when only a subset of rows is queried frequently.

______________________________________________________________________

# Covering Index

A covering index contains all columns required by a query.

Example

```sql id="djlwm2"
CREATE INDEX idx_orders_customer_status
ON orders(customer_id, status);
```

Query

```sql id="4w5v3a"
SELECT customer_id, status
FROM orders
WHERE customer_id = 10;
```

The database may satisfy the query using only the index, avoiding access to the base table. The exact behavior depends
on the database engine.

______________________________________________________________________

# Clustered vs Non-Clustered Index

Interview concept.

## Clustered Index

The table's data is stored in the same order as the index.

Only one clustered ordering can exist because the data itself has only one physical order.

## Non-Clustered Index

A separate structure that points to the table rows.

A table can have many non-clustered indexes.

Different databases implement clustered storage differently, so treat this as a conceptual distinction unless working
with a specific database.

______________________________________________________________________

# When Indexes Hurt Performance

Indexes speed up reads.

They slow down writes because every INSERT, UPDATE, and DELETE may also need to update the index.

Avoid creating indexes on:

- Very small tables
- Columns with very low selectivity (for example, a boolean column with mostly identical values)
- Columns that are rarely searched

Balance read performance against write overhead.

______________________________________________________________________

# Finding Missing Indexes

Symptoms include:

- Frequent sequential scans on large tables
- Slow JOIN operations
- Slow WHERE filters
- Slow ORDER BY operations
- Slow GROUP BY operations

Tools like `EXPLAIN` and `EXPLAIN ANALYZE` help identify these issues and will be covered in the next lecture.

______________________________________________________________________

# Common Mistakes

### Creating Too Many Indexes

Every additional index increases storage usage and write cost.

______________________________________________________________________

### Indexing Every Column

Only index columns that are frequently used in:

- WHERE
- JOIN
- ORDER BY
- GROUP BY

______________________________________________________________________

### Ignoring Composite Index Order

The order of columns inside a composite index matters.

______________________________________________________________________

### Assuming an Index Is Always Used

The optimizer may choose a sequential scan if it estimates that scanning the table is cheaper.

______________________________________________________________________

# Best Practices

- Always define PRIMARY KEYs.
- Use FOREIGN KEYs to maintain relationships.
- Use CHECK constraints to protect data quality.
- Use NOT NULL whenever appropriate.
- Create indexes based on query patterns, not guesswork.
- Review execution plans before adding new indexes.
- Remove unused indexes to reduce maintenance overhead.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between a PRIMARY KEY and a UNIQUE constraint?

A PRIMARY KEY uniquely identifies each row and does not allow NULL values. A table can have only one PRIMARY KEY,
although it may consist of multiple columns. A UNIQUE constraint also prevents duplicate values, but a table can have
multiple UNIQUE constraints. Additionally, most databases allow NULL values in UNIQUE columns, although the exact
behavior depends on the database engine.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is a constraint?
1. Explain PRIMARY KEY.
1. Explain FOREIGN KEY.
1. Difference between PRIMARY KEY and UNIQUE.
1. What is a CHECK constraint?
1. What is a DEFAULT constraint?
1. What is an index?
1. Explain composite indexes.
1. What is the leftmost prefix rule?
1. Why do indexes slow down writes?

## Coding

1. Create Employees and Departments tables with appropriate constraints.
1. Create a composite PRIMARY KEY.
1. Create a UNIQUE index on email.
1. Create a composite index on department and salary.
1. Create a CHECK constraint to prevent negative salaries.
1. Add a DEFAULT value for employee status.

______________________________________________________________________

# Hands-on Exercise

Create the following tables:

- Employees
- Departments
- Projects
- Assignments

Requirements:

1. Use PRIMARY KEYs.
1. Add FOREIGN KEY relationships.
1. Add NOT NULL constraints where appropriate.
1. Prevent duplicate emails.
1. Prevent negative salaries.
1. Create indexes to optimize employee lookups by department and salary.
1. Implement the schema using SQLAlchemy.
1. Implement the schema using SQLModel.

______________________________________________________________________

# Cheat Sheet

```text id="jlwm3"
Constraints

PRIMARY KEY
FOREIGN KEY
UNIQUE
NOT NULL
CHECK
DEFAULT

↓

Indexes

Single Column
Composite
Unique
Partial
Covering

↓

Read Faster
Write Slower
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- PRIMARY KEY
- Composite PRIMARY KEY
- FOREIGN KEY
- ON DELETE actions
- UNIQUE
- NOT NULL
- CHECK
- DEFAULT
- SQLAlchemy constraints
- SQLModel constraints
- Index fundamentals
- Composite indexes
- Partial indexes
- Covering indexes
- Clustered vs Non-Clustered indexes
- Leftmost prefix rule
- Index trade-offs
- Best practices
- Interview patterns

You now understand how constraints protect data integrity and how indexes improve query performance—two essential
concepts for designing reliable and efficient relational databases.

______________________________________________________________________

## Next File

[Query Optimization & Execution Plans - Part 1](09-query-optimization-part-1.md)
