# SQLAlchemy Fundamentals

## Introduction

SQLAlchemy is the most widely used ORM (Object Relational Mapper) in the Python ecosystem.

It allows Python applications to communicate with relational databases using Python objects instead of writing raw SQL
for every operation.

However, **SQLAlchemy is not just an ORM**.

It consists of two major layers:

- **SQLAlchemy Core** — SQL Expression Language
- **SQLAlchemy ORM** — Object Relational Mapper

As a backend engineer, you should understand both.

One of the biggest mistakes beginners make is learning SQLAlchemy without understanding the SQL generated behind the
scenes.

Throughout this course, every important SQLAlchemy example will include:

- Equivalent SQL
- Performance considerations
- Interview discussion

______________________________________________________________________

# Why Use an ORM?

Without an ORM:

```python
cursor.execute(
    """
    SELECT *
    FROM employees
    WHERE employee_id = 1
    """
)
```

With SQLAlchemy:

```python
employee = session.get(Employee, 1)
```

Advantages:

- Less boilerplate
- Database portability
- Safer parameter handling
- Easier maintenance
- Relationship management
- Better integration with Python

______________________________________________________________________

# ORM vs Raw SQL

| ORM | Raw SQL |
| ------------------ | ----------------------------------- |
| Easier to maintain | Full control |
| Object-oriented | SQL-oriented |
| Faster development | Better for highly optimized queries |
| Automatic mapping | Manual mapping |

Interview Tip:

**Good backend engineers know both ORM and SQL.**

______________________________________________________________________

# Installing SQLAlchemy

```bash
pip install sqlalchemy
```

Latest SQLAlchemy (2.x) uses the new **2.0 style API**, which we'll use throughout this course.

______________________________________________________________________

# Project Structure

```text
project/

│── database.py

│── models.py

│── crud.py

│── main.py
```

______________________________________________________________________

# Creating an Engine

The Engine is the entry point to the database.

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://user:password@localhost/company"
)
```

SQLite example

```python
engine = create_engine(
    "sqlite:///company.db"
)
```

______________________________________________________________________

# What is an Engine?

The Engine manages:

- Database connections
- Connection pooling
- SQL execution
- Transactions
- Dialect selection

Think of it as the communication layer between Python and the database.

______________________________________________________________________

# Database URL

General format

```text
dialect+driver://username:password@host:port/database
```

Examples

PostgreSQL

```text
postgresql+psycopg://user:password@localhost/company
```

SQLite

```text
sqlite:///company.db
```

MySQL

```text
mysql+pymysql://user:password@localhost/company
```

______________________________________________________________________

# Declarative Base

Every ORM model inherits from a Declarative Base.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

All models will inherit from `Base`.

______________________________________________________________________

# Creating Models

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Employee(Base):

    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    salary: Mapped[float]
```

______________________________________________________________________

# Equivalent SQL

```sql
CREATE TABLE employees (

    employee_id INTEGER PRIMARY KEY,

    name VARCHAR(100),

    salary FLOAT
);
```

______________________________________________________________________

# What is **tablename**?

```python
__tablename__ = "employees"
```

Specifies the database table name.

Without it, SQLAlchemy cannot map the model.

______________________________________________________________________

# mapped_column()

Represents a database column.

Example

```python
salary: Mapped[float] = mapped_column()
```

Equivalent SQL

```sql
salary FLOAT
```

______________________________________________________________________

# Mapped[]

`Mapped[]` is SQLAlchemy 2.x's typing system.

Example

```python
name: Mapped[str]
```

Benefits

- Better IDE support
- Static type checking
- Cleaner model definitions

______________________________________________________________________

# Creating Tables

```python
Base.metadata.create_all(engine)
```

Equivalent SQL

```sql
CREATE TABLE ...
```

Important:

`create_all()` creates only missing tables.

It is **not** a migration system.

We'll use **Alembic** for schema migrations later.

______________________________________________________________________

# Session

A Session represents a conversation with the database.

```python
from sqlalchemy.orm import Session

session = Session(engine)
```

Think of it as a workspace.

______________________________________________________________________

# Session Responsibilities

A Session manages:

- Queries
- Inserts
- Updates
- Deletes
- Transactions
- Identity map
- Unit of work

______________________________________________________________________

# Adding Data

```python
employee = Employee(

    name="Alice",

    salary=70000
)

session.add(employee)

session.commit()
```

Equivalent SQL

```sql
INSERT INTO employees(

name,

salary

)

VALUES(

'Alice',

70000

);
```

______________________________________________________________________

# Adding Multiple Rows

```python
employees = [

    Employee(name="Alice", salary=70000),

    Employee(name="Bob", salary=90000),

    Employee(name="Charlie", salary=85000)

]

session.add_all(employees)

session.commit()
```

______________________________________________________________________

# Querying Data

Retrieve all employees.

```python
from sqlalchemy import select

stmt = select(Employee)

employees = session.scalars(stmt).all()
```

Equivalent SQL

```sql
SELECT *
FROM employees;
```

______________________________________________________________________

# Query by Primary Key

```python
employee = session.get(
    Employee,
    1
)
```

Equivalent SQL

```sql
SELECT *
FROM employees
WHERE employee_id = 1;
```

`session.get()` is optimized for primary-key lookups.

______________________________________________________________________

# Filtering

```python
stmt = (

    select(Employee)

    .where(Employee.salary > 80000)

)
```

Equivalent SQL

```sql
SELECT *
FROM employees
WHERE salary > 80000;
```

______________________________________________________________________

# Multiple Filters

```python
stmt = (

    select(Employee)

    .where(
        Employee.salary > 80000,
        Employee.name.like("A%")
    )

)
```

Equivalent SQL

```sql
SELECT *
FROM employees
WHERE salary > 80000
AND name LIKE 'A%';
```

______________________________________________________________________

# Ordering

```python
stmt = (

    select(Employee)

    .order_by(Employee.salary.desc())

)
```

Equivalent SQL

```sql
SELECT *
FROM employees
ORDER BY salary DESC;
```

______________________________________________________________________

# Limiting Rows

```python
stmt = (

    select(Employee)

    .limit(10)

)
```

Equivalent SQL

```sql
SELECT *
FROM employees
LIMIT 10;
```

______________________________________________________________________

# Updating Data

```python
employee = session.get(Employee, 1)

employee.salary = 90000

session.commit()
```

Equivalent SQL

```sql
UPDATE employees
SET salary = 90000
WHERE employee_id = 1;
```

______________________________________________________________________

# Deleting Data

```python
employee = session.get(Employee, 1)

session.delete(employee)

session.commit()
```

Equivalent SQL

```sql
DELETE
FROM employees
WHERE employee_id = 1;
```

______________________________________________________________________

# Rolling Back

```python
try:

    session.commit()

except:

    session.rollback()

    raise
```

Always roll back failed transactions.

______________________________________________________________________

# Closing the Session

```python
session.close()
```

Better

```python
from sqlalchemy.orm import Session

with Session(engine) as session:

    ...
```

The context manager closes the session automatically.

______________________________________________________________________

# Common Mistakes

### Forgetting commit()

Changes remain uncommitted.

______________________________________________________________________

### Forgetting rollback()

Always roll back after failed commits.

______________________________________________________________________

### Using One Session Forever

Sessions should be short-lived.

______________________________________________________________________

### Confusing Engine and Session

- Engine manages connections.
- Session manages ORM operations and transactions.

______________________________________________________________________

### Using create_all() in Production

Use **Alembic** for schema migrations.

______________________________________________________________________

# Best Practices

- Use SQLAlchemy 2.x style.
- Keep sessions short.
- Use context managers.
- Prefer `session.get()` for primary keys.
- Use `select()` instead of the legacy `session.query()`.
- Commit only when necessary.
- Roll back on exceptions.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What is the difference between an Engine and a Session?

The **Engine** is the application's interface to the database. It manages database connections, connection pooling, SQL
execution, and database dialects. The **Session** is an ORM construct that manages object state, transactions, and
communication with the Engine. In practice, the Engine is typically created once for the application, while Sessions are
created per request or per unit of work and should be short-lived.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is SQLAlchemy?
1. Difference between SQLAlchemy Core and ORM.
1. What is an Engine?
1. What is a Session?
1. Why use `Mapped[]`?
1. What does `mapped_column()` do?
1. What is `Base.metadata.create_all()`?
1. Why is `session.get()` faster for primary-key lookups?
1. Why should sessions be short-lived?
1. Why shouldn't `create_all()` be used for production migrations?

## Coding

1. Create an Employee model.
1. Insert three employees.
1. Retrieve all employees.
1. Retrieve an employee by primary key.
1. Update an employee's salary.
1. Delete an employee.
1. Filter employees by salary.
1. Order employees by salary.
1. Limit results to five rows.
1. Handle commit failures using rollback.

______________________________________________________________________

# Hands-on Exercise

Build a small Employee Management application.

Requirements:

1. Create an Engine.
1. Create a Declarative Base.
1. Define Employee and Department models.
1. Create tables.
1. Insert sample data.
1. Retrieve all employees.
1. Filter employees earning more than ₹80,000.
1. Update one employee.
1. Delete one employee.
1. Use context-managed sessions throughout.

______________________________________________________________________

# Cheat Sheet

```text
Engine
↓

Session
↓

Model

↓

add()

↓

commit()

↓

select()

↓

where()

↓

order_by()

↓

limit()

↓

update

↓

delete

↓

rollback()
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- SQLAlchemy architecture
- ORM vs Raw SQL
- Engine
- Database URLs
- Declarative Base
- Models
- `Mapped[]`
- `mapped_column()`
- `create_all()`
- Session
- CRUD operations
- Filtering
- Ordering
- Limiting
- Transactions
- Rollback
- Session lifecycle
- Best practices
- Interview patterns

You now have a solid foundation for SQLAlchemy. In the next lecture, we'll build relationships between models and learn
how SQLAlchemy manages object graphs efficiently.

______________________________________________________________________

## Next File

[SQLAlchemy Relationships](16-sqlalchemy-relationships.md)
