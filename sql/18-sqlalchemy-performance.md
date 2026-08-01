# SQLAlchemy Performance & Production Patterns

## Introduction

Writing correct SQLAlchemy code is only the first step.

The real challenge begins when your application handles:

- Millions of rows
- Thousands of requests per second
- Hundreds of concurrent users
- Long-running background jobs
- Distributed services

At this stage, performance becomes more important than syntax.

Many developers blame SQLAlchemy for slow applications when the real problems are:

- Poor query design
- N+1 queries
- Long-lived sessions
- Fetching unnecessary data
- Missing indexes
- Improper transaction handling

In this chapter, you'll learn how SQLAlchemy behaves in production and how experienced backend engineers write scalable
ORM code.

______________________________________________________________________

# The ORM Lifecycle

A typical SQLAlchemy request looks like this:

```text id="sap001"
HTTP Request

↓

Session Created

↓

Execute Queries

↓

Commit / Rollback

↓

Session Closed

↓

HTTP Response
```

A session should normally live for **one request**.

______________________________________________________________________

# Identity Map

One of SQLAlchemy's most important concepts.

Within a Session, SQLAlchemy keeps **one Python object per database row**.

Example

```python id="sap002"
employee1 = session.get(Employee, 1)

employee2 = session.get(Employee, 1)
```

```python id="sap003"
print(employee1 is employee2)
```

Output

```text id="sap004"
True
```

No second SQL query is executed if the object is already present in the Session.

______________________________________________________________________

# Unit of Work

SQLAlchemy tracks object changes automatically.

Example

```python id="sap005"
employee = session.get(Employee, 1)

employee.salary = 95000
```

No SQL is executed yet.

Only during

```python id="sap006"
session.commit()
```

does SQLAlchemy determine what changed and generate the appropriate SQL.

Equivalent SQL

```sql id="sap007"
UPDATE employees
SET salary = 95000
WHERE employee_id = 1;
```

______________________________________________________________________

# Autoflush

Before executing many queries, SQLAlchemy automatically flushes pending changes.

Example

```python id="sap008"
employee.salary = 90000

employees = session.scalars(
    select(Employee)
).all()
```

SQLAlchemy flushes the pending update before running the SELECT.

Flush writes SQL to the database transaction.

Commit permanently saves it.

______________________________________________________________________

# Flush vs Commit

Interview favorite.

| Flush | Commit |
| ---------------------- | ---------------------------------- |
| Sends SQL | Makes transaction permanent |
| Transaction still open | Transaction completed |
| Can be rolled back | Cannot be rolled back after commit |

______________________________________________________________________

# expire_on_commit

By default,

```python id="sap009"
Session(engine)
```

expires ORM objects after commit.

The next attribute access reloads the object from the database if needed.

Many web applications configure

```python id="sap010"
expire_on_commit=False
```

to avoid unnecessary reloads after a successful commit.

______________________________________________________________________

# N+1 Query Problem

Bad

```python id="sap011"
employees = session.scalars(
    select(Employee)
).all()

for employee in employees:
    print(employee.department.name)
```

Queries

```text id="sap012"
1

+

N
```

______________________________________________________________________

# Solution

```python id="sap013"
stmt = (
    select(Employee)
    .options(
        selectinload(Employee.department)
    )
)
```

Usually

```text id="sap014"
2 Queries
```

instead of

```text id="sap015"
101 Queries
```

______________________________________________________________________

# Loading Only Required Columns

Bad

```python id="sap016"
select(Employee)
```

Good

```python id="sap017"
select(
    Employee.employee_id,
    Employee.name
)
```

Never retrieve columns you don't need.

______________________________________________________________________

# yield_per()

Large result sets can consume significant memory.

Example

```python id="sap018"
stmt = (
    select(Employee)
    .execution_options(
        yield_per=1000
    )
)
```

Rows are processed in batches instead of loading everything into memory at once.

Useful for exports and batch processing.

______________________________________________________________________

# Bulk Inserts

Slow

```python id="sap019"
for employee in employees:

    session.add(employee)
```

Better

```python id="sap020"
session.add_all(employees)
```

For very large datasets, SQLAlchemy also provides bulk operations such as `bulk_insert_mappings()`, though they bypass
some ORM features.

______________________________________________________________________

# Bulk Updates

Instead of updating rows individually:

```python id="sap021"
for employee in employees:
    employee.salary += 5000
```

Use a single SQL statement when appropriate.

```python id="sap022"
from sqlalchemy import update

stmt = (
    update(Employee)
    .values(
        salary=Employee.salary + 5000
    )
)

session.execute(stmt)
session.commit()
```

Equivalent SQL

```sql id="sap023"
UPDATE employees
SET salary = salary + 5000;
```

______________________________________________________________________

# Bulk Deletes

```python id="sap024"
from sqlalchemy import delete

stmt = (
    delete(Employee)
    .where(Employee.salary < 30000)
)

session.execute(stmt)
session.commit()
```

Equivalent SQL

```sql id="sap025"
DELETE
FROM employees
WHERE salary < 30000;
```

______________________________________________________________________

# Connection Pooling

Creating a new database connection for every query is expensive.

The Engine maintains a pool of reusable connections.

```python id="sap026"
engine = create_engine(

    DATABASE_URL,

    pool_size=10,

    max_overflow=20

)
```

Conceptually

```text id="sap027"
Application

↓

Connection Pool

↓

Database
```

______________________________________________________________________

# Session Per Request

Recommended architecture

```text id="sap028"
HTTP Request

↓

Create Session

↓

Business Logic

↓

Commit

↓

Close Session
```

Avoid global Sessions shared across requests.

______________________________________________________________________

# Repository Pattern

Many production applications isolate database access inside repositories.

Example

```python id="sap029"
class EmployeeRepository:

    def get_by_id(
        self,
        session,
        employee_id
    ):
        return session.get(
            Employee,
            employee_id
        )
```

Benefits:

- Easier testing
- Separation of concerns
- Reusable data access

______________________________________________________________________

# Unit of Work Pattern

The Unit of Work coordinates multiple repositories within a single transaction.

Conceptually

```text id="sap030"
Repositories

↓

Unit of Work

↓

Session

↓

Database
```

Useful for complex business operations involving multiple tables.

______________________________________________________________________

# Alembic

`create_all()` is suitable for learning and simple prototypes.

Production systems use migrations.

SQLAlchemy's official migration tool is **Alembic**.

Example workflow

```bash id="sap031"
alembic revision --autogenerate

alembic upgrade head
```

Alembic tracks schema changes over time and allows safe upgrades and rollbacks.

______________________________________________________________________

# Async SQLAlchemy

Modern web frameworks often use asynchronous database access.

Example

```python id="sap032"
from sqlalchemy.ext.asyncio import AsyncSession
```

Typical usage

```python id="sap033"
async with AsyncSession(engine) as session:

    result = await session.execute(
        select(Employee)
    )
```

Use async only when the rest of the application architecture benefits from it.

______________________________________________________________________

# Testing

A common testing pattern:

```text id="sap034"
Start Transaction

↓

Run Test

↓

Rollback

↓

Database Restored
```

This keeps tests isolated and repeatable.

______________________________________________________________________

# Logging SQL

To inspect generated SQL

```python id="sap035"
engine = create_engine(

    DATABASE_URL,

    echo=True

)
```

Useful for debugging and learning.

Avoid enabling verbose SQL logging in production unless troubleshooting.

______________________________________________________________________

# Profiling Queries

When investigating slow queries:

1. Enable SQL logging.
1. Inspect generated SQL.
1. Run `EXPLAIN ANALYZE`.
1. Check indexes.
1. Measure before and after changes.

Never optimize based on assumptions.

______________________________________________________________________

# Common Mistakes

### Long-Lived Sessions

Sessions should usually be scoped to a request or unit of work.

______________________________________________________________________

### Returning ORM Objects Everywhere

Large object graphs can consume unnecessary memory.

Sometimes selecting only required columns is more efficient.

______________________________________________________________________

### Committing Too Frequently

Each commit has overhead.

Group related changes into a single transaction when appropriate.

______________________________________________________________________

### Ignoring Lazy Loading

Unexpected lazy loads often become performance bottlenecks.

______________________________________________________________________

### Not Measuring

Always profile before optimizing.

______________________________________________________________________

# Best Practices

- Use one Session per request.
- Keep transactions short.
- Avoid N+1 queries.
- Load only required columns.
- Use eager loading deliberately.
- Batch inserts and updates.
- Use Alembic for schema changes.
- Profile generated SQL.
- Understand the SQL your ORM produces.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** Why can SQLAlchemy applications become slow, and how would you improve performance?

Most performance problems are caused by inefficient query patterns rather than the ORM itself. Common issues include N+1
queries, loading unnecessary columns, long-lived sessions, missing indexes, and issuing many small queries instead of
fewer efficient ones. I would inspect the generated SQL, analyze execution plans, use eager loading where appropriate,
select only the required columns, batch database operations, and verify improvements with profiling before making
further changes.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is the Identity Map?
1. What is the Unit of Work pattern?
1. Difference between `flush()` and `commit()`.
1. What is `expire_on_commit`?
1. Why is one Session per request recommended?
1. What is connection pooling?
1. Why use Alembic?
1. When should async SQLAlchemy be used?
1. What is the Repository Pattern?
1. How do you profile SQLAlchemy queries?

## Coding

1. Batch insert 1,000 employees.
1. Perform a bulk salary update.
1. Delete employees below a salary threshold using a bulk statement.
1. Configure connection pooling.
1. Log generated SQL.
1. Build a repository class.
1. Rewrite a query suffering from the N+1 problem.

______________________________________________________________________

# Hands-on Exercise

Extend the Employee Management application.

Requirements:

1. Implement one Session per request.
1. Build a repository layer.
1. Batch insert employee records.
1. Perform a bulk update.
1. Eliminate N+1 queries.
1. Enable SQL logging.
1. Compare generated SQL with handwritten SQL.
1. Prepare an Alembic migration for a schema change.

______________________________________________________________________

# Cheat Sheet

```text id="sap036"
Session

↓

Identity Map

↓

Unit of Work

↓

flush()

↓

commit()

↓

Connection Pool

↓

Repository

↓

Alembic

↓

AsyncSession

↓

Profile SQL
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- ORM lifecycle
- Identity Map
- Unit of Work
- `flush()` vs `commit()`
- `expire_on_commit`
- N+1 query optimization
- Efficient column selection
- Streaming large result sets
- Bulk inserts
- Bulk updates
- Bulk deletes
- Connection pooling
- Session-per-request pattern
- Repository Pattern
- Unit of Work Pattern
- Alembic migrations
- Async SQLAlchemy
- SQL logging
- Performance profiling
- Production best practices
- Interview patterns

You now understand how SQLAlchemy is used in production systems, how to identify common performance issues, and how to
build scalable ORM-based applications.

______________________________________________________________________

## Next File

[SQLAlchemy Interview Masterclass](19-sqlalchemy-interview-masterclass.md)
