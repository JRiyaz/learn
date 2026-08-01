# SQLModel Fundamentals

## Introduction

**SQLModel** is a modern ORM library created by the author of **FastAPI**, Sebastián Ramírez.

It combines the best features of:

- SQLAlchemy ORM
- Pydantic
- Python Type Hints

Instead of maintaining separate ORM models and API schemas, SQLModel allows you to use a single model for both database
operations and data validation in many applications.

This makes SQLModel an excellent choice for:

- FastAPI applications
- REST APIs
- CRUD applications
- Rapid backend development

______________________________________________________________________

# SQLAlchemy vs SQLModel

| SQLAlchemy | SQLModel |
| ------------------------------------- | ------------------------------ |
| Mature ORM | Built on top of SQLAlchemy |
| Separate Pydantic models | Integrated with Pydantic |
| More configuration | Less boilerplate |
| Greater flexibility | Easier to learn |
| Better for very complex ORM use cases | Excellent for FastAPI projects |

Interview Tip:

**SQLModel is not a replacement for SQLAlchemy.**

It is built **on top of SQLAlchemy** and internally uses SQLAlchemy's ORM.

______________________________________________________________________

# Installing SQLModel

```bash id="sm001"
pip install sqlmodel
```

For PostgreSQL

```bash id="sm002"
pip install psycopg
```

______________________________________________________________________

# Project Structure

```text id="sm003"
project/

│── database.py

│── models.py

│── crud.py

│── main.py
```

______________________________________________________________________

# Creating an Engine

```python id="sm004"
from sqlmodel import create_engine

engine = create_engine(
    "sqlite:///company.db"
)
```

PostgreSQL

```python id="sm005"
engine = create_engine(
    "postgresql+psycopg://user:password@localhost/company"
)
```

This is the same SQLAlchemy engine underneath.

______________________________________________________________________

# Creating a Model

```python id="sm006"
from sqlmodel import SQLModel
from sqlmodel import Field

class Employee(SQLModel, table=True):

    employee_id: int | None = Field(
        default=None,
        primary_key=True
    )

    name: str

    salary: float
```

______________________________________________________________________

# Equivalent SQL

```sql id="sm007"
CREATE TABLE employees (

employee_id INTEGER PRIMARY KEY,

name TEXT,

salary FLOAT

);
```

______________________________________________________________________

# SQLAlchemy Equivalent

```python id="sm008"
class Employee(Base):

    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str]

    salary: Mapped[float]
```

Notice how SQLModel removes much of the ORM boilerplate.

______________________________________________________________________

# table=True

```python id="sm009"
class Employee(
    SQLModel,
    table=True
):
```

This tells SQLModel to create a database table.

Without `table=True`, the class behaves as a Pydantic model and is not mapped to a database table.

______________________________________________________________________

# Field()

`Field()` is used to configure columns.

Example

```python id="sm010"
Field(
    primary_key=True
)
```

Equivalent SQLAlchemy

```python id="sm011"
mapped_column(
    primary_key=True
)
```

______________________________________________________________________

# Creating Tables

```python id="sm012"
SQLModel.metadata.create_all(
    engine
)
```

Equivalent SQL

```sql id="sm013"
CREATE TABLE ...
```

Like SQLAlchemy, this is suitable for development and prototypes.

Production applications should use Alembic migrations.

______________________________________________________________________

# Creating a Session

```python id="sm014"
from sqlmodel import Session

with Session(engine) as session:

    ...
```

Recommended approach.

______________________________________________________________________

# Insert Data

```python id="sm015"
employee = Employee(

    name="Alice",

    salary=75000

)

session.add(employee)

session.commit()

session.refresh(employee)
```

Why `refresh()`?

After committing, the database generates values such as the primary key.

`refresh()` loads those values back into the Python object.

______________________________________________________________________

# Equivalent SQL

```sql id="sm016"
INSERT INTO employees(

name,

salary

)

VALUES(

'Alice',

75000

);
```

______________________________________________________________________

# Insert Multiple Rows

```python id="sm017"
employees = [

    Employee(
        name="Alice",
        salary=70000
    ),

    Employee(
        name="Bob",
        salary=90000
    )

]

session.add_all(employees)

session.commit()
```

______________________________________________________________________

# Selecting Data

```python id="sm018"
from sqlmodel import select

statement = select(Employee)

employees = session.exec(
    statement
).all()
```

Unlike SQLAlchemy's `session.execute()` or `session.scalars()`, SQLModel provides the convenient `session.exec()`
method.

______________________________________________________________________

# Equivalent SQL

```sql id="sm019"
SELECT *
FROM employees;
```

______________________________________________________________________

# Query by Primary Key

```python id="sm020"
employee = session.get(
    Employee,
    1
)
```

Equivalent SQL

```sql id="sm021"
SELECT *
FROM employees
WHERE employee_id = 1;
```

______________________________________________________________________

# Filtering

```python id="sm022"
statement = (

    select(Employee)

    .where(
        Employee.salary > 80000
    )

)

employees = session.exec(
    statement
).all()
```

Equivalent SQL

```sql id="sm023"
SELECT *
FROM employees
WHERE salary > 80000;
```

______________________________________________________________________

# Multiple Filters

```python id="sm024"
statement = (

    select(Employee)

    .where(
        Employee.salary > 80000,
        Employee.name.startswith("A")
    )

)
```

Equivalent SQL

```sql id="sm025"
SELECT *
FROM employees
WHERE salary > 80000
AND name LIKE 'A%';
```

______________________________________________________________________

# Ordering

```python id="sm026"
statement = (

    select(Employee)

    .order_by(
        Employee.salary.desc()
    )

)
```

Equivalent SQL

```sql id="sm027"
SELECT *
FROM employees
ORDER BY salary DESC;
```

______________________________________________________________________

# Pagination

```python id="sm028"
statement = (

    select(Employee)

    .offset(20)

    .limit(10)

)
```

Equivalent SQL

```sql id="sm029"
SELECT *
FROM employees
LIMIT 10
OFFSET 20;
```

______________________________________________________________________

# Update Data

```python id="sm030"
employee = session.get(
    Employee,
    1
)

employee.salary = 90000

session.add(employee)

session.commit()

session.refresh(employee)
```

Equivalent SQL

```sql id="sm031"
UPDATE employees
SET salary = 90000
WHERE employee_id = 1;
```

______________________________________________________________________

# Delete Data

```python id="sm032"
employee = session.get(
    Employee,
    1
)

session.delete(employee)

session.commit()
```

Equivalent SQL

```sql id="sm033"
DELETE
FROM employees
WHERE employee_id = 1;
```

______________________________________________________________________

# Transactions

```python id="sm034"
from sqlmodel import Session

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

SQLModel relies on SQLAlchemy's transaction system.

______________________________________________________________________

# SQLModel with FastAPI

One of SQLModel's biggest advantages.

```python id="sm035"
@app.post("/employees")
def create_employee(
    employee: Employee,
    session: Session
):
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee
```

The same model is used for:

- Request validation
- Database mapping

For larger applications, it's still common to separate API models from database models to avoid exposing internal
fields.

______________________________________________________________________

# Common Mistakes

### Forgetting refresh()

Primary keys generated by the database won't automatically appear in the object until refreshed (or reloaded).

______________________________________________________________________

### Using create_all() in Production

Use Alembic.

______________________________________________________________________

### Keeping Sessions Open

Use

```python
with Session(engine)
```

______________________________________________________________________

### Assuming SQLModel Replaces SQLAlchemy

SQLModel depends on SQLAlchemy.

Learning SQLAlchemy first is a major advantage.

______________________________________________________________________

# Best Practices

- Use Python type hints.
- Keep sessions short.
- Use `session.exec()` for queries.
- Refresh objects after inserts when generated values are needed.
- Use Alembic for migrations.
- Understand the SQL generated by SQLModel.

______________________________________________________________________

# Interview Deep Dive

## Answer

**Question:** What are the advantages of SQLModel over SQLAlchemy?

SQLModel reduces boilerplate by combining SQLAlchemy ORM with Pydantic models and Python type hints. This allows
developers to define database models and validation models in a consistent way, making it especially convenient for
FastAPI applications. However, SQLModel still uses SQLAlchemy internally, so understanding SQLAlchemy remains important
for advanced ORM features and performance tuning.

______________________________________________________________________

# Practice Questions

## Conceptual

1. What is SQLModel?
1. Who created SQLModel?
1. How is SQLModel related to SQLAlchemy?
1. Why is SQLModel popular with FastAPI?
1. What does `table=True` do?
1. What is `Field()`?
1. Why use `session.refresh()`?
1. What is `session.exec()`?
1. Should SQLModel replace SQLAlchemy in every project?
1. Why should Alembic still be used?

## Coding

1. Create an Employee model.
1. Insert three employees.
1. Retrieve all employees.
1. Filter employees by salary.
1. Update an employee.
1. Delete an employee.
1. Order employees by salary.
1. Paginate results.

______________________________________________________________________

# Hands-on Exercise

Build an Employee Management API.

Requirements:

1. Create SQLModel models.
1. Create database tables.
1. Insert sample data.
1. Retrieve employees.
1. Filter employees.
1. Update salaries.
1. Delete employees.
1. Compare the generated SQL with equivalent handwritten SQL.
1. Integrate the models with a simple FastAPI endpoint.

______________________________________________________________________

# Cheat Sheet

```text id="sm036"
SQLModel

↓

SQLModel(table=True)

↓

Field()

↓

create_engine()

↓

Session()

↓

add()

↓

commit()

↓

refresh()

↓

select()

↓

exec()

↓

update

↓

delete
```

______________________________________________________________________

# Summary

In this lecture, you learned:

- SQLModel architecture
- SQLModel vs SQLAlchemy
- Creating models
- `Field()`
- `table=True`
- Engine
- Session
- CRUD operations
- Filtering
- Ordering
- Pagination
- Transactions
- FastAPI integration
- Best practices
- Interview patterns

You now have a solid understanding of SQLModel fundamentals and how it simplifies SQLAlchemy for modern Python backend
development.

______________________________________________________________________

## Next File

[SQLModel Advanced & Production Patterns](21-sqlmodel-advanced.md)
