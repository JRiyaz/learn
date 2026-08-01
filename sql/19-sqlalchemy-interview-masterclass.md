# SQLAlchemy Interview Masterclass

## Introduction

This chapter is a comprehensive revision of SQLAlchemy from an interview perspective.

Unlike previous chapters, this file focuses on:

- Frequently asked interview questions
- Production scenarios
- Common mistakes
- Coding questions
- Best practices
- Decision-making discussions

If you can confidently answer the questions in this chapter, you'll be well prepared for most SQLAlchemy interviews.

______________________________________________________________________

# Beginner Interview Questions

## 1. What is SQLAlchemy?

**Answer**

SQLAlchemy is a Python SQL toolkit and ORM that provides two major components:

- SQLAlchemy Core (SQL Expression Language)
- SQLAlchemy ORM (Object Relational Mapper)

It allows developers to work with relational databases using Python objects while still providing access to raw SQL when
needed.

______________________________________________________________________

## 2. What is an ORM?

**Answer**

An ORM maps database tables to Python classes and database rows to Python objects.

Instead of writing:

```sql id="orm001"
SELECT *
FROM employees;
```

you can write:

```python id="orm002"
session.scalars(
    select(Employee)
)
```

The ORM generates SQL automatically.

______________________________________________________________________

## 3. Difference Between SQLAlchemy Core and ORM

| Core | ORM |
| ------------------------- | ------------------ |
| SQL Expression Language | Python Objects |
| Lower-level | Higher-level |
| More SQL-like | More Pythonic |
| Excellent for complex SQL | Excellent for CRUD |

Interview Tip:

Many large applications use **both**.

______________________________________________________________________

## 4. What is an Engine?

**Answer**

The Engine manages:

- Connections
- Connection Pool
- SQL Execution
- Database Dialect

Normally, only one Engine exists per application.

______________________________________________________________________

## 5. What is a Session?

**Answer**

A Session is a unit of work.

It manages:

- ORM objects
- Transactions
- Identity Map
- Flush
- Commit
- Rollback

Sessions should generally be short-lived.

______________________________________________________________________

# Intermediate Interview Questions

## 6. Engine vs Session

| Engine | Session |
| --------------------- | ------------------- |
| Connection Management | ORM Management |
| Usually Singleton | Usually Per Request |
| Talks to Database | Talks to Engine |

______________________________________________________________________

## 7. Flush vs Commit

| Flush | Commit |
| ---------------- | ---------------------------- |
| Sends SQL | Makes Permanent |
| Transaction Open | Transaction Ends |
| Can Rollback | Cannot Rollback After Commit |

______________________________________________________________________

## 8. What is the Identity Map?

The Session keeps one Python object for each database row.

```python id="orm003"
a = session.get(Employee, 1)

b = session.get(Employee, 1)
```

```python id="orm004"
a is b
```

returns

```text id="orm005"
True
```

This avoids duplicate objects and unnecessary database queries.

______________________________________________________________________

## 9. What is Unit of Work?

SQLAlchemy tracks changes automatically.

```python id="orm006"
employee.salary = 95000
```

No SQL executes immediately.

SQL is generated during flush/commit.

______________________________________________________________________

## 10. Why Should Sessions Be Short?

Reasons:

- Avoid stale objects.
- Reduce memory usage.
- Release database connections promptly.
- Improve concurrency.
- Prevent long-running transactions.

______________________________________________________________________

# Relationships

## 11. Difference Between One-to-Many and Many-to-Many

One Department

↓

Many Employees

versus

Many Employees

↓

Many Projects

which requires an association table.

______________________________________________________________________

## 12. What Does relationship() Do?

It creates an ORM relationship between models.

It **does not** create a database foreign key.

______________________________________________________________________

## 13. Difference Between ForeignKey and relationship()

| ForeignKey | relationship |
| ------------------- | -------------- |
| Database Constraint | ORM Navigation |
| SQL Feature | Python Feature |

Both are usually used together.

______________________________________________________________________

## 14. What Does back_populates Do?

Creates a bidirectional relationship.

```python id="orm007"
employee.department
```

and

```python id="orm008"
department.employees
```

remain synchronized within the ORM.

______________________________________________________________________

# Loading Strategies

## 15. Lazy Loading

Loads related data only when accessed.

Pros

- Small initial query.

Cons

- Can create N+1 problems.

______________________________________________________________________

## 16. joinedload()

Uses JOIN.

One SQL query.

Good for:

- Many-to-One
- One-to-One

______________________________________________________________________

## 17. selectinload()

Uses two queries.

Typically preferred for One-to-Many collections.

Avoids row duplication.

______________________________________________________________________

## 18. subqueryload()

Uses a subquery.

Less common today than `selectinload()`, but useful in some scenarios.

______________________________________________________________________

## 19. Explain the N+1 Problem

Example

100 employees

↓

100 department lookups

↓

101 SQL queries

Solution

Use eager loading.

______________________________________________________________________

# Performance

## 20. Why is SQLAlchemy Slow?

Usually it isn't.

Common causes:

- N+1 queries.
- Missing indexes.
- Selecting unnecessary columns.
- Long-lived sessions.
- Too many round trips.
- Poor SQL.

______________________________________________________________________

## 21. How Do You Optimize SQLAlchemy?

- Inspect generated SQL.
- Use EXPLAIN.
- Add indexes.
- Use eager loading.
- Select required columns only.
- Batch operations.
- Measure before optimizing.

______________________________________________________________________

## 22. Why Use select() Instead of query()?

`query()` is part of SQLAlchemy's legacy API.

SQLAlchemy 2.x recommends `select()`.

______________________________________________________________________

## 23. When Should Raw SQL Be Used?

Examples:

- Vendor-specific SQL.
- Complex reporting.
- Recursive queries.
- Performance-critical operations after profiling.
- Features not directly exposed by the ORM.

______________________________________________________________________

## 24. How Do You View Generated SQL?

Enable SQL logging.

```python id="orm009"
engine = create_engine(

    DATABASE_URL,

    echo=True

)
```

______________________________________________________________________

## 25. What is Connection Pooling?

Instead of opening a new database connection every time:

```text id="orm010"
Application

↓

Connection Pool

↓

Database
```

Connections are reused.

______________________________________________________________________

# Transactions

## 26. How Are Transactions Managed?

```python id="orm011"
with Session(engine) as session:
    with session.begin():

        ...
```

Automatic

- Commit
- Rollback

______________________________________________________________________

## 27. How Do You Lock Rows?

```python id="orm012"
.with_for_update()
```

Equivalent SQL

```sql id="orm013"
FOR UPDATE
```

______________________________________________________________________

## 28. Explain Optimistic Locking

Use a version column.

If another transaction changes the row first, the update fails and can be retried.

______________________________________________________________________

## 29. Explain Pessimistic Locking

Lock rows before updating them.

Useful in:

- Banking
- Inventory
- Financial systems

______________________________________________________________________

# Production Questions

## 30. Why Not Use create_all()?

Because production applications use migrations.

Use

```text id="orm014"
Alembic
```

______________________________________________________________________

## 31. Why Repository Pattern?

Separates:

Business Logic

↓

Database Access

Benefits:

- Testability
- Maintainability
- Cleaner architecture

______________________________________________________________________

## 32. Session Per Request

Recommended architecture.

```text id="orm015"
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

______________________________________________________________________

## 33. Why Avoid Global Sessions?

Global sessions can:

- Leak memory.
- Hold stale objects.
- Cause concurrency issues.
- Keep transactions open unintentionally.

______________________________________________________________________

## 34. What is expire_on_commit?

After commit, ORM objects are expired by default.

The next attribute access reloads values from the database if necessary.

______________________________________________________________________

## 35. What is Autoflush?

Pending changes are automatically flushed before many queries to keep query results consistent with in-memory changes.

______________________________________________________________________

# Coding Questions

## 1

Create an Employee model.

______________________________________________________________________

## 2

Create a Department model.

______________________________________________________________________

## 3

Implement a One-to-Many relationship.

______________________________________________________________________

## 4

Implement a Many-to-Many relationship.

______________________________________________________________________

## 5

Retrieve employees earning above ₹80,000.

______________________________________________________________________

## 6

Retrieve employees and departments using `joinedload()`.

______________________________________________________________________

## 7

Retrieve departments with employees using `selectinload()`.

______________________________________________________________________

## 8

Find employees above average salary.

______________________________________________________________________

## 9

Create a CTE.

______________________________________________________________________

## 10

Write a window function.

______________________________________________________________________

## 11

Execute raw SQL safely using parameters.

______________________________________________________________________

## 12

Implement row locking using `with_for_update()`.

______________________________________________________________________

## 13

Batch insert 10,000 employees.

______________________________________________________________________

## 14

Perform a bulk update.

______________________________________________________________________

## 15

Build a Repository class.

______________________________________________________________________

## 16

Create an Alembic migration.

______________________________________________________________________

## Production Scenarios

### Scenario 1

Your API performs **500 SQL queries** for one request.

How would you investigate and fix it?

______________________________________________________________________

### Scenario 2

An endpoint takes **15 seconds** to return.

How would you identify whether the bottleneck is:

- SQL
- ORM
- Network
- Missing index

______________________________________________________________________

### Scenario 3

A dashboard loads 100,000 employees.

Would you:

- Load ORM objects?
- Stream results?
- Paginate?
- Return only selected columns?

Explain your choice.

______________________________________________________________________

### Scenario 4

Two users update the same employee simultaneously.

How would you prevent lost updates?

______________________________________________________________________

### Scenario 5

An interviewer asks:

> "Why shouldn't every query use joinedload()?"

Explain the advantages and disadvantages.

______________________________________________________________________

# Rapid Fire

1. Engine vs Session
1. Flush vs Commit
1. Core vs ORM
1. ForeignKey vs relationship()
1. joinedload vs selectinload
1. Lazy vs Eager Loading
1. Repository vs Service Layer
1. create_all vs Alembic
1. Bulk Update vs ORM Loop
1. Session Per Request vs Global Session
1. Identity Map vs Database Cache
1. Raw SQL vs ORM
1. delete-orphan vs ON DELETE CASCADE
1. `session.get()` vs `select()`
1. `scalar()` vs `scalars()`
1. `execute()` vs `scalars()`
1. `mapped_column()` vs `Column()` (2.x style vs classic style)
1. `Session.begin()` vs manual commit
1. `select()` vs legacy `query()`
1. `joinedload()` vs explicit `JOIN`

______________________________________________________________________

# Common Interview Mistakes

- Saying SQLAlchemy replaces SQL.
- Confusing Engine and Session.
- Using `relationship()` without a `ForeignKey`.
- Not understanding the SQL generated by ORM queries.
- Using lazy loading everywhere.
- Keeping Sessions alive too long.
- Believing ORM is always slower than raw SQL.
- Using `create_all()` for production schema changes.
- Ignoring execution plans.
- Optimizing without measuring.

______________________________________________________________________

# Final Checklist

You should now be able to explain:

- SQLAlchemy architecture
- Engine
- Session
- ORM lifecycle
- CRUD
- Relationships
- Loading strategies
- Query building
- Aggregations
- Window functions
- CTEs
- Raw SQL
- Transactions
- Locking
- Bulk operations
- Repository Pattern
- Unit of Work
- Alembic
- Async basics
- Performance optimization
- Production best practices

______________________________________________________________________

# Summary

After completing the SQL and SQLAlchemy sections, you should be comfortable:

- Writing efficient SQL.
- Translating SQL into SQLAlchemy.
- Understanding the SQL generated by the ORM.
- Optimizing database access.
- Designing production-ready data access layers.
- Answering beginner through senior-level SQLAlchemy interview questions.

______________________________________________________________________

## Next File

[SQLModel Fundamentals](20-sqlmodel-fundamentals.md)
