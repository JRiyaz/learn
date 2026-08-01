# SQLModel Interview Masterclass

## Introduction

This chapter is a complete interview revision guide for SQLModel.

Unlike previous chapters, this lecture focuses on:

- Frequently asked interview questions
- Production scenarios
- Coding problems
- Architecture discussions
- Best practices
- Common mistakes

If you can comfortably answer the questions in this chapter, you'll be well prepared for SQLModel interviews and FastAPI
backend interviews.

______________________________________________________________________

# Beginner Questions

## 1. What is SQLModel?

### Answer

SQLModel is a Python ORM library built on top of SQLAlchemy and Pydantic.

It combines:

- SQLAlchemy ORM
- Pydantic validation
- Python type hints

into a single model definition.

Example

```python
from sqlmodel import SQLModel
from sqlmodel import Field

class Employee(SQLModel, table=True):

    employee_id: int | None = Field(
        default=None,
        primary_key=True
    )

    name: str
```

______________________________________________________________________

## 2. Why was SQLModel created?

### Answer

Traditional FastAPI applications often required three models:

- SQLAlchemy ORM model
- Pydantic request model
- Pydantic response model

SQLModel reduces duplication by allowing one model to serve multiple purposes in many cases.

______________________________________________________________________

## 3. Is SQLModel a replacement for SQLAlchemy?

### Answer

No.

SQLModel is built on top of SQLAlchemy.

Internally it still uses:

- SQLAlchemy Engine
- SQLAlchemy Session
- SQLAlchemy ORM
- SQLAlchemy Query System

Knowing SQLAlchemy makes SQLModel much easier to understand.

______________________________________________________________________

## 4. SQLAlchemy vs SQLModel

| SQLAlchemy | SQLModel |
| ------------------- | ---------------------------- |
| Mature ORM | Wrapper around SQLAlchemy |
| More configuration | Less boilerplate |
| Maximum flexibility | Faster development |
| Works everywhere | Especially good with FastAPI |

______________________________________________________________________

## 5. What does `table=True` do?

```python
class Employee(
    SQLModel,
    table=True
):
    ...
```

### Answer

It tells SQLModel that this class represents a database table.

Without it, the class behaves only as a data model and is not mapped to the database.

______________________________________________________________________

# Intermediate Questions

## 6. What is `Field()`?

Example

```python
employee_id: int | None = Field(
    default=None,
    primary_key=True
)
```

Equivalent SQLAlchemy

```python
mapped_column(
    primary_key=True
)
```

### Answer

`Field()` configures:

- Primary keys
- Foreign keys
- Defaults
- Constraints
- Metadata

______________________________________________________________________

## 7. Why call `session.refresh()`?

Example

```python
employee = Employee(
    name="Alice"
)

session.add(employee)
session.commit()

session.refresh(employee)
```

### Answer

The database generates values such as:

- Primary key
- Identity column
- Database defaults

`refresh()` reloads the object so those generated values are available.

______________________________________________________________________

## 8. Difference Between `exec()` and `execute()`

SQLModel

```python
employees = session.exec(
    select(Employee)
).all()
```

SQLAlchemy

```python
employees = session.execute(
    select(Employee)
)
```

### Answer

`exec()` is SQLModel's convenience wrapper around SQLAlchemy execution APIs.

It returns results in a simpler form for common ORM use cases.

______________________________________________________________________

## 9. How Do Relationships Work?

Example

```python
class Department(SQLModel, table=True):

    employees: list["Employee"] = Relationship(
        back_populates="department"
    )
```

Employee

```python
department: Department | None = Relationship(
    back_populates="employees"
)
```

### Answer

Relationships are implemented using SQLAlchemy underneath.

______________________________________________________________________

## 10. Why Use a Link Model?

Example

```python
class EmployeeProjectLink(
    SQLModel,
    table=True
):

    employee_id: int = Field(
        foreign_key="employee.employee_id",
        primary_key=True
    )

    project_id: int = Field(
        foreign_key="project.project_id",
        primary_key=True
    )
```

### Answer

A link model represents a many-to-many relationship and corresponds to an association table in SQL.

______________________________________________________________________

# Advanced Questions

## 11. How Does SQLModel Avoid Boilerplate?

Traditional approach

```text
SQLAlchemy Model

↓

Pydantic Request

↓

Pydantic Response
```

SQLModel

```text
Single Model

↓

Database

+

Validation
```

For larger systems, many teams still use separate request and response models to keep API contracts independent of
persistence models.

______________________________________________________________________

## 12. Why Learn SQLAlchemy First?

### Answer

Because SQLModel internally uses SQLAlchemy.

Understanding SQLAlchemy helps with:

- Performance tuning
- Relationships
- Query optimization
- Transactions
- Loading strategies
- Advanced ORM features

______________________________________________________________________

## 13. How Are Transactions Managed?

```python
with Session(engine) as session:

    try:

        ...

        session.commit()

    except:

        session.rollback()

        raise
```

SQLModel relies entirely on SQLAlchemy's transaction management.

______________________________________________________________________

## 14. How Do You Prevent N+1 Queries?

Bad

```python
employees = session.exec(
    select(Employee)
).all()

for employee in employees:
    print(employee.department)
```

Better

```python
from sqlalchemy.orm import selectinload

statement = (
    select(Employee)
    .options(
        selectinload(Employee.department)
    )
)

employees = session.exec(statement).all()
```

______________________________________________________________________

## 15. How Do You Build FastAPI Applications?

Recommended architecture

```text
Route

↓

Service

↓

Repository

↓

Database
```

Avoid placing business logic directly in route handlers.

______________________________________________________________________

# Production Questions

## 16. Why Not Use Global Sessions?

Global Sessions may:

- Leak connections
- Keep stale objects
- Cause concurrency issues
- Create long-running transactions

Instead

```python
from sqlmodel import Session

def get_session():

    with Session(engine) as session:

        yield session
```

______________________________________________________________________

## 17. Why Use Alembic?

`create_all()` only creates missing tables.

Production applications require:

- Versioned schema changes
- Rollbacks
- Team collaboration

Alembic provides these capabilities.

______________________________________________________________________

## 18. Why Separate Repository and Service Layers?

Repository

- Database access

Service

- Business rules

API

- HTTP layer

This separation improves maintainability and testing.

______________________________________________________________________

## 19. SQLModel vs Django ORM

| SQLModel | Django ORM |
| ---------------------- | --------------------- |
| Built on SQLAlchemy | Built into Django |
| Excellent with FastAPI | Excellent with Django |
| Modern type hints | Traditional API |
| Flexible architecture | Opinionated framework |

______________________________________________________________________

## 20. SQLModel vs Raw SQL

Use SQLModel for:

- CRUD
- Relationships
- APIs
- Business logic

Use Raw SQL for:

- Very complex reporting
- Database-specific features
- Performance-critical queries after profiling

______________________________________________________________________

# Coding Questions

## 1

Create an Employee model.

______________________________________________________________________

## 2

Create Department and Employee relationships.

______________________________________________________________________

## 3

Implement a many-to-many relationship using a link model.

______________________________________________________________________

## 4

Insert multiple employees.

______________________________________________________________________

## 5

Retrieve employees earning more than ₹80,000.

______________________________________________________________________

## 6

Join Employee and Department.

______________________________________________________________________

## 7

Calculate average salary by department.

______________________________________________________________________

## 8

Rank employees by salary.

______________________________________________________________________

## 9

Implement pagination.

______________________________________________________________________

## 10

Implement a repository class.

______________________________________________________________________

## 11

Implement a service class.

______________________________________________________________________

## 12

Create a FastAPI endpoint using dependency injection.

______________________________________________________________________

# Production Scenarios

## Scenario 1

Your FastAPI endpoint performs 200 SQL queries.

How would you identify the N+1 problem?

How would you fix it?

______________________________________________________________________

## Scenario 2

A dashboard loads 1 million employees.

Would you:

- Load ORM objects?
- Stream results?
- Paginate?
- Select only required columns?

Explain your decision.

______________________________________________________________________

## Scenario 3

Your API returns ORM models directly.

What security or maintenance problems might this create?

______________________________________________________________________

## Scenario 4

A teammate wants to use one SQLModel Session for the entire application.

Explain why this is a bad idea.

______________________________________________________________________

## Scenario 5

A query is slow.

Would you:

- Optimize SQL?
- Add indexes?
- Profile ORM queries?
- Use raw SQL?

Explain the order in which you would investigate.

______________________________________________________________________

# Rapid Fire

1. SQLModel vs SQLAlchemy
1. SQLModel vs Pydantic
1. `Field()` vs `mapped_column()`
1. `exec()` vs `execute()`
1. `table=True` vs normal model
1. Repository vs Service
1. Relationship vs Foreign Key
1. `refresh()` vs `commit()`
1. Lazy vs Eager Loading
1. SQLModel vs Raw SQL
1. SQLModel vs Django ORM
1. `selectinload()` vs `joinedload()`
1. `Session` vs `Engine`
1. `create_all()` vs Alembic
1. CRUD vs Bulk Operations

______________________________________________________________________

# Common Mistakes

- Thinking SQLModel replaces SQLAlchemy.
- Ignoring generated SQL.
- Keeping Sessions alive too long.
- Returning database models directly in every API.
- Forgetting to use eager loading when appropriate.
- Using `create_all()` in production.
- Skipping database indexes because an ORM is used.

______________________________________________________________________

# Final Checklist

You should now be able to explain:

- SQLModel architecture
- SQLModel internals
- CRUD operations
- Relationships
- Link models
- Transactions
- Loading strategies
- Repository Pattern
- Service Layer
- Dependency Injection
- FastAPI integration
- Performance optimization
- SQLModel vs SQLAlchemy
- SQLModel vs Raw SQL
- Production best practices

______________________________________________________________________

# Summary

After completing this chapter, you should be comfortable building production-ready FastAPI applications using SQLModel,
understanding the SQLAlchemy features underneath, and discussing ORM design, performance, and architecture in technical
interviews.

______________________________________________________________________

# Course Completion

Congratulations! You have completed the SQL, SQLAlchemy, and SQLModel sections of the course.

At this point, you should be able to:

- Design normalized relational schemas.
- Write advanced SQL queries.
- Optimize SQL using indexes and execution plans.
- Translate SQL into SQLAlchemy.
- Build production-ready ORM models.
- Design scalable data access layers.
- Use SQLModel effectively with FastAPI.
- Confidently answer SQL, SQLAlchemy, and SQLModel interview questions.

The next natural step in a backend interview roadmap would be **Redis**, followed by **Docker**, **Kubernetes**,
**System Design**, or **Message Queues** depending on your overall learning plan.

## Next

[SQLAlchemy Session Management, Connection Pooling & Async - Part 1](23-sqlalchemy-session-management-async-part-1.md)
