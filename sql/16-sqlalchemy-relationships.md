# SQLAlchemy Relationships

## Introduction

Real-world databases rarely consist of a single table.

Consider an e-commerce application.

One customer can place many orders.

One order contains many products.

One product belongs to many orders.

These relationships are represented in SQL using **Foreign Keys** and in SQLAlchemy using the **relationship()**
function.

Understanding relationships is one of the most important SQLAlchemy interview topics because it forms the basis of
almost every production application.

In this chapter, you'll learn:

- One-to-One
- One-to-Many
- Many-to-One
- Many-to-Many
- Association Tables
- Cascades
- Lazy Loading
- Eager Loading
- `joinedload`
- `selectinload`
- `subqueryload`
- Performance considerations
- Interview questions

Throughout the lecture, we'll compare:

- SQL
- SQLAlchemy

______________________________________________________________________

# Sample Database

```text id="xjlwm01"
Department

1 ---- * Employee

Employee

* ---- * Project
```

______________________________________________________________________

# Foreign Key Review

SQL

```sql id="xjlwm02"
CREATE TABLE departments (

    department_id INTEGER PRIMARY KEY,

    department_name TEXT

);

CREATE TABLE employees (

    employee_id INTEGER PRIMARY KEY,

    department_id INTEGER
        REFERENCES departments(department_id)

);
```

The relationship already exists inside the database.

SQLAlchemy maps it into Python objects.

______________________________________________________________________

# relationship()

`relationship()` tells SQLAlchemy how two models are connected.

It does **not** create the foreign key.

The foreign key still belongs in the database schema.

______________________________________________________________________

# One-to-Many

One department has many employees.

One employee belongs to one department.

______________________________________________________________________

## Department Model

```python id="xjlwm03"
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Department(Base):

    __tablename__ = "departments"

    department_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    department_name: Mapped[str]

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department"
    )
```

______________________________________________________________________

## Employee Model

```python id="xjlwm04"
from sqlalchemy import ForeignKey

class Employee(Base):

    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.department_id")
    )

    department: Mapped["Department"] = relationship(
        back_populates="employees"
    )
```

______________________________________________________________________

# Equivalent SQL

```sql id="xjlwm05"
CREATE TABLE departments (

    department_id INTEGER PRIMARY KEY

);

CREATE TABLE employees (

    employee_id INTEGER PRIMARY KEY,

    department_id INTEGER
        REFERENCES departments(department_id)

);
```

______________________________________________________________________

# back_populates

Interview favorite.

```python id="xjlwm06"
back_populates="department"
```

Creates a bidirectional relationship.

You can navigate in both directions.

```python id="xjlwm07"
employee.department
```

```python id="xjlwm08"
department.employees
```

______________________________________________________________________

# Using Relationships

```python id="xjlwm09"
employee = session.get(Employee, 1)

print(employee.department.department_name)
```

Equivalent SQL

```sql id="xjlwm10"
SELECT *

FROM departments

WHERE department_id = ?;
```

SQLAlchemy loads the department automatically.

______________________________________________________________________

# Lazy Loading

Default behavior.

When this executes:

```python id="xjlwm11"
employee.department
```

SQLAlchemy sends another query.

Example

```text id="xjlwm12"
SELECT Employee

↓

SELECT Department
```

The related object is loaded only when accessed.

______________________________________________________________________

# Why Lazy Loading Can Be Slow

Suppose we load 100 employees.

```python id="xjlwm13"
employees = session.scalars(
    select(Employee)
).all()
```

Then

```python id="xjlwm14"
for employee in employees:

    print(employee.department.department_name)
```

Queries

```text id="xjlwm15"
1 Query

Employees

+

100 Queries

Departments
```

This is the **N+1 Query Problem**.

______________________________________________________________________

# Eager Loading

Instead of loading later,

load relationships immediately.

SQLAlchemy supports several eager loading strategies.

______________________________________________________________________

# joinedload()

Loads relationships using JOIN.

```python id="xjlwm16"
from sqlalchemy.orm import joinedload

stmt = (

    select(Employee)

    .options(

        joinedload(Employee.department)

    )

)
```

Equivalent SQL

```sql id="xjlwm17"
SELECT *

FROM employees

JOIN departments

ON employees.department_id =
departments.department_id;
```

Only one query.

______________________________________________________________________

# selectinload()

Interview favorite.

Instead of joining:

```text id="xjlwm18"
Query 1

Employees

↓

Query 2

Departments

WHERE id IN (...)
```

Example

```python id="xjlwm19"
from sqlalchemy.orm import selectinload

stmt = (

    select(Employee)

    .options(

        selectinload(Employee.department)

    )

)
```

Usually performs very well for one-to-many relationships.

______________________________________________________________________

# subqueryload()

Loads related objects using a subquery.

```python id="xjlwm20"
from sqlalchemy.orm import subqueryload

stmt = (

    select(Employee)

    .options(

        subqueryload(Employee.department)

    )

)
```

Less common today than `selectinload()`, but still useful in certain scenarios.

______________________________________________________________________

# joinedload vs selectinload

| joinedload | selectinload |
| -------------------------------- | ------------------------------- |
| JOIN | Two Queries |
| Larger result set | Smaller result sets |
| Good for many-to-one | Often preferred for one-to-many |
| Can duplicate parent rows in SQL | Avoids row multiplication |

Interview Tip

Don't memorize one as "better."

Choose based on:

- Relationship type
- Data size
- Query pattern

______________________________________________________________________

# Many-to-One

Many employees belong to one department.

From Employee's perspective

```python id="xjlwm21"
employee.department
```

This is many-to-one.

______________________________________________________________________

# One-to-One

Example

Employee

↓

EmployeeProfile

Each employee has exactly one profile.

```python id="xjlwm22"
profile: Mapped["Profile"] = relationship(
    back_populates="employee",
    uselist=False
)
```

`uselist=False` tells SQLAlchemy the relationship returns a single object instead of a list.

The database should also enforce one-to-one using a `UNIQUE` constraint on the foreign key.

______________________________________________________________________

# Many-to-Many

Employees

↓

Projects

One employee works on many projects.

One project has many employees.

Requires an association table.

______________________________________________________________________

# Association Table

```python id="xjlwm23"
employee_project = Table(

    "employee_project",

    Base.metadata,

    Column(
        "employee_id",
        ForeignKey("employees.employee_id"),
        primary_key=True
    ),

    Column(
        "project_id",
        ForeignKey("projects.project_id"),
        primary_key=True
    )

)
```

______________________________________________________________________

# Employee Model

```python id="xjlwm24"
projects: Mapped[list["Project"]] = relationship(

    secondary=employee_project,

    back_populates="employees"

)
```

______________________________________________________________________

# Project Model

```python id="xjlwm25"
employees: Mapped[list["Employee"]] = relationship(

    secondary=employee_project,

    back_populates="projects"

)
```

______________________________________________________________________

# Equivalent SQL

```text id="xjlwm26"
Employees

↓

Employee_Project

↓

Projects
```

Exactly the same database design as pure SQL.

______________________________________________________________________

# Cascades

What happens when a parent object is deleted?

Example

```python id="xjlwm27"
relationship(

    cascade="all, delete-orphan"

)
```

Common cascade options:

- save-update
- merge
- delete
- delete-orphan
- refresh-expire
- expunge

`all` is a shorthand for several common cascade behaviors.

______________________________________________________________________

# delete-orphan

Suppose

Department

↓

Employees

If an employee is removed from

```python id="xjlwm28"
department.employees
```

the employee row is automatically deleted when `delete-orphan` is configured.

Use carefully—it permanently deletes orphaned child rows.

______________________________________________________________________

# Relationship Loading Summary

| Strategy | Queries | Typical Use |
| ------------ | ------: | ------------------------ |
| Lazy | Many | Small datasets |
| joinedload | One | Many-to-one / one-to-one |
| selectinload | Two | One-to-many |
| subqueryload | Two | Specialized scenarios |

______________________________________________________________________

# SQLAlchemy Best Practices

- Always define Foreign Keys.
- Use `back_populates` instead of the older `backref` unless you specifically need automatic relationship creation.
- Prefer `selectinload()` for large one-to-many collections.
- Prefer `joinedload()` for many-to-one lookups.
- Avoid lazy loading inside loops.
- Understand the SQL generated by your ORM queries.

______________________________________________________________________

# Common Mistakes

### Forgetting ForeignKey

`relationship()` alone is not enough.

______________________________________________________________________

### Using Lazy Loading Everywhere

Can easily produce N+1 queries.

______________________________________________________________________

### Assuming joinedload Is Always Best

Large joins can duplicate parent rows and transfer much more data than necessary.

______________________________________________________________________

### Missing UNIQUE Constraint in One-to-One

`uselist=False` affects the ORM only.

The database must enforce one-to-one with a unique constraint.

______________________________________________________________________

### Misunderstanding Cascades

ORM cascade behavior is different from database `ON DELETE CASCADE`.

They solve related but different problems.

______________________________________________________________________

# Performance Considerations

- Measure before changing loading strategies.
- Inspect generated SQL.
- Avoid loading relationships you don't use.
- Prefer eager loading for predictable access patterns.
- Use indexes on foreign key columns.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between `joinedload()` and `selectinload()`?

`joinedload()` retrieves related objects using a SQL JOIN, allowing everything to be loaded in a single query. It works
well for many-to-one and one-to-one relationships but can produce duplicate parent rows when loading collections.
`selectinload()` executes a second query using an `IN` clause to fetch all related objects for the previously loaded
parents. It often performs better for one-to-many relationships because it avoids row multiplication and usually
transfers less redundant data.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is `relationship()`?
1. What does `back_populates` do?
1. Explain one-to-many relationships.
1. Explain many-to-many relationships.
1. What is an association table?
1. Difference between lazy and eager loading.
1. Difference between `joinedload()` and `selectinload()`.
1. What is `delete-orphan`?
1. Difference between ORM cascade and database cascade.
1. Why does the N+1 query problem occur?

## Coding

1. Create Department and Employee models.
1. Create a one-to-many relationship.
1. Create Employee and Project models with a many-to-many relationship.
1. Load employees with departments using `joinedload()`.
1. Load departments with employees using `selectinload()`.
1. Configure cascading deletes appropriately.

______________________________________________________________________

# Hands-on Exercise

Build a small company database.

Requirements:

1. Employee → Department (Many-to-One)
1. Department → Employees (One-to-Many)
1. Employee ↔ Project (Many-to-Many)
1. Insert sample data.
1. Query employees with departments.
1. Query departments with employees.
1. Compare lazy loading and eager loading.
1. Measure the number of SQL queries generated.
1. Rewrite the generated SQL manually to understand what SQLAlchemy is doing.

______________________________________________________________________

# Cheat Sheet

```text id="xjlwm29"
relationship()

↓

One-to-One

One-to-Many

Many-to-One

Many-to-Many

↓

back_populates

↓

Loading

Lazy

joinedload

selectinload

subqueryload

↓

Cascade

delete-orphan
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- `relationship()`
- One-to-One relationships
- One-to-Many relationships
- Many-to-One relationships
- Many-to-Many relationships
- Association tables
- `back_populates`
- Lazy loading
- Eager loading
- `joinedload()`
- `selectinload()`
- `subqueryload()`
- Cascades
- `delete-orphan`
- ORM vs database cascades
- Performance considerations
- Interview patterns
- Best practices

You now understand how SQLAlchemy models relationships, loads related objects efficiently, and how to choose the
appropriate loading strategy for different application scenarios.

______________________________________________________________________

## Next File

[SQLAlchemy Advanced Queries](17-sqlalchemy-advanced-queries.md)
