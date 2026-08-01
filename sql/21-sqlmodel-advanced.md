# SQLModel Advanced & Production Patterns

## Introduction

In the previous lecture, you learned the fundamentals of SQLModel:

- Models
- CRUD
- Sessions
- Filtering
- Ordering
- Pagination

In this chapter, we'll move to production-level SQLModel development.

Topics include:

- Relationships
- Joins
- Aggregations
- Transactions
- Eager Loading
- Advanced Queries
- Performance
- Repository Pattern
- FastAPI Dependency Injection
- Best Practices
- Interview Questions

Remember:

**SQLModel is built on top of SQLAlchemy.**

Many advanced SQLModel features are actually powered by SQLAlchemy internally.

______________________________________________________________________

# Relationships

Relationships work similarly to SQLAlchemy.

Example

```python id="smadv001"
from typing import Optional

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

class Department(SQLModel, table=True):

    department_id: int | None = Field(
        default=None,
        primary_key=True
    )

    department_name: str

    employees: list["Employee"] = Relationship(
        back_populates="department"
    )
```

Employee

```python id="smadv002"
class Employee(SQLModel, table=True):

    employee_id: int | None = Field(
        default=None,
        primary_key=True
    )

    department_id: int = Field(
        foreign_key="department.department_id"
    )

    department: Optional["Department"] = Relationship(
        back_populates="employees"
    )
```

______________________________________________________________________

# Equivalent SQL

```sql id="smadv003"
CREATE TABLE department (

    department_id INTEGER PRIMARY KEY,

    department_name TEXT

);

CREATE TABLE employee (

    employee_id INTEGER PRIMARY KEY,

    department_id INTEGER
        REFERENCES department(department_id)

);
```

______________________________________________________________________

# One-to-Many

One Department

↓

Many Employees

```python id="smadv004"
department.employees
```

______________________________________________________________________

# Many-to-One

Many Employees

↓

One Department

```python id="smadv005"
employee.department
```

______________________________________________________________________

# Many-to-Many

Many-to-many relationships require a **link model**.

Example

```python id="smadv006"
class EmployeeProjectLink(SQLModel, table=True):

    employee_id: int = Field(
        foreign_key="employee.employee_id",
        primary_key=True
    )

    project_id: int = Field(
        foreign_key="project.project_id",
        primary_key=True
    )
```

Employee

```python id="smadv007"
projects: list["Project"] = Relationship(
    back_populates="employees",
    link_model=EmployeeProjectLink
)
```

Project

```python id="smadv008"
employees: list["Employee"] = Relationship(
    back_populates="projects",
    link_model=EmployeeProjectLink
)
```

______________________________________________________________________

# Querying Relationships

```python id="smadv009"
statement = select(Employee)

employees = session.exec(
    statement
).all()
```

Later

```python id="smadv010"
employee.department
```

This may trigger an additional SQL query if the relationship wasn't eagerly loaded.

______________________________________________________________________

# SQLModel Uses SQLAlchemy Loading

SQLModel supports SQLAlchemy loading strategies.

Examples include:

- `selectinload()`
- `joinedload()`
- `subqueryload()`

______________________________________________________________________

# Example

```python id="smadv011"
from sqlalchemy.orm import selectinload

statement = (
    select(Employee)
    .options(
        selectinload(Employee.department)
    )
)
```

Equivalent SQL

```sql id="smadv012"
SELECT *
FROM employee;

SELECT *
FROM department
WHERE department_id IN (...);
```

______________________________________________________________________

# Joins

```python id="smadv013"
statement = (
    select(
        Employee,
        Department
    )
    .join(Department)
)
```

Equivalent SQL

```sql id="smadv014"
SELECT *
FROM employee
JOIN department
ON employee.department_id =
department.department_id;
```

______________________________________________________________________

# Filtering

```python id="smadv015"
statement = (
    select(Employee)
    .where(
        Employee.salary > 80000
    )
)
```

Equivalent SQL

```sql id="smadv016"
SELECT *
FROM employee
WHERE salary > 80000;
```

______________________________________________________________________

# Aggregations

```python id="smadv017"
from sqlalchemy import func

statement = (
    select(
        Employee.department_id,
        func.count()
    )
    .group_by(
        Employee.department_id
    )
)
```

Equivalent SQL

```sql id="smadv018"
SELECT
department_id,
COUNT(*)
FROM employee
GROUP BY department_id;
```

______________________________________________________________________

# HAVING

```python id="smadv019"
statement = (
    select(
        Employee.department_id,
        func.count()
    )
    .group_by(
        Employee.department_id
    )
    .having(
        func.count() > 5
    )
)
```

Equivalent SQL

```sql id="smadv020"
SELECT
department_id,
COUNT(*)
FROM employee
GROUP BY department_id
HAVING COUNT(*) > 5;
```

______________________________________________________________________

# Window Functions

SQLModel uses SQLAlchemy's window function support.

```python id="smadv021"
from sqlalchemy import func

statement = (
    select(
        Employee.name,
        func.rank().over(
            order_by=Employee.salary.desc()
        )
    )
)
```

Equivalent SQL

```sql id="smadv022"
SELECT
name,
RANK()
OVER(
ORDER BY salary DESC
)
FROM employee;
```

______________________________________________________________________

# Transactions

```python id="smadv023"
with Session(engine) as session:

    try:

        employee = Employee(
            name="Alice",
            salary=70000
        )

        session.add(employee)

        session.commit()

    except:

        session.rollback()

        raise
```

______________________________________________________________________

# Bulk Inserts

```python id="smadv024"
employees = [
    Employee(name="A", salary=60000),
    Employee(name="B", salary=70000)
]

session.add_all(employees)

session.commit()
```

______________________________________________________________________

# Repository Pattern

A repository isolates database access.

Example

```python id="smadv025"
class EmployeeRepository:

    def get_all(
        self,
        session: Session
    ):
        return session.exec(
            select(Employee)
        ).all()
```

Advantages

- Easier testing
- Cleaner architecture
- Reusable queries

______________________________________________________________________

# Service Layer

Keep business logic separate from database logic.

Example

```text id="smadv026"
FastAPI Route

↓

Service

↓

Repository

↓

Database
```

Responsibilities

Repository:

- Data access

Service:

- Business rules

API:

- HTTP request/response

______________________________________________________________________

# FastAPI Dependency Injection

A common pattern

```python id="smadv027"
from typing import Generator

def get_session() -> Generator:

    with Session(engine) as session:

        yield session
```

Usage

```python id="smadv028"
from fastapi import Depends

@app.get("/employees")
def get_employees(

    session: Session = Depends(get_session)

):
    return session.exec(
        select(Employee)
    ).all()
```

This creates one Session per request.

______________________________________________________________________

# Performance Considerations

### Avoid N+1 Queries

Use

```python id="smadv029"
selectinload()
```

when appropriate.

______________________________________________________________________

### Select Required Columns

Instead of returning every column, return only what is needed.

______________________________________________________________________

### Batch Operations

Use

```python id="smadv030"
add_all()
```

for multiple inserts.

______________________________________________________________________

### Keep Transactions Short

Commit promptly.

Avoid user interaction while a transaction is open.

______________________________________________________________________

### Understand Generated SQL

SQLModel is still SQLAlchemy underneath.

Always understand the SQL being executed.

______________________________________________________________________

# Common Mistakes

### Treating SQLModel as Magic

Learn the underlying SQLAlchemy concepts.

______________________________________________________________________

### Returning ORM Models Everywhere

For public APIs, consider dedicated response models to avoid exposing internal fields or relationships unintentionally.

______________________________________________________________________

### Ignoring Query Performance

ORMs don't automatically optimize queries.

______________________________________________________________________

### Forgetting Relationship Loading

Lazy loading inside loops can create N+1 problems.

______________________________________________________________________

### Large Transactions

Long-running transactions reduce concurrency.

______________________________________________________________________

# Best Practices

- Learn SQL first.
- Learn SQLAlchemy second.
- Use SQLModel to reduce boilerplate.
- Keep Sessions short.
- Use one Session per request.
- Prefer Repository + Service architecture for larger applications.
- Profile SQL before optimizing.
- Use Alembic for schema migrations.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Should SQLModel replace SQLAlchemy in all projects?

No. SQLModel is an excellent choice for FastAPI applications because it combines SQLAlchemy and Pydantic into a concise
API. However, SQLAlchemy remains the more flexible and feature-rich ORM. Projects requiring advanced ORM customization,
complex mappings, or full access to SQLAlchemy's capabilities may benefit from using SQLAlchemy directly. Since SQLModel
is built on SQLAlchemy, understanding SQLAlchemy is valuable regardless of which library is used.

______________________________________________________________________

# Practice Questions

## Conceptual

1. How are relationships defined in SQLModel?
1. What is a link model?
1. Why does SQLModel use SQLAlchemy loading strategies?
1. How do you perform joins?
1. How do you perform aggregations?
1. What is the Repository Pattern?
1. Why use a Service Layer?
1. Why create one Session per request?
1. How do you avoid N+1 queries?
1. Why should you understand generated SQL?

## Coding

1. Create Department and Employee relationships.
1. Create a many-to-many relationship using a link model.
1. Join employees and departments.
1. Calculate average salary by department.
1. Rank employees by salary.
1. Build a repository class.
1. Implement FastAPI dependency injection for Sessions.

______________________________________________________________________

# Hands-on Exercise

Extend the Employee Management API.

Requirements:

1. Create Department and Project models.
1. Implement one-to-many relationships.
1. Implement many-to-many relationships.
1. Retrieve employees with departments.
1. Aggregate salaries by department.
1. Use eager loading to avoid N+1 queries.
1. Build a repository layer.
1. Build a service layer.
1. Integrate everything into FastAPI.

______________________________________________________________________

# Cheat Sheet

```text id="smadv031"
SQLModel

↓

Relationships

↓

Link Models

↓

Joins

↓

Aggregations

↓

Window Functions

↓

Repository

↓

Service Layer

↓

FastAPI

↓

Performance
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- SQLModel relationships
- One-to-many relationships
- Many-to-many relationships
- Link models
- Joins
- Aggregations
- Window functions
- Transactions
- Repository Pattern
- Service Layer
- FastAPI dependency injection
- Performance optimization
- Best practices
- Interview patterns

You now understand how to build production-ready applications using SQLModel while leveraging the power of SQLAlchemy
underneath.

______________________________________________________________________

## Next File

[SQLModel Interview Masterclass](22-sqlmodel-interview-masterclass.md)
