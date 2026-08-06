# Database Integration with SQLAlchemy

> **Course:** Flask for Backend Engineers
>
> **Module:** 4
>
> **File:** `10_database_sqlalchemy.md`

______________________________________________________________________

# What You Will Learn

By the end of this chapter, you will understand:

- Why ORMs exist
- What SQLAlchemy is
- SQLAlchemy Architecture
- Flask-SQLAlchemy
- Models
- Columns
- Data Types
- Primary Keys
- Constraints
- CRUD Operations
- Sessions
- Transactions
- Relationships
- Querying
- Best Practices

______________________________________________________________________

# Why Do We Need an ORM?

Imagine writing raw SQL everywhere.

```python
cursor.execute(
    """
    SELECT * FROM users
    WHERE id = %s
    """,
    (user_id,)
)
```

As applications grow,

hundreds of SQL queries become difficult to maintain.

Instead

```
Python Object

↓

ORM

↓

SQL

↓

Database
```

______________________________________________________________________

# What is an ORM?

ORM

\=

**Object Relational Mapper**

It maps

```
Python Class

↓

Database Table
```

and

```
Python Object

↓

Database Row
```

______________________________________________________________________

# What is SQLAlchemy?

**SQLAlchemy** is the most popular ORM for Python.

It provides:

- ORM
- SQL Expression Language
- Connection Pooling
- Transactions
- Database Abstraction

Flask commonly uses **Flask-SQLAlchemy**, which integrates SQLAlchemy with Flask.

______________________________________________________________________

# Why Use SQLAlchemy?

Benefits

- Less repetitive SQL
- Database portability
- Object-oriented programming
- Relationship management
- Transactions
- Better maintainability

SQL can still be written directly when needed.

______________________________________________________________________

# Install

```bash
pip install flask-sqlalchemy
```

______________________________________________________________________

# Project Structure

```
project/

│

├── app/

│

├── models/

│      user.py

│      product.py

│      order.py

│

├── services/

└── config.py
```

Large applications usually keep models in a dedicated package.

______________________________________________________________________

# Initialize SQLAlchemy

extensions.py

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

Application Factory

```python
from extensions import db

db.init_app(app)
```

______________________________________________________________________

# Database Configuration

```python
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///app.db"
```

Production

```python
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = os.getenv(
    "DATABASE_URL"
)
```

______________________________________________________________________

# Creating a Model

```python
from extensions import db

class User(db.Model):

    __tablename__ = "users"
```

Every model represents one database table.

______________________________________________________________________

# Columns

```python
class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )
```

______________________________________________________________________

# Common Column Types

| Type | Purpose |
|------|----------|
| Integer | Numbers |
| String | Short Text |
| Text | Large Text |
| Boolean | True / False |
| Float | Decimal Values |
| Date | Date |
| DateTime | Timestamp |
| JSON | JSON Data (supported databases) |

______________________________________________________________________

# Primary Key

```python
id = db.Column(

    db.Integer,

    primary_key=True
)
```

Every table should have a primary key.

______________________________________________________________________

# Nullable

```python
email = db.Column(

    db.String(255),

    nullable=False
)
```

Database will reject NULL values.

______________________________________________________________________

# Unique Constraint

```python
email = db.Column(

    db.String(255),

    unique=True
)
```

Useful for

- Email
- Username
- Phone Number

______________________________________________________________________

# Default Value

```python
active = db.Column(

    db.Boolean,

    default=True
)
```

______________________________________________________________________

# Creating Tables

```python
with app.app_context():

    db.create_all()
```

This creates tables that do not already exist.

> **Note:** In production, schema changes should be managed using migrations (covered in the next chapter), not `create_all()`.

______________________________________________________________________

# Insert Data

```python
user = User(

    name="Riyaz"
)

db.session.add(user)

db.session.commit()
```

Flow

```
Object

↓

Session

↓

Commit

↓

Database
```

______________________________________________________________________

# Query All

```python
users = User.query.all()
```

Returns

```
List[User]
```

______________________________________________________________________

# Query First

```python
user = User.query.first()
```

Returns

```
User

or

None
```

______________________________________________________________________

# Query by ID

```python
user = User.query.get(1)
```

> **Note:** In SQLAlchemy 2.x, the preferred approach is:

```python
user = db.session.get(User, 1)
```

______________________________________________________________________

# Filter

```python
user = User.query.filter_by(

    email="a@example.com"

).first()
```

______________________________________________________________________

# Multiple Filters

```python
users = User.query.filter_by(

    active=True

).all()
```

For more complex queries,

the SQLAlchemy expression language can be used.

______________________________________________________________________

# Update

```python
user.name = "Ahmed"

db.session.commit()
```

No explicit UPDATE statement is required.

______________________________________________________________________

# Delete

```python
db.session.delete(user)

db.session.commit()
```

______________________________________________________________________

# Sessions

The Session tracks changes.

```
Object

↓

Modified

↓

Session

↓

Commit

↓

Database
```

Nothing is permanently written until `commit()`.

______________________________________________________________________

# Transactions

Example

```
Insert User

↓

Insert Order

↓

Insert Payment
```

If something fails,

```
Rollback
```

Everything is undone.

______________________________________________________________________

# Rollback

```python
try:

    db.session.commit()

except:

    db.session.rollback()
```

Always rollback after failed transactions before reusing the session.

______________________________________________________________________

# Relationships

Example

```
User

↓

Orders
```

One User

↓

Many Orders

______________________________________________________________________

# One-to-Many

```python
class User(db.Model):

    orders = db.relationship(

        "Order",

        back_populates="user"
    )
```

Order

```python
user_id = db.Column(

    db.Integer,

    db.ForeignKey("users.id")
)
```

______________________________________________________________________

# Foreign Key

```
Orders

↓

user_id

↓

Users.id
```

Maintains referential integrity.

______________________________________________________________________

# Lazy Loading

Default behavior

```
User

↓

Orders

↓

Load When Accessed
```

SQLAlchemy supports multiple loading strategies such as lazy loading, joined loading, and select-in loading.

Choosing the right strategy affects performance.

______________________________________________________________________

# Simple Query

```python
users = User.query.order_by(

    User.name

).all()
```

______________________________________________________________________

# Limit Results

```python
users = User.query.limit(10).all()
```

______________________________________________________________________

# Pagination

```python
page = 1

per_page = 20

users = User.query.paginate(

    page=page,

    per_page=per_page
)
```

Pagination is essential for large datasets.

______________________________________________________________________

# Architecture

```
Route

↓

Service

↓

Repository (Optional)

↓

SQLAlchemy

↓

Database
```

Business logic should not live inside models or route handlers.

______________________________________________________________________

# Common Mistakes

❌ Calling `commit()` after every small operation unnecessarily

❌ Forgetting to rollback after exceptions

❌ Using `create_all()` for production schema changes

❌ Writing business logic inside models

❌ Loading thousands of rows without pagination

❌ Ignoring relationship loading performance

______________________________________________________________________

# Production Best Practices

- Use migrations for schema changes.
- Use transactions for related operations.
- Rollback after failed commits.
- Keep models focused on persistence.
- Keep business logic in services.
- Paginate large queries.
- Add indexes where appropriate.
- Use eager loading strategically to avoid N+1 query problems.

______________________________________________________________________

# Interview Deep Dive

### Question

**Explain how SQLAlchemy manages database operations using sessions and transactions.**

### Answer

SQLAlchemy uses a **Session** as a unit of work.

1. Objects are created or modified in memory.
1. The Session tracks these changes.
1. Calling `commit()` writes all pending changes as a transaction.
1. If an error occurs, `rollback()` reverts the transaction and clears the failed transaction state.

This approach ensures atomicity and keeps related database operations consistent.

______________________________________________________________________

# Summary

In this chapter you learned:

- ORM Concepts
- SQLAlchemy
- Flask-SQLAlchemy
- Models
- Columns
- CRUD Operations
- Sessions
- Transactions
- Relationships
- Querying
- Pagination
- Best Practices

SQLAlchemy provides a powerful abstraction over relational databases while still allowing developers to use SQL when
necessary.

______________________________________________________________________

# Practice Questions

## ORM Basics

1. What is an ORM?
1. Why use SQLAlchemy instead of raw SQL everywhere?
1. What is Flask-SQLAlchemy?

______________________________________________________________________

## Models

4. How does a model map to a database table?
1. What is a primary key?
1. What is a foreign key?
1. Why use `nullable=False`?
1. Why use `unique=True`?

______________________________________________________________________

## CRUD

9. How do you insert a record?
1. How do you update a record?
1. How do you delete a record?
1. How do you query records?

______________________________________________________________________

## Sessions & Transactions

13. What is a SQLAlchemy Session?
01. Why is `commit()` required?
01. When should `rollback()` be used?
01. Why are transactions important?

______________________________________________________________________

## Relationships

17. What is a one-to-many relationship?
01. How does `db.relationship()` differ from `db.ForeignKey()`?
01. What is lazy loading?

______________________________________________________________________

## Scenario-Based

20. Your application creates a user, creates an order, and charges a payment. The payment fails after the user and order are inserted. How should SQLAlchemy transactions handle this?
01. A developer calls `db.create_all()` every time the production application starts. Why is this a poor approach?
01. Your API returns every user in a table containing five million rows. What changes would you make?
01. Your application issues one SQL query for users and then hundreds of additional queries for each user's orders. What ORM performance issue is occurring, and how might you address it?
01. A database commit fails due to a constraint violation. Why should `db.session.rollback()` be called before continuing?

______________________________________________________________________

# Next

[Database Migrations with Alembic & Flask-Migrate](11_migrations_alembic.md)
